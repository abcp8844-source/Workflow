const axios = require('axios');
const cheerio = require('cheerio');

let lastPostedTitle = "";

async function run() {
    try {
        const { data } = await axios.get('https://nuxas-aztr.vercel.app/?t=' + new Date().getTime());
        const $ = cheerio.load(data);
        
        const jobs = [];
        
        $('.group').each((i, el) => {
            const title = $(el).find('h3').text().trim();
            const company = $(el).find('p').text().trim();
            const link = $(el).attr('href');
            
            if (title) {
                jobs.push({ title, company, link: `https://nuxas-aztr.vercel.app${link}` });
            }
        });

        if (jobs.length === 0) return;

        const latestJob = jobs[0];

        if (latestJob.title === lastPostedTitle) {
            return;
        }

        const message = `✨ ${latestJob.title}\n\n🏢 ${latestJob.company}\n\nمزید تفصیلات اور اپلائی کرنے کے لیے ویب سائٹ وزٹ کریں:\n${latestJob.link}\n\n#NexusHire #GlobalJobs #VerifiedOpportunities`;

        const pageId = "514947098373834";
        const url = `https://graph.facebook.com/v20.0/${pageId}/feed`;

        await axios.post(url, {
            message: message,
            access_token: process.env.PAGE_ACCESS_TOKEN
        });

        lastPostedTitle = latestJob.title;
        console.log("Successfully posted: " + latestJob.title);

    } catch (error) {
        console.error("Error:", error.message);
    }
}

run();
