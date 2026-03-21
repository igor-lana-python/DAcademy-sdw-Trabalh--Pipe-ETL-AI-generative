#imports das bibliotecas que precisei para funcionamento do codigo
import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

# CONFIG-dados e processamento para gerar a mensagem usando gpt-5

load_dotenv()

API_URL = os.getenv("API_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not API_URL:
    raise ValueError("API_URL não definida")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY não definida")

client = OpenAI(api_key=OPENAI_API_KEY)

NEWS_ICON_URL = "https://www.svgrepo.com/show/95386/credit-card.svg"

#Carregamento dos dados de usuarios, pre preparamento

def get_all_users():
    """
    Busca todos os usuários da API:
    GET /users
    """
    try:
        response = requests.get(f"{API_URL}/users", timeout=10)
        response.raise_for_status()

        data = response.json()

        # Pode ser lista direta ou {"data": [...]}
        if isinstance(data, dict):
            return data.get("data", [])
        return data

    except requests.RequestException as e:
        print(f"Erro ao buscar usuários: {e}")
        return []

#Processo para gerar a mensagem usando GPT atraves de uma chave api-ai

def generate_ai_news(user: dict) -> str:
    name = user.get("name", "Cliente")
    account = user.get("account", {})
    card = user.get("card", {})

    prompt = f"""
Crie uma mensagem curta para cliente bancário.

Nome: {name}
Saldo: {account.get("balance", 0)}
Limite conta: {account.get("limit", 0)}
Limite cartão: {card.get("limit", 0)}

Regras:
- Português Brasil
- Máx 100 caracteres
- Sem emojis
- Apenas a mensagem final
"""

    try:
        response = client.responses.create(
            model="gpt-5",
            input=prompt,
            max_output_tokens=60
        )

        text = response.output_text.strip()

        if not text:
            text = f"{name}, cuide do seu dinheiro hoje para um futuro melhor."

        return text

    except Exception as e:
        print(f"Erro OpenAI ({name}): {e}")
        return f"{name}, organize suas finanças e comece a investir."

#Processo de atualização de dados de usuarios

def update_user(user: dict) -> bool:
    try:
        response = requests.put(
            f"{API_URL}/users/{user['id']}",
            json=user,
            timeout=10
        )
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Erro ao atualizar {user['id']}: {e}")
        return False

#Processamento de usuarios e dados recebidos

def process_users():
    users = get_all_users()

    print(f"Total de usuários recebidos: {len(users)}\n")

    for user in users:
        name = user.get("name")

        # Evita duplicar mensagem (boa prática)
        if user.get("news"):
            print(f"{name} já possui news, pulando...")
            continue

        news_text = generate_ai_news(user)

        user.setdefault("news", [])
        user["news"].append({
            "icon": NEWS_ICON_URL,
            "description": news_text
        })

        print(f"{name} -> {news_text}")

        success = update_user(user)
        print(f"Atualizado? {success}\n")

    print("Processamento finalizado.")

# -MAIN-

if __name__ == "__main__":
    process_users()