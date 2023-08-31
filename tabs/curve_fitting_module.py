# Curve Fitting Module
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QFileDialog, QTextEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from scipy.optimize import curve_fit
from utils.calculate_relationship import calculate_relationship
from utils.mapping import curve_types, initial_guesses, bounds
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class CurveFittingApp(QWidget):
    def __init__(self):
        super().__init__()

        self.data_loaded = False
        self.x_data = None
        self.y_data_sets = {}
        self.best_fits = {}

        self.init_ui()

    def init_ui(self):
        self.figure, self.ax = self.create_plot()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)  # Add navigation toolbar

        self.loadButton = QPushButton('Load Data')
        self.loadButton.clicked.connect(self.load_data)

        self.fitButton = QPushButton('Fit Curve')
        self.fitButton.clicked.connect(self.fit_curve)

        self.relationshipButton = QPushButton('Find Relationship')
        self.relationshipButton.clicked.connect(self.find_relationship)

        self.dataSetDropdown = QComboBox()  # Define the dropdown here
        self.dataSetDropdown.addItem("Select Data Set")

        self.statusWindow = QTextEdit()
        self.statusWindow.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)  # Add navigation toolbar
        layout.addWidget(self.canvas)
        layout.addWidget(self.loadButton)
        layout.addWidget(self.fitButton)
        layout.addWidget(self.relationshipButton)
        layout.addWidget(QLabel('Choose Data Set:'))  # Move this line here
        layout.addWidget(self.dataSetDropdown)  # Move this line here
        layout.addWidget(self.statusWindow)

        self.setLayout(layout)

    def create_plot(self):
        fig = Figure()
        ax = fig.add_subplot(111)
        return fig, ax

    def load_data(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Load Data File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if filePath:
            data = np.loadtxt(filePath, delimiter=',', skiprows=1)  # Skip header row
            self.x_data = data[:, 0]  # First column is X values
        
            num_columns = data.shape[1]
            if num_columns > 1:
                self.y_data_sets = {f"Data Set {i+1}": data[:, i] for i in range(1, num_columns)}
                self.dataSetDropdown.clear()
                self.dataSetDropdown.addItems([f"Data Set {i}" for i in range(1, num_columns)])
                self.plot_data()  # Plot the loaded data
                self.data_loaded = True
            else:
                print("No y-values found in the CSV file.")

    def plot_data(self):
        self.ax.clear()  # Clear the existing plot
        for curve_name, y_data in self.y_data_sets.items():
            self.ax.plot(self.x_data, y_data, label=curve_name)
        self.ax.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Place legend outside the plot
        self.ax.set_xlabel('X Values')
        self.ax.set_ylabel('Y Values')
        self.ax.set_title('Data Sets')
        self.canvas.draw()  # Redraw the canvas

    def fit_curve(self):
        if not self.data_loaded:
            print("Data not loaded. Cannot fit.")
            return

        best_fit_info = {}
        fitted_curves = {}  # Store the fitted curves for plotting

        for curve_name, y_data in self.y_data_sets.items():
            try:
                best_r2 = -1  # Initialize the best R-squared value
                best_fit_algorithm = None  # Initialize the best fit algorithm
                for func_name, func in curve_types.items():
                    params, params_covariance = curve_fit(func, self.x_data, y_data, p0=initial_guesses[func_name], bounds=bounds[func_name])
                    fitted_y = func(self.x_data, *params)
                    r_squared = 1 - (np.sum((y_data - fitted_y) ** 2) / ((len(y_data) - 1) * np.var(y_data, ddof=1)))
                    if r_squared > best_r2:
                        best_r2 = r_squared
                        best_fit_algorithm = func_name

                    if curve_name not in best_fit_info:
                        best_fit_info[curve_name] = {}
                    best_fit_info[curve_name][func_name] = {'params': params, 'r2': r_squared}
                    fitted_curves[(curve_name, func_name)] = fitted_y
                self.statusWindow.append(f"Best fit algorithm for {curve_name}: {best_fit_algorithm}\n")
            except Exception as e:
                print(f"Couldn't fit {curve_name} with {func_name} because {e}")

        self.best_fits = best_fit_info  # Store the best fit information for each curve type

        # Plot the fitted curves
        self.ax.clear()  # Clear the existing plot
        for curve_name, y_data in self.y_data_sets.items():
            self.ax.plot(self.x_data, y_data, label=curve_name)
            for func_name in curve_types.keys():
                fitted_y = fitted_curves.get((curve_name, func_name))
                if fitted_y is not None:
                    self.ax.plot(self.x_data, fitted_y, label=f"{curve_name} {func_name} Fit")
        self.ax.legend()

        self.canvas.draw()  # Redraw the canvas

    def find_relationship(self):
        if not self.data_loaded:
            print("Data not loaded. Cannot find relationship.")
            return

        self.statusWindow.clear()
        for curve_name, fit_info in self.best_fits.items():
            self.statusWindow.append(f"Calculating relationships for {curve_name}...\n")
            calculate_relationship(fit_info)  # Pass the fit_info dictionary directly

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = CurveFittingApp()
    ex.show()
    sys.exit(app.exec_())