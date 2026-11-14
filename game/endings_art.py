"""Minimalist ASCII art vignettes for canonical endings (Phase 3 Slice B, Task B03).

SUGGEST.md §7.3:
"Reserve ASCII art for three moments only: the title screen, the Hell Dog,
and each ending. Rarity is what makes it land."

Strict formatting constraints:
- Pure ASCII characters (no emojis or double-wide characters).
- Height <= 8 lines.
- Width <= 60 columns.
"""

from __future__ import annotations

# 1. The Long Walk: Stone floor threshold and fading silhouette
ASCII_THE_LONG_WALK = """      .---.
     (  .  )
      \\ : /
       : :
   ____:___:____
  /             \\
 /  .    .    .  \\
/_________________\\"""

# 2. Meat and Silence: Chained collar slack on gravel beside bone
ASCII_MEAT_AND_SILENCE = """        _______
      /         \\
     |   (===)   |
      \\_________/=========.
            \\             |
       .-.   \\            |
      ( o )====[=====]===='
       '-'"""

# 3. The Quiet Exit: Heavy iron gate slightly open to a starless horizon
ASCII_THE_QUIET_EXIT = """     +-------+     +-------+
     | | | | |    /| | | | |
     | | | | |   / | | | | |
     | |=|=| |  /  |=| |=| |
     | | | | | /   | | | | |
     | | | | |/    | | | | |
     +-------+     +-------+
     ~~~~~~~~~~~~~~~~~~~~~~~"""

# 4. What the Book Knew: Open black grimoire with unblinking eye glyph
ASCII_WHAT_THE_BOOK_KNEW = """           .---..---.
          /  /   \\   \\
         /  / (O) \\   \\
        |  |  ---  |   |
        |  |       |   |
         \\  \\     /   /
          \\__\\___/__/
           `--------`"""

# 5. The New Shadow: Twin long shadows cast against an empty wall
ASCII_THE_NEW_SHADOW = """      |                       |
      |                       |
      |       /\\     /\\       |
      |      /  \\   /  \\      |
      |     / /\\ \\ / /\\ \\     |
      |    / /  \\ V /  \\ \\    |
      |   /_/    \\_/    \\_\\   |
      |_______________________|"""

# 6. Homecoming: Small framed photograph with light beam across it
ASCII_HOMECOMING = """        .-------------------.
        |   .-----------.   |
        |   |  \\     /  |   |
        |   |   .---.   |   |
        |   |   | * |   |   |
        |   |   '---'   |   |
        |   '-----------'   |
        '-------------------'"""

# 7. Stay: Heavy door bolted from inside with key turned in lock
ASCII_STAY = """        .-------------------.
        |   .-----------.   |
        |   |   [===]   |   |
        |   |     | (O) |   |
        |   |     |  |  |   |
        |   |     |  |  |   |
        |   '-----------'   |
        '-------------------'"""

# Voluntary walk: The Shadow lowers itself like black silk
ASCII_SHADOW_WALK = """        .-------------------.
        |    /\\       /\\    |
        |   /  \\     /  \\   |
        |  / /\\ \\   / /\\ \\  |
        | | |  | | | |  | | |
        |  \\ \\/ /   \\ \\/ /  |
        |   \\__/     \\__/   |
        '-------------------'"""

# Fallback marker for unknown or generic endings
ASCII_FALLBACK = """        .-------------------.
        |    [ UNKNOWN ]    |
        '-------------------'"""

ENDINGS_ASCII: dict[str, str] = {
    "the_long_walk": ASCII_THE_LONG_WALK,
    "meat_and_silence": ASCII_MEAT_AND_SILENCE,
    "the_quiet_exit": ASCII_THE_QUIET_EXIT,
    "what_the_book_knew": ASCII_WHAT_THE_BOOK_KNEW,
    "the_new_shadow": ASCII_THE_NEW_SHADOW,
    "homecoming": ASCII_HOMECOMING,
    "stay": ASCII_STAY,
    "shadow_walk": ASCII_SHADOW_WALK,
}

MAX_ASCII_HEIGHT: int = 8
MAX_ASCII_WIDTH: int = 60


def get_ending_ascii(ending_id: str) -> str:
    """Retrieve the pure ASCII art vignette for a canonical ending ID.

    Returns safe fallback marker if the ID is unknown or empty.
    """
    if not ending_id:
        return ASCII_FALLBACK
    return ENDINGS_ASCII.get(ending_id.strip().lower(), ASCII_FALLBACK)
