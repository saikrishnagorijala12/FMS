from fms.models import Order, OrderItem, Product, Status, Franchisee, Inventory, User
from fms import db
from flask_jwt_extended import get_jwt_identity
from datetime import datetime, UTC
from sqlalchemy import func

def create_order(data):
    customer_id = get_jwt_identity()

    product_items = data.get("items")
    if not product_items or not isinstance(product_items, list):
        return {"message": "Invalid or missing product items"}, 400

    # ✅ Pre-validate all items first
    validated_items = []
    for item in product_items:
        product_id = item.get("product_id")
        quantity = item.get("quantity")

        if not isinstance(product_id, int) or not isinstance(quantity, int) or quantity <= 0:
            return {"message": f"Invalid product_id or quantity in {item}"}, 400

        product = Product.query.get(product_id)
        if not product:
            return {"message": f"Product ID {product_id} not found"}, 404

        validated_items.append((product, quantity))


    pending_status = Status.query.filter_by(status_name='pending').first()
    if not pending_status:
        return {"message": "Pending status not configured"}, 500

    try:
        new_order = Order(
            customer_id=customer_id,
            status_id=pending_status.status_id,
            created_time=datetime.now(UTC)
        )
        db.session.add(new_order)
        db.session.flush()

        for product, quantity in validated_items:
            order_item = OrderItem(
                order_id=new_order.order_id,
                product_id=product.product_id,
                quantity=quantity,
                price=product.price
            )
            db.session.add(order_item)

        db.session.commit()
        return {
            "message": "Order placed successfully",
            "order_id": new_order.order_id,
            "status": pending_status.status_name
        }, 201

    except Exception as e:
        db.session.rollback()
        return {"message": f"Internal server error: {str(e)}"}, 500


def get_orders_by_role(role_name, user_id):
    if role_name == 'customer':
        orders = Order.query.filter_by(customer_id=user_id).order_by(Order.created_time.desc()).all()
    elif role_name == 'admin':
        orders = Order.query.order_by(Order.created_time.desc()).all()
    elif role_name == 'franchisor':
        orders = Order.query.order_by(Order.created_time.desc()).all()
    elif role_name == 'franchisee':
        franchisee = Franchisee.query.filter_by(user_id=user_id).first()
        if not franchisee:
            return {"message": "Franchisee not found"}, 404
        # product_ids this franchisee manages
        product_ids = db.session.query(Inventory.product_id).filter_by(franchisee_id=franchisee.franchisee_id).subquery()
        order_ids = db.session.query(OrderItem.order_id).filter(OrderItem.product_id.in_(product_ids)).distinct().subquery()
        orders = Order.query.filter(Order.order_id.in_(order_ids)).order_by(Order.created_time.desc()).all()
    else:
        return {"message": "Unauthorized or unknown role"}, 403

    output = []
    for o in orders:
        items_str = []
        for item in o.order_item:
            if item.quantity > 1:
                items_str.append(f"{item.product.name} x{item.quantity}")
            else:
                items_str.append(item.product.name)

        output.append({
            # "id": f"ORD-{o.created_time.year}-{o.order_id:03d}",
            "id" : o.order_display_id,
            "date": o.created_time.strftime("%B %d, %Y"),
            "items": ", ".join(items_str),
            "total": float(o.total_amount) if o.total_amount else sum([float(i.price) * i.quantity for i in o.order_item]),
            "location": o.franchisee.franchisee_id if o.franchisee else "",
            "status": o.status.status_name if o.status else ""
        })

    return output, 200


def get_order_by_id(order_id, role_name, user_id):
    order = Order.query.get(order_id)
    if not order:
        return {"message": "Order not found"}, 404

    # Role-based access check
    if role_name == 'customer' and order.user_id != user_id:
        return {"message": "Unauthorized"}, 403

    if role_name == 'franchisee':
        franchisee = Franchisee.query.filter_by(user_id=user_id).first()
        if not franchisee:
            return {"message": "Franchisee not found"}, 404

        # Check if any product in this order belongs to this franchisee
        item_product_ids = [item.product_id for item in order.order_items]
        franchisee_product_ids = db.session.query(Inventory.product_id)\
            .filter_by(franchisee_id=franchisee.franchisee_id).all()
        franchisee_product_ids = [p[0] for p in franchisee_product_ids]

        if not any(pid in franchisee_product_ids for pid in item_product_ids):
            return {"message": "Unauthorized"}, 403

    # Admin and Franchisor have access to all orders

    customer = User.query.get(order.user_id)
    items = OrderItem.query.filter_by(order_id=order.order_id).all()

    order_details = {
        "order_id": order.order_id,
        "customer_name": customer.full_name if customer else "Unknown",
        "status": order.status.status_name,
        "created_time": order.created_time.isoformat(),
        "items": [
            {
                "product_id": item.product_id,
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": item.price
            }
            for item in items
        ]
    }

    return order_details, 200

