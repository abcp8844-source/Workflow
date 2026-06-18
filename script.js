const axios = require('axios');
const cheerio = require('cheerio');

async function run() {
    try {
        const { data } = await axios.get('https://nuxas-aztr.vercel.app/');
        const $ = cheerio.load(data);
        
        // یہ سلیکٹرز آپ کی ویب سائٹ کے مطابق ہیں
        const title = $('h2').first().text().trim();
        const content = $('p').first().text().trim().substring(0, 150) + "...";
        const link = "مزید تفصیلات: https://nuxas-aztr.vercel.app/";
        const message = `${title}\n\n${content}\n\n${link}`;

        const fbUrl = `https://graph.facebook.com/v20.0/${process.env.PAGE_ID}/feed`;
        
        await axios.post(fbUrl, null, {
            params: {
                message: message,
                access_token: process.env.PAGE_ACCESS_TOKEN
            }
        });
        console.log("پوسٹ کامیابی سے ہو گئی!");
    } catch (error) {
        console.error("ایرر:", error.response ? error.response.data : error.message);
    }
}
run();
