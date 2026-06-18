const axios = require('axios');
const cheerio = require('cheerio');

async function run() {
    try {
        const { data } = await axios.get('https://nuxas-aztr.vercel.app/');
        const $ = cheerio.load(data);
        
        // 1. ٹائٹل: مکمل اٹھائے گا
        const title = $('h2').first().text().trim();
        
        // 2. تفصیل: صرف ابتدائی 150 کریکٹرز (مختصر)
        const description = $('p').first().text().trim().substring(0, 150) + "...";
        
        // 3. لنک: جو ہم نے سیٹ کیا ہے
        const link = "مزید تفصیلات: https://nuxas-aztr.vercel.app/";
        
        // پوسٹ کا مجموعی ڈھانچہ
        const message = `${title}\n\n${description}\n\n${link}`;

        const pageId = "514947098373834";
        const url = `https://graph.facebook.com/v20.0/${pageId}/feed`;
        
        await axios.post(url, {
            message: message
        }, {
            params: {
                access_token: process.env.PAGE_ACCESS_TOKEN
            }
        });

        console.log("پوسٹ کامیابی سے ہو گئی!");
    } catch (error) {
        console.error("ایرر:", error.response ? error.response.data : error.message);
    }
}
run();
