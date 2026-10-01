// Advanced AI Agent Chat - PAREEK Pentesting Assistant

const pentestKnowledge = {
    'sql injection': {
        description: 'SQL Injection is a critical vulnerability where attacker-controlled input is concatenated into SQL queries.',
        detection: 'Look for user input in SQL queries, timing delays, error messages revealing database info.',
        remediation: 'Use parameterized queries, prepared statements, and ORM frameworks.',
        severity: 'CRITICAL',
        cwe: 'CWE-89',
        examples: ["' OR '1'='1", "1; DROP TABLE users--", "UNION SELECT NULL,NULL,NULL--"],
    },
    'xss': {
        description: 'Cross-Site Scripting (XSS) allows attackers to inject malicious scripts into web pages.',
        types: ['Reflected XSS', 'Stored XSS', 'DOM-based XSS'],
        detection: 'Test all user input fields with payloads like <img src=x onerror="alert(1)">',
        remediation: 'Output encoding, Content Security Policy, input validation',
        severity: 'HIGH',
        cwe: 'CWE-79',
    },
    'bola': {
        description: 'Broken Object Level Authorization (BOLA/IDOR) allows unauthorized access to other users\' data.',
        detection: 'Change object IDs in API requests and check if authorization is properly enforced.',
        remediation: 'Implement proper authorization checks for every resource access',
        severity: 'HIGH',
        cwe: 'CWE-639',
        examples: ['/api/users/123/profile', '/api/documents/456/download'],
    },
    'ssrf': {
        description: 'Server-Side Request Forgery allows attackers to make the server perform requests to internal systems.',
        detection: 'Test URL parameters with localhost, 127.0.0.1, internal IPs, cloud metadata URLs.',
        remediation: 'Whitelist allowed URLs, disable dangerous protocols, validate URLs server-side',
        severity: 'HIGH',
        cwe: 'CWE-918',
    },
    'file upload': {
        description: 'Unrestricted file uploads can lead to Remote Code Execution if executable files are uploaded.',
        detection: 'Try uploading PHP, JSP, ASPX files; double extensions; polyglot files.',
        remediation: 'Validate file types server-side, store outside web root, disable script execution',
        severity: 'CRITICAL',
        cwe: 'CWE-434',
    },
    'authentication': {
        description: 'Authentication weaknesses include weak password reset, session fixation, insecure token handling.',
        detection: 'Test password reset flows, session invalidation, token expiration.',
        remediation: 'Implement secure auth flows, use cryptographic tokens, enforce session regeneration',
        severity: 'HIGH',
        cwe: ['CWE-287', 'CWE-384', 'CWE-640'],
    },
    'graphql': {
        description: 'GraphQL introspection enabled can expose the entire API schema and internal structure.',
        detection: 'Send introspection query: query { __schema { types { name } } }',
        remediation: 'Disable introspection in production, add authentication to GraphQL endpoint',
        severity: 'MEDIUM',
        cwe: 'CWE-200',
    },
    'rate limiting': {
        description: 'Missing rate limiting allows brute force attacks, account enumeration, and resource exhaustion.',
        detection: 'Send rapid requests and check for rate limit headers.',
        remediation: 'Implement rate limiting, use API gateways, add CAPTCHA',
        severity: 'MEDIUM',
        cwe: 'CWE-770',
    },
    'cve': {
        description: 'Common Vulnerabilities and Exposures in dependencies and frameworks.',
        examples: ['OpenSSL vulnerabilities', 'nginx buffer overflow', 'Django authentication bypass'],
        remediation: 'Keep dependencies updated, use vulnerability scanning tools like Snyk',
    },
    'scan': {
        description: 'PAREEK AI RED TEAM performs comprehensive security assessments including OSINT, web scanning, API testing, and dependency analysis.',
        commands: [
            '/scan <url> - Start web application security scan',
            '/api-scan <api-url> - Test API security',
            '/recon <domain> - Perform reconnaissance',
            '/attack-chains - Analyze attack paths',
            '/report - Generate detailed report',
        ],
    },
};

function detectPentestIntent(message) {
    const lower = message.toLowerCase();

    for (const [key, value] of Object.entries(pentestKnowledge)) {
        if (lower.includes(key)) {
            return buildPentestResponse(key, value);
        }
    }

    if (lower.includes('scan')) return buildPentestResponse('scan', pentestKnowledge.scan);
    if (lower.includes('vulnerability')) return buildVulnerabilityResponse();
    if (lower.includes('payload')) return buildPayloadResponse(message);
    if (lower.includes('test')) return buildTestResponse(message);

    return buildDefaultResponse(message);
}

function buildPentestResponse(topic, knowledge) {
    let response = `<strong>${topic.toUpperCase()} ANALYSIS</strong><br><br>`;
    response += `<strong>Description:</strong> ${knowledge.description}<br><br>`;

    if (knowledge.detection) {
        response += `<strong>Detection:</strong> ${knowledge.detection}<br><br>`;
    }
    if (knowledge.remediation) {
        response += `<strong>Remediation:</strong> ${knowledge.remediation}<br><br>`;
    }
    if (knowledge.cwe) {
        const cwes = Array.isArray(knowledge.cwe) ? knowledge.cwe.join(', ') : knowledge.cwe;
        response += `<strong>CWE:</strong> ${cwes}<br><br>`;
    }
    if (knowledge.severity) {
        response += `<strong>Severity:</strong> <span style="color: ${getSeverityColor(knowledge.severity)}">${knowledge.severity}</span><br><br>`;
    }
    if (knowledge.examples) {
        response += `<strong>Examples:</strong><br>`;
        knowledge.examples.forEach(ex => {
            response += `• ${ex}<br>`;
        });
        response += '<br>';
    }
    if (knowledge.types) {
        response += `<strong>Types:</strong> ${knowledge.types.join(', ')}<br><br>`;
    }
    if (knowledge.commands) {
        response += `<strong>Available Commands:</strong><br>`;
        knowledge.commands.forEach(cmd => {
            response += `• ${cmd}<br>`;
        });
    }

    return response;
}

