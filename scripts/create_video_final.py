#!/usr/bin/env python3
"""
Vídeo MSA FINAL — Junta TUDO:
- Foto da Carla (real)
- Prova de venda R$ 8.594,83 (real)
- Backgrounds gerados (IA)
- Mockups gerados (IA)
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess

# Cores MSA
GOLD = (201, 162, 39)
GOLD_LIGHT = (229, 193, 88)
BLACK = (10, 10, 10)
WHITE = (255, 255, 255)

def load_image(path, size=None):
    if os.path.exists(path):
        img = Image.open(path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        if size:
            img = img.resize(size, Image.LANCZOS)
        return img
    return None

def ease_out(t):
    return 1 - (1 - t) ** 3

def create_frame(frame_num, total_frames, width, height, assets):
    time_sec = frame_num / 30.0
    
    # === FRAME 1: FOTO DA CARLA + BACKGROUND (0-4s) ===
    if time_sec < 4:
        progress = ease_out(min(time_sec / 2, 1))
        
        # Background
        bg = assets['background_vsl'].copy().resize((width, height), Image.LANCZOS)
        bg = bg.filter(ImageFilter.GaussianBlur(radius=3))
        draw = ImageDraw.Draw(bg)
        
        # Overlay escuro
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        ov_draw = ImageDraw.Draw(overlay)
        for y in range(height):
            ov_draw.line([(0, y), (width, y)], fill=(0, 0, 0, 100))
        bg = Image.alpha_composite(bg.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(bg)
        
        # Fontes
        try:
            f_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 100)
            f_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
            f_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
        except:
            f_title = f_sub = f_small = ImageFont.load_default()
        
        # Foto da Carla (circular, grande, centro)
        carla = assets['carla'].copy()
        size = 400
        carla = carla.resize((size, size), Image.LANCZOS)
        mask = Image.new('L', (size, size), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, size, size], fill=255)
        carla_rgba = carla.convert('RGBA')
        carla_rgba.putalpha(mask)
        
        x = (width - size) // 2
        y = 200 + int((1 - progress) * 100)
        
        # Borda dourada pulsante
        pulse = abs(math.sin(time_sec * 3)) * 12 + 6
        draw.ellipse([x - int(pulse), y - int(pulse), 
                     x + size + int(pulse), y + size + int(pulse)],
                    outline=GOLD, width=5)
        
        # Sombra da foto
        shadow = Image.new('RGBA', (size + 40, size + 40), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.ellipse([20, 20, size + 20, size + 20], fill=(0, 0, 0, 80))
        bg.paste(shadow, (x - 20, y - 20), shadow)
        bg.paste(carla_rgba, (x, y), carla_rgba)
        
        # Texto
        title = "Eu sou a Carla"
        bbox = draw.textbbox((0, 0), title, font=f_sub)
        tw = bbox[2] - bbox[0]
        draw.text(((width - tw) // 2, y + size + 50), title, font=f_sub, fill=WHITE)
        
        sub = "E descobri como faturar"
        bbox = draw.textbbox((0, 0), sub, font=f_sub)
        tw = bbox[2] - bbox[0]
        tx = (width - tw) // 2
        ty = y + size + 140
        draw.text((tx, ty), sub, font=f_sub, fill=GOLD)
        
        # Subtítulo
        sub2 = "SEM APARECER"
        bbox = draw.textbbox((0, 0), sub2, font=f_title)
        tw = bbox[2] - bbox[0]
        draw.text(((width - tw) // 2, ty + 90), sub2, font=f_title, fill=GOLD)
    
    # === FRAME 2: PROVA SOCIAL (4-8s) ===
    elif time_sec < 8:
        local = time_sec - 4
        progress = ease_out(min(local / 2, 1))
        
        # Background diferente
        bg = assets['background_ads'].copy().resize((width, height), Image.LANCZOS)
        bg = bg.filter(ImageFilter.GaussianBlur(radius=4))
        draw = ImageDraw.Draw(bg)
        
        # Overlay
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        ov_draw = ImageDraw.Draw(overlay)
        for y in range(height):
            ov_draw.line([(0, y), (width, y)], fill=(0, 0, 0, 120))
        bg = Image.alpha_composite(bg.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(bg)
        
        try:
            f_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 90)
            f_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 65)
            f_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 38)
            f_num = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        except:
            f_title = f_sub = f_small = f_num = ImageFont.load_default()
        
        # Badge
        badge = "✅ PROVA REAL"
        bbox = draw.textbbox((0, 0), badge, font=f_small)
        bw = bbox[2] - bbox[0] + 50
        bh = 55
        bx = (width - bw) // 2
        by = 120
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=28, fill=GOLD)
        draw.text((bx + 25, by + 10), badge, font=f_small, fill=BLACK)
        
        # Print da venda
        prova = assets['prova'].copy()
        max_w = int(width * 0.78)
        max_h = int(height * 0.42)
        ratio = min(max_w / prova.width, max_h / prova.height)
        new_w = int(prova.width * ratio)
        new_h = int(prova.height * ratio)
        prova = prova.resize((new_w, new_h), Image.LANCZOS)
        
        px = (width - new_w) // 2
        py = 220 + int((1 - progress) * 80)
        
        # Sombra do print
        shadow = Image.new('RGBA', (new_w + 30, new_h + 30), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.rounded_rectangle([15, 15, new_w + 15, new_h + 15], radius=20, fill=(0, 0, 0, 100))
        bg.paste(shadow, (px - 15, py - 15), shadow)
        
        # Borda dourada
        border = 4
        draw.rounded_rectangle([px - border, py - border, px + new_w + border, py + new_h + border],
                              radius=20, outline=GOLD, width=border)
        bg.paste(prova, (px, py))
        
        # Texto abaixo
        text = "Faturamento em 7 dias:"
        bbox = draw.textbbox((0, 0), text, font=f_sub)
        tw = bbox[2] - bbox[0]
        draw.text(((width - tw) // 2, py + new_h + 40), text, font=f_sub, fill=WHITE)
        
        # Valor em destaque
        val = "R$ 8.594,83"
        bbox = draw.textbbox((0, 0), val, font=f_num)
        vw = bbox[2] - bbox[0]
        # Glow
        for i in range(18, 0, -2):
            draw.text(((width - vw) // 2 + i//2, py + new_h + 120 + i//2), val, font=f_num,
                     fill=(*GOLD, 40))
        draw.text(((width - vw) // 2, py + new_h + 120), val, font=f_num, fill=GOLD)
    
    # === FRAME 3: CTA + MOCKUP (8-13s) ===
    elif time_sec < 13:
        local = time_sec - 8
        progress = ease_out(min(local / 2, 1))
        
        # Background escuro
        bg = assets['background_vsl'].copy().resize((width, height), Image.LANCZOS)
        bg = bg.filter(ImageFilter.GaussianBlur(radius=5))
        draw = ImageDraw.Draw(bg)
        
        # Overlay
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        ov_draw = ImageDraw.Draw(overlay)
        for y in range(height):
            ov_draw.line([(0, y), (width, y)], fill=(0, 0, 0, 80))
        bg = Image.alpha_composite(bg.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(bg)
        
        try:
            f_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 85)
            f_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
            f_cta = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 55)
            f_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 35)
        except:
            f_title = f_sub = f_cta = f_small = ImageFont.load_default()
        
        # Mockup de produto (no centro, flutuando)
        mockup = assets['mockup'].copy()
        mw = int(width * 0.65)
        mh = int(mw * mockup.height / mockup.width)
        mockup = mockup.resize((mw, mh), Image.LANCZOS)
        
        mx = (width - mw) // 2
        my = 180 + int((1 - progress) * 60)
        
        # Sombra
        shadow = Image.new('RGBA', (mw + 40, mh + 40), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.rounded_rectangle([20, 20, mw + 20, mh + 20], radius=25, fill=(0, 0, 0, 60))
        bg.paste(shadow, (mx - 20, my - 20), shadow)
        
        bg.paste(mockup, (mx, my))
        
        # Texto CTA
        cta1 = "QUER O MÉTODO?"
        bbox = draw.textbbox((0, 0), cta1, font=f_title)
        tw = bbox[2] - bbox[0]
        draw.text(((width - tw) // 2, my + mh + 50), cta1, font=f_title, fill=WHITE)
        
        cta2 = "Entre no Grupo VIP"
        bbox = draw.textbbox((0, 0), cta2, font=f_sub)
        tw = bbox[2] - bbox[0]
        draw.text(((width - tw) // 2, my + mh + 160), cta2, font=f_sub, fill=GOLD)
        
        # Botão
        btn = "👉 LINK NA BIO"
        bbox = draw.textbbox((0, 0), btn, font=f_cta)
        bw = bbox[2] - bbox[0] + 70
        bh = 85
        bx = (width - bw) // 2
        by = my + mh + 270
        
        pulse = abs(math.sin(local * 3)) * 10 + 5
        draw.rounded_rectangle([bx - int(pulse), by - int(pulse), bx + bw + int(pulse), by + bh + int(pulse)],
                              radius=22, outline=GOLD, width=4)
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=18, fill=GOLD)
        draw.text((bx + 35, by + 20), btn, font=f_cta, fill=BLACK)
        
        # Urgência
        urg = "🔥 Só 15 vagas — Grupo VIP de pré-lançamento"
        bbox = draw.textbbox((0, 0), urg, font=f_small)
        uw = bbox[2] - bbox[0]
        draw.text(((width - uw) // 2, by + 120), urg, font=f_small, fill=(180, 180, 180))
    
    # === FRAME 4: FOTO FINAL + RESULTADOS (13-15s) ===
    else:
        local = time_sec - 13
        progress = ease_out(min(local / 1.5, 1))
        
        # Background
        bg = assets['background_ads'].copy().resize((width, height), Image.LANCZOS)
        bg = bg.filter(ImageFilter.GaussianBlur(radius=3))
        draw = ImageDraw.Draw(bg)
        
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        ov_draw = ImageDraw.Draw(overlay)
        for y in range(height):
            ov_draw.line([(0, y), (width, y)], fill=(0, 0, 0, 100))
        bg = Image.alpha_composite(bg.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(bg)
        
        try:
            f_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
            f_num = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 130)
            f_cta = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 55)
            f_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        except:
            f_title = f_num = f_cta = f_small = ImageFont.load_default()
        
        # Foto da Carla (circular, topo)
        carla = assets['carla'].copy()
        size = 180
        carla = carla.resize((size, size), Image.LANCZOS)
        mask = Image.new('L', (size, size), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, size, size], fill=255)
        carla_rgba = carla.convert('RGBA')
        carla_rgba.putalpha(mask)
        
        cx = (width - size) // 2
        cy = 150
        bg.paste(carla_rgba, (cx, cy), carla_rgba)
        
        # Borda
        draw.ellipse([cx - 5, cy - 5, cx + size + 5, cy + size + 5], outline=GOLD, width=4)
        
        # Nome
        nome = "Carla Felicio"
        bbox = draw.textbbox((0, 0), nome, font=f_cta)
        nw = bbox[2] - bbox[0]
        draw.text(((width - nw) // 2, cy + size + 25), nome, font=f_cta, fill=WHITE)
        
        # Cargo
        cargo = "Criadora do MSA"
        bbox = draw.textbbox((0, 0), cargo, font=f_small)
        cw = bbox[2] - bbox[0]
        draw.text(((width - cw) // 2, cy + size + 85), cargo, font=f_small, fill=GOLD)
        
        # Números
        y_start = cy + size + 160
        stats = [
            ("+R$ 250k", "Faturados"),
            ("+500", "Alunas"),
            ("3-4h", "Por dia"),
        ]
        
        gap = width // 3
        for i, (num, label) in enumerate(stats):
            x = gap * i + gap // 2
            
            # Número
            bbox = draw.textbbox((0, 0), num, font=f_num)
            nw = bbox[2] - bbox[0]
            # Glow
            for j in range(12, 0, -2):
                draw.text((x - nw // 2 + j//2, y_start + j//2), num, font=f_num,
                         fill=(*GOLD, 30))
            draw.text((x - nw // 2, y_start), num, font=f_num, fill=GOLD)
            
            # Label
            bbox = draw.textbbox((0, 0), label, font=f_small)
            lw = bbox[2] - bbox[0]
            draw.text((x - lw // 2, y_start + 140), label, font=f_small, fill=WHITE)
        
        # CTA final
        cta = "CLIQUE NO LINK →"
        bbox = draw.textbbox((0, 0), cta, font=f_cta)
        cw = bbox[2] - bbox[0]
        cta_x = (width - cw) // 2
        cta_y = y_start + 260
        
        pulse = abs(math.sin(local * 4)) * 8 + 4
        draw.rounded_rectangle([cta_x - int(pulse), cta_y - int(pulse),
                               cta_x + cw + int(pulse), cta_y + 80 + int(pulse)],
                              radius=20, outline=GOLD, width=3)
        draw.rounded_rectangle([cta_x, cta_y, cta_x + cw, cta_y + 80],
                              radius=16, fill=GOLD)
        draw.text((cta_x + 30, cta_y + 18), cta, font=f_cta, fill=BLACK)
    
    # Barra de progresso no topo
    ratio = frame_num / total_frames
    bar_h = 8
    draw.rectangle([0, 0, width, bar_h], fill=(30, 30, 30))
    filled = int(width * ratio)
    for x in range(filled):
        r = int(168 + (229 - 168) * (x / filled if filled > 0 else 0))
        g = int(132 + (193 - 132) * (x / filled if filled > 0 else 0))
        b = int(32 + (88 - 32) * (x / filled if filled > 0 else 0))
        draw.line([(x, 0), (x, bar_h)], fill=(r, g, b))
    
    return bg

def main():
    print("🎬 Gerando VÍDEO FINAL MSA — TUDO junto!")
    print("=" * 50)
    
    # Carregar todos os assets
    assets_dir = "/root/.openclaw/workspace/projetos-msa/assets/imagens"
    
    assets = {
        'carla': load_image(f"{assets_dir}/carla_foto_evento.jpg"),
        'prova': load_image(f"{assets_dir}/prova_venda_hest.jpg"),
        'background_vsl': load_image(f"{assets_dir}/background_vsl.jpg"),
        'background_ads': load_image(f"{assets_dir}/background_ads.jpg"),
        'mockup': load_image(f"{assets_dir}/mockup_produtos.jpg"),
    }
    
    for name, img in assets.items():
        if img:
            print(f"✅ {name}: {img.size}")
        else:
            print(f"❌ {name}: NÃO ENCONTRADO")
    
    # Config
    width, height = 1080, 1920
    fps = 30
    duration = 15  # 15 segundos
    total_frames = fps * duration
    
    frames_dir = "/tmp/msa_final_frames"
    os.makedirs(frames_dir, exist_ok=True)
    for f in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, f))
    
    print(f"\n📸 Gerando {total_frames} frames...")
    for i in range(total_frames):
        if i % 30 == 0:
            print(f"  {i}/{total_frames} ({i*100//total_frames}%)")
        frame = create_frame(i, total_frames, width, height, assets)
        frame.save(f"{frames_dir}/frame_{i:04d}.png")
    
    print("\n🎞️ Compilando vídeo final...")
    output = "/root/.openclaw/workspace/projetos-msa/output/story_final_msa.mp4"
    
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", f"{frames_dir}/frame_%04d.png",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23",
        "-preset", "fast", "-movflags", "+faststart",
        output
    ], capture_output=True)
    
    if os.path.exists(output):
        size = os.path.getsize(output)
        print(f"\n✅ VÍDEO FINAL CRIADO!")
        print(f"📁 {output}")
        print(f"📊 Tamanho: {size/1024:.1f} KB")
        print(f"⏱️ Duração: {duration}s")
        print(f"📐 {width}x{height}")
    else:
        print("❌ Erro ao criar vídeo")
    
    # Limpar
    for f in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, f))
    os.rmdir(frames_dir)

if __name__ == "__main__":
    main()
