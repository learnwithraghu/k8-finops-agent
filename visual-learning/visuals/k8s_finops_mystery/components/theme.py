"""Centralized theme system for the K8s FinOps Mystery game.

This module defines a consistent design system including colors, spacing,
typography, and iconography used throughout the application.
"""

# =============================================================================
# COLOR PALETTE
# =============================================================================

# Semantic Colors (used for status indicators, alerts, etc.)
COLOR_CRITICAL = "#DC2626"  # Red-600 - errors, critical alerts, downtime
COLOR_WARNING = "#F59E0B"  # Amber-500 - warnings, degraded services
COLOR_SUCCESS = "#10B981"  # Emerald-500 - success, healthy, resolved
COLOR_INFO = "#3B82F6"  # Blue-500 - informational, neutral actions
COLOR_NEUTRAL = "#6B7280"  # Gray-500 - secondary text, disabled

# Background Colors
COLOR_BG_PAGE = "#0F172A"  # Slate-900 - main page background
COLOR_BG_SURFACE = "#1E293B"  # Slate-800 - cards, containers
COLOR_BG_ELEVATED = "#334155"  # Slate-700 - elevated elements, hover states
COLOR_BG_INPUT = "#1E293B"  # Slate-800 - input fields

# Text Colors
COLOR_TEXT_PRIMARY = "#F8FAFC"  # Slate-50 - headings, primary text
COLOR_TEXT_SECONDARY = "#94A3B8"  # Slate-400 - body text, descriptions
COLOR_TEXT_MUTED = "#64748B"  # Slate-500 - captions, metadata
COLOR_TEXT_ON_DARK = "#FFFFFF"  # White - text on colored backgrounds

# Border Colors
COLOR_BORDER = "#334155"  # Slate-700 - default borders
COLOR_BORDER_LIGHT = "#475569"  # Slate-600 - hover borders
COLOR_BORDER_FOCUS = "#3B82F6"  # Blue-500 - focused elements

# Gradient Definitions (for alerts, cards, etc.)
GRADIENT_CRITICAL = "linear-gradient(135deg, #DC2626 0%, #991B1B 100%)"
GRADIENT_WARNING = "linear-gradient(135deg, #F59E0B 0%, #D97706 100%)"
GRADIENT_SUCCESS = "linear-gradient(135deg, #10B981 0%, #059669 100%)"
GRADIENT_INFO = "linear-gradient(135deg, #3B82F6 0%, #2563EB 100%)"
GRADIENT_DARK = "linear-gradient(135deg, #1E293B 0%, #0F172A 100%)"

# =============================================================================
# SPACING SCALE (in pixels)
# =============================================================================

SPACE_XS = "4px"
SPACE_SM = "8px"
SPACE_MD = "12px"
SPACE_BASE = "16px"
SPACE_LG = "24px"
SPACE_XL = "32px"
SPACE_2XL = "48px"
SPACE_3XL = "64px"

# =============================================================================
# TYPOGRAPHY SCALE
# =============================================================================

FONT_FAMILY = "'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif"
FONT_MONO = "'JetBrains Mono', 'Fira Code', 'Consolas', monospace"

TEXT_XS = "12px"
TEXT_SM = "14px"
TEXT_BASE = "16px"
TEXT_LG = "18px"
TEXT_XL = "20px"
TEXT_2XL = "24px"
TEXT_3XL = "30px"
TEXT_4XL = "36px"

FONT_WEIGHT_NORMAL = "400"
FONT_WEIGHT_MEDIUM = "500"
FONT_WEIGHT_SEMIBOLD = "600"
FONT_WEIGHT_BOLD = "700"

LINE_HEIGHT_TIGHT = "1.2"
LINE_HEIGHT_NORMAL = "1.5"
LINE_HEIGHT_RELAXED = "1.75"

# =============================================================================
# BORDER RADIUS
# =============================================================================

RADIUS_SM = "6px"
RADIUS_BASE = "10px"
RADIUS_LG = "16px"
RADIUS_XL = "24px"
RADIUS_FULL = "9999px"

