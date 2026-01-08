import typing

class Plot:
    """
    Plot widget for displaying Matplotlib graphics.
    """
    def __init__(self, 
                 backend: typing.Any, 
                 x: int, 
                 y: int, 
                 w: int, 
                 h: int, 
                 p_type: str = "line", 
                 data: typing.Optional[typing.List[typing.Any]] = None, 
                 options: typing.Optional[typing.Dict[str, typing.Any]] = None) -> None:
        """
        Initializes the Plot widget.
        
        Args:
            backend: Backend instance.
            x, y, w, h: Pixel position and dimensions.
            p_type: Chart type ("line", "bar").
            data: List of initial data value.
            options: Dictionary of additional configuration options.
        """
        controller = backend.create_plot(x, y, w, h, p_type=p_type, data=data, options=options)
        self.widget = controller["widget"]
        self._update_func = controller["update"]

    def update(self, data: typing.List[typing.Any]) -> None:
        """
        Refreshes the chart with new data.
        
        Args:
            data (list): New data list (or (x, y) tuple for specific plots).
        """
        self._update_func(data)

    def get_current_coord(self) -> typing.Tuple[int, int]:
        """
        Returns the current pixel coordinates of the plot workspace.
        
        Returns:
            tuple: (x, y) in pixels.
        """
        return self.widget.winfo_x(), self.widget.winfo_y()