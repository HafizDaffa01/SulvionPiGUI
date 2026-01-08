import SPGUI as ui

# ============================================================================
# NUCLEAR REACTOR SIMULATOR - Pressurized Water Reactor (PWR)
# ============================================================================
# This simulator models a realistic PWR with proper physics including:
# - Neutron flux and reactivity
# - Temperature and pressure dynamics
# - Control rod positioning
# - Coolant flow systems
# - Safety systems and SCRAM
# ============================================================================

class ReactorPhysics:
    """Handles all nuclear reactor physics calculations"""
    
    def __init__(self):
        # Core Parameters
        self.neutron_flux = 50.0  # % of maximum
        self.reactivity = 0.0  # in dollars ($)
        self.control_rod_position = 50.0  # % withdrawn (0=fully inserted, 100=fully withdrawn)
        
        # Thermal Parameters
        self.core_temp = 300.0  # °C
        self.coolant_temp_in = 280.0  # °C
        self.coolant_temp_out = 320.0  # °C
        self.coolant_flow = 100.0  # % of nominal
        
        # Pressure Parameters
        self.primary_pressure = 155.0  # bar (15.5 MPa)
        self.secondary_pressure = 70.0  # bar
        
        # Power Parameters
        self.thermal_power = 0.0  # MW
        self.electrical_power = 0.0  # MW
        self.max_thermal_power = 3000.0  # MW
        
        # Safety Parameters
        self.scram_active = False
        self.emergency_cooling = False
        self.xenon_poisoning = 0.0  # Xe-135 poisoning effect
        
        # Constants
        self.TEMP_COEFFICIENT = -0.003  # Negative temperature feedback ($/°C)
        self.XENON_BUILDUP_RATE = 0.001
        self.XENON_DECAY_RATE = 0.0002
        self.HEAT_CAPACITY = 50.0  # Thermal inertia
        
        # Time tracking
        self.time_step = 0.1  # seconds
        self.total_time = 0.0
        
    def calculate_reactivity(self):
        """Calculate total reactivity from all sources"""
        # Control rod reactivity (non-linear)
        rod_reactivity = -2.0 + (self.control_rod_position / 100.0) * 2.5
        
        # Temperature feedback (negative)
        temp_feedback = (self.core_temp - 300.0) * self.TEMP_COEFFICIENT
        
        # Xenon poisoning (negative)
        xenon_reactivity = -self.xenon_poisoning * 0.5
        
        # Total reactivity
        self.reactivity = rod_reactivity + temp_feedback + xenon_reactivity
        
        # SCRAM overrides everything
        if self.scram_active:
            self.reactivity = -5.0
            
        return self.reactivity
    
    def update_neutron_flux(self):
        """Update neutron flux based on reactivity"""
        # Neutron flux changes based on reactivity
        # Simplified point kinetics equation
        flux_change = self.reactivity * self.neutron_flux * 0.1
        
        self.neutron_flux += flux_change * self.time_step
        
        # Clamp flux
        self.neutron_flux = max(0.0, min(120.0, self.neutron_flux))
        
    def update_thermal_power(self):
        """Calculate thermal power from neutron flux"""
        # Power is proportional to neutron flux
        self.thermal_power = (self.neutron_flux / 100.0) * self.max_thermal_power
        
    def update_temperatures(self):
        """Update core and coolant temperatures"""
        # Heat generation from fission
        heat_generated = self.thermal_power / self.HEAT_CAPACITY
        
        # Heat removal by coolant
        heat_removed = (self.coolant_flow / 100.0) * (self.core_temp - self.coolant_temp_in) * 0.5
        
        # Emergency cooling
        if self.emergency_cooling:
            heat_removed *= 2.0
        
        # Update core temperature
        temp_change = (heat_generated - heat_removed) * self.time_step
        self.core_temp += temp_change
        
        # Update coolant outlet temperature
        if self.coolant_flow > 0:
            self.coolant_temp_out = self.coolant_temp_in + (heat_removed / (self.coolant_flow / 100.0))
        
        # Clamp temperatures
        self.core_temp = max(20.0, min(2000.0, self.core_temp))
        self.coolant_temp_out = max(20.0, min(400.0, self.coolant_temp_out))
        
    def update_pressure(self):
        """Update primary and secondary pressure"""
        # Pressure increases with temperature
        temp_factor = (self.core_temp - 300.0) / 100.0
        self.primary_pressure = 155.0 + temp_factor * 5.0
        
        # Secondary pressure based on heat transfer
        heat_transfer = (self.coolant_temp_out - self.coolant_temp_in) * (self.coolant_flow / 100.0)
        self.secondary_pressure = 70.0 + heat_transfer * 0.1
        
        # Clamp pressures
        self.primary_pressure = max(0.0, min(200.0, self.primary_pressure))
        self.secondary_pressure = max(0.0, min(100.0, self.secondary_pressure))
        
    def update_xenon(self):
        """Update Xenon-135 poisoning"""
        # Xenon builds up during operation
        if self.neutron_flux > 10.0:
            buildup = self.XENON_BUILDUP_RATE * (self.neutron_flux / 100.0)
            self.xenon_poisoning += buildup * self.time_step
        
        # Xenon decays naturally
        decay = self.XENON_DECAY_RATE * self.xenon_poisoning
        self.xenon_poisoning -= decay * self.time_step
        
        # Clamp xenon
        self.xenon_poisoning = max(0.0, min(3.0, self.xenon_poisoning))
        
    def calculate_electrical_power(self):
        """Calculate electrical output (33% efficiency)"""
        self.electrical_power = self.thermal_power * 0.33
        
    def check_safety_limits(self):
        """Check if safety limits are exceeded"""
        alarms = []
        
        if self.core_temp > 600.0:
            alarms.append("HIGH CORE TEMP")
        if self.primary_pressure > 175.0:
            alarms.append("HIGH PRESSURE")
        if self.neutron_flux > 110.0:
            alarms.append("HIGH FLUX")
        if self.coolant_flow < 50.0 and self.thermal_power > 500.0:
            alarms.append("LOW COOLANT FLOW")
            
        # Auto SCRAM conditions
        if self.core_temp > 800.0 or self.primary_pressure > 185.0 or self.neutron_flux > 115.0:
            self.scram_active = True
            alarms.append("AUTO SCRAM ACTIVATED")
            
        return alarms
    
    def update(self):
        """Main update loop for reactor physics"""
        self.calculate_reactivity()
        self.update_neutron_flux()
        self.update_thermal_power()
        self.update_temperatures()
        self.update_pressure()
        self.update_xenon()
        self.calculate_electrical_power()
        self.total_time += self.time_step
        
        return self.check_safety_limits()


