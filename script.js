const axios = require('axios');
const cheerio = require('cheerio');

async function run() {
    const { data } = await axios.get('https://nuxas-aztr.vercel.app/');
    const $ = cheerio.load(data);
    const title = $('h2').first().text().trim();
    const content = $('p').first().text().trim().substring(0, 150) + "...";
    const link = "مزید: https://nuxas-aztr.vercel.app/";
    const message = `${title}\n\n${content}\n\n${link}`;

    await axios.post(`https://graph.facebook.com/v20.0/${process.env.PAGE_ID}/feed`, {
        message: message,
        access_token: process.env.PAGE_ACCESS_TOKEN
    });
}
run();
