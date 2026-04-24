#!/usr/bin/env python3
"""
Gerador de vídeo MSA profissional - 10 segundos
Usa Python + Pillow + FFmpeg
"""
import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess

# Cores MSA
GOLD = (201, 162, 39)
GOLD_LIGHT = (229, 193, 88)
GOLD_DARK = (168, 132, 32)
BLACK = (10, 10, 10)
DARK_BLUE = (22, 33, 62)
WHITE = (255, 255, 255)

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def lerp_color(c1, c2, t):
    """Interpolação linear entre cores"""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

def create_gradient_bg(width, height, frame_num, total_frames):
    """Background com gradiente animado"""
    img = Image.new('RGB', (width, height), BLACK)
    draw = ImageDraw.Draw(img)
    
    # Animar cores ao longo do tempo
    progress = frame_num / total_frames
    
    # Criar gradiente radial animado
    center_x = width // 2 + int(math.sin(progress * math.pi * 2) * 100)
    center_y = height // 2 + int(math.cos(progress * math.pi * 2) * 50)
    
    max_radius = int(math.sqrt(width**2 + height**2))
    
    for r in range(max_radius, 0, -5):
        ratio = r / max_radius
        # Gradiente do centro para fora
        inner_color = lerp_color(DARK_BLUE, BLACK, ratio)
        outer_color = BLACK
        color = lerp_color(inner_color, outer_color, ratio * 0.5)
        
        # Desenhar círculo
        bbox = [center_x - r, center_y - r, center_x + r, center_y + r]
        draw.ellipse(bbox, fill=color)
    
    return img

def add_glow(draw, x, y, text, font, color, glow_radius=15, intensity=3):
    """Adiciona efeito glow ao texto"""
    # Glow externo (várias camadas para suavizar)
    for radius in range(glow_radius, 0, -2):
        alpha = int(50 * (1 - radius / glow_radius))
        glow_color = (*GOLD, alpha)
        for offset in range(-intensity, intensity + 1, 2):
            draw.text((x + offset, y + offset), text, font=font, fill=(*GOLD[:3], 30))

def draw_text_with_shadow(draw, x, y, text, font, text_color, shadow_color=BLACK, shadow_offset=4):
    """Desenha texto com sombra"""
    # Sombra
    draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=shadow_color)
    # Texto principal
    draw.text((x, y), text, font=font, fill=text_color)

def ease_out_cubic(t):
    """Easing suave"""
    return 1 - (1 - t) ** 3

def ease_in_out_back(t):
    """Easing com elasticidade"""
    c1 = 1.70158
    c2 = c1 * 1.525
    if t < 0.5:
        return ((2 * t) ** 2 * ((c2 + 1) * 2 * t - c2)) / 2
    else:
        return ((2 * t - 2) ** 2 * ((c2 + 1) * (2 * t - 2) + c2) + 2) / 2

