export interface AppConfig {
  appName: string;
  apiEndpoint: string;
}

export const APP_CONFIG: AppConfig = {
  appName: 'Babl',
  apiEndpoint: 'http://localhost:8000'
};
