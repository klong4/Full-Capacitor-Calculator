import traceback
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from utils.units import (convert_capacitance, convert_voltage, convert_current, convert_resistance, convert_charge)
from utils.calculations import (calculate_capacitance, calculate_energy_storage,
                                calculate_voltage, calculate_charge, calculate_esr,
                                calculate_voltage_drop_esr, calculate_leakage_current)

class BasicParametersTab(QtWidgets.QWidget):
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

        # Charge/Capacitance Dropdown
        self.chargeDropdown = QtWidgets.QComboBox()
        self.chargeDropdown.addItems(["Coulombs", "Capacitance (F)", "Other Unit"])
        leftLayout.addWidget(QtWidgets.QLabel("Select Charge or Capacitance:"))
        leftLayout.addWidget(self.chargeDropdown)

        # Charge/Capacitance Input
        charge_layout, self.chargeInput, self.chargeUnitsComboBox = create_input_line("Value:", ["C", "F"], "Enter the value for the selected charge or capacitance unit.")
        leftLayout.addLayout(charge_layout)

        # Voltage Input
        voltage_layout, self.voltageInput, self.voltageUnitsComboBox = create_input_line("Voltage (V):", ["V", "mV", "kV"], "Potential difference across the capacitor (Volts).")
        leftLayout.addLayout(voltage_layout)

        # ESR Input
        esr_layout, self.esrInput, self.esrUnitsComboBox = create_input_line("Equivalent Series Resistance (Ohm):", ["Ohm", "mOhm", "uOhm", "kOhm"], "Internal resistance within the capacitor (Ohms).")
        leftLayout.addLayout(esr_layout)

        # Current Input
        current_layout, self.currentInput, self.currentUnitsComboBox = create_input_line("Current (A):", ["A", "mA"], "Flow of electric charge in the circuit (Amperes).")
        leftLayout.addLayout(current_layout)

        # Calculate Button
        calculateButton = QtWidgets.QPushButton("Calculate")
        calculateButton.clicked.connect(self.calculate)  # Connect to the calculate method
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

        # Default the charge to capacitance
        self.chargeDropdown.setCurrentIndex(1)
        self.update_charge_units()

        # Connect the charge dropdown signal to update the units
        self.chargeDropdown.currentIndexChanged.connect(self.update_charge_units)

    def update_charge_units(self):
        current_index = self.chargeDropdown.currentIndex()
        if current_index == 0:  # Coulombs
            self.chargeUnitsComboBox.clear()
            self.chargeUnitsComboBox.addItems(["C", "mC", "uC", "kC"])
        elif current_index == 1:  # Capacitance (F)
            self.chargeUnitsComboBox.clear()
            self.chargeUnitsComboBox.addItems(["F", "mF", "uF", "nF", "pF"])
        elif current_index == 2:  # Other Unit
            self.chargeUnitsComboBox.clear()
            self.chargeUnitsComboBox.addItems(["X", "Y", "Z"])

    def calculate(self):
        try:
        # Get the inputs
            charge_or_capacitance = float(self.chargeInput.text())
            voltage = float(self.voltageInput.text())
            esr = float(self.esrInput.text())
            current = float(self.currentInput.text())

            # Convert units if needed
            voltage = convert_voltage(voltage, self.voltageUnitsComboBox.currentText(), "V")
            esr = convert_resistance(esr, self.esrUnitsComboBox.currentText(), "Ohm")
            current = convert_current(current, self.currentUnitsComboBox.currentText(), "A")

            # Convert charge or capacitance based on the selected option
            if self.chargeDropdown.currentIndex() == 0:  # Coulombs
                charge = convert_charge(charge_or_capacitance, self.chargeUnitsComboBox.currentText(), "C")
                capacitance = calculate_capacitance(charge, voltage)
            elif self.chargeDropdown.currentIndex() == 1:  # Capacitance (F)
                capacitance = convert_capacitance(charge_or_capacitance, self.chargeUnitsComboBox.currentText(), "F")
                charge = capacitance * voltage  # Calculate charge from capacitance and voltage

            # Perform calculations
            energy_storage = calculate_energy_storage(capacitance, voltage)
            voltage_drop_esr = calculate_voltage_drop_esr(esr, current)
            leakage_current = calculate_leakage_current(capacitance, voltage, esr)
            # Add other calculations as needed

            # Set the results text
            results = (
                f"Capacitance (F): {'{:.6f}'.format(capacitance)}\n"
                f"Energy Storage (J): {'{:.6f}'.format(energy_storage)}\n"
                f"Voltage Drop (ESR) (V): {'{:.6f}'.format(voltage_drop_esr)}\n"
                f"Leakage Current (A): {'{:.6f}'.format(leakage_current)}\n"
                # Add other results as needed
            )
            self.resultsTextEdit.setText(results)

            # Set the calculations text (optional)
            calculations = (
                f"Capacitance = Charge / Voltage = {'{:.6f}'.format(charge)} / {'{:.6f}'.format(voltage)} = {'{:.6f}'.format(capacitance)} F\n"
                f"Energy Storage = 0.5 * Capacitance * Voltage^2 = 0.5 * {'{:.6f}'.format(capacitance)} * {'{:.6f}'.format(voltage)}^2 = {'{:.6f}'.format(energy_storage)} J\n"
                f"Voltage Drop (ESR) = ESR * Current = {'{:.6f}'.format(esr)} * {'{:.6f}'.format(current)} = {'{:.6f}'.format(voltage_drop_esr)} V\n"
                f"Leakage Current = (Capacitance * Voltage) / Resistance = ({'{:.6f}'.format(capacitance)} * {'{:.6f}'.format(voltage)}) / {'{:.6f}'.format(esr)} = {'{:.6f}'.format(leakage_current)} A\n"
                # Add other calculation details as needed
            )
            self.calculationsTextEdit.setText(calculations)

        except Exception as e:
            print(f"Debug: Exception: {str(e)}")  # Debugging print
            self.resultsTextEdit.setText(f"An unexpected error occurred: {str(e)}")
            traceback.print_exc()
