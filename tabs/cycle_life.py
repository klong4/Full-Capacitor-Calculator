from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np

class CycleLifeTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        mainLayout = QtWidgets.QHBoxLayout()

        # Inputs and Button Layout
        inputsLayout = QtWidgets.QVBoxLayout()
        inputsWidget = QtWidgets.QWidget()
        inputsWidget.setLayout(inputsLayout)
        inputsWidget.setFixedWidth(325)
        mainLayout.addWidget(inputsWidget)

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

        layout, self.L0Input, _ = create_input_field("Guaranteed Life (L0):", "Guaranteed Life (L0): The guaranteed life of the capacitor at maximum operating temperature.", ["hours"])
        inputsLayout.addLayout(layout)
        layout, self.T0Input, _ = create_input_field("Maximum Operating Temperature (T0):", "Maximum Operating Temperature (T0): The maximum temperature that the capacitor can withstand.", ["°C"])
        inputsLayout.addLayout(layout)
        layout, self.TxInput, _ = create_input_field("Actual Operating Temperature (Tx):", "Actual Operating Temperature (Tx): The actual temperature of the environment where the capacitor will be used.", ["°C"])
        inputsLayout.addLayout(layout)
        layout, self.V0Input, _ = create_input_field("Rated Voltage (V0):", "Rated Voltage (V0): The maximum voltage that the capacitor is rated for.", ["V"])
        inputsLayout.addLayout(layout)
        layout, self.VxInput, _ = create_input_field("Working Voltage (Vx):", "Working Voltage (Vx): The voltage applied to the capacitor in the application.", ["V"])
        inputsLayout.addLayout(layout)

        # Capacitor Technology Dropdown
        self.capacitorTechDropdown = QtWidgets.QComboBox()
        self.capacitorTechDropdown.addItems(["EDLC 3V", "EDLC 2.7V", "LiC 20-85 celsius", "LiC 20-70 celsius", "LCC"])
        self.capacitorTechDropdown.currentIndexChanged.connect(self.update_formula_window)
        inputsLayout.addWidget(QtWidgets.QLabel("Capacitor Technology:"))
        inputsLayout.addWidget(self.capacitorTechDropdown)

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
        self.formulaWindow.setText("Choose a graph type and click Calculate to see the formula.")
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

    def update_formula_window(self):
        tech = self.capacitorTechDropdown.currentText()
        formula_text = self.get_formula_text(tech)
        self.formulaWindow.setText(formula_text)

    def get_formula_text(self, tech):
        formulas = {
            "EDLC 3V": "Lx = L0 * 3.1 * ((T0 - Tx) / 10) * 1.58 * ((V0 - Vx) / .1)",
            "EDLC 2.7V": "Lx = L0 * 3.25 * ((T0 - Tx) / 10) * 1.52 * ((V0 - Vx) / .1)",
            "LiC 20-85 celsius": "Lx = L0 * 2.45 * ((T0 - Tx) / 10) * 1.58 * ((V0 - Vx) / .1)",
            "LiC 20-70 celsius": "Lx = L0 * 2.42 * ((T0 - Tx) / 10) * 1.34 * ((V0 - Vx) / .1)",
            "LCC": "Lx = L0 * 2 * ((T0 - Tx) / 10) * 2 * ((V0 - Vx) / .2)"
        }
        return f"{tech} Formula:\n{formulas[tech]}"

    def calculate(self):
        self.figure.clf()
        self.ax = self.figure.add_subplot(1, 1, 1)
    
        self.calculate_voltage_cycles()
    
        self.figure.tight_layout()  # Apply tight layout
        self.canvas.draw()  # Redraw the canvas after calculating

    def validate_inputs(self):
        # Check if all required input fields are filled in
        required_inputs = [self.L0Input, self.T0Input, self.TxInput, self.V0Input, self.VxInput]
        return all(input_field.text() for input_field in required_inputs)

    def calculate_voltage_cycles(self):
        # Initialize formula to None
        formula = None

        # Validate the input fields
        if not self.validate_inputs():
            self.formulaWindow.setText("Please input all required fields.")
            return

        # Retrieve the values from the input fields
        L0 = float(self.L0Input.text())
        T0 = float(self.T0Input.text())
        Tx = float(self.TxInput.text())
        V0 = float(self.V0Input.text())
        Vx = float(self.VxInput.text())

        # Determine the formula based on the selected capacitor technology
        tech = self.capacitorTechDropdown.currentText()
        if tech == "EDLC 3V":
            formula = lambda x: L0 * 3.1 * ((T0 - Tx) / 10) * 1.58 * ((V0 - x) / .1)
        elif tech == "EDLC 2.7V":
            formula = lambda x: L0 * 3.25 * ((T0 - Tx) / 10) * 1.52 * ((V0 - x) / .1)
        elif tech == "LiC 20-85 celsius":
            formula = lambda x: L0 * 2.45 * ((T0 - Tx) / 10) * 1.58 * ((V0 - x) / .1)
        elif tech == "LiC 20-70 celsius":
            formula = lambda x: L0 * 2.42 * ((T0 - Tx) / 10) * 1.34 * ((V0 - x) / .1)
        elif tech == "LCC":
            formula = lambda x: L0 * 2 * ((T0 - Tx) / 10) * 2 * ((V0 - x) / .2)   
            
        # Check if formula is defined before using it
        if formula is not None:
            voltages = np.linspace(0, V0, 100)
            cycles = [formula(v) for v in voltages]

            self.ax.clear()
            self.ax.plot(cycles, voltages)
            self.ax.set_xlabel('Cycles')
            self.ax.set_ylabel('Voltage (V)')
            self.ax.ticklabel_format(style='plain', axis='both')
            self.ax.set_xticklabels(self.ax.get_xticks(), rotation=90)
            self.canvas.draw()
            self.ax.set_xticklabels(self.ax.get_xticks(), rotation=90)

            formula_text = self.get_formula_text(tech)
            formula_text += f"\nL0 = {L0}, T0 = {T0}, Tx = {Tx}, V0 = {V0}, Vx = {Vx}"
            self.formulaWindow.setText(formula_text)
        else:
            self.formulaWindow.setText("Formula is not defined. Please select a valid technology.")
                        
        # Generate the graph data
        voltages = np.linspace(0, V0, 100)
        cycles = [formula(v) for v in voltages]

        # Plotting the graph
        self.ax.clear()
        self.ax.plot(cycles, voltages)  # Cycles on x-axis, Voltage on y-axis
        self.ax.set_xlabel('Cycles')
        self.ax.set_ylabel('Voltage (V)')
        self.ax.ticklabel_format(style='plain', axis='both')  # Avoid scientific notation
        self.ax.set_xticklabels(self.ax.get_xticks(), rotation=90)  # Vertical x-axis labels
        self.canvas.draw()
        self.ax.set_xticklabels(self.ax.get_xticks(), rotation=90)  # Rotate x-axis labels

        # Update formula window with the formula and values
        formula_text = self.get_formula_text(tech)
        formula_text += f"\nL0 = {L0}, T0 = {T0}, Tx = {Tx}, V0 = {V0}, Vx = {Vx}"
        self.formulaWindow.setText(formula_text)