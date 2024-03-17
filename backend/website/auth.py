from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from . import db
from .models import User, Balance,Unit,Transaction,Teller
import os
import qrcode
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_mail import Message, Mail
from itsdangerous import Serializer,BadSignature, SignatureExpired
import re
from re import match
from flask_jwt_extended import get_jwt_identity, unset_jwt_cookies
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from flask import jsonify, request
from flask import send_from_directory
from . import socketio
from datetime import datetime, date, timedelta
import json
from calendar import monthcalendar, THURSDAY
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, current_app
from flask_login import login_required, current_user
from .models import User, Balance, Transaction, Unit
from . import db
from datetime import datetime, date, timedelta
import json
from calendar import monthcalendar, THURSDAY

import calendar
from sqlalchemy import extract
from datetime import datetime, date
from calendar import monthcalendar
from sqlalchemy.exc import SQLAlchemyError
import os
from flask_wtf import csrf
from flask_wtf.csrf import generate_csrf
import qrcode
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import get_jwt_identity, unset_jwt_cookies
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
import calendar
from sqlalchemy import extract
from datetime import datetime, date
from calendar import monthcalendar
auth = Blueprint('auth', __name__)

mail = Mail


def get_updated_balance(unit_id):
    # Query the Balance model for the specified unit_id and get the latest balance
    balance = Balance.query.filter_by(unit_id=unit_id).order_by(Balance.id.desc()).first()
    if balance:
        return balance.balance
    else:
        return None
    
@auth.route('/update_balance/<int:unit_id>', methods=['POST'])
def update_balance(unit_id):
    # Update the balance for the unit
    # Assuming you have a function to retrieve the updated balance
    balance = get_updated_balance(unit_id)

    # Broadcast the updated balance to all clients
   

    return 'Balance updated successfully'
@auth.route('/check_email/<email>', methods=['GET'])
def check_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False})
    
@auth.route('/check_unit/<unit_info>', methods=['GET'])
def check_unit(unit_info):
    unit = Unit.query.filter_by(unit_info=unit_info).first()
    if unit:
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False})  
    
@auth.route('/check_unit/<username>', methods=['GET'])
def check_operator(username):
    teller = Teller.query.filter_by(username=username).first()
    if teller:
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False})       

@auth.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'permit':user.permit,
        'address':user.address,
        'license':user.license,
    }), 200 

@auth.route('/static/permit/<path:filename>')
def serve_permit(filename):
    return send_from_directory('C:\\Users\\Maverick\\Desktop\\capstone\\backend\\website\\static\\permit', filename)

@auth.route('/Teller', methods=['GET'])
@jwt_required()
def get_Teller():
    Teller_id = get_jwt_identity()
    teller = Teller.query.get(Teller_id)
    if not teller:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({
        'id': teller.id,
        'username': teller.username,
        'first_name': teller.first_name,
        'last_name': teller.last_name
    }), 200 

@auth.route('/unitdetails', methods=['GET'])
@jwt_required()
def get_unit():
    unit_id = get_jwt_identity()
    unit = Unit.query.get(unit_id)
    if not unit:
        return jsonify({'message': 'unit not found'}), 404

    return jsonify({
        'id': unit.id,
        'unit_info': unit.unit_info,
        'qrcode':unit.qrcode,
       
    }), 200 

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Missing JSON data'}), 400

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    # Generate access token
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200


