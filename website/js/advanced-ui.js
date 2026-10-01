// Enhanced UI Integration for Advanced Pentesting

class AdvancedChatUI {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.chatInput = document.getElementById('chatInput');
        this.scanActive = false;
    }

    addMessage(text, type = 'agent') {
        const msg = document.createElement('div');
        msg.className = `message ${type}`;
        msg.innerHTML = text;
        this.chatMessages.appendChild(msg);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    async sendPentestMessage() {
        const message = this.chatInput.value.trim();
        if (!message) return;

        this.addMessage(`<strong>You:</strong> ${message}`, 'user');
        this.chatInput.value = '';

        const thinking = document.createElement('div');
        thinking.className = 'message agent';
        thinking.innerHTML = '<strong>PAREEK Agent:</strong> <span class="loading-dot">●</span> <span class="loading-dot">●</span> <span class="loading-dot">●</span>';
        this.chatMessages.appendChild(thinking);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;

        setTimeout(() => {
            thinking.remove();
            let response = '';

            // Check for pentesting commands
            const cmdResponse = processPentestCommand(message);
            if (cmdResponse) {
                response = `<strong>PAREEK Agent:</strong> ${cmdResponse}`;
            } else {
                // Use pentesting knowledge base
                response = `<strong>PAREEK Agent:</strong> ${detectPentestIntent(message)}`;
            }

            this.addMessage(response, 'agent');
        }, 700);
    }

    displayScanResults(results) {
        const html = `
            <strong>📊 SCAN RESULTS</strong><br>
            Total Findings: ${results.findings.length}<br>
            Critical: <span style="color: #ff006e;">${results.summary.critical}</span> | 
            High: <span style="color: #ff6b00;">${results.summary.high}</span> | 
            Medium: <span style="color: #ffbe0b;">${results.summary.medium}</span><br>
            Risk Score: <span style="color: #00ff88;">${results.summary.risk_score}/100</span><br>
            Attack Chains: ${results.summary.attack_chains}
        `;
        this.addMessage(html, 'agent');
    }
}

const chatUI = new AdvancedChatUI();

function handleAdvancedChatKeypress(event) {
    if (event.key === 'Enter') {
        chatUI.sendPentestMessage();
    }
}

function sendAdvancedMessage() {
    chatUI.sendPentestMessage();
}