# ============================================================================
# GUI SETUP
# ============================================================================

# Initialize the application
app = ui.init(
    SIZE=[16, 14],
    title="Nuclear Reactor Simulator - PWR Control Room",
    theme="dark",
    show_grid=False
)

# Create reactor physics instance
reactor = ReactorPhysics()

# State variables
update_interval = 100  # ms
history_length = 100
power_history = []
temp_history = []
pressure_history = []
time_history = []
alarm_text = ""

# ============================================================================
# HEADER
# ============================================================================
app.label(pos=[0.3, 0.2], size=[15.4, 0.8], text="⚛ REACTOR CONTROL ROOM ⚛", 
          text_size=20, text_font="Outfit", align="center")
app.label(pos=[0.3, 0.9], size=[15.4, 0.5], text="PWR - 3000 MW Thermal", 
          text_size=10, align="center")

# ============================================================================
# LEFT PANEL - REACTOR STATUS
# ============================================================================
app.label(pos=[0.3, 1.6], size=[5, 0.6], text="CORE STATUS", 
          text_size=11, text_font="Outfit", align="center")

# Neutron Flux Display
flux_label = app.label(pos=[0.3, 2.3], size=[2.2, 0.5], text="Flux:", text_size=9, align="left")
flux_value = app.label(pos=[2.5, 2.3], size=[3.1, 0.5], text="50.0 %", text_size=9, align="right")

# Core Temperature
core_temp_label = app.label(pos=[0.3, 2.9], size=[2.2, 0.5], text="Core T:", text_size=9, align="left")
core_temp_value = app.label(pos=[2.5, 2.9], size=[3.1, 0.5], text="300 °C", text_size=9, align="right")

# Reactivity
reactivity_label = app.label(pos=[0.3, 3.5], size=[2.2, 0.5], text="React:", text_size=9, align="left")
reactivity_value = app.label(pos=[2.5, 3.5], size=[3.1, 0.5], text="0.00 $", text_size=9, align="right")

# Xenon Poisoning
xenon_label = app.label(pos=[0.3, 4.1], size=[2.2, 0.5], text="Xe-135:", text_size=9, align="left")
xenon_value = app.label(pos=[2.5, 4.1], size=[3.1, 0.5], text="0.00", text_size=9, align="right")

# COOLANT SYSTEM (continued in left panel)
app.label(pos=[0.3, 4.8], size=[5, 0.5], text="COOLANT", 
          text_size=11, text_font="Outfit", align="center")

# Coolant Flow
flow_label = app.label(pos=[0.3, 5.4], size=[2.2, 0.5], text="Flow:", text_size=9, align="left")
flow_value = app.label(pos=[2.5, 5.4], size=[3.1, 0.5], text="100 %", text_size=9, align="right")

