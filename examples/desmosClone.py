import SPGUI as ui
import math

# Initialize the Graphing App
app = ui.init(
    SIZE=[12, 14],
    title="Grapher (Desmos Clone)",
    theme="dark",
    debug_mode=True
)

# Header
app.text(pos=[1, 0.5], size=[12, 1.5], text="Sulvion Grapher", text_size=32, text_font="Outfit", align="center")

# Define the function BEFORE creating inputs so we can pass it to onchange
def graph_equation(expression=None):
    if not hasattr(app, "grapher_initialized"): return
    
    if expression is None:
        expression = eq_input.get_value()
    
    if not expression.strip():
        return

    try:
        # Get Range
        try:
            xmin = float(x_min_input.get_value())
            xmax = float(x_max_input.get_value())
        except:
            xmin, xmax = -10, 10

        # Preparation for calculation
        x_vals = []
        y_vals = []
        steps = 200
        step_size = (xmax - xmin) / steps
        
        # Safe Evaluation Context
        safe_dict = {
            "x": 0,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "sqrt": math.sqrt,
            "abs": abs,
            "pi": math.pi,
            "e": math.e,
            "log": math.log,
            "exp": math.exp,
            "pow": pow
        }

        # Calculate Points
        for i in range(steps + 1):
            curr_x = xmin + (i * step_size)
            safe_dict["x"] = curr_x
            
            # Replace ^ with ** for python style power
            clean_expr = expression.replace("^", "**")
            
            try:
                curr_y = eval(clean_expr, {"__builtins__": None}, safe_dict)
                x_vals.append(curr_x)
                y_vals.append(curr_y)
            except:
                continue
        
        if x_vals and y_vals:
            plotter.update((x_vals, y_vals))
            error_label.set_text("")
            error_label.configure(text_color="gray")
        else:
            error_label.set_text("No valid points to plot")
            error_label.configure(text_color="orange")

    except Exception as e:
        error_label.set_text(f"Error: {str(e)}")
        error_label.configure(text_color="#ff4444")

def on_input_change(val):
    graph_equation()

# Equation Input Section
app.text(pos=[1, 2.5], size=[2, 1], text="f(x) =", text_size=18, text_font="Outfit")
eq_input = app.input(pos=[3, 2.5], size=[10, 1], placeholder="e.g. sin(x) * x", text_size=16, onchange=on_input_change)

# Graph Range Section
app.text(pos=[1, 4], size=[2, 1], text="Range X:", text_size=14)
x_min_input = app.input(pos=[3, 4], size=[2, 1], placeholder="-10", onchange=on_input_change)
x_max_input = app.input(pos=[5, 4], size=[2, 1], placeholder="10", onchange=on_input_change)
x_min_input.set_value("-10")
x_max_input.set_value("10")

# Error Display
error_label = app.text(pos=[1, 5.2], size=[12, 0.8], text="", text_size=12)

# Plotter
plotter = app.plot(pos=[1, 6], size=[12, 9], type="line")

# Mark as initialized
app.grapher_initialized = True

# Initial Plot
if __name__ == "__main__":
    eq_input.set_value("sin(x) * x")
    app.wait(500, graph_equation)
    app.run()
