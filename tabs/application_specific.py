from PyQt5 import QtWidgets
from utils.calculations import (calculate_capacitance, calculate_energy_storage,
                                calculate_voltage, calculate_charge, calculate_esr)  # Add other functions as needed

class ApplicationSpecificTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        mainLayout = QtWidgets.QHBoxLayout()  # Main horizontal layout

        # Left side layout (for inputs and button)
        leftLayout = QtWidgets.QVBoxLayout()

        # Sizing for Backup Power
        self.backupPowerInput = QtWidgets.QLineEdit()
        leftLayout.addWidget(QtWidgets.QLabel("Backup Power Requirement (W):"))
        leftLayout.addWidget(self.backupPowerInput)

        # Integration with Batteries
        self.batteryCapacityInput = QtWidgets.QLineEdit()
        leftLayout.addWidget(QtWidgets.QLabel("Battery Capacity (Ah):"))
        leftLayout.addWidget(self.batteryCapacityInput)

        # Cost Analysis
        self.capacitorCostInput = QtWidgets.QLineEdit()
        leftLayout.addWidget(QtWidgets.QLabel("Capacitor Cost ($/F):"))
        leftLayout.addWidget(self.capacitorCostInput)
        self.totalCapacitanceInput = QtWidgets.QLineEdit()
        leftLayout.addWidget(QtWidgets.QLabel("Total Capacitance (F):"))
        leftLayout.addWidget(self.totalCapacitanceInput)

        # Calculate Button
        calculateButton = QtWidgets.QPushButton("Calculate")
        calculateButton.clicked.connect(self.calculate)
        leftLayout.addWidget(calculateButton)

        mainLayout.addLayout(leftLayout)

        # Right side layout (for results)
        self.resultsTextEdit = QtWidgets.QTextEdit()  # Text window for results
        mainLayout.addWidget(self.resultsTextEdit)

        self.setLayout(mainLayout)

    def calculate(self):
        try:
            # Sizing for Backup Power
            backup_power = self.get_float_input(self.backupPowerInput)
            backup_size = calculate_capacitance(backup_power, 0.5)  # Example calculation; adjust as needed

            # Integration with Batteries
            battery_capacity = self.get_float_input(self.batteryCapacityInput)
            integration_size = calculate_charge(battery_capacity, 0.8)  # Example calculation; adjust as needed

            # Cost Analysis
            capacitor_cost = self.get_float_input(self.capacitorCostInput)
            total_capacitance = self.get_float_input(self.totalCapacitanceInput)
            total_cost = capacitor_cost * total_capacitance

            results = (
                f"Sizing for Backup Power (F): {backup_size}\n"
                f"Integration with Batteries (F): {integration_size}\n"
                f"Total Cost ($): {total_cost}"
            )
            self.resultsTextEdit.setText(results)  # Set results in the text window

        except ValueError as e:
            self.resultsTextEdit.setText(f"Error: {str(e)}")
        except Exception as e:
            self.resultsTextEdit.setText(f"An unexpected error occurred: {str(e)}")

    def get_float_input(self, input_field):
        text = input_field.text()
        if text == '':
            raise ValueError("Please fill in all required fields.")
        return float(text)
