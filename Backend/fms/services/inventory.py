from flask import  jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity
from fms.models.Inventory import Inventory
from fms.models.User import User
from fms import db
from fms.models.StockRequest import StockRequest
from fms.models.Franchisee import Franchisee
from fms.models.Product import Product
from fms.models.Status import Status
from datetime import datetime, UTC


def get_inventory(user_id):
    franchisee = Franchisee.query.filter_by(user_id=user_id).first()
    if not franchisee:
        return {"message": "Franchisee not found for this user."}, 404

    inventories = Inventory.query.filter_by(franchisee_id=franchisee.franchisee_id).all()
    inventory_data = []

    for item in inventories:
        inventory_data.append({
            "inventory_id": item.inventory_id,
            "product_id": item.product.product_id,
            "product_name": item.product.name,
            "franchisee_id": item.franchisee.franchisee_id,
            "franchisee_name": item.franchisee.user.name,
            "quantity": item.quantity
        })

    return inventory_data, 200


def update_inventory(product_id, data):
    user_id = get_jwt_identity()
    new_quantity = data.get('quantity')
    if new_quantity is None or not isinstance(new_quantity, int) or new_quantity < 0:
        return jsonify({"error": "Invalid quantity"}), 400

    user = User.query.get(user_id)
    if not user or not user.franchisee:
        return {"error": "Franchisee not found for user"}, 404

    franchisee_id = user.franchisee.franchisee_id

    inventory_item = Inventory.query.filter_by(product_id=product_id, franchisee_id=franchisee_id).first()
    if not inventory_item:
        return {"error": "Inventory item not found"}, 404

    inventory_item.quantity = new_quantity
    db.session.commit()

    return {
        "message": "Inventory updated successfully",
        "inventory_id": inventory_item.inventory_id,
        "product_id": product_id,
        "franchisee_id": franchisee_id,
        "new_quantity": inventory_item.quantity
    }, 200


def stock_request(data, ):
    user_id = get_jwt_identity()
    claims = get_jwt()

    if claims.get('role_name') != 'franchisee':
        return {'msg': 'Only franchisees can request stock'}, 403

    product_id = data.get('product_id')
    quantity = data.get('quantity')
    urgency= data.get('urgency')

    if not product_id or not isinstance(quantity, int) or quantity <= 0:
        return {'msg': 'Invalid product_id or quantity'}, 400

    franchisee = Franchisee.query.filter_by(user_id=user_id).first()
    if not franchisee:
        return {'msg': 'Franchisee not found'}, 404

    product = Product.query.get(product_id)
    if not product:
        return {'msg': 'Product not found'}, 404

    pending_status = Status.query.filter_by(status_name='PENDING').first()
    if not pending_status:
        return {'msg': 'PENDING status not configured in system'}, 500

    new_request = StockRequest(
        franchisee_id=franchisee.franchisee_id,
        product_id=product_id,
        quantity=quantity,
        urgency=urgency,
        status_id=pending_status.status_id,
        created_time=datetime.now(UTC)
    )
    db.session.add(new_request)
    db.session.commit()

    return {
        'msg': 'Stock request submitted successfully',
        'request_id': new_request.request_id
    }, 201

# def get_all_stock_requests():
#     stock_requests = StockRequest.query.all()
#     data = []
#
#     for req in stock_requests:
#         data.append({
#             "request_id": req.request_id,
#             "product_id": req.product_id,
#             "product_name": req.product.name,
#             "franchisee_id": req.franchisee_id,
#             "franchisee_name": req.franchisee.franchise_location.name,
#             "quantity": req.quantity,
#             "status_id": req.status_id,
#             "status_name": req.status.status_name,
#             "created_time": req.created_time.isoformat()
#         })
#
#     return data, 200


