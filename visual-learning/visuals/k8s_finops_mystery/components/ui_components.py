"""Reusable UI components for the K8s FinOps Mystery game.

This module provides consistent, styled components that can be used
across all scenes to maintain visual coherence.
"""

import streamlit as st
from components.theme import (
    COLOR_BG_SURFACE,
    COLOR_BG_ELEVATED,
    COLOR_BG_PAGE,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_MUTED,
    COLOR_BORDER,
    COLOR_BORDER_LIGHT,
    COLOR_CRITICAL,
    COLOR_WARNING,
    COLOR_SUCCESS,
    COLOR_INFO,
    COLOR_NEUTRAL,
    GRADIENT_CRITICAL,
    GRADIENT_WARNING,
    GRADIENT_SUCCESS,
    GRADIENT_INFO,
    GRADIENT_DARK,
    SHADOW_SM,
    SHADOW_BASE,
    SHADOW_LG,
    SHADOW_GLOW_CRITICAL,
    SHADOW_GLOW_SUCCESS,
    RADIUS_SM,
    RADIUS_BASE,
    RADIUS_LG,
    SPACE_XS,
    SPACE_SM,
    SPACE_MD,
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
    get_status_color,
    get_status_icon,
    get_status_gradient,
    get_card_css,
    get_status_badge_css,
    ICONS,
)


# =============================================================================
# LAYOUT COMPONENTS
# =============================================================================


def scene_container(content_func, animation: str = "fade-in"):
    """Wrap scene content in a container with animation."""
    st.markdown(f'<div class="animate-{animation}">', unsafe_allow_html=True)
    content_func()
    st.markdown("</div>", unsafe_allow_html=True)


def section_header(title: str, icon: str = "", caption: str = ""):
    """Render a consistent section header."""
    icon_str = f"{icon} " if icon else ""
    st.markdown(f"### {icon_str}{title}")
    if caption:
        st.caption(caption)


def metric_row(metrics: list, columns: int = None):
    """Render a row of metric cards.

    Args:
        metrics: List of dicts with keys: label, value, delta, delta_color, icon
        columns: Number of columns (defaults to len(metrics))
    """
    if columns is None:
        columns = len(metrics)

    cols = st.columns(columns)
    for i, metric in enumerate(metrics):
        with cols[i]:
            value = metric.get("value", "")
            label = metric.get("label", "")
            delta = metric.get("delta", None)
            delta_color = metric.get("delta_color", "normal")
            icon = metric.get("icon", "")

            # Build label with icon
            label_str = f"{icon} {label}" if icon else label

            if delta is not None:
                st.metric(label=label_str, value=value, delta=delta, delta_color=delta_color)
            else:
                st.metric(label=label_str, value=value)


# =============================================================================
# CARD COMPONENTS
# =============================================================================


def styled_card(
    content: str,
    title: str = "",
    status: str = "neutral",
    icon: str = "",
    extra_css: str = "",
    hover: bool = False,
) -> str:
    """Generate HTML for a styled card.

    Args:
        content: HTML content for the card body
        title: Optional card title
        status: Status level (critical, warning, success, info, neutral)
        icon: Material icon string
        extra_css: Additional CSS to apply
        hover: Whether to add hover lift effect
    """
    color = get_status_color(status)
    gradient = get_status_gradient(status)

    title_html = (
        f"<h4 style='margin: 0 0 {SPACE_SM} 0; color: {COLOR_TEXT_PRIMARY};'>{icon} {title}</h4>"
        if title
        else ""
    )

    hover_class = "hover-lift" if hover else ""

    return f"""
    <div class='{hover_class}' style='
        background-color: {COLOR_BG_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-left: 4px solid {color};
        border-radius: {RADIUS_BASE};
        padding: {SPACE_LG};
        box-shadow: {SHADOW_SM};
        margin-bottom: {SPACE_BASE};
        {extra_css}
    '>
        {title_html}
        {content}
    </div>
    """


