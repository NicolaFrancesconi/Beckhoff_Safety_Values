import tkinter as tk
from tkinter import ttk
import numpy as np


def mm_to_rev(mm, transmission_ratio):
    """Convert millimeters to revolutions based on the transmission ratio."""
    return mm / transmission_ratio

def rev_to_mm(rev, transmission_ratio):
    """Convert revolutions to millimeters based on the transmission ratio."""
    return rev * transmission_ratio

def numerator_denominator_to_ratio(numerator, denominator, encoder_resolution):
    """Convert numerator and denominator to a transmission ratio."""
    if denominator == 0:
        raise ValueError("Denominator cannot be zero.")
    if denominator != encoder_resolution:
        return numerator * encoder_resolution /denominator
    else:
        return numerator
    
def calculate_SSR(pole_pairs, mm_s_max, transmission_ratio):
    """Calculate increments per millisecond (SSR) based on the given parameters."""
    revolution_s = mm_to_rev(mm_s_max, transmission_ratio)
    revolution_ms = revolution_s / 1000
    inc_ms = 2.0 * np.pow(2.0, 16) * pole_pairs * revolution_ms
    return inc_ms

def calculate_SOS(pole_pairs, mm_s_max, transmission_ratio):
    """Calculate increments (SOS) based on the given parameters."""
    revolution_s = mm_to_rev(mm_s_max, transmission_ratio)
    revolution_ms = revolution_s / 1000
    inc = np.pow(2.0, 16) * pole_pairs * revolution_ms
    return inc

def calculate_SCW(pole_pairs, mm_s_max, transmission_ratio):
    """Calculate increments per millisecond (SCW) based on the given parameters."""
    revolution_s = mm_to_rev(mm_s_max, transmission_ratio)
    revolution_ms = revolution_s / 1000
    inc_ms = np.pow(2.0, 16) * pole_pairs * revolution_ms
    inc_125_ms = inc_ms / 8.0
    return inc_125_ms


def calculate():
    try:
        pole_pairs = float(entry_pole.get())
        mm_s_max = float(entry_speed.get())
        if mode_var.get() == "transmission_ratio":
            transmission_ratio = float(entry_transmission.get())
        else:
            numerator = float(entry_numerator.get())
            denominator = float(entry_denominator.get())
            encoder_resolution = np.pow(2.0, float(entry_resolution.get()))
            if denominator == 0:
                result_var.set("Denominator cannot be zero.")
                return
            transmission_ratio = numerator_denominator_to_ratio(numerator, denominator, encoder_resolution)
            
        if calc_mode_var.get() == "SSR":
            result = calculate_SSR(pole_pairs, mm_s_max, transmission_ratio)
            result_var.set(f"SSR Increments/ms: {result:.2f}")
        elif calc_mode_var.get() == "SOS":
            result = calculate_SOS(pole_pairs, mm_s_max, transmission_ratio)
            result_var.set(f"SOS Increments: {result:.2f}")
        elif calc_mode_var.get() == "SCW":
            result = calculate_SCW(pole_pairs, mm_s_max, transmission_ratio)
            result_var.set(f"SCW Increments/125us: {result:.2f}")

    except Exception as e:
        result_var.set("Error in input values.")

def add_numerator_denominator_widgets():
    """Add numerator and denominator widgets to the GUI."""
    label_numerator.grid(row=4, column=0, sticky="e")
    entry_numerator.grid(row=4, column=1)
    label_denominator.grid(row=5, column=0, sticky="e")
    entry_denominator.grid(row=5, column=1)
    toggle_button.config(text="Switch to Ratio Mode")
    calc_button.grid(row=6, column=0, columnspan=2, pady=10)
    result_label.grid(row=7, column=0, columnspan=2)

def remove_numerator_denominator_widgets():
    """Remove numerator and denominator widgets from the GUI."""
    entry_numerator.grid_remove()
    label_numerator.grid_remove()
    entry_denominator.grid_remove()
    label_denominator.grid_remove()
    toggle_button.config(text="Switch to Fraction Mode")
    calc_button.grid(row=5, column=0, columnspan=2, pady=10)
    result_label.grid(row=6, column=0, columnspan=2)

