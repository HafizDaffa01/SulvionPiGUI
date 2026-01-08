import typing
from .core.app import App

__all__ = ['init', 'App']

def init(SIZE: typing.List[typing.Union[int, float]] = [10, 10], 
         gtp: int = 50, 
         title: str = "My App", 
         show_grid: bool = False, 
         grid_bgcolor: typing.Optional[str] = None, 
         grid_lncolor: str = "gray30", 
         coord_color: str = "gray50", 
         show_coord: bool = True,
         theme: str = "dark") -> App:
    """
    Initializes a new SulvionPiGUI application.
    
    Args:
        SIZE (list): Grid size [width, height].
        gtp (int): Pixel size for one grid square (default 50).
        title (str): Window title.
        show_grid (bool): If True, displays helper grid lines.
        grid_bgcolor (str): Grid background color (default matches theme).
        grid_lncolor (str): Grid line color.
        coord_color (str): Color of the grid coordinate text.
        show_coord (bool): If True, displays coordinate numbers on the grid.
        theme (str): Application theme ("light" or "dark").
        
    Returns:
        App: The initialized application instance.
    """
    
    return App(
        size=SIZE, 
        gtp=gtp, 
        title=title, 
        show_grid=show_grid,
        grid_bgcolor=grid_bgcolor,
        grid_lncolor=grid_lncolor,
        text_color=coord_color,
        text_coord=show_coord,
        theme=theme
    )
