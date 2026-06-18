const axios = require('axios');
const cheerio = require('cheerio');

let lastPostedTitle = "";

async function run() {
    try {
        const { data } = await axios.get('https://nuxas-aztr.vercel.app/?t=' + new Date().getTime());
        const $ = cheerio.load(data);
        
        let jobLink = $('.group').first().attr('href');
        if (!jobLink) return;
        
        const fullLink = "https://nuxas-aztr.vercel.app" + jobLink;

        const { data: jobData } = await axios.get(fullLink);
        const $$ = cheerio.load(jobData);

        const title = $$('h1').text().trim() || $$('h2').first().text().trim();
        const fullDesc = $$('p').text().trim();
        const shortDesc = fullDesc.substring(0, 150).trim() + "...";
        const imageUrl = $$('img').first().attr('src');

        if (title === lastPostedTitle) return;

        const message = `${title}\n\n${shortDesc}\n\nApply here: ${fullLink}`;

        const pageId = "514947098373834";
        const url = `https://graph.facebook.com/v20.0/${pageId}/feed`;

        await axios.post(url, {
            message: message,
            link: fullLink,
            access_token: process.env.PAGE_ACCESS_TOKEN
        });

        lastPostedTitle = title;
    } catch (error) {
        console.error("Error:", error.message);
    }
}

run();
