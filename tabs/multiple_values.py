from PyQt5 import QtWidgets
import numpy as np
from utils.calculations import calculate_energy_storage, calculate_charge

class MultipleValuesTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()

        # Capacitance Input Range
        self.capacitanceStartInput = QtWidgets.QLineEdit()
        self.capacitanceEndInput = QtWidgets.QLineEdit()
        self.capacitanceStepInput = QtWidgets.QLineEdit()
        layout.addWidget(QtWidgets.QLabel("Capacitance Range (F): Start, End, Step"))
        layout.addWidget(self.capacitanceStartInput)
        layout.addWidget(self.capacitanceEndInput)
        layout.addWidget(self.capacitanceStepInput)

        # Voltage Input Range
        self.voltageStartInput = QtWidgets.QLineEdit()
        self.voltageEndInput = QtWidgets.QLineEdit()
        self.voltageStepInput = QtWidgets.QLineEdit()
        layout.addWidget(QtWidgets.QLabel("Voltage Range (V): Start, End, Step"))
        layout.addWidget(self.voltageStartInput)
        layout.addWidget(self.voltageEndInput)
        layout.addWidget(self.voltageStepInput)

        # Calculate Button
        calculateButton = QtWidgets.QPushButton("Calculate")
        calculateButton.clicked.connect(self.calculate)
        layout.addWidget(calculateButton)

        # Results Display
        self.resultsLabel = QtWidgets.QLabel()
        layout.addWidget(self.resultsLabel)

        self.setLayout(layout)

    def calculate(self):
        try:
            capacitance_range = np.arange(
                self.get_float_input(self.capacitanceStartInput),
                self.get_float_input(self.capacitanceEndInput),
                self.get_float_input(self.capacitanceStepInput)
            )
            voltage_range = np.arange(
                self.get_float_input(self.voltageStartInput),
                self.get_float_input(self.voltageEndInput),
                self.get_float_input(self.voltageStepInput)
            )

            results = []
            for capacitance in capacitance_range:
                for voltage in voltage_range:
                    energy = calculate_energy_storage(capacitance, voltage) # Assuming the correct function name
                    charge = calculate_charge(capacitance, voltage)
                    results.append((capacitance, voltage, energy, charge))

            # Display results
            results_text = "\n".join([f"C: {c} F, V: {v} V, Energy: {e} J, Charge: {q} C" for c, v, e, q in results])
            self.resultsLabel.setText(results_text)

        except ValueError as e:
            self.resultsLabel.setText(f"Error: {str(e)}")
        except Exception as e:
            self.resultsLabel.setText(f"An unexpected error occurred: {str(e)}")

    def get_float_input(self, input_field):
        text = input_field.text()
        if text == '':
            raise ValueError("Please fill in all required fields.")
        return float(text)
