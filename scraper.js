const puppeteer = require('puppeteer');
const fs = require('fs');

async function scrapeToQueue() {
    console.log("Launching headless browser...");
    const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
    const page = await browser.newPage();
    
    await page.goto('https://nuxas-aztr.vercel.app/', { waitUntil: 'networkidle2' });
    
    const links = await page.evaluate(() => {
        const anchors = Array.from(document.querySelectorAll('a'));
        return anchors.map(a => a.href).filter(href => href.includes('/jobs/'));
    });

    const uniqueLinks = [...new Set(links)];
    console.log("Total potential job links found: " + uniqueLinks.length);

    const history = JSON.parse(fs.readFileSync('history.json', 'utf8') || '[]');
    let pending = JSON.parse(fs.readFileSync('pending_posts.json', 'utf8') || '[]');

    let newJobsFound = 0;
    for (const link of uniqueLinks) {
        if (!history.includes(link) && !pending.find(p => p.link === link)) {
            await page.goto(link, { waitUntil: 'networkidle2' });
            
            const data = await page.evaluate(() => {
                return {
                    title: document.querySelector('h1')?.innerText || document.querySelector('h2')?.innerText || "Job",
                    desc: document.querySelector('p')?.innerText.substring(0, 100) || "No desc",
                    image: document.querySelector('img')?.src
                };
            });

            pending.push({ ...data, link, timestamp: new Date().toISOString() });
            newJobsFound++;
        }
        if (newJobsFound >= 6) break;
    }

    fs.writeFileSync('pending_posts.json', JSON.stringify(pending, null, 2));
    await browser.close();
    console.log("Added " + newJobsFound + " new jobs.");
}

scrapeToQueue();