def status_card(
    title: str,
    status: str,
    details: str = "",
    icon: str = "",
    metrics: dict = None,
) -> str:
    """Generate a status card with badge and optional metrics."""
    color = get_status_color(status)
    status_icon = get_status_icon(status)

    badge_css = get_status_badge_css(status)

    metrics_html = ""
    if metrics:
        metrics_rows = ""
        for key, value in metrics.items():
            metrics_rows += f"<tr><td style='color: {COLOR_TEXT_MUTED}; padding: 4px 0;'>{key}</td><td style='color: {COLOR_TEXT_PRIMARY}; text-align: right;'>{value}</td></tr>"
        metrics_html = (
            f"<table style='width: 100%; margin-top: {SPACE_BASE};'>{metrics_rows}</table>"
        )

    return f"""
    <div style='
        background-color: {COLOR_BG_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-left: 4px solid {color};
        border-radius: {RADIUS_BASE};
        padding: {SPACE_LG};
        box-shadow: {SHADOW_SM};
        margin-bottom: {SPACE_BASE};
    '>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: {SPACE_SM};'>
            <h4 style='margin: 0; color: {COLOR_TEXT_PRIMARY};'>{icon} {title}</h4>
            <span style='{badge_css}'>{status_icon} {status.upper()}</span>
        </div>
        <p style='color: {COLOR_TEXT_SECONDARY}; margin: 0;'>{details}</p>
        {metrics_html}
    </div>
    """


def info_card(title: str, content: str, icon: str = ICONS["info"]) -> str:
    """Generate an informational card."""
    return styled_card(
        content=f"<p style='margin: 0; color: {COLOR_TEXT_SECONDARY};'>{content}</p>",
        title=title,
        status="info",
        icon=icon,
    )


def alert_card(title: str, content: str, status: str = "warning") -> str:
    """Generate an alert card with appropriate styling."""
    color = get_status_color(status)
    icon = get_status_icon(status)

    return f"""
    <div style='
        background: {get_status_gradient(status)};
        border-radius: {RADIUS_BASE};
        padding: {SPACE_LG};
        margin: {SPACE_BASE} 0;
        box-shadow: {SHADOW_BASE};
    '>
        <h3 style='margin: 0 0 {SPACE_SM} 0; color: white;'>{icon} {title}</h3>
        <p style='margin: 0; color: rgba(255,255,255,0.9);'>{content}</p>
    </div>
    """


# =============================================================================
# SERVICE / RESOURCE CARDS
# =============================================================================


def service_card(
    name: str,
    status: str,
    namespace: str = "",
    error_rate: str = "",
    latency: str = "",
    owner: str = "",
    extra_details: str = "",
) -> str:
    """Generate a Kubernetes service/resource card."""
    color = get_status_color(status)
    icon = ICONS["service"] if "svc" in name.lower() else ICONS["pod"]

    details_html = ""
    if namespace:
        details_html += (
            f"<span style='color: {COLOR_TEXT_MUTED};'>Namespace: {namespace}</span><br>"
        )
    if error_rate:
        details_html += f"<span style='color: {COLOR_TEXT_MUTED};'>Error Rate: <span style='color: {color};'>{error_rate}</span></span><br>"
    if latency:
        details_html += f"<span style='color: {COLOR_TEXT_MUTED};'>Latency: {latency}</span><br>"
    if owner:
        owner_color = COLOR_SUCCESS if owner != "unknown" and owner != "NOT SET" else COLOR_CRITICAL
        details_html += f"<span style='color: {COLOR_TEXT_MUTED};'>Owner: <span style='color: {owner_color};'>{owner}</span></span>"
    if extra_details:
        details_html += f"<br><span style='color: {COLOR_TEXT_MUTED};'>{extra_details}</span>"

    badge_css = get_status_badge_css(status)

    return f"""
    <div class='hover-lift' style='
        background-color: {COLOR_BG_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-top: 4px solid {color};
        border-radius: {RADIUS_BASE};
        padding: {SPACE_LG};
        text-align: center;
        box-shadow: {SHADOW_SM};
        height: 100%;
    '>
        <div style='margin-bottom: {SPACE_SM};'>
            <span style='font-size: {TEXT_2XL};'>{icon}</span>
        </div>
        <h4 style='margin: 0 0 {SPACE_XS} 0; color: {COLOR_TEXT_PRIMARY};'>{name}</h4>
        <div style='margin-bottom: {SPACE_SM};'>
            <span style='{badge_css}'>{status.upper()}</span>
        </div>
        <div style='font-size: {TEXT_SM}; text-align: left;'>
            {details_html}
        </div>
    </div>
    """


