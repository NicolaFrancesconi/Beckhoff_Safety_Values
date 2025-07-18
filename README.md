# Beckhoff Safety Value Calculator

This Python application provides a graphical interface (Tkinter-based) to calculate safety-related values for Beckhoff AX5805/AX5806 TwinSAFE drive option cards. The calculations are based on the official Beckhoff documentation and are intended to assist engineers and technicians in configuring safety parameters for servo drives.

## Purpose

The program calculates the following safety values:

- **SOS (Safe Operating Stop)**: Determines the increment window for detecting motion during standstill.
- **SSR (Safe Speed Range)**: Calculates the increment range per millisecond to monitor speed limits.
- **SCW (Speed Compare Window)**: Computes the increment range over 125 us for speed comparison.

These values are derived from the **linear speed or displacement** of the axis connected to the motor, taking into account the transmission ratio and motor pole pairs.

## Features

- Supports two input modes:
  - Direct transmission ratio
  - Encoder-based ratio using numerator/denominator and encoder resolution
- Allows selection of calculation mode: SSR, SOS, or SCW
- Dynamically updates the interface based on selected input mode
- Provides real-time results with error handling

## Reference

The calculations and logic are based on the official Beckhoff manual:

**SAFETY_ax5805_manuale_modulo_safety.pdf**

This document describes the mathematical relationships and safety function parameters used in TwinSAFE modules, including increment calculations for speed and position monitoring.

## Usage

1. Enter the number of motor pole pairs.
2. Enter the maximum linear speed or displacement (in mm/s or mm).
3. Choose the input mode:
   - Enter the transmission ratio directly, or
   - Enter the numerator, denominator, and encoder resolution (in bits).
4. Select the desired calculation mode (SSR, SOS, or SCW).
5. Click **Calculate** to view the result.

## Disclaimer

This tool is intended for educational and configuration assistance purposes. Always validate safety parameters using certified tools and procedures as required by your application and safety standards.
