import typing

class Slider:
    """
    Slider widget for selecting a value within a range.
    """
    def __init__(self, 
                 backend: typing.Any, 
                 x: int, 
                 y: int, 
                 w: int, 
                 h: int, 
                 from_: float = 0, 
                 to: float = 1, 
                 orientation: str = "horizontal", 
                 onchange: typing.Optional[typing.Callable[[float], None]] = None) -> None:
        """
        Initializes the Slider.
        
        Args:
            backend: Backend instance.
            x, y, w, h: Pixel position and dimensions.
            from_, to: Minimum and maximum range boundaries.
            orientation: Slider orientation ("horizontal" or "vertical").
            onchange: Callback called when the slider value changes.
        """
        self.widget = backend.create_slider(x, y, w, h, from_=from_, to=to, orientation=orientation, onchange=onchange)

    def set_value(self, value: float) -> None:
        """
        Programmatically sets the slider value.
        
        Args:
            value (float): New value.
        """
        self.widget.set(value)

    def get_value(self) -> float:
        """
        Returns the current slider value.
        
        Returns:
            float: Current slider position.
        """
        return self.widget.get()

    def configure(self, **kwargs) -> None:
        """Dynamically updates widget properties."""
        self.widget.configure(**kwargs)

    def get_current_coord(self) -> typing.Tuple[int, int]:
        """
        Returns the current pixel coordinates of the slider.
        
        Returns:
            tuple: (x, y) in pixels.
        """ 
        return self.widget.winfo_x(), self.widget.winfo_y()