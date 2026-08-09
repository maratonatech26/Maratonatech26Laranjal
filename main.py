import os
import base64
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from dotenv import load_dotenv

load_dotenv('kei.env')

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# 1. Rota principal para servir o HTML da pasta 'templates'
@app.route('/')
def index():
    return render_template('index.html')

# 2. Rota que processa a requisição da API
@app.route('/analisar', methods=['POST'])
def analisar_imagem():
    try:
        if not GEMINI_API_KEY:
            print("LOG: Chave GEMINI_API_KEY não configurada no arquivo kei.env.")
            return jsonify({
                'sucesso': False,
                'erro': 'GEMINI_API_KEY não configurada no arquivo kei.env.'
            }), 500

        if 'texto' not in request.form or not request.form['texto'].strip():
            print("LOG: Erro - Campo 'texto' ausente na requisição.")
            return jsonify({
                'sucesso': False,
                'erro': 'Envie pelo menos o campo "texto".'
            }), 400

        prompt_texto = request.form['texto']
        parts = [{"text": prompt_texto}]

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

        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent"

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

        candidates = dados.get('candidates', [])
        if not candidates:
            return jsonify({'sucesso': False, 'erro': 'Resposta vazia da API', 'detalhes': dados}), 500

        texto_resposta = candidates[0]['content']['parts'][0]['text']

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
