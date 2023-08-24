from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from utils.units import (
    convert_capacitance,
    convert_voltage,
    convert_density
)
from utils.calculations import (
    calculate_total_capacitance_series,
    calculate_energy_storage,
    calculate_energy_density
)

class SeriesCircuitsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        mainLayout = QtWidgets.QHBoxLayout()

        # Left side layout (for inputs and button)
        leftLayout = QtWidgets.QVBoxLayout()
        leftLayout.setAlignment(Qt.AlignTop)  # Align to the top

        # Function to create input line with label, input field, and unit dropdown
        def create_input_line(label_text, units, tooltip):
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(QtWidgets.QLabel(label_text))
            input_line = QtWidgets.QHBoxLayout()
            input_field = QtWidgets.QLineEdit()
            input_field.setToolTip(tooltip)  # Adding tooltip
            input_line.addWidget(input_field)
            units_combo_box = QtWidgets.QComboBox()
            units_combo_box.addItems(units)
            input_line.addWidget(units_combo_box)
            layout.addLayout(input_line)
            return layout, input_field, units_combo_box

        # Number of Capacitors Input
        leftLayout.addWidget(QtWidgets.QLabel("Number of Capacitors in Series:"))
        self.numberOfCapacitorsInput = QtWidgets.QSpinBox()
        self.numberOfCapacitorsInput.setMinimum(2)
        self.numberOfCapacitorsInput.setValue(2)
        leftLayout.addWidget(self.numberOfCapacitorsInput)

        # Capacitance Input
        capacitance_layout, self.capacitanceInput, self.capacitanceUnitsComboBox = create_input_line("Capacitance:", ["F", "mF", "uF", "nF", "pF"], "Enter the capacitance value")
        leftLayout.addLayout(capacitance_layout)

        # Nominal Voltage Input
        voltage_layout, self.nominalVoltageInput, self.nominalVoltageUnitsComboBox = create_input_line("Nominal Voltage:", ["V", "mV", "kV"], "Enter the nominal voltage value")
        leftLayout.addLayout(voltage_layout)

        # Mass Input
        mass_layout, self.massInput, self.massUnitsComboBox = create_input_line("Mass:", ["kg", "g", "mg"], "Enter the mass value")
        leftLayout.addLayout(mass_layout)

        # Volume Input
        volume_layout, self.volumeInput, self.volumeUnitsComboBox = create_input_line("Volume:", ["l", "ml", "cl"], "Enter the volume value")
        leftLayout.addLayout(volume_layout)

        # Energy Density Input
        energy_density_layout, self.energyDensityInput, self.energyDensityUnitsComboBox = create_input_line("Energy Density:", ["Wh/kg", "mWh/kg"], "Enter the energy density value")
        leftLayout.addLayout(energy_density_layout)

        # Calculate Button
        calculateButton = QtWidgets.QPushButton("Calculate")
        calculateButton.clicked.connect(self.calculate)
        leftLayout.addWidget(calculateButton)

        mainLayout.addLayout(leftLayout)

        # Right side layout (for results and calculations)
        rightLayout = QtWidgets.QVBoxLayout()

        # Results Text Edit
        self.resultsTextEdit = QtWidgets.QTextEdit()
        self.resultsTextEdit.setFixedHeight(200)  # Set the fixed height for the results window
        rightLayout.addWidget(self.resultsTextEdit)

        # Calculations Text Edit
        self.calculationsTextEdit = QtWidgets.QTextEdit()
        rightLayout.addWidget(self.calculationsTextEdit)  # Add the calculations window below the results

        mainLayout.addLayout(rightLayout)
        self.setLayout(mainLayout)

    def calculate(self):
        try:
            # Check for empty fields
            if not all([self.capacitanceInput.text(),
                        self.nominalVoltageInput.text(),
                        self.massInput.text(),
                        self.volumeInput.text(),
                        self.energyDensityInput.text()]):
                raise ValueError("All fields must be filled in.")
            num_capacitors = self.numberOfCapacitorsInput.value()
            capacitance = convert_capacitance(float(self.capacitanceInput.text()), self.capacitanceUnitsComboBox.currentText(), "F")
            nominal_voltage = convert_voltage(float(self.nominalVoltageInput.text()), self.nominalVoltageUnitsComboBox.currentText(), "V")
            mass = float(self.massInput.text())  # Assuming mass is in the desired unit
            volume = float(self.volumeInput.text())  # Assuming volume is in the desired unit
            energy_density_input = convert_density(float(self.energyDensityInput.text()), self.energyDensityUnitsComboBox.currentText(), "Wh/kg")

            # Total Capacitance in Series
            total_capacitance = calculate_total_capacitance_series([capacitance] * num_capacitors)  # F

            # Total Energy in Series
            total_energy_joules = calculate_energy_storage(total_capacitance, nominal_voltage)  # J

            # Energy Density (if not provided)
            if energy_density_input == 0:
                energy_density_input = calculate_energy_density(total_energy_joules, mass)  # Wh/kg

            # Total Voltage in Series
            total_voltage = nominal_voltage * num_capacitors

            # ASCII drawing of the circuit
            circuit_drawing = "----" + "||----" * (num_capacitors - 1) + "||----"

            results = (
                f"Number of Capacitors in Series: {num_capacitors}\n"
                f"Total Capacitance in Series (F): {total_capacitance}\n"
                f"Total Energy in Series (J): {total_energy_joules}\n"
                f"Energy Density (Wh/kg): {energy_density_input}\n"
                f"Total Voltage in Series (V): {total_voltage}\n" 
                f"Circuit Diagram:\n{circuit_drawing}"
            )
            self.resultsTextEdit.setText(results)

            # Calculations
            calculations = (
                f"Total Capacitance in Series: {capacitance} F / {num_capacitors} = {total_capacitance} F\n"
                f"Total Energy in Series: 0.5 * {total_capacitance} F * ({nominal_voltage} V)^2 = {total_energy_joules} J\n"
                f"Total Voltage in Series: {nominal_voltage} V * {num_capacitors} = {total_voltage} V"
            )
            self.calculationsTextEdit.setText(calculations)  # Set the calculations text

        except Exception as e:
            self.resultsTextEdit.setText(f"An unexpected error occurred: {str(e)}")
