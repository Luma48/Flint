import re
from typing import Dict, List, Tuple, Optional, Callable

# Project Imports
from managers.Resource_Manager import get_resource

# =====================================================================
# Icon Tag Mapping
# =====================================================================
TAG_ICON_MAP: Dict[str, str] = {
    "PAD_A": "Packaged_Resources/Images/Icons/Icon_A.png",
    "PAD_1": "Packaged_Resources/Images/Icons/Icon_One.png",
    "PAD_2": "Packaged_Resources/Images/Icons/Icon_Two.png",
    "PAD_PLUS": "Packaged_Resources/Images/Icons/Icon_Plus.png",
    "PAD_MINUS": "Packaged_Resources/Images/Icons/Icon_Minus.png",
    "PAD": "Packaged_Resources/Images/Icons/Icon_Pad.png",
    "WAIT": "Packaged_Resources/Images/Icons/Icon_Wait.png",
    "HM": "Packaged_Resources/Images/Icons/Icon_Heart.png",
    "DYNAMIC": "Packaged_Resources/Images/Icons/Icon_Dynamic.png",
    "SHAKE": "Packaged_Resources/Images/Icons/Icon_Shake.png",
    "WAVE": "Packaged_Resources/Images/Icons/Icon_Wave.png",
}

TAG_HTML_MAP: Dict[str, str] = {
    # "wave": "<div style='color: red;'>",
}

# =====================================================================
# Helpers
# =====================================================================
def _img_tag(path: str, size: int) -> str:
    return f'<img src="{path}" height="{size}">'

def _span_color(r: int, g: int, b: int) -> str:
    return f'<span style="color: rgb({r},{g},{b});">'

def _span_fontsize(size: int) -> str:
    return f'<span style="font-size: {size}px;">'

def _icon_with_value(icon_key: str, base_font_size: int, value: Optional[int] = None) -> str:
    icon_img = _img_tag(get_resource(TAG_ICON_MAP[icon_key]), base_font_size)
    if value is not None:
        return f"{icon_img}<span style='color: gray;'>{value}</span>"
    return icon_img

# =====================================================================
# Main renderer
# =====================================================================
def render_text_with_tags(
    text: str,
    base_font_size: int,
    persistent_color: Optional[Tuple[int, int, int]] = None
) -> str:

    scale_stack: List[int] = []
    color_stack: List[Tuple[int, int, int]] = []
    center_stack: List[bool] = []

    # Persistent color wrapper
    html_prefix, html_suffix = "", ""
    if persistent_color:
        r, g, b = persistent_color
        html_prefix = _span_color(r, g, b)
        html_suffix = "</span>"

    # Special character replacements
    specials = {
        "Þ": "Packaged_Resources/Images/Icons/Icon_Star.png",
        "®": "Packaged_Resources/Images/Icons/Icon_Arrow_Left.png",
    }
    for char, path in specials.items():
        text = text.replace(char, _img_tag(get_resource(path), base_font_size))

    # =================================================================
    # Dispatcher functions for each tag
    # =================================================================
    def handle_icon(parts: List[str]) -> str:
        if len(parts) < 2:
            return f"<{' '.join(parts)}>"
        icon = parts[1]
        if icon in TAG_ICON_MAP:
            return _img_tag(get_resource(TAG_ICON_MAP[icon]), base_font_size)
        return f"<{' '.join(parts)}>"

    def handle_scale(parts: List[str]) -> str:
        if len(parts) == 2:
            try:
                factor = float(parts[1])
                scaled = int(base_font_size * factor * 0.5)
                scale_stack.append(scaled)
                return _span_fontsize(scaled)
            except ValueError:
                pass
        return f"<{' '.join(parts)}>"

    def handle_endscale(_: List[str]) -> str:
        if scale_stack:
            scale_stack.pop()
        return "</span>"

    def handle_wait(parts: List[str]) -> str:
        if len(parts) == 2:
            try:
                wait_time = int(parts[1])
                img = _img_tag(get_resource(TAG_ICON_MAP["WAIT"]), base_font_size)
                return f"{img}<span style='color: gray;'>{wait_time}ms</span>"
            except ValueError:
                pass
        return f"<{' '.join(parts)}>"

    def handle_col(parts: List[str]) -> str:
        if len(parts) == 2 and len(parts[1]) == 8:
            try:
                r, g, b = (int(parts[1][i:i+2], 16) for i in (0, 2, 4))
                color_stack.append((r, g, b))
                return _span_color(r, g, b)
            except ValueError:
                pass
        return f"<{' '.join(parts)}>"

    def handle_endcol(_: List[str]) -> str:
        if color_stack:
            color_stack.pop()
        return "</span>"

    def handle_center(_: List[str]) -> str:
        center_stack.append(True)
        if color_stack:
            r, g, b = color_stack[-1]
            return f'</span><div style="text-align:center;">{_span_color(r,g,b)}'
        elif persistent_color:
            r, g, b = persistent_color
            return f'<div style="text-align:center;">{_span_color(r,g,b)}'
        return '<div style="text-align:center;">'

    def handle_endcenter(_: List[str]) -> str:
        if center_stack:
            center_stack.pop()
            if color_stack:
                r, g, b = color_stack[-1]
                return f'</span></div>{_span_color(r,g,b)}'
            elif persistent_color:
                r, g, b = persistent_color
                return f'</span></div>{_span_color(r,g,b)}'
        return "</div>"

    # ---- Generic tag handler factory for similar icon-value pairs ----
    def make_icon_value_handler(icon_key: str) -> Callable[[List[str]], str]:
        def handler(parts: List[str]) -> str:
            value = None
            if len(parts) == 2:
                try:
                    value = int(parts[1])
                except ValueError:
                    pass
            return _icon_with_value(icon_key, base_font_size, value)
        return handler

    # =================================================================
    # Tag dispatcher mapping
    # =================================================================
    tag_handlers: Dict[str, Callable[[List[str]], str]] = {
        "icon": handle_icon,
        "scale": handle_scale,
        "/scale": handle_endscale,
        "wait": handle_wait,
        "col": handle_col,
        "/col": handle_endcol,
        "center": handle_center,
        "/center": handle_endcenter,
        "dynamic": make_icon_value_handler("DYNAMIC"),
        "/dynamic": make_icon_value_handler("DYNAMIC"),
        "shake": make_icon_value_handler("SHAKE"),
        "/shake": make_icon_value_handler("SHAKE"),
        "wave": make_icon_value_handler("WAVE"),
        "/wave": make_icon_value_handler("WAVE"),
    }

    # =================================================================
    # Regex replacement
    # =================================================================
    def repl(match: re.Match) -> str:
        tag_content = match.group(1).strip()
        parts = tag_content.split()
        key = parts[0].lower()

        if key in tag_handlers:
            return tag_handlers[key](parts)
        if tag_content in TAG_HTML_MAP:
            return TAG_HTML_MAP[tag_content]
        return match.group(0)

    html_body = re.sub(r"<([^>]+)>", repl, text)

    # Close any unclosed color spans
    while color_stack:
        color_stack.pop()
        html_body += "</span>"

    return f"{html_prefix}{html_body}{html_suffix}"