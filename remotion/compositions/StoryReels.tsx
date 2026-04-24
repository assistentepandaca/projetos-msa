import {AbsoluteFill, useVideoConfig, useCurrentFrame, interpolate, Easing} from 'remotion';

interface StoryReelsProps {
  slides?: Array<{texto: string; destaque?: string}>;
  cta?: string;
  perfil?: string;
}

export const StoryReels: React.FC<StoryReelsProps> = ({
  slides = [
    {texto: 'Eu era esteticista...', destaque: '12h por dia'},
    {texto: 'Trabalhava', destaque: 'sem parar'},
    {texto: 'Hoje faturei', destaque: 'R$ 47.000'},
    {texto: 'Em apenas', destaque: '30 dias'},
    {texto: 'Sem aparecer', destaque: 'sem estoque'},
  ],
  cta = 'Link na bio',
  perfil = 'esteticista',
}) => {
  const {width, height, fps, durationInFrames} = useVideoConfig();
  const frame = useCurrentFrame();
  
  const colors = {
    gold: '#C9A227',
    goldLight: '#E5C158',
    black: '#0A0A0A',
    white: '#FFFFFF',
    gray: '#1E1E1E',
  };
  
  // Duração de cada slide
  const framesPorSlide = durationInFrames / (slides.length + 1);
  
  // Qual slide está ativo
  const slideAtual = Math.min(Math.floor(frame / framesPorSlide), slides.length);
  const progressoSlide = (frame % framesPorSlide) / framesPorSlide;
  
  // Se for o último slide, mostrar CTA
  const mostrarCTA = slideAtual >= slides.length;
  
  return (
    <AbsoluteFill style={{backgroundColor: colors.black}}>
      {/* Background animado */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: `radial-gradient(circle at ${50 + Math.sin(frame * 0.02) * 20}% ${50 + Math.cos(frame * 0.02) * 20}%, ${colors.gold}15 0%, transparent 50%)`,
        }}
      />
      
      {/* Contador de slides no topo */}
      <div
        style={{
          position: 'absolute',
          top: 40,
          left: 40,
          right: 40,
          display: 'flex',
          gap: 8,
          zIndex: 10,
        }}
      >
        {slides.map((_, i) => (
          <div
            key={i}
            style={{
              flex: 1,
              height: 4,
              background: colors.gray,
              borderRadius: 2,
              overflow: 'hidden',
            }}
          >
            <div
              style={{
                width: `${
                  i < slideAtual 
                    ? 100 
                    : i === slideAtual 
                      ? progressoSlide * 100 
                      : 0
                }%`,
                height: '100%',
                background: colors.gold,
                borderRadius: 2,
                transition: 'width 0.1s linear',
              }}
            />
          </div>
        ))}
      </div>
      
      {/* Slides */}
      {!mostrarCTA && slides[slideAtual] && (
        <AbsoluteFill
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: 80,
          }}
        >
          {/* Ícone/Emoji */}
          <div
            style={{
              fontSize: 120,
              marginBottom: 40,
              opacity: interpolate(progressoSlide, [0, 0.2], [0, 1]),
              transform: `scale(${interpolate(progressoSlide, [0, 0.3], [0.5, 1], {
                easing: Easing.out(Easing.back(1.5)),
              })})`,
            }}
          >
            {slideAtual === 0 && '💅'}
            {slideAtual === 1 && '😫'}
            {slideAtual === 2 && '💰'}
            {slideAtual === 3 && '📅'}
            {slideAtual === 4 && '🚀'}
          </div>
          
          {/* Texto */}
          <p
            style={{
              color: colors.white,
              fontSize: 56,
              fontWeight: 600,
              textAlign: 'center',
              lineHeight: 1.3,
              margin: 0,
              opacity: interpolate(progressoSlide, [0.1, 0.3], [0, 1]),
              transform: `translateY(${interpolate(progressoSlide, [0.1, 0.3], [30, 0])}px)`,
            }}
          >
            {slides[slideAtual].texto}
          </p>
          
          {/* Destaque */}
          {slides[slideAtual].destaque && (
            <h2
              style={{
                color: colors.gold,
                fontSize: 80,
                fontWeight: 900,
                textAlign: 'center',
                margin: '20px 0 0 0',
                lineHeight: 1.1,
                opacity: interpolate(progressoSlide, [0.2, 0.5], [0, 1]),
                transform: `scale(${interpolate(progressoSlide, [0.2, 0.5], [0.8, 1], {
                  easing: Easing.out(Easing.back(1.2)),
                })})`,
              }}
            >
              {slides[slideAtual].destaque}
            </h2>
          )}
        </AbsoluteFill>
      )}
      
      {/* CTA Final */}
      {mostrarCTA && (
        <AbsoluteFill
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: 80,
          }}
        >
          <div
            style={{
              background: colors.gold,
              color: colors.black,
              padding: '20px 40px',
              borderRadius: 50,
              fontSize: 36,
              fontWeight: 800,
              marginBottom: 40,
              textTransform: 'uppercase',
            }}
          >
            🔥 ÚLTIMA CHANCE
          </div>
          
          <h2
            style={{
              color: colors.white,
              fontSize: 64,
              fontWeight: 900,
              textAlign: 'center',
              lineHeight: 1.2,
              margin: '0 0 30px 0',
            }}
          >
            Clique no link
            <br />
            <span style={{color: colors.gold}}>antes que acabe</span>
          </h2>
          
          <div
            style={{
              background: `linear-gradient(135deg, ${colors.gold} 0%, ${colors.goldLight} 100%)`,
              color: colors.black,
              padding: '24px 48px',
              borderRadius: 16,
              fontSize: 36,
              fontWeight: 900,
              textTransform: 'uppercase',
              boxShadow: `0 8px 30px ${colors.gold}50`,
            }}
          >
            {cta} →
          </div>
          
          <p
            style={{
              color: colors.white,
              fontSize: 28,
              marginTop: 30,
              opacity: 0.7,
            }}
          >
            ⏰ Só 15 vagas
          </p>
        </AbsoluteFill>
      )}
      
      {/* Logo MSA no canto */}
      <div
        style={{
          position: 'absolute',
          bottom: 40,
          left: 40,
          color: colors.gold,
          fontSize: 24,
          fontWeight: 900,
          letterSpacing: 3,
          opacity: 0.5,
        }}
      >
        MSA
      </div>
    </AbsoluteFill>
  );
};