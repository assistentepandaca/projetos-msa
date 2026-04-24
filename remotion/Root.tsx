import {Composition, staticFile} from 'remotion';
import {VSLCarla} from './compositions/VSLCarla';
import {CriativoAds} from './compositions/CriativoAds';
import {StoryReels} from './compositions/StoryReels';

// Tema de cores MSA
export const MSA_COLORS = {
  gold: '#C9A227',
  goldLight: '#E5C158',
  goldDark: '#A88420',
  black: '#0A0A0A',
  white: '#FFFFFF',
  gray: '#6B7280',
  grayLight: '#F9F9F7',
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* VSL da Carla - 2min 30s = 150 frames a 30fps */}
      <Composition
        id="VSLCarla"
        component={VSLCarla}
        durationInFrames={4500} // 2min 30s
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          videoSrc: staticFile('videos/carla_vsl.mp4'),
          legendas: [],
          mostrarProvas: true,
        }}
      />
      
      {/* Criativo de Anúncio - 15s = 450 frames */}
      <Composition
        id="CriativoAds"
        component={CriativoAds}
        durationInFrames={450} // 15s
        fps={30}
        width={1080}
        height={1920} // 9:16 para Reels/TikTok
        defaultProps={{
          headline: 'Como faturei R$ 47k em 30 dias',
          subheadline: 'Sem aparecer, sem estoque',
          cta: 'Link na bio',
          imagem: staticFile('images/prova_venda.jpg'),
        }}
      />
      
      {/* Story/Reels - 15s = 450 frames */}
      <Composition
        id="StoryReels"
        component={StoryReels}
        durationInFrames={450} // 15s
        fps={30}
        width={1080}
        height={1920} // 9:16
        defaultProps={{
          slides: [
            {texto: 'Eu era esteticista...', imagem: ''},
            {texto: 'Trabalhava 12h por dia', imagem: ''},
            {texto: 'Hoje faturei R$ 47k', imagem: ''},
          ],
          cta: 'Link na bio',
        }}
      />
      
      {/* VSL Compacta - 30s = 900 frames */}
      <Composition
        id="VSLCompacta"
        component={VSLCarla}
        durationInFrames={900} // 30s
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          videoSrc: staticFile('videos/carla_vsl.mp4'),
          legendas: [],
          mostrarProvas: false,
          modoCompacto: true,
        }}
      />
    </>
  );
};