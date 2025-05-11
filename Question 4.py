import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk
from typer.colors import WHITE


# Voltage Deviation Functions
def voltage_low(x):
    if x <= 2:
        return 1
    elif 2 < x <= 5:
        return (5 - x) / 3
    return 0

def voltage_medium(x):
    if 3 <= x < 5:
        return (x - 3) / 2
    elif 5 <= x <= 7:
        return (7 - x) / 2
    return 0

def voltage_high(x):
    if x <= 6:
        return 0
    elif 6 < x <= 9:
        return (x - 6) / 3
    return 1



# Frequency Variation Functions
def frequency_stable(x):
    if x <= 0.2:
        return 1
    elif 0.2 < x <= 0.6:
        return (0.6 - x) / 0.4
    return 0

def frequency_unstable(x):
    if x <= 0.4:
        return 0
    elif 0.4 < x <= 0.8:
        return (x - 0.4) / 0.4
    return 1




# Load Imbalance Functions
def load_balanced(x):
    if x <= 10:
        return 1
    elif 10 < x <= 25:
        return (25 - x) / 15
    return 0

def load_unbalanced(x):
    if x <= 15:
        return 0
    elif 15 < x <= 35:
        return (x - 15) / 20
    return 1


#Fuzzy Rules
def fuzzy_infer(voltage, frequency, load):
    # Membership values for voltage deviation
    mu_voltage_low = voltage_low(voltage)
    mu_voltage_med = voltage_medium(voltage)
    mu_voltage_high = voltage_high(voltage)

    # Membership values for frequency variation
    mu_freq_stable = frequency_stable(frequency)
    mu_freq_unstable = frequency_unstable(frequency)

    # Membership values for load imbalance
    mu_load_balanced = load_balanced(load)
    mu_load_unbalanced = load_unbalanced(load)

    # Fuzzy rules for anomaly severity
    rule1 = min(mu_voltage_high, mu_freq_unstable, mu_load_unbalanced)
    rule2 = min(mu_voltage_med, mu_freq_unstable)
    rule3 = min(mu_voltage_low, mu_freq_stable, mu_load_balanced)
    rule4 = min(mu_voltage_high, mu_load_balanced)
    rule5 = min(mu_freq_stable, mu_load_unbalanced)
    rule6 = min(mu_freq_unstable, mu_load_balanced)

    # Weighted sum of the rule outputs for defuzzification
    total_weighted_output = (
        rule1 * 100 +
        rule2 * 50 +
        rule3 * 10 +
        rule4 * 50 +
        rule5 * 70 +
        rule6 * 60
    )

    total_weight = rule1 + rule2 + rule3 + rule4 + rule5 + rule6
    return total_weighted_output / total_weight if total_weight > 0 else 0

def mitigate_fault(severity_score):
    if severity_score > 80:
        return "High Severity:\nIsolate faulty section and redirect load."
    elif 40 < severity_score <= 80:
        return "Moderate Severity:\nBalance loads dynamically."
    elif severity_score > 0:
        return "Low Severity:\nAdjust power factor or use capacitors."
    else:
        return "No anomaly detected.\nNo mitigation needed."




# Graphs for Membership Functions
def plot_membership_functions():

    # Voltage Deviation
    x_voltage = np.linspace(0, 10, 200)
    plt.figure(figsize=(10, 6))
    plt.plot(x_voltage, [voltage_low(x) for x in x_voltage], label='Low Voltage', color='b')
    plt.plot(x_voltage, [voltage_medium(x) for x in x_voltage], label='Medium Voltage', color='g')
    plt.plot(x_voltage, [voltage_high(x) for x in x_voltage], label='High Voltage', color='r')
    plt.title('Voltage Deviation Membership Functions')
    plt.xlabel('Voltage Deviation')
    plt.ylabel('Membership')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Frequency Variation
    x_freq = np.linspace(0, 1, 200)
    plt.figure(figsize=(10, 6))
    plt.plot(x_freq, [frequency_stable(x) for x in x_freq], label='Stable Frequency', color='b')
    plt.plot(x_freq, [frequency_unstable(x) for x in x_freq], label='Unstable Frequency', color='r')
    plt.title('Frequency Variation Membership Functions')
    plt.xlabel('Frequency Variation')
    plt.ylabel('Membership')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Load Imbalance
    x_load = np.linspace(0, 30, 200)
    plt.figure(figsize=(10, 6))
    plt.plot(x_load, [load_balanced(x) for x in x_load], label='Balanced Load', color='b')
    plt.plot(x_load, [load_unbalanced(x) for x in x_load], label='Unbalanced Load', color='r')
    plt.title('Load Imbalance Membership Functions')
    plt.xlabel('Load Imbalance')
    plt.ylabel('Membership')
    plt.legend()
    plt.grid(True)
    plt.show()
plot_membership_functions()




ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

YELLOW = "#FFD700"
BLACK = "#000000"

window = ctk.CTk()
window.title("Fuzzy Fault Detection System")
window.geometry("500x620")
window.resizable(False, False)
window.configure(fg_color=BLACK)

ctk.CTkLabel(
    window,
    text="Fault Detection System",
    font=("Times New Roman", 28, "bold"),
    text_color=YELLOW
).pack(pady=20)


