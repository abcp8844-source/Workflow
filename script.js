const axios = require('axios');
const cheerio = require('cheerio');

async function run() {
    try {
        const { data } = await axios.get('https://nuxas-aztr.vercel.app/?t=' + new Date().getTime());
        const $ = cheerio.load(data);
        
        const jobLink = $('.group').first().attr('href');
        if (!jobLink) throw new Error("Job link not found.");
        
        const fullLink = "https://nuxas-aztr.vercel.app" + jobLink;
        const { data: jobData } = await axios.get(fullLink);
        const $$ = cheerio.load(jobData);

        const title = $$('h1').text().trim() || $$('h2').first().text().trim();
        const fullDesc = $$('p').text().trim();
        
        // 150 الفاظ کی حد کے اندر ٹائٹل، ڈسکرپشن اور لنک کا حساب
        const shortDesc = fullDesc.substring(0, 100).trim() + "...";
        const message = `${title}\n\n${shortDesc}\n\nApply here: ${fullLink}`;

        const payload = {
            message: message,
            link: fullLink,
            access_token: process.env.PAGE_ACCESS_TOKEN
        };

        const url = `https://graph.facebook.com/v20.0/${process.env.PAGE_ID}/feed`;
        const response = await axios.post(url, payload);

        console.log("Post ID:", response.data.id);
    } catch (error) {
        console.error("Error:", error.response ? JSON.stringify(error.response.data) : error.message);
    }
}

run();
