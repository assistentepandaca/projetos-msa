#!/usr/bin/env python3
"""
Gerador de Stories Instagram — 8 Alunas MSA
Gera 5 slides por aluna automaticamente
"""
import os
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

# Configurações
WIDTH, HEIGHT = 1080, 1920

# Dados das 8 alunas
ALUNAS = [
    {
        'nome': 'Aluna MSA',
        'valor': 'R$ 8.156,43',
        'periodo': 'fevereiro',
        'tempo': '3 meses',
        'vendas': '15 vendas',
        'dor': 'trabalhava de CLT e queria renda extra',
        'virada': 'descobriu que dava pra vender sem estoque, só pronta entrega e no orgânico',
        'prova_img': 'prova_aluna_8k.jpg',
        'hook': '3 meses de mentoria... e o resultado veio!',
        'sub_hook': 'Trabalhando de CLT e vendendo no orgânico',
        'identificacao': [
            'Ela trabalha de CLT',
            'Concilia o trabalho das 9 às 18h',
            'Não tem tempo para aparecer',
            'Não quer investir em estoque',
            'Queria renda extra no celular'
        ],
        'destaque_ident': 'Só vende no ORGÂNICO',
        'cta': 'QUER RESULTADOS IGUAIS?',
        'story_folder': 'story_aluna_8k'
    },
    {
        'nome': 'Ex-CLT 9 anos',
        'valor': 'R$ 15.447,62',
        'periodo': 'março',
        'tempo': '30 dias',
        'vendas': 'múltiplas vendas',
        'dor': 'saiu do CLT após 9 anos, foi demitida',
        'virada': 'faturou R$ 8k depois de ser demitida, e em 30 dias ganhou mais que 9 anos de CLT',
        'prova_img': 'prova_aluna_2_15k.jpg',
        'hook': '9 anos de CLT... e em 30 dias superou tudo!',
        'sub_hook': 'Demitida → Faturando R$ 15k no mês',
        'identificacao': [
            'Trabalhou 9 anos em CLT',
            'Foi demitida do emprego',
            'Achou que a vida tinha acabado',
            'Tinha contas para pagar',
            'Não sabia o que fazer'
        ],
        'destaque_ident': 'DEMITIDA → EMPREENDEDORA',
        'cta': 'QUER VIRAR O JOGO?',
        'story_folder': 'story_aluna_15k'
    },
    {
        'nome': 'Thais Linhares',
        'valor': 'R$ 10.266,79',
        'periodo': '4 meses',
        'tempo': '4 meses',
        'vendas': 'várias vendas',
        'dor': 'queria independência financeira',
        'virada': 'descobriu o método MSA e começou a vender produtos físicos sem aparecer',
        'prova_img': 'prova_venda_hest.jpg',
        'hook': 'Ela duvidou... até ver o resultado!',
        'sub_hook': 'R$ 10.266,79 em 4 meses de mentoria',
        'identificacao': [
            'Thais Linhares',
            'Queria independência financeira',
            'Não sabia por onde começar',
            'Tinha medo de investir',
            'Achava que precisava aparecer'
        ],
        'destaque_ident': 'HOJE: R$ 10 MIL FATURADOS',
        'cta': 'QUER O MESMO RESULTADO?',
        'story_folder': 'story_thais_10k'
    },
    {
        'nome': 'Demitida na Sexta',
        'valor': 'R$ 325,29',
        'periodo': '1 dia',
        'tempo': '1 dia',
        'vendas': '4 vendas',
        'dor': 'foi demitida na sexta-feira',
        'virada': 'no mesmo dia começou a vender e faturou o dobro do seu dia de CLT',
        'prova_img': 'prova_venda_hest.jpg',
        'hook': 'Demitida na sexta... e faturou no mesmo dia!',
        'sub_hook': 'O dobro do salário diário em poucas horas',
        'identificacao': [
            'Foi demitida na sexta-feira',
            'Recebeu a notícia de manhã',
            'Ficou desesperada',
            'Não sabia como pagar as contas',
            'Achou que ia passar necessidade'
        ],
        'destaque_ident': 'MESMO DIA: DOBRO DO SALÁRIO',
        'cta': 'NÃO ESPERE SER DEMITIDA!',
        'story_folder': 'story_demitida_sexta'
    },
    {
        'nome': 'Ana Corrêa',
        'valor': 'R$ 1.018,71',
        'periodo': '3 meses',
        'tempo': '3 meses',
        'vendas': '12 vendas',
        'dor': 'estava começando do zero, queria fazer o primeiro 1k',
        'virada': 'não desistiu, entrou para o premium e fechou o mês com R$ 1.018,71',
        'prova_img': 'prova_aluna_5_ana.jpg',
        'hook': 'Primeiros R$ 1.000 na internet!',
        'sub_hook': 'Começando do zero, sem experiência',
        'identificacao': [
            'Ana Corrêa',
            'Estava começando do zero',
            'Nunca tinha vendido online',
            'Queria fazer o primeiro 1k',
            'Pensou em desistir várias vezes'
        ],
        'destaque_ident': 'PRIMEIRO 1K CONQUISTADO!',
        'cta': 'COMECE DO ZERO HOJE!',
        'story_folder': 'story_ana_1k'
    },
    {
        'nome': 'Francielly Camillo',
        'valor': 'R$ 5.000,00',
        'periodo': '1 mês',
        'tempo': '1 mês',
        'vendas': 'várias vendas',
        'dor': 'começou do zero, 100% orgânico, ainda conciliando CLT',
        'virada': 'colocou meta de 5k em 1 mês, trabalhou com consistência e conseguiu',
        'prova_img': 'prova_aluna_6_fran.jpg',
        'hook': 'Meta de 5k em 1 mês... e conseguiu!',
        'sub_hook': '100% orgânico, conciliando CLT',
        'identificacao': [
            'Francielly Camillo',
            'Começou do ZERO',
            '100% no orgânico',
            'Ainda trabalha de CLT',
            'Colocou meta e foi atrás'
        ],
        'destaque_ident': 'METAL BATIDA: R$ 5K!',
        'cta': 'META DE 5K NO PRÓXIMO MÊS?',
        'story_folder': 'story_fran_5k'
    },
    {
        'nome': 'Aluna R$ 2.100',
        'valor': 'R$ 2.100,42',
        'periodo': 'mês atual',
        'tempo': 'em andamento',
        'vendas': '3 vendas',
        'dor': 'queria complementar a renda',
        'virada': 'começou a vender produtos físicos e já faturou R$ 2.100',
        'prova_img': 'prova_venda_hest.jpg',
        'hook': 'R$ 2.100 no mês... e ainda nem acabou!',
        'sub_hook': 'Começou como renda extra, virou principal',
        'identificacao': [
            'Queria apenas renda extra',
            'Trabalhava em outra área',
            'Não tinha experiência em vendas',
            'Começou com pouco investimento',
            'Foi crescendo aos poucos'
        ],
        'destaque_ident': 'RENDA EXTRA VIRANDO PRINCIPAL',
        'cta': 'COMECE SUA RENDA EXTRA!',
        'story_folder': 'story_aluna_2100'
    },
    {
        'nome': 'Aluna R$ 5.188',
        'valor': 'R$ 5.188,61',
        'periodo': 'mês atual',
        'tempo': 'em andamento',
        'vendas': '4 vendas',
        'dor': 'queria liberdade financeira',
        'virada': 'descobriu que conseguia vender todos os dias e já passou de R$ 5k',
        'prova_img': 'prova_venda_hest.jpg',
        'hook': 'R$ 5.188 e o mês nem acabou!',
        'sub_hook': 'Vendendo todos os dias, no automático',
        'identificacao': [
            'Queria liberdade financeira',
            'Não aguentava mais o trânsito',
            'Queria trabalhar de casa',
            'Não sabia como começar',
            'Descobriu o método certo'
        ],
        'destaque_ident': 'R$ 5K+ ANTES DO FIM DO MÊS',
        'cta': 'LIBERDADE FINANCEIRA É POSSÍVEL!',
        'story_folder': 'story_aluna_5188'
    }
]

