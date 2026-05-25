// State
let isScraping = false;
let scrollTimer = null;
let allScrapedTweets = new Map();
let limitTimeMs = 0;
let consecutiveOutCount = 0;
let totalScrolls = 0;
let lastDownloadCount = 0;
const STORAGE_KEY = 'X_tweets_cache';

// Load from chrome.storage on init
chrome.storage.local.get([STORAGE_KEY, 'cacheCount']).then((res) => {
    if (res[STORAGE_KEY]) {
        const parsed = JSON.parse(res[STORAGE_KEY]);
        parsed.forEach(item => {
            allScrapedTweets.set(item.key, item.value);
        });
        lastDownloadCount = Math.floor(allScrapedTweets.size / 200) * 200;
        console.log(`♻️ [X Scraper] 成功从缓存恢复了 ${allScrapedTweets.size} 条历史推文。`);
    }
});

async function saveToCache() {
    try {
        const arr = Array.from(allScrapedTweets.entries()).map(([key, value]) => ({ key, value }));
        await chrome.storage.local.set({ 
            [STORAGE_KEY]: JSON.stringify(arr),
            cacheCount: allScrapedTweets.size 
        });
    } catch (e) {
        console.error("写入缓存失败:", e);
    }
}

function getFormattedDate() {
    const d = new Date();
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

async function saveToFile(isBackup = false) {
    const tweetsArray = Array.from(allScrapedTweets.values())
        .sort((a, b) => b.timestamp - a.timestamp); // 按时间从新到旧排序

    if (tweetsArray.length === 0) {
        console.log("⚠️ 没有有效推文，取消下载。");
        return;
    }

    const fileContent = tweetsArray.map((tweet, i) => {
        return `[推文 ${i + 1}]\n发言人: ${tweet.user}\n时间: ${tweet.time}\n推文: ${tweet.text}`;
    }).join('\n\n========================================\n\n');

    const dateStr = getFormattedDate();
    const filename = isBackup
        ? `X_Tweets_48h_${dateStr}_backup_${tweetsArray.length}条.txt`
        : `X_Tweets_48h_${dateStr}.txt`;

    // 委托给 Background 下载
    chrome.runtime.sendMessage({
        action: "DOWNLOAD",
        payload: fileContent,
        filename: filename
    }, (response) => {
        if (response && response.success) {
            console.log(`✅ 已成功触发下载：${filename}`);
        } else {
            console.error("❌ 下载失败：", response?.error);
        }
    });
}

async function scrape() {
    if (!isScraping) return;

    const tweetArticles = document.querySelectorAll('article[data-testid="tweet"]');
    let newAddedThisRound = 0;
    let expiredThisRound = 0;
    let oldestTimeInRound = null;

    tweetArticles.forEach(article => {
        const userNameNode = article.querySelector('div[data-testid="User-Name"]');
        const timeNode = userNameNode ? (userNameNode.querySelector('time') || article.querySelector('time')) : article.querySelector('time');
        const textNodes = article.querySelectorAll('div[data-testid="tweetText"]');
        if (textNodes.length === 0) return;

        let text = textNodes[0].innerText.trim();
        if (textNodes.length > 1) {
            for (let i = 1; i < textNodes.length; i++) {
                const quoteText = textNodes[i].innerText.trim();
                if (quoteText) {
                    text += `\n\n[📌 引用旧内容]：\n${quoteText}`;
                }
            }
        }
        
        const user = userNameNode ? userNameNode.innerText.replace(/\n/g, ' ') : '未知用户';
        const timeStr = timeNode ? (timeNode.getAttribute('datetime') || timeNode.innerText) : null;

        if (!timeStr) return;

        const timestamp = new Date(timeStr).getTime();
        if (isNaN(timestamp)) return;

        const uniqueKey = `${user}_${timeStr}_${text.slice(0, 50)}`;

        if (timestamp >= limitTimeMs) {
            if (!allScrapedTweets.has(uniqueKey)) {
                allScrapedTweets.set(uniqueKey, { user, time: timeStr, text, timestamp });
                newAddedThisRound++;
            }
        } else {
            expiredThisRound++;
            if (!oldestTimeInRound || timestamp < oldestTimeInRound) {
                oldestTimeInRound = timestamp;
            }
        }
    });

    totalScrolls++;

    if (newAddedThisRound > 0) {
        await saveToCache();
        const currentCount = allScrapedTweets.size;
        if (currentCount >= lastDownloadCount + 200) {
            lastDownloadCount = Math.floor(currentCount / 200) * 200;
            console.log(`📥 已累计抓取 ${currentCount} 条推文，触发阶段性自动备份下载...`);
            saveToFile(true);
        }
    }

    // 智能停止逻辑
    if (expiredThisRound > 0 && newAddedThisRound === 0) {
        consecutiveOutCount++;
        console.log(`⏳ 连续 ${consecutiveOutCount}/5 次未发现新推文，且页面已触及过期推文区间...`);
        if (consecutiveOutCount >= 5) {
            console.log("🎯 已触及时间边界！自动停止抓取并导出文件...");
            stopScraping();
            return;
        }
    } else {
        if (newAddedThisRound > 0) {
            consecutiveOutCount = 0;
        }
    }

    // 自动向下滚动
    window.scrollBy({ top: window.innerHeight * 0.9, behavior: 'smooth' });
}

function startScraping(limitHours) {
    if (isScraping) return;
    
    console.log(`🚀 [X Scraper] 启动抓取！目标时间范围：最近 ${limitHours} 小时`);
    limitTimeMs = Date.now() - (limitHours * 60 * 60 * 1000);
    isScraping = true;
    consecutiveOutCount = 0;
    totalScrolls = 0;
    
    // 快速轮询滚动
    scrollTimer = setInterval(scrape, 800); // 适度放缓避免加载不出来
}

async function stopScraping() {
    if (!isScraping) return;
    isScraping = false;
    
    if (scrollTimer) {
        clearInterval(scrollTimer);
        scrollTimer = null;
    }
    
    console.log(`🛑 [X Scraper] 抓取停止！保存导出中...`);
    await saveToFile(false);
    
    // 自动清理缓存为下一次做准备
    allScrapedTweets.clear();
    lastDownloadCount = 0;
    await chrome.storage.local.remove([STORAGE_KEY, 'cacheCount']);
}

// 监听 Popup 消息
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "GET_STATE") {
        sendResponse({ isScraping, count: allScrapedTweets.size });
    } else if (message.action === "START_SCRAPING") {
        startScraping(message.limitHours || 48);
        sendResponse({ success: true });
    } else if (message.action === "STOP_SCRAPING") {
        stopScraping();
        sendResponse({ success: true });
    } else if (message.action === "CLEAR_CACHE") {
        allScrapedTweets.clear();
        lastDownloadCount = 0;
        chrome.storage.local.remove([STORAGE_KEY, 'cacheCount']).then(() => {
            sendResponse({ success: true });
        });
        return true;
    }
});
