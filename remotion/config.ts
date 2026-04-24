import {Config} from '@remotion/cli/config';

export const config: Config = {
  // Onde os vídeos serão salvos
  outDir: './output/',
  
  // Resolução padrão (Full HD)
  width: 1920,
  height: 1080,
  fps: 30,
  
  // Para stories/reels (1080x1920)
  // width: 1080,
  // height: 1920,
  
  // Tempo padrão de renderização
  defaultProps: {},
  
  // Log level
  logLevel: 'verbose',
  
  // Concorrência
  concurrency: 4,
  
  // Qualidade
  videoBitrate: '10M',
  
  // Frame range (para testes rápidos)
  // frameRange: [0, 150],
};