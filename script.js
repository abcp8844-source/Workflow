const axios = require('axios');
const cheerio = require('cheerio');

async function run() {
    try {
        const { data } = await axios.get('https://nuxas-aztr.vercel.app/');
        const $ = cheerio.load(data);
        
        // یہ لائن صرف ان باکسز کو ڈھونڈے گی جن میں جاب کی تفصیل ہوتی ہے
        // آپ کی ویب سائٹ کے ڈیزائن کے مطابق اسے جاب کارڈز کا پہلا حصہ اٹھانا چاہیے
        const jobTitle = $('h2, h3').filter((i, el) => $(el).text().length > 10).eq(1).text().trim();
        const jobDesc = $('p').filter((i, el) => $(el).text().length > 50).eq(1).text().trim().substring(0, 200) + "...";
        
        const link = "https://nuxas-aztr.vercel.app/";
        const message = `${jobTitle}\n\n${jobDesc}\n\nApply here: ${link}`;

        const pageId = "514947098373834";
        const url = `https://graph.facebook.com/v20.0/${pageId}/feed`;

        const params = new URLSearchParams();
        params.append('message', message);
        params.append('access_token', process.env.PAGE_ACCESS_TOKEN);

        await axios.post(url, params);

        console.log("Success");
    } catch (error) {
        console.error("Error:", error.response ? error.response.data : error.message);
    }
}
run();