def get_fonts():
    try:
        return {
            'title': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80),
            'subtitle': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 55),
            'text': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 42),
            'cta': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60),
            'small': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 35),
            'number': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120),
        }
    except:
        default = ImageFont.load_default()
        return {k: default for k in ['title', 'subtitle', 'text', 'cta', 'small', 'number']}

def create_bg():
    img = Image.new('RGB', (WIDTH, HEIGHT), BLACK)
    draw = ImageDraw.Draw(img)
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(15 + (8 - 15) * ratio)
        g = int(20 + (8 - 20) * ratio)
        b = int(40 + (15 - 40) * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    return img, draw

def draw_centered_text(draw, text, font, color, y, width, shadow=True):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (width - text_w) // 2
    if shadow:
        draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0))
    draw.text((x, y), text, font=font, fill=color)
    return x, text_w

def generate_story(aluna, output_dir, fonts):
    """Gera 5 slides para uma aluna"""
    story_dir = Path(output_dir) / aluna['story_folder']
    story_dir.mkdir(parents=True, exist_ok=True)
    
    # Slide 1: Hook
    img, draw = create_bg()
    lines = aluna['hook'].split('...')
    y = HEIGHT // 2 - 100
    for line in lines:
        line = line.strip()
        if line:
            draw_centered_text(draw, line, fonts['title'], WHITE, y, WIDTH)
            y += 110
    if aluna['sub_hook']:
        draw_centered_text(draw, aluna['sub_hook'], fonts['text'], GRAY, y + 30, WIDTH, shadow=False)
    # Badge
    badge = "🔥 PROVA REAL"
    bbox = draw.textbbox((0, 0), badge, font=fonts['small'])
    bw = bbox[2] - bbox[0] + 50
    bh = 55
    bx = (WIDTH - bw) // 2
    by = y + 100
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=28, fill=GOLD)
    draw.text((bx + 25, by + 10), badge, font=fonts['small'], fill=BLACK)
    img.save(story_dir / "01_hook.jpg")
    
    # Slide 2: Identificação
    img, draw = create_bg()
    title = aluna['identificacao'][0] if aluna['identificacao'] else aluna['nome']
    draw_centered_text(draw, title, fonts['subtitle'], GOLD, 150, WIDTH)
    y = 300
    for line in aluna['identificacao'][1:]:
        draw.text((80, y), line, font=fonts['text'], fill=WHITE)
        y += 80
    if aluna['destaque_ident']:
        draw_centered_text(draw, aluna['destaque_ident'], fonts['subtitle'], GOLD, y + 40, WIDTH)
    img.save(story_dir / "02_identificacao.jpg")
    
    # Slide 3: Virada
    img, draw = create_bg()
    y = HEIGHT // 2 - 150
    virada_lines = aluna['virada'].split(',')
    for line in virada_lines[:3]:
        line = line.strip().capitalize()
        if line:
            draw_centered_text(draw, line, fonts['text'], WHITE, y, WIDTH)
            y += 90
    destaque = f"{aluna['tempo']} depois..."
    draw_centered_text(draw, destaque, fonts['subtitle'], GOLD, y + 40, WIDTH)
    img.save(story_dir / "03_virada.jpg")
    
    # Slide 4: Prova
    img, draw = create_bg()
    badge = "✅ RESULTADO REAL"
    bbox = draw.textbbox((0, 0), badge, font=fonts['small'])
    bw = bbox[2] - bbox[0] + 50
    bh = 55
    bx = (WIDTH - bw) // 2
    by = 100
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=28, fill=GOLD)
    draw.text((bx + 25, by + 10), badge, font=fonts['small'], fill=BLACK)
    
    # Print da prova
    prova_path = f"/root/.openclaw/workspace/projetos-msa/assets/imagens/{aluna['prova_img']}"
    if os.path.exists(prova_path):
        prova = Image.open(prova_path).convert('RGB')
        max_w = int(WIDTH * 0.78)
        max_h = int(HEIGHT * 0.40)
        ratio = min(max_w / prova.width, max_h / prova.height)
        new_w = int(prova.width * ratio)
        new_h = int(prova.height * ratio)
        prova = prova.resize((new_w, new_h), Image.LANCZOS)
        px = (WIDTH - new_w) // 2
        py = 200
        border = 5
        draw.rounded_rectangle([px - border, py - border, px + new_w + border, py + new_h + border],
                              radius=25, outline=GOLD, width=border)
        img.paste(prova, (px, py))
        y_after = py + new_h + 50
    else:
        y_after = 350
    
    periodo_text = f"Resultado em {aluna['periodo']}:"
    draw_centered_text(draw, periodo_text, fonts['text'], WHITE, y_after, WIDTH, shadow=False)
    
    # Valor
    bbox = draw.textbbox((0, 0), aluna['valor'], font=fonts['number'])
    vw = bbox[2] - bbox[0]
    vx = (WIDTH - vw) // 2
    vy = y_after + 70
    for i in range(18, 0, -2):
        draw.text((vx + i//2, vy + i//2), aluna['valor'], font=fonts['number'], fill=(*GOLD, 45)[:3])
    draw.text((vx, vy), aluna['valor'], font=fonts['number'], fill=GOLD)
    
    # Detalhes
    details = f"{aluna['vendas']} | {aluna['tempo']} de mentoria"
    draw_centered_text(draw, details, fonts['small'], GRAY, vy + 160, WIDTH, shadow=False)
    img.save(story_dir / "04_prova.jpg")
    
    # Slide 5: CTA
    img, draw = create_bg()
    cta1 = "QUER RESULTADOS"
    draw_centered_text(draw, cta1, fonts['title'], WHITE, HEIGHT // 2 - 180, WIDTH)
    cta2 = "IGUAIS?"
    bbox = draw.textbbox((0, 0), cta2, font=fonts['title'])
    tw = bbox[2] - bbox[0]
    tx = (WIDTH - tw) // 2
    ty = HEIGHT // 2 - 60
    for i in range(18, 0, -2):
        draw.text((tx + i//2, ty + i//2), cta2, font=fonts['title'], fill=(*GOLD, 45)[:3])
    draw.text((tx, ty), cta2, font=fonts['title'], fill=GOLD)
    
    btn = "👉 LINK NA BIO"
    bbox = draw.textbbox((0, 0), btn, font=fonts['cta'])
    bw = bbox[2] - bbox[0] + 80
    bh = 90
    bx = (WIDTH - bw) // 2
    by = ty + 180
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=20, fill=GOLD)
    draw.text((bx + 40, by + 20), btn, font=fonts['cta'], fill=BLACK)
    
    urg = "⚠️ Só 15 vagas no grupo VIP de pré-lançamento"
    draw_centered_text(draw, urg, fonts['small'], GRAY, by + 120, WIDTH, shadow=False)
    img.save(story_dir / "05_cta.jpg")
    
    print(f"✅ {aluna['nome']}: {story_dir}")
    return story_dir

def main():
    print("🎨 Gerando STORIES para 8 ALUNAS MSA")
    print("=" * 60)
    
    output_dir = "/root/.openclaw/workspace/projetos-msa/output/stories"
    fonts = get_fonts()
    
    stories_gerados = []
    for i, aluna in enumerate(ALUNAS, 1):
        print(f"\n{i}/8. Gerando story: {aluna['nome']}")
        story_path = generate_story(aluna, output_dir, fonts)
        stories_gerados.append(story_path)
    
    print(f"\n{'='*60}")
    print(f"🎉 {len(stories_gerados)} STORIES COMPLETOS GERADOS!")
    print(f"{'='*60}")
    
    for story in stories_gerados:
        print(f"\n📁 {story.name}")
        for slide in sorted(story.glob("*.jpg")):
            size = slide.stat().st_size
            print(f"   - {slide.name}: {size/1024:.1f} KB")
    
    print(f"\n🚀 Total: {len(stories_gerados) * 5} slides prontos para postar!")
    print("📱 Suba os 5 slides de cada story no Instagram (Stories)")
    print("🔗 Não esqueça: link na bio no último slide")

if __name__ == "__main__":
    main()
