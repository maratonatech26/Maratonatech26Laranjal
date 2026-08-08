#flask
#spck
from flask import Flask, request, jsonify
import google.generativeai as genai
from PIL import Image
import os

app = Flask(__name__)

# Configuração da API Key do Gemini
# Dica: É boa prática usar variáveis de ambiente em produção (os.environ.get)
GENAI_API_KEY = os.environ["GENAI_API_KEY"]
genai.configure(api_key=GENAI_API_KEY)

# Inicializa o modelo
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/analisar', methods=['POST'])
def analisar_imagem():
    try:
        # 1. Verifica se os campos necessários estão na requisição
        if 'imagem' not in request.files or 'texto' not in request.form:
            return jsonify({
                'sucesso': False, 
                'erro': 'Envie tanto o campo "imagem" (arquivo) quanto o campo "texto" (form-data).'
            }), 400

        arquivo_imagem = request.files['imagem']
        prompt_texto = request.form['texto']

        # 2. Converte o arquivo recebido para uma imagem PIL válida
        imagem = Image.open(arquivo_imagem.stream)

        # 3. Faz a chamada para a API do Gemini
        response = model.generate_content([prompt_texto, imagem])

        # 4. Retorna o resultado em formato JSON para quem chamou
        return jsonify({
            'sucesso': True,
            'analise': response.text
        }), 200

    except Exception as e:
        return jsonify({
            'sucesso': False, 
            'erro': str(e)
        }), 500

if __name__ == '__main__':
    # Executa o servidor na porta 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
