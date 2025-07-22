from fms import db
from fms.models.Product import Product
from fms.models.Franchisee import Franchisee

def search_products_service(keyword):
    products = Product.query.filter(
        db.or_(
            Product.name.ilike(f"%{keyword}%"),
            Product.description.ilike(f"%{keyword}%")
        )
    ).all()

    return [{
        'product_id': p.product_id,
        'name': p.name,
        'description': p.description,
        'price': float(p.price),
        'franchisor_id': p.franchisor_id
    } for p in products]


def search_franchises_service(location):
    franchises = Franchisee.query.filter(
        Franchisee.region.ilike(f"%{location}%")
    ).all()

    return [{
        'franchisee_id': f.franchisee_id,
        'region': f.region,
        'franchisor_id': f.franchisor_id,
        'status': f.status.name if f.status else None
    } for f in franchises]
