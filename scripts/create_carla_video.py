#!/usr/bin/env python3
"""
Vídeo MSA Profissional com Foto da Carla — 10 segundos
Usa foto real + background + animações premium
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import subprocess
from pathlib import Path

# Cores MSA
GOLD = (201, 162, 39)
GOLD_LIGHT = (229, 193, 88)
GOLD_DARK = (168, 132, 32)
BLACK = (10, 10, 10)
DARK_BLUE = (22, 33, 62)
WHITE = (255, 255, 255)

def load_carla_photo():
    """Carrega e prepara foto da Carla"""
    photo_path = "/root/.openclaw/workspace/projetos-msa/assets/imagens/carla_foto_evento.jpg"
    if os.path.exists(photo_path):
        img = Image.open(photo_path)
        # Converter para RGB se necessário
        if img.mode != 'RGB':
            img = img.convert('RGB')
        return img
    return None

def load_background():
    """Carrega background gerado"""
    bg_path = "/root/.openclaw/workspace/projetos-msa/assets/imagens/background_vsl.jpg"
    if os.path.exists(bg_path):
        return Image.open(bg_path).convert('RGB')
    return None

def create_gradient_overlay(width, height, alpha=128):
    """Cria overlay gradiente escuro para legibilidade"""
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Gradiente do topo (mais escuro) para baixo
    for y in range(height):
        ratio = y / height
        alpha_val = int(alpha * (1 - ratio * 0.5))
        draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha_val))
    
    return overlay

def add_glow_text(draw, x, y, text, font, color, glow_radius=20, intensity=5):
    """Adiciona texto com efeito glow dourado"""
    # Glow externo
    for radius in range(glow_radius, 0, -2):
        alpha = int(40 * (1 - radius / glow_radius))
        for offset_x in range(-intensity, intensity + 1, 2):
            for offset_y in range(-intensity, intensity + 1, 2):
                if offset_x == 0 and offset_y == 0:
                    continue
                draw.text((x + offset_x, y + offset_y), text, font=font, 
                         fill=(*GOLD, alpha))

def draw_text_shadow(draw, x, y, text, font, text_color, shadow_offset=4):
    """Desenha texto com sombra forte"""
    # Sombra múltipla para profundidade
    for i in range(shadow_offset, 0, -1):
        alpha = int(100 * (1 - i / shadow_offset))
        draw.text((x + i, y + i), text, font=font, 
                 fill=(0, 0, 0, alpha))
    # Texto principal
    draw.text((x, y), text, font=font, fill=text_color)

def ease_out_cubic(t):
    """Easing suave"""
    return 1 - (1 - t) ** 3

def ease_out_back(t):
    """Easing com elasticidade"""
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2

def ease_elastic(t):
    """Easing elástico dramático"""
    if t == 0:
        return 0
    if t == 1:
        return 1
    return math.pow(2, -10 * t) * math.sin((t * 10 - 0.75) * (2 * math.pi) / 3) + 1

def create_frame(frame_num, total_frames, width, height, carla_photo, background):
    """Gera um frame do vídeo com foto da Carla"""
    
    # Tempo em segundos
    time_sec = frame_num / 30.0
    
    # ===== BACKGROUND =====
    if background:
        # Redimensionar background para o tamanho do vídeo
        bg = background.copy()
        bg = bg.resize((width, height), Image.LANCZOS)
        
        # Aplicar leve desfoque no background
        bg = bg.filter(ImageFilter.GaussianBlur(radius=2))
    else:
        # Criar gradiente se não tiver background
        bg = Image.new('RGB', (width, height), BLACK)
        draw_bg = ImageDraw.Draw(bg)
        for y in range(height):
            ratio = y / height
            r = int(10 + 16 * ratio)
            g = int(10 + 9 * ratio)
            b = int(10 + 52 * ratio)
            draw_bg.line([(0, y), (width, y)], fill=(r, g, b))
    
    # ===== OVERLAY ESCURO =====
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    
    # Gradiente escuro do topo
    for y in range(height):
        ratio = y / height
        alpha = int(120 * (1 - ratio * 0.3))
        draw_overlay.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))
    
    # Combinar background + overlay
    bg = Image.alpha_composite(bg.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(bg)
    
    # ===== FONTES =====
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 100)
        font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
        font_cta = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 35)
        font_emoji = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = font_title
        font_cta = font_title
        font_small = font_title
        font_emoji = font_title
    
    # ===== FOTO DA CARLA =====
    if carla_photo:
        # Tamanho da foto (lado esquerdo, grande)
        photo_width = int(width * 0.55)
        photo_height = int(photo_width * carla_photo.height / carla_photo.width)
        
        # Limitar altura
        if photo_height > height * 0.75:
            photo_height = int(height * 0.75)
            photo_width = int(photo_height * carla_photo.width / carla_photo.height)
        
        # Redimensionar
        photo = carla_photo.copy()
        photo = photo.resize((photo_width, photo_height), Image.LANCZOS)
        
        # Criar máscara circular/suave para a foto
        mask = Image.new('L', (photo_width, photo_height), 0)
        mask_draw = ImageDraw.Draw(mask)
        
        # Bordas arredondadas
        radius = 30
        mask_draw.rounded_rectangle([0, 0, photo_width, photo_height], radius=radius, fill=255)
        
        # Aplicar máscara
        photo_rgba = photo.convert('RGBA')
        photo_rgba.putalpha(mask)
        
        # Posição (esquerda, centralizada vertical)
        photo_x = int(width * 0.05)
        photo_y = (height - photo_height) // 2 + 50
        
        # ===== CENA 1: HOOK (0-2.5s) =====
        if time_sec < 2.5:
            progress = ease_out_cubic(min(time_sec / 1.5, 1.0))
            
            # Foto entra da esquerda
            photo_offset = int((1 - progress) * -200)
            bg.paste(photo_rgba, (photo_x + photo_offset, photo_y), photo_rgba)
            
            # Borda dourada na foto
            border_padding = 5
            draw.rounded_rectangle(
                [photo_x + photo_offset - border_padding, 
                 photo_y - border_padding,
                 photo_x + photo_offset + photo_width + border_padding,
                 photo_y + photo_height + border_padding],
                radius=radius + border_padding,
                outline=GOLD,
                width=4
            )
            
            # Texto na direita
            text_x = photo_x + photo_width + 80
            
            # Badge "MSA"
            badge_text = "🔥 MSA"
            bbox = draw.textbbox((0, 0), badge_text, font=font_small)
            badge_w = bbox[2] - bbox[0] + 50
            badge_h = 60
            badge_y = photo_y + 50
            
            # Fundo do badge
            draw.rounded_rectangle(
                [text_x, badge_y, text_x + badge_w, badge_y + badge_h],
                radius=30,
                fill=GOLD
            )
            draw.text((text_x + 25, badge_y + 12), badge_text, font=font_small, fill=BLACK)
            
            # Título principal
            title = "R$ 47.000"
            bbox = draw.textbbox((0, 0), title, font=font_title)
            title_w = bbox[2] - bbox[0]
            title_y = badge_y + 100
            
            # Glow no título
            for i in range(15, 0, -2):
                alpha = int(30 * (1 - i / 15))
                draw.text((text_x + i//2, title_y + i//2), title, font=font_title, 
                         fill=(*GOLD, alpha))
            
            draw.text((text_x, title_y), title, font=font_title, fill=GOLD)
            
            # Subtítulo
            sub = "em 30 dias"
            bbox = draw.textbbox((0, 0), sub, font=font_subtitle)
            sub_w = bbox[2] - bbox[0]
            sub_y = title_y + 130
            
            opacity = int(255 * progress)
            draw.text((text_x, sub_y), sub, font=font_subtitle, fill=(*WHITE, opacity))
            
            # Descrição
            desc = "Sem aparecer."
            desc2 = "Sem estoque."
            desc_y = sub_y + 100
            draw.text((text_x, desc_y), desc, font=font_small, fill=(*WHITE, 200))
            draw.text((text_x, desc_y + 45), desc2, font=font_small, fill=(*WHITE, 200))
        
        # ===== CENA 2: DOR (2.5-5s) =====
        elif time_sec < 5.0:
            local_time = time_sec - 2.5
            progress = ease_out_cubic(min(local_time / 1.5, 1.0))
            
            # Foto desaparece suavemente
            photo_alpha = int(255 * (1 - progress * 0.3))
            photo_rgba.putalpha(Image.new('L', (photo_width, photo_height), photo_alpha))
            bg.paste(photo_rgba, (photo_x, photo_y), photo_rgba)
            
            # Texto central grande
            text = "CANSADA DE"
            bbox = draw.textbbox((0, 0), text, font=font_title)
            text_w = bbox[2] - bbox[0]
            text_x = (width - text_w) // 2
            text_y = height // 2 - 150
            
            # Sombra forte
            for i in range(8, 0, -1):
                draw.text((text_x + i, text_y + i), text, font=font_title, 
                         fill=(0, 0, 0, 80))
            draw.text((text_x, text_y), text, font=font_title, fill=WHITE)
            
            # Destaque dourado
            sub = "trocar tempo"
            sub2 = "por dinheiro?"
            bbox = draw.textbbox((0, 0), sub, font=font_title)
            sub_w = bbox[2] - bbox[0]
            sub_x = (width - sub_w) // 2
            sub_y = text_y + 130
            
            # Glow dourado
            for i in range(20, 0, -2):
                alpha = int(40 * (1 - i / 20))
                draw.text((sub_x + i//2, sub_y + i//2), sub, font=font_title, 
                         fill=(*GOLD, alpha))
                draw.text((sub_x + i//2, sub_y + 120 + i//2), sub2, font=font_title, 
                         fill=(*GOLD, alpha))
            
            draw.text((sub_x, sub_y), sub, font=font_title, fill=GOLD)
            draw.text((sub_x, sub_y + 120), sub2, font=font_title, fill=GOLD)
        
        # ===== CENA 3: SOLUÇÃO (5-7.5s) =====
        elif time_sec < 7.5:
            local_time = time_sec - 5.0
            progress = ease_out_cubic(min(local_time / 1.5, 1.0))
            
            # Foto reaparece do lado direito
            photo_offset = int((1 - progress) * 300)
            photo_x_right = width - photo_width - int(width * 0.05) + photo_offset
            bg.paste(photo_rgba, (photo_x_right, photo_y), photo_rgba)
            
            # Texto na esquerda
            text_x = int(width * 0.08)
            
            # Emoji
            emoji = "🚀"
            draw.text((text_x, photo_y), emoji, font=font_emoji, fill=GOLD)
            
            # Título
            title = "VENDA"
            bbox = draw.textbbox((0, 0), title, font=font_title)
            title_y = photo_y + 100
            draw.text((text_x, title_y), title, font=font_title, fill=WHITE)
            
            # Subtítulo dourado
            sub = "produtos online"
            bbox = draw.textbbox((0, 0), sub, font=font_subtitle)
            sub_y = title_y + 130
            draw.text((text_x, sub_y), sub, font=font_subtitle, fill=GOLD)
            
            # Benefícios
            benefs = ["✓ Sem aparecer", "✓ Sem estoque", "✓ 3-4h por dia"]
            benef_y = sub_y + 120
            for i, benef in enumerate(benefs):
                y = benef_y + i * 50
                draw.text((text_x, y), benef, font=font_small, fill=(*WHITE, 220))
        
        # ===== CENA 4: CTA (7.5-10s) =====
        else:
            local_time = time_sec - 7.5
            progress = ease_out_cubic(min(local_time / 1.5, 1.0))
            
            # Foto no centro, circular
            circle_size = min(photo_width, photo_height)
            photo_circle = photo.copy()
            photo_circle = photo_circle.resize((circle_size, circle_size), Image.LANCZOS)
            
            # Máscara circular
            mask_circle = Image.new('L', (circle_size, circle_size), 0)
            mask_draw = ImageDraw.Draw(mask_circle)
            mask_draw.ellipse([0, 0, circle_size, circle_size], fill=255)
            
            photo_circle_rgba = photo_circle.convert('RGBA')
            photo_circle_rgba.putalpha(mask_circle)
            
            circle_x = (width - circle_size) // 2
            circle_y = height // 2 - circle_size - 50
            
            # Borda dourada pulsante
            pulse = abs(math.sin(local_time * 4)) * 15 + 5
            draw.ellipse(
                [circle_x - int(pulse), circle_y - int(pulse),
                 circle_x + circle_size + int(pulse), circle_y + circle_size + int(pulse)],
                outline=GOLD,
                width=4
            )
            
            bg.paste(photo_circle_rgba, (circle_x, circle_y), photo_circle_rgba)
            
            # Texto CTA
            cta_text = "GARANTA SUA VAGA"
            bbox = draw.textbbox((0, 0), cta_text, font=font_cta)
            cta_w = bbox[2] - bbox[0]
            cta_x = (width - cta_w) // 2
            cta_y = circle_y + circle_size + 50
            
            # Glow no CTA
            for i in range(15, 0, -2):
                alpha = int(50 * (1 - i / 15))
                draw.text((cta_x + i//2, cta_y + i//2), cta_text, font=font_cta, 
                         fill=(*GOLD, alpha))
            
            draw.text((cta_x, cta_y), cta_text, font=font_cta, fill=GOLD)
            
            # Botão
            btn_text = "LINK NA BIO →"
            bbox = draw.textbbox((0, 0), btn_text, font=font_cta)
            btn_w = bbox[2] - bbox[0] + 80
            btn_h = 80
            btn_x = (width - btn_w) // 2
            btn_y = cta_y + 100
            
            # Botão pulsante
            pulse_btn = abs(math.sin(local_time * 3)) * 8 + 4
            draw.rounded_rectangle(
                [btn_x - int(pulse_btn), btn_y - int(pulse_btn),
                 btn_x + btn_w + int(pulse_btn), btn_y + btn_h + int(pulse_btn)],
                radius=20,
                fill=(*GOLD, 40),
                outline=GOLD,
                width=3
            )
            
            draw.rounded_rectangle(
                [btn_x, btn_y, btn_x + btn_w, btn_y + btn_h],
                radius=20,
                fill=GOLD
            )
            
            draw.text((btn_x + 40, btn_y + 20), btn_text, font=font_cta, fill=BLACK)
            
            # Urgência
            vagas = "⚠️ Só 15 vagas no grupo VIP"
            bbox = draw.textbbox((0, 0), vagas, font=font_small)
            vagas_w = bbox[2] - bbox[0]
            vagas_x = (width - vagas_w) // 2
            vagas_y = btn_y + 120
            draw.text((vagas_x, vagas_y), vagas, font=font_small, fill=(*WHITE, 180))
    
    # ===== BARRA DE PROGRESSO =====
    progress_ratio = frame_num / total_frames
    bar_height = 8
    draw.rectangle([0, 0, width, bar_height], fill=(30, 30, 30))
    filled = int(width * progress_ratio)
    
    # Gradiente dourado na barra
    for x in range(filled):
        ratio = x / filled if filled > 0 else 0
        # Interpolar entre GOLD_DARK e GOLD_LIGHT
        r = int(GOLD_DARK[0] + (GOLD_LIGHT[0] - GOLD_DARK[0]) * ratio)
        g = int(GOLD_DARK[1] + (GOLD_LIGHT[1] - GOLD_DARK[1]) * ratio)
        b = int(GOLD_DARK[2] + (GOLD_LIGHT[2] - GOLD_DARK[2]) * ratio)
        draw.line([(x, 0), (x, bar_height)], fill=(r, g, b))
    
    return bg

def main():
    print("🎬 Gerando vídeo MSA PROFISSIONAL com foto da Carla...")
    
    # Carregar recursos
    carla_photo = load_carla_photo()
    background = load_background()
    
    if carla_photo:
        print(f"✅ Foto da Carla carregada: {carla_photo.size}")
    else:
        print("⚠️ Foto da Carla não encontrada, usando texto apenas")
    
    if background:
        print(f"✅ Background carregado: {background.size}")
    else:
        print("⚠️ Background não encontrado, usando gradiente")
    
    # Configurações
    width, height = 1080, 1920
    fps = 30
    duration = 10  # segundos
    total_frames = fps * duration
    
    # Criar diretório de frames
    frames_dir = "/tmp/msa_carla_frames"
    os.makedirs(frames_dir, exist_ok=True)
    
    # Limpar frames antigos
    for f in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, f))
    
    print(f"\n📸 Gerando {total_frames} frames...")
    
    # Gerar frames
    for i in range(total_frames):
        if i % 30 == 0:
            print(f"  Frame {i}/{total_frames} ({i*100//total_frames}%)")
        
        frame = create_frame(i, total_frames, width, height, carla_photo, background)
        frame.save(f"{frames_dir}/frame_{i:04d}.png")
    
    print("\n🎞️ Compilando vídeo com FFmpeg...")
    
    output_path = "/root/.openclaw/workspace/projetos-msa/output/story_carla_pro.mp4"
    
    cmd = [
        "ffmpeg",
        "-y",
        "-framerate", str(fps),
        "-i", f"{frames_dir}/frame_%04d.png",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "23",
        "-preset", "fast",
        "-movflags", "+faststart",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Vídeo criado com sucesso!")
        print(f"📁 Local: {output_path}")
        
        size = os.path.getsize(output_path)
        print(f"📊 Tamanho: {size / 1024:.1f} KB")
        print(f"⏱️ Duração: {duration}s")
        print(f"📐 Resolução: {width}x{height}")
        print(f"🎥 FPS: {fps}")
    else:
        print(f"❌ Erro FFmpeg: {result.stderr[:500]}")
        return False
    
    # Limpar frames
    for f in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, f))
    os.rmdir(frames_dir)
    
    return True

if __name__ == "__main__":
    main()
