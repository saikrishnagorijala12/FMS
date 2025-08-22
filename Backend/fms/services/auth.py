import fms as utils
from fms import jwt_blacklist,jwt
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from fms import db,mail
from fms.models.User import User
from flask_mail import Message

def create_user(data):
    if User.query.filter_by(email=data['email']).first():
        return {'error': 'Email already exists'}, 409
    user = User(
        # user_id=data['user-id'],
        name=data['name'],
        email=data['email'],
        password=generate_password_hash(data['password']),
        phone_no=data['phone_no'],
        role_id=data['role_id']
    )
    db.session.add(user)
    db.session.commit()

    return {'message': 'User created successfully'}, 201


def login_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return {'error': 'Invalid credentials'}, 401

    token = utils.generate_access_token(user)

    return {'access_token': token}, 200

def refresh_status(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
         return {'error': 'Invalid credentials'}, 401
    token = utils.refresh_access_token(user)

    return {'new_access_token': token}, 200

def logout_user():
    jti = get_jwt()["jti"]  # unique token ID
    jwt_blacklist.add(jti)
    return {"}Successfully logged out"}, 200


def forgot_user(data):
    email = data.get("email")

    if not email:
        return {"success": False, "message": "Email is required"}, 400

    # Check if user exists in DB
    user = User.query.filter_by(email=email).first()
    if not user:
        return {"success": False, "message": "Email not found.\n Please Check again."}, 404

    # Send email with reset link (dummy link for now)
    token = utils.generate_access_token(user)  # generate JWT or uuid instead
    reset_link = f"http://localhost:4200/reset-password/{token}"

    try:
        msg = Message("🔐 Reset Your Password", recipients=[email])

        # HTML template with inline CSS (Bootstrap-like card)
        msg.html = f"""
            <div style="font-family: Arial, sans-serif; background-color:#f4f4f4; padding:20px;">
              <div style="max-width:500px; margin:auto; background:#ffffff; border-radius:8px;
                          box-shadow:0 2px 6px rgba(0,0,0,0.1); padding:20px; text-align:center;">

                <h2 style="color:#333;">Password Reset Request</h2>
                <p style="color:#555; font-size:15px;">
                  Hi <b>{user.name}</b>,<br><br>
                  We received a request to reset your password. 
                  Click the button below to set a new password:
                </p>

                <a href="{reset_link}" style="display:inline-block; margin:20px 0;
                  padding:12px 20px; font-size:16px; color:white; background-color:#007bff;
                  border-radius:6px; text-decoration:none;">
                  Reset Password
                </a>

                <p style="color:#999; font-size:12px; margin-top:15px;">
                  If you didn’t request this, you can safely ignore this email.<br>
                  This link will expire in 30 minutes.
                </p>
              </div>
            </div>
            """

        mail.send(msg)

        return {"success": True, "message": "Reset email sent successfully"}, 200

    except Exception as e:
        return {"success": False, "message": str(e)}, 500