const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

async function scrapeToQueue() {
    try {
        await new Promise(resolve => setTimeout(resolve, 2000));

        const { data } = await axios.get('https://nuxas-aztr.vercel.app/?t=' + new Date().getTime());
        const $ = cheerio.load(data);
        
        const history = fs.existsSync('history.json') ? JSON.parse(fs.readFileSync('history.json')) : [];
        let pending = fs.existsSync('pending_posts.json') ? JSON.parse(fs.readFileSync('pending_posts.json')) : [];

        let foundLinks = [];
        $('.group').each((i, el) => {
            const href = $(el).attr('href');
            if (href && href.includes('/jobs/')) {
                const fullLink = "https://nuxas-aztr.vercel.app" + href;
                if (!history.includes(fullLink) && !pending.find(p => p.link === fullLink)) {
                    foundLinks.push(fullLink);
                }
            }
        });

        if (foundLinks.length === 0) return;

        const targetLink = foundLinks[0];
        const { data: jobData } = await axios.get(targetLink);
        const $$ = cheerio.load(jobData);

        const title = $$('h1').text().trim() || $$('h2').first().text().trim();
        const desc = $$('p').text().trim().substring(0, 100).trim() + "...";
        const imageUrl = $$('img').first().attr('src');

        const newPost = {
            title,
            description: desc,
            link: targetLink,
            image: imageUrl,
            timestamp: new Date().toISOString()
        };

        pending.push(newPost);
        fs.writeFileSync('pending_posts.json', JSON.stringify(pending, null, 2));
        console.log("New post added to pending_posts.json:", targetLink);

    } catch (error) {
        console.error("Scraping Error:", error.message);
    }
}

scrapeToQueue();
