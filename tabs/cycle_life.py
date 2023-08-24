from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class CycleLifeTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        mainLayout = QtWidgets.QHBoxLayout()  # Main horizontal layout

        # Inputs and Button Layout
        inputsLayout = QtWidgets.QVBoxLayout()

        # Function to create input field with unit dropdown
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

        # Creating input fields
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
        inputsLayout.addWidget(QtWidgets.QLabel("Capacitor Technology:"))
        inputsLayout.addWidget(self.capacitorTechDropdown)

        # Graph Type Dropdown
        self.graphTypeDropdown = QtWidgets.QComboBox()
        self.graphTypeDropdown.addItems(["Voltage/Cycles", "Arrhenius Plot (Leakage Current/Temp)", "Log/Log Plot (Capacitance/Resistance over Time)"])
        inputsLayout.addWidget(QtWidgets.QLabel("Graph Type:"))
        inputsLayout.addWidget(self.graphTypeDropdown)

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
        self.formulaWindow.setText("Choose a graph type to see the formula.")
        inputsLayout.addWidget(self.formulaWindow)

        mainLayout.addLayout(inputsLayout)

        # Plot Layout
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        mainLayout.addWidget(self.canvas)

        self.setLayout(mainLayout)

    def calculate(self):
        graph_type = self.graphTypeDropdown.currentText()
        if graph_type == "Voltage/Cycles":
            self.calculate_voltage_cycles()
        elif graph_type == "Arrhenius Plot (Leakage Current/Temp)":
            self.calculate_arrhenius_plot()
        elif graph_type == "Log/Log Plot (Capacitance/Resistance over Time)":
            self.calculate_log_log_plot()

    def calculate_voltage_cycles(self):
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

        # Generate the graph data
        voltages = np.linspace(0, V0, 100)
        cycles = [formula(v) for v in voltages]

        # Plotting the graph
        self.ax.clear()
        self.ax.plot(cycles, voltages)  # Cycles on x-axis, Voltage on y-axis
        self.ax.set_xlabel('Cycles')
        self.ax.set_ylabel('Voltage (V)')
        self.canvas.draw()

        # Update formula window with the formula and values
        formula_text = f"{tech} Formula:\nLx = {formula}\nL0 = {L0}, T0 = {T0}, Tx = {Tx}, V0 = {V0}, Vx = {Vx}"
        self.formulaWindow.setText(formula_text)

    def calculate_arrhenius_plot(self):
        # Example code for Arrhenius Plot
        temperatures = np.linspace(0, 100, 100)
        leakage_currents = np.exp(-1 / temperatures)  # Example Arrhenius equation
        self.ax.clear()
        self.ax.plot(temperatures, leakage_currents)
        self.ax.set_xlabel('Temperature (°C)')
        self.ax.set_ylabel('Leakage Current')
        self.canvas.draw()
        self.formulaWindow.setText("Arrhenius Plot of Leakage Current over Temperature.")

    def calculate_log_log_plot(self):
        # Example code for Log/Log Plot
        time_years = np.logspace(0, 3, 100)
        capacitance = np.log(time_years)  # Example relationship
        resistance = np.log(time_years)   # Example relationship
        self.ax.clear()
        self.ax.loglog(time_years, capacitance, label='Capacitance')
        self.ax.loglog(time_years, resistance, label='Resistance')
        self.ax.set_xlabel('Time (Years)')
        self.ax.set_ylabel('Value')
        self.ax.legend()
        self.canvas.draw()
        self.formulaWindow.setText("Log/Log Plot of Capacitance and Resistance over Time in Years.")
