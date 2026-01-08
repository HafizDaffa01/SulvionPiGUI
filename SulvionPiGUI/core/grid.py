import typing

class GridSystem:
    """
    Core system for converting between grid units and pixel coordinates.
    Enables precise widget placement using a standard grid-based coordinate system.
    """
    def __init__(self, gtp: int = 50) -> None:
        """
        Initializes the GridSystem.
        
        Args:
            gtp (int): Grid-to-Pixel factor. The number of pixels per 1 grid unit. Defaults to 50.
        """
        self.gtp = gtp

    def to_pixels(self, grid_pos: typing.List[typing.Union[int, float]]) -> typing.Tuple[int, int]:
        """
        Converts grid coordinates (0-based) to absolute pixel offsets.
        Example: [0, 0] results in (0, 0), [1, 1] with gtp 50 results in (50, 50).
        
        Args:
            grid_pos (list): A list containing [x, y] in grid units.
            
        Returns:
            tuple: (x, y) in pixels.
        """
        px_x = int(grid_pos[0] * self.gtp)
        px_y = int(grid_pos[1] * self.gtp)
        return (px_x, px_y)

    def dim_to_pixels(self, grid_dim: typing.List[typing.Union[int, float]]) -> typing.Tuple[int, int]:
        """
        Converts grid dimensions (width, height) to pixels.
        Used to determine widget size.
        
        Args:
            grid_dim (list): A list containing [width, height] in grid units.
            
        Returns:
            tuple: (width, height) in pixels.
        """
        px_w = int(grid_dim[0] * self.gtp)
        px_h = int(grid_dim[1] * self.gtp)
        return (px_w, px_h)

    def get_window_size(self, size_grid: typing.List[typing.Union[int, float]]) -> typing.Tuple[int, int]:
        """
        Calculates the total window dimensions in pixels based on the grid size.
        
        Args:
            size_grid (list): Grid size as [cols, rows].
            
        Returns:
            tuple: (width, height) of the window in pixels.
        """
        return self.dim_to_pixels(size_grid)
