from fms.models.Franchisee import Franchisee

def browse_categories_service():
    # Stub response since categories are not implemented
    return {
        'message': 'Product categories feature is not implemented in the current system.'
    }

def browse_franchises_service(region=None):
    query = Franchisee.query
    if region:
        query = query.filter(Franchisee.region.ilike(f"%{region}%"))

    franchises = query.all()
    return [{
        'franchisee_id': f.franchisee_id,
        'region': f.region,
        'franchisor_id': f.franchisor_id,
        'status': f.status.name if f.status else None
    } for f in franchises]