function buildVulnerabilityResponse() {
    return `<strong>VULNERABILITY CLASSES</strong><br><br>
    PAREEK detects and analyzes:<br><br>
    <strong>CRITICAL:</strong> SQL Injection, File Upload RCE, Authentication Bypass<br>
    <strong>HIGH:</strong> XSS, BOLA/IDOR, SSRF, Weak Authorization<br>
    <strong>MEDIUM:</strong> Missing Headers, GraphQL Introspection, Rate Limiting<br>
    <strong>LOW:</strong> Information Disclosure, Exposure<br><br>
    Ask me about specific vulnerabilities or run a scan to identify issues in your target.`;
}

function buildPayloadResponse(message) {
    return `<strong>⚠️ PAYLOAD INFORMATION</strong><br><br>
    PAREEK can assist with educational payload testing in authorized environments.<br><br>
    <strong>Remember:</strong><br>
    • Always have written authorization before testing<br>
    • Only test systems you own or have explicit permission to test<br>
    • Use SAFE mode by default<br>
    • Document all findings with evidence<br><br>
    What vulnerability class interests you? (SQL Injection, XSS, SSRF, BOLA, etc.)`;
}

function buildTestResponse(message) {
    return `<strong>TESTING METHODOLOGY</strong><br><br>
    PAREEK uses a structured security testing approach:<br><br>
    1. <strong>Reconnaissance:</strong> OSINT, DNS enumeration, subdomain discovery<br>
    2. <strong>Asset Mapping:</strong> Port scanning, technology detection<br>
    3. <strong>Web Security:</strong> Headers, authentication, authorization<br>
    4. <strong>Injection Testing:</strong> SQL, NoSQL, Command injection<br>
    5. <strong>XSS Analysis:</strong> Reflected, Stored, DOM-based<br>
    6. <strong>API Security:</strong> Authentication, rate limiting, schema exposure<br>
    7. <strong>Attack Chains:</strong> Correlation and impact analysis<br><br>
    Type '/scan <url>' to begin testing (authorized targets only).`;
}

function buildDefaultResponse(message) {
    return `I'm PAREEK AI, your advanced pentesting assistant. I can help you with:<br><br>
    <strong>Security Topics:</strong><br>
    • Vulnerability analysis and remediation<br>
    • Scanning techniques and tools<br>
    • Attack chain reasoning<br>
    • Compliance and best practices<br><br>
    <strong>Available Commands:</strong><br>
    • /scan <url> - Test web application<br>
    • /api-scan <url> - Test API security<br>
    • /recon <domain> - Reconnaissance<br>
    • /attack-chains - Analyze attack paths<br>
    • /vulnerabilities - List vulnerability types<br><br>
    What would you like to learn about?`;
}

function getSeverityColor(severity) {
    const colors = {
        CRITICAL: '#ff006e',
        HIGH: '#ff6b00',
        MEDIUM: '#ffbe0b',
        LOW: '#00ff88',
    };
    return colors[severity] || '#00ccff';
}

function processPentestCommand(message) {
    if (message.startsWith('/scan ')) {
        const url = message.substring(6);
        return `<strong>INITIATING WEB SCAN</strong><br>Target: ${url}<br>Mode: SAFE<br>Status: RUNNING...<br><br>Scanning for:<br>• Security headers<br>• Authentication weaknesses<br>• Authorization issues<br>• Injection vulnerabilities<br>• XSS and CSRF<br>• File upload issues<br><br>This is a demonstration. In production, actual scanning would begin.`;
    }
    if (message.startsWith('/api-scan ')) {
        const url = message.substring(10);
        return `<strong>INITIATING API SCAN</strong><br>Target: ${url}<br>Mode: SAFE<br><br>Analyzing:<br>• Authentication mechanisms<br>• Rate limiting<br>• Schema exposure<br>• Authorization enforcement<br>• Data exposure risks`;
    }
    if (message.startsWith('/recon ')) {
        const domain = message.substring(7);
        return `<strong>RECONNAISSANCE ON ${domain}</strong><br><br>Performing:<br>• DNS enumeration<br>• Subdomain discovery<br>• Port scanning<br>• Technology fingerprinting<br>• Service detection`;
    }
    if (message === '/attack-chains') {
        return `<strong>ATTACK CHAIN ANALYSIS</strong><br><br>
        Common attack chains detected:<br><br>
        <strong>Chain 1: Session Fixation → BOLA → Data Exfiltration</strong><br>
        Impact: CRITICAL | Effort: MEDIUM<br><br>
        <strong>Chain 2: File Upload → RCE → System Compromise</strong><br>
        Impact: CRITICAL | Effort: LOW<br><br>
        <strong>Chain 3: Authentication Bypass → Privilege Escalation</strong><br>
        Impact: CRITICAL | Effort: MEDIUM`;
    }
    if (message === '/report') {
        return `<strong>GENERATING SECURITY REPORT</strong><br><br>
        Report includes:<br>
        • Executive summary<br>
        • Detailed findings with evidence<br>
        • Risk scoring and prioritization<br>
        • Attack chain analysis<br>
        • Remediation roadmap<br>
        • Compliance mapping (OWASP, CWE, CVSS)<br><br>
        Report format: HTML, PDF, JSON`;
    }

    return null;
}
