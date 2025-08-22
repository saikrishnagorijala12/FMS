from flask import jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from fms import db
from fms.models import FranchiseApplication, FranchiseLocation
from fms.models.User import User
from fms.models.Franchisee import Franchisee
from fms.models.Franchisor import Franchisor
from fms.models.Status import Status


def apply_franchise(data):
    user_id = get_jwt_identity()
    if not data:
        return {'error': 'No data provided'}, 400

    region = data.get("region")
    franchisor_id = data.get("franchisor_id")
    location = data.get("location", {})

    if not region or not franchisor_id:
        return {"error": "region and franchisor_id are required"}, 400

    # Check if user already applied or is a franchisee
    if Franchisee.query.filter_by(user_id=user_id).first():
        return {"error": "User has already applied or is a franchisee"}, 400

    # Validate franchisor exists
    franchisor = Franchisor.query.get(franchisor_id)
    if not franchisor:
        return {"error": "Franchisor not found"}, 404

    # Get 'pending' status ID
    pending_status = Status.query.filter_by(status_name='pending').first()
    if not pending_status:
        return {"error": "Status 'pending' not found in database"}, 500

    try:
        # Create franchisee entry
        franchisee = Franchisee(
            user_id=user_id,
            franchisor_id=franchisor_id,
            region=region,
            status=pending_status.status_id
        )
        db.session.add(franchisee)
        db.session.flush()  # Get franchisee_id before commit

        # Create franchise application record
        application = FranchiseApplication(
            franchisee_id=franchisee.franchisee_id,
            franchisor_id=franchisor_id,
            region=region,
            status=pending_status.status_id
        )
        db.session.add(application)

        # Optional location
        if location and location.get("address"):
            franchise_location = FranchiseLocation(
                franchisee_id=franchisee.franchisee_id,
                address=location.get("address"),
                city=location.get("city"),
                state=location.get("state"),
                zipcode=location.get("zipcode")
            )
            db.session.add(franchise_location)

        db.session.commit()
        return {"message": "Franchise application submitted successfully."}, 201

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def get_applications():
    applications = Franchisee.query.filter(Franchisee.status.has(Status.status_name == 'pending')).all()
    data = [{
        "franchisee_id": f.franchisee_id,
        "user_name": f.user.full_name,
        "region": f.region,
        "status": f.status.status_name
    } for f in applications]
    return jsonify(data), 200

def update_application_status(application_id, approved):
    franchisee = Franchisee.query.get(application_id)
    if not franchisee:
        return jsonify({"msg": "Application not found"}), 404

    status_name = 'approved' if approved else 'rejected'
    status = Status.query.filter_by(status_name=status_name).first()
    if not status:
        return jsonify({"msg": f"{status_name.capitalize()} status not found"}), 400

    franchisee.status_id = status.status_id
    db.session.commit()
    return jsonify({"msg": f"Application {status_name}"}), 200

def get_all_franchises():
    franchises = FranchiseApplication.query.all()
    data = [{
        "id": app.application_display_id,
        "aid":app.application_id,
        "applicant": app.franchisee.user.name,  # assuming Franchisee has relationship to User as `user`
        "region": app.region,
        "investment": float(app.investment) if app.investment is not None else None,
        "experience": app.experience,
        "status": app.status.status_name
    } for app in franchises]
    return jsonify(data), 200

def get_franchise_by_id(franchise_id):
    f = Franchisee.query.get(franchise_id)
    if not f:
        return jsonify({"msg": "Franchise not found"}), 404
    data = {
        "franchisee_id": f.franchisee_id,
        "user_name": f.user.full_name,
        "region": f.region,
        "status": f.status.status_name
    }
    return jsonify(data), 200

def update_franchise(franchise_id, data):
    f = Franchisee.query.get(franchise_id)
    if not f:
        return jsonify({"msg": "Franchise not found"}), 404
    f.region = data.get("region", f.region)
    db.session.commit()
    return jsonify({"msg": "Franchise updated"}), 200

def update_status(application_id, data):
    new_status_id = data.get('status_id')  # directly sent as integer

    if new_status_id is None:
        return {"error": "Missing status_id"}, 400

    application = FranchiseApplication.query.filter_by(application_id=application_id).first()
    if not application:
        return {"error": "Application not found"}, 404

        # Optional: validate that the status_id exists
        # status_record = Status.query.get(new_status_id)
        # if not status_record:
        #     return jsonify({"error": "Invalid status_id"}), 400

    application.status_id = new_status_id
    db.session.commit()

    return {"message": f"Application {application_id} updated successfully", "status_id": new_status_id}, 200

def get_franchise_by_user(user_id):
    f = Franchisee.query.filter_by(user_id=user_id).first()
    if not f:
        return jsonify({"msg": "Franchise not found"}), 404
    data = {
        "franchisee_id": f.franchisee_id,
        "region": f.region,
        "status": f.status.status_name
    }
    return jsonify(data), 200