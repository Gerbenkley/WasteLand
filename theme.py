from questionary import Style

ORANGE = "#ff9d00"
GREEN = "#80ff72"
RED = "#ff5555"
YELLOW = "#f1fa8c"
MUTED = "#888888"


custom_style = Style([
    ("qmark", "fg:#ff9d00 bold"),
    ("question", "bold"),
    ("answer", "fg:#00ff00 bold"),
    ("pointer", "fg:#ff9d00 bold"),
    ("highlighted", "fg:#ff9d00 bold"),
    ("selected", "fg:#00ff00"),
])