@auth.route('/loginTeller', methods=['POST'])
def loginTeller():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Missing JSON data'}), 400

    username = data.get('username')
    password = data.get('password')

    teller = Teller.query.filter_by(username=username).first()
    if not teller or not check_password_hash(teller.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    # Generate access token
    access_token = create_access_token(identity=teller.id)
    return jsonify({'access_token': access_token}), 200


@auth.route('/loginunit', methods=['POST'])
def loginunit():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Missing JSON data'}), 400

    unit = data.get('unit')
    password = data.get('password')

    unit = Unit.query.filter_by(unit_info=unit).first()
    if not unit or not check_password_hash(unit.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    # Generate access token
    access_token = create_access_token(identity=unit.id)
    return jsonify({'access_token': access_token}), 200



@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    current_user_id = get_jwt_identity()
    logout_user()
    unset_jwt_cookies()
    return jsonify(message='Logout successful'), 200

@auth.route('/addTeller', methods=['POST'])
def addTeller():
    if request.method == 'POST':
        username = request.form.get('username')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        address = request.form.get('address')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        teller = Teller.query.filter_by(username=username).first()
        if teller:
                flash('username already exists.', category='error')
        elif len(first_name) < 2:
                flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
                flash('Last name must be greater than 1 character.', category='error')
        elif len(address) < 2:
                flash('Address must be greater than 1 character.', category='error')
        elif password1 != password2:
                flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
                flash('Password must be at least 7 characters.', category='error')
        else:
               

                # Create new user
                new_user = Teller(username=username, first_name=first_name, last_name=last_name,
                                address=address, password=generate_password_hash(password1, method='pbkdf2:sha256'),
                               )

                db.session.add(new_user)
                db.session.commit()

        return jsonify({'message': 'Account created successfully'}), 200

@auth.route('/signup', methods=['POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        address = request.form.get('address')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        license = request.form.get('license')
        permit = request.files['permit'] if 'permit' in request.files else None

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email address.', category='error')
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already exists.', category='error')
            elif len(first_name) < 2:
                flash('First name must be greater than 1 character.', category='error')
            elif len(last_name) < 2:
                flash('Last name must be greater than 1 character.', category='error')
            elif len(address) < 2:
                flash('Address must be greater than 1 character.', category='error')
            elif password1 != password2:
                flash('Passwords don\'t match.', category='error')
            elif len(password1) < 7:
                flash('Password must be at least 7 characters.', category='error')
            else:
                if permit:
                    permit_filename = secure_filename(email + '.png')
                    permit_path = os.path.join(current_app.root_path, 'static', 'permit', permit_filename)
                    os.makedirs(os.path.dirname(permit_path), exist_ok=True)
                    permit.save(permit_path)
                else:
                    permit_filename = 'default_permit.png'  # Set a default permit filename if no permit is provided

                # Create new user
                new_user = User(email=email, first_name=first_name, last_name=last_name,
                                address=address, password=generate_password_hash(password1, method='pbkdf2:sha256'),
                                license=license, permit=permit_filename)

                db.session.add(new_user)
                db.session.commit()

    return jsonify({'message': 'Account created successfully'}), 200





@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = generate_token(user.email)
            send_reset_email(user.email, token)
            flash('An email with instructions to reset your password has been sent.', 'info')
            return redirect(url_for('auth.login'))
        else:
            flash('Email address not found.', 'error')
    return render_template('forgot.html',user=None)

def generate_token(email):
    s = Serializer(current_app.config['SECRET_KEY'])
    token = s.dumps({'email': email})  
    return token


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
        email = data['email']
        user = User.query.filter_by(email=email).first()
        if request.method == 'POST':
            new_password = request.form.get('password')
            hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been reset. You can now log in with your new password.', 'success')
            return redirect(url_for('auth.login'))
    except:
        flash('The reset link is invalid or has expired. Please try again.', 'error')
        return redirect(url_for('auth.forgot_password'))
    return render_template('reset_password.html')


def send_reset_email(email, token):
    reset_link = url_for('auth.reset_password', token=token, _external=True)

    
def send_reset_email(email, token):
    reset_link = url_for('auth.reset_password', token=token, _external=True)
    msg = Message('Password Reset Request', sender='renzoofama@gmail.com', recipients=[email])
    msg.body = f'''To reset your password, visit the following link:
{reset_link}
If you did not make this request, simply ignore this email and no changes will be made.
'''
    mail.send(msg)










@auth.route('/units', methods=['GET'])
@jwt_required()
def get_all_units():
    units = Unit.query.all()

    units_data = []
    for unit in units:
        unit_data = {
            'id': unit.id,
            'unit_info': unit.unit_info,
            'unit_type': unit.unit_type,
            'qrcode': unit.qrcode,
            'color': unit.color
        }
        units_data.append(unit_data)

    return jsonify({'units': units_data}), 200

@auth.route('/user/units', methods=['GET'])
@jwt_required()
def get_user_units():
    # Get the current user's ID from the JWT token
    current_user_id = get_jwt_identity()

    # Query the database for units belonging to the current user
    units = Unit.query.filter_by(user_id=current_user_id).all()

    # Create a list of unit data to return
    units_data = []
    for unit in units:
        unit_data = {
            'id': unit.id,
            'unit_info': unit.unit_info,
            'unit_type': unit.unit_type,
            'qrcode': unit.qrcode,
            'color': unit.color
        }
        units_data.append(unit_data)

    return jsonify({'units': units_data}), 200


@auth.route('/transactions', methods=['GET'])
def get_all_transactions():
    transactions = Transaction.query.all()
    transaction_list = []
    for transaction in transactions:
        transaction_list.append({
            'id': transaction.id,
            
            # Add more fields as needed
        })
    return jsonify({'transactions': transaction_list})


@auth.route('/unit/<int:unit_id>/balances', methods=['GET'])
@jwt_required()
def get_unit_balances(unit_id):
    unit = Unit.query.get(unit_id)
    if not unit:
        return jsonify({'message': 'Unit not found'}), 404

    balances = Balance.query.filter_by(unit_id=unit_id).all()

    balances_data = []
    for balance in balances:
        balance_data = {
            'id': balance.id,
            'balance': balance.balance
        }
        balances_data.append(balance_data)

    return jsonify({'balances': balances_data}), 200

@auth.route('/unit/<int:unit_id>/transactions', methods=['GET'])
@jwt_required()
def get_unit_transactions(unit_id):
    unit = Unit.query.get(unit_id)
    if not unit or unit.user_id != current_user.id:
        return jsonify({'message': 'Unit not found or unauthorized'}), 404

    transactions = Transaction.query.filter_by(unit_id=unit_id).all()

    transactions_data = []
    for transaction in transactions:
        transaction_data = {
            'id': transaction.id,
            'amount': transaction.amount,
            'date': transaction.date,
            'branch': transaction.branch,
            'date_of_payment': transaction.date_of_payment,
            'type': transaction.type
        }
        transactions_data.append(transaction_data)

    return jsonify({'transactions': transactions_data}), 200



@auth.route('/updateuser', methods=['PUT'])
def update_user():
    # Check if user is logged in
    access_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not access_token:
        return jsonify({'message': 'Unauthorized access'}), 401
    
    # Validate the access token (you may need to implement this)
   

    # Get user data from request
    user_data = request.form
    email = user_data.get('email')
    first_name = user_data.get('first_name')
    last_name = user_data.get('last_name')
    address = user_data.get('address')
    license = user_data.get('license')
    password = user_data.get('password')
    permit = request.files.get('permit')

    # Update user information in the database
    # Assuming you have a User model with these attributes
    user = User.query.filter_by(email=email).first()
    if user:
        user.first_name = first_name
        user.last_name = last_name
        user.address = address
        user.license = license
        if password:
            user.set_password(password)  # Assuming set_password hashes the password
        if permit:
            # Handle permit file upload
            if user.permit:
                # Remove existing permit file
                existing_permit_path = os.path.join(current_app.root_path, 'static', 'permit', user.permit)
                if os.path.exists(existing_permit_path):
                    os.remove(existing_permit_path)

            # Save new permit file
            permit_filename = secure_filename(user.email + '_permit.png')  # Unique filename
            permit_path = os.path.join(current_app.root_path, 'static', 'permit', permit_filename)
            permit.save(permit_path)
            user.permit = permit_filename

        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404



    
@auth.route('/static/qrcodes/<path:filename>')
def serve_qrcode(filename):
    return send_from_directory('C:\\Users\\Maverick\\Desktop\\capstone\\backend\\website\\static\\qrcodes', filename)

@auth.route('/addunit', methods=['POST'])
@jwt_required()
def addunit():
    unit_info = request.form.get('unitinfo')
    unit_type = request.form.get('unittype')
    color = request.form.get('color')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    user_id = get_jwt_identity()
    if password1 != password2:
                flash('Passwords don\'t match.', category='error')
    elif len(password1) < 7:
                flash('Password must be at least 7 characters.', category='error')
 
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(unit_info)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
        
    qr_code_dir = os.path.join(current_app.root_path, 'static', 'qrcodes')
    os.makedirs(qr_code_dir, exist_ok=True)
    qr_code_filename = f'{unit_info}_qrcode.png'
    qr_code_path = os.path.join(qr_code_dir, qr_code_filename)
    img.save(qr_code_path)
        
    new_unit = Unit(unit_info=unit_info, unit_type=unit_type, qrcode=qr_code_filename, color=color, user_id=user_id,password=generate_password_hash(password1, method='pbkdf2:sha256'))
    db.session.add(new_unit)
    db.session.commit()
        
    
    new_balance = Balance(balance=0, unit=new_unit)
    db.session.add(new_balance)
    db.session.commit()

    return jsonify({'message': 'Unit added successfully'}), 200


@auth.route('/topup', methods=['POST'])
@jwt_required()
def topup():
    data = request.json
    amt = data.get('amount')
    unit_id = data.get('selectedUnit')
    branch = data.get('selectedBranch')
    teller_id = data.get('teller')
    teller = Teller.query.get(teller_id)


    unit = Unit.query.get(unit_id)

    if not unit:
            return jsonify({'message': 'Unit not found!'}), 400

    balance_entry = Balance.query.filter_by(unit_id=unit_id).first()

    if not balance_entry:
            balance_entry = Balance(unit_id=unit_id, balance=0)

    
    balance_entry.balance += int(amt)

   
    transaction = Transaction(amount=int(amt), unit=unit, branch=branch, balance=balance_entry, type='TOPUP',teller=teller)

   
    db.session.add(balance_entry)
    db.session.add(transaction)
    db.session.commit()
    print("Balance updated, emitting balance_update event...")  
    socketio.emit('balance_update', {'unit_id': unit_id, 'new_balance': balance_entry.balance}, namespace='/')

    # flash('Balance added!', category='success')

    return jsonify({'message': 'Top up successful!'}), 200


from random import choice
@auth.route('/api/message', methods=['GET'])
def get_message():
    messages = ["Hello from the backend!", "Welcome to the backend!", "Backend message here!"]
    message = choice(messages)
    return jsonify({'message': message})




@auth.route('/deduct', methods=['POST'])
def deduct():
    data = request.json
    unit_id = data.get('unit_id')
    date = data.get('date')
    amt = data.get('amount')
    branch = data.get('selectedBranch')
    teller_id = data.get('teller')
    unit = Unit.query.get(unit_id)
    teller = Teller.query.get(teller_id)

    if not unit:
        return jsonify({'message': 'Unit not found'}), 404

        

    payment_date_str = date
    if not payment_date_str:
        return jsonify({'error': 'Payment date is required'}), 400

    try:
        payment_date = datetime.strptime(payment_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    today = datetime.now().date()
    if payment_date > today:
        return jsonify({'error': 'Cannot process payment for future dates'}), 400

    balance_entry = Balance.query.filter_by(unit_id=unit_id).first()
    if not balance_entry:
        return jsonify({'error': 'No balance entry found'}), 404

    if balance_entry.balance < amt:
        return jsonify({'error': 'Insufficient balance'}), 400

    existing_transaction = Transaction.query.filter_by(unit_id=unit_id, date=payment_date).first()
    if existing_transaction:
        return jsonify({'error': 'Deduction already made for {}'.format(payment_date)}), 400 

    balance_entry.balance -= amt

    transaction = Transaction(amount=amt, unit_id=unit_id, balance_id=balance_entry.id, type='PAYMENT', date=payment_date, date_of_payment=today,branch=branch,teller=teller)

    db.session.add(transaction)
    db.session.commit()

    return jsonify({'message': 'Balance deducted successfully'}), 200