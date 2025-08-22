from flask_jwt_extended import get_jwt_identity

from fms.models import Franchisor
from fms.models.Product import Product
from fms.models.Stock import Stock
from fms import db
from datetime import datetime, UTC


def get_products_list(user_id):
    try:
        franchisor = Franchisor.query.filter_by(user_id=user_id).first()
        if not franchisor:
            return {"message": "Franchisor not found for this user."}, 404

        franchisor_id = franchisor.franchisor_id
        # Get all products belonging to franchisor_id
        products = Product.query.filter_by(franchisor_id=franchisor_id).all()
        if not products:
            return {"message": "No products found for this franchisor."}, 404

        # For each product, get stock quantity
        product_list = []
        for product in products:
            stock_entry = Stock.query.filter_by(product_id=product.product_id, franchisor_id=franchisor_id).first()
            product_list.append({
                "product_id": product.product_id,
                # "franchisor_id": franchisor_id,
                "name": product.name,
                "description": product.description,
                "price": float(product.price),
                "category": product.category,
                # "rating": product.rating,
                # "reviews": product.reviews,
                "stock_quantity": stock_entry.quantity if stock_entry else 0
            })

        return {"products": product_list}, 200

    except Exception as e:
        db.session.rollback()
        return {"message": "Error fetching products.", "error": str(e)}, 500


def add_new_product(data):
    try:
        user_id = data.get('user_id')
        franchisor = Franchisor.query.filter_by(user_id=user_id).first()

        if not franchisor:
            return {"message": "Franchisor not found for this user."}, 404

        franchisor_id = franchisor.franchisor_id

        # Extract product details
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        category = data.get('category')
        initial_stock = data.get('stock', 0)

        # Validate required fields
        if not franchisor_id or not name or price is None:
            return {"message": "Missing required fields"}, 400

        # 1️⃣ Create the product
        new_product = Product(
            franchisor_id=franchisor_id,
            name=name,
            description=description,
            price=price,
            category=category
        )
        db.session.add(new_product)
        db.session.flush()  # Get product_id before commit

        # 2️⃣ Create the stock record for that product
        new_stock = Stock(
            product_id=new_product.product_id,
            franchisor_id=franchisor_id,
            quantity=initial_stock
        )
        db.session.add(new_stock)
        db.session.commit()

        return {
            "message": "Product added successfully",
            "product": {
                "product_id": new_product.product_id,
                "name": new_product.name,
                "price": float(new_product.price),
                "category": new_product.category,
                "description": new_product.description,
                "franchisor_id": new_product.franchisor_id,
                "initial_stock": new_stock.quantity
            }
        }, 201

    except Exception as e:
        db.session.rollback()
        return {"message": f"Error adding product: {str(e)}"}, 500


def update_product(data, product_id):
    user_id = get_jwt_identity()
    franchisor = Franchisor.query.filter_by(user_id=user_id).first()
    if not franchisor:
        return {"message": "Franchisor not found for this user."}, 404

    new_stock = data.get('updateStock')
    if not new_stock or new_stock <1:
         return {"message": "Stock to be update is not Available"}, 404

    stock = Stock.query.filter_by(product_id=product_id).first()
    if not stock:
        return {'error': 'Product not found'}, 404

    stock.quantity = new_stock
    db.session.commit()

    return {'message': 'Stock updated successfully',
            "_id " : user_id,
            'product_id': product_id,
            'new_stock': stock.quantity}, 200


def update_price(data, product_id):
    user_id = get_jwt_identity()
    franchisor = Franchisor.query.filter_by(user_id=user_id).first()
    if not franchisor:
        return {"message": "Franchisor not found for this user."}, 404

    new_product = data.get('new_price')
    if not new_product or new_product < 1:
        return {"message": "Price to be update is not Available"}, 404

    product = Product.query.filter_by(product_id=product_id).first()
    if not product:
        return {'error': 'Product not found'}, 404

    product.price = new_product
    db.session.commit()

    return {'message': 'Stock updated successfully',
            "_id ": user_id,
            'product_id': product_id,
            'new_price': product.price}, 200


def deleteProduct(product_id):
    user_id = get_jwt_identity()
    franchisor = Franchisor.query.filter_by(user_id=user_id).first()
    if not franchisor:
        return {"message": "Franchisor not found for this user."}, 404

    product = Product.query.filter_by(product_id=product_id, franchisor_id=franchisor.franchisor_id).first()
    if not product:
        return {"message": "Product not found"}, 404
    stock_items = Stock.query.filter_by(product_id=product_id).all()
    for stock in stock_items:
        db.session.delete(stock)

    db.session.delete(product)
    db.session.commit()

    return {
        "message": "Product deleted successfully",
        "product_id": product_id
    }, 200