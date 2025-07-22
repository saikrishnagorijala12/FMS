from decimal import Decimal
from fms import db
from flask_jwt_extended import get_jwt_identity
from fms.models import  Product, Franchisor, User
from fms.utils import role_required



def new_product(data):
    user_id = get_jwt_identity()

    required_fields = ['name', 'price', 'stock']
    if not all(field in data for field in required_fields):
        return {'msg': 'Missing required fields'}, 400

    franchisor = Franchisor.query.filter_by(user_id=user_id).first()
    if not franchisor:
        return {'msg': 'Franchisor profile not found'}, 404

    product = Product(
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        stock=data['stock'],
        # category=data.get('category'),
        franchisor_id=franchisor.id
    )

    db.session.add(product)
    db.session.commit()

    return {'msg': 'Product created successfully', 'product_id': product.id}, 201


def list_products():
    products = Product.query.all()

    product_list = []
    for p in products:
        product_list.append({
            "id": p.product_id,
            "name": p.name,
            "description": p.description,
            "price": float(p.price),
            "rating": p.rating,
            "reviews": p.reviews,
            "category": p.category
        })

    return {'products': product_list}, 200


def get_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        return {'error': 'Product not found'}, 404

    product_data = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock,
        # 'category': product.category,
        'franchisor_id': product.franchisor_id
    }

    return {'product': product_data}, 200


def update_product(data, product_id):
    product = Product.query.get(product_id)
    if not product:
        return {"error": "Product not found"}, 404

    try:
        if "name" in data:
            product.name = data["name"]

        if "description" in data:
            product.description = data["description"]

        if "price" in data:
            try:
                product.price = Decimal(data["price"])
            except Exception as e:
                return {"error": "Invalid price format"}, 400

        db.session.commit()
        return {"message": "Product updated successfully"}, 200

    except Exception as e:
        db.session.rollback()
        return {"error": f"Update failed: {str(e)}"}, 500


def delete_product(product_id):
    db.session.delete(product_id)
    db.session.commit()

    return {"message": f"Product {product_id} deleted successfully."}, 200