import SPGUI as ui
import math

# Inisialisasi aplikasi dengan ukuran 16x12 grid untuk layout yang lebih luas
app = ui.init(
    SIZE=[16, 12],
    title="SPGUI - Test Semua Widget",
    theme="dark",
    grid_bgcolor="#1a1a1a",
    grid_lncolor="#333333",
    gtp=60,
    show_grid=True,
    coord_color="#00ff00",
    show_coord=True
)

# ============================================
# ROW 0: TITLE
# ============================================
title_label = app.label(
    pos=[0, 0],
    size=[16, 1],
    text="🎨 SPGUI WIDGET TEST 🎨",
    align="center",
    text_size=16
)

# ============================================
# ROW 1-2: BUTTONS & COUNTER
# ============================================
click_counter = {"count": 0}
counter_label = app.label(
    pos=[0, 2],
    size=[3, 1],
    text="Klik: 0",
    align="center",
    text_size=12
)

def on_button_click():
    click_counter["count"] += 1
    counter_label.set_text(f"Klik: {click_counter['count']}")

button1 = app.btn(
    pos=[4, 2],
    size=[3, 1],
    text="Klik!",
    onclick=on_button_click
)

def show_info():
    app.message("Info", "Ini adalah message box!", "info")

button2 = app.btn(
    pos=[7, 2],
    size=[3, 1],
    text="Info",
    onclick=show_info
)

# Theme state tracker
current_theme = {"mode": "dark"}

def switch_theme():
    if current_theme["mode"] == "dark":
        app.set_theme("light")
        current_theme["mode"] = "light"
    else:
        app.set_theme("dark")
        current_theme["mode"] = "dark"

theme_btn = app.btn(
    pos=[10, 2],
    size=[3, 1],
    text="Theme",
    onclick=switch_theme
)

def on_file_selected(filepath):
    filename = filepath.split("/")[-1] if "/" in filepath else filepath.split("\\")[-1]
    counter_label.set_text(f"File: {filename[:8]}")

open_btn = app.btn(
    pos=[13, 2],
    size=[3, 1],
    text="Open File",
    onclick=lambda: app.open_file_dialog(on_file_selected)
)

# ============================================
# ROW 3: TEXT INPUT
# ============================================
input_label = app.label(
    pos=[0, 3],
    size=[2, 1],
    text="Text Input:",
    align="left",
    text_size=11
)

input_display = app.label(
    pos=[3, 3],
    size=[4, 1],
    text="-",
    align="left"
)

def on_input_change(text):
    input_display.set_text(text[:20] if text else "-")

text_input = app.input(
    pos=[7, 3],
    size=[9, 1],
    placeholder="Ketik sesuatu di sini...",
    onchange=on_input_change
)

# ============================================
# ROW 4: CHECKBOX & NUMBER
# ============================================
checkbox_label = app.label(
    pos=[0, 5],
    size=[2, 1],
    text="Checkbox:",
    align="left",
    text_size=11
)

checkbox_status = app.label(
    pos=[3, 5],
    size=[2, 1],
    text="Off ✗",
    align="left"
)

def on_checkbox_change(checked):
    checkbox_status.set_text("On ✓" if checked else "Off ✗")

checkbox1 = app.checkbox(
    pos=[5, 5],
    text="Enable Feature",
    onchange=on_checkbox_change
)

number_label = app.label(
    pos=[9, 5],
    size=[3, 1],
    text="Num: 50",
    align="center"
)

def on_number_change(value):
    number_label.set_text(f"Num: {value}")

number_input = app.number(
    pos=[12, 5],
    size=[4, 1],
    min=0,
    max=100,
    onchange=on_number_change
)

# ============================================
# ROW 5.5: DROPDOWN
# ============================================
dropdown_label = app.label(
    pos=[0, 6],
    size=[2, 1],
    text="Language:",
    align="left",
    text_size=11
)

dropdown_display = app.label(
    pos=[3, 6],
    size=[4, 1],
    text="-",
    align="left"
)

def on_dropdown_change(selected):
    dropdown_display.set_text(selected)

dropdown1 = app.dropdown(
    pos=[7, 6],
    size=[9, 1],
    options=["Python", "JavaScript", "Java", "C++", "Go", "Rust"],
    onchange=on_dropdown_change
)

# ============================================
# ROW 7: SLIDER HORIZONTAL
# ============================================
slider_label = app.label(
    pos=[0, 8],
    size=[3, 1],
    text="Slider: 50",
    align="left",
    text_size=11
)

def on_slider_change(value):
    slider_label.set_text(f"Slider: {int(value)}")

slider_h = app.slider(
    pos=[3, 8],
    size=[13, 1],
    withrange=[0, 100],
    orientation="horizontal",
    onchange=on_slider_change
)

# ============================================
# ROW 8.5-10: PLOT & SLIDER VERTICAL
# ============================================
x_values = list(range(0, 360, 30))
y_values = [math.sin(math.radians(x)) for x in range(0, 360, 30)]

plot1 = app.plot(
    pos=[0, 9],
    size=[13, 3],
    type="line",
    data=(x_values, y_values)
)

slider_v = app.slider(
    pos=[14, 9],
    size=[1, 3],
    withrange=[0, 100],
    orientation="vertical"
)

slider_v_label = app.label(
    pos=[15, 9],
    size=[1, 3],
    text="V\nE\nR\nT",
    align="center",
    text_size=9
)

# Update plot dinamis
plot_counter = {"offset": 0}

def update_plot():
    plot_counter["offset"] += 30
    new_x = list(range(0, 360, 30))
    new_y = [math.sin(math.radians(x + plot_counter["offset"])) for x in range(0, 360, 30)]
    plot1.update((new_x, new_y))
    app.wait(10, update_plot)

app.wait(10, update_plot)



# ============================================
# MAIN LOOP
# ============================================
if __name__ == "__main__":
    print("=" * 60)
    print(f"SPGUI App Started - Grid: {app.get_window_size()}")
    print("✅ Semua widget berhasil dimuat dengan konversi integer otomatis!")
    print("=" * 60)
    app.run()