def generate_frame(frame_num, total_frames, width, height):
    """Gera um único frame do vídeo"""
    img = create_gradient_bg(width, height, frame_num, total_frames)
    draw = ImageDraw.Draw(img)
    
    # Tempo em segundos
    time_sec = frame_num / 30.0
    
    # Criar fontes (fallback para default se não achar)
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        font_cta = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = font_title
        font_cta = font_title
        font_small = font_title
    
    # ====== CENA 1: HOOK (0-2.5s) ======
    if time_sec < 2.5:
        progress = ease_out_cubic(min(time_sec / 1.5, 1.0))
        
        # Badge "MSA" no topo
        badge_text = "🔥 MÉTODO VALIDADO"
        bbox = draw.textbbox((0, 0), badge_text, font=font_small)
        badge_w = bbox[2] - bbox[0] + 60
        badge_h = 70
        badge_x = (width - badge_w) // 2
        badge_y = 200
        
        # Fundo do badge com borda dourada
        draw.rounded_rectangle(
            [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
            radius=35,
            fill=(*GOLD, 40),
            outline=GOLD,
            width=3
        )
        draw.text((badge_x + 30, badge_y + 15), badge_text, font=font_small, fill=GOLD)
        
        # Número grande "R$ 47.000"
        number_text = "R$ 47.000"
        bbox = draw.textbbox((0, 0), number_text, font=font_title)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (width - text_w) // 2
        y = height // 2 - 100 - int((1 - progress) * 200)
        
        # Glow effect
        for i in range(20, 0, -2):
            alpha = int(30 * (1 - i / 20))
            draw.text((x + i//3, y + i//3), number_text, font=font_title, 
                     fill=(*GOLD, alpha))
        
        # Texto principal
        draw.text((x, y), number_text, font=font_title, fill=GOLD)
        
        # Subtítulo
        sub_text = "em 30 dias"
        bbox = draw.textbbox((0, 0), sub_text, font=font_subtitle)
        sub_w = bbox[2] - bbox[0]
        sub_x = (width - sub_w) // 2
        sub_y = y + 150
        
        opacity = int(255 * progress)
        draw.text((sub_x, sub_y), sub_text, font=font_subtitle, fill=(*WHITE, opacity))
    
    # ====== CENA 2: DOR (2.5-5s) ======
    elif time_sec < 5.0:
        local_time = time_sec - 2.5
        progress = ease_out_cubic(min(local_time / 1.5, 1.0))
        
        # Emoji animado
        emoji = "😫"
        emoji_size = 150
        emoji_y = height // 2 - 250 - int((1 - progress) * 100)
        
        # Sombra do emoji
        draw.text((width//2 - 40 + 5, emoji_y + 5), emoji, font=font_title, fill=BLACK)
        draw.text((width//2 - 40, emoji_y), emoji, font=font_title, fill=WHITE)
        
        # Texto
        text = "Cansada de trocar"
        bbox = draw.textbbox((0, 0), text, font=font_subtitle)
        text_w = bbox[2] - bbox[0]
        x = (width - text_w) // 2
        y = height // 2 + 50
        
        draw.text((x + 3, y + 3), text, font=font_subtitle, fill=BLACK)
        draw.text((x, y), text, font=font_subtitle, fill=WHITE)
        
        # Subtexto em destaque
        sub = "tempo por dinheiro?"
        bbox = draw.textbbox((0, 0), sub, font=font_title)
        sub_w = bbox[2] - bbox[0]
        sub_x = (width - sub_w) // 2
        sub_y = y + 120
        
        # Glow no subtexto
        for i in range(15, 0, -2):
            draw.text((sub_x + i//2, sub_y + i//2), sub, font=font_title, 
                     fill=(*GOLD, 40))
        
        draw.text((sub_x, sub_y), sub, font=font_title, fill=GOLD)
    
    # ====== CENA 3: SOLUÇÃO (5-7.5s) ======
    elif time_sec < 7.5:
        local_time = time_sec - 5.0
        progress = ease_out_cubic(min(local_time / 1.5, 1.0))
        
        # Emoji
        emoji = "🚀"
        emoji_y = height // 2 - 250
        draw.text((width//2 - 40 + 5, emoji_y + 5), emoji, font=font_title, fill=BLACK)
        draw.text((width//2 - 40, emoji_y), emoji, font=font_title, fill=GOLD)
        
        # Texto principal
        text = "Venda produtos"
        bbox = draw.textbbox((0, 0), text, font=font_subtitle)
        text_w = bbox[2] - bbox[0]
        x = (width - text_w) // 2
        y = height // 2 + 50
        
        draw.text((x + 3, y + 3), text, font=font_subtitle, fill=BLACK)
        draw.text((x, y), text, font=font_subtitle, fill=WHITE)
        
        # Subtexto destaque
        sub = "sem aparecer"
        bbox = draw.textbbox((0, 0), sub, font=font_title)
        sub_w = bbox[2] - bbox[0]
        sub_x = (width - sub_w) // 2
        sub_y = y + 120
        
        draw.text((sub_x, sub_y), sub, font=font_title, fill=GOLD)
    
    # ====== CENA 4: CTA (7.5-10s) ======
    else:
        local_time = time_sec - 7.5
        progress = ease_out_cubic(min(local_time / 1.5, 1.0))
        
        # Badge de urgência
        badge_text = "⚠️ ÚLTIMA CHANCE"
        bbox = draw.textbbox((0, 0), badge_text, font=font_small)
        badge_w = bbox[2] - bbox[0] + 60
        badge_h = 70
        badge_x = (width - badge_w) // 2
        badge_y = 250
        
        draw.rounded_rectangle(
            [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
            radius=35,
            fill=GOLD,
            outline=GOLD_LIGHT,
            width=3
        )
        draw.text((badge_x + 30, badge_y + 15), badge_text, font=font_small, fill=BLACK)
        
        # Texto CTA
        cta_text = "Garanta sua vaga"
        bbox = draw.textbbox((0, 0), cta_text, font=font_cta)
        cta_w = bbox[2] - bbox[0]
        cta_x = (width - cta_w) // 2
        cta_y = height // 2 - 80
        
        draw.text((cta_x + 4, cta_y + 4), cta_text, font=font_cta, fill=BLACK)
        draw.text((cta_x, cta_y), cta_text, font=font_cta, fill=WHITE)
        
        # Botão pulsante
        btn_text = "LINK NA BIO →"
        bbox = draw.textbbox((0, 0), btn_text, font=font_cta)
        btn_w = bbox[2] - bbox[0] + 100
        btn_h = 100
        btn_x = (width - btn_w) // 2
        btn_y = height // 2 + 80
        
        # Efeito pulsante
        pulse = abs(math.sin(local_time * 3)) * 10 + 5
        draw.rounded_rectangle(
            [btn_x - int(pulse), btn_y - int(pulse), 
             btn_x + btn_w + int(pulse), btn_y + btn_h + int(pulse)],
            radius=20,
            fill=(*GOLD, 30),
            outline=GOLD,
            width=3
        )
        
        draw.rounded_rectangle(
            [btn_x, btn_y, btn_x + btn_w, btn_y + btn_h],
            radius=20,
            fill=GOLD,
            outline=GOLD_LIGHT,
            width=2
        )
        
        draw.text((btn_x + 50, btn_y + 25), btn_text, font=font_cta, fill=BLACK)
        
        # Vagas
        vagas_text = "Só 15 vagas no grupo VIP"
        bbox = draw.textbbox((0, 0), vagas_text, font=font_small)
        vagas_w = bbox[2] - bbox[0]
        vagas_x = (width - vagas_w) // 2
        vagas_y = height // 2 + 220
        
        draw.text((vagas_x, vagas_y), vagas_text, font=font_small, fill=(*WHITE, 200))
    
    # Barra de progresso superior
    progress_ratio = frame_num / total_frames
    bar_width = width
    filled = int(bar_width * progress_ratio)
    
    # Fundo da barra
    draw.rectangle([0, 0, width, 8], fill=(30, 30, 30))
    # Barra preenchida com gradiente
    for x in range(filled):
        ratio = x / filled if filled > 0 else 0
        color = lerp_color(GOLD_DARK, GOLD_LIGHT, ratio)
        draw.line([(x, 0), (x, 8)], fill=color)
    
    return img

def main():
    print("🎬 Gerando vídeo profissional MSA...")
    
    # Configurações
    width, height = 1080, 1920
    fps = 30
    duration = 10  # segundos
    total_frames = fps * duration
    
    # Criar diretório de frames
    frames_dir = "/tmp/msa_frames"
    os.makedirs(frames_dir, exist_ok=True)
    
    # Limpar frames antigos
    for f in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, f))
    
    print(f"📸 Gerando {total_frames} frames...")
    
    # Gerar frames
    for i in range(total_frames):
        if i % 30 == 0:
            print(f"  Frame {i}/{total_frames} ({i*100//total_frames}%)")
        
        frame = generate_frame(i, total_frames, width, height)
        frame.save(f"{frames_dir}/frame_{i:04d}.png")
    
    print("🎞️ Compilando vídeo com FFmpeg...")
    
    output_path = "/root/.openclaw/workspace/projetos-msa/output/story_profissional.mp4"
    
    # Usar FFmpeg para criar vídeo
    cmd = [
        "ffmpeg",
        "-y",
        "-framerate", str(fps),
        "-i", f"{frames_dir}/frame_%04d.png",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "23",  # Qualidade boa
        "-preset", "fast",
        "-movflags", "+faststart",
        "-vf", "format=yuv420p",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Vídeo criado com sucesso!")
        print(f"📁 Local: {output_path}")
        
        # Verificar tamanho
        size = os.path.getsize(output_path)
        print(f"📊 Tamanho: {size / 1024:.1f} KB")
        print(f"⏱️ Duração: {duration}s")
        print(f"📐 Resolução: {width}x{height}")
        print(f"🎥 FPS: {fps}")
    else:
        print(f"❌ Erro: {result.stderr}")
        return False
    
    # Limpar frames
    for f in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, f))
    os.rmdir(frames_dir)
    
    return True

if __name__ == "__main__":
    main()
