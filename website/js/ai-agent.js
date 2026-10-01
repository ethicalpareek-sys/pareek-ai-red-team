const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');

const knowledgeBase = {
    "pareek": "PAREEK AI RED TEAM is an AI-assisted cyber security assessment platform built for authorized security research, web app analysis, API testing, asset discovery, and evidence-based vulnerability review.",
    "security": "PAREEK enforces scope control, allowlists, rate limits, request budgets, and audit logging before active testing. It is designed for authorized targets only.",
    "termux": "Termux can be used for lightweight local automation and authorized lab work, but full production-class scanning is better on Linux or a cloud-hosted environment with Docker and PostgreSQL.",
    "dashboard": "The dashboard shows asset discovery, endpoint inventory, findings, attack paths, scan status, and technology intelligence.",
    "api": "PAREEK analyzes HTTP, REST, GraphQL, and WebSocket APIs for authorization gaps, data exposure, authentication issues, and schema problems.",
    "scan": "The platform supports SAFE, STANDARD, DEEP, API, AUTHENTICATED, and FULL ASSESSMENT modes, with SAFE as the default.",
    "default": "PAREEK AI RED TEAM focuses on authorized security research, evidence-based findings, and safe workflow enforcement. Ask about discovery, scan modes, API security, or architecture."
};

function addMessage(text, type = 'agent') {
    const msg = document.createElement('div');
    msg.className = `message ${type}`;
    msg.innerHTML = text;
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function detectIntent(message) {
    const lower = message.toLowerCase();

    if (lower.includes('termux')) return knowledgeBase.termux;
    if (lower.includes('api')) return knowledgeBase.api;
    if (lower.includes('dashboard')) return knowledgeBase.dashboard;
    if (lower.includes('scan')) return knowledgeBase.scan;
    if (lower.includes('security')) return knowledgeBase.security;
    if (lower.includes('pareek')) return knowledgeBase.pareek;
    return knowledgeBase.default;
}

function buildReply(message) {
    const intent = detectIntent(message);
    return `"${message}"<br><br>${intent}`;
}

function sendChatMessage() {
    const message = chatInput.value.trim();
    if (!message) return;

    addMessage(`<strong>You:</strong> ${message}`, 'user');
    chatInput.value = '';

    const thinking = document.createElement('div');
    thinking.className = 'message agent';
    thinking.innerHTML = '<strong>PAREEK Agent:</strong> <span class="loading-dot">●</span> <span class="loading-dot">●</span> <span class="loading-dot">●</span>';
    chatMessages.appendChild(thinking);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    setTimeout(() => {
        thinking.remove();
        addMessage(`<strong>PAREEK Agent:</strong> ${buildReply(message)}`, 'agent');
    }, 700);
}

function handleChatKeypress(event) {
    if (event.key === 'Enter') {
        sendChatMessage();
    }
}

function toggleChat() {
    const chat = document.querySelector('.chat-container');
    const btn = document.querySelector('.chat-toggle-btn');
    if (chat.style.display === 'none') {
        chat.style.display = 'flex';
        btn.textContent = '−';
    } else {
        chat.style.display = 'none';
        btn.textContent = '+';
    }
}
