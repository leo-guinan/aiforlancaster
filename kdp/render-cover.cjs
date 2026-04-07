const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  
  await page.setViewport({ width: 1600, height: 2560, deviceScaleFactor: 1 });
  
  const filePath = path.resolve(__dirname, 'cover-photo.html');
  await page.goto(`file://${filePath}`, { waitUntil: 'networkidle0' });
  
  // Wait for font to load
  await page.evaluateHandle('document.fonts.ready');
  await new Promise(r => setTimeout(r, 2000));
  
  await page.screenshot({
    path: path.resolve(__dirname, 'cover-front-photo.png'),
    type: 'png',
    clip: { x: 0, y: 0, width: 1600, height: 2560 }
  });
  
  console.log('Cover rendered: cover-front-photo.png (1600x2560)');
  await browser.close();
})();
