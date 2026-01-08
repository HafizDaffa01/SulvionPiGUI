import typing

class Input:
    """
    Text Input widget for receiving user entries.
    """
    def __init__(self, 
                 backend: typing.Any, 
                 x: int, 
                 y: int, 
                 w: int, 
                 h: int, 
                 placeholder: str = "", 
                 onchange: typing.Optional[typing.Callable[[str], None]] = None, 
                 font: typing.Optional[typing.Tuple[str, int]] = None) -> None:
        """
        Initializes the Text Input.
        
        Args:
            backend: Backend instance.
            x, y, w, h: Pixel position and dimensions.
            placeholder: Hint text shown when empty.
            onchange: Callback called on text modification.
            font: Font settings.
        """
        self.widget = backend.create_entry(x, y, w, h, placeholder=placeholder, onchange=onchange, font=font)

    def get_value(self) -> str:
        """
        Returns the current text content.
        
        Returns:
            str: Input field text.
        """
        return self.widget.get()

    def set_value(self, text: str) -> None:
        """
        Programmatically sets the input text content.
        
        Args:
            text (str): New text to display.
        """
        self.widget.delete(0, 'end')
        self.widget.insert(0, text)

    def configure(self, **kwargs) -> None:
        """Dynamically updates widget properties."""
        self.widget.configure(**kwargs)

    def get_current_coord(self) -> typing.Tuple[int, int]:
        """
        Returns the current pixel coordinates of the widget.
        
        Returns:
            tuple: (x, y) in pixels.
        """
        return self.widget.winfo_x(), self.widget.winfo_y()