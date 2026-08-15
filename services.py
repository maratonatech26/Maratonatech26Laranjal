import os
import requests
import base64
from dotenv import load_dotenv

# Carrega o arquivo de ambiente
load_dotenv('kei.env')

def buscar_videos_youtube(termo='como identificar golpes virtuais phishing'):
    youtube_key = os.environ.get("YOUTUBE_API_KEY")
    if not youtube_key:
        return {'sucesso': False, 'erro': 'YOUTUBE_API_KEY não configurada no kei.env'}

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'key': youtube_key,
        'q': termo,
        'part': 'snippet',
        'type': 'video',
        'maxResults': 5,
        'relevanceLanguage': 'pt'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        dados = response.json()

        if response.status_code != 200:
            return {'sucesso': False, 'erro': dados}

        videos = []
        for item in dados.get('items', []):
            videos.append({
                'id': item['id']['videoId'],
                'titulo': item['snippet']['title'],
                'descricao': item['snippet']['description'],
                'thumb': item['snippet']['thumbnails']['high']['url'],
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            })

        return {'sucesso': True, 'videos': videos}

    except Exception as e:
        return {'sucesso': False, 'erro': str(e)}


def analisar_com_gemini(prompt_texto, arquivo_imagem=None):
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        return {'sucesso': False, 'erro': 'GEMINI_API_KEY não configurada no kei.env'}

    parts = [{"text": prompt_texto}]

    if arquivo_imagem and arquivo_imagem.filename != '':
        bytes_imagem = arquivo_imagem.read()
        imagem_b64 = base64.b64encode(bytes_imagem).decode('utf-8')
        mime_type = arquivo_imagem.mimetype or 'image/jpeg'

        parts.append({
            "inline_data": {
                "mime_type": mime_type,
                "data": imagem_b64
            }
        })

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": gemini_key.strip()
    }
    payload = {"contents": [{"parts": parts}]}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        dados = response.json()

        if response.status_code != 200:
            return {'sucesso': False, 'erro': dados}

        candidates = dados.get('candidates', [])
        if not candidates:
            return {'sucesso': False, 'erro': 'Resposta vazia da API', 'detalhes': dados}

        texto_resposta = candidates[0]['content']['parts'][0]['text']
        return {'sucesso': True, 'analise': texto_resposta}

    except Exception as e:
        return {'sucesso': False, 'erro': str(e)}
