#!/usr/bin/env python3
"""
Vídeo MSA PREMIUM — Meta Ads Professional
Alta conversão, estilo premium, prova social
"""
import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import subprocess
import numpy as np

# ============================================
# CORES PREMIUM MSA
# ============================================
GOLD = (201, 162, 39)
GOLD_LIGHT = (229, 193, 88)
GOLD_BRIGHT = (255, 215, 100)
GOLD_DARK = (140, 110, 20)
BLACK = (8, 8, 15)
DARK_NAVY = (15, 20, 40)
DARK_BLUE = (25, 30, 60)
WHITE = (255, 255, 255)
WHITE_SOFT = (230, 230, 240)
GRAY = (120, 120, 140)

def lerp(a, b, t):
    """Interpolação linear"""
    return a + (b - a) * t

def lerp_color(c1, c2, t):
    """Interpolação entre cores"""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

def ease_out_expo(t):
    """Exponential ease out - rápido no início, suave no final"""
    return 1.0 if t >= 1 else 1.0 - math.pow(2, -10 * t)

def ease_out_back(t):
    """Back ease out com overshoot sutil"""
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * math.pow(t - 1, 3) + c1 * math.pow(t - 1, 2)

def ease_in_out_cubic(t):
    """Cubic ease in-out"""
    return 4 * t * t * t if t < 0.5 else 1 - math.pow(-2 * t + 2, 3) / 2

def create_premium_background(width, height, frame_num, total_frames):
    """Background premium com gradiente animado e partículas"""
    progress = frame_num / total_frames
    
    # Base gradiente animado
    img = Image.new('RGB', (width, height), BLACK)
    draw = ImageDraw.Draw(img)
    
    # Gradiente radial sutil que se move
    center_x = width // 2 + math.sin(progress * math.pi * 2) * 50
    center_y = height // 2 + math.cos(progress * math.pi * 3) * 30
    
    max_r = int(math.sqrt(width**2 + height**2))
    
    for r in range(max_r, 0, -8):
        ratio = r / max_r
        # Gradiente do centro (azul escuro) para fora (preto)
        inner = lerp_color(DARK_NAVY, DARK_BLUE, 0.3 + math.sin(progress * 4) * 0.2)
        outer = BLACK
        color = lerp_color(inner, outer, ratio * 0.7)
        
        # Desenhar círculo com alpha simulado
        draw.ellipse([
            center_x - r, center_y - r,
            center_x + r, center_y + r
        ], fill=color)
    
    # Partículas douradas sutis
    random.seed(42)  # Seed fixo para consistência
    particles = []
    for i in range(30):
        px = random.randint(0, width)
        py = random.randint(0, height)
        size = random.randint(2, 5)
        speed = random.uniform(0.5, 2.0)
        phase = random.uniform(0, math.pi * 2)
        particles.append((px, py, size, speed, phase))
    
    for px, py, size, speed, phase in particles:
        # Animar posição Y
        anim_y = py + math.sin(progress * speed * 10 + phase) * 20
        anim_alpha = int(100 + math.sin(progress * speed * 5 + phase) * 60)
        
        # Desenhar partícula com glow
        for r in range(size + 3, 0, -1):
            alpha = int(anim_alpha * (1 - r / (size + 3)))
            color = (*GOLD, alpha) if len(GOLD) == 3 else (*GOLD[:3], alpha)
            draw.ellipse([
                px - r, int(anim_y) - r,
                px + r, int(anim_y) + r
            ], fill=color[:3])
    
    # Light leak dourado sutil no canto superior
    leak_x = width * 0.7 + math.sin(progress * 3) * 100
    leak_y = -100 + math.cos(progress * 2) * 50
    for r in range(400, 0, -10):
        alpha = int(15 * (1 - r / 400))
        draw.ellipse([
            leak_x - r, leak_y - r,
            leak_x + r, leak_y + r
        ], fill=(*GOLD, alpha)[:3])
    
    return img

