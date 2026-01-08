import typing

class CheckBox:
    """
    Checkbox widget for boolean input.
    """
    def __init__(self, 
                 backend: typing.Any, 
                 x: int, 
                 y: int, 
                 text: str, 
                 onchange: typing.Optional[typing.Callable[[bool], None]] = None, 
                 font: typing.Optional[typing.Tuple[str, int]] = None) -> None:
        """
        Initializes the CheckBox.
        
        Args:
            backend: Backend instance.
            x, y: Pixel position.
            text: Checkbox label text.
            onchange: Callback when status changes (receives boolean argument).
            font: Font settings (name, size).
        """
        self.widget = backend.create_checkbox(x, y, text, onchange=onchange, font=font)

    def get_value(self) -> bool:
        """
        Returns the current checked status.
        
        Returns:
            bool: True if checked, False otherwise.
        """
        return bool(self.widget.get())

    def set_value(self, value: bool) -> None:
        """
        Programmatically sets the checkout status.
        
        Args:
            value (bool): True to check, False to uncheck.
        """
        if value: self.widget.select()
        else: self.widget.deselect()

    def configure(self, **kwargs) -> None:
        """Dynamically updates widget properties."""
        self.widget.configure(**kwargs)

    def get_current_coord(self) -> typing.Tuple[int, int]:
        """
        Returns the current pixel coordinates of the checkbox.
        
        Returns:
            tuple: (x, y) in pixels.
        """
        return (self.widget.winfo_x(), self.widget.winfo_y())