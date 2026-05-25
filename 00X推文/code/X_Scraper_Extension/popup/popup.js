document.addEventListener('DOMContentLoaded', async () => {
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const clearBtn = document.getElementById('clearBtn');
    const countDisplay = document.getElementById('countDisplay');
    const statusBadge = document.getElementById('statusBadge');
    const hoursInput = document.getElementById('hoursInput');
    const errorMsg = document.getElementById('errorMsg');

    // Get current active tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab.url || (!tab.url.includes('x.com') && !tab.url.includes('twitter.com'))) {
        errorMsg.style.display = 'block';
        startBtn.disabled = true;
        startBtn.style.opacity = '0.5';
        return;
    }

    // Connect and poll state from content script
    async function updateState() {
        try {
            const response = await chrome.tabs.sendMessage(tab.id, { action: "GET_STATE" });
            if (response) {
                countDisplay.textContent = response.count || 0;
                if (response.isScraping) {
                    setUIStateScraping();
                } else {
                    setUIStateIdle();
                }
            }
        } catch (e) {
            // Content script not injected yet, which is fine
            setUIStateIdle();
            const { cacheCount = 0 } = await chrome.storage.local.get('cacheCount');
            countDisplay.textContent = cacheCount;
        }
    }

    // Refresh state periodically if popup is open
    setInterval(updateState, 1000);
    await updateState();

    function setUIStateScraping() {
        startBtn.style.display = 'none';
        stopBtn.style.display = 'flex';
        statusBadge.textContent = '⚡ 抓取运行中...';
        statusBadge.classList.add('active');
        hoursInput.disabled = true;
    }

    function setUIStateIdle() {
        startBtn.style.display = 'flex';
        stopBtn.style.display = 'none';
        statusBadge.textContent = '待命休眠中';
        statusBadge.classList.remove('active');
        hoursInput.disabled = false;
    }

    async function injectContentScript() {
        // Ensure content script is injected
        try {
            await chrome.scripting.executeScript({
                target: { tabId: tab.id },
                files: ['content_scripts/scraper.js']
            });
        } catch (e) {
            console.log("Script already injected or error:", e);
        }
    }

    startBtn.addEventListener('click', async () => {
        await injectContentScript();
        const limitHours = parseInt(hoursInput.value, 10) || 48;
        
        try {
            await chrome.tabs.sendMessage(tab.id, { 
                action: "START_SCRAPING",
                limitHours: limitHours
            });
            setUIStateScraping();
        } catch (e) {
            console.error("Failed to start:", e);
        }
    });

    stopBtn.addEventListener('click', async () => {
        try {
            await chrome.tabs.sendMessage(tab.id, { action: "STOP_SCRAPING" });
            setUIStateIdle();
        } catch (e) {
            console.error("Failed to stop:", e);
        }
    });

    clearBtn.addEventListener('click', async () => {
        const confirmClear = confirm("确定要清除历史抓取缓存吗？此操作不可恢复。");
        if (!confirmClear) return;

        try {
            // Clear content script cache if running
            try {
                await chrome.tabs.sendMessage(tab.id, { action: "CLEAR_CACHE" });
            } catch (e) {
                // If script not injected, clear storage directly
                await chrome.storage.local.remove(['X_tweets_cache', 'cacheCount']);
            }
            
            await chrome.storage.local.remove(['X_tweets_cache', 'cacheCount']);
            countDisplay.textContent = '0';
            setUIStateIdle();
        } catch (e) {
            console.error("Failed to clear cache:", e);
        }
    });
});
