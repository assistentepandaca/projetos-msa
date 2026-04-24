#!/usr/bin/env python3
"""
Gerador Automático de Stories Instagram — MSA
Cria stories completos baseados em depoimentos de alunas
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Cores MSA
GOLD = (201, 162, 39)
GOLD_LIGHT = (229, 193, 88)
BLACK = (8, 8, 15)
DARK_NAVY = (15, 20, 40)
WHITE = (255, 255, 255)
WHITE_SOFT = (220, 220, 230)
GRAY = (150, 150, 170)

def create_gradient_bg(width, height, color1=DARK_NAVY, color2=BLACK):
    """Background gradiente"""
    img = Image.new('RGB', (width, height), color2)
    draw = ImageDraw.Draw(img)
    for y in range(height):
        ratio = y / height
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return img

def get_fonts():
    """Carrega fontes"""
    try:
        return {
            'title': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80),
            'subtitle': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 55),
            'text': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 42),
            'cta': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60),
            'small': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 35),
            'number': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 110),
        }
    except:
        default = ImageFont.load_default()
        return {k: default for k in ['title', 'subtitle', 'text', 'cta', 'small', 'number']}

def draw_text_centered(draw, text, font, color, y, width):
    """Desenha texto centralizado"""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (width - text_w) // 2
    draw.text((x, y), text, font=font, fill=color)
    return x, text_w

def draw_text_left(draw, text, font, color, x, y):
    """Desenha texto alinhado à esquerda"""
    draw.text((x, y), text, font=font, fill=color)

def create_slide_hook(width, height, fonts, hook_text, sub_text=None):
    """Slide 1: Hook/Pergunta"""
    bg = create_gradient_bg(width, height)
    draw = ImageDraw.Draw(bg)
    
    # Ícone de pergunta grande
    draw.text_centered = lambda t, f, c, y: draw_text_centered(draw, t, f, c, y, width)
    
    # Pergunta principal
    y = height // 2 - 100
    
    # Quebrar texto em múltiplas linhas se necessário
    words = hook_text.split()
    lines = []
    current_line = ""
    for word in words:
        test = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test, font=fonts['title'])
        if bbox[2] - bbox[0] > width * 0.85:
            if current_line:
                lines.append(current_line)
                current_line = word
            else:
                lines.append(word)
        else:
            current_line = test
    if current_line:
        lines.append(current_line)
    
    # Desenhar linhas
    total_height = len(lines) * 100
    start_y = (height - total_height) // 2
    
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=fonts['title'])
        text_w = bbox[2] - bbox[0]
        x = (width - text_w) // 2
        y_pos = start_y + i * 100
        
        # Sombra
        draw.text((x + 3, y_pos + 3), line, font=fonts['title'], fill=(0, 0, 0))
        draw.text((x, y_pos), line, font=fonts['title'], fill=WHITE)
    
    # Subtítulo
    if sub_text:
        bbox = draw.textbbox((0, 0), sub_text, font=fonts['subtitle'])
        sw = bbox[2] - bbox[0]
        sx = (width - sw) // 2
        sy = start_y + len(lines) * 100 + 40
        draw.text((sx, sy), sub_text, font=fonts['subtitle'], fill=GRAY)
    
    return bg

def create_slide_story(width, height, fonts, title, story_lines):
    """Slide 2-3: Story/Narrativa"""
    bg = create_gradient_bg(width, height)
    draw = ImageDraw.Draw(bg)
    
    # Título da pessoa
    if title:
        bbox = draw.textbbox((0, 0), title, font=fonts['subtitle'])
        tw = bbox[2] - bbox[0]
        tx = (width - tw) // 2
        draw.text((tx, 120), title, font=fonts['subtitle'], fill=GOLD)
    
    # Linhas da história
    y_start = 250
    for i, line in enumerate(story_lines):
        y = y_start + i * 70
        
        # Sombra suave
        draw.text((52, y + 2), line, font=fonts['text'], fill=(0, 0, 0))
        draw.text((50, y), line, font=fonts['text'], fill=WHITE_SOFT)
    
    return bg

def create_slide_prova(width, height, fonts, period_text, valor, descricao, prova_img=None):
    """Slide 4: Prova/Resultado"""
    bg = create_gradient_bg(width, height)
    draw = ImageDraw.Draw(bg)
    
    # Badge "PROVA REAL"
    badge = "✅ PROVA REAL"
    bbox = draw.textbbox((0, 0), badge, font=fonts['small'])
    bw = bbox[2] - bbox[0] + 50
    bh = 55
    bx = (width - bw) // 2
    by = 100
    
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=28, fill=GOLD)
    draw.text((bx + 25, by + 10), badge, font=fonts['small'], fill=BLACK)
    
    # Se tiver imagem da prova
    if prova_img and os.path.exists(prova_img):
        img = Image.open(prova_img).convert('RGB')
        max_w = int(width * 0.75)
        max_h = int(height * 0.42)
        ratio = min(max_w / img.width, max_h / img.height)
        new_w = int(img.width * ratio)
        new_h = int(img.height * ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        
        px = (width - new_w) // 2
        py = 200
        
        # Borda
        border = 4
        draw.rounded_rectangle([px - border, py - border, px + new_w + border, py + new_h + border],
                              radius=20, outline=GOLD, width=border)
        bg.paste(img, (px, py))
        
        y_after = py + new_h + 40
    else:
        y_after = 250
    
    # Texto do período
    bbox = draw.textbbox((0, 0), period_text, font=fonts['text'])
    tw = bbox[2] - bbox[0]
    tx = (width - tw) // 2
    draw.text((tx, y_after), period_text, font=fonts['text'], fill=WHITE)
    
    # Valor em destaque
    bbox = draw.textbbox((0, 0), valor, font=fonts['number'])
    vw = bbox[2] - bbox[0]
    vx = (width - vw) // 2
    vy = y_after + 70
    
    # Glow
    for i in range(15, 0, -2):
        draw.text((vx + i//2, vy + i//2), valor, font=fonts['number'], fill=(*GOLD, 40)[:3])
    draw.text((vx, vy), valor, font=fonts['number'], fill=GOLD)
    
    # Descrição
    if descricao:
        bbox = draw.textbbox((0, 0), descricao, font=fonts['text'])
        dw = bbox[2] - bbox[0]
        dx = (width - dw) // 2
        draw.text((dx, vy + 140), descricao, font=fonts['text'], fill=WHITE_SOFT)
    
    return bg

def create_slide_cta(width, height, fonts, headline, subheadline, btn_text, urgency):
    """Slide 5-6: CTA"""
    bg = create_gradient_bg(width, height)
    draw = ImageDraw.Draw(bg)
    
    # Headline
    bbox = draw.textbbox((0, 0), headline, font=fonts['title'])
    tw = bbox[2] - bbox[0]
    tx = (width - tw) // 2
    ty = height // 2 - 150
    
    draw.text((tx + 2, ty + 2), headline, font=fonts['title'], fill=(0, 0, 0))
    draw.text((tx, ty), headline, font=fonts['title'], fill=WHITE)
    
    # Subheadline
    if subheadline:
        bbox = draw.textbbox((0, 0), subheadline, font=fonts['subtitle'])
        sw = bbox[2] - bbox[0]
        sx = (width - sw) // 2
        draw.text((sx, ty + 120), subheadline, font=fonts['subtitle'], fill=GOLD)
    
    # Botão
    bbox = draw.textbbox((0, 0), btn_text, font=fonts['cta'])
    bw = bbox[2] - bbox[0] + 70
    bh = 85
    bx = (width - bw) // 2
    by = ty + 250
    
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=20, fill=GOLD)
    draw.text((bx + 35, by + 20), btn_text, font=fonts['cta'], fill=BLACK)
    
    # Urgência
    if urgency:
        bbox = draw.textbbox((0, 0), urgency, font=fonts['small'])
        uw = bbox[2] - bbox[0]
        ux = (width - uw) // 2
        draw.text((ux, by + 120), urgency, font=fonts['small'], fill=GRAY)
    
    return bg

def generate_story_from_depoimento(depoimento_data, output_dir):
    """
    Gera story completo baseado em depoimento
    
    depoimento_data = {
        'nome': 'Luna',
        'profissao': 'Escritório',
        'dor': 'Demitida na sexta-feira',
        'tempo': '1 semana',
        'valor': 'R$ 4.200',
        'prova_img': 'path/to/print.jpg',
        'cta': 'Quer saber como a Luna fez?',
    }
    """
    width, height = 1080, 1920
    fonts = get_fonts()
    
    nome = depoimento_data.get('nome', 'Aluna')
    profissao = depoimento_data.get('profissao', 'CLT')
    dor = depoimento_data.get('dor', 'Sem tempo')
    tempo = depoimento_data.get('tempo', '30 dias')
    valor = depoimento_data.get('valor', 'R$ X.XXX')
    prova_img = depoimento_data.get('prova_img')
    
    # Criar diretório
    story_dir = Path(output_dir) / f"story_{nome.lower()}"
    story_dir.mkdir(parents=True, exist_ok=True)
    
    # Slide 1: Hook
    hook_text = f"Já pensou {dor.lower()}..."
    sub = "e não saber o que fazer depois?"
    slide1 = create_slide_hook(width, height, fonts, hook_text, sub)
    slide1.save(story_dir / "01_hook.jpg")
    
    # Slide 2: Identificação
    title = f"Essa é a {nome}"
    story_lines = [
        f"Trabalhava em {profissao}",
        f"{dor}",
        "Achava que não tinha saída..."
    ]
    slide2 = create_slide_story(width, height, fonts, title, story_lines)
    slide2.save(story_dir / "02_identificacao.jpg")
    
    # Slide 3: Virada
    story_lines_virada = [
        f"Descobriu o MSA",
        f"{tempo} depois..."
    ]
    slide3 = create_slide_story(width, height, fonts, None, story_lines_virada)
    slide3.save(story_dir / "03_virada.jpg")
    
    # Slide 4: Prova
    slide4 = create_slide_prova(width, height, fonts, 
                                f"Resultado em {tempo}:", 
                                valor, 
                                "Sem aparecer. Sem estoque.",
                                prova_img)
    slide4.save(story_dir / "04_prova.jpg")
    
    # Slide 5: CTA
    headline = "QUER RESULTADOS"
    subhead = "IGUAIS?"
    btn = "👉 LINK NA BIO"
    urg = "🔥 Só 15 vagas no grupo VIP"
    slide5 = create_slide_cta(width, height, fonts, headline, subhead, btn, urg)
    slide5.save(story_dir / "05_cta.jpg")
    
    print(f"✅ Story da {nome} criado em: {story_dir}")
    print(f"   - 5 slides gerados")
    print(f"   - Pronto para postar no Instagram")
    
    return story_dir

# ============================================
# EXEMPLO DE USO
# ============================================
if __name__ == "__main__":
    # Exemplo: Story da Luna
    depoimento_luna = {
        'nome': 'Luna',
        'profissao': 'escritório há 4 anos',
        'dor': 'ser DEMITIDA na sexta-feira',
        'tempo': '1 semana',
        'valor': 'R$ 4.200',
        'prova_img': None,  # Colocar path da imagem quando tiver
    }
    
    output = "/root/.openclaw/workspace/projetos-msa/output/stories"
    
    print("🎨 Gerador de Stories Instagram — MSA")
    print("=" * 50)
    print("\nExemplo: Story da Luna")
    print("-" * 50)
    
    story_path = generate_story_from_depoimento(depoimento_luna, output)
    
    print(f"\n📁 Story salvo em: {story_path}")
    print("\n🚀 Próximos passos:")
    print("1. Subir os 5 slides no Instagram (Stories)")
    print("2. Adicionar enquete no slide 2")
    print("3. Colocar 'link na bio' no último slide")
    print("4. Repetir com próxima aluna")
    
    print("\n💡 Para gerar mais stories, edite o script e mude 'depoimento_luna'")
    print("   ou me envie os depoimentos reais que eu gero automaticamente!")
