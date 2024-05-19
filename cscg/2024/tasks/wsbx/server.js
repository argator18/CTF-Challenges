const path = require('node:path');
const express = require('express');
const morgan = require('morgan');
const puppeteer = require('puppeteer');

const HOST = process.env.HOST ?? '127.0.0.1';
const PORT = process.env.PORT ?? '1337';
const FLAG = process.env.FLAG ?? 'CSCG{fake_flag}';
const BOT_TIMEOUT = Number(process.env.BOT_TIMEOUT || 10);
const PAGE_URL = `http://localhost:${PORT}`;

const app = express();
app.use(morgan('common'));
app.use(express.static(path.join(__dirname, 'static')));

app.get('/report', express.json(), (req, res) => {
    const { code = '' } = req.query;
    visit(code);
    res.status(204).end();
});

app.listen(PORT, HOST, () => console.log(`Listening on ${HOST}:${PORT}`));

async function visit(code) {
    try {
        const url = new URL(PAGE_URL);

        const browser = await puppeteer.launch({
            args: [ '--no-sandbox' ],
            headless: 'old',
        });
        
        console.log('Placing flag');
        const page = await browser.newPage();
        await page.goto(url.toString());
        await page.evaluate((flag) => localStorage.setItem('flag', flag), FLAG);
        await page.close();
    
        url.searchParams.set('code', code);
        console.log(`Visiting ${url}`);
        const playerPage = await browser.newPage();
        setTimeout(() => browser.close(), BOT_TIMEOUT * 1000);
        await playerPage.goto(url.toString());
    } catch (error) {
        console.error(error);
    }
}
