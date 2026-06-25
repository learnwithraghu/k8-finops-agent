"""Pydantic models for the MCP-powered FinOps agent."""

from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class ResourceSnapshot(BaseModel):
    """Raw Kubernetes resource facts collected through MCP."""

    kind: str
    namespace: str
    name: str
    labels: Dict[str, str] = Field(default_factory=dict)
    annotations: Dict[str, str] = Field(default_factory=dict)
    owners: List[str] = Field(default_factory=list)

    replicas: Optional[int] = None
    cpu_request_m: int = 0
    memory_request_mi: int = 0

    phase: Optional[str] = None
    node_name: Optional[str] = None
    restart_count: Optional[int] = None

    service_type: Optional[str] = None
    selector: Dict[str, str] = Field(default_factory=dict)

    pvc_size_gi: Optional[float] = None
    is_bound: Optional[bool] = None
    is_mounted: Optional[bool] = None
    mounted_by: List[str] = Field(default_factory=list)

    configmap_keys: List[str] = Field(default_factory=list)
    pvc_names: List[str] = Field(default_factory=list)


class ClusterSnapshot(BaseModel):
    """A complete raw snapshot of the cluster."""

    scanned_at: str
    cluster: str
    namespaces: List[str] = Field(default_factory=list)
    resources: List[ResourceSnapshot] = Field(default_factory=list)


class ResourceAssessment(BaseModel):
    """LLM-produced compliance assessment for one resource."""

    kind: str
    namespace: str
    name: str
    is_compliant: bool
    missing_tags: List[str] = Field(default_factory=list)
    category: Literal["tagged", "unallocated", "unowned", "orphaned", "unknown"]
    priority: Literal["critical", "high", "medium", "low"]
    reason: str
    suggested_cost_center: str = ""
    suggested_owner: str = ""
    suggested_tags: Dict[str, str] = Field(default_factory=dict)


class ComplianceReport(BaseModel):
    """Structured report derived from a raw cluster snapshot."""

    scanned_at: str
    cluster: str
    total_resources: int
    compliant_count: int
    violation_count: int
    assessments: List[ResourceAssessment] = Field(default_factory=list)


class AnalysisEnvelope(BaseModel):
    """Bundle passed from the analyst to the tracker step."""

    snapshot: ClusterSnapshot
    report: ComplianceReport
