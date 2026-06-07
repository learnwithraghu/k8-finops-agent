"""Act 1: The Incident Begins

This module renders the scenes for Act 1 where the player receives a critical
alert and begins investigating a Kubernetes service outage.
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
    SHADOW_GLOW_CRITICAL,
    RADIUS_BASE,
    RADIUS_LG,
    SPACE_BASE,
    SPACE_LG,
    SPACE_XL,
    TEXT_LG,
    TEXT_XL,
    TEXT_2XL,
    FONT_WEIGHT_SEMIBOLD,
    FONT_WEIGHT_BOLD,
    ICONS,
)
from components.ui_components import (
    styled_card,
    status_card,
    alert_card,
    service_card,
    label_table,
    action_button,
    nav_button,
    divider,
    spacer,
)
from components.state_manager import (
    add_mttr,
    get_mttr_display,
    get_revenue_display,
    BROKEN_SERVICES,
    advance_scene,
    advance_act,
)


def render_act1():
    """Render Act 1: The Incident Begins"""
    scene = st.session_state.current_scene

    if scene == 0:
        render_scene_1_1_pager_alert()
    elif scene == 1:
        render_scene_1_2_dashboard()
    elif scene == 2:
        render_scene_1_3_check_labels()
    else:
        advance_act()
        st.rerun()


def render_scene_1_1_pager_alert():
    """Scene 1.1: The 2 AM Page - Critical alert notification"""

    # Time display
    st.markdown(
        f"""
    <div class='animate-fade-in' style='
        text-align: center;
        margin: 32px 0;
    '>
        <div style='
            display: inline-flex;
            align-items: center;
            gap: 12px;
            background-color: {COLOR_BG_SURFACE};
            border: 1px solid {COLOR_BORDER};
            border-radius: {RADIUS_LG};
            padding: 16px 32px;
        '>
            <span style='font-size: 32px;'>{ICONS["time"]}</span>
            <span style='font-size: 36px; font-weight: {FONT_WEIGHT_BOLD}; color: {COLOR_CRITICAL};'>2:17 AM</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Critical alert banner
    st.markdown(
        f"""
    <div class='animate-pulse' style='
        background: {GRADIENT_CRITICAL};
        border-radius: {RADIUS_LG};
        padding: 40px;
        text-align: center;
        margin: 24px 0;
        box-shadow: {SHADOW_GLOW_CRITICAL};
    '>
        <div style='font-size: 48px; margin-bottom: 16px;'>{ICONS["critical"]}</div>
        <h1 style='color: white; margin: 0 0 8px 0; font-size: 32px;'>CRITICAL ALERT</h1>
        <h2 style='color: rgba(255,255,255,0.9); margin: 0 0 16px 0; font-size: 24px;'>Service: payment-api</h2>
        <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 18px;'>
            Impact: Payment processing DOWN. Customers cannot complete purchases.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Alert details
    st.markdown(
        f"""
    <div class='animate-slide-in-right' style='
        background-color: rgba(220, 38, 38, 0.1);
        border: 1px solid rgba(220, 38, 38, 0.3);
        border-radius: {RADIUS_BASE};
        padding: 16px;
        margin: 16px 0;
        display: flex;
        align-items: center;
        gap: 12px;
    '>
        <span style='font-size: 24px;'>{ICONS["alert"]}</span>
        <div>
            <span style='color: {COLOR_CRITICAL}; font-weight: {FONT_WEIGHT_SEMIBOLD}; font-size: 16px;'>SEV-1 Incident Declared</span>
            <br>
            <span style='color: {COLOR_TEXT_SECONDARY}; font-size: 14px;'>You are the on-call engineer. This is your responsibility to resolve.</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Metrics row
    st.markdown("### Impact Metrics")

    cols = st.columns(3)
    metrics = [
        {
            "label": "Error Rate",
            "value": "98.5%",
            "delta": "+95%",
            "delta_color": "inverse",
            "icon": ICONS["error"],
        },
        {
            "label": "Latency",
            "value": "45s",
            "delta": "+40s",
            "delta_color": "inverse",
            "icon": ICONS["time"],
        },
        {
            "label": "Affected Users",
            "value": "12,400",
            "delta": "+12,000",
            "delta_color": "inverse",
            "icon": ICONS["customer"],
        },
    ]

    for i, metric in enumerate(metrics):
        with cols[i]:
            st.markdown(
                f"""
            <div style='
                background-color: {COLOR_BG_SURFACE};
                border: 1px solid {COLOR_BORDER};
                border-radius: {RADIUS_BASE};
                padding: 20px;
                text-align: center;
            '>
                <div style='font-size: 24px; margin-bottom: 8px;'>{metric["icon"]}</div>
                <div style='font-size: 12px; color: {COLOR_TEXT_MUTED}; margin-bottom: 4px;'>{metric["label"]}</div>
                <div style='font-size: 28px; font-weight: {FONT_WEIGHT_BOLD}; color: {COLOR_CRITICAL};'>{metric["value"]}</div>
                <div style='font-size: 12px; color: {COLOR_CRITICAL};'>{metric["delta"]}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    spacer()

    # Action button
    if action_button(
        "ACKNOWLEDGE ALERT & BEGIN INVESTIGATION",
        key="ack_alert",
        icon=ICONS["ack"],
        type="primary",
    ):
        add_mttr(2)
        advance_scene()
        st.rerun()


def render_scene_1_2_dashboard():
    """Scene 1.2: The Dashboard - Cascading failure visualization"""

    st.markdown(f"### {ICONS['dashboard']} Incident Dashboard")
    st.caption(f"MTTR: {get_mttr_display()} | Revenue impact: {get_revenue_display()}")

    # Cascading failure alert
    st.markdown(
        f"""
    <div style='
        background-color: rgba(220, 38, 38, 0.1);
        border: 1px solid rgba(220, 38, 38, 0.3);
        border-radius: {RADIUS_BASE};
        padding: 20px;
        margin: 16px 0;
    '>
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 12px;'>
            <span style='font-size: 24px;'>{ICONS["error"]}</span>
            <span style='color: {COLOR_CRITICAL}; font-weight: {FONT_WEIGHT_SEMIBOLD}; font-size: 18px;'>CASCADING FAILURE DETECTED</span>
        </div>
        <p style='color: {COLOR_TEXT_SECONDARY}; margin: 0; line-height: 1.6;'>
            The payment-api failure is causing downstream impacts across multiple services:
        </p>
        <ul style='color: {COLOR_TEXT_SECONDARY}; margin: 8px 0 0 0;'>
            <li>order-service: <span style='color: {COLOR_CRITICAL};'>67% error rate</span></li>
            <li>notification-service: <span style='color: {COLOR_WARNING};'>45% error rate</span></li>
            <li>analytics-pipeline: <span style='color: {COLOR_WARNING};'>Backpressure building</span></li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("### Failure Propagation")

    # Service cascade cards
    services = [
        {
            "name": "payment-api",
            "status": "critical",
            "detail": "98.5% errors",
            "icon": ICONS["pod"],
        },
        {
            "name": "order-svc",
            "status": "warning",
            "detail": "67% errors",
            "icon": ICONS["service"],
        },
        {
            "name": "notify-svc",
            "status": "warning",
            "detail": "45% errors",
            "icon": ICONS["service"],
        },
        {"name": "analytics", "status": "info", "detail": "Backpressure", "icon": ICONS["metric"]},
    ]

    cols = st.columns(4)
    for i, svc in enumerate(services):
        with cols[i]:
            st.markdown(
                service_card(
                    name=svc["name"],
                    status=svc["status"],
                    error_rate=svc["detail"] if "error" in svc["detail"] else "",
                    extra_details=svc["detail"] if "error" not in svc["detail"] else "",
                ),
                unsafe_allow_html=True,
            )

    # Connection arrows
    st.markdown(
        f"""
    <div style='
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;
        margin: 16px 0;
        color: {COLOR_TEXT_MUTED};
        font-size: 14px;
    '>
        <span>Cascading impact</span>
        <span style='font-size: 20px;'>{ICONS["arrow_forward"]}</span>
        <span>Downstream services affected</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Info card
    st.markdown(
        f"""
    <div style='
        background-color: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: {RADIUS_BASE};
        padding: 16px;
        margin: 16px 0;
        display: flex;
        align-items: flex-start;
        gap: 12px;
    '>
        <span style='font-size: 20px; margin-top: 2px;'>{ICONS["lightbulb"]}</span>
        <div>
            <span style='color: {COLOR_INFO}; font-weight: {FONT_WEIGHT_SEMIBOLD};'>Your first step:</span>
            <span style='color: {COLOR_TEXT_SECONDARY};'> Find who owns the payment-api service so they can investigate.</span>
            <br>
            <span style='color: {COLOR_TEXT_MUTED}; font-size: 14px;'>In a well-organized cluster, you'd check the service labels or service catalog...</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    spacer()

    if action_button(
        "CHECK SERVICE LABELS & OWNERSHIP",
        key="check_labels",
        icon=ICONS["search"],
        type="primary",
    ):
        add_mttr(5)
        advance_scene()
        st.rerun()


def render_scene_1_3_check_labels():
    """Scene 1.3: Check Labels - The pain begins"""

    st.markdown(f"### {ICONS['label']} Kubernetes Resource Labels")
    st.caption(f"MTTR: {get_mttr_display()} | Revenue impact: {get_revenue_display()}")

    st.markdown(
        f"""
    <div style='
        background-color: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: {RADIUS_BASE};
        padding: 16px;
        margin: 16px 0;
        display: flex;
        align-items: center;
        gap: 12px;
    '>
        <span style='font-size: 20px;'>{ICONS["warning"]}</span>
        <span style='color: {COLOR_WARNING};'>You found the payment-api resources. Now let's check their labels...</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(f"### {ICONS['pod']} Pod: payment-api-7d9f4b8c5-x2v9p")

    # Labels table
    labels = {
        "app": "payment-api",
        "version": "v2.3.1",
        "owner": "unknown",
        "cost-center": "legacy",
        "team": "NOT SET",
        "contact": "NOT SET",
        "oncall-slack": "NOT SET",
    }

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(label_table(labels, status="critical"), unsafe_allow_html=True)

    with col2:
        # Annotations
        st.markdown(
            f"""
        <div style='
            background-color: {COLOR_BG_SURFACE};
            border: 1px solid {COLOR_BORDER};
            border-left: 4px solid {COLOR_WARNING};
            border-radius: {RADIUS_BASE};
            padding: 20px;
        '>
            <h4 style='margin: 0 0 12px 0; color: {COLOR_TEXT_PRIMARY};'>{ICONS["info"]} Annotations</h4>
            <table style='width: 100%; color: {COLOR_TEXT_SECONDARY};'>
                <tr>
                    <td><code>description</code></td>
                    <td style='text-align: right;'>Payment processing API</td>
                </tr>
                <tr>
                    <td><code>deployed-by</code></td>
                    <td style='text-align: right; color: {COLOR_WARNING};'>john.smith@company.com</td>
                </tr>
                <tr>
                    <td><code>deployed-on</code></td>
                    <td style='text-align: right;'>2023-08-15</td>
                </tr>
            </table>
            <div style='
                margin-top: 12px;
                padding: 8px;
                background-color: rgba(245, 158, 11, 0.1);
                border-radius: 6px;
                font-size: 12px;
                color: {COLOR_WARNING};
            '>
                {ICONS["warning"]} john.smith left the company 6 months ago...
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    spacer()

    # Problem identified
    st.markdown(
        f"""
    <div style='
        background-color: rgba(220, 38, 38, 0.1);
        border: 1px solid rgba(220, 38, 38, 0.3);
        border-radius: {RADIUS_BASE};
        padding: 20px;
        margin: 16px 0;
    '>
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 12px;'>
            <span style='font-size: 24px;'>{ICONS["error"]}</span>
            <span style='color: {COLOR_CRITICAL}; font-weight: {FONT_WEIGHT_SEMIBOLD}; font-size: 18px;'>PROBLEM IDENTIFIED</span>
        </div>
        <p style='color: {COLOR_TEXT_SECONDARY}; margin: 0 0 12px 0;'>
            The payment-api pod has <strong style='color: {COLOR_TEXT_PRIMARY};'>no ownership information</strong>:
        </p>
        <ul style='color: {COLOR_TEXT_SECONDARY}; margin: 0;'>
            <li><code>owner=unknown</code> — not helpful</li>
            <li><code>cost-center=legacy</code> — service was migrated, but labels weren't updated</li>
            <li>No team Slack channel for escalation</li>
            <li>The person who deployed it (john.smith) is no longer at the company</li>
        </ul>
        <p style='color: {COLOR_CRITICAL}; font-weight: {FONT_WEIGHT_SEMIBOLD}; margin: 12px 0 0 0;'>
            You cannot identify the owner from the Kubernetes labels alone.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # What would FinOps fix
    st.markdown(
        f"""
    <div style='
        background-color: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: {RADIUS_BASE};
        padding: 20px;
        margin: 16px 0;
    '>
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 12px;'>
            <span style='font-size: 20px;'>{ICONS["lightbulb"]}</span>
            <span style='color: {COLOR_INFO}; font-weight: {FONT_WEIGHT_SEMIBOLD}; font-size: 16px;'>What would FinOps fix this?</span>
        </div>
        <p style='color: {COLOR_TEXT_SECONDARY}; margin: 0 0 12px 0;'>With proper FinOps tagging policy:</p>
        <div style='display: flex; flex-wrap: wrap; gap: 8px;'>
            <span style='
                background-color: rgba(16, 185, 129, 0.2);
                color: {COLOR_SUCCESS};
                border: 1px solid rgba(16, 185, 129, 0.4);
                border-radius: 9999px;
                padding: 4px 12px;
                font-size: 13px;
            '>owner=team-payments</span>
            <span style='
                background-color: rgba(16, 185, 129, 0.2);
                color: {COLOR_SUCCESS};
                border: 1px solid rgba(16, 185, 129, 0.4);
                border-radius: 9999px;
                padding: 4px 12px;
                font-size: 13px;
            '>cost-center=payments-revenue</span>
            <span style='
                background-color: rgba(16, 185, 129, 0.2);
                color: {COLOR_SUCCESS};
                border: 1px solid rgba(16, 185, 129, 0.4);
                border-radius: 9999px;
                padding: 4px 12px;
                font-size: 13px;
            '>team-slack=#payments-oncall</span>
            <span style='
                background-color: rgba(16, 185, 129, 0.2);
                color: {COLOR_SUCCESS};
                border: 1px solid rgba(16, 185, 129, 0.4);
                border-radius: 9999px;
                padding: 4px 12px;
                font-size: 13px;
            '>service-catalog-id=svc-pay-001</span>
        </div>
        <p style='color: {COLOR_TEXT_MUTED}; margin: 12px 0 0 0; font-size: 14px;'>
            You'd know exactly who to contact in <strong style='color: {COLOR_SUCCESS};'>under 30 seconds</strong>.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    spacer()

    if action_button(
        "CONTINUE INVESTIGATION",
        key="continue_investigation",
        icon=ICONS["arrow_forward"],
        type="primary",
    ):
        add_mttr(15)
        advance_scene()
        st.rerun()
