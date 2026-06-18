const axios = require('axios');
const cheerio = require('cheerio');

async function run() {
    try {
        const { data } = await axios.get('https://nuxas-aztr.vercel.app/');
        const $ = cheerio.load(data);
        
        const title = $('h2').first().text().trim();
        const content = $('p').first().text().trim().substring(0, 150) + "...";
        const link = "مزید: https://nuxas-aztr.vercel.app/";
        const message = `${title}\n\n${content}\n\n${link}`;

        // یہاں براہ راست پیج آئی ڈی ہے
        const pageId = "514947098373834";
        const url = `https://graph.facebook.com/v20.0/${pageId}/feed`;
        
        await axios.post(url, {
            message: message
        }, {
            params: {
                access_token: process.env.PAGE_ACCESS_TOKEN
            }
        });
        console.log("کامیابی سے پوسٹ ہو گئی!");
    } catch (error) {
        console.error("ایرر:", error.response ? error.response.data : error.message);
    }
}
run();
