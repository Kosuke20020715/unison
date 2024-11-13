// server.js
const express = require('express');
const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3000;



// スクリーンショットの保存ディレクトリを作成
const screenshotDir = path.join(__dirname, 'screenshots');
if (!fs.existsSync(screenshotDir)) {
    fs.mkdirSync(screenshotDir);
}

// スクリーンショットを取得するエンドポイント
app.get('/screenshot', async (req, res) => {
    const url = req.query.url;
    if (!url) {
        return res.status(400).send('URLが必要です');
    }

    const screenshotPath = path.join(screenshotDir, `${encodeURIComponent(url)}.png`);

    // 既にスクリーンショットが存在すれば、それを返す
    if (fs.existsSync(screenshotPath)) {
        return res.sendFile(screenshotPath);
    }

    try {
        //ブラウザの軽量化
        const browser = await puppeteer.launch({
            args: ['--no-sandbox', '--disable-setuid-sandbox'],
            headless: true
        });
        const page = await browser.newPage();
        await page.goto(url, { waitUntil: 'domcontentloaded' });
        await page.screenshot({ path: screenshotPath, fullPage: false,});
        await browser.close();

        res.sendFile(screenshotPath);
    } catch (error) {
        console.error('Error taking screenshot:', error);
        res.status(500).send('スクリーンショットの取得に失敗しました');
    }
});

// スタティックファイル（例: フロントエンドHTML）を提供
app.use(express.static('public'));

app.listen(PORT, () => {
    console.log(`サーバーが起動しました http://localhost:${PORT}`);
});
