const axios = require('axios');
const cheerio = require('cheerio');

async function run() {
    try {
        const { data } = await axios.get('https://nuxas-aztr.vercel.app/');
        const $ = cheerio.load(data);
        
        const title = $('h2').first().text().trim();
        const description = $('p').first().text().trim().substring(0, 150) + "...";
        const link = "https://nuxas-aztr.vercel.app/";
        const fullMessage = `${title}\n\n${description}\n\n${link}`;

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