def draw_glow_text(draw, x, y, text, font, color, glow_radius=25, intensity=6):
    """Desenha texto com glow premium"""
    # Múltiplas camadas de glow para suavidade
    for radius in range(glow_radius, 0, -2):
        alpha = int(50 * (1 - radius / glow_radius))
        for ox in range(-intensity, intensity + 1, 2):
            for oy in range(-intensity, intensity + 1, 2):
                if ox == 0 and oy == 0:
                    continue
                draw.text((x + ox, y + oy), text, font=font, fill=(*color[:3], alpha))

def draw_text_premium(draw, x, y, text, font, color, shadow=True):
    """Desenha texto com sombra profissional"""
    if shadow:
        # Sombra múltipla para profundidade
        for i in range(8, 0, -1):
            alpha = int(80 * (1 - i / 8))
            draw.text((x + i, y + i), text, font=font, fill=(0, 0, 0))
    draw.text((x, y), text, font=font, fill=color)

def create_shine_effect(draw, x, y, width, height, progress):
    """Efeito de brilho metálico passando"""
    shine_pos = (progress * (width + 200)) - 100
    
    for i in range(20):
        offset = i - 10
        alpha = int(30 * (1 - abs(offset) / 10))
        line_x = int(shine_pos + offset)
        if 0 <= line_x < width:
            draw.line([(x + line_x, y), (x + line_x, y + height)], fill=(*GOLD_BRIGHT, alpha)[:3])

