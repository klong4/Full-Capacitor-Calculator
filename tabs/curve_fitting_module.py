# Curve Fitting Module
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score, mean_squared_error
from numpy.polynomial.polynomial import Polynomial
from matplotlib.lines import Line2D
from scipy.interpolate import interp1d, CubicSpline
from sklearn.model_selection import ParameterGrid
from scipy.stats.mstats import winsorize, gmean, hmean
from scipy.stats import mode, trim_mean
from PyQt5 import QtWidgets
from utils.mapping import curve_types, initial_guesses, bounds
from utils.calculate_relationship import calculate_relationship
from utils.calculations import calculate_rms
from PyQt5.QtWidgets import QFileDialog


class CurveFittingApp(QWidget):
    def __init__(self, *args, **kwargs):
        super(CurveFittingApp, self).__init__(*args, **kwargs)

        self.figure, self.ax = plt.subplots()  # Initialize figure and axes
        self.canvas = FigureCanvas(self.figure)
        self.calculate_relationship = calculate_relationship

        # Initialize x_data, best_fits, and y_data_sets
        self.x_data = np.array([])  # Initialize as empty array
        self.best_fits = {}  # Initialize as empty dictionary
        self.y_data_sets = {}  # Initialize as empty dictionary
        self.data_loaded = False  # Flag to check if data is loaded

        # Initialize the UI
        self.initUI()

    def on_pick(self, event):
        # Your code to handle the pick event
        print("Pick event detected!")

    def update_plot(self):
        # Your code to update the plot
        print("Updating plot!")

    def my_function(self, x, a, b, c):
        return a * np.exp(-b * x) + c

    def initUI(self):
        self.setWindowTitle("Combined Curve Fitting App")
        self.setGeometry(100, 100, 800, 600)
        self.createWidgets()
        self.createLayout()
    
    def createWidgets(self):
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.mpl_connect('pick_event', self.on_pick)  # Connect pick event to the handler
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.resultsWindow = QtWidgets.QTextEdit()
        self.resultsWindow.setReadOnly(True)
        self.dataSetDropdown = QtWidgets.QComboBox()  # Add QtWidgets. before QComboBox
        self.dataSetDropdown.currentIndexChanged.connect(self.update_plot)
        self.loadButton = QtWidgets.QPushButton("Load CSV", clicked=self.load_csv)
        self.fitButton = QtWidgets.QPushButton("Fit Curve", clicked=self.fit_curve)
        self.calculateButton = QtWidgets.QPushButton("Calculate Relationship", clicked=self.calculate_relationship)

    def createLayout(self):
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.toolbar)
        mainLayout.addWidget(self.canvas)
        mainLayout.addWidget(self.dataSetDropdown)
        mainLayout.addWidget(self.loadButton)
        mainLayout.addWidget(self.fitButton)
        mainLayout.addWidget(self.resultsWindow)
        self.setLayout(mainLayout)

    def load_csv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        csv_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if csv_path:
            try:
                df = pd.read_csv(csv_path, header=None)
                self.x_data = df.iloc[:, 0].values  # First column as x-data
            
                self.y_data_sets = {}  # Reset the existing y_data_sets
            
                for idx, col in enumerate(df.columns[1:]):  # Loop through all columns other than the first one
                    curve_name = f"Curve {idx + 1}"  # Generate a curve name
                    self.y_data_sets[curve_name] = df[col].values  # Each subsequent column as a different y-dataset
            
                self.data_loaded = True
                print("CSV loaded successfully.")
            
                # Update the dropdown for selecting y-datasets
                self.dataSetDropdown.clear()
                self.dataSetDropdown.addItems(list(self.y_data_sets.keys()))
            
            except Exception as e:
                print(f"Error in loading CSV: {e}")
                self.data_loaded = False
        else:
            print("No file selected.")

    def fit_curve(self):
        if not self.data_loaded:
            print("Data not loaded. Cannot fit.")
            return
    try:
        # Define the curve function you're trying to fit
        def my_function(x, a, b, c):
            return a * np.exp(-b * x) + c

        # Perform curve fitting
        params, params_covariance = curve_fit(my_function, self.x_data, self.y_data)

        # Print the covariance of parameters
        print("Covariance of parameters: ", params_covariance)

        # Calculate R-squared value to evaluate the fit
        residuals = self.y_data - my_function(self.x_data, *params)
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((self.y_data - np.mean(self.y_data))**2)
        r2 = 1 - (ss_res / ss_tot)

        # Use calculate_rms to get the root mean square of the residuals
        rms_value = self.calculate_rms(residuals)
        
        print(f"Fit successful. R^2 value is {r2}")
        print(f"Root Mean Square of residuals: {rms_value}")

    except Exception as e:
        print(f"An error occurred while fitting the curve: {e}")
        
    def update_plot(self):
        print("Updating plot...")

        # Debug: Print out data to ensure it's loaded
        print(f"x_data: {self.x_data}")
        print(f"y_data_sets: {self.y_data_sets}")

        self.ax.clear()  # Clear previous plot

        # Check if data is loaded, skip if not
        if not self.data_loaded:
            print("Data not loaded, skipping plot update.")
            return

        try:
            for i, (name, y_data) in enumerate(self.y_data_sets.items()):
                self.ax.plot(self.x_data, y_data, marker='o', linestyle='', label=name)
                print(f"Plotted {name}")

            self.ax.set_yscale('log')  # Set y-axis to log scale, if applicable
            self.ax.set_xscale('log')  # Set x-axis to log scale, if applicable

            self.ax.legend(loc='upper right')
            self.canvas.draw()
        except Exception as e:
            print(f"Error in updating plot: {e}")

        print("Plot update complete.")

