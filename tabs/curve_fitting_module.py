from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.widgets import CheckButtons
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from utils.calculations import curve_types, initial_guesses, bounds

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
        self.canvas.mpl_connect('pick_event', self.on_pick)
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
        self.ax.clear()
        for i, (name, y_data) in enumerate(self.y_data_sets.items()):
            line, = self.ax.plot(self.x_data, y_data, marker='o', linestyle='', picker=5, label=name)
            line.set_color(plt.cm.jet(i / len(self.y_data_sets)))
        
        self.ax.legend(loc='upper right')
        self.canvas.draw()

    def fit_curve(self):
        best_fits = {}
        for i, (name, y_data) in enumerate(self.y_data_sets.items()):
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
            
            best_fits[name] = best_fit
            
            if best_fit:
                func = curve_types[best_fit]
                y_pred = func(np.array(self.x_data), *best_params)
                line, = self.ax.plot(self.x_data, y_pred, picker=5, label=f"{name} ({best_fit})")
                line.set_color(plt.cm.jet(i / len(self.y_data_sets)))
        
        self.ax.legend(loc='upper right')
        self.canvas.draw()
        
        results_text = "\n".join([f"{name}: {fit}" for name, fit in best_fits.items()])
        self.resultsWindow.setText(f"Best Fits:\n{results_text}")

    def on_pick(self, event):
        line = event.artist
        line.set_visible(not line.get_visible())
        self.canvas.draw()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = CurveFittingApp()
    window.show()
    app.exec_()
