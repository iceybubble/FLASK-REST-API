from flask import Flask, request, jsonify

app = Flask(__name__)


users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 2

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_id = max([user["id"] for user in users], default=0) + 1
    new_user = {
        "id": new_id,
        "name": data.get("name"),
        "email": data.get("email")
    }

    if not new_user["name"] or not new_user["email"]:
        return jsonify({"error": "Name and email are required"}), 400

    users.append(new_user)
    return jsonify(new_user), 201


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    for user in users:
        if user["id"] == user_id:
            user["name"] = data.get("name", user["name"])
            user["email"] = data.get("email", user["email"])
            return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [user for user in users if user["id"] != user_id]
    return jsonify({"message": f"User {user_id} deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
