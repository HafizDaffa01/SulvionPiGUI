import customtkinter as ctk
import typing
from .grid import GridSystem

class DebugLayer:
    """
    Handles drawing the visual debug overlay (grid).
    Automatically accounts for CustomTkinter scaling factors to ensure
    grid lines align perfectly with widgets on High-DPI displays.
    """
    def __init__(self, 
                 backend: typing.Any, 
                 grid_system: GridSystem, 
                 size_grid: typing.List[int], 
                 bgcolor: typing.Optional[str] = None, 
                 lncolor: str = "gray30", 
                 txtcolor: str = "gray50", 
                 show_coords: bool = True) -> None:
        """
        Initializes the DebugLayer.
        
        Args:
            backend: Instance of the UI backend.
            grid_system: GridSystem instance for pixel calculations.
            size_grid: Grid size as [cols, rows].
            bgcolor: Optional grid background color.
            lncolor: Grid line color.
            txtcolor: Coordinate text color.
            show_coords: Whether to display coordinate labels.
        """
        self.backend = backend
        self.grid_system = grid_system
        self.size_grid = size_grid
        self.bgcolor = bgcolor
        self.lncolor = lncolor
        self.txtcolor = txtcolor
        self.show_coords = show_coords
        self.canvas: typing.Optional[typing.Any] = None

    def create_canvas(self) -> typing.Any:
        """
        Creates a canvas for the debug overlay that covers the entire window.
        
        Returns:
            Canvas object.
        """
        # Using ctk.CTkCanvas for better theme integration
        canvas = ctk.CTkCanvas(self.backend.root, highlightthickness=0)
        canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        return canvas

    def draw(self) -> None:
        """
        Initializes and draws the debug grid.
        Uses after() to ensure window geometry is finalized by the OS.
        """
        self.backend.root.after(150, self._actual_draw)

    def _actual_draw(self) -> None:
        """
        Core logic for drawing the grid. Calculates scaling, creates the canvas,
        and draws lines plus coordinates.
        """
        # 1. Get accurate scaling (High-DPI)
        try:
            scaling = ctk.ScalingTracker.get_window_scaling(self.backend.root)
        except:
            scaling = 1.0
            
        # 2. Setup or refresh Canvas
        if self.canvas:
            self.canvas.destroy()
            
        # Get unscaled pixels to pass to backend
        grid_w_px, grid_h_px = self.grid_system.get_window_size(self.size_grid)
        self.canvas = self.backend.create_canvas(grid_w_px, grid_h_px)
        
        # Apply background color
        if self.bgcolor is None:
            # Use fixed standard CTk colors for standard Canvas compatibility
            bg_color = "#242424" if ctk.get_appearance_mode() == "Dark" else "#ebebeb"
        else:
            bg_color = self.bgcolor
        self.canvas.configure(bg=bg_color)
        
        # 3. Draw Grid Lines
        # Wait for canvas to be placed and sized correctly by CTk
        self.canvas.update()
        canv_w = self.canvas.winfo_width()
        canv_h = self.canvas.winfo_height()
        
        # Drawing in physical pixels
        gtp = self.grid_system.gtp * scaling
        
        # Vertical Lines
        num_cols = int(canv_w / gtp) + 1
        for x in range(max(num_cols, self.size_grid[0] + 1)):
            px = x * gtp
            self.canvas.create_line(px, 0, px, canv_h, fill=self.lncolor, dash=(2, 4))
            
        # Horizontal Lines
        num_rows = int(canv_h / gtp) + 1
        for y in range(max(num_rows, self.size_grid[1] + 1)):
            py = y * gtp
            self.canvas.create_line(0, py, canv_w, py, fill=self.lncolor, dash=(2, 4))

        # Draw Coordinate labels (0-based)
        if self.show_coords:
            font_size = int(8 * scaling)
            for x in range(self.size_grid[0]):
                for y in range(self.size_grid[1]):
                    px = (x * gtp) + (4 * scaling)
                    py = (y * gtp) + (2 * scaling)
                    # Display x,y for standard 0-based addressing
                    self.canvas.create_text(
                        px, py, text=f"{x},{y}", anchor="nw", 
                        fill=self.txtcolor, font=("Arial", font_size)
                    )

        # 4. Push to background so it doesn't obstruct widgets
        self.backend.root.after(10, lambda: self.backend.root.tk.call('lower', self.canvas._w))
