import sys
import numpy as np
from scipy.stats import mode, trim_mean, gmean, hmean
from numpy.polynomial.polynomial import Polynomial
from scipy.interpolate import interp1d, CubicSpline
import matplotlib.pyplot as plt
from utils.mapping import curve_types  # Assuming you have this module
from PyQt5.QtWidgets import QApplication, QMainWindow
from scipy.stats.mstats import winsorize
from utils.calculations import agm  # Assuming you have this module

def calculate_relationship(self):
    if not hasattr(self, 'data_loaded') or not self.data_loaded:
        print("Warning: Data not loaded or fitted yet. Skipping calculations.")
        return

    # Initialize y_values for EWMA
    y_values = np.zeros_like(self.x_data)
    
    # Initialize final_y_avg for storing final average Y values
    final_y_avg = np.zeros_like(self.x_data)
    
    # Collect all parameters from the best fit information
    all_params = np.array([info['params'] for info in self.best_fits.values()])
    
    # Initialize mode_values for storing mode of Y values
    mode_values = np.zeros_like(self.x_data)
    
    # Collect all Y values into a single array
    all_y_values = np.array(list(self.y_data_sets.values()))
    
    # Calculate the root mean square (RMS) of Y values
    rms = np.sqrt(np.mean(np.square(np.array(list(self.y_data_sets.values()))), axis=0))
    
    # Calculate the mode of Y values
    mode_result = mode(all_y_values, axis=0)
    if mode_result.mode.shape:  
        mode_values = mode_result.mode[0]
    else:
        mode_values = mode_result.mode

    # Initialize final_y_avg based on curve fitting
    for name, info in self.best_fits.items():
        best_fit = info['fit']
        best_params = info['params']
        func = curve_types[best_fit]
        final_y_avg += func(np.array(self.x_data), *best_params)
    final_y_avg /= len(self.best_fits)

    # Initialize weights based on R-squared values and calculate weighted average
    weights = [info['r2'] for info in self.best_fits.values()]
    if np.sum(weights) == 0:
        print("Warning: Weights sum to zero. Using uniform weights.")
        final_y_weighted = np.mean(np.array(list(self.y_data_sets.values())), axis=0)
    else:
        final_y_weighted = np.average(np.array(list(self.y_data_sets.values())), axis=0, weights=weights)
    
    # Polynomial Regression
    if len(self.x_data) > 0 and len(final_y_avg) > 0:
        final_y_poly = p(self.x_data)  # Evaluate the polynomial at x_data
        self.ax.plot(self.x_data, final_y_poly, 'b:', label='Polynomial Regression')
    else:
        print("Warning: x_data or final_y_avg is empty. Skipping Polynomial fit.")
        
    # Complex Operations
    final_y_complex = np.sqrt(np.prod(np.array(list(self.y_data_sets.values())), axis=0))

    # Median Values
    median_values = np.median(np.array(list(self.y_data_sets.values())), axis=0)
    
    # Trimmed Mean
    trim_percentage = 10  
    trimmed_mean = np.zeros_like(self.x_data)
    for name, info in self.best_fits.items():
        best_fit = info['fit']
        best_params = info['params']
        func = curve_types[best_fit]
        y_values = func(np.array(self.x_data), *best_params)
        trimmed_mean += trim_mean(y_values, trim_percentage / 100.0)
    trimmed_mean /= len(self.best_fits)
    
    # Winsorized Mean
    lower_limit = 0.1  
    upper_limit = 0.1  
    winsorized_data = [winsorize(y_data, limits=[lower_limit, upper_limit]) for y_data in list(self.y_data_sets.values())]
    winsorized_mean = np.mean(np.array(winsorized_data), axis=0)

    # Log Mean
    log_mean = np.zeros_like(self.x_data)
    for name, info in self.best_fits.items():
        best_fit = info['fit']
        best_params = info['params']
        func = curve_types[best_fit]
        log_mean += np.log(func(np.array(self.x_data), *best_params))
    log_mean /= len(self.best_fits)
    log_mean = np.exp(log_mean)
    
    # Geometric Mean
    geometric_mean = np.ones_like(self.x_data)
    for name, info in self.best_fits.items():
        best_fit = info['fit']
        best_params = info['params']
        func = curve_types[best_fit]
        geometric_mean *= func(np.array(self.x_data), *best_params)
    if len(self.best_fits) > 0:
        geometric_mean = np.power(geometric_mean, 1 / len(self.best_fits))
    else:
        print("Warning: best_fits is empty. Skipping geometric mean calculation.")

    # Harmonic Mean
    harmonic_mean = np.zeros_like(self.x_data)
    for name, info in self.best_fits.items():
        best_fit = info['fit']
        best_params = info['params']
        func = curve_types[best_fit]
        harmonic_mean += 1 / func(np.array(self.x_data), *best_params)
    harmonic_mean = len(self.best_fits) / harmonic_mean

    # Exponentially Weighted Moving Average (EWMA)
    alpha = 0.2
    ewma = np.zeros_like(self.x_data)
    for name, info in self.best_fits.items():
        best_fit = info['fit']
        best_params = info['params']
        func = curve_types[best_fit]
        y_values = func(np.array(self.x_data), *best_params)
        ewma = alpha * y_values + (1 - alpha) * ewma

    # Interpolated Mean
    try:
        interp_func = interp1d(self.x_data, np.mean(np.array(list(self.y_data_sets.values())), axis=0))
        interpolated_mean = interp_func(self.x_data)
    except Exception as e:
        print(f"Interpolated Mean Error: {e}")

    # Cubic Spline
    try:
        cs = CubicSpline(self.x_data, np.mean(np.array(list(self.y_data_sets.values())), axis=0))
        cubic_spline_values = cs(self.x_data)
    except Exception as e:
        print(f"Cubic Spline Error: {e}")

    # Quadratic Mean (RMS)
    quadratic_mean = np.sqrt(np.mean(np.square(np.array(list(self.y_data_sets.values()))), axis=0))

    # Arithmetic-Geometric Mean
    arithmetic_mean = np.mean(np.array(list(self.y_data_sets.values())), axis=0)
    geometric_mean = gmean(np.array(list(self.y_data_sets.values())), axis=0)
    arithmetic_geometric_mean = agm(arithmetic_mean, geometric_mean)
    
    # Contraharmonic Mean
    contraharmonic_mean = np.sum(np.square(np.array(list(self.y_data_sets.values()))), axis=0) / np.sum(np.array(list(self.y_data_sets.values())), axis=0)

    # Geometric-Harmonic Mean
    harmonic_mean = hmean(np.array(list(self.y_data_sets.values())), axis=0)
    geometric_harmonic_mean = np.sqrt(geometric_mean * harmonic_mean)

    # Weighted Harmonic Mean
    weights = np.array([info['r2'] for info in self.best_fits.values()])  # Assuming R^2 as weights
    weighted_harmonic_mean = np.sum(weights) / np.sum(weights / np.array(list(self.y_data_sets.values())), axis=0)

    # Plotting Section
    self.ax.clear()  # Clear existing plots

    # Plot each relationship
    self.ax.plot(self.x_data, final_y_avg, 'r--', label='Simple Average')
    if len(self.x_data) == len(final_y_weighted) and len(self.x_data) > 0:
        self.ax.plot(self.x_data, final_y_weighted, 'g-.', label='Weighted Average')
    else:
        print("Warning: Dimensions of x_data and final_y_weighted do not match or are empty. Skipping this plot.")
    self.ax.plot(self.x_data, final_y_poly, 'b:', label='Polynomial Regression')
    self.ax.plot(self.x_data, final_y_complex, 'm-', label='Complex Operations')
    self.ax.plot(self.x_data, geometric_mean, 'c--', label='Geometric Mean')
    self.ax.plot(self.x_data, harmonic_mean, 'y-.', label='Harmonic Mean')
    self.ax.plot(self.x_data, mode_values, 'g--', label='Mode')
    self.ax.plot(self.x_data, ewma, 'b-.', label='EWMA')
    self.ax.plot(self.x_data, rms, 'm:', label='RMS')
    self.ax.plot(self.x_data, log_mean, 'r--', label='Log Mean')
    self.ax.plot(self.x_data, trimmed_mean, 'g-.', label='Trimmed Mean')
    self.ax.plot(self.x_data, winsorized_mean, 'b:', label='Winsorized Mean')
    self.ax.plot(self.x_data, median_values, 'k--', label='Median')
    self.ax.plot(self.x_data, interpolated_mean, 'r-.', label='Interpolated Mean')
    self.ax.plot(self.x_data, cubic_spline_values, 'g:', label='Cubic Spline')
    self.ax.plot(self.x_data, quadratic_mean, 'b-', label='Quadratic Mean')
    self.ax.plot(self.x_data, arithmetic_geometric_mean, 'c-.', label='Arithmetic-Geometric Mean')
    self.ax.plot(self.x_data, contraharmonic_mean, 'm--', label='Contraharmonic Mean')
    self.ax.plot(self.x_data, geometric_harmonic_mean, 'y:', label='Geometric-Harmonic Mean')
    self.ax.plot(self.x_data, weighted_harmonic_mean, 'k-.', label='Weighted Harmonic Mean')

    # Add labels and title
    self.ax.set_xlabel('X-axis')
    self.ax.set_ylabel('Y-axis')
    self.ax.set_title('Relationships')

    # Add legend
    self.ax.legend(loc='upper right').set_draggable(True)

    # Show plot
    self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window.show()
    sys.exit(app.exec_())
