# Import necessary libraries
import pyvisa
import numpy as np
import matplotlib.pyplot as plt

# Establish a connection to the instruments
rm = pyvisa.ResourceManager()
function_generator_id = 'GPIB1::10::INSTR'  # Replace with your actual ID
oscilloscope_id = 'TCPIP0::169.254.254.254::inst0::INSTR'  # Replace with your actual ID

# Open the connection to the function generator and oscilloscope
function_generator = rm.open_resource(function_generator_id)
oscilloscope = rm.open_resource(oscilloscope_id)

# Function to set the function generator
def set_function_generator(frequency, amplitude=1.0):
    function_generator.write(f"VOLT {amplitude}")  # Set the amplitude
    function_generator.write(f"FREQ {frequency}")  # Set the frequency

# Function to read the oscilloscope
def read_oscilloscope():
    data = oscilloscope.query("MEASU:IMM:VAL?")
    return float(data)

# Parameters for the sweep
start_freq = 10  # Start frequency in Hz
stop_freq = 10000  # Stop frequency in Hz
steps = 100  # Number of steps in the sweep
frequencies = np.logspace(np.log10(start_freq), np.log10(stop_freq), steps)
amplitudes = []
phases = []

# Perform the sweep
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

# Calculate gain and phase for Bode plot
gains = 20 * np.log10(amplitudes)
phases = np.unwrap(phases)  # Unwrap the phase to avoid discontinuities

# Generate Bode plot
plt.figure()
plt.subplot(2, 1, 1)
plt.semilogx(frequencies, gains)
plt.title('Bode Plot')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Gain [dB]')

plt.subplot(2, 1, 2)
plt.semilogx(frequencies, phases)
plt.xlabel('Frequency [Hz]')
plt.ylabel('Phase [Radians]')

# Save the Bode plot
plt.savefig("bode_plot.png")

# Close the connections
function_generator.close()
oscilloscope.close()
