chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "DOWNLOAD") {
        const { payload, filename } = message;
        
        // Convert text payload to Data URL
        // Using encodeURIComponent to safely encode text data
        const dataUrl = `data:text/plain;charset=utf-8,${encodeURIComponent(payload)}`;

        // Trigger the download via the extension API
        chrome.downloads.download({
            url: dataUrl,
            filename: filename,
            conflictAction: 'uniquify'
        }, (downloadId) => {
            if (chrome.runtime.lastError) {
                console.error("Download failed:", chrome.runtime.lastError);
                sendResponse({ success: false, error: chrome.runtime.lastError.message });
            } else {
                console.log(`Successfully triggered download with ID: ${downloadId}`);
                sendResponse({ success: true, downloadId });
            }
        });

        return true; // Keep the message channel open for the async response
    }
});
