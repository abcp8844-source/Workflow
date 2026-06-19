const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

async function scrapeToQueue() {
    try {
        console.log("Starting scrape...");

        // فائل پڑھنے کا محفوظ طریقہ
        const readJson = (file) => {
            if (!fs.existsSync(file)) return [];
            const content = fs.readFileSync(file, 'utf8').trim();
            try { return JSON.parse(content || '[]'); } 
            catch (e) { return []; }
        };

        const history = readJson('history.json');
        let pending = readJson('pending_posts.json');

        const { data } = await axios.get('https://nuxas-aztr.vercel.app/');
        const $ = cheerio.load(data);
        
        let foundLinks = [];
        // ویب سائٹ کا ڈھانچہ چیک کریں، اگر .group نہیں مل رہا تو یہ ایرر دے گا
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

        console.log("Found " + foundLinks.length + " new jobs.");

        for (const link of foundLinks) {
            const { data: jobData } = await axios.get(link);
            const $$ = cheerio.load(jobData);

            const title = $$('h1').text().trim() || $$('h2').first().text().trim();
            const desc = $$('p').text().trim().substring(0, 100).trim() + "...";
            const imageUrl = $$('img').first().attr('src');

            pending.push({ title, description: desc, link, image: imageUrl, timestamp: new Date().toISOString() });
        }

        fs.writeFileSync('pending_posts.json', JSON.stringify(pending, null, 2));
        fs.writeFileSync('history.json', JSON.stringify(history, null, 2));
        console.log("Successfully saved data to files.");

    } catch (error) {
        console.error("Critical Failure:", error.message);
    }
}

scrapeToQueue();
