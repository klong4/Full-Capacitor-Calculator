import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
from numpy.polynomial.polynomial import Polynomial
from matplotlib.lines import Line2D


# Define curve types, initial guesses, and bounds (imported from utils.calculations)
from utils.calculations import curve_types, initial_guesses, bounds

class CurveFittingApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.x_data = np.linspace(0, 10, 100)  # Example x_data
        self.best_fits = {}  # Example best_fits (to be populated later)
        self.ax = None  # Will be set in createWidgets()

        self.initUI()

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
        self.dataSetDropdown = QtWidgets.QComboBox()
        self.dataSetDropdown.currentIndexChanged.connect(self.update_plot)
        self.loadButton = QtWidgets.QPushButton("Load CSV", clicked=self.load_csv)
        self.fitButton = QtWidgets.QPushButton("Fit Curve", clicked=self.fit_curve)
        self.calculateButton = QtWidgets.QPushButton("Calculate Relationship", clicked=self.calculate_relationship)

    def createLayout(self):
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.toolbar)
        mainLayout.addWidget(self.canvas)
        mainLayout.addWidget(self.dataSetDropdown)
        mainLayout.addWidget(self.loadButton)
        mainLayout.addWidget(self.fitButton)
        mainLayout.addWidget(self.calculateButton)
        mainLayout.addWidget(self.resultsWindow)

        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

    def load_csv(self):
        options = QtWidgets.QFileDialog.Options()
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)", options=options)
    
        if filePath:
            df = pd.read_csv(filePath)
            self.x_data = df.iloc[:, 0].tolist()  # Update x_data with the first column of the CSV
            self.y_data_sets = df.iloc[:, 1:].to_dict(orient='list')
            self.dataSetDropdown.clear()
            self.dataSetDropdown.addItems(list(self.y_data_sets.keys()))

    def update_plot(self):
        self.ax.clear()
        for i, (name, y_data) in enumerate(self.y_data_sets.items()):
            line, = self.ax.plot(self.x_data, y_data, marker='o', linestyle='', picker=5, label=name)
            line.set_color(plt.cm.jet(i / len(self.y_data_sets)))
        self.canvas.draw()

    def fit_curve(self):
        name = "Sample Data"  # Replace with the actual name you want to use for the data

        try:
            print(f"Trying to fit curves for {name}...")

            self.best_fits = {}  # Reset best fits
            for i, y_data in enumerate(self.y_data_sets.values()):
                best_r2 = -1
                best_fit = None
                best_params = None

                for curve_name, func in curve_types.items():
                    try:
                        initial_guess = initial_guesses[curve_name]
                        bound = bounds[curve_name]

                        params, _ = curve_fit(func, np.array(self.x_data), np.array(y_data), p0=initial_guess, bounds=bound)
                        y_pred = func(np.array(self.x_data), *params)
                        r2 = r2_score(y_data, y_pred)

                        if r2 > best_r2:
                            best_r2 = r2
                            best_fit = curve_name
                            best_params = params
                    except Exception as e:
                        print(f"Failed to fit {curve_name} for {name}: {e}")

                if best_fit:
                    self.best_fits[name] = {'fit': best_fit, 'params': best_params, 'r2': best_r2}
                    func = curve_types[best_fit]
                    y_pred = func(np.array(self.x_data), *best_params)
                    line, = self.ax.plot(self.x_data, y_pred, picker=5, label=f"{name} ({best_fit})")
                    line.set_color(plt.cm.jet(i / len(self.y_data_sets)))

            self.ax.legend(loc='upper right').set_draggable(True)  # Make the legend draggable
            self.canvas.draw()

            results_text = "\n".join([f"{name}: {fit['fit']}" for name, fit in self.best_fits.items()])
            self.resultsWindow.setText(f"Best Fits:\n{results_text}")

        except Exception as e:
            print(f"Failed to fit curves for {name}: {e}")    
    
