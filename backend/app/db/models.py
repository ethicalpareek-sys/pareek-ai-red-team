from __future__ import annotations
from sqlalchemy import String, Integer, JSON, Boolean, Text, TIMESTAMP, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.db.base import Base


class Target(Base):
    __tablename__ = "targets"

    id: Mapped[PGUUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner_user_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    authorized: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    authorization_document: Mapped[str | None] = mapped_column(Text, nullable=True)
    allowed_domains: Mapped[dict] = mapped_column(JSON, default=list)
    allowed_ips: Mapped[dict] = mapped_column(JSON, default=list)
    excluded_targets: Mapped[dict] = mapped_column(JSON, default=list)
    allowed_ports: Mapped[dict] = mapped_column(JSON, default=list)
    rate_limit_per_minute: Mapped[int] = mapped_column(Integer, default=10)
    request_budget: Mapped[int] = mapped_column(Integer, default=2500)
    time_limit_minutes: Mapped[int] = mapped_column(Integer, default=240)
    safe_mode: Mapped[bool] = mapped_column(Boolean, default=True)
    prohibited_actions: Mapped[dict] = mapped_column(JSON, default=list)


class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[PGUUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    target_id: Mapped[PGUUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("targets.id"), nullable=False)
    mode: Mapped[str] = mapped_column(String(32), default="SAFE", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="PENDING", nullable=False)
    started_at: Mapped[str | None] = mapped_column(TIMESTAMP, nullable=True)
    finished_at: Mapped[str | None] = mapped_column(TIMESTAMP, nullable=True)
    request_budget_remaining: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[PGUUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    target_id: Mapped[PGUUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("targets.id"), nullable=False)
    hostname: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ip: Mapped[str | None] = mapped_column(String(64), nullable=True)
    port: Mapped[int | None] = mapped_column(Integer, nullable=True)
    protocol: Mapped[str | None] = mapped_column(String(16), nullable=True)
    technology: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    confidence: Mapped[int] = mapped_column(Integer, default=0)
    source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    discovered_at: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)


class Endpoint(Base):
    __tablename__ = "endpoints"

    id: Mapped[PGUUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    target_id: Mapped[PGUUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("targets.id"), nullable=False)
    asset_id: Mapped[PGUUID | None] = mapped_column(PGUUID(as_uuid=True), ForeignKey("assets.id"), nullable=True)
    method: Mapped[str | None] = mapped_column(String(16), nullable=True)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    parameters: Mapped[dict] = mapped_column(JSON, default=dict)
    headers: Mapped[dict] = mapped_column(JSON, default=dict)
    cookies: Mapped[dict] = mapped_column(JSON, default=dict)
    auth_state: Mapped[dict] = mapped_column(JSON, default=dict)
    content_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    response_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    size_bytes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    technology: Mapped[dict] = mapped_column(JSON, default=dict)
    discovery_source: Mapped[str | None] = mapped_column(String(255), nullable=True)


class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[PGUUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    target_id: Mapped[PGUUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("targets.id"), nullable=False)
    asset_id: Mapped[PGUUID | None] = mapped_column(PGUUID(as_uuid=True), ForeignKey("assets.id"), nullable=True)
    endpoint_id: Mapped[PGUUID | None] = mapped_column(PGUUID(as_uuid=True), ForeignKey("endpoints.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    method: Mapped[str | None] = mapped_column(String(16), nullable=True)
    category: Mapped[str | None] = mapped_column(String(128), nullable=True)
    cwe: Mapped[str | None] = mapped_column(String(64), nullable=True)
    owasp: Mapped[str | None] = mapped_column(String(128), nullable=True)
    severity: Mapped[str] = mapped_column(String(32), nullable=False)
    confidence: Mapped[int] = mapped_column(Integer, default=0)
    classification: Mapped[str] = mapped_column(String(32), default="POSSIBLE")
    evidence: Mapped[dict] = mapped_column(JSON, default=list)
    affected_component: Mapped[str | None] = mapped_column(Text, nullable=True)
    security_impact: Mapped[str | None] = mapped_column(Text, nullable=True)
    business_impact: Mapped[str | None] = mapped_column(Text, nullable=True)
    safe_validation: Mapped[str | None] = mapped_column(Text, nullable=True)
    remediation: Mapped[str | None] = mapped_column(Text, nullable=True)
    references: Mapped[dict] = mapped_column(JSON, default=list)


class AttackPath(Base):
    __tablename__ = "attack_paths"

    id: Mapped[PGUUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    target_id: Mapped[PGUUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("targets.id"), nullable=False)
    entry_point: Mapped[str | None] = mapped_column(Text, nullable=True)
    precondition: Mapped[str | None] = mapped_column(Text, nullable=True)
    observed_weakness: Mapped[str | None] = mapped_column(Text, nullable=True)
    affected_asset: Mapped[str | None] = mapped_column(Text, nullable=True)
    potential_impact: Mapped[str | None] = mapped_column(Text, nullable=True)
    evidence: Mapped[dict] = mapped_column(JSON, default=list)
    confidence: Mapped[int] = mapped_column(Integer, default=0)
    remediation: Mapped[str | None] = mapped_column(Text, nullable=True)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[PGUUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    target_id: Mapped[PGUUID | None] = mapped_column(PGUUID(as_uuid=True), ForeignKey("targets.id"), nullable=True)
    actor_user_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    event_type: Mapped[str] = mapped_column(String(128), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)
