import time
import os
from rich.console import Console
from rich.text import Text


console = Console()


def type_text(delay, text):
    styled_text = Text.from_markup(text)

    for i, char in enumerate(styled_text.plain):
        char_style = styled_text.get_style_at_offset(console, i)

        console.print(
            Text(char, style=char_style),
            end="",
            markup=False,
            highlight=False,
        )

        #time.sleep(delay)

    console.print()




def clear_console():
    os.system("cls" if os.name == "nt" else "clear")
