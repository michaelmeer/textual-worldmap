
#!/usr/bin/env python3
"""
Demo Program to show the World Map Widget using the Textual Library
"""
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, RadioSet, RadioButton

from textual_worldmap.worldmapwidget import WorldCoordinate, WorldMapWidget


LOCATIONS = [
    #               Lat        Lon       Name
    WorldCoordinate(-43.532055, 172.636230, "Christchurch :new_zealand:"),
    WorldCoordinate(-33.9221, 18.4231, "Cape Town :south_africa:"),
    WorldCoordinate(-6.200000, 106.816666, "Jakarta :indonesia:"),
    WorldCoordinate(33.929047, -118.441495, "LA :united_states:"),
    WorldCoordinate(51.369208, 0.106923, "London :united_kingdom:"),
    WorldCoordinate(-18.259349, -313.850023, "Madagascar :madagascar:"),
    WorldCoordinate(-34.520136, -222.565312, "Melbourne :australia:"),
    WorldCoordinate(39.768173, -434.715499, "New York :united_states:"),
    WorldCoordinate(59.334591, 18.063240, "Stockholm :sweden:"),
    WorldCoordinate(-23.5558, -46.6396, "Sao Paolo :brazil:"),
    WorldCoordinate(35.689487, 139.691711, "Tokyo :japan:"),
    WorldCoordinate(49.240186, -123.110419, "Vancouver :canada:"),
    WorldCoordinate(48.208176, 16.373819, "Vienna :austria:"),
    WorldCoordinate(47.3769, 8.5417, "Zürich :switzerland:"),
]


class WorldmapWidgetDemoApp(App[None]):
    """Demo App"""

    TITLE = "Worldmap Widget Demo"

    CSS = """
    Screen {
        layout: horizontal;
    }

    WorldMapWidget {
        border: double $accent;
        height: auto;
        width: auto;
        align: center middle;
    }

    RadioSet {
        background: green 20%;
        color: green;
        border: panel green;
        margin: 3;
        padding: 1;
        width: auto;
        align: left top;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with RadioSet(id="location_selection"):
            for location in LOCATIONS:
                yield RadioButton(location.label)

        yield WorldMapWidget(id="world_map")

        yield Footer()

    def on_mount(self) -> None:
        """Setting up widgets when mounting"""
        label = self.query_one("#location_selection")
        label.border_title = "Select location..."

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        """If the selected town has changed, update the world map to highlight that town"""
        worldmapwidget = self.query_one("#world_map", WorldMapWidget)
        worldmapwidget.set_world_coordinate(LOCATIONS[event.radio_set.pressed_index])


if __name__ == "__main__":
    WorldmapWidgetDemoApp().run()
