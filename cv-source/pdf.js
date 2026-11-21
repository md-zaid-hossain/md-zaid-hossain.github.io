// node pdf.js  ->  Md_Zaid_Hossain_CV.pdf (A4, one page) from cv.html, with the site's local fonts
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage();
await p.goto(`file://${__dirname}/cv.html`); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(800);
await p.pdf({path:`${__dirname}/../media/cv/Md_Zaid_Hossain_CV.pdf`, format:'A4', printBackground:true, preferCSSPageSize:true});
await b.close(); })();
