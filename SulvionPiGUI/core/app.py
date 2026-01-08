from .grid import GridSystem
from .debug import DebugLayer
from ..backend.customtk import BackendCustomTK
from ..widgets.button import Button
from ..widgets.label import Label
from ..widgets.input import Input
from ..widgets.checkbox import CheckBox
from ..widgets.dropdown import Dropdown
from ..widgets.image import Image
from ..widgets.plot import Plot
from ..widgets.table import Table
from ..widgets.slider import Slider
import typing


class App:
    """
    Main class for managing a SulvionPiGUI application.
    Integrates the GridSystem, Backend, and Widgets into a single easy-to-use interface.
    """
    def __init__(self, 
                 size: typing.List[typing.Union[int, float]] = [10, 10], 
                 gtp: int = 50, 
                 title: str = "SulvionPiGUI App", 
                 show_grid: bool = False,
                 grid_bgcolor: typing.Optional[str] = None, 
                 grid_lncolor: str = "gray30", 
                 text_color: str = "gray50", 
                 text_coord: bool = True,
                 theme: str = "dark") -> None:
        """
        Initializes the SPGUI application.
        
        Args:
            size: Grid size as [width, height].
            gtp: Grid-to-Pixel factor (the size of one grid square).
            title: The window title.
            show_grid: Displays the helper grid if True.
            grid_bgcolor: Grid background color.
            grid_lncolor: Color of the grid lines.
            text_color: Color of the grid coordinate text.
            text_coord: Displays coordinate numbers on the grid if True.
            theme: Application theme ("dark" or "light").
        """
        self.size_grid = [int(s) for s in size]
        self.gtp = int(gtp)
        self.title = title
        self.show_grid = show_grid
        
        self.grid_system = GridSystem(gtp=gtp)
        width, height = self.grid_system.get_window_size(size)
        
        self.backend = BackendCustomTK(title, width, height, theme=theme)
        
        if self.show_grid:
            self.debug_layer = DebugLayer(
                self.backend, 
                self.grid_system, 
                self.size_grid,
                bgcolor=grid_bgcolor,
                lncolor=grid_lncolor,
                txtcolor=text_color,
                show_coords=text_coord
            )
            self.debug_layer.draw()

    def run(self) -> None:
        """Runs the application and starts the main event loop."""
        self.backend.run()

    def get_window_size(self) -> typing.List[int]:
        """Gets the window size in grid units."""
        return self.size_grid

    def btn(self, 
            pos: typing.List[typing.Union[int, float]], 
            size: typing.List[typing.Union[int, float]] = [2, 1], 
            text: str = "Button", 
            onclick: typing.Optional[typing.Callable] = None, 
            value: typing.Optional[typing.Any] = None,
            text_size: typing.Optional[int] = None,
            text_font: typing.Optional[str] = None,
            align: typing.Literal["center", "left", "right", "top", "bottom"] = "center") -> Button:
        """
        Creates an interactive button.
        
        Args:
            pos: Grid coordinates [x, y].
            size: Button size in grid units [width, height].
            text: Label text on the button.
            onclick: Function to call when the button is clicked.
            value: Argument to pass to the onclick function (optional).
            text_size: Text font size.
            text_font: Text font name.
            align: Text alignment ("center", "left", etc.).
        """
        # Pastikan integer
        pos = [int(p) for p in pos]
        size = [int(s) for s in size]
        
        px_pos = self.grid_system.to_pixels(pos)
        px_size = self.grid_system.dim_to_pixels(size)
        
        # Bungkus command jika ada value
        command = onclick
        if value is not None and onclick is not None:
            command = lambda: onclick(value)
            
        return Button(
            self.backend,
            x=px_pos[0],
            y=px_pos[1],
            w=px_size[0],
            h=px_size[1],
            text=text,
            command=command,
            text_size=text_size,
            text_font=text_font,
            align=align
        )

    button = btn # Alias
    
    def label(self, 
              pos: typing.List[typing.Union[int, float]], 
              size: typing.List[typing.Union[int, float]] = [2, 1], 
              text: str = "Label", 
              align: typing.Literal["center", "left", "right", "top", "bottom"] = "center",
              text_size: typing.Optional[int] = None,
              text_font: typing.Optional[str] = None) -> Label:
        """
        Creates a static text label.
        
        Args:
            pos: Grid coordinates [x, y].
            size: Label size in grid units [width, height].
            text: Label content text.
            align: Text alignment.
            text_size: Font size.
            text_font: Font family name.
        """
        pos = [int(p) for p in pos]
        size = [int(s) for s in size]
        
        px_pos = self.grid_system.to_pixels(pos)
        px_size = self.grid_system.dim_to_pixels(size)
        
        return Label(
            self.backend,
            x=px_pos[0],
            y=px_pos[1],
            w=px_size[0],
            h=px_size[1],
            text=text,
            align=align,
            text_size=text_size,
            text_font=text_font
        )
    
    text = label  # Alias
    write = label # Alias

    def input(self, 
              pos: typing.List[typing.Union[int, float]], 
              size: typing.List[typing.Union[int, float]] = [2, 1], 
              placeholder: str = "", 
              onchange: typing.Optional[typing.Callable[[str], None]] = None,
              text_size: typing.Optional[int] = None,
              text_font: typing.Optional[str] = None) -> Input:
        """
        Creates a text input (Entry) widget.
        
        Args:
            pos: Grid coordinates [x, y].
            size: Input size in grid units [width, height].
            placeholder: Hint text shown when empty.
            onchange: Callback function called when text is modified.
        """
        pos = [int(p) for p in pos]
        size = [int(s) for s in size]
        
        px_pos = self.grid_system.to_pixels(pos)
        px_size = self.grid_system.dim_to_pixels(size)
        font = (text_font, text_size) if text_font or text_size else None
        return Input(self.backend, px_pos[0], px_pos[1], px_size[0], px_size[1], 
                    placeholder=placeholder, onchange=onchange, font=font)

    def checkbox(self, 
                 pos: typing.List[typing.Union[int, float]], 
                 text: str = "CheckBox", 
                 onchange: typing.Optional[typing.Callable[[bool], None]] = None,
                 text_size: typing.Optional[int] = None,
                 text_font: typing.Optional[str] = None) -> CheckBox:
        """
        Creates a checkbox widget.
        
        Args:
            pos: Grid coordinates [x, y].
            text: Text label.
            onchange: Callback when checkbox status changes.
        """
        pos = [int(p) for p in pos]
        px_pos = self.grid_system.to_pixels(pos)
        font = (text_font, text_size) if text_font or text_size else None
        return CheckBox(self.backend, px_pos[0], px_pos[1], text, onchange=onchange, font=font)

    def dropdown(self, 
                 pos: typing.List[typing.Union[int, float]], 
                 size: typing.List[typing.Union[int, float]] = [2, 1], 
                 options: typing.List[str] = ["Option 1"], 
                 onchange: typing.Optional[typing.Callable[[str], None]] = None,
                 text_size: typing.Optional[int] = None,
                 text_font: typing.Optional[str] = None) -> Dropdown:
        """
        Creates a dropdown selection menu.
        
        Args:
            pos: Grid coordinates [x, y].
            size: Dropdown size in grid units [width, height].
            options: List of string options.
            onchange: Callback when an option is selected.
        """
        pos = [int(p) for p in pos]
        size = [int(s) for s in size]
        
        px_pos = self.grid_system.to_pixels(pos)
        px_size = self.grid_system.dim_to_pixels(size)
        font = (text_font, text_size) if text_font or text_size else None
        return Dropdown(self.backend, px_pos[0], px_pos[1], px_size[0], px_size[1], 
                       options=options, onchange=onchange, font=font)

    def slider(self, 
               pos: typing.List[typing.Union[int, float]], 
               size: typing.List[typing.Union[int, float]] = [4, 1], 
               withrange: typing.List[typing.Union[int, float]] = [0, 100], 
               orientation: typing.Literal["horizontal", "vertical"] = "horizontal",
               onchange: typing.Optional[typing.Callable[[float], None]] = None) -> Slider:
        """
        Creates a slider control widget.
        
        Args:
            pos: Grid coordinates [x, y].
            size: Slider size in grid units [width, height].
            withrange: Value range as [min, max].
            orientation: Orientation ("horizontal" or "vertical").
            onchange: Callback when the slider value changes.
        """
        pos = [int(p) for p in pos]
        size = [int(s) for s in size]
        withrange = [int(r) for r in withrange]
        
        px_pos = self.grid_system.to_pixels(pos)
        px_size = self.grid_system.dim_to_pixels(size)
        return Slider(self.backend, px_pos[0], px_pos[1], px_size[0], px_size[1], 
                     from_=withrange[0], to=withrange[1], orientation=orientation, onchange=onchange)

    def number(self, 
               pos: typing.List[typing.Union[int, float]], 
               size: typing.List[typing.Union[int, float]] = [2, 1], 
               min: int = 0, 
               max: int = 100, 
               onchange: typing.Optional[typing.Callable[[int], None]] = None) -> Input:
        """
        Creates a numeric-only input widget with filtering.
        
        Args:
            pos: Grid coordinates [x, y].
            size: Input size in grid units [width, height].
            min, max: Allowed value boundaries.
            onchange: Callback function called when valid numeric text is entered.
        """
        def filter_numbers(val: str):
            if val == "": return
            temp_val = val
            if val.startswith('-'): temp_val = val[1:]
            if not temp_val.isdigit(): return
            
            num = int(val)
            if num < min or num > max: return
            if onchange: onchange(num)
            
        return self.input(pos, size, placeholder=f"{min}-{max}", onchange=filter_numbers)

    def image(self, 
              pos: typing.List[typing.Union[int, float]], 
              size: typing.List[typing.Union[int, float]] = [2, 2], 
              src: str = "", 
              fit: str = "stretch") -> Image:
        """
        Displays an image on the grid.
        
        Args:
            pos: Grid coordinates [x, y].
            size: Image size in grid units [width, height].
            src: Path to the image file.
            fit: Resizing mode ("stretch", "contain").
        """
        pos = [int(p) for p in pos]
        size = [int(s) for s in size]
        
        px_pos = self.grid_system.to_pixels(pos)
        px_size = self.grid_system.dim_to_pixels(size)
        return Image(self.backend, px_pos[0], px_pos[1], px_size[0], px_size[1], src, fit=fit)

    def plot(self, 
             pos: typing.List[typing.Union[int, float]], 
             size: typing.List[typing.Union[int, float]] = [4, 3], 
             type: str = "line", 
             data: typing.Optional[typing.List] = None, 
             options: typing.Optional[typing.Dict] = None) -> Plot:
        """
        Creates a Matplotlib plot widget.
        
        Args:
            pos: Grid coordinates [x, y].
            size: Widget size in grid units [width, height].
            type: Plot type ("line", "bar").
            data: Initial plot data.
        """
        pos = [int(p) for p in pos]
        size = [int(s) for s in size]
        
        px_pos = self.grid_system.to_pixels(pos)
        px_size = self.grid_system.dim_to_pixels(size)
        return Plot(self.backend, px_pos[0], px_pos[1], px_size[0], px_size[1], 
                   p_type=type, data=data, options=options)

    def table(self, 
              pos: typing.List[typing.Union[int, float]], 
              size: typing.List[typing.Union[int, float]] = [4, 4], 
              columns: typing.List[str] = ["Col 1"], 
              data: typing.List[typing.List] = [[]]) -> Table:
        """
        Creates a data table widget.
        
        Args:
            pos: Grid coordinates [x, y].
            size: Widget size in grid units [width, height].
            columns: List of column header names.
            data: Initial data rows.
        """
        pos = [int(p) for p in pos]
        size = [int(s) for s in size]
        
        px_pos = self.grid_system.to_pixels(pos)
        px_size = self.grid_system.dim_to_pixels(size)
        return Table(self.backend, px_pos[0], px_pos[1], px_size[0], px_size[1], columns, data)

    # Event binding
    def on_key(self, key: str, func: typing.Callable[[], None]) -> None:
        """Binds a keyboard key to a function."""
        self.backend.root.bind(f"<{key}>", lambda e: func())

    def on_mouse_click(self, func: typing.Callable[[], None]) -> None:
        """Binds a global mouse click to a function."""
        self.backend.root.bind("<Button-1>", lambda e: func())

    def on_mouse_move(self, func: typing.Callable[[], None]) -> None:
        """Binds global mouse movement to a function."""
        self.backend.root.bind("<Motion>", lambda e: func())

    def message(self, title: str, msg: str, msgtype: typing.Literal["info", "warning", "error"] = "info") -> None:
        """Displays a message box popup."""
        self.backend.message(title, msg, msgtype)

    def wait(self, ms: int, func: typing.Callable[[], None]) -> None:
        """Executes a function after a specified time delay (milliseconds)."""
        self.backend.root.after(ms, func)

    def open_file_dialog(self, on_select: typing.Optional[typing.Callable[[str], None]] = None) -> typing.Optional[str]:
        """Opens a file selection dialog."""
        file = self.backend.open_file()
        if file and on_select: on_select(file)
        return file

    def save_file_dialog(self, on_select: typing.Optional[typing.Callable[[str], None]] = None) -> typing.Optional[str]:
        """Opens a save file dialog."""
        file = self.backend.save_file()
        if file and on_select: on_select(file)
        return file

    def set_theme(self, theme: str) -> None:
        """Changes the application theme dynamically."""
        self.backend.set_theme(theme)

    def make_draggable(self, widget_wrapper: typing.Any) -> None:
        """Makes a widget draggable via mouse with grid-snapping."""
        widget = widget_wrapper.widget
        import customtkinter as ctk
        
        state = {"start_root_x": 0, "start_root_y": 0, "start_w_x": 0, "start_w_y": 0, "moved": False}

        def on_press(event):
            state["start_root_x"] = event.x_root
            state["start_root_y"] = event.y_root
            state["scaling"] = ctk.ScalingTracker.get_window_scaling(self.backend.root)
            scaling = state["scaling"]
            state["start_w_x"] = widget.winfo_x() / scaling
            state["start_w_y"] = widget.winfo_y() / scaling
            state["moved"] = False
            try: self.backend.root.tk.call('raise', widget._w)
            except: pass

        def on_motion(event):
            scaling = state.get("scaling", 1.0)
            dx = (event.x_root - state["start_root_x"]) / scaling
            dy = (event.y_root - state["start_root_y"]) / scaling
            if abs(dx) > 3 or abs(dy) > 3: state["moved"] = True
            new_x = state["start_w_x"] + dx
            new_y = state["start_w_y"] + dy
            widget.place(x=new_x, y=new_y)
            self.backend.root.update_idletasks()

        def on_release(event):
            if not state["moved"]:
                if hasattr(widget, "invoke"): widget.invoke()
                return
            scaling = ctk.ScalingTracker.get_window_scaling(self.backend.root)
            curr_x, curr_y = widget.winfo_x() / scaling, widget.winfo_y() / scaling
            grid_x, grid_y = round(curr_x / self.gtp), round(curr_y / self.gtp)
            widget.place(x=grid_x * self.gtp, y=grid_y * self.gtp)

        self.backend.bind_event(widget, "<Button-1>", on_press)
        self.backend.bind_event(widget, "<B1-Motion>", on_motion)
        self.backend.bind_event(widget, "<ButtonRelease-1>", on_release)
        
        def bind_recursive(w):
            for child in w.winfo_children():
                self.backend.bind_event(child, "<Button-1>", on_press)
                self.backend.bind_event(child, "<B1-Motion>", on_motion)
                self.backend.bind_event(child, "<ButtonRelease-1>", on_release)
                bind_recursive(child)
        bind_recursive(widget)

    def make_resizable(self, widget_wrapper: typing.Any) -> None:
        """Adds a handle in the bottom-right corner to allow widget resizing."""
        widget = widget_wrapper.widget
        import customtkinter as ctk
        handle = ctk.CTkFrame(widget, width=14, height=14, fg_color="gray40", corner_radius=4, cursor="size_nw_se", border_width=1, border_color="gray20")
        handle.place(relx=1.0, rely=1.0, anchor="se", x=-2, y=-2)

        state = {"start_root_x": 0, "start_root_y": 0, "start_w": 0, "start_h": 0}

        def on_press(event):
            state["start_root_x"], state["start_root_y"] = event.x_root, event.y_root
            scaling = ctk.ScalingTracker.get_window_scaling(self.backend.root)
            state["start_w"], state["start_h"] = widget.winfo_width() / scaling, widget.winfo_height() / scaling
            try: self.backend.root.tk.call('raise', widget._w)
            except: pass

        def on_motion(event):
            scaling = ctk.ScalingTracker.get_window_scaling(self.backend.root)
            dx, dy = (event.x_root - state["start_root_x"]) / scaling, (event.y_root - state["start_root_y"]) / scaling
            new_w, new_h = max(self.gtp, state["start_w"] + dx), max(self.gtp, state["start_h"] + dy)
            widget.configure(width=new_w, height=new_h)

        def on_release(event):
            scaling = ctk.ScalingTracker.get_window_scaling(self.backend.root)
            curr_w, curr_h = widget.winfo_width() / scaling, widget.winfo_height() / scaling
            grid_w, grid_h = max(1, round(curr_w / self.gtp)), max(1, round(curr_h / self.gtp))
            widget.configure(width=grid_w * self.gtp, height=grid_h * self.gtp)

        handle.bind("<Button-1>", on_press)
        handle.bind("<B1-Motion>", on_motion)
        handle.bind("<ButtonRelease-1>", on_release)