# =============================================================================
# BUTTON COMPONENTS
# =============================================================================


def action_button(label: str, key: str, icon: str = "", type: str = "primary"):
    """Render a consistent action button."""
    label_str = f"{icon} {label}" if icon else label
    return st.button(label_str, key=key, type=type, use_container_width=True)


def nav_button(label: str, key: str, direction: str = "forward"):
    """Render a navigation button with appropriate icon."""
    icon = ICONS["arrow_forward"] if direction == "forward" else ICONS["arrow_back"]
    return action_button(label, key, icon, type="primary")


# =============================================================================
# TIMELINE COMPONENT
# =============================================================================


def timeline_item(
    time: str,
    event: str,
    elapsed: str = "",
    status: str = "neutral",
    is_last: bool = False,
) -> str:
    """Generate a timeline item."""
    color = get_status_color(status)
    icon = get_status_icon(status)

    elapsed_html = (
        f"<span style='color: {COLOR_TEXT_MUTED}; font-size: {TEXT_SM};'>({elapsed})</span>"
        if elapsed
        else ""
    )

    return f"""
    <div style='display: flex; gap: {SPACE_BASE}; margin-bottom: {SPACE_BASE};'>
        <div style='display: flex; flex-direction: column; align-items: center;'>
            <div style='
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background-color: {color};
                box-shadow: 0 0 8px {color}40;
                z-index: 1;
            '></div>
            {"" if is_last else f"<div style='width: 2px; flex: 1; background-color: {COLOR_BORDER};'></div>"}
        </div>
        <div style='flex: 1; padding-bottom: {SPACE_BASE};'>
            <div style='display: flex; align-items: center; gap: {SPACE_XS}; margin-bottom: 2px;'>
                <span style='color: {color};'>{icon}</span>
                <span style='font-weight: {FONT_WEIGHT_SEMIBOLD}; color: {COLOR_TEXT_PRIMARY};'>{time}</span>
                {elapsed_html}
            </div>
            <p style='margin: 0; color: {COLOR_TEXT_SECONDARY};'>{event}</p>
        </div>
    </div>
    """


def timeline_container(items: list):
    """Render a complete timeline from a list of items."""
    html = f"<div style='padding: {SPACE_BASE} 0;'>"
    for i, item in enumerate(items):
        html += timeline_item(
            time=item.get("time", ""),
            event=item.get("event", ""),
            elapsed=item.get("elapsed", ""),
            status=item.get("status", "neutral"),
            is_last=(i == len(items) - 1),
        )
    html += "</div>"
    return html


# =============================================================================
# COMPARISON COMPONENT
# =============================================================================


def comparison_card(
    title: str,
    items: list,
    status: str = "neutral",
) -> str:
    """Generate a comparison card (Before/After style).

    Args:
        title: Card title
        items: List of dicts with keys: label, value, highlight
        status: Overall status (affects border color)
    """
    color = get_status_color(status)

    rows_html = ""
    for item in items:
        label = item.get("label", "")
        value = item.get("value", "")
        highlight = item.get("highlight", False)

        value_color = color if highlight else COLOR_TEXT_PRIMARY
        weight = FONT_WEIGHT_BOLD if highlight else FONT_WEIGHT_MEDIUM

        rows_html += f"""
        <tr>
            <td style='color: {COLOR_TEXT_SECONDARY}; padding: {SPACE_SM} 0; border-bottom: 1px solid {COLOR_BORDER};'>{label}</td>
            <td style='color: {value_color}; font-weight: {weight}; text-align: right; padding: {SPACE_SM} 0; border-bottom: 1px solid {COLOR_BORDER};'>{value}</td>
        </tr>
        """

    return f"""
    <div style='
        background-color: {COLOR_BG_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-top: 4px solid {color};
        border-radius: {RADIUS_BASE};
        padding: {SPACE_LG};
        box-shadow: {SHADOW_BASE};
        height: 100%;
    '>
        <h3 style='text-align: center; margin: 0 0 {SPACE_LG} 0; color: {color};'>{title}</h3>
        <table style='width: 100%;'>
            {rows_html}
        </table>
    </div>
    """