# Inlet Temperature
inlet_temp_label = app.label(pos=[0.3, 6.0], size=[2.2, 0.5], text="In T:", text_size=9, align="left")
inlet_temp_value = app.label(pos=[2.5, 6.0], size=[3.1, 0.5], text="280 °C", text_size=9, align="right")

# Outlet Temperature
outlet_temp_label = app.label(pos=[0.3, 6.6], size=[2.2, 0.5], text="Out T:", text_size=9, align="left")
outlet_temp_value = app.label(pos=[2.5, 6.6], size=[3.1, 0.5], text="320 °C", text_size=9, align="right")

# Primary Pressure
pri_pressure_label = app.label(pos=[0.3, 7.2], size=[2.2, 0.5], text="Pri P:", text_size=9, align="left")
pri_pressure_value = app.label(pos=[2.5, 7.2], size=[3.1, 0.5], text="155 bar", text_size=9, align="right")

# Secondary Pressure
sec_pressure_label = app.label(pos=[0.3, 7.8], size=[2.2, 0.5], text="Sec P:", text_size=9, align="left")
sec_pressure_value = app.label(pos=[2.5, 7.8], size=[3.1, 0.5], text="70 bar", text_size=9, align="right")

# POWER OUTPUT (continued in left panel)
app.label(pos=[0.3, 8.5], size=[5, 0.5], text="POWER", 
          text_size=11, text_font="Outfit", align="center")

# Thermal Power
thermal_power_label = app.label(pos=[0.3, 9.1], size=[2.2, 0.5], text="Therm:", text_size=9, align="left")
thermal_power_value = app.label(pos=[2.5, 9.1], size=[3.1, 0.5], text="0 MW", text_size=9, align="right")

# Electrical Power
elec_power_label = app.label(pos=[0.3, 9.7], size=[2.2, 0.5], text="Elec:", text_size=9, align="left")
elec_power_value = app.label(pos=[2.5, 9.7], size=[3.1, 0.5], text="0 MW", text_size=9, align="right")

# ============================================================================
# CENTER PANEL - VISUALIZATION
# ============================================================================
app.label(pos=[5.9, 1.6], size=[4.8, 0.6], text="MONITORING", 
          text_size=11, text_font="Outfit", align="center")

# Power History Graph
power_plot = app.plot(pos=[5.9, 2.3], size=[4.8, 3.8], type="bar")

# Temperature History Graph
temp_plot = app.plot(pos=[5.9, 6.3], size=[4.8, 3.8], type="bar")

# Status Display
status_display = app.label(pos=[5.9, 10.3], size=[4.8, 1.2], text="REACTOR ONLINE", 
                           text_size=9, align="center")

# ============================================================================
# RIGHT PANEL - CONTROLS
# ============================================================================
app.label(pos=[11, 1.6], size=[4.7, 0.6], text="CONTROLS", 
          text_size=11, text_font="Outfit", align="center")

# Control Rod Position
app.label(pos=[11, 2.3], size=[4.7, 0.5], text="Control Rods (% out)", text_size=9, align="center")

def on_control_rod_change(value):
    if not reactor.scram_active:
        reactor.control_rod_position = value

control_rod_slider = app.slider(pos=[11, 2.9], size=[4.7, 0.6], 
                                withrange=[0, 100], orientation="horizontal",
                                onchange=on_control_rod_change)

control_rod_display = app.label(pos=[11, 3.6], size=[4.7, 0.5], text="50.0 %", 
                                text_size=10, align="center")

# Coolant Flow Control
app.label(pos=[11, 4.3], size=[4.7, 0.5], text="Coolant Flow (%)", text_size=9, align="center")

def on_coolant_change(value):
    reactor.coolant_flow = value

coolant_slider = app.slider(pos=[11, 4.9], size=[4.7, 0.6], 
                            withrange=[0, 150], orientation="horizontal",
                            onchange=on_coolant_change)

coolant_display = app.label(pos=[11, 5.6], size=[4.7, 0.5], text="100.0 %", 
                            text_size=10, align="center")

# Emergency Controls
app.label(pos=[11, 6.4], size=[4.7, 0.5], text="EMERGENCY", text_size=10, align="center")

def scram_button_click(val=None):
    reactor.scram_active = True
    reactor.control_rod_position = 0.0
    control_rod_slider.set_value(0)

scram_btn = app.btn(pos=[11, 7], size=[4.7, 0.9], text="⚠ SCRAM ⚠", 
                    onclick=scram_button_click, text_size=12)

def emergency_cooling_toggle(checked):
    reactor.emergency_cooling = checked

