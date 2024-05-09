from datetime import datetime
from flask import Flask, jsonify, session, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lego_marvel_thor'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


loggedInUser = {}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    creds = db.Column(db.Integer, default=40)
    isClient = db.Column(db.Boolean, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'creds': self.creds,
            'isClient': self.isClient,
            'createdAt': self.createdAt.isoformat()
        }


class MarketplaceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isHourly = db.Column(db.Boolean, nullable=False)
    minCreds = db.Column(db.Integer, nullable=False)
    maxCreds = db.Column(db.Integer, nullable=False)
    isHired = db.Column(db.Boolean, default=False)
    hiredByUserId = db.Column(db.Integer, db.ForeignKey('user.id'))
    hiredUserId = db.Column(db.Integer, db.ForeignKey('user.id'), default=None)
    user = db.relationship(
        'User', backref='marketplace_items', foreign_keys=[hiredByUserId, hiredByUserId])
    isPaid = db.Column(db.Boolean, default=False)
    isCompleted = db.Column(db.Boolean, default=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'isHourly': self.isHourly,
            'minCreds': self.minCreds,
            'maxCreds': self.maxCreds,
            'isHired': self.isHired,
            'hiredByUserId': self.user.to_dict(),
            'hiredUserId': self.hiredUserId,
            'isPaid': self.isPaid,
            'isCompleted': self.isCompleted,
            'createdAt': self.createdAt.isoformat()
        }


class Proposal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marketplaceItemId = db.Column(db.Integer, db.ForeignKey(
        'marketplace_item.id'), nullable=False)
    marketplaceItem = db.relationship('MarketplaceItem', backref='proposals')
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='proposals')
    proposalText = db.Column(db.String(512), nullable=False)
    isAccepted = db.Column(db.Boolean, default=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


with app.app_context():
    db.create_all()


def getActiveContracts(userId):
    user = User.query.filter_by(id=userId).first()

    if not user:
        return jsonify(message="User not found!"), 404

    activeContractsCount = None

    if user.isClient:
        activeContractsCount = MarketplaceItem.query.filter_by(
            hiredByUserId=userId, isCompleted=False).count()
    else:
        activeContractsCount = MarketplaceItem.query.filter_by(
            hiredUserId=userId, isCompleted=False).count()

    return activeContractsCount


def getCompletedContracts(userId):
    user = User.query.filter_by(id=userId).first()

    if not user:
        return jsonify(message="User not found!"), 404

    completedContractsCount = None

    if user.isClient:
        completedContractsCount = MarketplaceItem.query.filter_by(
            hiredByUserId=userId, isCompleted=True).count()
    else:
        completedContractsCount = MarketplaceItem.query.filter_by(
            hiredUserId=userId, isCompleted=True).count()

    return completedContractsCount


def getMutualActiveContracts(byUserId, userId):
    client = User.query.filter_by(id=byUserId).first()
    freelancer = User.query.filter_by(id=userId).first()

    if not client:
        return jsonify(message="User not found!"), 404

    if not freelancer:
        return jsonify(message="User not found!"), 404

    if not client.isClient:
        return jsonify(message="User is not a client!"), 403

    if freelancer.isClient:
        return jsonify(message="User is not a freelancer!"), 403

    mutualActiveContractsCount = MarketplaceItem.query.filter_by(
        hiredByUserId=byUserId, hiredUserId=userId, isCompleted=False).count()

    return mutualActiveContractsCount


def getMutualCompletedContracts(byUserId, userId):
    client = User.query.filter_by(id=byUserId).first()
    freelancer = User.query.filter_by(id=userId).first()

    if not client:
        return jsonify(message="User not found!"), 404

    if not freelancer:
        return jsonify(message="User not found!"), 404

    if not client.isClient:
        return jsonify(message="User is not a client!"), 403

    if freelancer.isClient:
        return jsonify(message="User is not a freelancer!"), 403

    mutualCompletedContractsCount = MarketplaceItem.query.filter_by(
        hiredByUserId=byUserId, hiredUserId=userId, isCompleted=True).count()

    return mutualCompletedContractsCount


@app.route('/')
def index():
    return jsonify(message='Flask server is running!')


@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        user_name = data['username']
        user_email = data['email']
        user_password = data['password']
        user_isClient = data['isClient']

        hashed_password = generate_password_hash(user_password)

        user = User(username=user_name, email=user_email,
                    password=hashed_password, isClient=user_isClient)

        db.session.add(user)
        db.session.commit()

        return jsonify(message='User created successfully!'), 201
    except Exception as e:
        print(str(e))
        return jsonify(message='Some error occurred!'), 500


@app.route('/signin', methods=['POST'])
def signin():
    try:
        data = request.get_json()
        user_email = data['email']
        user_password = data['password']

        user = User.query.filter_by(email=user_email).first()

        if user and check_password_hash(user.password, user_password):
            loggedInUser['username'] = user.username
            loggedInUser['userid'] = user.id
            return jsonify(message='User login success!'), 200
        else:
            return jsonify(message='Invalid email or password'), 401
    except Exception as e:
        print(str(e))
        return jsonify(message='Some error occurred!'), 500


@app.route('/get_login_user', methods=['GET'])
def getLoggedInUser():
    try:
        if 'userid' not in loggedInUser:
            return jsonify(message='User not authenticated!'), 404
        return jsonify(loggedInUser), 200
    except Exception as e:
        print(str(e))
        return jsonify(message='Some error occurred!'), 500


@app.route('/users', methods=['GET'])
def users():
    try:
        users = User.query.all()
        user_data = []
        for user in users:
            user_data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'creds': user.creds,
                'isClient': user.isClient,
                'createdAt': user.createdAt.isoformat()
            })
        return jsonify(user_data), 200
    except Exception as e:
        print(str(e))
        return jsonify(message='Some error occurred!'), 500


@app.route('/marketplace_items', methods=['GET'])
def getMarketplaceItems():
    mpItems = MarketplaceItem.query.join(
        MarketplaceItem.user, isouter=True).all()

    if len(mpItems) == 0:
        return jsonify(message='No marketplace items found!'), 404

    return jsonify([item.to_dict() for item in mpItems]), 200


@app.route('/marketplace_item', methods=['POST'])
def setMarketplaceItem():
    try:
        if 'userid' not in loggedInUser:
            return jsonify(message='User not authenticated!'), 404

        data = request.get_json()
        title = data['title']
        description = data['description']
        price = data['price']
        isHourly = data['isHourly']
        minCreds = data['minCreds']
        maxCreds = data['maxCreds']
        hiredByUserId = loggedInUser.get('userid')

        newMarketplaceItem = MarketplaceItem(
            title=title, description=description, price=price, isHourly=isHourly, minCreds=minCreds, maxCreds=maxCreds, hiredByUserId=hiredByUserId)

        db.session.add(newMarketplaceItem)
        db.session.commit()

        return jsonify(message='Marketplace Item created successfully!'), 201
    except Exception as e:
        print(str(e))
        return jsonify(message='Some error occurred!'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
