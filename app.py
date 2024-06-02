from datetime import datetime
import email
from flask import Flask, jsonify, session, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.sqlite import JSON
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
    rating = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'creds': self.creds,
            'isClient': self.isClient,
            'createdAt': self.createdAt.isoformat(),
            'rating': self.rating
        }


class MarketplaceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    skills = db.Column(JSON, nullable=False, default=[])
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
            'skills': self.skills,
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
    marketplaceItem = db.relationship(
        'MarketplaceItem', backref='proposals', foreign_keys=[marketplaceItemId])
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='proposals', foreign_keys=[userId])
    proposalText = db.Column(db.String(512), nullable=False)
    isAccepted = db.Column(db.Boolean, default=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'marketplaceItemId': self.marketplaceItem.to_dict(),
            'userId': self.user.to_dict(),
            'proposalText': self.proposalText,
            'isAccepted': self.isAccepted,
            'createdAt': self.createdAt.isoformat()
        }


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rater_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ratee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    comment = db.Column(db.String(512), nullable=True)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'rater_id': self.rater_id,
            'ratee_id': self.ratee_id,
            'rating': self.rating,
            'comment': self.comment,
            'createdAt': self.createdAt.isoformat()
        }


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

        existingUser = User.query.filter_by(email=user_email).first()
        if existingUser:
            return jsonify(message="Email already exists!"), 422

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
                'createdAt': user.createdAt.isoformat(),
                'rating': user.rating
            })
        return jsonify(user_data), 200
    except Exception as e:
        print(str(e))
        return jsonify(message='Some error occurred!'), 500


@app.route('/users/<int:user_id>', methods=['GET'])
def getUserById(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify(message='User does not exist!'), 404
        return jsonify(user.to_dict())
    except Exception as e:
        print(str(e))
        return jsonify(message='Some error occurred!'), 500


@app.route('/marketplace_items', methods=['GET'])
def getMarketplaceItems():
    try:
        mpItems = MarketplaceItem.query.join(
            MarketplaceItem.user, isouter=True).all()

        if len(mpItems) == 0:
            return jsonify(message='No marketplace items found!'), 404

        return jsonify([item.to_dict() for item in mpItems]), 200
    except Exception as e:
        print(str(e))
        return jsonify(message='Some error occurred!'), 500


@app.route('/marketplace_item/<int:item_id>', methods=['GET'])
def getMarketplaceItemById(item_id):
    try:
        mpItem = MarketplaceItem.query.filter_by(id=item_id).first()
        if not mpItem:
            return jsonify(message='Item not found!'), 404
        return jsonify(mpItem.to_dict())
    except Exception as e:
        print(str(e))
        return jsonify(message='Some error occurred!'), 500


@app.route('/marketplace_item/user/<int:user_id>', methods=['GET'])
def getMarketplaceItemByUserId(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify(message='User not found!'), 404
        mpItems = MarketplaceItem.query.filter_by(hiredByUserId=user_id).all()
        if not mpItems:
            return jsonify(message='Marketplace Items not found!'), 404
        return jsonify([item.to_dict() for item in mpItems])
    except Exception as e:
        print(str(e))
        return jsonify(message='Some error occurred!'), 500


@app.route('/marketplace_item', methods=['POST'])
def setMarketplaceItem():
    try:
        if 'userid' not in loggedInUser:
            return jsonify(message='User not authenticated!'), 404

        data = request.get_json()
        title = data['title']
        description = data['description']
        skills = data['skills']
        price = data['price']
        isHourly = data['isHourly']
        minCreds = data['minCreds']
        maxCreds = data['maxCreds']
        hiredByUserId = loggedInUser.get('userid')

        newMarketplaceItem = MarketplaceItem(
            title=title, description=description, skills=skills, price=price, isHourly=isHourly, minCreds=minCreds, maxCreds=maxCreds, hiredByUserId=hiredByUserId)

        db.session.add(newMarketplaceItem)
        db.session.commit()

        return jsonify(message='Marketplace Item created successfully!'), 201
    except Exception as e:
        print(str(e))
        return jsonify(message='Some error occurred!'), 500


@app.route('/proposals', methods=['GET'])
def getProposals():
    try:
        proposals = Proposal.query.join(Proposal.marketplaceItem, isouter=True).join(
            Proposal.user, isouter=True).all()

        if len(proposals) == 0:
            return jsonify(message='No proposals found!'), 404

        return jsonify([p.to_dict() for p in proposals]), 200
    except Exception as e:
        print(str(e))
        return jsonify(message='Some error occurred!'), 500


@app.route('/proposal/<int:p_id>', methods=['GET'])
def getProposalById(p_id):
    try:
        proposal = Proposal.query.filter_by(id=p_id).first()
        if not proposal:
            return jsonify(message='Proposal not found!'), 404
        return jsonify(proposal.to_dict())
    except Exception as e:
        print(str(e))
        return jsonify(message='Some error occurred!'), 500


@app.route('/proposal/user/<int:user_id>', methods=['GET'])
def getProposalByUserId(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify(message='User not found!'), 404
        proposals = Proposal.query.filter_by(userId=user_id).all()
        if not proposals:
            return jsonify(message='Proposals not found!'), 404
        return jsonify([p.to_dict() for p in proposals])
    except Exception as e:
        print(str(e))
        return jsonify(message='Some error occurred!'), 500


@app.route('/proposal/mpitem/<int:item_id>', methods=['GET'])
def getProposalByMarketplaceId(item_id):
    try:
        mpItem = MarketplaceItem.query.filter_by(id=item_id).first()
        if not mpItem:
            return jsonify(message='Marketplace Item not found!'), 404
        proposals = Proposal.query.filter_by(marketplaceItemId=item_id).all()
        if not proposals:
            return jsonify(message='Proposals not found!'), 404
        return jsonify([p.to_dict() for p in proposals])
    except Exception as e:
        print(str(e))
        return jsonify(message='Some error occurred!'), 500


@app.route('/proposal', methods=['POST'])
def setProposal():
    try:
        if 'userid' not in loggedInUser:
            return jsonify(message='User not authenticated!'), 404

        data = request.get_json()
        marketplaceItemId = data['marketplaceItemId']
        userId = loggedInUser['userid']
        proposalText = data['proposalText']

        proposal = Proposal(
            marketplaceItemId=marketplaceItemId, userId=userId, proposalText=proposalText)

        db.session.add(proposal)
        db.session.commit()

        return jsonify(message='Proposal sent successfully!'), 201
    except Exception as e:
        print(str(e))
        return jsonify(message='Some error occurred!'), 500


@app.route('/rate', methods=['POST'])
def rate_user():
    data = request.get_json()
    try:
        rater_id=data['rater_id'],
        ratee_id=data['ratee_id'],
        rating=data['rating'],
        comment=data.get('comment'),

        rating = Rating(rater_id=rater_id, ratee_id=ratee_id, rating=rating, comment=comment)

        db.session.add(rating)
        db.session.commit()

        ratee = User.query.get(ratee_id)
        ratings = Rating.query.filter_by(ratee_id=ratee_id).all()
        if ratings:
            average_rating = sum(r.rating for r in ratings) / len(ratings)
            ratee.rating = average_rating
            db.session.commit()

        return jsonify(rating.to_dict()), 201
    except Exception as e:
        print(str(e))
        return jsonify({"error": "An error occurred"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
