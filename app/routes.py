from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models import Customer, Bill

api_bp = Blueprint('api', __name__)

@api_bp.route('/customers', methods=['POST'])
@jwt_required()
def create_customer():
    data = request.json
    customer = Customer(name=data['name'], phone=data['phone'])
    db.session.add(customer)
    db.session.commit()
    return jsonify(message='Customer created'), 201

@api_bp.route('/customers', methods=['GET'])
@jwt_required()
def get_customers():
    customers = Customer.query.all()
    return jsonify([
        {'id': c.id, 'name': c.name, 'phone': c.phone} for c in customers
    ])