"""Act 3: The Revelation

This module renders the scenes for Act 3 where the player discovers
the root cause and sees the full impact of the incident.
"""

import streamlit as st

from components.theme import (
    COLOR_BG_SURFACE,
    COLOR_BG_ELEVATED,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_MUTED,
    COLOR_CRITICAL,
    COLOR_WARNING,
    COLOR_SUCCESS,
    COLOR_INFO,
    COLOR_BORDER,
    GRADIENT_CRITICAL,
    SHADOW_BASE,
    RADIUS_BASE,
    RADIUS_LG,
    SPACE_BASE,
    SPACE_LG,
    SPACE_XL,
    TEXT_SM,
    TEXT_BASE,
    TEXT_LG,
    TEXT_XL,
    TEXT_2XL,
    FONT_WEIGHT_MEDIUM,
    FONT_WEIGHT_SEMIBOLD,
    FONT_WEIGHT_BOLD,
    ICONS,
)
from components.ui_components import (
    styled_card,
    status_card,
    alert_card,
    action_button,
    nav_button,
    timeline_container,
    divider,
    spacer,
)
from components.state_manager import (
    get_mttr_display,
    get_revenue_display,
    advance_scene,
    advance_act,
)


def render_act3():
    """Render Act 3: The Revelation"""
    scene = st.session_state.current_scene

    if scene == 0:
        render_scene_3_1_discovery()
    elif scene == 1:
        render_scene_3_2_consequences()
    else:
        advance_act()
        st.rerun()


