CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS targets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    owner_user_id VARCHAR(255),
    authorized BOOLEAN NOT NULL DEFAULT FALSE,
    authorization_document TEXT,
    allowed_domains JSONB NOT NULL DEFAULT '[]'::jsonb,
    allowed_ips JSONB NOT NULL DEFAULT '[]'::jsonb,
    excluded_targets JSONB NOT NULL DEFAULT '[]'::jsonb,
    allowed_ports JSONB NOT NULL DEFAULT '[]'::jsonb,
    rate_limit_per_minute INTEGER NOT NULL DEFAULT 10,
    request_budget INTEGER NOT NULL DEFAULT 2500,
    time_limit_minutes INTEGER NOT NULL DEFAULT 240,
    safe_mode BOOLEAN NOT NULL DEFAULT TRUE,
    prohibited_actions JSONB NOT NULL DEFAULT '[]'::jsonb
);

CREATE TABLE IF NOT EXISTS assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    target_id UUID REFERENCES targets(id) ON DELETE CASCADE,
    hostname VARCHAR(255),
    ip VARCHAR(64),
    port INTEGER,
    protocol VARCHAR(16),
    technology JSONB NOT NULL DEFAULT '{}'::jsonb,
    status VARCHAR(64),
    confidence INTEGER NOT NULL DEFAULT 0,
    source VARCHAR(255),
    discovered_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS endpoints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    target_id UUID REFERENCES targets(id) ON DELETE CASCADE,
    asset_id UUID REFERENCES assets(id) ON DELETE SET NULL,
    method VARCHAR(16),
    url TEXT NOT NULL,
    parameters JSONB NOT NULL DEFAULT '{}'::jsonb,
    headers JSONB NOT NULL DEFAULT '{}'::jsonb,
    cookies JSONB NOT NULL DEFAULT '{}'::jsonb,
    auth_state JSONB NOT NULL DEFAULT '{}'::jsonb,
    content_type VARCHAR(255),
    response_type VARCHAR(255),
    status_code INTEGER,
    size_bytes INTEGER,
    technology JSONB NOT NULL DEFAULT '{}'::jsonb,
    discovery_source VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS findings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    target_id UUID REFERENCES targets(id) ON DELETE CASCADE,
    asset_id UUID REFERENCES assets(id) ON DELETE SET NULL,
    endpoint_id UUID REFERENCES endpoints(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    method VARCHAR(16),
    category VARCHAR(128),
    cwe VARCHAR(64),
    owasp VARCHAR(128),
    severity VARCHAR(32) NOT NULL,
    confidence INTEGER NOT NULL DEFAULT 0,
    classification VARCHAR(32) NOT NULL DEFAULT 'POSSIBLE',
    evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
    affected_component TEXT,
    security_impact TEXT,
    business_impact TEXT,
    safe_validation TEXT,
    remediation TEXT,
    references JSONB NOT NULL DEFAULT '[]'::jsonb,
    first_seen TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS attack_paths (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    target_id UUID REFERENCES targets(id) ON DELETE CASCADE,
    entry_point TEXT,
    precondition TEXT,
    observed_weakness TEXT,
    affected_asset TEXT,
    potential_impact TEXT,
    evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
    confidence INTEGER NOT NULL DEFAULT 0,
    remediation TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS scans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    target_id UUID REFERENCES targets(id) ON DELETE CASCADE,
    mode VARCHAR(32) NOT NULL DEFAULT 'SAFE',
    status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,
    request_budget_remaining INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    target_id UUID REFERENCES targets(id) ON DELETE CASCADE,
    actor_user_id VARCHAR(255),
    event_type VARCHAR(128) NOT NULL,
    message TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_targets_authorized ON targets (authorized);
CREATE INDEX IF NOT EXISTS idx_assets_target_id ON assets (target_id);
CREATE INDEX IF NOT EXISTS idx_endpoints_target_id ON endpoints (target_id);
CREATE INDEX IF NOT EXISTS idx_findings_target_id ON findings (target_id);
CREATE INDEX IF NOT EXISTS idx_audit_target_id ON audit_logs (target_id);
