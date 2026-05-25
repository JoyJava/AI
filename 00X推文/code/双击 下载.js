(() => {
    console.log("🚀 保险版抓取脚本已启动！");
    console.log("💡 提示：当你想下载时，在网页任意空白处【双击鼠标左键】。它不会弹窗下载，而是会将所有文本排好版打印在下方，你直接复制即可！");

    const allScrapedTweets = new Set();

    // 1. 自动循环滚动
    const scrollAndScrape = setInterval(() => {
        const tweetNodes = document.querySelectorAll('div[data-testid="tweetText"]');
        tweetNodes.forEach(node => {
            const text = node.innerText.trim();
            if (text) allScrapedTweets.add(text);
        });
        console.log(`[当前进度] 已抓取独立推文: ${allScrapedTweets.size} 条 (继续滚动中...)`);
        window.scrollBy(0, window.innerHeight * 0.8);
    }, 1500);

    // 2. 双击页面空白处，直接在控制台吐出全部文本
    document.addEventListener('dblclick', function windowDoubleClickHandler() {
        clearInterval(scrollAndScrape);
        document.removeEventListener('dblclick', windowDoubleClickHandler);

        console.clear();
        console.log("%c🏁 抓取已停止！请复制下方框内的所有文本：", "color: #00ba7c; font-weight: bold; font-size: 14px;");
        console.log("==================================================================");

        // 将 Set 转换为排版好的字符串
        const textResult = Array.from(allScrapedTweets)
            .map((text, i) => `[推文 ${i + 1}]\n${text}`)
            .join('\n\n========================================\n\n');

        console.log(textResult);

        console.log("==================================================================");
        console.log("%c💡 复制方法：用鼠标全选上面的推文内容，按 Ctrl+C (Mac用 Cmd+C) 复制，然后在电脑上新建一个 txt 文件粘贴进去保存即可！", "color: #1d9bf0; font-weight: bold;");
    });
})();