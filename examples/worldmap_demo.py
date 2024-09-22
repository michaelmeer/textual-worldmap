"""
Demo Program to show the World Map Widget using the Textual Library
"""
import logging
from itertools import cycle

from textual.app import App, ComposeResult
from textual.logging import TextualHandler
from textual.widgets import Footer, Header, Label

from textual_worldmap.worldmapwidget import (
    AsciiArtWidget,
    Coordinate,
    WorldCoordinate,
    WorldMapWidget)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[TextualHandler()],
)

LOCATIONS = [
    #               Lat        Lon       Name
    WorldCoordinate(-6.200000, 106.816666, "Jakarta"),
    WorldCoordinate(59.334591, 18.063240, "Stockholm"),
    WorldCoordinate(51.369208, 0.106923, "London"),
    WorldCoordinate(39.768173, -434.715499, "New York"),
    WorldCoordinate(-18.259349, -313.850023, "Madagascar"),
    WorldCoordinate(-34.520136, -222.565312, "Melbourne"),
    WorldCoordinate(48.208176, 16.373819, "Vienna"),
    WorldCoordinate(-43.532055, 172.636230, "Christchurch"),
    WorldCoordinate(35.689487, 139.691711, "Tokyo"),
    WorldCoordinate(33.929047, -118.441495, "LA"),
    WorldCoordinate(49.240186, -123.110419, "Vancouver"),
]


class AsciiArtDemoApp(App[None]):
    """Demo App"""
    TITLE = "Ascii Art Demo"

    CSS = """
    AsciiArtWidget {
        border: heavy;
        height: auto;
        width: auto;
    }

    GeneratedWidget {
        border: heavy;
        align: center middle;
        width: 50;
        height: 50;
    }
    """

    BINDINGS = [
        ("l", "location", "Cycle example locations"),
    ]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._locations = cycle(LOCATIONS)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(id="location_label")
        yield WorldMapWidget(id="world_map")
        yield AsciiArtWidget(self.graphic_floppy(), id="floppy")
        yield AsciiArtWidget(self.graphic_robot(), id="robot")
        yield Footer()

    def on_mount(self) -> None:
        """Sets the widgets to initial values"""
        self.query_one("#floppy", AsciiArtWidget).highlighted_coordinate = Coordinate(2, 2)
        self.query_one("#robot", AsciiArtWidget).highlighted_coordinate = Coordinate(2, 2)
        self.action_location()

    def action_location(self) -> None:
        """Changes the WorldMapWidget to the next location in the list, and updates
        the Label with the name of the location too"""
        location = next(self._locations)
        self.query_one("#world_map", WorldMapWidget).set_world_coordinate(location)
        self.query_one("#location_label", Label).update(f"Location: {location.label}")

    def key_up(self) -> None:
        """Moves highlighted coordinate up"""
        floppy = self.query_one("#floppy", AsciiArtWidget)
        if floppy.highlighted_coordinate:
            floppy.highlighted_coordinate = Coordinate(
                floppy.highlighted_coordinate.x, floppy.highlighted_coordinate.y - 1
            )

    def key_down(self) -> None:
        """Moves highlighted coordinate down"""
        floppy = self.query_one("#floppy", AsciiArtWidget)
        if floppy.highlighted_coordinate:
            floppy.highlighted_coordinate = Coordinate(
                floppy.highlighted_coordinate.x, floppy.highlighted_coordinate.y + 1
            )

    def key_left(self) -> None:
        """Moves highlighted coordinate to the left"""
        floppy = self.query_one("#floppy", AsciiArtWidget)
        if floppy.highlighted_coordinate:
            floppy.highlighted_coordinate = Coordinate(
                floppy.highlighted_coordinate.x - 1, floppy.highlighted_coordinate.y
            )

    def key_right(self) -> None:
        """Moves highlighted coordinate to the right"""
        floppy = self.query_one("#floppy", AsciiArtWidget)
        if floppy.highlighted_coordinate:
            floppy.highlighted_coordinate = Coordinate(
                floppy.highlighted_coordinate.x + 1, floppy.highlighted_coordinate.y
            )

    def graphic_floppy(self) -> str:
        """Returns a little ascii art floppy"""
        floppy_graphic = r""" ___,___,_______,____
|  :::|///./||'||    \
|  :::|//.//|| || H)  |
|  :::|/.///|!!!|     |
|   _______________   |
|  |:::::::::::::::|  |
|  |_______________|  |
|  |_______________|  |
|  |_______________|  |
|  |_______________|  |
||_|     boba      ||_| 
|__|_______________|__|"""
        return floppy_graphic

    def graphic_robot(self) -> str:
        """Returns a little ascii art robot"""
        robot_graphic = r"""      \_/
     (* *)
    __)#(__
   ( )...( )(_)
   || |_| ||//
>==() | | ()/
    _(___)_
   [-]   [-]MJP"""
        return robot_graphic


if __name__ == "__main__":
    # AsciiArtDemoApp().run(inline=True)
    AsciiArtDemoApp().run()
