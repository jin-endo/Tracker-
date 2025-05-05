from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import db, bcrypt
from models import User, Transaction
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['first_name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('views.register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered!')
            return redirect(url_for('views.register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(email=email, first_name=first_name, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! Please log in.')
        return redirect(url_for('views.login'))
    return render_template('register.html')

@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('views.dashboard'))
        else:
            flash('Invalid login credentials.')
            return redirect(url_for('views.login'))
    return render_template('login.html')

@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@views.route('/dashboard')
@login_required
def dashboard():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    income = sum(t.amount for t in transactions if t.type == 'income')
    expenses = sum(t.amount for t in transactions if t.type == 'expense')
    balance = income - expenses
    return render_template('dashboard.html', transactions=transactions, income=income, expenses=expenses, balance=balance)

@views.route('/add-transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    if request.method == 'POST':
        category = request.form['category']
        amount = float(request.form['amount'])
        trans_type = request.form['type']
        new_trans = Transaction(
            category=category,
            amount=amount,
            type=trans_type,
            user_id=current_user.id
            # ✅ date will auto-fill from model default
        )
        db.session.add(new_trans)
        db.session.commit()
        flash('Transaction added!')
        return redirect(url_for('views.dashboard'))
    return render_template('add_transaction.html')

@views.route('/edit-transaction/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(id):
    trans = Transaction.query.get_or_404(id)
    if trans.user_id != current_user.id:
        flash('Unauthorized access.')
        return redirect(url_for('views.dashboard'))

    if request.method == 'POST':
        trans.category = request.form['category']
        trans.amount = float(request.form['amount'])
        trans.type = request.form['type']
        db.session.commit()
        flash('Transaction updated!')
        return redirect(url_for('views.dashboard'))

    return render_template('edit_transaction.html', transaction=trans)