def render_scene_3_1_discovery():
    """Scene 3.1: The Accidental Discovery"""

    st.markdown(f"### {ICONS['search']} The Revelation")
    st.caption(f"Final MTTR: {get_mttr_display()} | Total revenue impact: {get_revenue_display()}")

    # Discovery card
    st.markdown(
        f"""
    <div class='animate-fade-in' style='
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid {COLOR_BORDER};
        border-radius: {RADIUS_LG};
        padding: 40px;
        text-align: center;
        margin: 24px 0;
    '>
        <div style='font-size: 48px; margin-bottom: 16px;'>{ICONS["lightbulb"]}</div>
        <h2 style='color: {COLOR_INFO}; margin: 0 0 16px 0;'>The Truth Revealed</h2>
        <p style='color: {COLOR_TEXT_SECONDARY}; font-size: 18px; margin: 0 0 24px 0;'>
            After hours of searching, you find a random Slack thread from 3 months ago...
        </p>
        <div style='
            background-color: {COLOR_BG_SURFACE};
            border: 1px solid {COLOR_BORDER};
            border-radius: {RADIUS_BASE};
            padding: 24px;
            text-align: left;
            max-width: 600px;
            margin: 0 auto;
        '>
            <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 12px;'>
                <span style='font-size: 20px;'>{ICONS["slack"]}</span>
                <span style='font-weight: {FONT_WEIGHT_SEMIBOLD}; color: {COLOR_TEXT_PRIMARY};'>#general — March 15th</span>
            </div>
            <hr style='border-color: {COLOR_BORDER}; margin: 12px 0;'>
            <div style='margin-bottom: 12px;'>
                <span style='color: {COLOR_INFO}; font-weight: {FONT_WEIGHT_MEDIUM};'>@sarah-payments:</span>
                <span style='color: {COLOR_TEXT_SECONDARY};'> Hey team, just a heads up — we're taking over payment-api from team-backend starting next sprint.</span>
            </div>
            <div style='margin-bottom: 12px;'>
                <span style='color: {COLOR_INFO}; font-weight: {FONT_WEIGHT_MEDIUM};'>@mike-backend:</span>
                <span style='color: {COLOR_TEXT_SECONDARY};'> Great! Don't forget to update the K8s labels and service catalog.</span>
            </div>
            <div style='margin-bottom: 12px;'>
                <span style='color: {COLOR_INFO}; font-weight: {FONT_WEIGHT_MEDIUM};'>@sarah-payments:</span>
                <span style='color: {COLOR_TEXT_SECONDARY};'> Will do!</span>
            </div>
            <div style='
                background-color: rgba(220, 38, 38, 0.1);
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
                color: {COLOR_CRITICAL};
                text-align: center;
            '>
                {ICONS["warning"]} [3 months later... labels were never updated]
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Root cause
    st.markdown(
        f"""
    <div style='
        background-color: rgba(220, 38, 38, 0.1);
        border: 1px solid rgba(220, 38, 38, 0.3);
        border-radius: {RADIUS_BASE};
        padding: 24px;
        margin: 16px 0;
    '>
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 16px;'>
            <span style='font-size: 28px;'>{ICONS["error"]}</span>
            <span style='color: {COLOR_CRITICAL}; font-weight: {FONT_WEIGHT_SEMIBOLD}; font-size: 20px;'>ROOT CAUSE IDENTIFIED</span>
        </div>
        <p style='color: {COLOR_TEXT_SECONDARY}; margin: 0 0 12px 0;'>
            The incident took 4+ hours to resolve because:
        </p>
        <ul style='color: {COLOR_TEXT_SECONDARY}; margin: 0;'>
            <li>K8s labels were never updated after team migration</li>
            <li>No service catalog entry reflected the new ownership</li>
            <li>Cost attribution tags were missing</li>
            <li>Org chart didn't match reality</li>
        </ul>
        <p style='color: {COLOR_CRITICAL}; font-weight: {FONT_WEIGHT_SEMIBOLD}; margin: 16px 0 0 0; font-size: 16px;'>
            This is a FinOps failure, not just a technical failure.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    spacer()

    if action_button(
        "SEE THE FULL IMPACT", key="to_impact", icon=ICONS["arrow_forward"], type="primary"
    ):
        advance_scene()
        st.rerun()


def render_scene_3_2_consequences():
    """Scene 3.2: The Consequence Screen"""

    st.markdown(f"### {ICONS['metric']} Incident Impact Report")

    # Header
    st.markdown(
        f"""
    <div style='
        background: {GRADIENT_CRITICAL};
        border-radius: {RADIUS_LG};
        padding: 32px;
        text-align: center;
        margin: 24px 0;
        box-shadow: {SHADOW_BASE};
    '>
        <div style='font-size: 40px; margin-bottom: 12px;'>{ICONS["warning"]}</div>
        <h2 style='color: white; margin: 0;'>POST-INCIDENT REVIEW</h2>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Business Impact
    st.markdown("#### Business Impact")

    cols = st.columns(3)
    business_metrics = [
        {
            "label": "Revenue Lost",
            "value": "$127,000",
            "color": COLOR_CRITICAL,
            "icon": ICONS["money"],
        },
        {"label": "MTTR", "value": "4h 23m", "color": COLOR_CRITICAL, "icon": ICONS["time"]},
        {
            "label": "Customer Tickets",
            "value": "340",
            "color": COLOR_WARNING,
            "icon": ICONS["ticket"],
        },
    ]

    for i, metric in enumerate(business_metrics):
        with cols[i]:
            st.markdown(
                f"""
            <div style='
                background-color: {COLOR_BG_SURFACE};
                border: 1px solid {COLOR_BORDER};
                border-top: 4px solid {metric["color"]};
                border-radius: {RADIUS_BASE};
                padding: 24px;
                text-align: center;
            '>
                <div style='font-size: 28px; margin-bottom: 8px;'>{metric["icon"]}</div>
                <div style='font-size: 12px; color: {COLOR_TEXT_MUTED}; margin-bottom: 4px;'>{metric["label"]}</div>
                <div style='font-size: 32px; font-weight: {FONT_WEIGHT_BOLD}; color: {metric["color"]};'>{metric["value"]}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # Operational Impact
    st.markdown("#### Operational Impact")

    cols = st.columns(3)
    operational_metrics = [
        {
            "label": "SLO Breach",
            "value": "99.9% → 94.2%",
            "color": COLOR_CRITICAL,
            "icon": ICONS["slo"],
        },
        {
            "label": "Teams Disrupted",
            "value": "8 teams",
            "color": COLOR_WARNING,
            "icon": ICONS["team"],
        },
        {
            "label": "On-Call Burnout",
            "value": "CRITICAL",
            "color": COLOR_CRITICAL,
            "icon": ICONS["alert"],
        },
    ]

    for i, metric in enumerate(operational_metrics):
        with cols[i]:
            st.markdown(
                f"""
            <div style='
                background-color: {COLOR_BG_SURFACE};
                border: 1px solid {COLOR_BORDER};
                border-top: 4px solid {metric["color"]};
                border-radius: {RADIUS_BASE};
                padding: 24px;
                text-align: center;
            '>
                <div style='font-size: 28px; margin-bottom: 8px;'>{metric["icon"]}</div>
                <div style='font-size: 12px; color: {COLOR_TEXT_MUTED}; margin-bottom: 4px;'>{metric["label"]}</div>
                <div style='font-size: 24px; font-weight: {FONT_WEIGHT_BOLD}; color: {metric["color"]};'>{metric["value"]}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    spacer()

    # Timeline
    st.markdown("#### Timeline of Pain")

    timeline_items = [
        {"time": "2:17 AM", "event": "Alert fires", "elapsed": "0 min", "status": "info"},
        {
            "time": "2:19 AM",
            "event": "On-call acknowledges",
            "elapsed": "2 min",
            "status": "success",
        },
        {
            "time": "2:24 AM",
            "event": "Check K8s labels — dead end",
            "elapsed": "7 min",
            "status": "critical",
        },
        {
            "time": "2:45 AM",
            "event": "Slack chaos — 3 wrong teams",
            "elapsed": "28 min",
            "status": "critical",
        },
        {
            "time": "3:30 AM",
            "event": "Org chart hunt — outdated info",
            "elapsed": "73 min",
            "status": "critical",
        },
        {
            "time": "4:15 AM",
            "event": "Cost reports — 60% untagged",
            "elapsed": "118 min",
            "status": "critical",
        },
        {
            "time": "5:00 AM",
            "event": "Escalation to VP",
            "elapsed": "163 min",
            "status": "critical",
        },
        {
            "time": "5:45 AM",
            "event": "Finally find team-payments",
            "elapsed": "208 min",
            "status": "warning",
        },
        {
            "time": "5:48 AM",
            "event": "Fix applied (restart pod)",
            "elapsed": "211 min",
            "status": "success",
        },
        {
            "time": "6:30 AM",
            "event": "Service fully recovered",
            "elapsed": "253 min",
            "status": "success",
        },
    ]

    st.markdown(timeline_container(timeline_items), unsafe_allow_html=True)

    spacer()

    # Brutal truth
    st.markdown(
        f"""
    <div style='
        background-color: rgba(220, 38, 38, 0.15);
        border: 2px solid {COLOR_CRITICAL};
        border-radius: {RADIUS_BASE};
        padding: 24px;
        margin: 16px 0;
        text-align: center;
    '>
        <div style='font-size: 32px; margin-bottom: 12px;'>{ICONS["critical"]}</div>
        <h3 style='color: {COLOR_CRITICAL}; margin: 0 0 12px 0;'>THE BRUTAL TRUTH</h3>
        <p style='color: {COLOR_TEXT_SECONDARY}; font-size: 18px; margin: 0 0 8px 0;'>
            The actual technical fix took <strong style='color: {COLOR_SUCCESS};'>3 minutes</strong>.
        </p>
        <p style='color: {COLOR_TEXT_SECONDARY}; font-size: 18px; margin: 0;'>
            Finding who should apply the fix took <strong style='color: {COLOR_CRITICAL};'>4 hours and 20 minutes</strong>.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # What if FinOps
    st.markdown(
        f"""
    <div style='
        background-color: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: {RADIUS_BASE};
        padding: 20px;
        margin: 16px 0;
        display: flex;
        align-items: center;
        gap: 12px;
    '>
        <span style='font-size: 24px;'>{ICONS["lightbulb"]}</span>
        <div>
            <span style='color: {COLOR_INFO}; font-weight: {FONT_WEIGHT_SEMIBOLD};'>What if we had proper FinOps from the start?</span>
            <br>
            <span style='color: {COLOR_TEXT_MUTED}; font-size: 14px;'>Let's rewind and see how this incident would have played out...</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    spacer()

    if action_button(
        "REWIND WITH FINOPS ENABLED", key="rewind", icon=ICONS["refresh"], type="primary"
    ):
        st.session_state.finops_enabled = True
        st.session_state.mttr_minutes = 0
        st.session_state.revenue_lost = 0
        advance_act()
        st.rerun()
