const axios = require('axios');
const cheerio = require('cheerio');

async function run() {
    try {
        const { data } = await axios.get('https://nuxas-aztr.vercel.app/');
        const $ = cheerio.load(data);
        
        // یہاں ہم پہلی ہیڈنگ (NexusHire) کو چھوڑ کر جاب کارڈز والی ہیڈنگ ڈھونڈ رہے ہیں
        // جاب کارڈز کے ٹائٹل اکثر <h3> یا <h2> میں ہوتے ہیں، ہم پہلے کارڈ کا ٹائٹل اٹھائیں گے
        const title = $('h3, h2').not(':contains("NexusHire")').first().text().trim();
        
        // جاب کارڈ کی تفصیل اٹھانا (اگر پیراگراف میں ہے)
        const description = $('p').not(':contains("NexusHire")').filter((i, el) => $(el).text().length > 30).first().text().trim().substring(0, 200) + "...";
        
        const link = "https://nuxas-aztr.vercel.app/";
        const fullMessage = `${title}\n\n${description}\n\nRead more:\n${link}`;

        const pageId = "514947098373834";
        const url = `https://graph.facebook.com/v20.0/${pageId}/feed`;

        const params = new URLSearchParams();
        params.append('message', fullMessage);
        params.append('access_token', process.env.PAGE_ACCESS_TOKEN);

        await axios.post(url, params);

        console.log("Success");
    } catch (error) {
        console.error("Error:", error.response ? error.response.data : error.message);
    }
}
run();
