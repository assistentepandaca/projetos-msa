import {AbsoluteFill, useVideoConfig, useCurrentFrame, Img, interpolate, Easing} from 'remotion';

interface CriativoAdsProps {
  headline?: string;
  subheadline?: string;
  cta?: string;
  imagem?: string;
  perfil?: 'estetica' | 'maes' | 'clt' | 'vergonha' | 'sair_emprego';
}

export const CriativoAds: React.FC<CriativoAdsProps> = ({
  headline = 'Como faturei R$ 47k em 30 dias',
  subheadline = 'Sem aparecer, sem estoque',
  cta = 'Link na bio',
  imagem,
  perfil = 'estetica',
}) => {
  const {width, height, fps, durationInFrames} = useVideoConfig();
  const frame = useCurrentFrame();
  
  // Hook: primeiro 3 segundos
  const hookProgress = interpolate(frame, [0, 90], [0, 1], {
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });
  
  // Corpo: segundos 3-10
  const corpoProgress = interpolate(frame, [90, 300], [0, 1], {
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });
  
  // CTA: últimos 5 segundos
  const ctaProgress = interpolate(frame, [300, 450], [0, 1], {
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.back(1.2)),
  });
  
  // Cores do tema
  const colors = {
    gold: '#C9A227',
    goldLight: '#E5C158',
    black: '#0A0A0A',
    white: '#FFFFFF',
    gray: '#1E1E1E',
  };
  
  return (
    <AbsoluteFill style={{backgroundColor: colors.black}}>
      {/* Background gradiente animado */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: `radial-gradient(ellipse at center, ${colors.gold}20 0%, transparent 70%)`,
          opacity: interpolate(frame, [0, 60], [0, 1]),
        }}
      />
      
      {/* Hook - Primeiros 3s */}
      {frame < 90 && (
        <AbsoluteFill
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: 60,
            opacity: hookProgress,
            transform: `translateY(${(1 - hookProgress) * 50}px)`,
          }}
        >
          <div
            style={{
              background: colors.gold,
              color: colors.black,
              padding: '12px 24px',
              borderRadius: 50,
              fontSize: 32,
              fontWeight: 800,
              marginBottom: 40,
              textTransform: 'uppercase',
              letterSpacing: 2,
            }}
          >
            🔥 ATENÇÃO
          </div>
          <h1
            style={{
              color: colors.white,
              fontSize: 72,
              fontWeight: 900,
              textAlign: 'center',
              lineHeight: 1.1,
              margin: 0,
              textShadow: `0 0 40px ${colors.gold}40`,
            }}
          >
            {headline}
          </h1>
        </AbsoluteFill>
      )}
      
      {/* Corpo - Segundos 3-10 */}
      {frame >= 90 && frame < 300 && (
        <AbsoluteFill
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: 60,
          }}
        >
          {/* Imagem de prova */}
          {imagem && (
            <div
              style={{
                width: width * 0.7,
                height: height * 0.4,
                borderRadius: 20,
                overflow: 'hidden',
                border: `3px solid ${colors.gold}`,
                marginBottom: 40,
                opacity: corpoProgress,
                transform: `scale(${0.8 + corpoProgress * 0.2})`,
              }}
            >
              <Img
                src={imagem}
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover',
                }}
              />
            </div>
          )}
          
          {/* Subheadline */}
          <p
            style={{
              color: colors.white,
              fontSize: 48,
              fontWeight: 700,
              textAlign: 'center',
              margin: 0,
              opacity: corpoProgress,
              transform: `translateY(${(1 - corpoProgress) * 30}px)`,
            }}
          >
            {subheadline}
          </p>
          
          {/* Prova social */}
          <div
            style={{
              marginTop: 30,
              opacity: corpoProgress,
            }}
          >
            <div
              style={{
                display: 'flex',
                gap: 20,
                justifyContent: 'center',
              }}
            >
              {[
                {icon: '💰', texto: '+R$ 250k'},
                {icon: '👩‍🎓', texto: '+500 alunas'},
                {icon: '⏱️', texto: '3-4h/dia'},
              ].map((item, i) => (
                <div
                  key={i}
                  style={{
                    background: colors.gray,
                    padding: '16px 24px',
                    borderRadius: 12,
                    textAlign: 'center',
                    border: `1px solid ${colors.gold}40`,
                  }}
                >
                  <span style={{fontSize: 32, display: 'block'}}>{item.icon}</span>
                  <span style={{color: colors.gold, fontWeight: 800, fontSize: 24}}>{item.texto}</span>
                </div>
              ))}
            </div>
          </div>
        </AbsoluteFill>
      )}
      
      {/* CTA - Últimos 5s */}
      {frame >= 300 && (
        <AbsoluteFill
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: 60,
            opacity: ctaProgress,
          }}
        >
          <h2
            style={{
              color: colors.gold,
              fontSize: 64,
              fontWeight: 900,
              textAlign: 'center',
              marginBottom: 30,
              textShadow: `0 0 30px ${colors.gold}60`,
            }}
          >
            NÃO PERCA TEMPO
          </h2>
          
          <div
            style={{
              background: `linear-gradient(135deg, ${colors.gold} 0%, ${colors.goldLight} 100%)`,
              color: colors.black,
              padding: '28px 56px',
              borderRadius: 16,
              fontSize: 40,
              fontWeight: 900,
              textTransform: 'uppercase',
              letterSpacing: 2,
              boxShadow: `0 8px 30px ${colors.gold}50`,
              animation: frame % 30 < 15 ? 'none' : 'pulse 0.5s ease',
            }}
          >
            {cta} →
          </div>
          
          <p
            style={{
              color: colors.white,
              fontSize: 28,
              marginTop: 30,
              opacity: 0.8,
            }}
          >
            ⚠️ Só 15 vagas no grupo VIP
          </p>
        </AbsoluteFill>
      )}
      
      {/* Barra de progresso */}
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          height: 8,
          background: colors.gray,
        }}
      >
        <div
          style={{
            width: `${(frame / durationInFrames) * 100}%`,
            height: '100%',
            background: colors.gold,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};