import typing

class Table:
    """
    Table widget for displaying tabular data.
    """
    def __init__(self, 
                 backend: typing.Any, 
                 x: int, 
                 y: int, 
                 w: int, 
                 h: int, 
                 columns: typing.List[str], 
                 data: typing.List[typing.List[typing.Any]]) -> None:
        """
        Initializes the Table widget.
        
        Args:
            backend: Backend instance.
            x, y, w, h: Pixel position and dimensions.
            columns: List of column header names.
            data: List of data rows.
        """
        self.widget = backend.create_table(x, y, w, h, columns, data)

    def get_current_coord(self) -> typing.Tuple[int, int]:
        """
        Returns the current pixel coordinates of the table.
        
        Returns:
            tuple: (x, y) in pixels.
        """
        return self.widget.winfo_x(), self.widget.winfo_y()