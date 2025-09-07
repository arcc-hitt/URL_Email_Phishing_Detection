// set-env.ts
import { writeFileSync } from 'fs';
import { resolve } from 'path';

const targetPath = resolve(__dirname, './src/environments/environment.ts');

// Choose file based on Angular CLI environment (default = development)
const isProd = process.argv.includes('--prod');
const envFile = isProd ? '.env.production' : '.env.development';

// Load env vars
const dotenv = require('dotenv');
dotenv.config({ path: envFile });

// Build the environment.ts content
const envConfig = `
export const environment = {
  production: ${isProd},
  apiUrl: '${process.env['NG_APP_API_URL']}',
  googleClientId: '${process.env['NG_APP_GOOGLE_CLIENT_ID']}',
  discoveryDocs: '${process.env['NG_APP_DISCOVERY_DOCS']}',
  gmailScope: '${process.env['NG_APP_GMAIL_SCOPE']}'
};
`;

writeFileSync(targetPath, envConfig, { encoding: 'utf-8' });