# =============================================================================
# SHADOWS
# =============================================================================

SHADOW_SM = "0 1px 2px 0 rgba(0, 0, 0, 0.3)"
SHADOW_BASE = "0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -1px rgba(0, 0, 0, 0.2)"
SHADOW_LG = "0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.3)"
SHADOW_GLOW_CRITICAL = "0 0 20px rgba(220, 38, 38, 0.4)"
SHADOW_GLOW_SUCCESS = "0 0 20px rgba(16, 185, 129, 0.4)"

# =============================================================================
# ICON MAP (Material Icons only - no emoji)
# =============================================================================

ICONS = {
    # Status
    "alert": ":material/warning:",
    "success": ":material/check_circle:",
    "error": ":material/error:",
    "info": ":material/info:",
    "critical": ":material/emergency:",
    "pending": ":material/hourglass_empty:",
    "warning": ":material/warning:",
    # Actions
    "search": ":material/search:",
    "restart": ":material/restart_alt:",
    "arrow_forward": ":material/arrow_forward:",
    "arrow_back": ":material/arrow_back:",
    "play": ":material/play_circle:",
    "refresh": ":material/refresh:",
    "ack": ":material/done_all:",
    "close": ":material/close:",
    "settings": ":material/settings:",
    # K8s / Infrastructure
    "pod": ":material/deployed_code:",
    "service": ":material/cloud:",
    "deployment": ":material/rocket_launch:",
    "namespace": ":material/folder:",
    "node": ":material/computer:",
    "cluster": ":material/hub:",
    "ingress": ":material/door_front:",
    "config": ":material/settings_applications:",
    "secret": ":material/lock:",
    # Business / Metrics
    "revenue": ":material/trending_up:",
    "cost": ":material/paid:",
    "money": ":material/attach_money:",
    "chart": ":material/assessment:",
    "dashboard": ":material/dashboard:",
    "metric": ":material/analytics:",
    "ticket": ":material/confirmation_number:",
    "customer": ":material/people:",
    "slo": ":material/speed:",
    # Communication
    "slack": ":material/chat:",
    "email": ":material/email:",
    "phone": ":material/phone:",
    "team": ":material/groups:",
    "person": ":material/person:",
    "contact": ":material/contacts:",
    "message": ":material/message:",
    # Time
    "time": ":material/schedule:",
    "timer": ":material/timer:",
    "clock": ":material/schedule:",
    "calendar": ":material/calendar_today:",
    "history": ":material/history:",
    "rewind": ":material/replay:",
    # Navigation
    "home": ":material/home:",
    "menu": ":material/menu:",
    "more": ":material/more_vert:",
    "expand": ":material/expand_more:",
    "collapse": ":material/expand_less:",
    # Game
    "game": ":material/sports_esports:",
    "trophy": ":material/emoji_events:",
    "star": ":material/star:",
    "heart": ":material/favorite:",
    "lightbulb": ":material/lightbulb:",
    "book": ":material/menu_book:",
    "label": ":material/label:",
    "tag": ":material/sell:",
    "escalation": ":material/escalator_warning:",
    "org": ":material/account_tree:",
    "compare": ":material/compare_arrows:",
    # Misc
    "rocket": ":material/rocket_launch:",
    "fire": ":material/local_fire_department:",
    "bug": ":material/bug_report:",
    "shield": ":material/security:",
    "lock": ":material/lock:",
    "unlock": ":material/lock_open:",
    "eye": ":material/visibility:",
    "edit": ":material/edit:",
    "delete": ":material/delete:",
    "add": ":material/add_circle:",
    "remove": ":material/remove_circle:",
    "check": ":material/check:",
    "cancel": ":material/cancel:",
    "help": ":material/help:",
    "link": ":material/link:",
    "open": ":material/open_in_new:",
    "download": ":material/download:",
    "upload": ":material/upload:",
    "filter": ":material/filter_list:",
    "sort": ":material/sort:",
    "search_advanced": ":material/manage_search:",
}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def get_status_color(status: str) -> str:
    """Get the color for a given status string."""
    status_map = {
        "critical": COLOR_CRITICAL,
        "error": COLOR_CRITICAL,
        "down": COLOR_CRITICAL,
        "failed": COLOR_CRITICAL,
        "warning": COLOR_WARNING,
        "degraded": COLOR_WARNING,
        "pending": COLOR_WARNING,
        "success": COLOR_SUCCESS,
        "healthy": COLOR_SUCCESS,
        "ok": COLOR_SUCCESS,
        "resolved": COLOR_SUCCESS,
        "info": COLOR_INFO,
        "neutral": COLOR_NEUTRAL,
    }
    return status_map.get(status.lower(), COLOR_NEUTRAL)


