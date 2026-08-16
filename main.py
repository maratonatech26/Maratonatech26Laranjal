import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

from services import buscar_videos_youtube, analisar_com_gemini

load_dotenv('kei.env')

app = Flask(__name__)
CORS(app)

# --- ROTAS DE PÁGINAS (HTML) ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/noticias')
def noticias():
    return render_template('noticias.html')

@app.route('/videos')
def videos():
    return render_template('videos.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')


# --- ENDPOINTS DAS APIs (DADOS) ---

@app.route('/analisar', methods=['POST'])
def analisar():
    if 'texto' not in request.form or not request.form['texto'].strip():
        return jsonify({'sucesso': False, 'erro': 'Envie pelo menos o campo "texto".'}), 400

    prompt_texto = request.form['texto']
    arquivo_imagem = request.files.get('imagem')

    resultado = analisar_com_gemini(prompt_texto, arquivo_imagem)
    status_code = 200 if resultado.get('sucesso') else 500
    return jsonify(resultado), status_code

@app.route('/api/videos', methods=['GET'])
def api_videos():
    # Permite passar um termo de busca opcional via query string (ex: /api/videos?q=phishing)
    termo = request.args.get('q', 'como identificar golpes virtuais phishing')
    resultado = buscar_videos_youtube(termo)
    status_code = 200 if resultado.get('sucesso') else 500
    return jsonify(resultado), status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