emergency_cooling_check = app.checkbox(pos=[11, 8.1], text="Emerg. Cooling", 
                                       onchange=emergency_cooling_toggle, text_size=8)

def reset_scram_click(val=None):
    if reactor.core_temp < 400 and reactor.neutron_flux < 20:
        reactor.scram_active = False

reset_btn = app.btn(pos=[11, 9], size=[4.7, 0.8], text="Reset SCRAM", 
                    onclick=reset_scram_click, text_size=9)

# Alarm Display
app.label(pos=[11, 10.1], size=[4.7, 0.5], text="ALARMS", text_size=9, align="center")
alarm_display = app.label(pos=[11, 10.7], size=[4.7, 2.8], text="", 
                          text_size=8, align="center")

# ============================================================================
# UPDATE LOOP
# ============================================================================

def update_reactor():
    """Main update function called periodically"""
    global alarm_text, power_history, temp_history, pressure_history, time_history
    
    # Update reactor physics
    alarms = reactor.update()
    
    # Update all displays
    flux_value.set_text(f"{reactor.neutron_flux:.1f} %")
    core_temp_value.set_text(f"{reactor.core_temp:.0f} °C")
    reactivity_value.set_text(f"{reactor.reactivity:.3f} $")
    xenon_value.set_text(f"{reactor.xenon_poisoning:.3f}")
    
    flow_value.set_text(f"{reactor.coolant_flow:.0f} %")
    inlet_temp_value.set_text(f"{reactor.coolant_temp_in:.0f} °C")
    outlet_temp_value.set_text(f"{reactor.coolant_temp_out:.0f} °C")
    pri_pressure_value.set_text(f"{reactor.primary_pressure:.1f} bar")
    sec_pressure_value.set_text(f"{reactor.secondary_pressure:.1f} bar")
    
    thermal_power_value.set_text(f"{reactor.thermal_power:.0f} MW")
    elec_power_value.set_text(f"{reactor.electrical_power:.0f} MW")
    
    control_rod_display.set_text(f"{reactor.control_rod_position:.1f} %")
    coolant_display.set_text(f"{reactor.coolant_flow:.1f} %")
    
    # Update history for graphs
    time_history.append(reactor.total_time)
    power_history.append(reactor.thermal_power)
    temp_history.append(reactor.core_temp)
    pressure_history.append(reactor.primary_pressure)
    
    # Keep only recent history
    if len(time_history) > history_length:
        time_history.pop(0)
        power_history.pop(0)
        temp_history.pop(0)
        pressure_history.pop(0)
    
    # Update plots
    if len(time_history) > 1:
        power_plot.update((time_history, power_history))
        temp_plot.update((time_history, temp_history))
    
    # Update status
    if reactor.scram_active:
        status_display.set_text("⚠ SCRAM ACTIVE - REACTOR SHUTDOWN ⚠")
        status_display.configure(text_color="#ff4444")
    elif alarms:
        status_display.set_text("⚠ ALARM CONDITION ⚠")
        status_display.configure(text_color="#ffaa00")
    elif reactor.thermal_power > 2000:
        status_display.set_text("REACTOR AT HIGH POWER")
        status_display.configure(text_color="#44ff44")
    elif reactor.thermal_power > 500:
        status_display.set_text("REACTOR ONLINE - NORMAL OPERATION")
        status_display.configure(text_color="#44ff44")
    else:
        status_display.set_text("REACTOR AT LOW POWER")
        status_display.configure(text_color="#4444ff")
    
    # Update alarms
    if alarms:
        alarm_display.set_text("\n".join(alarms))
        alarm_display.configure(text_color="#ff4444")
    else:
        alarm_display.set_text("NO ACTIVE ALARMS")
        alarm_display.configure(text_color="#44ff44")
    
    # Color coding for critical values
    if reactor.core_temp > 600:
        core_temp_value.configure(text_color="#ff4444")
    elif reactor.core_temp > 450:
        core_temp_value.configure(text_color="#ffaa00")
    else:
        core_temp_value.configure(text_color="#44ff44")
    
    if reactor.neutron_flux > 100:
        flux_value.configure(text_color="#ff4444")
    elif reactor.neutron_flux > 90:
        flux_value.configure(text_color="#ffaa00")
    else:
        flux_value.configure(text_color="#44ff44")
    
    # Schedule next update
    app.wait(update_interval, update_reactor)

# ============================================================================
# STARTUP
# ============================================================================

if __name__ == "__main__":
    # Set initial slider values
    control_rod_slider.set_value(50)
    coolant_slider.set_value(100)
    
    # Start update loop
    app.wait(1000, update_reactor)
    
    # Run the application
    app.run()
