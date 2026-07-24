const puppeteer = require('puppeteer');
const fs = require('fs');

async function scrape() {
    const browser = await puppeteer.launch({ 
        args: ['--no-sandbox', '--disable-setuid-sandbox'] 
    });
    const page = await browser.newPage();
    
    await page.goto('https://zunexhire.com/', { 
        waitUntil: 'domcontentloaded', 
        timeout: 60000 
    });

    await new Promise(r => setTimeout(r, 3000));

    const jobLinks = await page.evaluate(() => {
        const items = Array.from(document.querySelectorAll('a'));
        return [...new Set(items.filter(a => a.href.includes('/jobs/')).map(a => a.href))];
    });

    const history = fs.existsSync('history.json') && fs.readFileSync('history.json', 'utf8').trim() 
        ? JSON.parse(fs.readFileSync('history.json', 'utf8')) 
        : [];

    let pending = fs.existsSync('pending_posts.json') && fs.readFileSync('pending_posts.json', 'utf8').trim() 
        ? JSON.parse(fs.readFileSync('pending_posts.json', 'utf8')) 
        : [];

    for (const link of jobLinks) {
        if (!history.includes(link) && !pending.find(p => p.link === link)) {
            const jobPage = await browser.newPage();
            try {
                await jobPage.goto(link, { waitUntil: 'domcontentloaded', timeout: 30000 });
                await new Promise(r => setTimeout(r, 2000));

                const jobData = await jobPage.evaluate(() => {
                    const titleElement = document.querySelector('h1') || document.querySelector('title');
                    const descElement = document.querySelector('meta[name="description"]') || document.querySelector('p');
                    
                    // تصویر کا لنک ڈھونڈنے کے لیے (پہلے og:image، پھر فیچرڈ امیج یا پہلی بڑی تصویر)
                    const ogImage = document.querySelector('meta[property="og:image"]');
                    const imgElement = document.querySelector('.job-banner img') || document.querySelector('article img') || document.querySelector('img');
                    
                    let imageUrl = '';
                    if (ogImage && ogImage.content) {
                        imageUrl = ogImage.content;
                    } else if (imgElement && imgElement.src) {
                        imageUrl = imgElement.src;
                    }

                    return {
                        title: titleElement ? titleElement.innerText || titleElement.content || 'ZunexHire Job' : 'ZunexHire Job',
                        description: descElement ? descElement.innerText || descElement.content || 'Explore verified professional opportunity at ZunexHire.' : 'Explore verified professional opportunity at ZunexHire.',
                        image: imageUrl
                    };
                });

                pending.push({
                    title: jobData.title.trim(),
                    description: jobData.description.trim(),
                    image: jobData.image,
                    link: link,
                    timestamp: new Date().toISOString()
                });

                if (pending.length >= 7) {
                    await jobPage.close();
                    break;
                }
            } catch (err) {
                console.log(`Error scraping ${link}:`, err.message);
            }
            await jobPage.close();
        }
    }

    fs.writeFileSync('pending_posts.json', JSON.stringify(pending, null, 2));
    await browser.close();
}

scrape();