def add_transmission_widgets():
    """Add transmission widgets to the GUI."""
    label_transmission.grid(row=4, column=0, sticky="e")
    entry_transmission.grid(row=4, column=1)

def remove_transmission_widgets():
    """Remove transmission widgets from the GUI."""
    entry_transmission.grid_remove()
    label_transmission.grid_remove()

def add_encoder_widgets():
    """Add encoder resolution widgets to the GUI."""
    label_resolution.grid(row=1, column=0, sticky="e")
    entry_resolution.grid(row=1, column=1)

def remove_encoder_widgets():
    """Remove encoder resolution widgets from the GUI."""
    entry_resolution.grid_remove()
    label_resolution.grid_remove()

def toggle_mode():
    if mode_var.get() == "transmission_ratio":
        mode_var.set("fraction")
        remove_transmission_widgets()
        add_numerator_denominator_widgets()
        add_encoder_widgets()
        toggle_button.config(text="Switch to Transmission Ratio Mode")
        calc_button.grid(row=6, column=0, columnspan=2, pady=10)
        result_label.grid(row=7, column=0, columnspan=2)
    else:
        mode_var.set("transmission_ratio")
        remove_numerator_denominator_widgets()
        remove_encoder_widgets()
        add_transmission_widgets()
        toggle_button.config(text="Switch to Numerator/Denominator Mode")
        calc_button.grid(row=5, column=0, columnspan=2, pady=10)
        result_label.grid(row=6, column=0, columnspan=2)

def update_speed_label(*args):
    if calc_mode_var.get() == "SSR" or calc_mode_var.get() == "SCW":
        speed_text_label.config(text="Max Speed (mm/s):")
    else:
        speed_text_label.config(text="Max Displacement (mm):")

    # If the result is already calculated, update it
    if result_var.get() != "" and result_var.get() != "Error in input values.":
        calculate()
    

root = tk.Tk()
root.title("Safety Value Calculator")

# Calculation mode radio buttons
calc_mode_var = tk.StringVar(value="SSR")
calc_mode_var.trace_add("write", update_speed_label)

frame_top = ttk.Frame(root)
frame_top.grid(row=0, column=0, columnspan=2, pady=5)
ttk.Radiobutton(frame_top, text="Increments/ms (SSR)", variable=calc_mode_var, value="SSR").pack(side="left", padx=5)
ttk.Radiobutton(frame_top, text="Increments (SOS)", variable=calc_mode_var, value="SOS").pack(side="left", padx=5)
ttk.Radiobutton(frame_top, text="Increments/125us (SCW)", variable=calc_mode_var, value="SCW").pack(side="left", padx=5)

label_resolution = ttk.Label(root, text="Encoder Resolution (Bits):")
label_resolution.grid(row=1, column=0, sticky="e")
entry_resolution = ttk.Entry(root)
entry_resolution.grid(row=1, column=1)
remove_encoder_widgets()

label_pole = ttk.Label(root, text="Pole Pairs:")
label_pole.grid(row=2, column=0, sticky="e")
entry_pole = ttk.Entry(root)
entry_pole.grid(row=2, column=1)

speed_text_label = ttk.Label(root, text="Max Speed (mm/s):")
speed_text_label.grid(row=3, column=0, sticky="e")
entry_speed = ttk.Entry(root)
entry_speed.grid(row=3, column=1)



mode_var = tk.StringVar(value="transmission_ratio")

label_transmission = ttk.Label(root, text="Transmission Ratio (mm/rev):")
label_transmission.grid(row=4, column=0, sticky="e")
entry_transmission = ttk.Entry(root)
entry_transmission.grid(row=4, column=1)

label_numerator = ttk.Label(root, text="Numerator:")
entry_numerator = ttk.Entry(root)
label_denominator = ttk.Label(root, text="Denominator:")
entry_denominator = ttk.Entry(root)

toggle_button = ttk.Button(root, text="Switch to Numerator/Denominator Mode", command=toggle_mode)
toggle_button.grid(row=8, column=0, columnspan=2, pady=5)

calc_button = ttk.Button(root, text="Calculate", command=calculate)
calc_button.grid(row=5, column=0, columnspan=2, pady=10)

result_var = tk.StringVar()
result_label = ttk.Label(root, textvariable=result_var)
result_label.grid(row=6, column=0, columnspan=2)

root.mainloop()

