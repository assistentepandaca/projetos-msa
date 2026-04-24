#!/usr/bin/env python3
"""
Vídeo MSA com PROVA SOCIAL REAL — 10 segundos
Usa foto da Carla + print de venda R$ 8.594,83
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess

def load_image(path):
    """Carrega imagem se existir"""
    if os.path.exists(path):
        img = Image.open(path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        return img
    return None

def create_gradient_bg(width, height):
    """Background gradiente"""
    img = Image.new('RGB', (width, height), (10, 10, 10))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        ratio = y / height
        r = int(10 + 16 * ratio)
        g = int(10 + 9 * ratio)
        b = int(10 + 52 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return img

def create_frame(frame_num, total_frames, width, height, carla_photo, prova_venda):
    """Gera um frame do vídeo"""
    time_sec = frame_num / 30.0
    
    # Background
    bg = create_gradient_bg(width, height)
    draw = ImageDraw.Draw(bg)
    
    # Fontes
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 90)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
        font_cta = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 35)
    except:
        font_title = ImageFont.load_default()
        font_sub = font_title
        font_cta = font_title
        font_small = font_title
    
    # ===== CENA 1: HOOK COM FOTO (0-2.5s) =====
    if time_sec < 2.5:
        progress = 1 - (1 - min(time_sec / 1.5, 1.0)) ** 3
        
        # Foto da Carla (circular, no topo)
        if carla_photo:
            size = 250
            photo = carla_photo.copy().resize((size, size), Image.LANCZOS)
            mask = Image.new('L', (size, size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse([0, 0, size, size], fill=255)
            photo.putalpha(mask)
            
            x = (width - size) // 2
            y = 150
            bg.paste(photo, (x, y), photo)
            
            # Borda dourada pulsante
            pulse = abs(math.sin(time_sec * 3)) * 8 + 4
            draw.ellipse([x - int(pulse), y - int(pulse), 
                         x + size + int(pulse), y + size + int(pulse)],
                        outline=(201, 162, 39), width=4)
        
        # Texto
        title = "R$ 47.000"
        bbox = draw.textbbox((0, 0), title, font=font_title)
        text_w = bbox[2] - bbox[0]
        text_x = (width - text_w) // 2
        text_y = 450
        
        # Glow
        for i in range(12, 0, -2):
            draw.text((text_x + i//2, text_y + i//2), title, font=font_title, 
                     fill=(201, 162, 39, 40))
        draw.text((text_x, text_y), title, font=font_title, fill=(201, 162, 39))
        
        # Subtítulo
        sub = "em 30 dias"
        bbox = draw.textbbox((0, 0), sub, font=font_sub)
        sub_w = bbox[2] - bbox[0]
        sub_x = (width - sub_w) // 2
        draw.text((sub_x, text_y + 120), sub, font=font_sub, fill=(255, 255, 255))
        
        # Descrição
        desc = "Sem aparecer. Sem estoque."
        bbox = draw.textbbox((0, 0), desc, font=font_small)
        desc_w = bbox[2] - bbox[0]
        desc_x = (width - desc_w) // 2
        draw.text((desc_x, text_y + 220), desc, font=font_small, fill=(180, 180, 180))
    
    # ===== CENA 2: PROVA SOCIAL (2.5-6s) =====
    elif time_sec < 6.0:
        local_time = time_sec - 2.5
        progress = 1 - (1 - min(local_time / 2, 1.0)) ** 3
        
        # Badge "PROVA REAL"
        badge = "✅ PROVA REAL"
        bbox = draw.textbbox((0, 0), badge, font=font_small)
        badge_w = bbox[2] - bbox[0] + 60
        badge_h = 60
        badge_x = (width - badge_w) // 2
        badge_y = 100
        
        draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
                              radius=30, fill=(201, 162, 39))
        draw.text((badge_x + 30, badge_y + 12), badge, font=font_small, fill=(0, 0, 0))
        
        # Print da venda (centralizado, grande)
        if prova_venda:
            # Calcular tamanho para ocupar 70% da largura
            max_w = int(width * 0.75)
            max_h = int(height * 0.5)
            
            ratio = min(max_w / prova_venda.width, max_h / prova_venda.height)
            new_w = int(prova_venda.width * ratio)
            new_h = int(prova_venda.height * ratio)
            
            prova = prova_venda.resize((new_w, new_h), Image.LANCZOS)
            
            # Borda arredondada e sombra
            x = (width - new_w) // 2
            y = 200 + int((1 - progress) * 100)
            
            # Sombra
            shadow_offset = 15
            draw.rounded_rectangle([x + shadow_offset, y + shadow_offset,
                                   x + new_w + shadow_offset, y + new_h + shadow_offset],
                                  radius=25, fill=(0, 0, 0, 100))
            
            # Borda dourada
            border = 5
            draw.rounded_rectangle([x - border, y - border,
                                   x + new_w + border, y + new_h + border],
                                  radius=25, outline=(201, 162, 39), width=border)
            
            bg.paste(prova, (x, y))
        
        # Texto abaixo do print
        text = "Faturamento em 7 dias"
        bbox = draw.textbbox((0, 0), text, font=font_sub)
        text_w = bbox[2] - bbox[0]
        text_x = (width - text_w) // 2
        text_y = y + new_h + 40
        
        draw.text((text_x, text_y), text, font=font_sub, fill=(255, 255, 255))
        
        # Destaque
        dest = "R$ 8.594,83"
        bbox = draw.textbbox((0, 0), dest, font=font_title)
        dest_w = bbox[2] - bbox[0]
        dest_x = (width - dest_w) // 2
        draw.text((dest_x, text_y + 90), dest, font=font_title, fill=(201, 162, 39))
    
    # ===== CENA 3: CTA (6-10s) =====
    else:
        local_time = time_sec - 6.0
        progress = 1 - (1 - min(local_time / 2, 1.0)) ** 3
        
        # Foto da Carla (pequena, canto superior)
        if carla_photo:
            size = 120
            photo = carla_photo.copy().resize((size, size), Image.LANCZOS)
            mask = Image.new('L', (size, size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse([0, 0, size, size], fill=255)
            photo.putalpha(mask)
            bg.paste(photo, (width//2 - size//2, 120), photo)
        
        # Texto CTA
        cta1 = "QUER RESULTADOS"
        cta2 = "IGUAIS?"
        
        bbox = draw.textbbox((0, 0), cta1, font=font_title)
        cta1_w = bbox[2] - bbox[0]
        cta_x = (width - cta1_w) // 2
        cta_y = 300
        
        draw.text((cta_x, cta_y), cta1, font=font_title, fill=(255, 255, 255))
        
        bbox = draw.textbbox((0, 0), cta2, font=font_title)
        cta2_w = bbox[2] - bbox[0]
        cta2_x = (width - cta2_w) // 2
        draw.text((cta2_x, cta_y + 110), cta2, font=font_title, fill=(201, 162, 39))
        
        # Botão CTA
        btn = "👉 LINK NA BIO"
        bbox = draw.textbbox((0, 0), btn, font=font_cta)
        btn_w = bbox[2] - bbox[0] + 80
        btn_h = 90
        btn_x = (width - btn_w) // 2
        btn_y = cta_y + 280
        
        # Pulsante
        pulse = abs(math.sin(local_time * 3)) * 10 + 5
        draw.rounded_rectangle([btn_x - int(pulse), btn_y - int(pulse),
                               btn_x + btn_w + int(pulse), btn_y + btn_h + int(pulse)],
                              radius=25, outline=(201, 162, 39), width=4)
        
        draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h],
                              radius=20, fill=(201, 162, 39))
        draw.text((btn_x + 40, btn_y + 22), btn, font=font_cta, fill=(0, 0, 0))
        
        # Urgência
        vagas = "🔥 Só 15 vagas no grupo VIP"
        bbox = draw.textbbox((0, 0), vagas, font=font_small)
        vagas_w = bbox[2] - bbox[0]
        vagas_x = (width - vagas_w) // 2
        draw.text((vagas_x, btn_y + 130), vagas, font=font_small, fill=(180, 180, 180))
    
    # Barra de progresso
    progress_ratio = frame_num / total_frames
    filled = int(width * progress_ratio)
    draw.rectangle([0, 0, width, 8], fill=(30, 30, 30))
    for x in range(filled):
        ratio = x / filled if filled > 0 else 0
        r = int(168 + (229 - 168) * ratio)
        g = int(132 + (193 - 132) * ratio)
        b = int(32 + (88 - 32) * ratio)
        draw.line([(x, 0), (x, 8)], fill=(r, g, b))
    
    return bg

def main():
    print("🎬 Gerando vídeo com PROVA SOCIAL REAL...")
    
    carla_photo = load_image("/root/.openclaw/workspace/projetos-msa/assets/imagens/carla_foto_evento.jpg")
    prova_venda = load_image("/root/.openclaw/workspace/projetos-msa/assets/imagens/prova_venda_hest.jpg")
    
    if carla_photo:
        print(f"✅ Foto da Carla: {carla_photo.size}")
    if prova_venda:
        print(f"✅ Prova de venda: {prova_venda.size}")
        print(f"💰 Valor: R$ 8.594,83")
    
    width, height = 1080, 1920
    fps, duration = 30, 10
    total_frames = fps * duration
    
    frames_dir = "/tmp/msa_prova_frames"
    os.makedirs(frames_dir, exist_ok=True)
    for f in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, f))
    
    print(f"\n📸 Gerando {total_frames} frames...")
    for i in range(total_frames):
        if i % 30 == 0:
            print(f"  {i}/{total_frames} ({i*100//total_frames}%)")
        frame = create_frame(i, total_frames, width, height, carla_photo, prova_venda)
        frame.save(f"{frames_dir}/frame_{i:04d}.png")
    
    print("\n🎞️ Compilando vídeo...")
    output = "/root/.openclaw/workspace/projetos-msa/output/story_com_prova.mp4"
    
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", f"{frames_dir}/frame_%04d.png",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23",
        output
    ], capture_output=True)
    
    if os.path.exists(output):
        size = os.path.getsize(output)
        print(f"✅ Vídeo criado: {output}")
        print(f"📊 Tamanho: {size/1024:.1f} KB")
        print(f"⏱️ Duração: {duration}s")
    
    # Limpar
    for f in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, f))
    os.rmdir(frames_dir)

if __name__ == "__main__":
    main()