def update_order_status(order_id, user_id, status_id):
    order = Order.query.get(order_id)
    if not order:
        return {"message": "Order not found"}, 404

    franchisee = Franchisee.query.filter_by(user_id=user_id).first()
    if not franchisee:
        return {"message": "Franchisee not found"}, 404

    franchisee_product_ids = db.session.query(Inventory.product_id).filter_by(franchisee_id=franchisee.franchisee_id).all()
    franchisee_product_ids = [p[0] for p in franchisee_product_ids]

    order_product_ids = [item.product_id for item in order.order_items]
    if not any(pid in franchisee_product_ids for pid in order_product_ids):
        return {"message": "Unauthorized to update this order"}, 403

    order.status_id = status_id
    db.session.commit()
    return {"message": "Order status updated"}, 200


def cancel_order(order_id, user_id):
    order = Order.query.get(order_id)
    if not order or order.user_id != user_id:
        return {"message": "Order not found or unauthorized"}, 404

    canceled_status = Status.query.filter_by(status_name='cancelled').first()
    if not canceled_status:
        return {"message": "Cancel status not configured"}, 500

    order.status_id = canceled_status.status_id
    db.session.commit()
    return {"message": "Order cancelled"}, 200


def get_tracking_info(order_id, role, user_id):
    order = Order.query.get(order_id)
    if not order:
        return {"message": "Order not found"}, 404

    if role == "customer" and order.user_id != user_id:
        return {"message": "Unauthorized"}, 403

    tracking_info = {
        "order_id": order.order_id,
        "status": order.status.status_name,
        "created_time": order.created_time.isoformat(),
    }
    return tracking_info, 200


def add_order_item(order_id, user_id, data):
    product_id = data.get("product_id")
    quantity = data.get("quantity")
    price = data.get("price")

    order = Order.query.get(order_id)
    if not order or order.user_id != user_id:
        return {"message": "Order not found or unauthorized"}, 404

    new_item = OrderItem(
        order_id=order_id,
        product_id=product_id,
        quantity=quantity,
        price=price
    )
    db.session.add(new_item)
    db.session.commit()
    return {"message": "Item added to order"}, 201


def remove_order_item(order_id, item_id, user_id):
    order = Order.query.get(order_id)
    if not order or order.user_id != user_id:
        return {"message": "Order not found or unauthorized"}, 404

    item = OrderItem.query.get(item_id)
    if not item or item.order_id != order_id:
        return {"message": "Item not found in this order"}, 404

    db.session.delete(item)
    db.session.commit()
    return {"message": "Item removed from order"}, 200


def get_order_by_user(user_id):
    franchisee = Franchisee.query.filter_by(user_id=user_id).first()
    if not franchisee:
        return {"message": "Franchisee not found for this user"}, 404
    orders = Order.query.filter_by(franchisee_id=franchisee.franchisee_id).all()

    order_list = []
    for order in orders:
        # Get all order items for each order
        items = []
        for oi in order.order_item:  # thanks to backref in OrderItem
            items.append({
                "product_id": oi.product_id,
                "product_name": oi.product.name,
                "quantity": oi.quantity,
                "price": str(oi.price)  # convert Decimal to str
            })

        order_list.append({
            "id": order.order_id,
            "order_id": order.order_display_id,
            "customer_id": order.customer_id,
            "franchisee_id": order.franchisee_id,
            "total_amount": str(order.total_amount),
            "delivery_address": order.delivery_address,
            "status": order.status.status_name if order.status else None,
            "created_time": order.created_time.isoformat() if order.created_time else None,
            "items": items
        })

    return order_list, 200


def get_product_sales():
    stock_subq = (
        db.session.query(
            Inventory.product_id,
            func.coalesce(func.sum(Inventory.quantity), 0).label('stock')
        )
        .group_by(Inventory.product_id)
        .subquery()
    )

    # Sum sales from OrderItem table
    sales_subq = (
        db.session.query(
            OrderItem.product_id,
            func.coalesce(func.sum(OrderItem.quantity), 0).label('sales')
        )
        .group_by(OrderItem.product_id)
        .subquery()
    )

    # Join with Product
    results = (
        db.session.query(
            Product.product_id,
            Product.name,
            Product.price,
            func.coalesce(stock_subq.c.stock, 0).label('stock'),
            func.coalesce(sales_subq.c.sales, 0).label('sales')
        )
        .outerjoin(stock_subq, stock_subq.c.product_id == Product.product_id)
        .outerjoin(sales_subq, sales_subq.c.product_id == Product.product_id)
        .all()
    )

    # Build JSON response
    data = [
        {
            "name": name,
            "price": float(price),
            "stock": int(stock),
            "sales": int(sales)
        }
        for _, name, price, stock, sales in results
    ]

    return data, 200