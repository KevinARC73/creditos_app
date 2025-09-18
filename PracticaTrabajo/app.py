from flask import Flask, request, jsonify, render_template
from database import init_db
import models

app = Flask(__name__)

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/creditos', methods=['POST'])
def crear():
    data = request.json
    if not all(k in data for k in ("cliente", "monto", "tasa_interes", "plazo", "fecha_otorgamiento")):
        return jsonify({"error": "Campos incompletos"}), 400
    
    new_id = models.crear(
        data["cliente"], data["monto"], data["tasa_interes"], data["plazo"], data["fecha_otorgamiento"]
    )
    return jsonify({"message": "Credito creado", "id": new_id}), 201

@app.route('/creditos', methods=["GET"])
def listar():
    creditos = models.obtener()
    return jsonify(creditos), 200
    
@app.route('/creditos/<int:id>', methods=['PUT'])
def actualizar(id):
    data = request.json
    if not all(k in data for k in ("cliente", "monto", "tasa_interes", "plazo", "fecha_otorgamiento")):
        return jsonify({"error": "Campos incompletos"}), 400
    
    actualizado = models.actualizar(
        id, data["cliente"], data["monto"], data["tasa_interes"], data["plazo"], data["fecha_otorgamiento"]
    )
    if actualizado:
        return jsonify({"message": "Registro actualizado"}), 200
    return jsonify({"error": "Registro no encontrado"}), 404

@app.route('/creditos/<int:id>', methods=['DELETE'])
def eliminar(id):
    eliminado = models.borrar(id)
    if eliminado:
        return jsonify({"message": "Registro eliminado"}), 200
    return jsonify({"error": "Registro no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
