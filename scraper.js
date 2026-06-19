const puppeteer = require('puppeteer');
const fs = require('fs');

async function scrape() {
    const browser = await puppeteer.launch({ 
        args: ['--no-sandbox', '--disable-setuid-sandbox'] 
    });
    const page = await browser.newPage();
    
    // تبدیلی: networkidle2 ہٹا دیا، domcontentloaded لگا دیا
    await page.goto('https://nuxas-aztr.vercel.app/', { 
        waitUntil: 'domcontentloaded', 
        timeout: 60000 
    });

    // تھوڑا سا انتظار تاکہ جاوا اسکرپٹ رینڈر ہو جائے
    await new Promise(r => setTimeout(r, 3000));

    const jobs = await page.evaluate(() => {
        const items = Array.from(document.querySelectorAll('a'));
        return items.filter(a => a.href.includes('/jobs/')).map(a => ({
            link: a.href,
            title: a.innerText || 'Job Post'
        }));
    });

    const history = JSON.parse(fs.readFileSync('history.json', 'utf8') || '[]');
    let pending = JSON.parse(fs.readFileSync('pending_posts.json', 'utf8') || '[]');

    for (const job of jobs) {
        if (!history.includes(job.link) && !pending.find(p => p.link === job.link)) {
            pending.push({
                title: job.title,
                link: job.link,
                timestamp: new Date().toISOString()
            });
            if (pending.length >= 7) break;
        }
    }

    fs.writeFileSync('pending_posts.json', JSON.stringify(pending, null, 2));
    await browser.close();
}
scrape();
