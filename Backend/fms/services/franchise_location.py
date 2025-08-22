from fms import db
from fms.models import  FranchiseLocation

def create_franchise_location(data):
    try:
        new_location = FranchiseLocation(
            franchisee_id=data['franchisee_id'],
            name=data['name'],
            address=data['address'],
            phone=data.get('phone'),
            hours=data.get('hours'),
            services=data.get('services', []),
            city=data.get('city'),
            state=data.get('state'),
            zipcode=data.get('zipcode')
        )

        db.session.add(new_location)
        db.session.commit()

        return {'message': 'Franchise location created successfully.'}, 201

    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500


def fetch_franchise_location():
    locations = FranchiseLocation.query.all()
    result = []
    for loc in locations:
        result.append({
            'location_id': loc.location_id,
            'franchisee_id': loc.franchisee_id,  # ✅ needed for inventory
            'franchisee_user_id': loc.franchisee.user_id if loc.franchisee else None,
            # ✅ direct link to /inventory/{user_id}
            'name': loc.name,
            'address': loc.address,
            'phone': loc.phone,
            'hours': loc.hours,
            'services': loc.services,
            'city': loc.city,
            'state': loc.state,
            'zipcode': loc.zipcode,
        })
    return result, 200


def update_franchise_location(data, location_id):
    location = FranchiseLocation.query.get(location_id)

    if not location:
        return {'error': 'Location not found'}, 404

    # update fields if present
    location.name = data.get('name', location.name)
    location.address = data.get('address', location.address)
    location.phone = data.get('phone', location.phone)
    location.hours = data.get('hours', location.hours)
    location.services = data.get('services', location.services)
    location.city = data.get('city', location.city)
    location.state = data.get('state', location.state)
    location.zipcode = data.get('zipcode', location.zipcode)

    db.session.commit()
    return {'message': 'Location updated successfully'}, 200


def delete_franchise_location(location_id):
    location = FranchiseLocation.query.get(location_id)
    if not location:
        return {'error': 'Location not found'}, 404

    db.session.delete(location)
    db.session.commit()
    return {'message': 'Location deleted successfully'}, 200