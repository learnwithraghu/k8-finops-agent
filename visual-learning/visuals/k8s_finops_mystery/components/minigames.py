"""Mini-Games for The K8s Mystery

This module contains interactive educational mini-games that reinforce
FinOps learning objectives through hands-on problem-solving.
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
    action_button,
    tag,
    divider,
    spacer,
)


# =============================================================================
# LABEL DETECTIVE MINI-GAME
# =============================================================================

LABEL_GAME_DATA = {
    "service_name": "payment-api",
    "namespace": "team-a-prod",
    "current_labels": {
        "app": "payment-api",
        "version": "v2.3.1",
        "owner": "unknown",
        "cost-center": "legacy",
        "team": "NOT SET",
        "contact": "NOT SET",
        "oncall-slack": "NOT SET",
        "service-catalog-id": "NOT SET",
    },
    "correct_labels": {
        "owner": "team-payments",
        "cost-center": "payments-revenue",
        "team": "payments",
        "contact": "sarah.payments@company.com",
        "oncall-slack": "#payments-oncall",
        "service-catalog-id": "svc-pay-001",
    },
    "explanations": {
        "owner": "Every resource must have a clear owner team for incident response.",
        "cost-center": "Cost attribution ensures the right budget is charged.",
        "team": "Team name enables quick Slack channel lookup.",
        "contact": "Direct contact for the on-call engineer.",
        "oncall-slack": "Slack channel for immediate escalation.",
        "service-catalog-id": "Links the resource to the central service catalog.",
    },
    "wrong_options": {
        "owner": ["team-backend", "team-platform", "tbd"],
        "cost-center": ["legacy", "operations", "platform-infra"],
        "team": ["backend", "platform", "NOT SET"],
        "contact": ["john.smith@company.com", "oncall@company.com", "NOT SET"],
        "oncall-slack": ["#general", "#backend-oncall", "NOT SET"],
        "service-catalog-id": ["svc-001", "unknown", "NOT SET"],
    },
}


def init_label_game_state():
    """Initialize session state for the label detective game."""
    if "label_game_fixed" not in st.session_state:
        st.session_state.label_game_fixed = {}
    if "label_game_attempts" not in st.session_state:
        st.session_state.label_game_attempts = 0
    if "label_game_score" not in st.session_state:
        st.session_state.label_game_score = 0


def reset_label_game():
    """Reset the label detective game state."""
    st.session_state.label_game_fixed = {}
    st.session_state.label_game_attempts = 0
    st.session_state.label_game_score = 0


def render_label_detective(integration_mode: str = "inline"):
    """Render the Label Detective mini-game.

    Args:
        integration_mode: How the game is integrated:
            - "inline": Embedded within an act scene (shows compact version)
            - "standalone": Full-screen mini-game experience
    """
    init_label_game_state()

    data = LABEL_GAME_DATA
    fixed = st.session_state.label_game_fixed

    # Header
    st.markdown(
        f"""
    <div class='animate-fade-in' style='
        background: {GRADIENT_INFO};
        border-radius: {RADIUS_LG};
        padding: 24px;
        margin: 16px 0;
        box-shadow: {SHADOW_BASE};
    '>
        <div style='display: flex; align-items: center; gap: 12px;'>
            <span style='font-size: 32px;'>{ICONS["search"]}</span>
            <div>
                <h2 style='color: white; margin: 0;'>Label Detective</h2>
                <p style='color: rgba(255,255,255,0.9); margin: 4px 0 0 0;'>
                    Fix the broken labels to identify the service owner.
                </p>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Progress
    total_labels = len(data["correct_labels"])
    fixed_count = len(fixed)
    progress = fixed_count / total_labels

    st.progress(progress, text=f"Labels fixed: {fixed_count}/{total_labels}")

    # Score display
    if st.session_state.label_game_score > 0:
        st.markdown(
            f"""
        <div style='
            text-align: center;
            margin: 8px 0;
        '>
            <span style='
                background-color: rgba(16, 185, 129, 0.15);
                color: {COLOR_SUCCESS};
                border: 1px solid rgba(16, 185, 129, 0.3);
                border-radius: 9999px;
                padding: 4px 16px;
                font-size: 14px;
                font-weight: {FONT_WEIGHT_SEMIBOLD};
            '>
                {ICONS["star"]} Score: {st.session_state.label_game_score}
            </span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    col1, col2 = st.columns([1, 1])

    with col1:
        # Current manifest
        st.markdown(f"#### {ICONS['pod']} Current Pod Manifest")

        manifest_rows = ""
        for key, value in data["current_labels"].items():
            if key in fixed:
                # Fixed label — show in green
                correct_value = data["correct_labels"][key]
                manifest_rows += f"""
                <tr>
                    <td style='padding: 8px 0;'><code>{key}</code></td>
                    <td style='text-align: right; color: {COLOR_SUCCESS}; font-weight: {FONT_WEIGHT_SEMIBOLD};'>
                        {correct_value} {ICONS["success"]}
                    </td>
                </tr>
                """
            else:
                # Broken label — show in red/orange
                is_bad = value.lower() in ["unknown", "not set", "tbd", "legacy"]
                color = COLOR_CRITICAL if is_bad else COLOR_WARNING
                manifest_rows += f"""
                <tr>
                    <td style='padding: 8px 0;'><code>{key}</code></td>
                    <td style='text-align: right; color: {color};'>{value}</td>
                </tr>
                """

        st.markdown(
            f"""
        <div style='
            background-color: {COLOR_BG_SURFACE};
            border: 1px solid {COLOR_BORDER};
            border-radius: {RADIUS_BASE};
            padding: 20px;
        '>
            <div style='font-size: 12px; color: {COLOR_TEXT_MUTED}; margin-bottom: 8px;'>
                Namespace: {data["namespace"]} | Pod: {data["service_name"]}-7d9f4b8c5-x2v9p
            </div>
            <table style='width: 100%; color: {COLOR_TEXT_SECONDARY}; font-size: 14px;'>
                {manifest_rows}
            </table>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        # Fix panel
        st.markdown(f"#### {ICONS['label']} Fix Labels")

        if fixed_count < total_labels:
            # Find next unfixed label
            next_label = None
            for key in data["correct_labels"]:
                if key not in fixed:
                    next_label = key
                    break

            if next_label:
                st.markdown(
                    f"""
                <div style='
                    background-color: rgba(245, 158, 11, 0.1);
                    border: 1px solid rgba(245, 158, 11, 0.3);
                    border-radius: {RADIUS_BASE};
                    padding: 12px;
                    margin-bottom: 12px;
                '>
                    <span style='color: {COLOR_WARNING}; font-size: 14px;'>
                        {ICONS["warning"]} Fix <code>{next_label}</code>
                    </span>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # Generate options: 1 correct + 3 wrong
                correct = data["correct_labels"][next_label]
                wrongs = data["wrong_options"][next_label]
                options = [correct] + wrongs[:3]
                # Shuffle
                import random

                random.shuffle(options)

                st.markdown(
                    f"""
                <p style='color: {COLOR_TEXT_SECONDARY}; font-size: 14px; margin: 0 0 8px 0;'>
                    Choose the correct value for <strong>{next_label}</strong>:
                </p>
                """,
                    unsafe_allow_html=True,
                )

                for opt in options:
                    icon = ICONS["check"] if opt == correct else ICONS["cancel"]
                    if st.button(
                        f"{opt}",
                        key=f"label_opt_{next_label}_{opt}",
                        use_container_width=True,
                    ):
                        st.session_state.label_game_attempts += 1
                        if opt == correct:
                            st.session_state.label_game_fixed[next_label] = True
                            st.session_state.label_game_score += 100
                            st.success(f"Correct! {data['explanations'][next_label]}")
                        else:
                            st.session_state.label_game_score = max(
                                0, st.session_state.label_game_score - 25
                            )
                            st.error(f"Wrong! '{opt}' is incorrect. Try again.")
                        st.rerun()
        else:
            # All fixed!
            st.markdown(
                f"""
            <div class='animate-fade-in' style='
                background: {GRADIENT_SUCCESS};
                border-radius: {RADIUS_LG};
                padding: 24px;
                text-align: center;
                box-shadow: {SHADOW_BASE};
            '>
                <div style='font-size: 48px; margin-bottom: 12px;'>{ICONS["success"]}</div>
                <h3 style='color: white; margin: 0 0 8px 0;'>All Labels Fixed!</h3>
                <p style='color: rgba(255,255,255,0.9); margin: 0;'>
                    Final Score: <strong>{st.session_state.label_game_score}</strong>
                </p>
                <p style='color: rgba(255,255,255,0.8); font-size: 14px; margin: 8px 0 0 0;'>
                    You identified the owner in seconds instead of hours.
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )

            st.session_state.minigames_completed["label_detective"] = True

            if integration_mode == "standalone":
                if action_button(
                    "CONTINUE",
                    key="label_game_continue",
                    icon=ICONS["arrow_forward"],
                    type="primary",
                ):
                    reset_label_game()
                    # Return to caller to handle navigation
                    return "complete"
            else:
                st.markdown(
                    f"""
                <div style='
                    background-color: rgba(16, 185, 129, 0.1);
                    border: 1px solid rgba(16, 185, 129, 0.3);
                    border-radius: {RADIUS_BASE};
                    padding: 16px;
                    margin: 16px 0;
                    text-align: center;
                '>
                    <span style='color: {COLOR_SUCCESS}; font-weight: {FONT_WEIGHT_SEMIBOLD};'>
                        {ICONS["success"]} Mini-game complete! You can now continue the story.
                    </span>
                </div>
                """,
                    unsafe_allow_html=True,
                )

    # Educational sidebar for standalone mode
    if integration_mode == "standalone":
        spacer()
        st.markdown(
            f"""
        <div style='
            background-color: {COLOR_BG_SURFACE};
            border: 1px solid {COLOR_BORDER};
            border-radius: {RADIUS_BASE};
            padding: 20px;
        '>
            <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 12px;'>
                <span style='font-size: 20px;'>{ICONS["book"]}</span>
                <span style='color: {COLOR_TEXT_PRIMARY}; font-weight: {FONT_WEIGHT_SEMIBOLD};'>Why Labels Matter</span>
            </div>
            <ul style='color: {COLOR_TEXT_SECONDARY}; font-size: 14px; margin: 0; padding-left: 20px; line-height: 1.8;'>
                <li><strong>owner</strong>: Who to contact during incidents</li>
                <li><strong>cost-center</strong>: Budget attribution and chargeback</li>
                <li><strong>team</strong>: Quick team/Slack lookup</li>
                <li><strong>contact</strong>: Direct on-call engineer</li>
                <li><strong>oncall-slack</strong>: Escalation channel</li>
                <li><strong>service-catalog-id</strong>: Link to docs and dependencies</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    return "playing" if fixed_count < total_labels else "complete"


# =============================================================================
# COST ALLOCATION PUZZLE (Future expansion)
# =============================================================================


def render_cost_allocation_puzzle():
    """Placeholder for the Cost Allocation Puzzle mini-game."""
    st.info("""
    :material/construction: **Cost Allocation Puzzle**
    
    Coming soon! This mini-game will let you drag untagged resources into
the correct team buckets and watch the cloud bill "light up" as attribution improves.
    """)


# =============================================================================
# ESCALATION LADDER (Future expansion)
# =============================================================================


def render_escalation_ladder():
    """Placeholder for the Escalation Ladder mini-game."""
    st.info("""
    :material/construction: **Escalation Ladder**
    
    Coming soon! Race against the clock to find the right owner.
    With FinOps: 1 click. Without: 8 clicks and dead ends.
    """)
