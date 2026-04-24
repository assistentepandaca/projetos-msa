import {AbsoluteFill, useVideoConfig, useCurrentFrame, Video, staticFile, interpolate, spring} from 'remotion';
import {useCallback, useEffect, useState} from 'react';

interface VSLCarlaProps {
  videoSrc?: string;
  legendas?: Array<{texto: string; inicio: number; fim: number}>;
  mostrarProvas?: boolean;
  modoCompacto?: boolean;
}

// Legendas padrão do roteiro VSL
const legendasPadrao = [
  {texto: 'R$ 47.000 EM UM MÊS', inicio: 0, fim: 5},
  {texto: 'SEM APARECER', inicio: 5, fim: 10},
  {texto: 'PRESO NA CLÍNICA', inicio: 15, fim: 20},
  {texto: 'A VIRADA: R$ 20 DE ANÚNCIO', inicio: 30, fim: 35},
  {texto: '3 PASSOS SIMPLES', inicio: 45, fim: 50},
  {texto: '+R$ 250 MIL FATURADOS', inicio: 60, fim: 65},
  {texto: 'MSA: MÉTODO VALIDADO', inicio: 80, fim: 85},
  {texto: '7 DIAS DE GARANTIA', inicio: 95, fim: 100},
  {texto: 'SÓ 15 VAGAS', inicio: 110, fim: 115},
  {texto: 'CLIQUE ABAIXO', inicio: 130, fim: 135},
];

export const VSLCarla: React.FC<VSLCarlaProps> = ({
  videoSrc,
  legendas = legendasPadrao,
  mostrarProvas = true,
  modoCompacto = false,
}) => {
  const {width, height, fps, durationInFrames} = useVideoConfig();
  const frame = useCurrentFrame();
  
  // Animar entrada de elementos
  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: 'clamp',
  });
  
  // Legendas dinâmicas baseadas no tempo atual
  const tempoAtual = frame / fps;
  const legendaAtual = legendas.find(
    (l) => tempoAtual >= l.inicio && tempoAtual <= l.fim
  );
  
  // Animação da legenda
  const legendaOpacity = legendaAtual 
    ? interpolate(
        frame - legendaAtual.inicio * fps,
        [0, 10, (legendaAtual.fim - legendaAtual.inicio) * fps - 10, (legendaAtual.fim - legendaAtual.inicio) * fps],
        [0, 1, 1, 0],
        {extrapolateRight: 'clamp'}
      )
    : 0;
  
  return (
    <AbsoluteFill style={{backgroundColor: '#0A0A0A'}}>
      {/* Vídeo da Carla (quando disponível) */}
      {videoSrc && (
        <Video
          src={videoSrc}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
          }}
          startFrom={modoCompacto ? 0 : 0}
          endAt={modoCompacto ? 900 : undefined}
        />
      )}
      
      {/* Placeholder quando não tem vídeo */}
      {!videoSrc && (
        <AbsoluteFill
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
          }}
        >
          <div style={{textAlign: 'center', color: '#fff'}}>
            <h1 style={{fontSize: 80, fontWeight: 900, color: '#C9A227', marginBottom: 20}}>
              MSA
            </h1>
            <p style={{fontSize: 32, color: '#ccc'}}>
              Adicione o vídeo da Carla aqui
            </p>
            <p style={{fontSize: 20, color: '#666', marginTop: 10}}>
              Coloque o arquivo em remotion/public/videos/carla_vsl.mp4
            </p>
          </div>
        </AbsoluteFill>
      )}
      
      {/* Overlay escuro nos cantos para legibilidade */}
      <AbsoluteFill
        style={{
          background: 'linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, transparent 30%, transparent 70%, rgba(0,0,0,0.5) 100%)',
          pointerEvents: 'none',
        }}
      />
      
      {/* Legendas grandes no estilo Cabelinho Black */}
      {legendaAtual && (
        <AbsoluteFill
          style={{
            display: 'flex',
            alignItems: 'flex-end',
            justifyContent: 'center',
            paddingBottom: 120,
            opacity: legendaOpacity,
          }}
        >
          <div
            style={{
              background: 'rgba(0,0,0,0.7)',
              padding: '20px 40px',
              borderRadius: 12,
              borderLeft: '6px solid #C9A227',
              maxWidth: width * 0.8,
            }}
          >
            <p
              style={{
                color: '#fff',
                fontSize: 48,
                fontWeight: 800,
                textAlign: 'center',
                margin: 0,
                textShadow: '2px 2px 4px rgba(0,0,0,0.8)',
                lineHeight: 1.3,
              }}
            >
              {legendaAtual.texto}
            </p>
          </div>
        </AbsoluteFill>
      )}
      
      {/* Badge de prova social flutuante */}
      {mostrarProvas && (
        <div
          style={{
            position: 'absolute',
            top: 40,
            right: 40,
            background: 'rgba(201, 162, 39, 0.9)',
            color: '#0A0A0A',
            padding: '16px 24px',
            borderRadius: 12,
            fontWeight: 800,
            fontSize: 24,
            opacity: interpolate(frame, [60, 90], [0, 1]),
          }}
        >
          🔥 +R$ 250k FATURADOS
        </div>
      )}
      
      {/* CTA no final */}
      {frame > durationInFrames - 150 && (
        <AbsoluteFill
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: 'rgba(0,0,0,0.8)',
            opacity: interpolate(frame, [durationInFrames - 150, durationInFrames - 120], [0, 1]),
          }}
        >
          <div style={{textAlign: 'center'}}>
            <h2
              style={{
                color: '#C9A227',
                fontSize: 64,
                fontWeight: 900,
                marginBottom: 30,
                textShadow: '0 0 30px rgba(201, 162, 39, 0.5)',
              }}
            >
              🚀 CLIQUE ABAIXO
            </h2>
            <p style={{color: '#fff', fontSize: 32, marginBottom: 20}}>
              Garanta sua vaga no Grupo VIP
            </p>
            <div
              style={{
                display: 'inline-block',
                background: '#C9A227',
                color: '#0A0A0A',
                padding: '20px 40px',
                borderRadius: 12,
                fontSize: 28,
                fontWeight: 800,
                animation: 'pulse 2s infinite',
              }}
            >
              SÓ 15 VAGAS →
            </div>
          </div>
        </AbsoluteFill>
      )}
      
      {/* Barra de progresso no topo */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: 6,
          background: 'rgba(255,255,255,0.1)',
        }}
      >
        <div
          style={{
            width: `${(frame / durationInFrames) * 100}%`,
            height: '100%',
            background: '#C9A227',
            transition: 'width 0.1s linear',
          }}
        />
      </div>
    </AbsoluteFill>
  );
};