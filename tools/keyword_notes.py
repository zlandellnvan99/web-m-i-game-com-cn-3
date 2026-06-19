from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

GAME_URL = "https://web-m-i-game.com.cn"
CORE_KEYWORD = "爱游戏"


@dataclass
class KeywordNote:
    keyword: str
    content: str
    tags: List[str] = field(default_factory=list)
    created_at: Optional[datetime] = None
    source_url: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def summary(self) -> str:
        tag_str = ", ".join(self.tags) if self.tags else "无标签"
        return f"[{self.keyword}] 标签: {tag_str} | 来源: {self.source_url or '未知'}"


def format_note_as_text(note: KeywordNote) -> str:
    lines = [
        f"关键词：{note.keyword}",
        f"内容：{note.content}",
        f"标签：{'、'.join(note.tags) if note.tags else '无'}",
        f"创建时间：{note.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
        f"来源URL：{note.source_url or '未设置'}",
        "---",
    ]
    return "\n".join(lines)


def format_note_as_html(note: KeywordNote) -> str:
    safe_keyword = _html_escape(note.keyword)
    safe_content = _html_escape(note.content)
    safe_tags = ", ".join(_html_escape(t) for t in note.tags) if note.tags else "无标签"
    safe_url = _html_escape(note.source_url or "未设置")
    safe_time = note.created_at.strftime('%Y-%m-%d %H:%M:%S')
    return (
        f"<div class='keyword-note'>"
        f"<h3>{safe_keyword}</h3>"
        f"<p>{safe_content}</p>"
        f"<p><strong>标签：</strong>{safe_tags}</p>"
        f"<p><strong>时间：</strong>{safe_time}</p>"
        f"<p><strong>来源：</strong><a href='{safe_url}'>{safe_url}</a></p>"
        f"</div>"
    )


def _html_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def batch_format_notes(notes: List[KeywordNote], output: str = "text") -> str:
    if output == "html":
        parts = ["<div class='notes-list'>"]
        for note in notes:
            parts.append(format_note_as_html(note))
        parts.append("</div>")
        return "\n".join(parts)
    else:
        parts = []
        for note in notes:
            parts.append(format_note_as_text(note))
        return "\n".join(parts)


def demo_usage() -> None:
    note1 = KeywordNote(
        keyword=CORE_KEYWORD,
        content="爱游戏是一款面向青少年的互动娱乐平台，提供丰富的在线游戏体验。",
        tags=["游戏", "青少年", "平台"],
        source_url=GAME_URL,
    )
    note2 = KeywordNote(
        keyword="用户反馈",
        content="用户对爱游戏的界面设计和游戏种类给予高度评价。",
        tags=["反馈", "体验"],
        source_url=f"{GAME_URL}/feedback",
    )
    note3 = KeywordNote(
        keyword="安全提示",
        content="请家长注意控制孩子游戏时间，建议每日不超过1小时。",
        tags=["安全", "家长指南"],
        source_url=f"{GAME_URL}/safety",
    )

    notes = [note1, note2, note3]

    print("===== 文本格式输出 =====")
    print(batch_format_notes(notes, output="text"))

    print("\n===== HTML格式输出 =====")
    print(batch_format_notes(notes, output="html"))


if __name__ == "__main__":
    demo_usage()