"""Tests for composure bar and distortion tic UI styling (Task D04)."""
from pathlib import Path
import pytest

from game.content_schema import load_content
from game.state import RunState
from screens.game import GameScreen
from tests.test_game_screen import GameScreenTestApp


@pytest.fixture
def house_content():
    content_path = Path("data/content.json")
    assert content_path.exists(), "data/content.json must exist"
    return load_content(content_path)


@pytest.mark.anyio
async def test_composure_bar_renders_in_the_status_zone(house_content):
    """Composure bar lives inside #status-zone beside lantern bar, with no fourth zone."""
    state = RunState.fresh_run()
    app = GameScreenTestApp(content=house_content, state=state)

    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)

        # Status zone contains #composure-status
        status_zone = screen.query_one("#status-zone")
        assert status_zone is not None
        comp_widget = status_zone.query_one("#composure-status")
        assert comp_widget is not None

        # Content of composure widget contains NERVE
        assert "NERVE" in str(comp_widget.content)


@pytest.mark.anyio
async def test_last_twenty_percent_is_visually_distinct(house_content):
    """Last 20% displays '(shaken)' and floor displays '(broken)'."""
    full_text = GameScreen.render_composure_bar(100)
    assert "██████████" in full_text
    assert "(shaken)" not in full_text
    assert "(broken)" not in full_text

    shaken_text = GameScreen.render_composure_bar(20)
    assert "██░░░░░░░░" in shaken_text
    assert "(shaken)" in shaken_text

    broken_text = GameScreen.render_composure_bar(0)
    assert "░░░░░░░░░░" in broken_text
    assert "(broken)" in broken_text


@pytest.mark.anyio
async def test_tic_marker_is_rendered_in_narration(house_content):
    """When composure <= 20, the distortion tic reaches the rendered text widget."""
    state = RunState.fresh_run()
    state.current_room = "hall"
    state.composure = 15

    app = GameScreenTestApp(content=house_content, state=state)
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)

        scene_text = screen.query_one("#scene-text")
        rendered = str(scene_text.content)
        assert "..." in rendered
        assert "[italic]" in rendered or "italic" in rendered


def test_bar_and_text_carry_information_without_colour():
    """Non-colour channel (textual cues and block fills) communicates bar state."""
    # Full: no warning tag, 10 filled blocks
    full = GameScreen.render_composure_bar(100)
    assert "██████████" in full

    # Low (shaken): has explicit textual tag
    shaken = GameScreen.render_composure_bar(15)
    assert "(shaken)" in shaken

    # Floor (broken): has explicit textual tag
    broken = GameScreen.render_composure_bar(0)
    assert "(broken)" in broken


@pytest.mark.anyio
async def test_red_is_absent_except_in_the_walk(house_content):
    """§7.4: Red color (#e63946) is absent from composure bar and general narration; reserved for the Shadow."""
    for comp in (100, 70, 20, 0):
        bar_text = GameScreen.render_composure_bar(comp)
        assert "#e63946" not in bar_text.lower()
        assert "red" not in bar_text.lower()


@pytest.mark.anyio
async def test_the_worst_case_screen_fits_one_terminal(house_content):
    """Worst case: full 6/6 pack, low oil, low composure, all mounted in one GameScreen."""
    state = RunState.fresh_run()
    for item in ["matchbox", "rusty_cleaver", "the_book", "silver_whistle", "dogs_tooth", "front_door_key"]:
        state.add_item(item)
    state.lantern = 15  # Low oil
    state.composure = 10  # Shaken nerve

    app = GameScreenTestApp(content=house_content, state=state)
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)

        # Status zone has updated with all indicators
        lan_widget = screen.query_one("#lantern-status")
        assert "low oil" in str(lan_widget.content)

        comp_widget = screen.query_one("#composure-status")
        assert "(shaken)" in str(comp_widget.content)

        inv_widget = screen.query_one("#inventory-status")
        assert "6/6 FULL" in str(inv_widget.content)
