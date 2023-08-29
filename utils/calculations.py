import numpy as np
from scipy.special import beta  # Import the beta function for the Beta Distribution
from scipy import stats


# Basic Parameters
def calculate_capacitance(charge, voltage):
    return charge / voltage

def calculate_energy_storage(capacitance, voltage):
    return 0.5 * capacitance * voltage ** 2

def calculate_voltage(charge, capacitance):
    return charge / capacitance

def calculate_charge(capacitance, voltage):
    return capacitance * voltage

def calculate_esr(voltage_drop, current):
    return voltage_drop / current

def calculate_voltage_drop_esr(esr, current):
    return esr * current

def calculate_leakage_current(capacitance, voltage, resistance):
    return (capacitance * voltage) / resistance

# Charging and Discharging
def calculate_time(capacitance, initial_voltage, final_voltage, amperage=None, power=None):
    if amperage is not None:
        current = amperage
    elif power is not None and initial_voltage != 0:
        current = power / initial_voltage
    else:
        raise ValueError("Either amperage or power must be provided.")

    return (capacitance * (initial_voltage - final_voltage)) / current

# Performance Metrics
def calculate_efficiency(output_power, input_power):
    return output_power / input_power

def calculate_power_density(power, volume):
    return power / volume

# Thermal Considerations
def calculate_heat_generation(current, esr):
    return current ** 2 * esr

# Lifetime Reliability
def calculate_failure_rate(cycle_life, temperature, stress_factors):
    activation_energy = 0.7  # Example value, in eV
    k_boltzmann = 8.617e-5    # Boltzmann constant, in eV/K
    reference_temp = 298     # Reference temperature, in K
    failure_rate = stress_factors * (cycle_life ** -0.5) * \
                   (2 ** ((activation_energy / k_boltzmann) * (1 / reference_temp - 1 / (temperature + 273))))
    return failure_rate

# Series Circuits
def calculate_total_capacitance_series(capacitances):
    return 1 / np.sum(1 / np.array(capacitances))

def calculate_voltage_distribution_series(voltage, resistances):
    return voltage * np.array(resistances) / np.sum(resistances)

# Parallel Circuits
def calculate_total_capacitance_parallel(capacitances):
    return np.sum(capacitances)

def calculate_current_distribution_parallel(current, resistances):
    return current * np.array(resistances) / np.sum(resistances)

# Mixed Series and Parallel Circuits
# These calculations would depend on the specific configuration and may require more complex analysis.

# Advanced Modeling
def calculate_total_capacitance(double_layer, pseudo):
    return double_layer + pseudo

def calculate_specific_capacitance(total_capacitance, surface_area):
    return total_capacitance / surface_area

def calculate_effective_surface_area(surface_area, porosity):
    return surface_area * porosity

# Energy Density
def calculate_energy_density(energy, mass):
    return energy / mass * 3600  # Converting from Joules to Watt-hours

def calculate_energy_charge_discharge(capacitance, initial_voltage, final_voltage):
    return 0.5 * (capacitance * (initial_voltage ** 2 - final_voltage ** 2))

# Additional Calculations
def calculate_pmax_continuous(max_continuous_current, voltage):
    return max_continuous_current * voltage

def calculate_current_max_time(max_current):
    return max_current  # MAX current (A) for 1 second

def calculate_voltage_max(wvdc):
    return wvdc

def calculate_capacity_min(capacitance):
    return capacitance

def calculate_esr_dc_max(dc_esr):
    return dc_esr

def calculate_length(dimensions):
    return dimensions[0]

def calculate_width(dimensions):
    return dimensions[2]

def calculate_height(dimensions):
    return dimensions[1]



#def LifeCycles
#        if tech == "EDLC 3V":
#            formula = lambda x: L0 * 3.1 * ((T0 - Tx) / 10) * 1.58 * ((V0 - Vx) / .1)
#        elif tech == "EDLC 2.7V":
#            formula = lambda x: L0 * 3.25 * ((T0 - Tx) / 10) * 1.52 * ((V0 - Vx) / .1)
#        elif tech == "LiC 20-85 celsius":
#            formula = lambda x: L0 * 2.45 * ((T0 - Tx) / 10) * 1.58 * ((V0 - Vx) / .1)
#        elif tech == "LiC 20-70 celsius":
#            formula = lambda x: L0 * 2.42 * ((T0 - Tx) / 10) * 1.34 * ((V0 - Vx) / .1)
#        elif tech == "LCC":
#            formula = lambda x: L0 * 2 * ((T0 - Tx) / 10) * 2 * ((V0 - x) / .2)

# Define curve types
def linear(x, a, b):
    return a * x + b

def quadratic(x, a, b, c):
    return a * x**2 + b * x + c