def get_status_icon(status: str) -> str:
    """Get the icon for a given status string."""
    status_map = {
        "critical": ICONS["critical"],
        "error": ICONS["error"],
        "down": ICONS["error"],
        "failed": ICONS["error"],
        "warning": ICONS["warning"],
        "degraded": ICONS["warning"],
        "pending": ICONS["pending"],
        "success": ICONS["success"],
        "healthy": ICONS["success"],
        "ok": ICONS["success"],
        "resolved": ICONS["success"],
        "info": ICONS["info"],
        "neutral": ICONS["info"],
    }
    return status_map.get(status.lower(), ICONS["info"])


def get_status_gradient(status: str) -> str:
    """Get the gradient for a given status string."""
    status_map = {
        "critical": GRADIENT_CRITICAL,
        "error": GRADIENT_CRITICAL,
        "down": GRADIENT_CRITICAL,
        "warning": GRADIENT_WARNING,
        "degraded": GRADIENT_WARNING,
        "success": GRADIENT_SUCCESS,
        "healthy": GRADIENT_SUCCESS,
        "resolved": GRADIENT_SUCCESS,
        "info": GRADIENT_INFO,
    }
    return status_map.get(status.lower(), GRADIENT_DARK)


# =============================================================================
# CSS GENERATION
# =============================================================================


