const axios = require('axios');
const cheerio = require('cheerio');

async function run() {
    try {
        const { data } = await axios.get('https://nuxas-aztr.vercel.app/');
        const $ = cheerio.load(data);
        
        const title = $('h2').first().text().trim();
        const content = $('p').first().text().trim().substring(0, 150) + "...";
        const link = "https://nuxas-aztr.vercel.app/";
        const message = `${title}\n\n${content}\n\n${link}`;

        await axios.post(`https://graph.facebook.com/v20.0/me/feed`, null, {
            params: {
                message: message,
                access_token: process.env.PAGE_ACCESS_TOKEN
            }
        });

        console.log("Post success");
    } catch (error) {
        console.error("Error:", error.response ? error.response.data : error.message);
    }
}
run();
