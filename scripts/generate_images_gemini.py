#!/usr/bin/env python3
"""
Gerador de Imagens MSA usando Gemini Imagen API
Gera mockups, backgrounds e imagens conceituais para vídeos e criativos
"""
import os
import requests
import json
import base64
from pathlib import Path

# Carregar API key
with open('/root/.openclaw/.gemini_key', 'r') as f:
    API_KEY = f.read().strip()

BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "imagen-4.0-generate-001"  # Modelo correto para geração de imagens

# Diretório de saída
OUTPUT_DIR = Path("/root/.openclaw/workspace/projetos-msa/assets/imagens")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_image(prompt, filename, aspect_ratio="16:9"):
    """Gera imagem usando Gemini Imagen API"""
    
    url = f"{BASE_URL}/models/{MODEL}:predict?key={API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "instances": [{
            "prompt": prompt
        }],
        "parameters": {
            "aspectRatio": aspect_ratio,
            "numberOfImages": 1,
            "outputMimeType": "image/jpeg"
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        
        # Extrair imagem da resposta (formato Imagen)
        if 'predictions' in result and len(result['predictions']) > 0:
            prediction = result['predictions'][0]
            if 'bytesBase64Encoded' in prediction:
                image_data = base64.b64decode(prediction['bytesBase64Encoded'])
                
                filepath = OUTPUT_DIR / filename
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                
                print(f"✅ Imagem gerada: {filepath}")
                print(f"📊 Tamanho: {len(image_data)} bytes")
                return filepath
        
        print(f"⚠️ Resposta inesperada: {json.dumps(result, indent=2)[:500]}")
        return None
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        if hasattr(e, 'response'):
            print(f"Response: {e.response.text[:500]}")
        return None

def generate_all_images():
    """Gera todas as imagens necessárias para o projeto MSA"""
    
    print("🎨 Gerando imagens para o projeto MSA...\n")
    print(f"API: {MODEL}")
    print(f"Output: {OUTPUT_DIR}\n")
    
    # 1. Background premium para VSL
    print("1️⃣ Background premium VSL...")
    generate_image(
        "Abstract luxury background, dark gradient from deep navy blue (#0A0A1A) to black (#0A0A0A), "
        "subtle golden light rays emanating from center, floating golden particles, "
        "professional marketing video background, cinematic lighting, 4K quality, "
        "minimalist elegant, no text, no people",
        "background_vsl.jpg",
        "16:9"
    )
    
    # 2. Mockup de produtos digitais
    print("\n2️⃣ Mockup produtos MSA...")
    generate_image(
        "Professional product mockup showing a smartphone and laptop displaying "
        "a digital course interface with gold and black color scheme, "
        "floating around the devices: icons of money, graphs trending up, "
        "notification bell with sales notifications, "
        "premium marketing style, dark background with golden accents, "
        "isometric 3D render, photorealistic",
        "mockup_produtos.jpg",
        "16:9"
    )
    
    # 3. Mulher livre/trabalhando de casa
    print("\n3️⃣ Imagem conceitual liberdade...")
    generate_image(
        "Professional photo of a confident brazilian woman in her 30s working on laptop "
        "from a beautiful home office, natural light coming through window, "
        "she's smiling while looking at screen showing sales dashboard, "
        "modern minimalist interior, plants in background, "
        "conveying freedom and success, lifestyle photography, "
        "warm tones with subtle golden hour lighting",
        "mulher_liberdade.jpg",
        "16:9"
    )
    
    # 4. Thumbnail YouTube
    print("\n4️⃣ Thumbnail YouTube...")
    generate_image(
        "YouTube thumbnail design, bold text space on left side (dark background), "
        "right side shows excited brazilian woman holding smartphone "
        "showing sales notification, big golden number 'R$ 47.000' floating, "
        "fire emojis, high contrast, eye-catching, clickbait style but professional, "
        "colors: black, gold, white, red accents for urgency",
        "thumbnail_youtube.jpg",
        "16:9"
    )
    
    # 5. Prova social / Dashboard
    print("\n5️⃣ Dashboard de vendas...")
    generate_image(
        "Professional dashboard screenshot showing sales analytics, "
        "big numbers: R$ 47.000 revenue this month, 847 sales, "
        "green upward trending graph, golden trophy icon, "
        "clean modern UI design, dark mode interface with gold accents, "
        "notification badges showing recent sales, "
        "premium SaaS dashboard style, photorealistic render",
        "dashboard_vendas.jpg",
        "16:9"
    )
    
    # 6. Background para criativos de anúncio (9:16)
    print("\n6️⃣ Background criativo ads (9:16)...")
    generate_image(
        "Abstract dynamic background for social media ad, "
        "dark gradient with golden light streaks, motion blur effect, "
        "geometric shapes floating, energy and movement, "
        "premium luxury feel, no text, no people, "
        "vertical composition 9:16 ratio feeling, "
        "cinematic, 4K, marketing campaign background",
        "background_ads.jpg",
        "9:16"
    )
    
    # 7. Checklist / Benefícios visual
    print("\n7️⃣ Visual checklist benefícios...")
    generate_image(
        "Clean infographic style image showing 4 golden checkmarks "
        "with glowing effect on dark background, each checkmark connected "
        "to a subtle icon: house (home), eye with slash (no appearance), "
        "package (no stock), money (profit), "
        "premium 3D render style, floating elements, "
        "golden metallic material, dark navy background",
        "checklist_beneficios.jpg",
        "16:9"
    )
    
    print("\n✅ Todas as imagens foram geradas!")
    print(f"📁 Diretório: {OUTPUT_DIR}")
    
    # Listar arquivos
    files = list(OUTPUT_DIR.glob("*.jpg"))
    for f in files:
        size = f.stat().st_size
        print(f"  - {f.name}: {size/1024:.1f} KB")

if __name__ == "__main__":
    generate_all_images()