def sine_wave(x, A, omega, phi):
    return A * np.sin(omega * x + phi)

def exponential(x, a, b):
    return a * np.exp(b * x)

def logarithmic(x, a, b):
    return a + b * np.log(x)

def cubic(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d

def power_law(x, a, b):
    return a * x ** b

def gaussian(x, a, b, c):
    return a * np.exp(-((x - b)**2) / (2 * c**2))

def logistic(x, a, b, c):
    return a / (1 + np.exp(-b * (x - c)))

def hyperbolic(x, a, b):
    return a / (b + x)

def cosine_wave(x, A, omega, phi):
    return A * np.cos(omega * x + phi)

def tangent(x, a, b):
    return a * np.tan(b * x)

def square_root(x, a, b):
    return a * np.sqrt(x) + b

def exponential_decay(x, a, b):
    return a * np.exp(-b * x)

def logarithmic_decay(x, a, b):
    return a - b * np.log(x)

def polynomial_4th_degree(x, a, b, c, d, e):
    return a * x**4 + b * x**3 + c * x**2 + d * x + e

def inverse_square(x, a):
    return a / (x ** 2)

def sigmoid(x, a, b):
    return 1 / (1 + np.exp(-a * (x - b)))

def rational_function(x, a, b, c):
    return a / (b + c * x)

def weibull_distribution(x, a, b):
    return a * b * x**(b - 1) * np.exp(-a * x**b)

def rayleigh_distribution(x, a, b):
    return a * x * np.exp(-x**2 / (2 * b**2))

def poisson_distribution(x, lmbda):
    return np.exp(-lmbda) * lmbda**x / np.math.factorial(x)

def beta_distribution(x, alpha, beta):
    return x**(alpha - 1) * (1 - x)**(beta - 1) / beta(alpha, beta)

def cauchy_distribution(x, gamma, x0):
    return 1 / (np.pi * gamma * (1 + ((x - x0) / gamma)**2))

def gompertz_function(x, a, b, c):
    return a * np.exp(-b * np.exp(-c * x))

def hill_equation(x, a, b, n):
    return a * x**n / (b**n + x**n)

def double_exponential(x, a, b, c, d):
    return a * np.exp(b * x) + c * np.exp(d * x)

def fourier_series(x, a0, a1, b1):
    return a0 + a1 * np.cos(2 * np.pi * x) + b1 * np.sin(2 * np.pi * x)

def calculate_geometric_mean(best_fits):
    geometric_mean = np.prod(best_fits)
    return np.power(geometric_mean, 1 / len(best_fits))

def calculate_harmonic_mean(best_fits):
    harmonic_mean = len(best_fits) / np.sum(1.0 / np.array(best_fits))
    return harmonic_mean

def calculate_median(median_list):
    return np.median(np.array(median_list), axis=0)

def calculate_mode(mode_list):
    return stats.mode(np.array(mode_list), axis=0)[0][0]

def calculate_ewma(ewma_list):
    ewma = np.mean(ewma_list)
    return ewma / len(ewma_list)

def calculate_rms(rms_list):
    rms = np.sqrt(np.mean(np.square(rms_list)))
    return rms

def calculate_log_mean(log_list):
    log_mean = np.exp(np.mean(np.log(log_list)))
    return log_mean

def calculate_trimmed_mean(trimmed_mean_list):
    return stats.trim_mean(np.array(trimmed_mean_list), 0.1, axis=0)

def calculate_winsorized_mean(winsorized_mean_list):
    return stats.mstats.winsorize(np.array(winsorized_mean_list), limits=[0.05, 0.05])

# Dictionary mapping curve names to functions
curve_types = {
    'Linear': linear,
    'Quadratic': quadratic,
    'Sine Wave': sine_wave,
    'Exponential': exponential,
    'Logarithmic': logarithmic,
    'Cubic': cubic,
    'Power Law': power_law,
    'Gaussian': gaussian,
    'Logistic': logistic,
    'Hyperbolic': hyperbolic,
    'Cosine Wave': cosine_wave,
    'Tangent': tangent,
    'Square Root': square_root,
    'Exponential Decay': exponential_decay,
    'Logarithmic Decay': logarithmic_decay,
    'Polynomial (4th degree)': polynomial_4th_degree,
    'Inverse Square': inverse_square,
    'Sigmoid': sigmoid,
    'Rational Function': rational_function,
    'Weibull Distribution': weibull_distribution,
    'Rayleigh Distribution': rayleigh_distribution,
    'Poisson Distribution': poisson_distribution,
    'Beta Distribution': beta_distribution,
    'Cauchy Distribution': cauchy_distribution,
    'Gompertz Function': gompertz_function,
    'Hill Equation': hill_equation,
    'Double Exponential': double_exponential,
    'Fourier Series': fourier_series
}

# Define initial guesses for each curve type
initial_guesses = {
    'Linear': [1, 1],
    'Quadratic': [1, 1, 1],
    'Sine Wave': [1, 1, 0],
    'Exponential': [1, 1],
    'Logarithmic': [1, 1],
    'Cubic': [1, 1, 1, 1],
    'Power Law': [1, 1],
    'Gaussian': [1, 0, 1],
    'Logistic': [1, 1, 1],
    'Hyperbolic': [1, 1],
    'Cosine Wave': [1, 1, 0],
    'Tangent': [1, 1],
    'Square Root': [1, 1],
    'Exponential Decay': [1, 1],
    'Logarithmic Decay': [1, 1],
    'Polynomial (4th degree)': [1, 1, 1, 1, 1],
    'Inverse Square': [1],
    'Sigmoid': [1, 1],
    'Rational Function': [1, 1, 1],
    'Weibull Distribution': [1, 1],
    'Rayleigh Distribution': [1, 1],
    'Poisson Distribution': [1],
    'Beta Distribution': [1, 1],
    'Cauchy Distribution': [1, 1],
    'Gompertz Function': [1, 1, 1],
    'Hill Equation': [1, 1, 1],
    'Double Exponential': [1, 1, 1, 1],
    'Fourier Series': [1, 1, 1]
}

# Define bounds for each curve type
bounds = {
    'Linear': ([-np.inf, -np.inf], [np.inf, np.inf]),
    'Quadratic': ([-np.inf, -np.inf, -np.inf], [np.inf, np.inf, np.inf]),
    'Sine Wave': ([-np.inf, -np.inf, -np.inf], [np.inf, np.inf, np.inf]),
    'Exponential': ([0, 0], [np.inf, np.inf]),
    'Logarithmic': ([-np.inf, 0], [np.inf, np.inf]),
    'Cubic': ([-np.inf, -np.inf, -np.inf, -np.inf], [np.inf, np.inf, np.inf, np.inf]),
    'Power Law': ([0, 0], [np.inf, np.inf]),
    'Gaussian': ([-np.inf, -np.inf, 0], [np.inf, np.inf, np.inf]),
    'Logistic': ([-np.inf, -np.inf, -np.inf], [np.inf, np.inf, np.inf]),
    'Hyperbolic': ([-np.inf, -np.inf], [np.inf, np.inf]),
    'Cosine Wave': ([-np.inf, -np.inf, -np.inf], [np.inf, np.inf, np.inf]),
    'Tangent': ([-np.inf, -np.inf], [np.inf, np.inf]),
    'Square Root': ([0, -np.inf], [np.inf, np.inf]),
    'Exponential Decay': ([0, 0], [np.inf, np.inf]),
    'Logarithmic Decay': ([-np.inf, 0], [np.inf, np.inf]),
    'Polynomial (4th degree)': ([-np.inf, -np.inf, -np.inf, -np.inf, -np.inf], [np.inf, np.inf, np.inf, np.inf, np.inf]),
    'Inverse Square': ([0], [np.inf]),
    'Sigmoid': ([-np.inf, -np.inf], [np.inf, np.inf]),
    'Rational Function': ([-np.inf, -np.inf, -np.inf], [np.inf, np.inf, np.inf]),
    'Weibull Distribution': ([0, 0], [np.inf, np.inf]),
    'Rayleigh Distribution': ([0, 0], [np.inf, np.inf]),
    'Poisson Distribution': ([0], [np.inf]),
    'Beta Distribution': ([0, 0], [np.inf, np.inf]),
    'Cauchy Distribution': ([-np.inf, -np.inf], [np.inf, np.inf]),
    'Gompertz Function': ([0, 0, 0], [np.inf, np.inf, np.inf]),
    'Hill Equation': ([0, 0, 0], [np.inf, np.inf, np.inf]),
    'Double Exponential': ([-np.inf, -np.inf, -np.inf, -np.inf], [np.inf, np.inf, np.inf, np.inf]),
    'Fourier Series': ([-np.inf, -np.inf, -np.inf], [np.inf, np.inf, np.inf])
}

if __name__ == "__main__":
    test_array = [1, 2, 3, 4, 5]
    print("Geometric Mean:", calculate_geometric_mean(test_array))
    print("Harmonic Mean:", calculate_harmonic_mean(test_array))
    print("Median:", calculate_median(test_array))
    print("Mode:", calculate_mode(test_array))
    print("EWMA:", calculate_ewma(test_array))
    print("RMS:", calculate_rms(test_array))
    print("Log Mean:", calculate_log_mean(test_array))
    print("Trimmed Mean:", calculate_trimmed_mean(test_array))
    print("Winsorized Mean:", calculate_winsorized_mean(test_array))