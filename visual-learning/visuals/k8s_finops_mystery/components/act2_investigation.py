"""Act 2: The Investigation Deepens

This module renders the scenes for Act 2 where the player tries multiple
avenues to find the service owner, experiencing frustration at each turn.
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
    GRADIENT_WARNING,
    SHADOW_BASE,
    SHADOW_SM,
    RADIUS_BASE,
    RADIUS_LG,
    SPACE_BASE,
    SPACE_LG,
    SPACE_XL,
    TEXT_SM,
    TEXT_BASE,
    TEXT_LG,
    TEXT_XL,
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
    tag,
    divider,
    spacer,
)
from components.state_manager import (
    add_mttr,
    get_mttr_display,
    get_revenue_display,
    TEAMS,
    ORG_CHART,
    COST_DATA,
    advance_scene,
    advance_act,
)


def render_act2():
    """Render Act 2: The Investigation Deepens"""
    scene = st.session_state.current_scene

    if scene == 0:
        render_scene_2_1_slack_chaos()
    elif scene == 1:
        render_scene_2_2_org_chart()
    elif scene == 2:
        render_scene_2_3_cost_report()
    elif scene == 3:
        render_scene_2_4_escalation()
    else:
        advance_act()
        st.rerun()


def render_scene_2_1_slack_chaos():
    """Scene 2.1: Slack Chaos - Pinging teams"""

    st.markdown(f"### {ICONS['slack']} Slack Investigation")
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
        <span style='color: {COLOR_WARNING};'>Since labels don't help, you start messaging teams on Slack...</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(f"### {ICONS['team']} Contact Teams")
    st.write(
        "Click on team channels to ask if they own payment-api. Each wrong guess adds 10 minutes."
    )

    # Team cards grid
    team_cols = st.columns(3)
    for i, team in enumerate(TEAMS):
        with team_cols[i % 3]:
            team_name = team["name"]
            slack_channel = team["slack"]

            if team_name in st.session_state.teams_contacted:
                # Already contacted - show result
                if "payment-api" in team["owns"]:
                    st.markdown(
                        f"""
                    <div style='
                        background-color: rgba(16, 185, 129, 0.1);
                        border: 1px solid rgba(16, 185, 129, 0.3);
                        border-radius: {RADIUS_BASE};
                        padding: 16px;
                        text-align: center;
                        margin-bottom: 12px;
                    '>
                        <div style='font-size: 24px; margin-bottom: 8px;'>{ICONS["success"]}</div>
                        <div style='font-weight: {FONT_WEIGHT_SEMIBOLD}; color: {COLOR_SUCCESS};'>{team_name}</div>
                        <div style='font-size: 12px; color: {COLOR_TEXT_MUTED}; margin: 4px 0;'>{slack_channel}</div>
                        <div style='font-size: 13px; color: {COLOR_SUCCESS};'>YES! We own payment-api!</div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
                    <div style='
                        background-color: rgba(220, 38, 38, 0.1);
                        border: 1px solid rgba(220, 38, 38, 0.3);
                        border-radius: {RADIUS_BASE};
                        padding: 16px;
                        text-align: center;
                        margin-bottom: 12px;
                    '>
                        <div style='font-size: 24px; margin-bottom: 8px;'>{ICONS["error"]}</div>
                        <div style='font-weight: {FONT_WEIGHT_SEMIBOLD}; color: {COLOR_TEXT_PRIMARY};'>{team_name}</div>
                        <div style='font-size: 12px; color: {COLOR_TEXT_MUTED}; margin: 4px 0;'>{slack_channel}</div>
                        <div style='font-size: 13px; color: {COLOR_CRITICAL};'>Not ours</div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
            else:
                # Not yet contacted - show button
                if st.button(
                    f"{ICONS['message']} Message {slack_channel}",
                    key=f"team_{i}",
                    use_container_width=True,
                ):
                    st.session_state.teams_contacted.append(team_name)
                    if "payment-api" not in team["owns"]:
                        add_mttr(10)
                    st.rerun()

    # Progress
    contacted_count = len(st.session_state.teams_contacted)
    st.progress(
        contacted_count / len(TEAMS), text=f"Teams contacted: {contacted_count}/{len(TEAMS)}"
    )

    # Check if owner found
    owner_found = any(
        "payment-api" in team["owns"]
        for team in TEAMS
        if team["name"] in st.session_state.teams_contacted
    )

    if owner_found:
        st.markdown(
            f"""
        <div style='
            background-color: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: {RADIUS_BASE};
            padding: 20px;
            margin: 16px 0;
        '>
            <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 12px;'>
                <span style='font-size: 24px;'>{ICONS["success"]}</span>
                <span style='color: {COLOR_SUCCESS}; font-weight: {FONT_WEIGHT_SEMIBOLD}; font-size: 18px;'>FOUND!</span>
            </div>
            <p style='color: {COLOR_TEXT_SECONDARY}; margin: 0;'>
                <strong style='color: {COLOR_TEXT_PRIMARY};'>team-payments</strong> owns payment-api!
            </p>
            <p style='color: {COLOR_TEXT_MUTED}; margin: 8px 0 0 0; font-size: 14px; font-style: italic;'>
                "We took over payment-api last quarter during the reorg, but the labels were never updated. Sorry about that!"
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        spacer()

        if action_button(
            "CONTINUE", key="continue_from_slack", icon=ICONS["arrow_forward"], type="primary"
        ):
            advance_scene()
            st.rerun()

    elif contacted_count >= 3:
        st.markdown(
            f"""
        <div style='
            background-color: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: {RADIUS_BASE};
            padding: 16px;
            margin: 16px 0;
            display: flex;
            align-items: center;
            gap: 12px;
        '>
            <span style='font-size: 20px;'>{ICONS["lightbulb"]}</span>
            <div>
                <span style='color: {COLOR_INFO};'>You've contacted several teams but haven't found the owner yet.</span>
                <br>
                <span style='color: {COLOR_TEXT_MUTED}; font-size: 14px;'>This is taking too long. Maybe try checking the org chart or cost reports?</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button(
            f"{ICONS['arrow_forward']} SKIP TO ORG CHART",
            key="skip_to_org",
            type="secondary",
            use_container_width=True,
        ):
            add_mttr(30)
            advance_scene()
            st.rerun()


def render_scene_2_2_org_chart():
    """Scene 2.2: The Org Chart Hunt"""

    st.markdown(f"### {ICONS['org']} Organizational Chart Hunt")
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
        <span style='color: {COLOR_WARNING};'>The Slack search is slow. Let's check the org chart...</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Org restructure info
    st.markdown(
        f"""
    <div style='
        background-color: {COLOR_BG_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-radius: {RADIUS_BASE};
        padding: 20px;
        margin: 16px 0;
    '>
        <h4 style='margin: 0 0 12px 0; color: {COLOR_TEXT_PRIMARY};'>{ICONS["info"]} Org Chart Reality</h4>
        <p style='color: {COLOR_TEXT_SECONDARY}; margin: 0 0 12px 0;'>
            Your company has undergone <strong style='color: {COLOR_TEXT_PRIMARY};'>3 restructurings</strong> in the past 18 months:
        </p>
        <ul style='color: {COLOR_TEXT_SECONDARY}; margin: 0 0 12px 0;'>
            <li>Q1 2023: Platform team split into Infrastructure & SRE</li>
            <li>Q3 2023: Backend team reorganized into Payments & Fulfillment</li>
            <li>Q1 2024: Frontend & Mobile merged into Product Engineering</li>
        </ul>
        <div style='
            background-color: rgba(245, 158, 11, 0.1);
            border-radius: 6px;
            padding: 10px;
            font-size: 13px;
            color: {COLOR_WARNING};
        '>
            {ICONS["warning"]} Many services still have old team labels from previous org structures.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("### Navigate the Org Chart")
    st.write("Click through the hierarchy to find who might own payment-api.")

    # Org chart navigation
    current_level = st.session_state.get("org_level", "CTO")

    st.markdown(f"**Current view: {current_level}**")

    if current_level in ORG_CHART:
        reports = ORG_CHART[current_level]["reports"]
        knows = ORG_CHART[current_level]["knows_about"]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**{ICONS['person']} Direct Reports:**")
            for report in reports:
                if st.button(f"{ICONS['arrow_forward']} {report}", key=f"org_{report}"):
                    st.session_state.org_level = report
                    add_mttr(8)
                    st.rerun()

        with col2:
            st.markdown(f"**{ICONS['team']} Known Teams:**")
            if knows:
                for team in knows:
                    owns_payment = "payment-api" in next(
                        (t["owns"] for t in TEAMS if t["name"] == team), []
                    )
                    if owns_payment:
                        st.markdown(f"{ICONS['success']} **{team}** (owns payment-api!)")
                    else:
                        st.markdown(f"{ICONS['team']} {team}")
            else:
                st.caption("No direct team knowledge at this level.")
    else:
        # At leaf node
        team = current_level
        st.markdown(f"**Reached: {team}**")

        team_data = next((t for t in TEAMS if t["name"] == team), None)
        if team_data:
            if "payment-api" in team_data["owns"]:
                st.markdown(f"{ICONS['success']} **{team} owns payment-api!**")
            else:
                st.markdown(f"{ICONS['error']} **{team} does NOT own payment-api.**")
                st.caption(f"They own: {', '.join(team_data['owns'])}")

    spacer()

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            f"{ICONS['refresh']} RESET ORG CHART", type="secondary", use_container_width=True
        ):
            st.session_state.org_level = "CTO"
            st.rerun()

    with col2:
        if action_button(
            "CONTINUE TO COST REPORTS", key="to_cost", icon=ICONS["arrow_forward"], type="primary"
        ):
            advance_scene()
            st.rerun()


def render_scene_2_3_cost_report():
    """Scene 2.3: The Cost Report Dead End"""

    st.markdown(f"### {ICONS['cost']} Cloud Cost Investigation")
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
        <span style='color: {COLOR_WARNING};'>Let's check if cost attribution can help us find the owner...</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Cost metrics
    st.markdown("### Monthly Cloud Spend")

    cols = st.columns(3)
    with cols[0]:
        st.markdown(
            f"""
        <div style='
            background-color: {COLOR_BG_SURFACE};
            border: 1px solid {COLOR_BORDER};
            border-radius: {RADIUS_BASE};
            padding: 20px;
            text-align: center;
        '>
            <div style='font-size: 12px; color: {COLOR_TEXT_MUTED}; margin-bottom: 4px;'>Total Monthly</div>
            <div style='font-size: 28px; font-weight: {FONT_WEIGHT_BOLD}; color: {COLOR_TEXT_PRIMARY};'>${COST_DATA["total_monthly"]:,}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with cols[1]:
        st.markdown(
            f"""
        <div style='
            background-color: {COLOR_BG_SURFACE};
            border: 1px solid {COLOR_BORDER};
            border-left: 4px solid {COLOR_CRITICAL};
            border-radius: {RADIUS_BASE};
            padding: 20px;
            text-align: center;
        '>
            <div style='font-size: 12px; color: {COLOR_TEXT_MUTED}; margin-bottom: 4px;'>Untagged</div>
            <div style='font-size: 28px; font-weight: {FONT_WEIGHT_BOLD}; color: {COLOR_CRITICAL};'>${COST_DATA["untagged"]:,}</div>
            <div style='font-size: 12px; color: {COLOR_CRITICAL};'>60%</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with cols[2]:
        st.markdown(
            f"""
        <div style='
            background-color: {COLOR_BG_SURFACE};
            border: 1px solid {COLOR_BORDER};
            border-radius: {RADIUS_BASE};
            padding: 20px;
            text-align: center;
        '>
            <div style='font-size: 12px; color: {COLOR_TEXT_MUTED}; margin-bottom: 4px;'>Tagged</div>
            <div style='font-size: 28px; font-weight: {FONT_WEIGHT_BOLD}; color: {COLOR_SUCCESS};'>${COST_DATA["tagged"]:,}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Cost chart
    import pandas as pd

    cost_df = pd.DataFrame(
        {
            "Team": list(COST_DATA["by_team"].keys()),
            "Spend": list(COST_DATA["by_team"].values()),
        }
    )

    st.bar_chart(cost_df.set_index("Team"), use_container_width=True)

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
            <span style='color: {COLOR_CRITICAL}; font-weight: {FONT_WEIGHT_SEMIBOLD}; font-size: 18px;'>COST REPORT IS USELESS</span>
        </div>
        <p style='color: {COLOR_TEXT_SECONDARY}; margin: 0 0 12px 0;'>
            60% of resources are untagged! The payment-api service falls into the "unallocated" bucket.
        </p>
        <p style='color: {COLOR_TEXT_SECONDARY}; margin: 0;'>Without proper cost attribution tags, you cannot:</p>
        <ul style='color: {COLOR_TEXT_SECONDARY}; margin: 8px 0 0 0;'>
            <li>Identify which team owns the resource</li>
            <li>Attribute costs to the right budget</li>
            <li>Find the right escalation path</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # What FinOps would fix
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
            <span style='color: {COLOR_INFO}; font-weight: {FONT_WEIGHT_SEMIBOLD};'>With FinOps cost allocation:</span>
        </div>
        <ul style='color: {COLOR_TEXT_SECONDARY}; margin: 0;'>
            <li><code>cost-center</code> = actual business unit</li>
            <li><code>team</code> = owning team</li>
            <li><code>environment</code> = prod/staging/dev</li>
            <li><code>service</code> = service catalog ID</li>
        </ul>
        <p style='color: {COLOR_TEXT_MUTED}; margin: 12px 0 0 0; font-size: 14px;'>
            You'd see payment-api clearly attributed to team-payments with $18K/month spend.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    spacer()

    if action_button(
        "CONTINUE TO ESCALATION", key="to_escalation", icon=ICONS["arrow_forward"], type="primary"
    ):
        add_mttr(20)
        advance_scene()
        st.rerun()


def render_scene_2_4_escalation():
    """Scene 2.4: Escalation Roulette"""

    st.markdown(f"### {ICONS['escalation']} Escalation Roulette")
    st.caption(f"MTTR: {get_mttr_display()} | Revenue impact: {get_revenue_display()}")

    st.markdown(
        f"""
    <div style='
        background-color: rgba(220, 38, 38, 0.1);
        border: 1px solid rgba(220, 38, 38, 0.3);
        border-radius: {RADIUS_BASE};
        padding: 16px;
        margin: 16px 0;
        display: flex;
        align-items: center;
        gap: 12px;
    '>
        <span style='font-size: 20px;'>{ICONS["error"]}</span>
        <span style='color: {COLOR_CRITICAL};'>You've been searching for over an hour. Time to escalate...</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    escalation_levels = [
        {
            "level": 1,
            "role": "Team Lead",
            "time": 15,
            "result": "Doesn't know. Suggests checking with Platform team.",
        },
        {
            "level": 2,
            "role": "Engineering Manager",
            "time": 20,
            "result": "Thinks it might be Backend team, but not sure since reorg.",
        },
        {
            "level": 3,
            "role": "Director of Engineering",
            "time": 30,
            "result": "Remembers payment services moved to new Payments team last quarter.",
        },
        {
            "level": 4,
            "role": "VP of Engineering",
            "time": 45,
            "result": "Confirms: team-payments owns it now. But labels were never updated!",
        },
    ]

    current_escalation = st.session_state.escalation_level

    if current_escalation < len(escalation_levels):
        level = escalation_levels[current_escalation]

        # Show escalation path visualization
        st.markdown("### Escalation Path")

        path_html = "<div style='display: flex; align-items: center; gap: 8px; margin-bottom: 20px; flex-wrap: wrap;'>"
        for i, esc in enumerate(escalation_levels):
            if i < current_escalation:
                path_html += f"""
                <div style='
                    background-color: rgba(220, 38, 38, 0.2);
                    border: 1px solid rgba(220, 38, 38, 0.4);
                    border-radius: 9999px;
                    padding: 6px 16px;
                    font-size: 12px;
                    color: {COLOR_CRITICAL};
                '>{esc["role"]}</div>
                """
                if i < len(escalation_levels) - 1:
                    path_html += (
                        f"<span style='color: {COLOR_CRITICAL};'>{ICONS['arrow_forward']}</span>"
                    )
            elif i == current_escalation:
                path_html += f"""
                <div style='
                    background: {GRADIENT_WARNING};
                    border-radius: 9999px;
                    padding: 6px 16px;
                    font-size: 12px;
                    color: white;
                    font-weight: {FONT_WEIGHT_SEMIBOLD};
                    box-shadow: {SHADOW_BASE};
                '>{esc["role"]} ← Current</div>
                """
                if i < len(escalation_levels) - 1:
                    path_html += (
                        f"<span style='color: {COLOR_WARNING};'>{ICONS['arrow_forward']}</span>"
                    )
            else:
                path_html += f"""
                <div style='
                    background-color: {COLOR_BG_SURFACE};
                    border: 1px solid {COLOR_BORDER};
                    border-radius: 9999px;
                    padding: 6px 16px;
                    font-size: 12px;
                    color: {COLOR_TEXT_MUTED};
                '>{esc["role"]}</div>
                """
                if i < len(escalation_levels) - 1:
                    path_html += (
                        f"<span style='color: {COLOR_TEXT_MUTED};'>{ICONS['arrow_forward']}</span>"
                    )
        path_html += "</div>"

        st.markdown(path_html, unsafe_allow_html=True)

        # Current escalation card
        st.markdown(
            f"""
        <div style='
            background-color: {COLOR_BG_SURFACE};
            border: 1px solid {COLOR_BORDER};
            border-left: 4px solid {COLOR_WARNING};
            border-radius: {RADIUS_BASE};
            padding: 24px;
            margin: 16px 0;
        '>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>
                <span style='font-size: 18px; font-weight: {FONT_WEIGHT_SEMIBOLD}; color: {COLOR_TEXT_PRIMARY};'>
                    Escalation Level {level["level"]}: {level["role"]}
                </span>
                <span style='
                    background-color: rgba(245, 158, 11, 0.2);
                    color: {COLOR_WARNING};
                    border-radius: 9999px;
                    padding: 4px 12px;
                    font-size: 12px;
                '>+{level["time"]} min</span>
            </div>
            <p style='color: {COLOR_TEXT_SECONDARY}; margin: 0; font-size: 16px;'>
                <strong style='color: {COLOR_TEXT_PRIMARY};'>Response:</strong> {level["result"]}
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        next_role = escalation_levels[min(current_escalation + 1, len(escalation_levels) - 1)][
            "role"
        ]

        if action_button(
            f"ESCALATE TO {next_role.upper()}",
            key=f"escalate_{current_escalation}",
            icon=ICONS["escalation"],
            type="primary",
        ):
            add_mttr(level["time"])
            st.session_state.escalation_level += 1
            st.rerun()
    else:
        # All escalations complete
        st.markdown(
            f"""
        <div style='
            background-color: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: {RADIUS_BASE};
            padding: 24px;
            margin: 16px 0;
        '>
            <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 16px;'>
                <span style='font-size: 32px;'>{ICONS["success"]}</span>
                <span style='color: {COLOR_SUCCESS}; font-weight: {FONT_WEIGHT_SEMIBOLD}; font-size: 24px;'>FINALLY FOUND!</span>
            </div>
            <p style='color: {COLOR_TEXT_SECONDARY}; margin: 0 0 12px 0;'>
                After escalating all the way to VP of Engineering:
            </p>
            <ul style='color: {COLOR_TEXT_SECONDARY}; margin: 0 0 16px 0;'>
                <li><strong style='color: {COLOR_TEXT_PRIMARY};'>Owner:</strong> team-payments</li>
                <li><strong style='color: {COLOR_TEXT_PRIMARY};'>Reason for confusion:</strong> Service migrated during Q3 reorg, labels never updated</li>
                <li><strong style='color: {COLOR_TEXT_PRIMARY};'>Total time wasted:</strong> 4+ hours of escalation</li>
            </ul>
            <div style='
                background-color: rgba(220, 38, 38, 0.1);
                border-radius: 8px;
                padding: 12px;
                text-align: center;
            '>
                <span style='color: {COLOR_CRITICAL}; font-weight: {FONT_WEIGHT_SEMIBOLD};'>
                    {ICONS["warning"]} The actual fix (restarting a stuck pod) took 3 minutes.
                </span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        spacer()

        if action_button(
            "SEE THE CONSEQUENCES",
            key="to_consequences",
            icon=ICONS["arrow_forward"],
            type="primary",
        ):
            advance_scene()
            st.rerun()