def calculate_relationship(self):
    name = "Sample Data"
        
    final_y_avg = np.zeros_like(self.x_data)
    all_params = np.array([info['params'] for info in self.best_fits.values()])

    for name, info in self.best_fits.items():
        best_fit = info['fit']
        best_params = info['params']
        func = curve_types[best_fit]
        final_y_avg += func(np.array(self.x_data), *best_params)
    final_y_avg /= len(self.best_fits)

    median_values = np.zeros_like(self.x_data)
    median_params = np.median(all_params, axis=0)
    
    for i, x in enumerate(self.x_data):
        median_value = 0
        for curve_name, func in curve_types.items():
            params = median_params
            try:
                median_value += func(np.array([x]), *params)
            except Exception as e:
                print(f"Failed to calculate median for {curve_name}: {e}")
        median_values[i] = median_value / len(curve_types)

    # Rest of the code...


        # Approach 2: Weighted Average Based on R^2 Value
        final_y_weighted = np.zeros_like(self.x_data)
        total_weight = 0
        for name, info in self.best_fits.items():
            best_fit = info['fit']
            best_params = info['params']
            r2 = info['r2']
            func = curve_types[best_fit]
            final_y_weighted += r2 * func(np.array(self.x_data), *best_params)
            total_weight += r2
        final_y_weighted /= total_weight

        # Approach 3: Polynomial Regression on Best Fits
        p = Polynomial.fit(self.x_data, final_y_avg, 4)
        final_y_poly = p(np.array(self.x_data))

        # Approach 4: Complex Mathematical Operations
        final_y_complex = np.ones_like(self.x_data)
        for name, info in self.best_fits.items():
            best_fit = info['fit']
            best_params = info['params']
            func = curve_types[best_fit]
            final_y_complex *= func(np.array(self.x_data), *best_params)
        final_y_complex = np.sqrt(final_y_complex)

        # Approach 5: Geometric Mean
        geometric_mean = np.ones_like(self.x_data)
        for name, info in self.best_fits.items():
            best_fit = info['fit']
            best_params = info['params']
            func = curve_types[best_fit]
            geometric_mean *= func(np.array(self.x_data), *best_params)
        geometric_mean = np.power(geometric_mean, 1 / len(self.best_fits))

        # Approach 6: Harmonic Mean
        harmonic_mean = np.zeros_like(self.x_data)
        for name, info in self.best_fits.items():
            best_fit = info['fit']
            best_params = info['params']
            func = curve_types[best_fit]
            harmonic_mean += 1 / func(np.array(self.x_data), *best_params)
        harmonic_mean = len(self.best_fits) / harmonic_mean

        # Approach 7: Median
        median_values = np.median(np.array([info['params'] for info in self.best_fits.values()]), axis=0)

        # Approach 8: Mode (Not a typical approach for continuous data)
        mode_values = stats.mode(np.array([info['params'] for info in self.best_fits.values()]), axis=0)[0][0]

        # Approach 9: Exponential Weighted Moving Average (EWMA)
        alpha = 0.2
        ewma = np.zeros_like(self.x_data)
        for name, info in self.best_fits.items():
            best_fit = info['fit']
            best_params = info['params']
            func = curve_types[best_fit]
            y_values = func(np.array(self.x_data), *best_params)
            ewma = alpha * y_values + (1 - alpha) * ewma

        # Approach 10: Root Mean Square (RMS)
        rms = np.zeros_like(self.x_data)
        for name, info in self.best_fits.items():
            best_fit = info['fit']
            best_params = info['params']
            func = curve_types[best_fit]
            y_values = func(np.array(self.x_data), *best_params)
            rms += y_values ** 2
        rms = np.sqrt(rms / len(self.best_fits))

        # Approach 11: Logarithmic Mean
        log_mean = np.zeros_like(self.x_data)
        for name, info in self.best_fits.items():
            best_fit = info['fit']
            best_params = info['params']
            func = curve_types[best_fit]
            y_values = func(np.array(self.x_data), *best_params)
            log_mean += np.log(y_values)
        log_mean = np.exp(log_mean / len(self.best_fits))

        # Approach 12: Trimmed Mean (Trim 10% from each end)
        trimmed_mean_list = []
        for name, info in self.best_fits.items():
            best_fit = info['fit']
            best_params = info['params']
            func = curve_types[best_fit]
            y_values = func(np.array(self.x_data), *best_params)
            trimmed_mean_list.append(y_values)
        trimmed_mean = stats.trim_mean(np.array(trimmed_mean_list), 0.1, axis=0)

        # Approach 13: Winsorized Mean (Winsorize 5% from each end)
        winsorized_mean_list = []
        for name, info in self.best_fits.items():
            best_fit = info['fit']
            best_params = info['params']
            func = curve_types[best_fit]
            y_values = func(np.array(self.x_data), *best_params)
            winsorized_mean_list.append(y_values)
        winsorized_mean = stats.mstats.winsorize(np.array(winsorized_mean_list), limits=[0.05, 0.05])

        # Plotting all the relationship lines with unique identifiers and make them pickable
        line1, = self.ax.plot(self.x_data, final_y_avg, 'r--', label='Simple Average', gid='relationship_line', picker=5)
        line2, = self.ax.plot(self.x_data, final_y_weighted, 'g-.', label='Weighted Average', gid='relationship_line', picker=5)
        line3, = self.ax.plot(self.x_data, final_y_poly, 'b:', label='Polynomial Regression', gid='relationship_line', picker=5)
        line4, = self.ax.plot(self.x_data, final_y_complex, 'm-', label='Complex Operations', gid='relationship_line', picker=5)
        line5, = self.ax.plot(self.x_data, geometric_mean, 'c--', label='Geometric Mean', gid='relationship_line', picker=5)
        line6, = self.ax.plot(self.x_data, harmonic_mean, 'y-.', label='Harmonic Mean', gid='relationship_line', picker=5)
        line7, = self.ax.plot(self.x_data, median_values, 'k:', label='Median', gid='relationship_line', picker=5)
        line8, = self.ax.plot(self.x_data, mode_values, 'g--', label='Mode', gid='relationship_line', picker=5)
        line9, = self.ax.plot(self.x_data, ewma, 'b-.', label='EWMA', gid='relationship_line', picker=5)
        line10, = self.ax.plot(self.x_data, rms, 'm:', label='RMS', gid='relationship_line', picker=5)
        line11, = self.ax.plot(self.x_data, log_mean, 'r--', label='Log Mean', gid='relationship_line', picker=5)
        line12, = self.ax.plot(self.x_data, trimmed_mean, 'g-.', label='Trimmed Mean', gid='relationship_line', picker=5)
        line13, = self.ax.plot(self.x_data, winsorized_mean, 'b:', label='Winsorized Mean', gid='relationship_line', picker=5)

        # Update the plot and results window
        self.ax.legend(loc='upper right').set_draggable(True)  # Make the legend draggable
        self.canvas.draw()
        
        # Define equations dictionary for storing equations for each approach
        equations = {}

        # Update the results window with equations for each approach
        equations['Simple Average'] = 'y = (1/n) * Σ f_i(x)'
        equations['Weighted Average'] = 'y = (1/Σ R^2) * Σ (R^2 * f_i(x))'
        equations['Polynomial Regression'] = f'Polynomial: {p}'
        equations['Complex Operations'] = 'y = sqrt(Π f_i(x))'
        equations['Geometric Mean'] = 'y = √(Π f_i(x))'
        equations['Harmonic Mean'] = 'y = n / Σ (1 / f_i(x))'
        equations['Median'] = 'y = median(f_i(x))'
        equations['Mode'] = 'y = mode(f_i(x))'
        equations['EWMA'] = f'y[n] = α * f_i(x)[n] + (1 - α) * y[n-1]'
        equations['RMS'] = 'y = √(Σ f_i(x)^2 / n)'
        equations['Log Mean'] = 'y = exp(Σ ln(f_i(x)) / n)'
        equations['Trimmed Mean'] = 'y = trimmed_mean(f_i(x))'
        equations['Winsorized Mean'] = 'y = winsorized_mean(f_i(x))'

        results_text = "\n".join([f"{approach}: {eq}" for approach, eq in equations.items()])
        self.resultsWindow.setText(f"Equations for Each Approach:\n{results_text}")

    def on_pick(self, event):
        if isinstance(event.artist, Line2D):
            picked_line = event.artist
            label = picked_line.get_label()

            # Highlight the picked line
            picked_line.set_linewidth(3)
            self.ax.legend(loc='upper right').set_draggable(True)
            self.canvas.draw()

            # Access best fit information for the picked line
            if label in self.best_fits:
                best_fit_info = self.best_fits[label]
                best_fit = best_fit_info['fit']
                best_params = best_fit_info['params']
                r2 = best_fit_info['r2']

                # Example: Print detailed information about the best fit
                print(f"Selected Line: {label}")
                print(f"Best Fit: {best_fit}")
                print(f"Best Fit Parameters: {best_params}")
                print(f"R-squared Value: {r2}")

                # Perform more advanced actions based on the picked line
                # For example, you could update a separate results area with the selected line's details

        else:
            print("Pick event detected, but not on a Line2D object")

    # Reset the linewidth of all lines (unhighlight all lines except the picked one)
    for line in self.ax.lines:
        line.set_linewidth(1)
    self.ax.legend(loc='upper right').set_draggable(True)
    self.canvas.draw()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = CurveFittingApp()
    window.show()
    app.exec_()
