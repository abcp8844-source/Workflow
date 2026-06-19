const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

async function scrapeToQueue() {
    try {
        console.log("Scraping started...");
        const { data } = await axios.get('https://nuxas-aztr.vercel.app/?t=' + new Date().getTime());
        const $ = cheerio.load(data);
        
        const history = JSON.parse(fs.readFileSync('history.json', 'utf8') || '[]');
        let pending = JSON.parse(fs.readFileSync('pending_posts.json', 'utf8') || '[]');

        let foundLinks = [];
        $('.group').each((i, el) => {
            const href = $(el).attr('href');
            if (href && href.includes('/jobs/')) {
                const fullLink = "https://nuxas-aztr.vercel.app" + href;
                if (!history.includes(fullLink) && !pending.find(p => p.link === fullLink)) {
                    foundLinks.push(fullLink);
                }
            }
            if (foundLinks.length >= 6) return false;
        });

        console.log("Links found: " + foundLinks.length);

        for (const link of foundLinks) {
            const { data: jobData } = await axios.get(link);
            const $$ = cheerio.load(jobData);

            const title = $$('h1').text().trim() || $$('h2').first().text().trim();
            const desc = $$('p').text().trim().substring(0, 100).trim() + "...";
            const imageUrl = $$('img').first().attr('src');

            pending.push({ title, description: desc, link, image: imageUrl, timestamp: new Date().toISOString() });
        }

        fs.writeFileSync('pending_posts.json', JSON.stringify(pending, null, 2));
        console.log("Data saved successfully.");
    } catch (error) {
        console.error("Critical Failure:", error.message);
    }
}

scrapeToQueue();
