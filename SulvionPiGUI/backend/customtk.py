import customtkinter as ctk
import typing   

class BackendCustomTK:
    """
    CustomTkinter implementation for the SulvionPiGUI backend.
    Translates high-level widget requests into CTk objects.
    """
    def __init__(self, title: str, width: int, height: int, theme: str = "dark") -> None:
        """
        Initializes the CustomTkinter backend.
        
        Args:
            title: Window title.
            width: Window width in pixels.
            height: Window height in pixels.
            theme: Appearance theme ("dark" or "light").
        """
        ctk.set_appearance_mode(theme)
        self.root = ctk.CTk()
        self.root.title(title)
        
        # Set geometry and update to ensure scaling is applied correctly
        self.root.geometry(f"{width}x{height}")
        self.root.update_idletasks() # Force geometry update
        
        self.root.resizable(False, False)
        
        # Handle clean exit to prevent Matplotlib-related errors
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self) -> None:
        """Handles cleaning up resources before the window is destroyed."""
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass

    def run(self) -> None:
        """Starts the main event loop (mainloop)."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_close()
        except Exception:
            # Join silently on closing errors
            pass

    def set_theme(self, theme: str) -> None:
        """
        Dynamically changes the appearance theme.
        
        Args:
            theme: Theme name ("dark" or "light").
        """
        ctk.set_appearance_mode(theme)

    def create_button(self, x: int, y: int, w: int, h: int, text: str, command: typing.Optional[typing.Callable], font: typing.Optional[typing.Tuple[str, int]] = None, anchor: str = "center") -> ctk.CTkButton:
        """
        Creates a CTkButton with pixel coordinates.
        
        Args:
            x, y: Pixel position.
            w, h: Pixel dimensions.
            text: Button label.
            command: Callback function on click.
            font: Tuple of (font_name, size).
            anchor: Text alignment.
        """
        anchor_map = {"center": "center", "left": "w", "right": "e", "top": "n", "bottom": "s"}
        tk_anchor = anchor_map.get(anchor, "center")
        
        btn = ctk.CTkButton(self.root, text=text, command=command, width=w, height=h, font=font, anchor=tk_anchor)
        btn.place(x=x, y=y)
        return btn

    def create_label(self, x: int, y: int, w: int, h: int, text: str, anchor: str = "center", font: typing.Optional[typing.Tuple[str, int]] = None) -> ctk.CTkLabel:
        """
        Creates a CTkLabel with pixel coordinates.
        
        Args:
            x, y, w, h: Pixel position and dimensions.
            text: Label content.
            anchor: Text alignment.
            font: Font settings.
        """
        anchor_map = {"center": "center", "left": "w", "right": "e", "top": "n", "bottom": "s"}
        tk_anchor = anchor_map.get(anchor, "center")
        
        lbl = ctk.CTkLabel(self.root, text=text, anchor=tk_anchor, width=w, height=h, font=font)
        lbl.place(x=x, y=y)
        return lbl

    def create_entry(self, x: int, y: int, w: int, h: int, placeholder: str = "", onchange: typing.Optional[typing.Callable[[str], None]] = None, font: typing.Optional[typing.Tuple[str, int]] = None) -> ctk.CTkEntry:
        """
        Creates a CTkEntry (text input).
        
        Args:
            x, y, w, h: Pixel position and dimensions.
            placeholder: Hint text inside the input.
            onchange: Callback when text is modified.
        """
        entry = ctk.CTkEntry(self.root, placeholder_text=placeholder, width=w, height=h, font=font)
        entry.place(x=x, y=y)
        if onchange:
            entry.bind("<KeyRelease>", lambda e: onchange(entry.get()))
        return entry

    def create_checkbox(self, x: int, y: int, text: str, onchange: typing.Optional[typing.Callable[[bool], None]] = None, font: typing.Optional[typing.Tuple[str, int]] = None) -> ctk.CTkCheckBox:
        """
        Creates a CTkCheckBox.
        
        Args:
            x, y: Pixel position.
            text: Text label next to the checkbox.
            onchange: Callback when status changes (returns boolean).
        """
        cb = ctk.CTkCheckBox(self.root, text=text, command=lambda: onchange(bool(cb.get())) if onchange else None, font=font)
        cb.place(x=x, y=y)
        return cb

    def create_optionmenu(self, x: int, y: int, w: int, h: int, values: typing.List[str], onchange: typing.Optional[typing.Callable[[str], None]] = None, font: typing.Optional[typing.Tuple[str, int]] = None) -> ctk.CTkOptionMenu:
        """
        Creates a CTkOptionMenu (dropdown).
        
        Args:
            x, y, w, h: Pixel position and dimensions.
            values: List of selectable options.
            onchange: Callback when selection changes.
        """
        om = ctk.CTkOptionMenu(self.root, values=values, command=onchange, width=w, height=h, font=font)
        om.place(x=x, y=y)
        return om

    def create_slider(self, x: int, y: int, w: int, h: int, from_: float = 0, to: float = 1, orientation: str = "horizontal", onchange: typing.Optional[typing.Callable[[float], None]] = None) -> ctk.CTkSlider:
        """
        Creates a CTkSlider.
        
        Args:
            x, y, w, h: Pixel position and dimensions.
            from_, to: Value range boundaries.
            orientation: Slider orientation ("horizontal" or "vertical").
            onchange: Callback when value changes.
        """
        slider = ctk.CTkSlider(self.root, width=w, height=h, from_=from_, to=to, orientation=orientation, command=onchange)
        slider.place(x=x, y=y)
        return slider

    def create_image(self, x: int, y: int, w: int, h: int, src: str, fit: str = "stretch") -> ctk.CTkLabel:
        """
        Creates a CTkLabel containing a CTkImage.
        
        Args:
            x, y, w, h: Pixel position and dimensions.
            src: Path to the image file.
        """
        from PIL import Image
        pil_img = Image.open(src)
        ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(w, h))
        lbl = ctk.CTkLabel(self.root, image=ctk_img, text="", width=w, height=h)
        lbl.place(x=x, y=y)
        return lbl

    def create_plot(self, x: int, y: int, w: int, h: int, p_type: str = "line", data: typing.Optional[typing.List] = None, options: typing.Optional[typing.Dict] = None) -> typing.Dict[str, typing.Any]:
        """
        Creates a Matplotlib plot inside a CTk frame.
        
        Returns:
            Dict containing the frame widget and an update function.
        """
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
        frame = ctk.CTkFrame(self.root, width=w, height=h, fg_color="transparent", border_width=0)
        frame.place(x=x, y=y)
        
        # Theme-aware colors
        is_dark = ctk.get_appearance_mode() == "Dark"
        bg_color = '#1a1a1a' if is_dark else '#f0f0f0'
        fg_color = 'white' if is_dark else 'black'
        
        fig = Figure(figsize=(w/100, h/100), dpi=100)
        ax = fig.add_subplot(111)
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        ax.tick_params(colors=fg_color, labelsize=8)
        for spine in ax.spines.values():
            spine.set_color(fg_color)
            
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)

        def update_plot(data):
            ax.clear()
            ax.set_facecolor(bg_color)
            ax.tick_params(colors=fg_color, labelsize=8)
            ax.grid(True, color='gray', linestyle='--', alpha=0.3)
            for spine in ax.spines.values():
                spine.set_color(fg_color)
            
            # Support both Y-value lists or (X, Y) tuples
            if isinstance(data, tuple) and len(data) == 2:
                x_data, y_data = data
                if p_type == "line":
                    ax.plot(x_data, y_data, color='cyan', linewidth=2)
                elif p_type == "bar":
                    ax.bar(x_data, y_data, color='cyan')
            else:
                if p_type == "line":
                    ax.plot(data, color='cyan', linewidth=2)
                elif p_type == "bar":
                    ax.bar(range(len(data)), data, color='cyan')
            
            canvas.draw()

        if data:
            update_plot(data)
            
        frame.pack_propagate(False)
        
        return {"widget": frame, "update": update_plot}

    def create_table(self, x: int, y: int, w: int, h: int, columns: typing.List[str], data: typing.List[typing.List]) -> ctk.CTkFrame:
        """
        Creates a table using ttk.Treeview.
        
        Args:
            x, y, w, h: Pixel position and dimensions.
            columns: Column headers.
            data: List of data rows.
        """
        from tkinter import ttk
        frame = ctk.CTkFrame(self.root, width=w, height=h)
        frame.place(x=x, y=y)
        
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=int(w/len(columns)))
            
        for row in data:
            tree.insert("", "end", values=row)
            
        tree.pack(fill="both", expand=True)
        return frame

    def create_canvas(self, width: int, height: int) -> typing.Any:
        """Creates a standard tkinter canvas for the debug overlay."""
        import tkinter as tk
        canvas = tk.Canvas(self.root, highlightthickness=0, borderwidth=0)
        canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        return canvas

    def bind_event(self, widget: typing.Any, event_name: str, callback: typing.Callable) -> None:
        """Binds a tkinter event to a specific widget."""
        widget.bind(event_name, callback)

    def open_file(self) -> typing.Optional[str]:
        """Opens a file selection dialog."""
        from tkinter import filedialog
        return filedialog.askopenfilename()

    def save_file(self) -> typing.Optional[str]:
        """Opens a file save dialog."""
        from tkinter import filedialog
        return filedialog.asksaveasfilename()

    def message(self, title: str, msg: str, msgtype: typing.Literal["info", "warning", "error"] = "info") -> None:
        """Displays a message box dialog."""
        from tkinter import messagebox

        match msgtype:
            case "info":
                messagebox.showinfo(title, msg)
            case "warning":
                messagebox.showwarning(title, msg)
            case "error":
                messagebox.showerror(title, msg)
