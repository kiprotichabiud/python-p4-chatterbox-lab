from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

# Initialize CORS and migrations
CORS(app)
migrate = Migrate(app, db)

# Initialize the database
db.init_app(app)

@app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages = Message.query.order_by(Message.updated_at.desc()).all()  # Retrieve all messages
        response = [message.to_dict() for message in messages]  # Convert each message to dict
        return make_response(response, 200)
    
    elif request.method == "POST":
        data = request.get_json() if request.is_json else request.form
        if not data or 'body' not in data or 'username' not in data:
            return make_response({"error": "Invalid data. Body and username are required."}, 400)
        
        message = Message(**data)  # Create a new message instance
        db.session.add(message)  # Add it to the session
        db.session.commit()  # Commit to the database
        return make_response(message.to_dict(), 201)  # Return the new message

@app.route("/messages/<int:id>", methods=["GET", "PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.get(id)  # Fetch the message by ID
    if message is None:
        return make_response({"error": "Message not found"}, 404)

    if request.method == "GET":
        return make_response(message.to_dict(), 200)

    elif request.method == "PATCH":
        data = request.get_json() if request.is_json else request.form
        for key, value in data.items():
            setattr(message, key, value)  # Update the message fields
        db.session.commit()  # Commit changes to the database
        return make_response(message.to_dict(), 200)

    elif request.method == "DELETE":
        db.session.delete(message)  # Remove the message
        db.session.commit()  # Commit changes
        return make_response({"message": "Message deleted"}, 200)

    return make_response({"error": "Invalid request"}, 400)



if __name__ == "__main__":
    app.run(port=5555)
