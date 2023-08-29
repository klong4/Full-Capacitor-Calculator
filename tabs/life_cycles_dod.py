from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np

class LifeCyclesDODTAB(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        mainLayout = QtWidgets.QHBoxLayout()

        # Inputs and Button Layout
        inputsLayout = QtWidgets.QVBoxLayout()
        inputsWidget = QtWidgets.QWidget()
        inputsWidget.setLayout(inputsLayout)
        inputsWidget.setFixedWidth(325)
        mainLayout.addWidget(inputsWidget)

        # Create input fields
        def create_input_field(label_text, tooltip, units):
            layout = QtWidgets.QHBoxLayout()
            input_field = QtWidgets.QLineEdit()
            input_field.setToolTip(tooltip)
            unit_dropdown = QtWidgets.QComboBox()
            unit_dropdown.addItems(units)
            layout.addWidget(QtWidgets.QLabel(label_text))
            layout.addWidget(input_field)
            layout.addWidget(unit_dropdown)
            return layout, input_field, unit_dropdown

        # Add your input fields here
        layout, self.capacitanceInput, _ = create_input_field("Capacitance:", "Capacitance of the capacitor.", ["F"])
        inputsLayout.addLayout(layout)
        layout, self.startVoltageInput, _ = create_input_field("Starting Voltage:", "Starting voltage of the capacitor.", ["V"])
        inputsLayout.addLayout(layout)
        layout, self.endVoltageInput, _ = create_input_field("Ending Voltage:", "Ending voltage of the capacitor.", ["V"])
        inputsLayout.addLayout(layout)
        layout, self.dischargeCurrentInput, _ = create_input_field("Discharge Current:", "Discharge current of the capacitor.", ["A"])
        inputsLayout.addLayout(layout)

        # Calculate Button
        calculateButton = QtWidgets.QPushButton("Calculate")
        calculateButton.clicked.connect(self.calculate)
        inputsLayout.addWidget(calculateButton)

        # Results Display
        self.resultsLabel = QtWidgets.QLabel()
        inputsLayout.addWidget(self.resultsLabel)

        # Formula Display
        self.formulaWindow = QtWidgets.QTextEdit()
        self.formulaWindow.setReadOnly(True)
        self.formulaWindow.setFixedWidth(300)
        self.formulaWindow.setText("Click Calculate to see the formula.")
        inputsLayout.addWidget(self.formulaWindow)

        mainLayout.addLayout(inputsLayout)

        # Plot Layout
        plotLayout = QtWidgets.QVBoxLayout()
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.figure.tight_layout()

        # Adding Custom Navigation Toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        plotLayout.addWidget(self.toolbar)
        plotLayout.addWidget(self.canvas)

        mainLayout.addLayout(plotLayout)

        self.setLayout(mainLayout)

    def calculate(self):
        # Clear the figure for new plots
        self.figure.clf()
        self.ax = self.figure.add_subplot(1, 1, 1)

        # Validate the input fields
        if not all([self.capacitanceInput.text(), self.startVoltageInput.text(), self.endVoltageInput.text(), self.dischargeCurrentInput.text()]):
            self.formulaWindow.setText("Please input all required fields.")
            return

        # Retrieve the values from the input fields
        capacitance = float(self.capacitanceInput.text())
        startVoltage = float(self.startVoltageInput.text())
        endVoltage = float(self.endVoltageInput.text())
        dischargeCurrent = float(self.dischargeCurrentInput.text())

        # Use the derived formula for life cycle calculation based on DoD
        def life_cycle_formula(x):
            return 6.64 * x + (-4.57)

        # Generate the graph data
        dod_values = np.linspace(startVoltage, endVoltage, 100)
        y_values = life_cycle_formula(dod_values)

        # Plotting the graph
        self.ax.clear()
        self.ax.plot(dod_values, y_values)
        self.ax.set_xlabel('DoD')
        self.ax.set_ylabel('Life Cycle')
        self.ax.ticklabel_format(style='plain', axis='both')
        self.ax.set_xticklabels(self.ax.get_xticks(), rotation=90)
        self.canvas.draw()

        # Update formula window with the formula
        self.formulaWindow.setText("Final Formula:\n6.64x + (-4.57)")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = LifeCyclesDODTAB()
    window.show()
    sys.exit(app.exec_())
