#flask
import os
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv  # <-- Importado

# Carrega as variáveis de ambiente do seu arquivo kei.env
load_dotenv('kei.env')

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/analisar', methods=['POST'])
def analisar_imagem():
    try:
        # 1. Valida a API Key
        if not GEMINI_API_KEY:
            print("LOG: Chave GEMINI_API_KEY não configurada no arquivo .env.")
            return jsonify({
                'sucesso': False, 
                'erro': 'GEMINI_API_KEY não configurada no arquivo .env.'
            }), 500

        # 2. Valida se o texto foi enviado (campo obrigatório)
        if 'texto' not in request.form or not request.form['texto'].strip():
            print("LOG: Erro - Campo 'texto' ausente na requisição.")
            return jsonify({
                'sucesso': False,
                'erro': 'Envie pelo menos o campo "texto".'
            }), 400

        prompt_texto = request.form['texto']
        parts = [{"text": prompt_texto}]

        # 3. Adiciona imagem caso ela tenha sido enviada
        if 'imagem' in request.files and request.files['imagem'].filename != '':
            arquivo_imagem = request.files['imagem']
            bytes_imagem = arquivo_imagem.read()
            imagem_b64 = base64.b64encode(bytes_imagem).decode('utf-8')
            mime_type = arquivo_imagem.mimetype or 'image/jpeg'

            parts.append({
                "inline_data": {
                    "mime_type": mime_type,
                    "data": imagem_b64
                }
            })

        # 4. Requisição para a API do Gemini (ATUALIZADO AQUI)
        # URL sem a query string ?key=
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

        # A chave enviada via Header x-goog-api-key resolve o erro 401
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY.strip()
        }

        payload = {
            "contents": [
                {
                    "parts": parts
                }
            ]
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)
        dados = response.json()

        if response.status_code != 200:
            print(f"LOG: Erro retornado pela API do Gemini: {dados}")
            return jsonify({'sucesso': False, 'erro': dados}), response.status_code

        # 5. Extrai a resposta da API
        texto_resposta = dados['candidates'][0]['content']['parts'][0]['text']

        return jsonify({
            'sucesso': True,
            'analise': texto_resposta
        }), 200

    except Exception as e:
        print(f"LOG: Ocorreu uma exceção no try/except: {e}")
        return jsonify({
            'sucesso': False,
            'erro': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
