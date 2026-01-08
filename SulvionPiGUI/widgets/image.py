import typing

class Image:
    """
    Image widget for displaying graphic files on the grid.
    """
    def __init__(self, 
                 backend: typing.Any, 
                 x: int, 
                 y: int, 
                 w: int, 
                 h: int, 
                 src: str, 
                 fit: str = "stretch") -> None:
        """
        Initializes the Image widget.
        
        Args:
            backend: Backend instance.
            x, y, w, h: Pixel position and dimensions.
            src: Path to the local image file.
            fit: Resizing mode ("stretch").
        """
        self.widget = backend.create_image(x, y, w, h, src, fit=fit)

    def get_current_coord(self) -> typing.Tuple[int, int]:
        """
        Returns the current pixel coordinates of the image.
        
        Returns:
            tuple: (x, y) in pixels.
        """
        return (self.widget.winfo_x(), self.widget.winfo_y())