"""
GUI Theme and Styling Configuration
Defines colors, fonts, and dimensions for Dark and Light modes.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ThemeColors:
    """Color palette definition for calculator themes."""
    name: str
    bg_window: str
    bg_card: str
    bg_display: str
    text_primary: str
    text_secondary: str
    text_accent: str
    
    # Button Colors
    btn_num_bg: str
    btn_num_hover: str
    btn_num_text: str
    
    btn_op_bg: str
    btn_op_hover: str
    btn_op_text: str
    
    btn_action_bg: str
    btn_action_hover: str
    btn_action_text: str
    
    btn_equal_bg: str
    btn_equal_hover: str
    btn_equal_text: str
    
    # History Sidebar
    history_bg: str
    history_item_bg: str
    history_item_hover: str
    history_border: str


DARK_THEME = ThemeColors(
    name="dark",
    bg_window="#18181b",         # Zinc 900
    bg_card="#27272a",           # Zinc 800
    bg_display="#202023",        # Charcoal display
    text_primary="#fafafa",      # White/light zinc
    text_secondary="#a1a1aa",    # Muted zinc 400
    text_accent="#818cf8",       # Indigo 400
    
    btn_num_bg="#2e2e33",        # Dark grey
    btn_num_hover="#3f3f46",     # Zinc 700
    btn_num_text="#fafafa",
    
    btn_op_bg="#383840",         # Slightly tinted operator
    btn_op_hover="#4c4c57",
    btn_op_text="#93c5fd",       # Soft blue accent text
    
    btn_action_bg="#383840",     # AC, DEL
    btn_action_hover="#4c4c57",
    btn_action_text="#f87171",   # Soft red/coral text
    
    btn_equal_bg="#6366f1",      # Premium Indigo accent
    btn_equal_hover="#4f46e5",   # Darker indigo on hover
    btn_equal_text="#ffffff",
    
    history_bg="#1f1f23",
    history_item_bg="#27272a",
    history_item_hover="#323238",
    history_border="#3f3f46",
)

LIGHT_THEME = ThemeColors(
    name="light",
    bg_window="#f4f4f5",         # Zinc 100
    bg_card="#ffffff",           # White card
    bg_display="#ffffff",
    text_primary="#18181b",      # Zinc 900
    text_secondary="#71717a",    # Zinc 500
    text_accent="#4f46e5",       # Indigo 600
    
    btn_num_bg="#ffffff",        # Clean white
    btn_num_hover="#e4e4e7",     # Zinc 200
    btn_num_text="#18181b",
    
    btn_op_bg="#e0e7ff",         # Light indigo tint
    btn_op_hover="#c7d2fe",
    btn_op_text="#3730a3",       # Deep indigo
    
    btn_action_bg="#fee2e2",     # Light red tint
    btn_action_hover="#fecaca",
    btn_action_text="#dc2626",   # Red text
    
    btn_equal_bg="#4f46e5",      # Vibrant Indigo
    btn_equal_hover="#4338ca",
    btn_equal_text="#ffffff",
    
    history_bg="#fafafa",
    history_item_bg="#ffffff",
    history_item_hover="#f4f4f5",
    history_border="#e4e4e7",
)

THEMES: Dict[str, ThemeColors] = {
    "dark": DARK_THEME,
    "light": LIGHT_THEME,
}