# Define dynamic_initial_guess and other utility methods here
def dynamic_initial_guess(self, x_data, y_data):
    # ... (Your dynamic initial guess logic here)
    return None  # Placeholder, replace with your logic

def on_pick(self, event):
    if isinstance(event.artist, Line2D):
        picked_line = event.artist
        label = picked_line.get_label()

        picked_line.set_linewidth(3)
        self.ax.legend(loc='upper right').set_draggable(True)
        self.canvas.draw()

        if label in self.best_fits:
            best_fit_info = self.best_fits[label]
            best_fit = best_fit_info['fit']
            best_params = best_fit_info['params']
            r2 = best_fit_info['r2']

            print(f"Selected Line: {label}")
            print(f"Best Fit: {best_fit}")
            print(f"Best Fit Parameters: {best_params}")
            print(f"R-squared Value: {r2}")

        else:
            print("Pick event detected, but not on a Line2D object")

        for line in self.ax.lines:
            line.set_linewidth(1)
        self.ax.legend(loc='upper right').set_draggable(True)
        self.canvas.draw()

# Your additional methods (e.g., fit_data, calculate_rms, etc.)
def fit_data(self):
    if not self.data_loaded:
        print("Data not loaded. Cannot fit.")
        return
        
    # Assuming that self.x_data and self.y_data are loaded
    try:
        # Define the curve function you're trying to fit
        def my_function(x, a, b, c):
            return a * np.exp(-b * x) + c
            
        params, params_covariance = curve_fit(my_function, self.x_data, self.y_data)
            
        # Calculate R-squared value to evaluate the fit
        residuals = self.y_data - my_function(self.x_data, *params)
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((self.y_data - np.mean(self.y_data))**2)
        r2 = 1 - (ss_res / ss_tot)
            
        print(f"Fit successful. R^2 value is {r2}")
            
    except Exception as e:
        print(f"An error occurred while fitting the data: {e}")
    
def calculate_rms(self, array):
    """Calculate the root mean square of the given array."""
    return math.sqrt(mean_squared_error(array, np.zeros_like(array)))

if __name__ == "__main__":
    app = QApplication([])
    window = CurveFittingApp()
    window.show()
    app.exec_()
