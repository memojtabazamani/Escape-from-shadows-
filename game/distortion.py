"""Unreliable narration transformation for low composure.

SUGGEST.md §3.2 & ASM-6:
"Composure distortion is capped at the last 20% of the bar and always carries a tic
(italic, stutter, repeated word)... Distortion never affects the existence of an exit,
only its description."

RISK-4:
"Unreliable narration is the highest-variance feature in the phase — wonderful once,
infuriating when overdone."

This module provides a pure, deterministic transformation from (prose, composure) -> prose.
Above 20% composure (composure > 20), it is strictly the identity function.
At or below 20% composure (composure <= 20), each non-empty line receives a cognitive stutter tic
naming the slippage of the player's perception without obfuscating room facts.
"""

from __future__ import annotations

from game.composure import DISTORTION_THRESHOLD

# The distinct, assertable marker indicating a line carries the distortion tic.
TIC_MARKER: str = "..."


def distort_line(line: str) -> str:
    """Distort a single non-empty line with a perceptible stutter tic.

    Deterministic:
    "Cold stone floor." -> "Cold... cold... stone floor."
    """
    stripped = line.strip()
    if not stripped:
        return line

    words = line.split(" ", 1)
    if len(words) == 1:
        first = words[0]
        clean = first.strip(",.?!;:\"'()")
        if not clean:
            return f"[italic]...[/italic] {line}"
        return f"[italic]{clean}... {clean.lower()}...[/italic]"

    first, rest = words
    clean = first.strip(",.?!;:\"'()")
    if not clean:
        return f"[italic]...[/italic] {line}"

    stutter = f"[italic]{clean}... {clean.lower()}...[/italic]"
    return f"{stutter} {rest}"


def distort_narration(prose: str, composure: int) -> str:
    """Transform room narration if composure is in the last 20% band (<= 20).

    Returns prose verbatim when composure > 20.
    Pure and deterministic: does not mutate any state.
    """
    if composure > DISTORTION_THRESHOLD:
        return prose

    lines = prose.split("\n")
    distorted = [distort_line(line) if line.strip() else line for line in lines]
    return "\n".join(distorted)


def has_distortion_tic(text: str) -> bool:
    """Check whether a text line carries the required distortion tic."""
    return TIC_MARKER in text
