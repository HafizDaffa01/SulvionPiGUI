import typing

class Dropdown:
    """
    Dropdown menu widget for selections.
    """
    def __init__(self, 
                 backend: typing.Any, 
                 x: int, 
                 y: int, 
                 w: int, 
                 h: int, 
                 options: typing.List[str], 
                 onchange: typing.Optional[typing.Callable[[str], None]] = None, 
                 font: typing.Optional[typing.Tuple[str, int]] = None) -> None:
        """
        Initializes the Dropdown.
        
        Args:
            backend: Backend instance.
            x, y, w, h: Pixel position and dimensions.
            options: List of string options.
            onchange: Callback when an option is selected.
            font: Font settings.
        """
        self.widget = backend.create_optionmenu(x, y, w, h, options, onchange=onchange, font=font)

    def get_value(self) -> str:
        """
        Returns the currently selected value.
        
        Returns:
            str: Selected option string.
        """
        return self.widget.get()

    def set_value(self, value: str) -> None:
        """
        Programmatically sets the selected value.
        
        Args:
            value (str): New value to select.
        """
        self.widget.set(value)

    def configure(self, **kwargs) -> None:
        """Dynamically updates widget properties."""
        self.widget.configure(**kwargs)

    def get_current_coord(self) -> typing.Tuple[int, int]:
        """
        Returns the current pixel coordinates of the dropdown.
        
        Returns:
            tuple: (x, y) in pixels.
        """
        return (self.widget.winfo_x(), self.widget.winfo_y())