def get_global_css() -> str:
    """Generate the global CSS stylesheet for the application."""
    return f"""
    <style>
        /* Import Inter font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Global Reset & Base Styles */
        .stApp {{
            background-color: {COLOR_BG_PAGE};
            color: {COLOR_TEXT_PRIMARY};
            font-family: {FONT_FAMILY};
        }}
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            color: {COLOR_TEXT_PRIMARY} !important;
            font-weight: {FONT_WEIGHT_SEMIBOLD};
            line-height: {LINE_HEIGHT_TIGHT};
            margin-bottom: {SPACE_BASE};
        }}
        
        h1 {{ font-size: {TEXT_3XL}; }}
        h2 {{ font-size: {TEXT_2XL}; }}
        h3 {{ font-size: {TEXT_XL}; }}
        h4 {{ font-size: {TEXT_LG}; }}
        
        p, li, td {{
            color: {COLOR_TEXT_SECONDARY};
            line-height: {LINE_HEIGHT_NORMAL};
        }}
        
        /* Links */
        a {{
            color: {COLOR_INFO};
            text-decoration: none;
            transition: color 0.2s ease;
        }}
        
        a:hover {{
            color: #60A5FA;
            text-decoration: underline;
        }}
        
        /* Code / Monospace */
        code {{
            font-family: {FONT_MONO};
            background-color: {COLOR_BG_ELEVATED};
            color: {COLOR_TEXT_PRIMARY};
            padding: 2px 6px;
            border-radius: {RADIUS_SM};
            font-size: {TEXT_SM};
        }}
        
        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {COLOR_BG_SURFACE};
            border-right: 1px solid {COLOR_BORDER};
        }}
        
        [data-testid="stSidebar"] .stMarkdown {{
            color: {COLOR_TEXT_SECONDARY};
        }}
        
        /* Buttons */
        .stButton > button {{
            background-color: {COLOR_INFO};
            color: {COLOR_TEXT_ON_DARK};
            border: none;
            border-radius: {RADIUS_BASE};
            padding: {SPACE_BASE} {SPACE_LG};
            font-weight: {FONT_WEIGHT_SEMIBOLD};
            font-size: {TEXT_BASE};
            transition: all 0.2s ease;
            box-shadow: {SHADOW_SM};
        }}
        
        .stButton > button:hover {{
            background-color: #2563EB;
            transform: translateY(-1px);
            box-shadow: {SHADOW_BASE};
        }}
        
        .stButton > button:active {{
            transform: translateY(0);
            box-shadow: {SHADOW_SM};
        }}
        
        .stButton > button[kind="secondary"] {{
            background-color: transparent;
            color: {COLOR_TEXT_SECONDARY};
            border: 1px solid {COLOR_BORDER};
        }}
        
        .stButton > button[kind="secondary"]:hover {{
            background-color: {COLOR_BG_ELEVATED};
            border-color: {COLOR_BORDER_LIGHT};
            color: {COLOR_TEXT_PRIMARY};
        }}
        
        /* Primary button variant */
        .stButton > button[kind="primary"] {{
            background: {GRADIENT_INFO};
        }}
        
        /* Metric Cards */
        [data-testid="stMetric"] {{
            background-color: {COLOR_BG_SURFACE};
            border: 1px solid {COLOR_BORDER};
            border-radius: {RADIUS_BASE};
            padding: {SPACE_BASE};
        }}
        
        [data-testid="stMetricLabel"] {{
            color: {COLOR_TEXT_MUTED};
            font-size: {TEXT_SM};
            font-weight: {FONT_WEIGHT_MEDIUM};
        }}
        
        [data-testid="stMetricValue"] {{
            color: {COLOR_TEXT_PRIMARY};
            font-size: {TEXT_XL};
            font-weight: {FONT_WEIGHT_BOLD};
        }}
        
        [data-testid="stMetricDelta"] {{
            font-size: {TEXT_SM};
        }}
        
        /* Alerts */
        .stAlert {{
            border-radius: {RADIUS_BASE};
            border-left-width: 4px;
            padding: {SPACE_BASE};
        }}
        
        .stAlert [data-baseweb="notification"] {{
            border-radius: {RADIUS_BASE};
        }}
        
        /* Info alert */
        .stAlert.alert-info {{
            background-color: rgba(59, 130, 246, 0.1);
            border-left-color: {COLOR_INFO};
        }}
        
        /* Success alert */
        .stAlert.alert-success {{
            background-color: rgba(16, 185, 129, 0.1);
            border-left-color: {COLOR_SUCCESS};
        }}
        
        /* Warning alert */
        .stAlert.alert-warning {{
            background-color: rgba(245, 158, 11, 0.1);
            border-left-color: {COLOR_WARNING};
        }}
        
        /* Error alert */
        .stAlert.alert-error {{
            background-color: rgba(220, 38, 38, 0.1);
            border-left-color: {COLOR_CRITICAL};
        }}
        
        /* Progress Bar */
        .stProgress > div > div {{
            background-color: {COLOR_BG_ELEVATED};
            border-radius: {RADIUS_FULL};
        }}
        
        .stProgress > div > div > div {{
            background: {GRADIENT_INFO};
            border-radius: {RADIUS_FULL};
            transition: width 0.5s ease;
        }}
        
        /* Divider */
        hr {{
            border-color: {COLOR_BORDER};
            margin: {SPACE_LG} 0;
        }}
        
        /* Caption */
        .stCaption {{
            color: {COLOR_TEXT_MUTED};
            font-size: {TEXT_SM};
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background-color: {COLOR_BG_SURFACE};
            border: 1px solid {COLOR_BORDER};
            border-radius: {RADIUS_BASE};
            color: {COLOR_TEXT_PRIMARY};
            font-weight: {FONT_WEIGHT_MEDIUM};
        }}
        
        .streamlit-expanderContent {{
            background-color: {COLOR_BG_PAGE};
            border: 1px solid {COLOR_BORDER};
            border-top: none;
            border-radius: 0 0 {RADIUS_BASE} {RADIUS_BASE};
        }}
        
        /* Animations */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes slideInRight {{
            from {{ opacity: 0; transform: translateX(20px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        
        @keyframes slideInLeft {{
            from {{ opacity: 0; transform: translateX(-20px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        
        @keyframes pulse {{
            0%, 100% {{ box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.4); }}
            50% {{ box-shadow: 0 0 0 15px rgba(220, 38, 38, 0); }}
        }}
        
        @keyframes glow {{
            0%, 100% {{ box-shadow: 0 0 5px rgba(59, 130, 246, 0.3); }}
            50% {{ box-shadow: 0 0 20px rgba(59, 130, 246, 0.6); }}
        }}
        
        @keyframes countUp {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes spin {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}
        
        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            10%, 30%, 50%, 70%, 90% {{ transform: translateX(-5px); }}
            20%, 40%, 60%, 80% {{ transform: translateX(5px); }}
        }}
        
        @keyframes rewind {{
            0% {{ filter: hue-rotate(0deg) brightness(1); }}
            50% {{ filter: hue-rotate(180deg) brightness(0.5); }}
            100% {{ filter: hue-rotate(360deg) brightness(1); }}
        }}
        
        /* Animation utility classes */
        .animate-fade-in {{
            animation: fadeIn 0.4s ease-out forwards;
        }}
        
        .animate-slide-in-right {{
            animation: slideInRight 0.4s ease-out forwards;
        }}
        
        .animate-slide-in-left {{
            animation: slideInLeft 0.4s ease-out forwards;
        }}
        
        .animate-pulse {{
            animation: pulse 2s infinite;
        }}
        
        .animate-glow {{
            animation: glow 2s infinite;
        }}
        
        .animate-shake {{
            animation: shake 0.5s ease-in-out;
        }}
        
        .animate-spin {{
            animation: spin 1s linear infinite;
        }}
        
        .animate-rewind {{
            animation: rewind 1.5s ease-in-out;
        }}
        
        /* Card hover effect */
        .hover-lift {{
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .hover-lift:hover {{
            transform: translateY(-2px);
            box-shadow: {SHADOW_LG};
        }}
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {COLOR_BG_PAGE};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {COLOR_BORDER};
            border-radius: {RADIUS_FULL};
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {COLOR_BORDER_LIGHT};
        }}
        
        /* Responsive adjustments */
        @media (max-width: 768px) {{
            h1 {{ font-size: {TEXT_2XL}; }}
            h2 {{ font-size: {TEXT_XL}; }}
            h3 {{ font-size: {TEXT_LG}; }}
            
            .stButton > button {{
                width: 100%;
                margin-bottom: {SPACE_SM};
            }}
        }}
        
        /* Reduced motion preference */
        @media (prefers-reduced-motion: reduce) {{
            *, *::before, *::after {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
        }}
    </style>
    """


def get_card_css(
    border_color: str = COLOR_BORDER,
    background_color: str = COLOR_BG_SURFACE,
    padding: str = SPACE_BASE,
    border_radius: str = RADIUS_BASE,
    border_left_width: str = "4px",
    shadow: str = SHADOW_SM,
) -> str:
    """Generate CSS for a styled card."""
    return f"""
        background-color: {background_color};
        border: 1px solid {border_color};
        border-left: {border_left_width} solid {border_color};
        border-radius: {border_radius};
        padding: {padding};
        box-shadow: {shadow};
        transition: all 0.2s ease;
    """


def get_status_badge_css(status: str) -> str:
    """Generate CSS for a status badge."""
    color = get_status_color(status)
    return f"""
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background-color: {color}20;
        color: {color};
        border: 1px solid {color}40;
        border-radius: {RADIUS_FULL};
        padding: 4px 12px;
        font-size: {TEXT_SM};
        font-weight: {FONT_WEIGHT_MEDIUM};
    """
