from moviepy import *
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# Cores MSA
GOLD = '#C9A227'
GOLD_LIGHT = '#E5C158'
BLACK = '#0A0A0A'
WHITE = '#FFFFFF'
GRAY = '#1E1E1E'

def create_gradient_bg(width, height, color1, color2):
    """Cria background gradiente"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        r = int(10 + (26 - 10) * (y / height))
        g = int(10 + (19 - 10) * (y / height))
        b = int(46 + (62 - 46) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return np.array(img)

def create_frame_with_text(text, subtext=None, emoji=None, width=1080, height=1920):
    """Cria um frame com texto estilizado"""
    # Background gradiente
    bg = create_gradient_bg(width, height, BLACK, '#16213e')
    img = Image.fromarray(bg)
    draw = ImageDraw.Draw(img)
    
    # Fontes (usar fonte padrão se não achar)
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 50)
    except:
        font_large = ImageFont.load_default()
        font_medium = font_large
        font_small = font_large
    
    # Emoji
    if emoji:
        bbox = draw.textbbox((0, 0), emoji, font=font_large)
        emoji_w = bbox[2] - bbox[0]
        draw.text(((width - emoji_w) // 2, 300), emoji, font=font_large, fill=GOLD)
    
    # Texto principal
    bbox = draw.textbbox((0, 0), text, font=font_medium)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    y_pos = 600 if emoji else 500
    
    # Desenhar texto com sombra
    draw.text(((width - text_w) // 2 + 3, y_pos + 3), text, font=font_medium, fill='black')
    draw.text(((width - text_w) // 2, y_pos), text, font=font_medium, fill=WHITE)
    
    # Subtexto
    if subtext:
        bbox2 = draw.textbbox((0, 0), subtext, font=font_large)
        sub_w = bbox2[2] - bbox2[0]
        draw.text(((width - sub_w) // 2, y_pos + 150), subtext, font=font_large, fill=GOLD)
    
    return np.array(img)

def create_cta_frame(width=1080, height=1920):
    """Frame final com CTA"""
    bg = create_gradient_bg(width, height, BLACK, '#16213e')
    img = Image.fromarray(bg)
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 100)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 45)
    except:
        font_large = ImageFont.load_default()
        font_medium = font_large
        font_small = font_large
    
    # Badge
    badge_text = "🔥 ULTIMA CHANCE"
    bbox = draw.textbbox((0, 0), badge_text, font=font_small)
    badge_w = bbox[2] - bbox[0] + 60
    badge_h = 80
    draw.rounded_rectangle([(width//2 - badge_w//2, 300), (width//2 + badge_w//2, 300 + badge_h)], 
                           radius=40, fill=GOLD)
    draw.text((width//2 - (bbox[2]-bbox[0])//2, 310), badge_text, font=font_small, fill=BLACK)
    
    # Texto CTA
    cta_lines = ["Clique no link", "antes que acabe"]
    y_start = 500
    for i, line in enumerate(cta_lines):
        color = GOLD if i == 1 else WHITE
        bbox = draw.textbbox((0, 0), line, font=font_large)
        text_w = bbox[2] - bbox[0]
        draw.text(((width - text_w) // 2, y_start + i * 140), line, font=font_large, fill=color)
    
    # Botão CTA
    btn_text = "LINK NA BIO →"
    bbox = draw.textbbox((0, 0), btn_text, font=font_medium)
    btn_w = bbox[2] - bbox[0] + 80
    btn_h = 100
    btn_y = 900
    draw.rounded_rectangle([(width//2 - btn_w//2, btn_y), (width//2 + btn_w//2, btn_y + btn_h)], 
                           radius=20, fill=GOLD)
    draw.text((width//2 - (bbox[2]-bbox[0])//2, btn_y + 20), btn_text, font=font_medium, fill=BLACK)
    
    # Urgência
    urgency = "⚠️ Só 15 vagas"
    bbox = draw.textbbox((0, 0), urgency, font=font_small)
    text_w = bbox[2] - bbox[0]
    draw.text(((width - text_w) // 2, 1100), urgency, font=font_small, fill='gray')
    
    return np.array(img)

def create_progress_bar_frame(width=1080, height=1920, progress=0):
    """Frame com barra de progresso no topo"""
    bg = create_gradient_bg(width, height, BLACK, '#16213e')
    img = Image.fromarray(bg)
    draw = ImageDraw.Draw(img)
    
    # Barra de progresso
    bar_h = 8
    draw.rectangle([(0, 0), (width, bar_h)], fill='#333')
    filled_width = int(width * progress)
    draw.rectangle([(0, 0), (filled_width, bar_h)], fill=GOLD)
    
    return np.array(img)

# Criar vídeo de 15 segundos (450 frames a 30fps)
print("🎬 Criando vídeo de demonstração MSA...")

# Slides do StoryReels
slides = [
    {"text": "Eu era esteticista...", "subtext": "12h por dia", "emoji": "💅", "duration": 3},
    {"text": "Trabalhava", "subtext": "sem parar", "emoji": "😫", "duration": 3},
    {"text": "Hoje faturei", "subtext": "R$ 47.000", "emoji": "💰", "duration": 3},
    {"text": "Em apenas", "subtext": "30 dias", "emoji": "📅", "duration": 3},
    {"text": "Sem aparecer", "subtext": "sem estoque", "emoji": "🚀", "duration": 3},
]

# Criar clips
clips = []

for i, slide in enumerate(slides):
    frame = create_frame_with_text(slide["text"], slide["subtext"], slide["emoji"])
    frame_clip = ImageClip(frame).with_duration(slide["duration"])
    clips.append(frame_clip)

# Frame CTA final
cta_frame = create_cta_frame()
cta_clip = ImageClip(cta_frame).with_duration(3)
clips.append(cta_clip)

# Concatenar
final_video = concatenate_videoclips(clips, method="compose")

# Adicionar barra de progresso animada
progress_clips = []
total_duration = sum(s["duration"] for s in slides) + 3
for i in range(int(total_duration * 30)):
    progress = i / (total_duration * 30)
    frame = create_progress_bar_frame(progress=progress)
    progress_clips.append(ImageClip(frame).with_duration(1/30))

progress_video = concatenate_videoclips(progress_clips, method="compose")

# Combinar vídeo principal com barra de progresso
final_composite = CompositeVideoClip([final_video, progress_video.with_position("top")])

# Salvar
output_path = "/root/.openclaw/workspace/projetos-msa/output/story_teste.mp4"
final_composite.write_videofile(output_path, fps=30, codec="libx264", audio=False)

print(f"✅ Vídeo criado: {output_path}")
print(f"📊 Duração: {final_composite.duration}s")
print(f"📐 Resolução: 1080x1920 (9:16)")
