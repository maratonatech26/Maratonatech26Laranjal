import os
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Libera acesso para requisições externas (CORS)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/analisar', methods=['POST'])
def analisar_imagem():
    try:
        if not GEMINI_API_KEY:
            return jsonify({
                'sucesso': False, 
                'erro': 'GEMINI_API_KEY não configurada no servidor.'
            }), 500

        # Exige APENAS o texto como obrigatório
        if 'texto' not in request.form or not request.form['texto'].strip():
            return jsonify({
                'sucesso': False,
                'erro': 'O campo "texto" é obrigatório.'
            }), 400

        prompt_texto = request.form['texto']
        parts = [{"text": prompt_texto}]

        # Se houver imagem enviada na requisição, adiciona ao payload
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

        # Endpoint REST oficial
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": parts
                }
            ]
        }

        response = requests.post(url, json=payload, timeout=30)
        dados = response.json()

        if response.status_code != 200:
            return jsonify({'sucesso': False, 'erro': dados}), response.status_code

        texto_resposta = dados['candidates'][0]['content']['parts'][0]['text']

        return jsonify({
            'sucesso': True,
            'analise': texto_resposta
        }), 200

    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
