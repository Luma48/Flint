import re
from typing import List, Tuple, Optional
from managers.Debug_Manager import debug

# Project Imports
from renderer.models.bubble_block import BubbleBlock

#===================================================================================================================================
# SPM Text parser (for your viewing pleasure)                                                                                                    
#===================================================================================================================================
# Helper function to remove plain text Linefeeds 
def _clean_line(line: str) -> str:
    cleaned = line.replace("[LF]", "").strip()
    if cleaned.lower() in {"<p>"}:
        return ""
    return cleaned


# =====================================================================
# Stage Token System (Pattern, Finding and Validation) 
# =====================================================================
# Core Stage Token Pattern
_STAGE_TOKEN_PATTERN = r"(?:anna_)?(?:stg|teki|peach|kaisou|opening|pro|shop|he|mi|ta|sp|gn|wa|an|ls)\d*_[^\[\]<\s]+"

# Finding Stage Tokens from Raw Input (Starts with [NUL] or string start)
_STAGE_TOKEN_RE = re.compile(
    rf"(?:^|\[NUL\])\s*({_STAGE_TOKEN_PATTERN})\s*(?:\[NUL\])?",
    flags=re.IGNORECASE,
)

# Validating if a line is exactly a Stage Token
_STAGE_LINE_RE = re.compile(
    rf"^{_STAGE_TOKEN_PATTERN}$",
    flags=re.IGNORECASE,
)

# =====================================================================
# Tokenize Function from raw
# =====================================================================
def _tokenize_lines(visible_text: str) -> List[str]:
    raw_lines = visible_text.splitlines()
    tokens: List[str] = []

    debug.debug("Starting tokenization. Total lines: %d", len(raw_lines))

    for line_index, raw in enumerate(raw_lines, start=1):
        cleaned = _clean_line(raw)
        debug.debug("Line %d: '%s' -> Cleaned: '%s'", line_index, raw, cleaned)
        if not cleaned:
            debug.debug("Line %d is empty after cleaning. Skipping.", line_index)
            continue

        # Repeatedly cut out stage tokens that occur only at start or after [NUL]
        pos = 0
        for match in _STAGE_TOKEN_RE.finditer(cleaned):
            prefix = cleaned[pos:match.start()].strip()
            stage_id = match.group(1)

            if prefix:
                tokens.append(prefix)

            debug.debug("Line %d stage token: '%s'", line_index, stage_id)
            tokens.append(stage_id.strip())

            pos = match.end()

        # Potential trailing text as final token
        tail = cleaned[pos:].strip()
        if tail:
            tokens.append(tail)

    debug.debug("Tokenization complete. Total tokens: %d", len(tokens))
    debug.debug("All tokens collected: %s", tokens)
    return tokens

# =====================================================================
# Page join helper (Inline tags remain inline with no extra newlines ; Dialogue/text lines are separated with \n.
# =====================================================================
INLINE_TAGS = ("<col", "</col", "<center", "</center", "<icon", "</icon>", "<select", "</select>", "<dynamic", "</dynamic", "<shake", "</shake", "<wait", "</wait", "<scale", "</scale>", "<wave", "</wave>")

def _join_page_lines(lines: List[str]) -> str:
    if not lines:
        return ""

    result_parts = []
    for line in lines:
        stripped = line.strip()

        # Inline tags stay inline
        if stripped.startswith(INLINE_TAGS):
            result_parts.append(stripped)
        else:
            # If the last item was an inline tag, don't force a newline
            if result_parts and result_parts[-1].startswith(INLINE_TAGS):
                result_parts.append(stripped)
            else:
                if result_parts:
                    result_parts.append("\n" + stripped)
                else:
                    result_parts.append(stripped)

    return "".join(result_parts).strip()


# =====================================================================
# Parsing function
# =====================================================================
def parse_spm_text(visible_text: str) -> List[BubbleBlock]:
    lines = _tokenize_lines(visible_text)
    bubbles: List[BubbleBlock] = []
    i = 0

    debug.debug("Starting parse_spm_text. Total tokenized lines: %d", len(lines))

    def is_stage_line(line: str) -> bool:
        return bool(_STAGE_LINE_RE.fullmatch(line.strip()))
    
    _BUBBLE_TAGS = {"diary", "system", "fairy", "kanban", "fairy2", "housou", "majo", "adv", "clear", "small"}
    
    def _parse_position(line: str, tag: str) -> Optional[Tuple[int, int, int, int]]:
        m = re.match(
            fr"<{tag}\s+(-?\d+)\s+(-?\d+)\s+(\d+)\s+(\d+)>",
            line,
            flags=re.IGNORECASE,
        )
        return tuple(map(int, m.groups())) if m else None

    while i < len(lines):
        if not is_stage_line(lines[i]):
            i += 1
            continue

        stage_npc = lines[i].strip()
        i += 1

        bubble_type = "none"
        bubble_sound = "none"
        position = (0, 0, 0, 0)

        # Read multiple tag lines immediately after stage token
        while i < len(lines) and lines[i].startswith("<") and not lines[i].lower().startswith("<p"):
            inner_line = lines[i].lower().strip()

            # Handle sound tags
            if inner_line.startswith("<se 1>"):
                bubble_sound = "Typewriter"
                i += 1
                continue
            elif inner_line.startswith("<se 2>"):
                bubble_sound = "Pencil"
                i += 1
                continue

            # Handle bubble types
            matched_type = False
            for tag in _BUBBLE_TAGS:
                if inner_line.startswith(f"<{tag}>"):
                    bubble_type = tag
                    remainder = lines[i][len(f"<{tag}>") :].strip()
                    i += 1
                    if remainder:
                        lines.insert(i, remainder)
                    matched_type = True
                    break
            if matched_type:
                continue

            # Handle <select> and <adv_select>
            for select_tag in ("select", "adv_select"):
                if inner_line.startswith(f"<{select_tag}"):
                    bubble_type = select_tag
                    pos = _parse_position(lines[i], select_tag)
                    if pos:
                        position = pos
                    i += 1
                    matched_type = True
                    break
            if matched_type:
                continue

            # Handle <wpos> anywhere in these lines
            if inner_line.startswith("<wpos"):
                pos = _parse_position(lines[i], "wpos")
                if pos:
                    position = pos
                i += 1
                continue

            # If none matched, break out of tag scanning
            break

        # Collect pages, <k> splits pages, <p> ignored
        pages: List[str] = []
        page_buf: List[str] = []
        while i < len(lines) and not is_stage_line(lines[i]):
            line = lines[i]
            if line.startswith("<k>"):
                if page_buf:
                    pages.append(_join_page_lines(page_buf))
                    page_buf = []
            else:
                page_buf.append(line)
            i += 1
        if page_buf:
            pages.append(_join_page_lines(page_buf))

        # Store parsed bubble
        bubbles.append(BubbleBlock(stage_npc, bubble_type, position, pages, bubble_sound))

    debug.info("Parsing complete. Total bubbles: %d", len(bubbles))
    return bubbles