const axios = require('axios');
const cheerio = require('cheerio');

async function run() {
    const siteUrl = 'https://nuxas-aztr.vercel.app/';
    const { data } = await axios.get(siteUrl);
    const $ = cheerio.load(data);

    // آپ کی ویب سائٹ کے مطابق selectors
    const title = $('h2').first().text().trim(); // پہلا ٹائٹل
    const content = $('p').first().text().trim().substring(0, 150) + "..."; 
    const link = "مزید تفصیلات یہاں دیکھیں: " + siteUrl;

    const message = `${title}\n\n${content}\n\n${link}`;

    // فیس بک پر پوسٹ
    await axios.post(`https://graph.facebook.com/v20.0/${process.env.GROUP_ID}/feed`, {
        message: message,
        access_token: process.env.FB_ACCESS_TOKEN
    });
    console.log("پوسٹ کامیابی سے ہو گئی!");
}

run().catch(err => console.error("Error:", err.message));
