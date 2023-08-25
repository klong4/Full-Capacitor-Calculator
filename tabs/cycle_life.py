from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QProgressBar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np

class CycleLifeTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        mainLayout = QtWidgets.QHBoxLayout()  # Main Horizontal layout

        # Inputs and Button Layout
        inputsLayout = QtWidgets.QVBoxLayout()
        inputsWidget = QtWidgets.QWidget()  # Create a widget to contain the layout
        inputsWidget.setLayout(inputsLayout)  # Set the layout to the widget
        inputsWidget.setFixedWidth(325)  # Set fixed width for the widget containing input fields
        mainLayout.addWidget(inputsWidget)  # Add the widget to the main layout

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
        layout, self.IInput, _ = create_input_field("Discharge Current (I):", "Discharge Current (I): The current at which the capacitor is discharged.", ["A"])
        inputsLayout.addLayout(layout)

        # Capacitor Technology Dropdown
        self.capacitorTechDropdown = QtWidgets.QComboBox()
        self.capacitorTechDropdown.addItems(["EDLC 3V", "EDLC 2.7V", "LiC 20-85 celsius", "LiC 20-70 celsius", "LCC"])
        self.capacitorTechDropdown.currentIndexChanged.connect(self.update_formula_window)
        inputsLayout.addWidget(QtWidgets.QLabel("Capacitor Technology:"))
        inputsLayout.addWidget(self.capacitorTechDropdown)

        # Graph Type Dropdown
        self.graphTypeDropdown = QtWidgets.QComboBox()
        #self.graphTypeDropdown.addItems(["Voltage/Cycles", "Arrhenius Plot (Leakage Current/Temp)", "Log/Log Plot (Capacitance/Resistance over Time)"])
        self.graphTypeDropdown.addItems(["Voltage/Cycles", "Log/Log Plot (Capacitance/Resistance over Time)"])
        inputsLayout.addWidget(QtWidgets.QLabel("Graph Type:"))
        inputsLayout.addWidget(self.graphTypeDropdown)

        # Calculate Button
        calculateButton = QtWidgets.QPushButton("Calculate")
        calculateButton.clicked.connect(self.calculate)
        inputsLayout.addWidget(calculateButton)
        
        # Add Progress Bar
        self.progressBar = QProgressBar(self)
        inputsLayout.addWidget(self.progressBar)

        # Results Display
        self.resultsLabel = QtWidgets.QLabel()
        inputsLayout.addWidget(self.resultsLabel)

        # Formula Display
        self.formulaWindow = QtWidgets.QTextEdit()
        self.formulaWindow.setReadOnly(True)
        self.formulaWindow.setFixedWidth(300)  # Set fixed width for formula window
        self.formulaWindow.setText("Choose a graph type and click Calculate to see the formula.")
        inputsLayout.addWidget(self.formulaWindow)

        mainLayout.addLayout(inputsLayout)

        # Plot Layout
        plotLayout = QtWidgets.QVBoxLayout()  # Plot vertical layout
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.figure.tight_layout()  # Set tight layout by default

        # Adding Custom Navigation Toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        plotLayout.addWidget(self.toolbar)  # Add toolbar first
        plotLayout.addWidget(self.canvas)   # Then add canvas

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

    def reset_graph(self):
        self.ax.clear()
        self.canvas.draw()

    def calculate(self):
        graph_type = self.graphTypeDropdown.currentText()
        self.figure.clf()
        self.ax = self.figure.add_subplot(1, 1, 1)
        
        if graph_type == "Voltage/Cycles":
            self.calculate_voltage_cycles()
        elif graph_type == "Arrhenius Plot (Leakage Current/Temp)":
            self.calculate_arrhenius_plot()
        elif graph_type == "Log/Log Plot (Capacitance/Resistance over Time)":
            self.calculate_log_log_plot()
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

    def calculate_arrhenius_plot(self):
        # Example code for Arrhenius Plot (using a simple exponential decay model)
        temperatures = np.linspace(0, 100, 100)
        # Assuming a base leakage current and an activation energy
        base_leakage_current = 1e-6
        activation_energy = 0.5
        k_boltzmann = 8.617e-5  # Boltzmann constant, in eV/K
        leakage_currents = base_leakage_current * np.exp(-activation_energy / (k_boltzmann * (temperatures + 273)))
        self.ax.clear()
        self.ax.plot(temperatures, leakage_currents)
        self.ax.set_xlabel('Temperature (°C)')
        self.ax.set_ylabel('Leakage Current (A)')
        self.ax.ticklabel_format(style='plain', axis='both')  # Avoid scientific notation
        self.ax.set_xticklabels(self.ax.get_xticks(), rotation=90)  # Vertical x-axis labels
        self.canvas.draw()
        self.formulaWindow.setText("Arrhenius Plot of Leakage Current over Temperature.")
        self.ax.set_xticklabels(self.ax.get_xticks(), rotation=90)  # Rotate x-axis labels
        
    def calculate_log_log_plot(self):    
        I = float(self.IInput.text())  # Replace this with the actual input field
    
        # Calculate V1 and V2 based on V0
        V1 = 0.8 * float(self.V0Input.text())
        V2 = 0.4 * float(self.V0Input.text())
    
        # Assuming T1 and T2 are available (replace these with actual values)
        T1 = float(self.L0Input.text())  # Starting time of test
        T2 = float(self.T2Input.text())  # Assuming you have an input field for T2
    
        # Calculate capacitance using the formula
        C = I * ((T2 - T1) / (V1 - V2))
    
        # Generate the log-log plot data
        time_months = np.logspace(0, 12, 100)  # Time in months
        capacity = C * np.ones_like(time_months)  # Assuming constant capacitance
        resistance = 1 + 0.01 * time_months  # Example resistance formula
    
        # Plotting the graph
        self.ax.clear()
        self.ax.loglog(time_months, capacity, label='Capacitance (F)')
        self.ax.set_xlabel('Time (Months)')
        self.ax.set_ylabel('Capacitance (F)')
    
        ax2 = self.ax.twinx()  # Create a second y-axis
        ax2.loglog(time_months, resistance, label='Resistance (Ohms)', color='orange')
        ax2.set_ylabel('Resistance (Ohms)')
    
        # Custom formatting for tick labels
        self.ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0f}'.format(x)))
        self.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0f}'.format(x)))
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0f}'.format(x)))
    
        self.ax.legend(loc='upper left')
        ax2.legend(loc='upper right')
    
        self.canvas.draw()
    
        # Update the formula window
        self.formulaWindow.setText(f"Capacitance (C) = {C} Farads")
    
        # Update the progress bar
        num_steps = len(time_months)
        for i in range(num_steps):
            self.progressBar.setValue((i + 1) * 100 // num_steps)
            QtWidgets.QApplication.processEvents()
    
        self.progressBar.setValue(0)
