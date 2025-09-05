// Example 1: Getting final logs (waits for all data)
async function getFinalLogs() {
    try {
        const response = await fetch("http://127.0.0.1:8000/final-logs");
        const data = await response.json();   // waits for the entire JSON body
        document.getElementById('final-logs').innerHTML = data.logs.join('<br>');
        console.log("Final response:", data);
    } catch (error) {
        console.error("Error fetching final logs:", error);
        document.getElementById('final-logs').innerHTML = 'Error fetching logs';
    }
}

// Example 2: Streaming logs (processes chunks as they arrive)
async function getStreamingLogs() {
    try {
        const response = await fetch("http://127.0.0.1:8000/stream-logs");
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        const streamingLogsElement = document.getElementById('streaming-logs');
        streamingLogsElement.innerHTML = '';

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            console.log("Received chunk:", chunk);
            streamingLogsElement.innerHTML += chunk;
        }
    } catch (error) {
        console.error("Error fetching streaming logs:", error);
        document.getElementById('streaming-logs').innerHTML = 'Error fetching streaming logs';
    }
}

// Call both examples
getFinalLogs();
getStreamingLogs();