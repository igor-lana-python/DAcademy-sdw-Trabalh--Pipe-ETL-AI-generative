from flask import Flask, jsonify, abort, request
import random

app = Flask(__name__)

API_URL = "http://localhost:5000"

#Parte onde fica os dados e local host de onde tirais os dados de usuarios com base na lista dos ususarios

def generate_users():
    users = []

    nomes = [
        "Pyterson", "Pip", "Pep", "Ana", "João", "Maria", "Carlos", "Fernanda",
        "Lucas", "Beatriz", "Rafael", "Juliana", "Bruno", "Patricia", "Gabriel",
        "Camila", "Rodrigo", "Amanda", "Thiago", "Larissa", "Eduardo", "Bianca",
        "Felipe", "Vanessa", "Gustavo", "Renata", "Daniel", "Aline", "Marcelo",
        "Natália", "André", "Paula", "Vinicius", "Leticia", "Igor", "Carla",
        "Leandro", "Tatiane", "Caio", "Priscila", "Hugo", "Monique", "Otavio",
        "Sabrina", "Diego", "Flavia", "Matheus", "Cristina", "Vitor", "Elaine"
    ]
#quantos usuarios ele vai percorrer e exibir os resultados pos processo final
    for i in range(1, 5):
        nome = nomes[i - 1]

        user = {
            "id": i,
            "name": nome,
            "account": {
                "id": i + 3,
                "number": f"{i:05d}-{i}",
                "agency": "0001",
                "balance": round(random.uniform(0, 5000), 2),
                "limit": 500.0
            },
            "card": {
                "id": i,
                "number": f"**** **** **** {str(i).zfill(4)}",
                "limit": 1000.0
            },
            "features": [],
            "news": []
        }

        users.append(user)

    return users


USERS = generate_users()

#Verificação de integração dos dados e devericidade dos usuarios existentes

@app.route("/users", methods=["GET"])
def list_users():
    return jsonify(USERS)


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in USERS if u["id"] == user_id), None)

    if not user:
        abort(404, description="Usuário não encontrado")

    return jsonify(user)


@app.route("/users/<int:user_id>/news", methods=["PUT"])
def update_user_news(user_id):
    user = next((u for u in USERS if u["id"] == user_id), None)

    if not user:
        abort(404, description="Usuário não encontrado")

    data = request.get_json()

    if not data or "news" not in data:
        abort(400, description="Campo 'news' é obrigatório")

    if not isinstance(data["news"], list):
        abort(400, description="Campo 'news' deve ser uma lista")

    for item in data["news"]:
        if not isinstance(item, dict):
            abort(400, description="Cada item de 'news' deve ser um objeto")

        if "id" not in item or "icon" not in item or "description" not in item:
            abort(400, description="Formato inválido em 'news'")

    user["news"] = data["news"]

    return jsonify(user), 200


if __name__ == "__main__":
    app.run(debug=True)