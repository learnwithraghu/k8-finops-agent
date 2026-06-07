"""Act 4: The FinOps Solution

This module renders the scenes for Act 4 where the game rewinds and replays
the incident with proper FinOps practices in place, demonstrating the stark
contrast between poor and excellent FinOps hygiene.
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
    GRADIENT_SUCCESS,
    GRADIENT_INFO,
    GRADIENT_DARK,
    SHADOW_BASE,
    SHADOW_SM,
    SHADOW_GLOW_SUCCESS,
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
    service_card,
    label_table,
    comparison_card,
    action_button,
    nav_button,
    tag,
    divider,
    spacer,
)
from components.state_manager import (
    get_mttr_display,
    get_revenue_display,
    BROKEN_SERVICES,
    TEAMS,
    COST_DATA,
    advance_scene,
    advance_act,
)


def render_act4():
    """Render Act 4: The FinOps Solution"""
    scene = st.session_state.current_scene

    if scene == 0:
        render_scene_4_1_rewind()
    elif scene == 1:
        render_scene_4_2_finops_enabled()
    elif scene == 2:
        render_scene_4_3_comparison()
    elif scene == 3:
        render_scene_4_4_finops_dashboard()
    else:
        advance_act()
        st.rerun()


# =============================================================================
# SCENE 4.1: THE REWIND
# =============================================================================


def render_scene_4_1_rewind():
    """Scene 4.1: The Rewind — time-rewind animation and setup."""

    # Time rewind visual
    st.markdown(
        f"""
    <div class='animate-rewind' style='
        background: {GRADIENT_DARK};
        border: 2px solid {COLOR_INFO};
        border-radius: {RADIUS_LG};
        padding: 48px;
        text-align: center;
        margin: 32px 0;
        box-shadow: {SHADOW_BASE};
    '>
        <div style='font-size: 64px; margin-bottom: 16px;'>{ICONS["rewind"]}</div>
        <h1 style='color: {COLOR_INFO}; margin: 0 0 12px 0; font-size: 36px;'>TIME REWIND</h1>
        <p style='color: {COLOR_TEXT_SECONDARY}; font-size: 18px; margin: 0 0 24px 0; max-width: 600px; margin-left: auto; margin-right: auto;'>
            Let's replay the same incident with proper FinOps practices in place...
        </p>
        <div style='
            background-color: {COLOR_BG_SURFACE};
            border: 1px solid {COLOR_BORDER};
            border-radius: {RADIUS_BASE};
            padding: 20px;
            max-width: 500px;
            margin: 0 auto;
            text-align: left;
        '>
            <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 12px;'>
                <span style='font-size: 20px;'>{ICONS["info"]}</span>
                <span style='color: {COLOR_TEXT_PRIMARY}; font-weight: {FONT_WEIGHT_SEMIBOLD};'>What changed?</span>
            </div>
            <ul style='color: {COLOR_TEXT_SECONDARY}; margin: 0; padding-left: 20px; line-height: 1.8;'>
                <li>All K8s resources have proper ownership labels</li>
                <li>Service catalog is up-to-date and accurate</li>
                <li>100% cost attribution with enforced tagging</li>
                <li>Single FinOps dashboard for everything</li>
            </ul>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Promise
    st.markdown(
        f"""
    <div class='animate-fade-in' style='
        background-color: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: {RADIUS_BASE};
        padding: 20px;
        margin: 16px 0;
        text-align: center;
    '>
        <span style='color: {COLOR_SUCCESS}; font-size: 18px; font-weight: {FONT_WEIGHT_SEMIBOLD};'>
            {ICONS["success"]} Watch how the same 3-minute fix takes <strong>30 seconds</strong> to find the owner.
        </span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    spacer()

    if action_button(
        "PLAY WITH FINOPS ENABLED",
        key="play_finops",
        icon=ICONS["play"],
        type="primary",
    ):
        advance_scene()
        st.rerun()


# =============================================================================
# SCENE 4.2: WITH PROPER FINOPS
# =============================================================================


def render_scene_4_2_finops_enabled():
    """Scene 4.2: The FinOps-Enabled Investigation — instant ownership discovery."""

    st.markdown(f"### {ICONS['dashboard']} FinOps-Enabled Investigation")
    st.caption(f"MTTR so far: {get_mttr_display()} | Revenue impact: {get_revenue_display()}")

    # Alert with success styling
    st.markdown(
        f"""
    <div class='animate-fade-in' style='
        background: {GRADIENT_SUCCESS};
        border-radius: {RADIUS_LG};
        padding: 24px;
        margin: 16px 0;
        box-shadow: {SHADOW_GLOW_SUCCESS};
    '>
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 8px;'>
            <span style='font-size: 28px;'>{ICONS["success"]}</span>
            <span style='color: white; font-weight: {FONT_WEIGHT_SEMIBOLD}; font-size: 20px;'>2:17 AM — Alert Fires</span>
        </div>
        <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 16px;'>
            You get the PagerDuty alert. Now let's find the owner...
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(f"### {ICONS['label']} Step 1: Check K8s Labels")
    st.caption("Every resource has complete ownership information")

    # Good labels table
    good_labels = {
        "app": "payment-api",
        "version": "v2.3.1",
        "owner": "team-payments",
        "cost-center": "payments-revenue",
        "team": "payments",
        "contact": "sarah.payments@company.com",
        "oncall-slack": "#payments-oncall",
        "service-catalog-id": "svc-pay-001",
        "oncall-rotation": "payments-primary",
    }

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
        <div class='animate-slide-in-left' style='
            background-color: {COLOR_BG_SURFACE};
            border: 1px solid {COLOR_BORDER};
            border-left: 4px solid {COLOR_SUCCESS};
            border-radius: {RADIUS_BASE};
            padding: 20px;
        '>
            <h4 style='margin: 0 0 12px 0; color: {COLOR_TEXT_PRIMARY};'>
                {ICONS["pod"]} Pod: payment-api-7d9f4b8c5-x2v9p
            </h4>
            {label_table(good_labels, status="success")}
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        # Service catalog info
        st.markdown(
            f"""
        <div class='animate-slide-in-right' style='
            background-color: {COLOR_BG_SURFACE};
            border: 1px solid {COLOR_BORDER};
            border-left: 4px solid {COLOR_SUCCESS};
            border-radius: {RADIUS_BASE};
            padding: 20px;
        '>
            <h4 style='margin: 0 0 12px 0; color: {COLOR_TEXT_PRIMARY};'>
                {ICONS["service"]} Service Catalog Entry
            </h4>
            <table style='width: 100%; color: {COLOR_TEXT_SECONDARY};'>
                <tr>
                    <td style='padding: 6px 0;'><code>owner</code></td>
                    <td style='text-align: right; color: {COLOR_SUCCESS};'>team-payments</td>
                </tr>
                <tr>
                    <td style='padding: 6px 0;'><code>contact</code></td>
                    <td style='text-align: right; color: {COLOR_TEXT_PRIMARY};'>sarah.payments@company.com</td>
                </tr>
                <tr>
                    <td style='padding: 6px 0;'><code>slack-channel</code></td>
                    <td style='text-align: right; color: {COLOR_SUCCESS};'>#payments-oncall</td>
                </tr>
                <tr>
                    <td style='padding: 6px 0;'><code>service-catalog</code></td>
                    <td style='text-align: right; color: {COLOR_INFO}; font-size: 12px;'>svc-pay-001</td>
                </tr>
                <tr>
                    <td style='padding: 6px 0;'><code>cost-per-month</code></td>
                    <td style='text-align: right; color: {COLOR_TEXT_PRIMARY}; font-weight: {FONT_WEIGHT_BOLD};'>$18,500</td>
                </tr>
            </table>
        </div>
        """,
            unsafe_allow_html=True,
        )

    spacer()

    # Success banner
    st.markdown(
        f"""
    <div class='animate-fade-in' style='
        background-color: rgba(16, 185, 129, 0.15);
        border: 2px solid {COLOR_SUCCESS};
        border-radius: {RADIUS_LG};
        padding: 32px;
        margin: 24px 0;
        text-align: center;
    '>
        <div style='font-size: 48px; margin-bottom: 12px;'>{ICONS["success"]}</div>
        <h2 style='color: {COLOR_SUCCESS}; margin: 0 0 12px 0;'>FOUND IN 30 SECONDS!</h2>
        <p style='color: {COLOR_TEXT_SECONDARY}; font-size: 16px; margin: 0 0 16px 0;'>
            Complete ownership information is available everywhere:
        </p>
        <div style='display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;'>
            <span style='
                background-color: rgba(16, 185, 129, 0.2);
                color: {COLOR_SUCCESS};
                border: 1px solid rgba(16, 185, 129, 0.4);
                border-radius: 9999px;
                padding: 6px 16px;
                font-size: 14px;
            '>{ICONS["label"]} K8s Labels</span>
            <span style='
                background-color: rgba(16, 185, 129, 0.2);
                color: {COLOR_SUCCESS};
                border: 1px solid rgba(16, 185, 129, 0.4);
                border-radius: 9999px;
                padding: 6px 16px;
                font-size: 14px;
            '>{ICONS["service"]} Service Catalog</span>
            <span style='
                background-color: rgba(16, 185, 129, 0.2);
                color: {COLOR_SUCCESS};
                border: 1px solid rgba(16, 185, 129, 0.4);
                border-radius: 9999px;
                padding: 6px 16px;
                font-size: 14px;
            '>{ICONS["cost"]} Cost Attribution</span>
        </div>
        <p style='color: {COLOR_TEXT_MUTED}; margin: 16px 0 0 0; font-size: 14px;'>
            No searching, no dead ends, no frustration.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    spacer()

    if action_button(
        "CONTINUE",
        key="continue_from_finops",
        icon=ICONS["arrow_forward"],
        type="primary",
    ):
        advance_scene()
        st.rerun()


# =============================================================================
# SCENE 4.3: SIDE-BY-SIDE COMPARISON
# =============================================================================


def render_scene_4_3_comparison():
    """Scene 4.3: Before vs After comparison using theme-aware cards."""

    st.markdown(f"### {ICONS['compare']} Before vs After")
    st.caption(f"MTTR so far: {get_mttr_display()} | Revenue impact: {get_revenue_display()}")

    st.markdown(
        f"""
    <div class='animate-fade-in' style='text-align: center; margin-bottom: 24px;'>
        <p style='color: {COLOR_TEXT_SECONDARY}; font-size: 18px; margin: 0;'>
            The same incident. Two very different outcomes.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            comparison_card(
                title=f"{ICONS['error']} WITHOUT FINOPS",
                status="critical",
                items=[
                    {"label": "Time to identify owner", "value": "4+ hours", "highlight": True},
                    {"label": "Revenue lost", "value": "$127,000", "highlight": True},
                    {"label": "Teams contacted", "value": "8 teams", "highlight": False},
                    {"label": "Escalation levels", "value": "4 levels", "highlight": False},
                    {"label": "Customer tickets", "value": "340 tickets", "highlight": True},
                    {"label": "SLO breach", "value": "99.9% → 94.2%", "highlight": True},
                    {"label": "On-call burnout", "value": "CRITICAL", "highlight": True},
                    {"label": "MTTR", "value": "4h 23m", "highlight": True},
                ],
            ),
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            comparison_card(
                title=f"{ICONS['success']} WITH FINOPS",
                status="success",
                items=[
                    {"label": "Time to identify owner", "value": "30 seconds", "highlight": True},
                    {"label": "Revenue lost", "value": "$0", "highlight": True},
                    {"label": "Teams contacted", "value": "1 team", "highlight": False},
                    {"label": "Escalation levels", "value": "0 (direct)", "highlight": False},
                    {"label": "Customer tickets", "value": "0 tickets", "highlight": True},
                    {"label": "SLO breach", "value": "99.9% → 99.9%", "highlight": True},
                    {"label": "On-call burnout", "value": "NONE", "highlight": True},
                    {"label": "MTTR", "value": "3 minutes", "highlight": True},
                ],
            ),
            unsafe_allow_html=True,
        )

    spacer()

    # Impact summary
    st.markdown(
        f"""
    <div class='animate-fade-in' style='
        background: {GRADIENT_INFO};
        border-radius: {RADIUS_LG};
        padding: 32px;
        margin: 24px 0;
        box-shadow: {SHADOW_BASE};
    '>
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 16px;'>
            <span style='font-size: 28px;'>{ICONS["metric"]}</span>
            <h3 style='color: white; margin: 0;'>The Impact of Proper FinOps</h3>
        </div>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;'>
            <div style='
                background-color: rgba(255,255,255,0.1);
                border-radius: {RADIUS_BASE};
                padding: 16px;
                text-align: center;
            '>
                <div style='font-size: 24px; font-weight: {FONT_WEIGHT_BOLD}; color: white;'>4h 20m</div>
                <div style='font-size: 12px; color: rgba(255,255,255,0.8);'>Time saved per incident</div>
            </div>
            <div style='
                background-color: rgba(255,255,255,0.1);
                border-radius: {RADIUS_BASE};
                padding: 16px;
                text-align: center;
            '>
                <div style='font-size: 24px; font-weight: {FONT_WEIGHT_BOLD}; color: white;'>$127K</div>
                <div style='font-size: 12px; color: rgba(255,255,255,0.8);'>Revenue saved per incident</div>
            </div>
            <div style='
                background-color: rgba(255,255,255,0.1);
                border-radius: {RADIUS_BASE};
                padding: 16px;
                text-align: center;
            '>
                <div style='font-size: 24px; font-weight: {FONT_WEIGHT_BOLD}; color: white;'>340</div>
                <div style='font-size: 12px; color: rgba(255,255,255,0.8);'>Fewer customer tickets</div>
            </div>
            <div style='
                background-color: rgba(255,255,255,0.1);
                border-radius: {RADIUS_BASE};
                padding: 16px;
                text-align: center;
            '>
                <div style='font-size: 24px; font-weight: {FONT_WEIGHT_BOLD}; color: white;'>100%</div>
                <div style='font-size: 12px; color: rgba(255,255,255,0.8);'>SLO compliance</div>
            </div>
        </div>
        <p style='color: rgba(255,255,255,0.9); margin: 16px 0 0 0; text-align: center; font-size: 14px;'>
            These aren't theoretical numbers. This is the real-world impact of good FinOps practices.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    spacer()

    if action_button(
        "EXPLORE FINOPS DASHBOARD",
        key="to_dashboard",
        icon=ICONS["dashboard"],
        type="primary",
    ):
        advance_scene()
        st.rerun()


# =============================================================================
# SCENE 4.4: INTERACTIVE FINOPS DASHBOARD
# =============================================================================


def render_scene_4_4_finops_dashboard():
    """Scene 4.4: Interactive FinOps Dashboard — the single pane of glass."""

    st.markdown(f"### {ICONS['dashboard']} The FinOps Dashboard")
    st.caption(f"MTTR so far: {get_mttr_display()} | Revenue impact: {get_revenue_display()}")

    # Info banner
    st.markdown(
        f"""
    <div class='animate-fade-in' style='
        background-color: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: {RADIUS_BASE};
        padding: 16px;
        margin: 16px 0;
        display: flex;
        align-items: center;
        gap: 12px;
    '>
        <span style='font-size: 24px;'>{ICONS["info"]}</span>
        <div>
            <span style='color: {COLOR_INFO}; font-weight: {FONT_WEIGHT_SEMIBOLD};'>Single Pane of Glass</span>
            <br>
            <span style='color: {COLOR_TEXT_MUTED}; font-size: 14px;'>
                Ownership + Cost + Health + Environment — all linked together.
            </span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Service header with status
    st.markdown(f"### {ICONS['service']} Service: payment-api")

    # Top metric row
    cols = st.columns(5)
    dashboard_metrics = [
        {"label": "Owner", "value": "team-payments", "color": COLOR_SUCCESS, "icon": ICONS["team"]},
        {
            "label": "Cost/Month",
            "value": "$18,500",
            "color": COLOR_TEXT_PRIMARY,
            "icon": ICONS["cost"],
        },
        {"label": "Health", "value": "Critical", "color": COLOR_CRITICAL, "icon": ICONS["alert"]},
        {"label": "Environment", "value": "prod", "color": COLOR_INFO, "icon": ICONS["cluster"]},
        {"label": "SLO", "value": "94.2%", "color": COLOR_WARNING, "icon": ICONS["slo"]},
    ]

    for i, metric in enumerate(dashboard_metrics):
        with cols[i]:
            st.markdown(
                f"""
            <div class='hover-lift' style='
                background-color: {COLOR_BG_SURFACE};
                border: 1px solid {COLOR_BORDER};
                border-top: 3px solid {metric["color"]};
                border-radius: {RADIUS_BASE};
                padding: 16px;
                text-align: center;
            '>
                <div style='font-size: 20px; margin-bottom: 6px;'>{metric["icon"]}</div>
                <div style='font-size: 11px; color: {COLOR_TEXT_MUTED}; margin-bottom: 4px;'>{metric["label"]}</div>
                <div style='font-size: 18px; font-weight: {FONT_WEIGHT_BOLD}; color: {metric["color"]};'>{metric["value"]}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    st.divider()

    # Service Dependencies
    st.markdown(f"### {ICONS['org']} Service Dependencies")

    st.markdown(
        f"""
    <div style='
        background-color: {COLOR_BG_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-radius: {RADIUS_LG};
        padding: 32px;
        text-align: center;
    '>
        <div style='
            display: inline-block;
            background-color: {COLOR_BG_ELEVATED};
            border: 2px solid {COLOR_CRITICAL};
            border-radius: {RADIUS_BASE};
            padding: 16px 32px;
            margin-bottom: 16px;
        '>
            <div style='font-size: 18px; font-weight: {FONT_WEIGHT_BOLD}; color: {COLOR_TEXT_PRIMARY};'>
                {ICONS["service"]} payment-api
            </div>
            <div style='font-size: 12px; color: {COLOR_CRITICAL};'>Critical Service</div>
        </div>

        <div style='color: {COLOR_TEXT_MUTED}; font-size: 14px; margin: 12px 0;'>depends on ↑</div>

        <div style='display: flex; justify-content: center; gap: 16px; margin: 16px 0; flex-wrap: wrap;'>
            <div class='hover-lift' style='
                background-color: rgba(220, 38, 38, 0.15);
                border: 1px solid rgba(220, 38, 38, 0.4);
                border-radius: {RADIUS_BASE};
                padding: 14px 24px;
                text-align: center;
                min-width: 120px;
            '>
                <div style='font-weight: {FONT_WEIGHT_SEMIBOLD}; color: {COLOR_TEXT_PRIMARY};'>order-service</div>
                <div style='font-size: 12px; color: {COLOR_CRITICAL};'>{ICONS["error"]} DOWN</div>
            </div>
            <div class='hover-lift' style='
                background-color: rgba(245, 158, 11, 0.15);
                border: 1px solid rgba(245, 158, 11, 0.4);
                border-radius: {RADIUS_BASE};
                padding: 14px 24px;
                text-align: center;
                min-width: 120px;
            '>
                <div style='font-weight: {FONT_WEIGHT_SEMIBOLD}; color: {COLOR_TEXT_PRIMARY};'>database</div>
                <div style='font-size: 12px; color: {COLOR_WARNING};'>{ICONS["warning"]} DEGRADED</div>
            </div>
            <div class='hover-lift' style='
                background-color: rgba(16, 185, 129, 0.15);
                border: 1px solid rgba(16, 185, 129, 0.4);
                border-radius: {RADIUS_BASE};
                padding: 14px 24px;
                text-align: center;
                min-width: 120px;
            '>
                <div style='font-weight: {FONT_WEIGHT_SEMIBOLD}; color: {COLOR_TEXT_PRIMARY};'>cache</div>
                <div style='font-size: 12px; color: {COLOR_SUCCESS};'>{ICONS["success"]} OK</div>
            </div>
        </div>

        <div style='color: {COLOR_TEXT_MUTED}; font-size: 14px; margin: 12px 0;'>called by ↓</div>

        <div style='display: flex; justify-content: center; gap: 16px; margin: 16px 0; flex-wrap: wrap;'>
            <div class='hover-lift' style='
                background-color: rgba(16, 185, 129, 0.15);
                border: 1px solid rgba(16, 185, 129, 0.4);
                border-radius: {RADIUS_BASE};
                padding: 14px 24px;
                text-align: center;
                min-width: 120px;
            '>
                <div style='font-weight: {FONT_WEIGHT_SEMIBOLD}; color: {COLOR_TEXT_PRIMARY};'>web-app</div>
                <div style='font-size: 12px; color: {COLOR_SUCCESS};'>{ICONS["success"]} OK</div>
            </div>
            <div class='hover-lift' style='
                background-color: rgba(16, 185, 129, 0.15);
                border: 1px solid rgba(16, 185, 129, 0.4);
                border-radius: {RADIUS_BASE};
                padding: 14px 24px;
                text-align: center;
                min-width: 120px;
            '>
                <div style='font-weight: {FONT_WEIGHT_SEMIBOLD}; color: {COLOR_TEXT_PRIMARY};'>mobile-app</div>
                <div style='font-size: 12px; color: {COLOR_SUCCESS};'>{ICONS["success"]} OK</div>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.divider()

    # Team Ownership & Contact Info
    st.markdown(f"### {ICONS['team']} Team Ownership")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
        <div class='animate-slide-in-left hover-lift' style='
            background-color: {COLOR_BG_SURFACE};
            border: 1px solid {COLOR_BORDER};
            border-left: 4px solid {COLOR_SUCCESS};
            border-radius: {RADIUS_BASE};
            padding: 24px;
            height: 100%;
        '>
            <h4 style='margin: 0 0 16px 0; color: {COLOR_TEXT_PRIMARY};'>
                {ICONS["team"]} Team: team-payments
            </h4>
            <table style='width: 100%; color: {COLOR_TEXT_SECONDARY}; font-size: 14px;'>
                <tr><td style='padding: 6px 0;'>Owner</td><td style='text-align: right; color: {COLOR_TEXT_PRIMARY};'>Sarah Payments</td></tr>
                <tr><td style='padding: 6px 0;'>Slack</td><td style='text-align: right; color: {COLOR_SUCCESS};'>#payments-oncall</td></tr>
                <tr><td style='padding: 6px 0;'>Rotation</td><td style='text-align: right; color: {COLOR_TEXT_PRIMARY};'>Payments Primary</td></tr>
                <tr><td style='padding: 6px 0;'>Service Catalog</td><td style='text-align: right; color: {COLOR_INFO};'>svc-pay-001</td></tr>
                <tr><td style='padding: 6px 0;'>Cost Center</td><td style='text-align: right; color: {COLOR_TEXT_PRIMARY};'>payments-revenue</td></tr>
                <tr><td style='padding: 6px 0;'>Monthly Spend</td><td style='text-align: right; color: {COLOR_TEXT_PRIMARY}; font-weight: {FONT_WEIGHT_BOLD};'>$18,500</td></tr>
            </table>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class='animate-slide-in-right hover-lift' style='
            background-color: {COLOR_BG_SURFACE};
            border: 1px solid {COLOR_BORDER};
            border-left: 4px solid {COLOR_INFO};
            border-radius: {RADIUS_BASE};
            padding: 24px;
            height: 100%;
        '>
            <h4 style='margin: 0 0 16px 0; color: {COLOR_TEXT_PRIMARY};'>
                {ICONS["contact"]} Contact Information
            </h4>
            <table style='width: 100%; color: {COLOR_TEXT_SECONDARY}; font-size: 14px;'>
                <tr><td style='padding: 6px 0;'>Email</td><td style='text-align: right; color: {COLOR_TEXT_PRIMARY};'>sarah.payments@company.com</td></tr>
                <tr><td style='padding: 6px 0;'>Slack</td><td style='text-align: right; color: {COLOR_SUCCESS};'>#payments-oncall</td></tr>
                <tr><td style='padding: 6px 0;'>Phone</td><td style='text-align: right; color: {COLOR_TEXT_PRIMARY};'>+1 (555) PAY-HELP</td></tr>
                <tr><td style='padding: 6px 0;'>On-Call Today</td><td style='text-align: right; color: {COLOR_TEXT_PRIMARY}; font-weight: {FONT_WEIGHT_BOLD};'>Sarah Payments</td></tr>
                <tr><td style='padding: 6px 0;'>Backup</td><td style='text-align: right; color: {COLOR_TEXT_PRIMARY};'>Mike Payments</td></tr>
            </table>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.divider()

    # Summary
    st.markdown(
        f"""
    <div class='animate-fade-in' style='
        background: {GRADIENT_SUCCESS};
        border-radius: {RADIUS_LG};
        padding: 32px;
        margin: 24px 0;
        box-shadow: {SHADOW_GLOW_SUCCESS};
    '>
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 16px;'>
            <span style='font-size: 28px;'>{ICONS["success"]}</span>
            <h3 style='color: white; margin: 0;'>Complete Ownership Information in One Place</h3>
        </div>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 16px;'>
            <div>
                <p style='color: rgba(255,255,255,0.9); font-weight: {FONT_WEIGHT_SEMIBOLD}; margin: 0 0 8px 0;'>No more:</p>
                <ul style='color: rgba(255,255,255,0.8); margin: 0; padding-left: 20px; font-size: 14px; line-height: 1.8;'>
                    <li>Searching through Slack threads</li>
                    <li>Navigating outdated org charts</li>
                    <li>Wasting time on cost reports</li>
                    <li>Escalating through multiple levels</li>
                </ul>
            </div>
            <div>
                <p style='color: rgba(255,255,255,0.9); font-weight: {FONT_WEIGHT_SEMIBOLD}; margin: 0 0 8px 0;'>Everything is:</p>
                <ul style='color: rgba(255,255,255,0.8); margin: 0; padding-left: 20px; font-size: 14px; line-height: 1.8;'>
                    <li><strong>Accurate</strong> — tags are validated</li>
                    <li><strong>Up-to-date</strong> — synced with service catalog</li>
                    <li><strong>Complete</strong> — all attributes present</li>
                    <li><strong>Accessible</strong> — single dashboard</li>
                </ul>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Key practices
    st.markdown(
        f"""
    <div class='animate-fade-in' style='
        background-color: {COLOR_BG_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-radius: {RADIUS_BASE};
        padding: 24px;
        margin: 16px 0;
    '>
        <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 12px;'>
            <span style='font-size: 20px;'>{ICONS["lightbulb"]}</span>
            <span style='color: {COLOR_TEXT_PRIMARY}; font-weight: {FONT_WEIGHT_SEMIBOLD};'>Key FinOps Practices Demonstrated</span>
        </div>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px;'>
            <div style='
                background-color: {COLOR_BG_ELEVATED};
                border-radius: {RADIUS_BASE};
                padding: 14px;
            '>
                <div style='font-size: 14px; font-weight: {FONT_WEIGHT_SEMIBOLD}; color: {COLOR_SUCCESS}; margin-bottom: 4px;'>
                    {ICONS["label"]} Consistent Labeling
                </div>
                <div style='font-size: 12px; color: {COLOR_TEXT_MUTED};'>All resources have the same ownership tags</div>
            </div>
            <div style='
                background-color: {COLOR_BG_ELEVATED};
                border-radius: {RADIUS_BASE};
                padding: 14px;
            '>
                <div style='font-size: 14px; font-weight: {FONT_WEIGHT_SEMIBOLD}; color: {COLOR_INFO}; margin-bottom: 4px;'>
                    {ICONS["service"]} Service Catalog
                </div>
                <div style='font-size: 12px; color: {COLOR_TEXT_MUTED};'>Every service has an entry with owner and contact</div>
            </div>
            <div style='
                background-color: {COLOR_BG_ELEVATED};
                border-radius: {RADIUS_BASE};
                padding: 14px;
            '>
                <div style='font-size: 14px; font-weight: {FONT_WEIGHT_SEMIBOLD}; color: {COLOR_WARNING}; margin-bottom: 4px;'>
                    {ICONS["cost"]} Cost Attribution
                </div>
                <div style='font-size: 12px; color: {COLOR_TEXT_MUTED};'>100% of resources are tagged and allocated</div>
            </div>
            <div style='
                background-color: {COLOR_BG_ELEVATED};
                border-radius: {RADIUS_BASE};
                padding: 14px;
            '>
                <div style='font-size: 14px; font-weight: {FONT_WEIGHT_SEMIBOLD}; color: {COLOR_TEXT_PRIMARY}; margin-bottom: 4px;'>
                    {ICONS["dashboard"]} Single Source of Truth
                </div>
                <div style='font-size: 12px; color: {COLOR_TEXT_MUTED};'>All information in one accessible dashboard</div>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    spacer()

    if action_button(
        "PLAY AGAIN",
        key="play_again",
        icon=ICONS["restart"],
        type="primary",
    ):
        st.session_state.reset = True
        st.rerun()
