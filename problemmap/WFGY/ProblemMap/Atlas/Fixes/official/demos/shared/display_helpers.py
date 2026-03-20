from __future__ import annotations

import json
from typing import Any, Mapping, Sequence


def _try_import_ipython_display():
    try:
        from IPython.display import Markdown, display  # type: ignore
        return display, Markdown
    except Exception:
        return None, None


def _to_pretty_json(data: Any, indent: int = 2) -> str:
    return json.dumps(data, indent=indent, ensure_ascii=False, sort_keys=False)


def _escape_markdown_text(value: str) -> str:
    return value.replace("_", "\\_")


def print_divider(char: str = "=", width: int = 88) -> None:
    print(char * width)


def print_title(title: str, width: int = 88) -> None:
    print()
    print_divider("=", width)
    print(title)
    print_divider("=", width)


def print_subtitle(title: str, width: int = 88) -> None:
    print()
    print_divider("-", width)
    print(title)
    print_divider("-", width)


def print_json_block(title: str, data: Any, width: int = 88) -> None:
    print_subtitle(title, width)
    print(_to_pretty_json(data))


def print_text_block(title: str, text: str, width: int = 88) -> None:
    print_subtitle(title, width)
    print(text)


def print_key_values(title: str, data: Mapping[str, Any], width: int = 88) -> None:
    print_subtitle(title, width)
    max_key_len = max((len(str(key)) for key in data.keys()), default=0)
    for key, value in data.items():
        print(f"{str(key).ljust(max_key_len)} : {value}")


def print_before_after(
    before: Any,
    after: Any,
    before_label: str = "Before",
    after_label: str = "After",
    width: int = 88,
) -> None:
    print_subtitle(before_label, width)
    if isinstance(before, (dict, list)):
        print(_to_pretty_json(before))
    else:
        print(before)

    print_subtitle(after_label, width)
    if isinstance(after, (dict, list)):
        print(_to_pretty_json(after))
    else:
        print(after)


def print_bullets(title: str, items: Sequence[str], width: int = 88) -> None:
    print_subtitle(title, width)
    for item in items:
        print(f"- {item}")


def display_markdown_block(markdown_text: str) -> None:
    display, Markdown = _try_import_ipython_display()
    if display is not None and Markdown is not None:
        display(Markdown(markdown_text))
    else:
        print(markdown_text)


def display_section_title(title: str, level: int = 2) -> None:
    safe_level = min(max(level, 1), 6)
    display_markdown_block(f"{'#' * safe_level} {title}")


def display_callout(text: str) -> None:
    display_markdown_block(f"> {text}")


def display_json_card(title: str, data: Any) -> None:
    json_text = _to_pretty_json(data)
    markdown = f"### {title}\n\n```json\n{json_text}\n```"
    display_markdown_block(markdown)


def display_route_card(
    primary_family: str,
    secondary_family: str,
    best_current_fit: str,
    broken_invariant: str,
    title: str = "Route Summary",
) -> None:
    markdown = "\n".join(
        [
            f"### {title}",
            "",
            f"- **Primary family:** {primary_family}",
            f"- **Secondary family:** {secondary_family}",
            f"- **Best current fit:** {best_current_fit}",
            f"- **Broken invariant:** {broken_invariant}",
        ]
    )
    display_markdown_block(markdown)


def display_mode_note(mode_label: str, note: str | None = None) -> None:
    safe_label = _escape_markdown_text(mode_label)
    markdown_lines = [
        "### Mode",
        "",
        f"- **Current mode:** {safe_label}",
    ]
    if note:
        markdown_lines.append(f"- **Note:** {note}")
    display_markdown_block("\n".join(markdown_lines))


def display_before_after_card(
    before: Any,
    after: Any,
    before_label: str = "Before",
    after_label: str = "After",
    title: str = "Before / After",
) -> None:
    if isinstance(before, (dict, list)):
        before_text = _to_pretty_json(before)
    else:
        before_text = str(before)

    if isinstance(after, (dict, list)):
        after_text = _to_pretty_json(after)
    else:
        after_text = str(after)

    markdown = "\n".join(
        [
            f"### {title}",
            "",
            f"#### {before_label}",
            "",
            "```text",
            before_text,
            "```",
            "",
            f"#### {after_label}",
            "",
            "```text",
            after_text,
            "```",
        ]
    )
    display_markdown_block(markdown)


def display_checklist(title: str, items: Sequence[str]) -> None:
    markdown = [f"### {title}", ""]
    for item in items:
        markdown.append(f"- [x] {item}")
    display_markdown_block("\n".join(markdown))


__all__ = [
    "print_divider",
    "print_title",
    "print_subtitle",
    "print_json_block",
    "print_text_block",
    "print_key_values",
    "print_before_after",
    "print_bullets",
    "display_markdown_block",
    "display_section_title",
    "display_callout",
    "display_json_card",
    "display_route_card",
    "display_mode_note",
    "display_before_after_card",
    "display_checklist",
]
