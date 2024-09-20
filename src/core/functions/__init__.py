from .weather import tools as weather_tools
from .weather import get_current_weather
from .robot import tools as robot_tools
from .robot import go_to_place

tools = []
tools.extend(weather_tools)
tools.extend(robot_tools)
__all__ = ["tools"]

available_functions = {
    "get_current_weather": get_current_weather,
    "go_to_place": go_to_place,
}
