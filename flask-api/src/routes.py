from flask import *  
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todoapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define a simple model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# Set up application context
with app.app_context():
    # Create the database tables
    db.create_all()

# Define routes
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        user_data = {'id': user.id, 'username': user.username, 'email': user.email}
        result.append(user_data)
    return jsonify(result)

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!'})


# Home Route
@app.route('/')  
def home():  
  return jsonify({"msg":"home"})

@app.errorhandler(404)
def page_not_found(e):
  return render_template("404.html")
