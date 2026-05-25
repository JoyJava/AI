// clearTweetsCache() //断点续传
(() => {
    console.clear();
    console.log("%c🚀 X(Twitter) 48小时推文全自动智能抓取脚本（断点续传版）已启动！", "color: #00bcd4; font-size: 16px; font-weight: bold;");

    // 1. 时间参数设置
    const NOW = Date.now();
    const LIMIT_HOURS = 48;
    const TIME_LIMIT_MS = LIMIT_HOURS * 60 * 60 * 1000;
    const LIMIT_TIME = NOW - TIME_LIMIT_MS;

    const limitDate = new Date(LIMIT_TIME);
    console.log(`%c📅 目标时间窗口：最近 ${LIMIT_HOURS} 小时`, "color: #4caf50; font-weight: bold;");
    console.log(`⏱️ 抓取终点时间（48小时前）：${limitDate.toLocaleString()}`);
    console.log("%c💡 提示：脚本会自动滚动并抓取。已支持本地缓存，若中途断开，重新运行脚本可自动读取历史数据继续抓取！", "color: #ff9800;");
    console.log("%c💡 提示：每隔 200 条会自动触发一次备份下载。页面任意空白处【双击鼠标左键】可随时提前结束并保存。", "color: #ff9800;");
    console.log("%c💡 清缓存指令：如需清空历史缓存重新开始，可在控制台输入 clearTweetsCache() 并回车。", "color: #ff9800;");

    const allScrapedTweets = new Map(); // 使用 Map 去重，Key 为唯一标识，Value 为推文对象
    const STORAGE_KEY = 'X_tweets_cache';

    // 2. 本地缓存与恢复机制
    try {
        const cached = localStorage.getItem(STORAGE_KEY);
        if (cached) {
            const parsed = JSON.parse(cached);
            parsed.forEach(item => {
                allScrapedTweets.set(item.key, item.value);
            });
            console.log(`%c♻️ 成功从本地缓存恢复了 ${allScrapedTweets.size} 条历史抓取记录！继续抓取将在其基础上累加。`, "color: #e91e63; font-weight: bold;");
        }
    } catch (e) {
        console.error("加载缓存失败:", e);
    }

    let consecutiveOutCount = 0; // 连续检测到过期推文的计数，用于智能自动停止
    let scrollTimer = null;
    let totalScrolls = 0;
    // 记录上一次下载时的条数（按200向下取整），用于触发每200条自动下载
    let lastDownloadCount = Math.floor(allScrapedTweets.size / 200) * 200;

    // 缓存同步函数
    function saveToCache() {
        try {
            const arr = Array.from(allScrapedTweets.entries()).map(([key, value]) => ({ key, value }));
            localStorage.setItem(STORAGE_KEY, JSON.stringify(arr));
        } catch (e) {
            console.error("写入缓存失败:", e);
        }
    }

    // 提供全局重置函数
    window.clearTweetsCache = () => {
        localStorage.removeItem(STORAGE_KEY);
        allScrapedTweets.clear();
        lastDownloadCount = 0;
        console.log("%c🧹 历史缓存已清除！再次运行脚本将从零开始。", "color: #ff5722; font-weight: bold;");
    };

    // 格式化输出文件名
    function getFormattedDate() {
        const d = new Date();
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    // 3. 核心文件生成与下载函数
    function saveToFile(isBackup = false) {
        const tweetsArray = Array.from(allScrapedTweets.values())
            .sort((a, b) => b.timestamp - a.timestamp); // 按时间从新到旧排序

        if (tweetsArray.length === 0) {
            console.log("%c⚠️ 没有有效推文，取消下载。", "color: #f44336; font-weight: bold;");
            return;
        }

        const fileContent = tweetsArray.map((tweet, i) => {
            return `[推文 ${i + 1}]\n发言人: ${tweet.user}\n时间: ${tweet.time}\n推文: ${tweet.text}`;
        }).join('\n\n========================================\n\n');

        const blob = new Blob([fileContent], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        const dateStr = getFormattedDate();
        a.download = isBackup
            ? `X_Tweets_48h_${dateStr}_backup_${tweetsArray.length}条.txt`
            : `X_Tweets_48h_${dateStr}.txt`;

        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        const textType = isBackup ? "阶段备份" : "正式导出";
        console.log(`%c💾 已成功自动生成${textType}文件：${a.download}（共计 ${tweetsArray.length} 条推文）`, "color: #4caf50; font-size: 14px; font-weight: bold;");
    }

    // 4. 智能抓取逻辑
    function scrape() {
        const tweetArticles = document.querySelectorAll('article[data-testid="tweet"]');
        let newAddedThisRound = 0;
        let expiredThisRound = 0;
        let oldestTimeInRound = null;

        tweetArticles.forEach(article => {
            const userNameNode = article.querySelector('div[data-testid="User-Name"]');
            // 优先取最上方发言人区域 of time 节点，确保引用的老推文时间不会干扰主推文的新时间判定
            const timeNode = userNameNode ? (userNameNode.querySelector('time') || article.querySelector('time')) : article.querySelector('time');
            // 获取当前 article 内部所有的推文文本（主推文 + 被引用的推文）
            const textNodes = article.querySelectorAll('div[data-testid="tweetText"]');
            if (textNodes.length === 0) return;

            let text = textNodes[0].innerText.trim();
            // 如果存在引用的旧推文内容，一并拼接存下来供后续分析使用
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

            // 构造去重唯一 Key
            const uniqueKey = `${user}_${timeStr}_${text.slice(0, 50)}`;

            // 判断是否是 48 小时内的推文
            if (timestamp >= LIMIT_TIME) {
                if (!allScrapedTweets.has(uniqueKey)) {
                    allScrapedTweets.set(uniqueKey, { user, time: timeStr, text, timestamp });
                    newAddedThisRound++;
                }
            } else {
                // 属于 48 小时之前的过期推文
                expiredThisRound++;
                if (!oldestTimeInRound || timestamp < oldestTimeInRound) {
                    oldestTimeInRound = timestamp;
                }
            }
        });

        totalScrolls++;

        // 打印本轮滚动状态
        const oldestDateStr = oldestTimeInRound ? new Date(oldestTimeInRound).toLocaleString() : '无';
        console.log(
            `%c[滚动 #${totalScrolls}] %c当前已累计有效推文: ${allScrapedTweets.size} 条 %c| 本轮新增: ${newAddedThisRound} %c| 本轮发现已过期: ${expiredThisRound} (最旧: ${oldestDateStr})`,
            "color: #888;",
            "color: #00bcd4; font-weight: bold;",
            "color: #4caf50;",
            "color: #ff5722;"
        );

        // 如果有新增推文，同步更新本地缓存，并检查是否触发 200 条的自动下载备份
        if (newAddedThisRound > 0) {
            saveToCache();

            const currentCount = allScrapedTweets.size;
            if (currentCount >= lastDownloadCount + 200) {
                lastDownloadCount = Math.floor(currentCount / 200) * 200;
                console.log(`%c📥 已累计抓取 ${currentCount} 条推文，触发阶段性自动备份下载...`, "color: #9c27b0; font-weight: bold;");
                saveToFile(true);
            }
        }

        // 5. 智能停止逻辑
        // 如果连续多次滚动中，页面上出现了过期推文，且没有新的有效推文增加，说明我们已经把 48 小时内的数据抓完了。
        if (expiredThisRound > 0 && newAddedThisRound === 0) {
            consecutiveOutCount++;
            console.log(`%c⏳ 连续 ${consecutiveOutCount}/5 次未发现新的 48 小时内推文，且页面已触及过期推文区间...`, "color: #ff9800;");
            if (consecutiveOutCount >= 5) {
                console.log("%c🎯 已完全抓取到 48 小时的时间边界！正在自动结束并保存文件...", "color: #4caf50; font-size: 14px; font-weight: bold;");
                stopScraping();
                return;
            }
        } else {
            // 如果抓到了新推文，重置计数器
            if (newAddedThisRound > 0) {
                consecutiveOutCount = 0;
            }
        }

        // 6. 自动向下滚动
        window.scrollBy(0, window.innerHeight * 0.9);
    }

    // 启动滚动循环（每 200 毫秒执行一次，快速滚动）
    scrollTimer = setInterval(scrape, 200);

    // 停止抓取并收尾
    function stopScraping() {
        if (scrollTimer) {
            clearInterval(scrollTimer);
            scrollTimer = null;
        }
        saveToFile();

        // 抓取圆满结束后，自动清除本地缓存，以便下一次开始新任务
        localStorage.removeItem(STORAGE_KEY);
        document.removeEventListener('dblclick', manualStopHandler);
        console.log("%c🏁 抓取任务圆满结束！本地临时缓存已清理。", "color: #00bcd4; font-weight: bold;");
    }

    // 双击页面空白处手动结束
    function manualStopHandler() {
        console.log("%c🛑 用户双击页面，手动终止抓取并保存！", "color: #f44336; font-weight: bold;");
        stopScraping();
    }
    document.addEventListener('dblclick', manualStopHandler);

})();