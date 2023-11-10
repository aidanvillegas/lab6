import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
import pyvisa
import numpy as np
import matplotlib.pyplot as plt


function_generator = None
oscilloscope = None

# Function to handle Bode plot sweep
def sweep_and_plot():
    try:
        # Perform the frequency sweep and collect data here
        # This is a placeholder for the actual implementation
        start_freq = 10  # Start frequency in Hz
        stop_freq = 10000  # Stop frequency in Hz
        steps = 100  # Number of steps in the sweep
        frequencies = np.logspace(np.log10(start_freq), np.log10(stop_freq), steps)
        gains = []  # Placeholder for gain data
        phases = []  # Placeholder for phase data

         # Turn on the output and display of the function generator and oscilloscope
        function_generator.write('OUTPUT ON')
        oscilloscope.write('CHAN1:DISP ON')

        for freq in frequencies:
            # Set the function generator frequency and amplitude
            function_generator.write(f'FREQ {freq}')
            function_generator.write(f'VOLT {amplitude}')

            # Measure the output voltage and phase from the oscilloscope
            # These will be specific commands for your oscilloscope
            vout = oscilloscope.query('MEASURE:VPP?')  # Placeholder for Vout measurement command
            phase = oscilloscope.query('MEASURE:PHASE?')  # Placeholder for phase measurement command

            # Convert the measurements to the correct units if necessary and store them
            measured_vouts.append(float(vout))
            measured_phases.append(float(phase))
         # Turn off the output of the function generator after the sweep
        function_generator.write('OUTPUT OFF')

        
        # Calculate the gain in dB and unwrap the phase
        gains_db = 20 * np.log10(gains)
        phases_unwrapped = np.unwrap(phases)
        
        # Plot the Bode plot
        plt.figure()
        plt.subplot(211)
        plt.semilogx(frequencies, gains_db)
        plt.title('Bode Plot of Gain')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Gain (dB)')
        
        plt.subplot(212)
        plt.semilogx(frequencies, phases_unwrapped)
        plt.title('Bode Plot of Phase')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Phase (Radians)')
        
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        # Ensure the instruments are closed properly if an error occurs
        if function_generator:
            function_generator.close()
        if oscilloscope:
            oscilloscope.close()

# Define the command functions
def connect_instruments():
    # Establish a connection to the instruments
    global function_generator, oscilloscope
    try:
        rm = pyvisa.ResourceManager()
        function_generator = rm.open_resource(entry_function_gen.get())
        oscilloscope = rm.open_resource(entry_oscilloscope.get())
        messagebox.showinfo("Connection Status", "Instruments connected successfully")
    except Exception as e:
        messagebox.showerror("Connection Status", f"Failed to connect instruments: {e}")

def set_frequency():
    try:
        freq = float(entry_frequency.get())
        function_generator.write(f"FREQ {freq}")
        messagebox.showinfo("Action Status", f"Frequency set to {freq} Hz")
    except Exception as e:
        messagebox.showerror("Action Status", f"Failed to set frequency: {e}")

def set_voltage():
    try:
        voltage = float(entry_voltage.get())
        function_generator.write(f"VOLT {voltage}")
        messagebox.showinfo("Action Status", f"Voltage set to {voltage} V")
    except Exception as e:
        messagebox.showerror("Action Status", f"Failed to set voltage: {e}")

def disconnect_instruments():
    try:
        function_generator.close()
        oscilloscope.close()
        messagebox.showinfo("Connection Status", "Instruments disconnected successfully")
    except Exception as e:
        messagebox.showerror("Connection Status", f"Failed to disconnect instruments: {e}")

# Create the main window
root = tk.Tk()
root.title("Function Generator & Oscilloscope Control")

# Set window size (width x height)
root.geometry('500x300')  # You can change the numbers to whatever size you want

# Define a larger font
large_font = tkfont.Font(family="Helvetica", size=14)

# Create and place the widgets with a larger font
tk.Label(root, text="Function Generator Address:", font=large_font).grid(row=0, column=0)
entry_function_gen = tk.Entry(root, font=large_font)
entry_function_gen.grid(row=0, column=1)

tk.Label(root, text="Oscilloscope Address:", font=large_font).grid(row=1, column=0)
entry_oscilloscope = tk.Entry(root, font=large_font)
entry_oscilloscope.grid(row=1, column=1)

tk.Label(root, text="Frequency (Hz):", font=large_font).grid(row=2, column=0)
entry_frequency = tk.Entry(root, font=large_font)
entry_frequency.grid(row=2, column=1)

tk.Label(root, text="Voltage (V):", font=large_font).grid(row=3, column=0)
entry_voltage = tk.Entry(root, font=large_font)
entry_voltage.grid(row=3, column=1)

connect_button = tk.Button(root, text="Connect", command=connect_instruments, font=large_font)
connect_button.grid(row=4, column=0)

disconnect_button = tk.Button(root, text="Disconnect", command=disconnect_instruments, font=large_font)
disconnect_button.grid(row=4, column=1)

set_freq_button = tk.Button(root, text="Set Frequency", command=set_frequency, font=large_font)
set_freq_button.grid(row=5, column=0)

set_volt_button = tk.Button(root, text="Set Voltage", command=set_voltage, font=large_font)
set_volt_button.grid(row=5, column=1)

sweep_button = tk.Button(root, text="Perform Sweep and Plot Bode", command=sweep_and_plot, font=large_font)
sweep_button.grid(row=6, columnspan=2)

# Run the main loop
root.mainloop()
