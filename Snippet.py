import pyperclip
from typing import Optional

def copy_to_clipboard(text: str) -> None:
    'Copy text to the system clipboard'

    if not text:
        raise ValueError('⚠️ Cannot copy empty text')
    pyperclip.copy(text)


def paste_from_clipboard() -> Optional[str]:
    "Paste text from the system clipboard"
    "Returns None if clipboard is empty"

    content = pyperclip.paste()
    return content if content else None


if __name__ == "__main__":
    copy_to_clipboard('Hello from the side of Konain worsi')
    print('✅ Copied text to the clipboard')
    print('Pasted: ',paste_from_clipboard())