form_frame = ctk.CTkFrame(window, fg_color=BLACK, corner_radius=15)
form_frame.pack(pady=10, padx=20, fill="x")


# Input validation
def validate_input(new_value, min_val, max_val):
    if new_value.strip() == "":
        return True
    try:
        val = float(new_value)
        return min_val <= val <= max_val
    except ValueError:
        return False


# Function to move focus on arrow keys
def bind_arrow_navigation(entries):
    for i, entry in enumerate(entries):
        def focus_next(event, idx=i):
            if event.keysym == "Down" and idx + 1 < len(entries):
                entries[idx + 1].focus_set()
            elif event.keysym == "Up" and idx - 1 >= 0:
                entries[idx - 1].focus_set()

        entry.bind("<Down>", focus_next)
        entry.bind("<Up>", focus_next)


# Create labeled input field
def create_labeled_entry(label, min_val, max_val):
    ctk.CTkLabel(
        form_frame,
        text=label,
        text_color=YELLOW,
        font=ctk.CTkFont(size=14)
    ).pack(pady=(10, 4))

    entry = ctk.CTkEntry(
        form_frame,
        width=200,
        height=40,
        corner_radius=10,
        border_width=2,
        border_color=YELLOW,
        fg_color=BLACK,
        text_color=YELLOW
    )
    entry.pack(pady=6)

    vcmd = (entry.register(lambda val: validate_input(val, min_val, max_val)), '%P')
    entry.configure(validate="key", validatecommand=vcmd)
    return entry


# Inputs
voltage_entry = create_labeled_entry("Voltage (0 - 10):", 0, 10)
frequency_entry = create_labeled_entry("Frequency (0 - 1):", 0, 1)
load_entry = create_labeled_entry("Load (0 - 40):", 0, 40)

# Bind keyboard navigation
bind_arrow_navigation([voltage_entry, frequency_entry, load_entry])

# Result box
result_text = ctk.StringVar()
ctk.CTkLabel(
    window,
    textvariable=result_text,
    font=ctk.CTkFont(size=15, weight="bold"),
    text_color=WHITE,
    wraplength=440,
    justify="left",
    height=100,
    width=400,
    corner_radius=15,
    fg_color=BLACK,
    padx=15,
    pady=15
).pack(pady=25)



# Run Fuzzy Logic
def run_fuzzy_inference():
    try:
        voltage = float(voltage_entry.get())
        frequency = float(frequency_entry.get())
        load = float(load_entry.get())

        severity_score = fuzzy_infer(voltage, frequency, load)
        mitigation_action = mitigate_fault(severity_score)

        result_text.set(
            f"Severity Score: {severity_score:.2f}/100\n\nMitigation Suggestion:\n{mitigation_action}"
        )
    except ValueError:
        result_text.set("Please enter valid numeric values for all fields.")


# Reset fields
def reset_fields():
    voltage_entry.delete(0, "end")
    frequency_entry.delete(0, "end")
    load_entry.delete(0, "end")
    result_text.set("")
    voltage_entry.focus_set()


# Button section
button_frame = ctk.CTkFrame(window, fg_color="transparent")
button_frame.pack(pady=10)

ctk.CTkButton(
    button_frame,
    text="Run Fuzzy",
    fg_color=YELLOW,
    text_color=BLACK,
    hover_color="#e6c200",
    width=150,
    height=50,
    corner_radius=15,
    font=ctk.CTkFont(size=14, weight="bold"),
    command=run_fuzzy_inference
).pack(side="left", padx=15)

ctk.CTkButton(
    button_frame,
    text="Reset",
    fg_color=BLACK,
    text_color=YELLOW,
    hover_color="#222222",
    border_color=YELLOW,
    width=150,
    height=50,
    border_width=2,
    corner_radius=15,
    font=ctk.CTkFont(size=14, weight="bold"),
    command=reset_fields
).pack(side="left", padx=15)

# Start with focus on voltage input
voltage_entry.focus_set()

# Main loop
window.mainloop()








# test_cases = [
#     {"voltage": 8, "frequency": 0.8, "load": 30},
#     {"voltage": 5.5, "frequency": 0.7, "load": 20},
#     {"voltage": 3, "frequency": 0.1, "load": 8},
#     {"voltage": 7, "frequency": 0.4, "load": 12},
#     {"voltage": 5, "frequency": 0.3, "load": 35},
#     {"voltage": 6, "frequency": 0.7, "load": 15}
# ]
#
# for test_case in test_cases:
#     voltage = test_case["voltage"]
#     frequency = test_case["frequency"]
#     load = test_case["load"]
#     expected_result = test_case["expected_result"]
#
#     # Calculate severity score
#     severity_score = fuzzy_infer(voltage, frequency, load)
#     mitigation_action = mitigate_fault(severity_score)
#
#     print(f"Test case - Voltage: {voltage}, Frequency: {frequency}, Load: {load}")
#     print(f"Expected Result: {expected_result}")
#     print(f"Anomaly Severity Score: {severity_score:.2f}")
#     print(mitigation_action)
#     print("=" * 50)






