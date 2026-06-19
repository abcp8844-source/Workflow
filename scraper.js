const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

async function scrapeToQueue() {
    try {
        console.log("Starting scrape...");
        // ویب سائٹ کا مین پیج
        const { data } = await axios.get('https://nuxas-aztr.vercel.app/');
        const $ = cheerio.load(data);
        
        // یہاں ہم نے سلیکٹر تبدیل کیا ہے۔ 
        // ہم تمام <a> لنکس ڈھونڈ رہے ہیں جن میں /jobs/ ہے
        let foundLinks = [];
        $('a').each((i, el) => {
            const href = $(el).attr('href');
            if (href && href.includes('/jobs/')) {
                const fullLink = "https://nuxas-aztr.vercel.app" + href;
                foundLinks.push(fullLink);
            }
        });

        // ڈپلیکیٹ لنکس ہٹا دیں
        foundLinks = [...new Set(foundLinks)];
        console.log("Total potential job links found: " + foundLinks.length);

        // ہسٹری چیک
        const history = JSON.parse(fs.readFileSync('history.json', 'utf8') || '[]');
        let pending = JSON.parse(fs.readFileSync('pending_posts.json', 'utf8') || '[]');
        
        let newJobsFound = 0;
        for (const link of foundLinks) {
            if (!history.includes(link) && !pending.find(p => p.link === link)) {
                // ڈیٹا نکالیں
                const { data: jobData } = await axios.get(link);
                const $$ = cheerio.load(jobData);
                
                const title = $$('h1').text().trim() || "No Title";
                const desc = $$('p').text().trim().substring(0, 100).trim() + "...";
                
                pending.push({ title, description: desc, link, timestamp: new Date().toISOString() });
                newJobsFound++;
            }
            if (newJobsFound >= 6) break;
        }

        fs.writeFileSync('pending_posts.json', JSON.stringify(pending, null, 2));
        console.log("Successfully added " + newJobsFound + " new jobs to queue.");

    } catch (error) {
        console.error("Critical Failure:", error.message);
    }
}

scrapeToQueue();
