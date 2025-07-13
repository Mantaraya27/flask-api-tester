from flask import Flask, jsonify, request

app = Flask(__name__)

# Datos de ejemplo
users = [
    {"id": 1, "name": "Alice", "role": "user"},
    {"id": 2, "name": "Bob", "role": "admin"}
]

@app.route('/')
def home():
    """Endpoint raíz que devuelve un mensaje de bienvenida"""
    return jsonify({"message": "Bienvenido a la API Flask"})

@app.route('/users', methods=['GET'])
def get_users():
    """Devuelve todos los usuarios"""
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Devuelve un usuario específico"""
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    """Crea un nuevo usuario (sin autenticación real)"""
    if not request.is_json:
        return jsonify({"error": "Solo se acepta JSON"}), 400
    
    new_user = request.get_json()
    users.append(new_user)
    return jsonify(new_user), 201

if __name__ == '__main__':
    app.run(debug=True)