def get_all_stock_requests():
    stock_requests = StockRequest.query.all()
    data = []

    for req in stock_requests:
        # Get franchise location name (first one if exists)
        location_name = None
        if req.franchisee and req.franchisee.franchise_location:
            if isinstance(req.franchisee.franchise_location, list) and len(req.franchisee.franchise_location) > 0:
                location_name = req.franchisee.franchise_location[0].name
            else:
                # in case of direct scalar relation (but your backref gives a list)
                location_name = req.franchisee.franchise_location.name

        data.append({
            "id": req.request_id,
            # "product_id": req.product_id,
            "product": req.product.name if req.product else None,
            # "franchisee_id": req.franchisee_id,
            "franchise": location_name,
            "quantity": req.quantity,
            # "status_id": req.status_id,
            "status_name": req.status.status_name if req.status else None,
            "urgency":req.urgency
            # "created_time": req.created_time.isoformat() if req.created_time else None
        })

    return data, 200


def approve_stock_request(request_id):
    stock_requests = StockRequest.query.get(request_id)
    if not stock_request:
        return {"message": "Stock request not found"}, 404

    if stock_requests.status.status_name != 'PENDING':
        return {"message": f"Stock request already {stock_requests.status.status_name}"}, 400

    approved_status = Status.query.filter_by(status_name='APPROVED').first()
    if not approved_status:
        return {"message": "APPROVED status not configured in system"}, 500

    stock_request.status_id = approved_status.status_id

    inventory_item = Inventory.query.filter_by(
        franchisee_id=stock_requests.franchisee_id,
        product_id=stock_requests.product_id
    ).first()

    if inventory_item:
        inventory_item.quantity += stock_requests.quantity
    else:
        inventory_item = Inventory(
            franchisee_id=stock_requests.franchisee_id,
            product_id=stock_requests.product_id,
            quantity=stock_requests.quantity
        )
        db.session.add(inventory_item)

    db.session.commit()

    return {
        "message": "Stock request approved and inventory updated",
        "request_id": stock_requests.request_id,
        "product_id": stock_requests.product_id,
        "franchisee_id": stock_requests.franchisee_id,
        "approved_quantity": stock_requests.quantity
    }, 200

def reject_stock_request(request_id):
    stock_requests = StockRequest.query.get(request_id)
    if not stock_request:
        return {"message": "Stock request not found"}, 404

    if stock_requests.status.status_name != 'PENDING':
        return {"message": f"Stock request already {stock_requests.status.status_name}"}, 400

    rejected_status = Status.query.filter_by(status_name='REJECTED').first()
    if not rejected_status:
        return {"message": "REJECTED status not configured in system"}, 500

    stock_request.status_id = rejected_status.status_id
    db.session.commit()

    return {
        "message": "Stock request rejected",
        "request_id": stock_requests.request_id,
        "product_id": stock_requests.product_id,
        "franchisee_id": stock_requests.franchisee_id
    }, 200

def ship_stock_request(request_id):
    stock_requests = StockRequest.query.get(request_id)

    if not stock_request:
        return {"message": "Stock request not found"}, 404

    if stock_requests.status.status_name.lower() != "approved":
        return {"message": "Only approved stock requests can be marked as shipped"}, 400

    shipped_status = Status.query.filter_by(status_name='shipped').first()
    if not shipped_status:
        return {"message": "Shipped status not configured"}, 500

    stock_request.status_id = shipped_status.status_id
    db.session.commit()

    return {
        "message": "Stock request marked as shipped",
        "request_id": request_id,
        "status": "shipped"
    }, 200


def mark_stock_delivered(request_id):
    stock_requests = StockRequest.query.get(request_id)

    if not stock_request:
        return {"message": "Stock request not found"}, 404

    if stock_requests.status.status_name.lower() != "shipped":
        return {"message": "Only shipped stock requests can be marked as delivered"}, 400

    delivered_status = Status.query.filter_by(status_name='delivered').first()
    if not delivered_status:
        return {"message": "Delivered status not configured"}, 500

    stock_request.status_id = delivered_status.status_id
    db.session.commit()

    return {
        "message": "Stock request marked as delivered",
        "request_id": request_id,
        "status": "delivered"
    }, 200
