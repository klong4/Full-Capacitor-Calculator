from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.widgets import CheckButtons
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

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

# Define initial guesses and bounds for each curve type
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
    'Sigmoid': [1, 1]
}

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
    'Sigmoid': ([-np.inf, -np.inf], [np.inf, np.inf])
}

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
    'Sigmoid': sigmoid
}


class CurveFittingApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Curve Fitting App")
        self.setGeometry(100, 100, 800, 600)
        self.createWidgets()
        self.createLayout()

    def createWidgets(self):
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.resultsWindow = self.createResultsWindow()
        self.dataSetDropdown = self.createDataSetDropdown()
        self.loadButton = self.createLoadButton()
        self.fitButton = self.createFitButton()

    def createResultsWindow(self):
        resultsWindow = QtWidgets.QTextEdit()
        resultsWindow.setReadOnly(True)
        return resultsWindow

    def createDataSetDropdown(self):
        dataSetDropdown = QtWidgets.QComboBox()
        dataSetDropdown.currentIndexChanged.connect(self.update_plot)
        return dataSetDropdown

    def createLoadButton(self):
        loadButton = QtWidgets.QPushButton("Load CSV")
        loadButton.clicked.connect(self.load_csv)
        return loadButton

    def createFitButton(self):
        fitButton = QtWidgets.QPushButton("Fit Curve")
        fitButton.clicked.connect(self.fit_curve)
        return fitButton

    def createLayout(self):
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.canvas)
        mainLayout.addWidget(self.dataSetDropdown)
        mainLayout.addWidget(self.loadButton)
        mainLayout.addWidget(self.fitButton)
        mainLayout.addWidget(self.resultsWindow)
        
        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

    def load_csv(self):
        options = QtWidgets.QFileDialog.Options()
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)", options=options)
        
        if filePath:
            df = pd.read_csv(filePath)
            self.x_data = df.iloc[:, 0].tolist()
            self.y_data_sets = df.iloc[:, 1:].to_dict(orient='list')
            
            self.dataSetDropdown.clear()
            self.dataSetDropdown.addItems(list(self.y_data_sets.keys()))
            
            self.update_plot()

    def update_plot(self):
        selected_data_set = self.dataSetDropdown.currentText()
        if selected_data_set:
            self.y_data = self.y_data_sets[selected_data_set]
            self.ax.clear()
            self.ax.plot(self.x_data, self.y_data, 'bo')
            self.canvas.draw()

    def fit_curve(self):
        best_fits = {}
        
        for name, y_data in self.y_data_sets.items():
            best_r2 = -1
            best_fit = None
            
            for curve_name, func in curve_types.items():
                try:
                    # Define initial guesses and bounds based on the curve type
                    if curve_name == 'Linear':
                        initial_guess = [1, 1]
                        bounds = ([-np.inf, -np.inf], [np.inf, np.inf])
                    elif curve_name == 'Quadratic':
                        initial_guess = [1, 1, 1]
                        bounds = ([-np.inf, -np.inf, -np.inf], [np.inf, np.inf, np.inf])
                    # Add more elif conditions for other curve types
                    
                    params, _ = curve_fit(func, np.array(self.x_data), np.array(y_data), p0=initial_guess, bounds=bounds)
                    y_pred = func(np.array(self.x_data), *params)
                    r2 = r2_score(y_data, y_pred)
                    
                    if r2 > best_r2:
                        best_r2 = r2
                        best_fit = curve_name
                except Exception as e:
                    print(f"Failed to fit {curve_name} for {name}: {e}")
            
            best_fits[name] = best_fit
        
        # Display the best fits in the results window
        results_text = "\n".join([f"{name}: {fit}" for name, fit in best_fits.items()])
        self.resultsWindow.setText(f"Best Fits:\n{results_text}")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = CurveFittingApp()
    window.show()
    app.exec_()
