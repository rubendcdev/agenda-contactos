from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Datos en memoria
contacts = []
next_id = 1

def reset_data():
    """Limpia los contactos en memoria (para pruebas)."""
    global contacts, next_id
    contacts = []
    next_id = 1
    precargar_contactos()

def precargar_contactos():
    """Agrega algunos contactos iniciales"""
    global contacts, next_id
    contactos_iniciales = [
        {"name": "Juan Pérez", "email": "juan@mail.com", "phone": "123456789"},
        {"name": "Ana López", "email": "ana@mail.com", "phone": "987654321"},
        {"name": "Carlos Díaz", "email": "carlos@mail.com", "phone": "555555555"}
    ]
    for c in contactos_iniciales:
        c["id"] = next_id
        next_id += 1
        contacts.append(c)

# Llamamos a precarga al inicio
precargar_contactos()

@app.route("/contacts", methods=["POST"])
def create_contact():
    global next_id
    data = request.get_json(silent=True)
    if not data or "name" not in data or "email" not in data:
        abort(400, "Faltan campos obligatorios: name y email")

    contact = {
        "id": next_id,
        "name": data["name"],
        "email": data["email"],
        "phone": data.get("phone", "")
    }
    contacts.append(contact)
    next_id += 1
    return jsonify(contact), 201

@app.route("/contacts", methods=["GET"])
def list_contacts():
    return jsonify(contacts)

@app.route("/contacts/<int:contact_id>", methods=["GET"])
def get_contact(contact_id):
    for c in contacts:
        if c["id"] == contact_id:
            return jsonify(c)
    abort(404, "Contacto no encontrado")

@app.route("/contacts/<int:contact_id>", methods=["PUT"])
def update_contact(contact_id):
    data = request.get_json(silent=True)
    if not data:
        abort(400, "No se enviaron datos")

    for c in contacts:
        if c["id"] == contact_id:
            c["name"] = data.get("name", c["name"])
            c["email"] = data.get("email", c["email"])
            c["phone"] = data.get("phone", c["phone"])
            return jsonify(c)
    abort(404, "Contacto no encontrado")

@app.route("/contacts/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    global contacts
    for c in contacts:
        if c["id"] == contact_id:
            contacts = [x for x in contacts if x["id"] != contact_id]
            return jsonify({"message": "Contacto eliminado"})
    abort(404, "Contacto no encontrado")

if __name__ == "__main__":
    app.run(debug=True)
