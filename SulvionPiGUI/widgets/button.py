import typing

class Button:
    """
    Interactive Button widget.
    """
    def __init__(self, 
                 backend: typing.Any, 
                 x: int, 
                 y: int, 
                 w: int, 
                 h: int, 
                 text: str, 
                 command: typing.Optional[typing.Callable], 
                 text_font: typing.Optional[str] = None, 
                 text_size: typing.Optional[int] = None, 
                 align: str = "center") -> None:
        """
        Initializes the Button.
        
        Args:
            backend: Backend instance.
            x, y, w, h: Pixel geometry.
            text: Button label text.
            command: Callback function when clicked.
            text_font: Font name.
            text_size: Font size.
            align: Text alignment ("center", "left", "right", "top", "bottom").
        """
        font = (text_font, text_size) if text_font or text_size else None
        self.widget = backend.create_button(x, y, w, h, text, command, font=font, anchor=align)

    def set_text(self, text: str) -> None:
        """
        Changes the button text.
        
        Args:
            text (str): New text content.
        """
        self.widget.configure(text=text)

    def get_text(self) -> str:
        """
        Returns the current button text.
        
        Returns:
            str: Button label text.
        """
        return self.widget.cget("text")

    def configure(self, **kwargs) -> None:
        """
        Dynamically updates widget properties.
        """
        self.widget.configure(**kwargs)
        
    def get_current_coord(self) -> typing.Tuple[int, int]:
        """
        Returns the current pixel coordinates of the button.
        
        Returns:
            tuple: (x, y) in pixels.
        """
        return (self.widget.winfo_x(), self.widget.winfo_y())