# =============================================================================
# LABEL / TAG COMPONENTS
# =============================================================================


def tag(label: str, status: str = "neutral") -> str:
    """Generate a small tag/badge."""
    color = get_status_color(status)
    return f"""
    <span style='
        display: inline-block;
        background-color: {color}20;
        color: {color};
        border: 1px solid {color}40;
        border-radius: {RADIUS_FULL};
        padding: 2px 10px;
        font-size: {TEXT_SM};
        font-weight: {FONT_WEIGHT_MEDIUM};
        margin: 2px;
    '>{label}</span>
    """


def label_table(labels: dict, status: str = "neutral") -> str:
    """Generate a table of labels/tags.

    Args:
        labels: Dict of {label_name: label_value}
        status: Overall status (affects border)
    """
    color = get_status_color(status)

    rows_html = ""
    for key, value in labels.items():
        # Determine if value is "bad"
        is_bad = value.lower() in ["unknown", "not set", "tbd", "legacy", "deprecated"]
        value_color = COLOR_CRITICAL if is_bad else COLOR_SUCCESS

        rows_html += f"""
        <tr>
            <td style='padding: {SPACE_SM} 0;'><code>{key}</code></td>
            <td style='color: {value_color}; text-align: right;'>{value}</td>
        </tr>
        """

    return f"""
    <div style='
        background-color: {COLOR_BG_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-left: 4px solid {color};
        border-radius: {RADIUS_BASE};
        padding: {SPACE_LG};
    '>
        <table style='width: 100%; color: {COLOR_TEXT_SECONDARY};'>
            {rows_html}
        </table>
    </div>
    """


# =============================================================================
# SLACK / CHAT COMPONENTS
# =============================================================================


def slack_message(
    channel: str,
    sender: str,
    message: str,
    timestamp: str = "",
    is_reply: bool = False,
) -> str:
    """Generate a Slack-style message bubble."""
    indent = "margin-left: 40px;" if is_reply else ""

    return f"""
    <div style='
        background-color: {COLOR_BG_ELEVATED if is_reply else COLOR_BG_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-radius: {RADIUS_BASE};
        padding: {SPACE_BASE};
        margin-bottom: {SPACE_SM};
        {indent}
    '>
        <div style='display: flex; justify-content: space-between; margin-bottom: 4px;'>
            <span style='font-weight: {FONT_WEIGHT_SEMIBOLD}; color: {COLOR_INFO};'>@{sender}</span>
            <span style='font-size: {TEXT_SM}; color: {COLOR_TEXT_MUTED};'>{timestamp}</span>
        </div>
        <p style='margin: 0; color: {COLOR_TEXT_SECONDARY};'>{message}</p>
        <div style='margin-top: 4px;'>
            <span style='font-size: {TEXT_SM}; color: {COLOR_TEXT_MUTED};'>{ICONS["slack"]} {channel}</span>
        </div>
    </div>
    """


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def divider():
    """Render a styled divider."""
    st.markdown(
        f"""
    <hr style='
        border: none;
        border-top: 1px solid {COLOR_BORDER};
        margin: {SPACE_LG} 0;
    '>
    """,
        unsafe_allow_html=True,
    )


def spacer(height: str = SPACE_LG):
    """Add vertical spacing."""
    st.markdown(f"<div style='height: {height};'></div>", unsafe_allow_html=True)


def animated_counter(value: int, prefix: str = "", suffix: str = ""):
    """Render an animated counter that counts up."""
    st.markdown(
        f"""
    <div class='animate-fade-in' style='
        font-size: {TEXT_3XL};
        font-weight: {FONT_WEIGHT_BOLD};
        color: {COLOR_TEXT_PRIMARY};
        text-align: center;
        padding: {SPACE_LG};
    '>
        {prefix}{value:,}{suffix}
    </div>
    """,
        unsafe_allow_html=True,
    )
