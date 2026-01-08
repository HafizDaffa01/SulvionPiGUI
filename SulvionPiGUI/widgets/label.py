import typing

class Label:
    """
    Static text Label widget.
    """
    def __init__(self, 
                 backend: typing.Any, 
                 x: int, 
                 y: int, 
                 w: int, 
                 h: int, 
                 text: str, 
                 align: str = "center", 
                 text_font: typing.Optional[str] = None, 
                 text_size: typing.Optional[int] = None) -> None:
        """
        Initializes the Label.
        
        Args:
            backend: Backend instance.
            x, y, w, h: Pixel position and dimensions.
            text: Label content text.
            align: Text alignment ("center", "left", etc.).
            text_font: Font family name.
            text_size: Font size.
        """
        font = (text_font, text_size) if text_font or text_size else None
        self.widget = backend.create_label(x, y, w, h, text, anchor=align, font=font)

    def set_text(self, text: str) -> None:
        """
        Changes the label text content.
        
        Args:
            text (str): New text to display.
        """
        self.widget.configure(text=text)

    def get_text(self) -> str:
        """
        Returns the current label text.
        
        Returns:
            str: Current text content.
        """
        return self.widget.cget("text")

    def configure(self, **kwargs) -> None:
        """Dynamically updates widget properties."""
        self.widget.configure(**kwargs)

    def get_current_coord(self) -> typing.Tuple[int, int]:
        """
        Returns the current pixel coordinates of the label.
        
        Returns:
            tuple: (x, y) in pixels.
        """
        return self.widget.winfo_x(), self.widget.winfo_y()