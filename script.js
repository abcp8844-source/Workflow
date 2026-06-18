const axios = require('axios');
const cheerio = require('cheerio');

async function run() {
    try {
        const { data } = await axios.get('https://nuxas-aztr.vercel.app/');
        const $ = cheerio.load(data);
        
        let targetLink = "";
        $('.group').each((i, el) => {
            if (i === 0) {
                targetLink = "https://nuxas-aztr.vercel.app" + $(el).attr('href');
            }
        });

        if (!targetLink) throw new Error("No job link found");

        const { data: jobData } = await axios.get(targetLink);
        const $$ = cheerio.load(jobData);

        const title = $$('h1').text().trim() || $$('h2').first().text().trim();
        const fullDesc = $$('p').text().trim();
        const shortDesc = fullDesc.substring(0, 150).trim() + "...";
        
        if (!title) throw new Error("Title not found");

        const message = `${title}\n\n${shortDesc}\n\nApply here: ${targetLink}`;

        const url = `https://graph.facebook.com/v20.0/${process.env.PAGE_ID}/feed`;

        await axios.post(url, {
            message: message,
            link: targetLink,
            access_token: process.env.PAGE_ACCESS_TOKEN
        });

        console.log("Post successful");
    } catch (error) {
        console.error("Error:", error.message);
    }
}

run();
