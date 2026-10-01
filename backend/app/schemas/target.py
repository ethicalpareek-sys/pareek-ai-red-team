from typing import List
from pydantic import BaseModel, Field


class TargetResponse(BaseModel):
    id: str
    name: str
    authorized: bool
    safe_mode: bool
    allowed_domains: List[str] = Field(default_factory=list)
    allowed_ips: List[str] = Field(default_factory=list)
    excluded_targets: List[str] = Field(default_factory=list)
    allowed_ports: List[int] = Field(default_factory=list)
