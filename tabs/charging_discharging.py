from PyQt5 import QtWidgets, QtCore
import math
from utils.calculations import calculate_energy_charge_discharge, calculate_charge

class ChargingDischargingTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        mainLayout = QtWidgets.QVBoxLayout()
        inputLayout = QtWidgets.QHBoxLayout()
        leftLayout = QtWidgets.QVBoxLayout()

        # Function to create input field with dropdown
        def create_input_field(label_text, tooltip_text, dropdown_items):
            label = QtWidgets.QLabel(label_text)
            input_field = QtWidgets.QLineEdit()
            input_field.setToolTip(tooltip_text)
            dropdown = QtWidgets.QComboBox()
            dropdown.addItems(dropdown_items)
            h_layout = QtWidgets.QHBoxLayout()
            h_layout.addWidget(input_field)
            h_layout.addWidget(dropdown)
            v_layout = QtWidgets.QVBoxLayout()
            v_layout.addWidget(label)
            v_layout.addLayout(h_layout)
            return v_layout, input_field, dropdown

        # Capacitance
        layout, self.capacitanceInput, self.capacitanceUnitDropdown = create_input_field(
            "Capacitance:", "Capacitance is the ability of a capacitor to store charge. Measured in Farads (F).", ['F', 'mF', 'uF', 'nF', 'pF'])
        leftLayout.addLayout(layout)

        # Initial Voltage
        layout, self.initialVoltageInput, self.initialVoltageUnitDropdown = create_input_field(
            "Initial Voltage (V0):", "Initial voltage across the capacitor before charging or discharging. Measured in Volts (V).", ['V', 'mV', 'uV'])
        leftLayout.addLayout(layout)

        # Final Voltage
        layout, self.finalVoltageInput, self.finalVoltageUnitDropdown = create_input_field(
            "Final Voltage (V1):", "Final voltage across the capacitor after charging or discharging. Measured in Volts (V).", ['V', 'mV', 'uV'])
        leftLayout.addLayout(layout)

        # Resistance (Optional)
        layout, self.resistanceInput, self.resistanceUnitDropdown = create_input_field(
            "Resistance (Optional):", "Resistance in the circuit. Used to calculate time when current or power is not provided. Measured in Ohms (Ω).", ['Ω', 'kΩ', 'MΩ'])
        leftLayout.addLayout(layout)

        # Current or Power
        layout, self.currentOrPowerInput, self.currentOrPowerUnitDropdown = create_input_field(
            "Charge/Discharge Amperage/Power (Optional):", "Current or power used for charging/discharging. Measured in Amperes (A) or Watts (W).", ['A', 'mA', 'uA'])
        self.currentOrPowerDropdown = QtWidgets.QComboBox()
        self.currentOrPowerDropdown.addItems(['Amperage', 'Power'])
        self.currentOrPowerDropdown.currentIndexChanged.connect(self.update_current_or_power_units)
        layout.itemAt(1).insertWidget(1, self.currentOrPowerDropdown)
        leftLayout.addLayout(layout)

        calculateButton = QtWidgets.QPushButton("Calculate")
        calculateButton.clicked.connect(self.calculate)
        leftLayout.addWidget(calculateButton)

        inputLayout.addLayout(leftLayout)

        self.resultsTextEdit = QtWidgets.QTextEdit()
        self.resultsTextEdit.setAlignment(QtCore.Qt.AlignTop)  # Align text to the top
        inputLayout.addWidget(self.resultsTextEdit)

        mainLayout.addLayout(inputLayout)

        # Formulas Window
        self.formulasTextEdit = QtWidgets.QTextEdit()
        self.formulasTextEdit.setAlignment(QtCore.Qt.AlignTop)  # Align text to the top
        formulas = (
            "Time (with current or power): (Capacitance * (Initial Voltage - Final Voltage)) / Amperage\n"
            "Time (with resistance): -tau * log(1 - Final Voltage / Initial Voltage), where tau = Resistance * Capacitance\n"
            "Energy: 0.5 * Capacitance * (Initial Voltage^2 - Final Voltage^2)\n"
            "Charge: Energy / Initial Voltage\n"
        )
        self.formulasTextEdit.setText(formulas)
        mainLayout.addWidget(self.formulasTextEdit)

        self.setLayout(mainLayout)

    def update_current_or_power_units(self):
        if self.currentOrPowerDropdown.currentText() == 'Amperage':
            self.currentOrPowerUnitDropdown.clear()
            self.currentOrPowerUnitDropdown.addItems(['A', 'mA', 'uA'])
        else:  # Power
            self.currentOrPowerUnitDropdown.clear()
            self.currentOrPowerUnitDropdown.addItems(['W', 'mW'])

    def get_float_input(self, input_field, unit_dropdown, optional=False):
        text = input_field.text()
        if text == '' and optional:
            return None
        elif text == '' and not optional:
            raise ValueError("Please fill in all required fields.")
        value = float(text)
        unit = unit_dropdown.currentText()
        conversion_factors = {'mF': 1e-3, 'uF': 1e-6, 'nF': 1e-9, 'pF': 1e-12,
                            'mV': 1e-3, 'uV': 1e-6,
                            'mA': 1e-3, 'uA': 1e-6,
                            'W': 1, 'mW': 1e-3,
                            'Ω': 1, 'kΩ': 1e3, 'MΩ': 1e6}
        return value * conversion_factors.get(unit, 1)
    
    def calculate(self):
        try:
            capacitance = self.get_float_input(self.capacitanceInput, self.capacitanceUnitDropdown)
            initialVoltage = self.get_float_input(self.initialVoltageInput, self.initialVoltageUnitDropdown)
            finalVoltage = self.get_float_input(self.finalVoltageInput, self.finalVoltageUnitDropdown)
            resistance = self.get_float_input(self.resistanceInput, self.resistanceUnitDropdown, optional=True)
            current_or_power = self.get_float_input(self.currentOrPowerInput, self.currentOrPowerUnitDropdown, optional=True)
            current_or_power_type = self.currentOrPowerDropdown.currentText()

            amperage = None
            tau = None
            if current_or_power is not None:
                if current_or_power_type == 'Amperage':
                    amperage = current_or_power
                else:  # Power
                    amperage = current_or_power / initialVoltage

                time = (capacitance * (initialVoltage - finalVoltage)) / amperage
            else:
                if resistance is None:
                    raise ValueError("Please provide either resistance or current/power for calculation.")
                tau = resistance * capacitance
                time = -tau * math.log(1 - finalVoltage / initialVoltage)

            # Convert time to different units
            time_minutes = time / 60
            time_hours = time_minutes / 60
            time_days = time_hours / 24

            # Energy in joules
            energy_joules = calculate_energy_charge_discharge(capacitance, initialVoltage, finalVoltage)

            # Charge in Ah and mAh
            charge_ah = calculate_charge(energy_joules, initialVoltage)
            charge_mah = charge_ah * 1000

            # Energy in Wh
            energy_wh = energy_joules / 3600

            results = (
                f"Time: {time:.4f} seconds, {time_minutes:.4f} minutes, {time_hours:.4f} hours, {time_days:.4f} days\n"
                f"Energy: {energy_joules:.4f} Joules, {energy_wh:.4f} Wh\n"
                f"Charge: {charge_ah:.4f} Ah, {charge_mah:.4f} mAh"
            )
            self.resultsTextEdit.setText(results)

            # Formulas with values
            formulas_with_values = (
                (f"Time (with current or power): ({capacitance} * ({initialVoltage} - {finalVoltage})) / {amperage} = {time:.4f} seconds\n" if amperage else "") +
                (f"Time (with resistance): -{tau} * log(1 - {finalVoltage} / {initialVoltage}) = {time:.4f} seconds\n" if tau else "") +
                f"Energy: 0.5 * {capacitance} * ({initialVoltage}^2 - {finalVoltage}^2) = {energy_joules:.4f} Joules\n"
                f"Charge: {energy_joules} / {initialVoltage} = {charge_ah:.4f} Ah\n"
            )
            self.formulasTextEdit.setText(formulas_with_values)

        except ValueError as e:
            self.resultsTextEdit.setText(f"Error: {str(e)}")
        except Exception as e:
            self.resultsTextEdit.setText(f"An unexpected error occurred: {str(e)}")
