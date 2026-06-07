import streamlit as st
import random
import time
from datetime import datetime, timedelta


def init_game_state():
    """Initialize all session state variables for the game."""
    if "game_started" not in st.session_state:
        st.session_state.game_started = False
    if "current_act" not in st.session_state:
        st.session_state.current_act = 0
    if "current_scene" not in st.session_state:
        st.session_state.current_scene = 0
    if "mttr_minutes" not in st.session_state:
        st.session_state.mttr_minutes = 0
    if "revenue_lost" not in st.session_state:
        st.session_state.revenue_lost = 0
    if "teams_contacted" not in st.session_state:
        st.session_state.teams_contacted = []
    if "labels_found" not in st.session_state:
        st.session_state.labels_found = []
    if "escalation_level" not in st.session_state:
        st.session_state.escalation_level = 0
    if "incident_resolved" not in st.session_state:
        st.session_state.incident_resolved = False
    if "finops_enabled" not in st.session_state:
        st.session_state.finops_enabled = False
    if "minigames_completed" not in st.session_state:
        st.session_state.minigames_completed = {
            "label_detective": False,
            "cost_allocation": False,
            "escalation_ladder": False,
        }
    if "player_score" not in st.session_state:
        st.session_state.player_score = 0


def reset_game():
    """Reset all game state to start fresh."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_game_state()


def advance_scene():
    """Advance to the next scene within the current act."""
    st.session_state.current_scene += 1


def advance_act():
    """Advance to the next act and reset scene counter."""
    st.session_state.current_act += 1
    st.session_state.current_scene = 0


def add_mttr(minutes):
    """Add time to the MTTR counter and calculate revenue impact."""
    st.session_state.mttr_minutes += minutes
    # Rough calculation: $500/minute of downtime for a payment service
    st.session_state.revenue_lost = st.session_state.mttr_minutes * 500


def get_mttr_display():
    """Format MTTR as hours:minutes."""
    hours = st.session_state.mttr_minutes // 60
    minutes = st.session_state.mttr_minutes % 60
    return f"{hours}h {minutes}m"


def get_revenue_display():
    """Format revenue lost with dollar sign and commas."""
    return f"${st.session_state.revenue_lost:,}"


# Mock data for the game
BROKEN_SERVICES = [
    {
        "name": "payment-api",
        "namespace": "team-a-prod",
        "error_rate": "98.5%",
        "latency": "45s",
        "owner_label": "unknown",
        "cost_center": "legacy",
        "actual_owner": "team-payments",
        "severity": "critical",
    },
    {
        "name": "user-auth",
        "namespace": "team-b-staging",
        "error_rate": "87.2%",
        "latency": "12s",
        "owner_label": "tbd",
        "cost_center": "platform",
        "actual_owner": "team-security",
        "severity": "high",
    },
    {
        "name": "inventory-svc",
        "namespace": "team-c-prod",
        "error_rate": "45.1%",
        "latency": "8s",
        "owner_label": "team-legacy (deprecated)",
        "cost_center": "operations",
        "actual_owner": "team-fulfillment",
        "severity": "medium",
    },
]

TEAMS = [
    {
        "name": "team-platform",
        "slack": "#platform-oncall",
        "owns": ["ingress-controller", "monitoring"],
    },
    {"name": "team-backend", "slack": "#backend-ops", "owns": ["api-gateway", "cache-layer"]},
    {"name": "team-frontend", "slack": "#frontend-alerts", "owns": ["web-app", "cdn"]},
    {"name": "team-data", "slack": "#data-pipelines", "owns": ["etl-jobs", "warehouse"]},
    {"name": "team-security", "slack": "#security-ops", "owns": ["user-auth", "secrets-manager"]},
    {"name": "team-payments", "slack": "#payments-oncall", "owns": ["payment-api", "billing"]},
    {
        "name": "team-fulfillment",
        "slack": "#fulfillment-ops",
        "owns": ["inventory-svc", "shipping"],
    },
]

ORG_CHART = {
    "CTO": {"reports": ["VP Engineering", "VP Infrastructure", "VP Product"], "knows_about": []},
    "VP Engineering": {
        "reports": ["Director Backend", "Director Frontend"],
        "knows_about": ["team-backend", "team-frontend"],
    },
    "VP Infrastructure": {
        "reports": ["Director Platform", "Director SRE"],
        "knows_about": ["team-platform", "team-data"],
    },
    "VP Product": {
        "reports": ["Director Payments", "Director Fulfillment"],
        "knows_about": ["team-payments", "team-fulfillment"],
    },
    "Director Backend": {"reports": ["team-backend"], "knows_about": ["team-backend"]},
    "Director Frontend": {"reports": ["team-frontend"], "knows_about": ["team-frontend"]},
    "Director Platform": {"reports": ["team-platform"], "knows_about": ["team-platform"]},
    "Director SRE": {"reports": ["team-security"], "knows_about": ["team-security"]},
    "Director Payments": {"reports": ["team-payments"], "knows_about": ["team-payments"]},
    "Director Fulfillment": {"reports": ["team-fulfillment"], "knows_about": ["team-fulfillment"]},
}

COST_DATA = {
    "total_monthly": 127500,
    "untagged": 76500,
    "tagged": 51000,
    "by_team": {
        "team-platform": 12500,
        "team-backend": 15000,
        "team-frontend": 8000,
        "team-data": 22000,
        "team-security": 9500,
        "team-payments": 18000,
        "team-fulfillment": 14000,
        "unallocated": 28500,
    },
}
