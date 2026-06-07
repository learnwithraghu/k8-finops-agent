"""The K8s Mystery: FinOps Learning Game — Main Application

An interactive narrative-driven simulation demonstrating the real-world
impact of poor FinOps practices on Kubernetes operations.
"""

import streamlit as st

from components.theme import get_global_css, ICONS
from components.state_manager import init_game_state, reset_game
from components.act1_incident import render_act1
from components.act2_investigation import render_act2
from components.act3_revelation import render_act3
from components.act4_solution import render_act4

# Initialize game state on first run
init_game_state()

# Page configuration
st.set_page_config(
    page_title="The K8s Mystery: FinOps Learning Game",
    page_icon=":material/rocket_launch:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply global CSS
st.markdown(get_global_css(), unsafe_allow_html=True)

# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    # Game title in sidebar
    st.markdown(
        f"""
    <div style='text-align: center; margin-bottom: 16px;'>
        <div style='font-size: 32px; margin-bottom: 8px;'>{ICONS["rocket"]}</div>
        <h3 style='margin: 0; color: #F8FAFC;'>The K8s Mystery</h3>
        <p style='color: #94A3B8; font-size: 12px; margin: 4px 0 0 0;'>FinOps Learning Game</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.divider()

    # Progress section
    st.markdown(f"### {ICONS['game']} Progress")

    act_names = ["The Incident", "Investigation", "Revelation", "The Solution"]
    current_act = st.session_state.current_act

    # Progress bar
    progress = min((current_act * 3 + st.session_state.current_scene) / 12, 1.0)
    st.progress(progress, text=f"Act {current_act + 1} of 4")

    # Act indicators
    for i, name in enumerate(act_names):
        if i < current_act:
            st.markdown(f"{ICONS['success']} **{i + 1}. {name}**")
        elif i == current_act:
            st.markdown(f"{ICONS['arrow_forward']} **{i + 1}. {name}** ← Current")
        else:
            st.markdown(f"{ICONS['pending']} {i + 1}. {name}")

    st.divider()

    # Stats section
    st.markdown(f"### {ICONS['metric']} Live Stats")

    # MTTR with visual indicator
    mttr_minutes = st.session_state.mttr_minutes
    mttr_hours = mttr_minutes // 60
    mttr_mins = mttr_minutes % 60
    mttr_display = f"{mttr_hours}h {mttr_mins}m" if mttr_hours > 0 else f"{mttr_mins}m"

    # Color code MTTR based on severity
    if mttr_minutes > 240:
        mttr_color = "#DC2626"  # Critical
        mttr_icon = ICONS["critical"]
    elif mttr_minutes > 60:
        mttr_color = "#F59E0B"  # Warning
        mttr_icon = ICONS["warning"]
    else:
        mttr_color = "#10B981"  # OK
        mttr_icon = ICONS["success"]

    st.markdown(
        f"""
    <div style='
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 12px;
    '>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;'>
            <span style='color: #94A3B8; font-size: 12px;'>{ICONS["time"]} MTTR</span>
            <span style='color: {mttr_color};'>{mttr_icon}</span>
        </div>
        <div style='font-size: 24px; font-weight: 700; color: #F8FAFC;'>{mttr_display}</div>
        <div style='font-size: 11px; color: #64748B; margin-top: 2px;'>Time to resolve</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Revenue impact
    revenue = st.session_state.revenue_lost
    revenue_display = f"${revenue:,}"

    revenue_color = "#DC2626" if revenue > 50000 else "#F59E0B" if revenue > 10000 else "#10B981"

    st.markdown(
        f"""
    <div style='
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 12px;
    '>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;'>
            <span style='color: #94A3B8; font-size: 12px;'>{ICONS["cost"]} Revenue Impact</span>
            <span style='color: {revenue_color};'>{ICONS["money"]}</span>
        </div>
        <div style='font-size: 24px; font-weight: 700; color: {revenue_color};'>{revenue_display}</div>
        <div style='font-size: 11px; color: #64748B; margin-top: 2px;'>Lost revenue</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Investigation stats
    teams_contacted = len(st.session_state.teams_contacted)
    escalation = st.session_state.escalation_level

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
        <div style='
            background-color: #1E293B;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 10px;
            text-align: center;
        '>
            <div style='font-size: 20px;'>{ICONS["team"]}</div>
            <div style='font-size: 18px; font-weight: 700; color: #F8FAFC;'>{teams_contacted}</div>
            <div style='font-size: 10px; color: #64748B;'>Teams</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div style='
            background-color: #1E293B;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 10px;
            text-align: center;
        '>
            <div style='font-size: 20px;'>{ICONS["escalation"]}</div>
            <div style='font-size: 18px; font-weight: 700; color: #F8FAFC;'>{escalation}</div>
            <div style='font-size: 10px; color: #64748B;'>Escalations</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.divider()

    # Controls
    st.markdown(f"### {ICONS['settings']} Controls")

    if st.button(f"{ICONS['restart']} Restart Game", type="secondary", use_container_width=True):
        reset_game()
        st.rerun()

    st.markdown(
        f"""
    <div style='
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 12px;
        margin-top: 16px;
    '>
        <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 8px;'>
            <span style='font-size: 16px;'>{ICONS["info"]}</span>
            <span style='font-weight: 600; color: #F8FAFC; font-size: 14px;'>About</span>
        </div>
        <p style='color: #94A3B8; font-size: 12px; margin: 0; line-height: 1.5;'>
            Experience the real-world impact of poor FinOps practices on 
            Kubernetes incident response. Learn why proper labeling, cost 
            attribution, and service catalogs matter.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# =============================================================================
# MAIN CONTENT
# =============================================================================

# Header
st.markdown(
    f"""
<div style='text-align: center; margin-bottom: 8px;'>
    <div style='font-size: 48px; margin-bottom: 12px;'>{ICONS["rocket"]}</div>
    <h1 style='margin: 0; font-size: 36px;'>The K8s Mystery</h1>
    <p style='color: #94A3B8; font-size: 18px; margin: 8px 0 0 0;'>
        Experience the real-world pain of operating a large Kubernetes cluster 
        without proper FinOps practices.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

st.divider()

# Handle reset
if st.session_state.get("reset", False):
    reset_game()
    st.rerun()

# Game routing
if st.session_state.current_act == 0:
    render_act1()
elif st.session_state.current_act == 1:
    render_act2()
elif st.session_state.current_act == 2:
    render_act3()
elif st.session_state.current_act == 3:
    render_act4()
else:
    # Game complete screen
    st.markdown(
        f"""
    <div class='animate-fade-in' style='
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 2px solid #10B981;
        border-radius: 16px;
        padding: 48px;
        text-align: center;
        margin: 32px 0;
    '>
        <div style='font-size: 64px; margin-bottom: 16px;'>{ICONS["trophy"]}</div>
        <h1 style='color: #10B981; margin: 0 0 16px 0;'>Game Complete!</h1>
        <p style='color: #94A3B8; font-size: 18px; max-width: 600px; margin: 0 auto 24px auto; line-height: 1.6;'>
            You've experienced firsthand how poor FinOps practices can impact operational 
            efficiency, revenue, customer satisfaction, and team morale.
        </p>
        <div style='background-color: #0F172A; border-radius: 12px; padding: 24px; max-width: 500px; margin: 0 auto;'>
            <p style='color: #F8FAFC; font-weight: 600; margin: 0 0 12px 0;'>Key Takeaway</p>
            <p style='color: #94A3B8; margin: 0; font-size: 16px; line-height: 1.6;'>
                FinOps is not just about saving money — it's about enabling 
                efficient, reliable operations and reducing on-call burnout.
            </p>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("### What You Learned")

    lessons = [
        {
            "icon": ICONS["label"],
            "title": "1. Labels Matter",
            "description": "Proper Kubernetes labels are critical for ownership identification and incident response.",
            "color": "#10B981",
        },
        {
            "icon": ICONS["cost"],
            "title": "2. Cost Attribution",
            "description": "100% of resources should be tagged and allocated to the right team and cost center.",
            "color": "#3B82F6",
        },
        {
            "icon": ICONS["service"],
            "title": "3. Service Catalog",
            "description": "Every service needs an entry with owner, contact, dependencies, and documentation.",
            "color": "#F59E0B",
        },
        {
            "icon": ICONS["dashboard"],
            "title": "4. Single Source of Truth",
            "description": "All ownership information should be centralized, not scattered across tools.",
            "color": "#8B5CF6",
        },
    ]

    cols = st.columns(4)
    for i, lesson in enumerate(lessons):
        with cols[i]:
            st.markdown(
                f"""
            <div class='hover-lift' style='
                background-color: #1E293B;
                border: 1px solid #334155;
                border-top: 4px solid {lesson["color"]};
                border-radius: 12px;
                padding: 24px;
                text-align: center;
                height: 100%;
            '>
                <div style='font-size: 32px; margin-bottom: 12px;'>{lesson["icon"]}</div>
                <h4 style='color: {lesson["color"]}; margin: 0 0 8px 0; font-size: 16px;'>{lesson["title"]}</h4>
                <p style='color: #94A3B8; font-size: 13px; margin: 0; line-height: 1.5;'>{lesson["description"]}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

    st.divider()

    st.markdown(
        f"""
    <div style='
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 24px;
    '>
        <h3 style='margin: 0 0 16px 0;'>{ICONS["book"]} Next Steps</h3>
        <ul style='color: #94A3B8; margin: 0; padding-left: 20px; line-height: 2;'>
            <li>Implement proper Kubernetes labeling policies with validation</li>
            <li>Set up a service catalog (Backstage, ServiceNow, or custom)</li>
            <li>Enable automated cost attribution and tagging enforcement</li>
            <li>Create FinOps dashboards for visibility and accountability</li>
            <li>Train teams on FinOps best practices and ownership standards</li>
        </ul>
        <p style='color: #F8FAFC; font-weight: 600; margin: 16px 0 0 0; text-align: center;'>
            Remember: Good FinOps practices save money AND save time.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button(f"{ICONS['restart']} Play Again", type="primary", use_container_width=True):
        reset_game()
        st.rerun()
