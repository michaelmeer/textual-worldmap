"""Some widgets"""
from dataclasses import dataclass

import pyproj
from rich.segment import Segment
from rich.style import Style
from textual.geometry import Size
from textual.reactive import reactive
from textual.strip import Strip
from textual.widgets import Static


@dataclass
class Coordinate:
    """A coordinate within a widget"""
    x: int
    y: int


@dataclass
class WorldCoordinate:
    """ A geographical coordinate with an optional label"""
    lat: float
    lon: float
    label: str | None = None


class AsciiArtWidget(Static):
    """ Simple custom widget just meant to show some ascii art and optionallyh
    hightlight one coordinate
    """
    highlighted_coordinate: reactive[Coordinate | None] = reactive(None)

    def __init__(self, graphic: str, **kwargs):
        super().__init__(**kwargs)
        self.graphic = self.normalize_graphic(graphic)
        self.graphic_lines = self.graphic.split("\n")
        self.graphic_width = len(self.graphic_lines[0])
        self.graphic_height = len(self.graphic_lines)

    def normalize_graphic(self, graphic: str) -> str:
        """ Makes sure that all lines are th same length
        """
        lines = graphic.split("\n")
        max_length = max(len(line) for line in lines)
        return "\n".join(line.ljust(max_length) for line in lines)

    def render_line(self, y: int) -> Strip:
        if y < len(self.graphic_lines):
            if self.highlighted_coordinate is not None and y == self.highlighted_coordinate.y:
                segments = [
                    Segment(self.graphic_lines[y][: self.highlighted_coordinate.x]),
                    Segment("X", Style(color="red", bgcolor="blue", bold=True, frame=True)),
                    # Segment("X", Style(reverse=True)),
                    Segment(self.graphic_lines[y][self.highlighted_coordinate.x + 1:]),
                ]
                return Strip(segments)
            return Strip([Segment(self.graphic_lines[y])])
        return Strip.blank(self.size.width)

    def get_content_width(self, container: Size, viewport: Size) -> int:
        """Force content width size."""
        return self.graphic_width

    def get_content_height(self, container: Size, viewport: Size, width: int) -> int:
        """Force content height size."""
        return len(self.graphic_lines)


class WorldMapWidget(AsciiArtWidget):
    """A textual customer widgt showing a world map, and optionally highlights a location"""

    def __init__(self, **kwargs):
        super().__init__(graphic=self.world_map_graphic(), **kwargs)

    @staticmethod
    def world_map_graphic() -> str:
        """A world map as ascii art"""
        return r"""          . _..::__:  ,-"-"._       |]       ,     _,.__
  _.___ _ _<_>`!(._`.`-.    /        _._     `_ ,_/  '  '-._.---.-.__ 
.{     " " `-==,',._\{  \  / {)     / _ ">_,-' `                 /-/_ 
 \_.:--.       `._ )`^-. "'      , [_/(                       __,/-'  
'"'     \         "    _L       |-_,--'                )     /. (|    
         |           ,'         _)_.\\._<> {}              _,' /  '   
         `.         /          [_/_'` `"(                <'}  )       
          \\    .-. )          /   `-'"..' `:._          _)  '        
   `        \  (  `(          /         `:\  > \  ,-^.  /' '          
             `._,   ""        |           \`'   \|   ?_)  {\          
                `=.---.       `._._       ,'     "`  |' ,- '.         
                  |    `-._        |     /          `:`<_|=--._       
                  (        >       .     | ,          `=.__.`-'\      
                   `.     /        |     |{|              ,-.,\     . 
                    |   ,'          \   / `'            ,"     \      
                    |  /             |_'                |  __  /      
                    | |                                 '-'  `-'   \. 
                    |/                                        "    /  
                    \.                                            '   

                     ,/           ______._.--._ _..---.---------.     
__,-----"-..?----_/ )\    . ,-'"             "                  (__--/
                      /__/\/                                          
        """

    @staticmethod
    def inverse_num_in_range(num, min_num, max_num):
        """
            Returns the inverse of a number in a range eg:
                reverseNumRange(1, 0, 10) => 9
        """
        return (max_num + min_num) - num

    def convert_world_coordinate(self, world_coordinate: WorldCoordinate) -> Coordinate:
        """
            Takes a Lat, Lon pair and return the Mercador projection X, Y suitable for this map
            It ignores the very top and bottom of the map due to them being arctic regions and empty
            Lat range:
        """
        # sets up the conversion
        crs_from = pyproj.Proj(init='epsg:4326')  # standard lon, lat coords
        crs_to = pyproj.Proj(init='epsg:3857')  # Web mercator projection (same as google maps)

        x, y = pyproj.transform(crs_from, crs_to, world_coordinate.lon, world_coordinate.lat)

        # we standardise the coords in the given ranges here, so it becomes a percentage
        x_range = (-20037508.34, 20037508.34)
        y_range = (-20048966.10, 20048966.10)
        x_percent = (x - x_range[0]) / (x_range[1] - x_range[0])
        y_percent = (y - y_range[0]) / (y_range[1] - y_range[0])

        # we then take that percentage and apply it to the map width or height
        map_cols = 69
        map_rows = 41
        map_x = int(x_percent * map_cols)
        map_y = int(y_percent * map_rows)

        # we have to reverse the y
        map_y = self.inverse_num_in_range(map_y, 0, map_rows)

        # ANything above or below our
        top_margin = 10
        bottom_margin = 10
        if map_y - top_margin < 0 or map_y > map_rows - bottom_margin:
            raise ValueError(
                f'The Lat, Lon ({world_coordinate.lat}, {world_coordinate.lon}) was above'
                f' or below our margins'
            )

        result = Coordinate(map_x, map_y - top_margin)
        return result

    def set_world_coordinate(self, world_coordinate: WorldCoordinate):
        """Converts from geographical coordinates to x/y coordinates on the widget"""
        self.highlighted_coordinate = self.convert_world_coordinate(world_coordinate)