def load_image_safe(path, size=None):
    """Carrega imagem com tratamento de erro"""
    try:
        if os.path.exists(path):
            img = Image.open(path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            if size:
                img = img.resize(size, Image.LANCZOS)
            return img
    except Exception as e:
        print(f"Erro ao carregar {path}: {e}")
    return None

def create_circular_mask(size):
    """Cria máscara circular com borda suave"""
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    
    # Círculo principal
    draw.ellipse([0, 0, size, size], fill=255)
    
    # Borda suave (anti-aliasing manual)
    border = 3
    for i in range(border, 0, -1):
        alpha = int(255 * (1 - i / border))
        draw.ellipse([i, i, size - i, size - i], fill=255)
    
    return mask

def create_rounded_card(width, height, radius=30):
    """Cria card com cantos arredondados e sombra 3D"""
    # Base do card
    card = Image.new('RGBA', (width + 40, height + 60), (0, 0, 0, 0))
    
    # Sombra 3D
    shadow = Image.new('RGBA', (width + 40, height + 60), (0, 0, 0, 0))
    draw_shadow = ImageDraw.Draw(shadow)
    draw_shadow.rounded_rectangle(
        [20, 30, 20 + width, 30 + height],
        radius=radius,
        fill=(0, 0, 0, 80)
    )
    
    # Card principal com gradiente
    card_main = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw_card = ImageDraw.Draw(card_main)
    
    # Fundo semi-transparente com gradiente
    for y in range(height):
        ratio = y / height
        alpha = int(180 + (20 * ratio))
        color = (*DARK_NAVY, alpha)
        draw_card.line([0, y, width, y], fill=color)
    
    # Borda dourada
    border = 3
    draw_card.rounded_rectangle(
        [border, border, width - border, height - border],
        radius=radius - 5,
        outline=(*GOLD, 200),
        width=border
    )
    
    # Brilho na borda superior
    draw_card.line([radius, 2, width - radius, 2], fill=(*GOLD_LIGHT, 150), width=2)
    
    # Combinar
    result = Image.new('RGBA', (width + 40, height + 60), (0, 0, 0, 0))
    result.paste(shadow, (0, 0), shadow)
    result.paste(card_main, (20, 20), card_main)
    
    return result

# ============================================
# FONTES
# ============================================
def get_fonts():
    """Carrega fontes do sistema"""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                return {
                    'title': ImageFont.truetype(path, 120),
                    'subtitle': ImageFont.truetype(path, 80),
                    'cta': ImageFont.truetype(path, 65),
                    'small': ImageFont.truetype(path, 40),
                    'badge': ImageFont.truetype(path, 35),
                    'number': ImageFont.truetype(path, 140),
                    'number_small': ImageFont.truetype(path, 100),
                }
            except:
                continue
    
    # Fallback
    default = ImageFont.load_default()
    return {k: default for k in ['title', 'subtitle', 'cta', 'small', 'badge', 'number', 'number_small']}

# ============================================
# GERADOR DE FRAMES
# ============================================
def generate_frame(frame_num, total_frames, width, height, assets):
    """Gera um único frame do vídeo premium"""
    time_sec = frame_num / 30.0
    fonts = get_fonts()
    
    # === TELA 1: IMPACTO (0-3.5s) ===
    if time_sec < 3.5:
        local_time = time_sec
        progress = ease_out_expo(min(local_time / 1.2, 1.0))
        
        # Background premium
        bg = create_premium_background(width, height, frame_num, total_frames)
        draw = ImageDraw.Draw(bg)
        
        # === FOTO CIRCULAR COM BORDA DOURADA ===
        if assets['carla']:
            photo_size = 280
            carla = assets['carla'].copy().resize((photo_size, photo_size), Image.LANCZOS)
            
            # Máscara circular com anti-aliasing
            mask = create_circular_mask(photo_size)
            carla_rgba = carla.convert('RGBA')
            carla_rgba.putalpha(mask)
            
            photo_x = (width - photo_size) // 2
            photo_y = 120 + int((1 - progress) * 50)
            
            # Borda dourada brilhante com pulsação
            pulse = 1.0 + math.sin(time_sec * 4) * 0.08
            border_width = int(6 * pulse)
            
            # Glow externo da borda
            for r in range(border_width + 15, border_width, -2):
                alpha = int(60 * (1 - (r - border_width) / 15))
                draw.ellipse([
                    photo_x - r, photo_y - r,
                    photo_x + photo_size + r, photo_y + photo_size + r
                ], outline=(*GOLD, alpha)[:3], width=2)
            
            # Borda principal dourada
            draw.ellipse([
                photo_x - border_width, photo_y - border_width,
                photo_x + photo_size + border_width, photo_y + photo_size + border_width
            ], outline=GOLD, width=border_width)
            
            # Brilho na borda superior
            shine_angle = (time_sec * 3) % (2 * math.pi)
            shine_x = photo_x + photo_size // 2 + int(math.cos(shine_angle) * (photo_size // 2 + 10))
            shine_y = photo_y + photo_size // 2 + int(math.sin(shine_angle) * (photo_size // 2 + 10))
            
            for r in range(15, 0, -2):
                alpha = int(80 * (1 - r / 15))
                draw.ellipse([shine_x - r, shine_y - r, shine_x + r, shine_y + r], 
                           fill=(*GOLD_BRIGHT, alpha)[:3])
            
            bg.paste(carla_rgba, (photo_x, photo_y), carla_rgba)
        
        # === TEXTO PRINCIPAL: R$ 47.000 ===
        title_text = "R$ 47.000"
        bbox = draw.textbbox((0, 0), title_text, font=fonts['number'])
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        tx = (width - tw) // 2
        ty = 480 + int((1 - progress) * 80)
        
        # Animação de contagem (efeito de números subindo)
        count_progress = ease_out_expo(min(local_time / 1.5, 1.0))
        
        # Glow intenso atrás do número
        for r in range(40, 0, -3):
            alpha = int(50 * (1 - r / 40) * count_progress)
            glow_color = (*GOLD, alpha)[:3]
            for ox in range(-8, 9, 4):
                for oy in range(-8, 9, 4):
                    draw.text((tx + ox, ty + oy), title_text, font=fonts['number'], fill=glow_color)
        
        # Efeito shine passando
        create_shine_effect(draw, tx - 50, ty - 20, tw + 100, th + 40, 
                          (time_sec * 0.8) % 1.5)
        
        # Texto principal dourado
        draw_text_premium(draw, tx, ty, title_text, fonts['number'], GOLD)
        
        # === SUBTÍTULO: em 30 dias ===
        sub_text = "em 30 dias"
        bbox = draw.textbbox((0, 0), sub_text, font=fonts['subtitle'])
        sw = bbox[2] - bbox[0]
        sx = (width - sw) // 2
        sy = ty + 160
        
        sub_progress = ease_out_expo(min(max(local_time - 0.5, 0) / 1.0, 1.0))
        sub_y = sy + int((1 - sub_progress) * 40)
        sub_alpha = int(255 * sub_progress)
        
        # Sombra suave
        draw.text((sx + 2, sub_y + 2), sub_text, font=fonts['subtitle'], fill=(0, 0, 0))
        draw.text((sx, sub_y), sub_text, font=fonts['subtitle'], 
                 fill=(*WHITE, sub_alpha)[:3] if sub_alpha < 255 else WHITE)
        
        # === DESCRIÇÃO: Sem aparecer. Sem estoque. ===
        desc_text = "Sem aparerer.    Sem estoque."
        bbox = draw.textbbox((0, 0), desc_text, font=fonts['small'])
        dw = bbox[2] - bbox[0]
        dx = (width - dw) // 2
        dy = sy + 100
        
        desc_progress = ease_out_expo(min(max(local_time - 0.8, 0) / 1.0, 1.0))
        desc_y = dy + int((1 - desc_progress) * 30)
        desc_alpha = int(255 * desc_progress)
        
        draw.text((dx + 1, desc_y + 1), desc_text, font=fonts['small'], fill=(0, 0, 0))
        draw.text((dx, desc_y), desc_text, font=fonts['small'], 
                 fill=(*WHITE_SOFT, desc_alpha)[:3] if desc_alpha < 255 else WHITE_SOFT)
    
    # === TELA 2: PROVA SOCIAL (3.5-7.5s) ===
    elif time_sec < 7.5:
        local_time = time_sec - 3.5
        
        # Transição: zoom + blur do background
        transition_progress = ease_in_out_cubic(min(local_time / 0.5, 1.0))
        
        # Background com zoom sutil
        bg = create_premium_background(width, height, frame_num, total_frames)
        
        # Aplicar zoom durante transição
        if transition_progress < 1.0:
            zoom_factor = 1.0 + (1.0 - transition_progress) * 0.1
            new_size = (int(width * zoom_factor), int(height * zoom_factor))
            bg = bg.resize(new_size, Image.LANCZOS)
            
            # Crop central
            left = (new_size[0] - width) // 2
            top = (new_size[1] - height) // 2
            bg = bg.crop([left, top, left + width, top + height])
        
        # Overlay escuro para destacar card
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        ov_draw = ImageDraw.Draw(overlay)
        for y in range(height):
            ov_draw.line([(0, y), (width, y)], fill=(0, 0, 0, 160))
        bg = Image.alpha_composite(bg.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(bg)
        
        # === CARD FLOTANTE COM PROVA ===
        card_progress = ease_out_back(min(max(local_time - 0.3, 0) / 1.0, 1.0))
        
        if assets['prova']:
            prova = assets['prova'].copy()
            
            # Tamanho do card
            card_w = int(width * 0.82)
            card_h = int(card_w * 0.75)  # Proporção do print
            
            # Redimensionar print
            prova_resized = prova.resize((card_w - 60, card_h - 80), Image.LANCZOS)
            
            # Criar card com sombra 3D
            card_total_w = card_w + 40
            card_total_h = card_h + 80
            
            card = Image.new('RGBA', (card_total_w, card_total_h), (0, 0, 0, 0))
            
            # Sombra 3D deslocada
            shadow = Image.new('RGBA', (card_total_w, card_total_h), (0, 0, 0, 0))
            sd = ImageDraw.Draw(shadow)
            sd.rounded_rectangle(
                [25, 45, 25 + card_w, 45 + card_h],
                radius=25,
                fill=(0, 0, 0, 100)
            )
            card.paste(shadow, (0, 0), shadow)
            
            # Fundo do card com gradiente
            card_bg = Image.new('RGBA', (card_w, card_h), (0, 0, 0, 0))
            cbg = ImageDraw.Draw(card_bg)
            
            for y in range(card_h):
                ratio = y / card_h
                alpha = int(200 + 30 * ratio)
                color = (*lerp_color(DARK_NAVY, DARK_BLUE, ratio), alpha)
                cbg.line([0, y, card_w, y], fill=color)
            
            # Borda dourada
            border = 4
            cbg.rounded_rectangle(
                [border, border, card_w - border, card_h - border],
                radius=22,
                outline=(*GOLD, 220),
                width=border
            )
            
            # Brilho na borda superior
            cbg.line([22, 2, card_w - 22, 2], fill=(*GOLD_LIGHT, 150), width=3)
            
            card.paste(card_bg, (20, 20), card_bg)
            
            # Colar print dentro do card
            print_x = 20 + 30
            print_y = 20 + 40
            card.paste(prova_resized, (print_x, print_y))
            
            # Posição do card (flutuando com bounce)
            card_x = (width - card_total_w) // 2
            card_y = 180 + int((1 - card_progress) * 100)
            
            # Animação flutuante sutil
            float_y = int(math.sin(time_sec * 2) * 5)
            
            bg.paste(card, (card_x, card_y + float_y), card)
        
        # === BADGE "PROVA REAL" ===
        badge_progress = ease_out_expo(min(max(local_time - 0.5, 0) / 0.8, 1.0))
        
        badge_text = "📲 PROVA REAL"
        bbox = draw.textbbox((0, 0), badge_text, font=fonts['badge'])
        bw = bbox[2] - bbox[0] + 50
        bh = 55
        bx = (width - bw) // 2
        by = 80 + int((1 - badge_progress) * 30)
        
        # Fundo do badge com gradiente
        badge_bg = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
        bbg = ImageDraw.Draw(badge_bg)
        for x in range(bw):
            ratio = x / bw
            color = (*lerp_color(GOLD_DARK, GOLD, ratio), int(230 * badge_progress))
            bbg.line([x, 0, x, bh], fill=color)
        
        bbg.rounded_rectangle([0, 0, bw, bh], radius=28, outline=(*GOLD_LIGHT, int(200 * badge_progress)), width=2)
        
        # Badge shine
        shine_pos = int((time_sec * 2) % (bw + 100)) - 50
        for i in range(30):
            sx = shine_pos + i - 15
            if 0 <= sx < bw:
                alpha = int(80 * (1 - abs(i - 15) / 15) * badge_progress)
                bbg.line([sx, 0, sx, bh], fill=(*GOLD_BRIGHT, alpha))
        
        bg.paste(badge_bg, (bx, by), badge_bg)
        draw.text((bx + 25, by + 12), badge_text, font=fonts['badge'], fill=BLACK)
        
        # === TEXTO ABAIXO DO CARD ===
        text_progress = ease_out_expo(min(max(local_time - 0.8, 0) / 0.8, 1.0))
        
        text1 = "Faturamento em 7 dias:"
        bbox = draw.textbbox((0, 0), text1, font=fonts['small'])
        tw = bbox[2] - bbox[0]
        tx = (width - tw) // 2
        ty = 850 + int((1 - text_progress) * 30)
        
        draw.text((tx + 2, ty + 2), text1, font=fonts['small'], fill=(0, 0, 0))
        draw.text((tx, ty), text1, font=fonts['small'], fill=WHITE)
        
        # === VALOR EM DESTAQUE: R$ 8.594,83 ===
        val_progress = ease_out_back(min(max(local_time - 1.0, 0) / 0.8, 1.0))
        
        val_text = "R$ 8.594,83"
        bbox = draw.textbbox((0, 0), val_text, font=fonts['number'])
        vw = bbox[2] - bbox[0]
        vx = (width - vw) // 2
        vy = 920 + int((1 - val_progress) * 40)
        
        # Glow intenso
        for r in range(30, 0, -2):
            alpha = int(60 * (1 - r / 30) * val_progress)
            for ox in range(-6, 7, 3):
                for oy in range(-6, 7, 3):
                    draw.text((vx + ox, vy + oy), val_text, font=fonts['number'], 
                             fill=(*GOLD, alpha)[:3])
        
        # Shine no valor
        create_shine_effect(draw, vx - 30, vy - 10, vw + 60, 100, (time_sec * 1.5) % 2.0)
        
        draw_text_premium(draw, vx, vy, val_text, fonts['number'], GOLD)
    
    # === TELA 3: CTA FINAL (7.5-12s) ===
    else:
        local_time = time_sec - 7.5
        
        bg = create_premium_background(width, height, frame_num, total_frames)
        
        # Overlay mais escuro para contraste
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        ov_draw = ImageDraw.Draw(overlay)
        for y in range(height):
            ov_draw.line([(0, y), (width, y)], fill=(0, 0, 0, 100))
        bg = Image.alpha_composite(bg.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(bg)
        
        progress = ease_out_expo(min(local_time / 1.0, 1.0))
        
        # === TEXTO PRINCIPAL ===
        text1 = "QUER RESULTADOS"
        bbox = draw.textbbox((0, 0), text1, font=fonts['title'])
        tw = bbox[2] - bbox[0]
        tx = (width - tw) // 2
        ty = 300 + int((1 - progress) * 50)
        
        draw_text_premium(draw, tx, ty, text1, fonts['title'], WHITE)
        
        text2 = "IGUAIS?"
        bbox = draw.textbbox((0, 0), text2, font=fonts['title'])
        tw2 = bbox[2] - bbox[0]
        tx2 = (width - tw2) // 2
        ty2 = ty + 140
        
        # Glow dourado intenso
        for r in range(25, 0, -2):
            alpha = int(50 * (1 - r / 25))
            for ox in range(-5, 6, 2):
                for oy in range(-5, 6, 2):
                    draw.text((tx2 + ox, ty2 + oy), text2, font=fonts['title'], 
                             fill=(*GOLD, alpha)[:3])
        
        draw_text_premium(draw, tx2, ty2, text2, fonts['title'], GOLD)
        
        # === BOTÃO CTA ===
        btn_progress = ease_out_back(min(max(local_time - 0.5, 0) / 0.8, 1.0))
        
        btn_text = "📲 LINK NA BIO"
        bbox = draw.textbbox((0, 0), btn_text, font=fonts['cta'])
        bw = bbox[2] - bbox[0] + 80
        bh = 90
        bx = (width - bw) // 2
        by = ty2 + 200 + int((1 - btn_progress) * 40)
        
        # Pulsação suave do botão
        pulse = 1.0 + math.sin(time_sec * 3) * 0.06
        pulse_px = int(8 * pulse)
        
        # Glow externo pulsante
        for r in range(pulse_px + 15, pulse_px, -2):
            alpha = int(40 * (1 - (r - pulse_px) / 15))
            draw.rounded_rectangle(
                [bx - r, by - r, bx + bw + r, by + bh + r],
                radius=25,
                outline=(*GOLD, alpha)[:3],
                width=2
            )
        
        # Fundo do botão com gradiente dourado
        btn_bg = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
        bbg = ImageDraw.Draw(btn_bg)
        
        for x in range(bw):
            ratio = x / bw
            color = (*lerp_color(GOLD_DARK, GOLD, ratio), 255)
            bbg.line([x, 0, x, bh], fill=color)
        
        bbg.rounded_rectangle([0, 0, bw, bh], radius=20, outline=(*GOLD_LIGHT, 200), width=3)
        
        # Brilho na borda superior
        bbg.line([20, 2, bw - 20, 2], fill=(*GOLD_BRIGHT, 150), width=2)
        
        # Shine passando
        shine_pos = int((time_sec * 3) % (bw + 60)) - 30
        for i in range(20):
            sx = shine_pos + i - 10
            if 0 <= sx < bw:
                alpha = int(100 * (1 - abs(i - 10) / 10))
                bbg.line([sx, 0, sx, bh], fill=(*GOLD_BRIGHT, alpha))
        
        bg.paste(btn_bg, (bx, by), btn_bg)
        
        # Texto do botão
        draw.text((bx + 40, by + 22), btn_text, font=fonts['cta'], fill=BLACK)
        
        # === TEXTO DE URGÊNCIA ===
        urg_progress = ease_out_expo(min(max(local_time - 0.8, 0) / 0.8, 1.0))
        
        urg_text = "⚠️ Só 15 vagas no grupo VIP"
        bbox = draw.textbbox((0, 0), urg_text, font=fonts['small'])
        uw = bbox[2] - bbox[0]
        ux = (width - uw) // 2
        uy = by + 130 + int((1 - urg_progress) * 20)
        
        # Ícone de alerta pulsante
        alert_pulse = abs(math.sin(time_sec * 4)) * 0.3 + 0.7
        
        draw.text((ux + 2, uy + 2), urg_text, font=fonts['small'], fill=(0, 0, 0))
        draw.text((ux, uy), urg_text, font=fonts['small'], 
                 fill=(*lerp_color((200, 200, 200), WHITE, alert_pulse), 255)[:3])
    
    # === BARRA DE PROGRESSO (todas as telas) ===
    progress_ratio = frame_num / total_frames
    bar_h = 6
    
    # Fundo da barra
    draw.rectangle([0, 0, width, bar_h], fill=(20, 20, 30))
    
    # Barra preenchida com gradiente dourado
    filled = int(width * progress_ratio)
    for x in range(filled):
        ratio = x / filled if filled > 0 else 0
        r = int(lerp(140, 255, ratio))
        g = int(lerp(110, 215, ratio))
        b = int(lerp(20, 100, ratio))
        draw.line([(x, 0), (x, bar_h)], fill=(r, g, b))
    
    # Brilho na ponta da barra
    if filled > 0:
        for r in range(8, 0, -1):
            alpha = int(100 * (1 - r / 8))
            draw.ellipse([filled - r, bar_h//2 - r, filled + r, bar_h//2 + r], 
                        fill=(*GOLD_BRIGHT, alpha)[:3])
    
    return bg

# ============================================
# MAIN
# ============================================
def main():
    print("🎬 Gerando VÍDEO PREMIUM MSA — Meta Ads Professional")
    print("=" * 60)
    
    # Carregar assets
    assets_dir = "/root/.openclaw/workspace/projetos-msa/assets/imagens"
    assets = {
        'carla': load_image_safe(f"{assets_dir}/carla_foto_evento.jpg"),
        'prova': load_image_safe(f"{assets_dir}/prova_venda_hest.jpg"),
        'background_vsl': load_image_safe(f"{assets_dir}/background_vsl.jpg"),
        'background_ads': load_image_safe(f"{assets_dir}/background_ads.jpg"),
    }
    
    print("\n📦 Assets carregados:")
    for name, img in assets.items():
        status = f"{img.size}" if img else "❌ NÃO ENCONTRADO"
        print(f"  {'✅' if img else '❌'} {name}: {status}")
    
    # Configurações
    width, height = 1080, 1920
    fps = 30
    duration = 12  # segundos
    total_frames = fps * duration
    
    # Diretório de frames
    frames_dir = "/tmp/msa_premium_frames"
    os.makedirs(frames_dir, exist_ok=True)
    
    # Limpar frames antigos
    for f in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, f))
    
    print(f"\n📸 Gerando {total_frames} frames premium...")
    
    for i in range(total_frames):
        if i % 30 == 0:
            print(f"  Frame {i:4d}/{total_frames} ({i*100//total_frames:3d}%)")
        
        frame = generate_frame(i, total_frames, width, height, assets)
        frame.save(f"{frames_dir}/frame_{i:04d}.png")
    
    print("\n🎞️ Compilando vídeo premium...")
    
    output_path = "/root/.openclaw/workspace/projetos-msa/output/story_premium_msa.mp4"
    
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", f"{frames_dir}/frame_%04d.png",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "22",  # Qualidade ligeiramente melhor
        "-preset", "slow",  # Melhor compressão
        "-movflags", "+faststart",
        "-vf", "format=yuv420p",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0 and os.path.exists(output_path):
        size = os.path.getsize(output_path)
        print(f"\n{'='*60}")
        print(f"✅ VÍDEO PREMIUM CRIADO COM SUCESSO!")
        print(f"{'='*60}")
        print(f"📁 {output_path}")
        print(f"📊 Tamanho: {size/1024:.1f} KB")
        print(f"⏱️ Duração: {duration}s")
        print(f"📐 Resolução: {width}x{height} (9:16)")
        print(f"🎥 FPS: {fps}")
        print(f"🎨 Qualidade: Premium (Meta Ads)")
        print(f"{'='*60}")
    else:
        print(f"\n❌ Erro ao criar vídeo:")
        print(result.stderr[:500])
    
    # Limpar frames
    for f in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, f))
    os.rmdir(frames_dir)

if __name__ == "__main__":
    main()
