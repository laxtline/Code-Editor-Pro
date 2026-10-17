const { defineConfig } = require('@playwright/test');
module.exports = defineConfig({
  testDir: './tests', timeout: 90000, workers: 1,
  use: { baseURL: 'http://127.0.0.1:4173', browserName: 'chromium', headless: true },
  webServer: [
    { command: 'python -m http.server 4173 --bind 127.0.0.1', url: 'http://127.0.0.1:4173', reuseExistingServer: true },
    { command: 'python tests/serve_packaged.py', url: 'http://127.0.0.1:4174/Code-Editor-Pro/', reuseExistingServer: true }
  ]
});
