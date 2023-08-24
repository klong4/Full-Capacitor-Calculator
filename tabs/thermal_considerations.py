from PyQt5 import QtWidgets

class ThermalConsiderationsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()

        # Heat Generation Input
        self.currentInput = QtWidgets.QLineEdit()
        layout.addWidget(QtWidgets.QLabel("Current (A):"))
        layout.addWidget(self.currentInput)

        self.resistanceInput = QtWidgets.QLineEdit()
        layout.addWidget(QtWidgets.QLabel("Resistance (Ω):"))
        layout.addWidget(self.resistanceInput)

        # Thermal Management Input
        self.ambientTemperatureInput = QtWidgets.QLineEdit()
        layout.addWidget(QtWidgets.QLabel("Ambient Temperature (°C):"))
        layout.addWidget(self.ambientTemperatureInput)

        self.thermalResistanceInput = QtWidgets.QLineEdit()
        layout.addWidget(QtWidgets.QLabel("Thermal Resistance (°C/W):"))
        layout.addWidget(self.thermalResistanceInput)

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
            current = self.get_float_input(self.currentInput)
            resistance = self.get_float_input(self.resistanceInput)
            ambient_temperature = self.get_float_input(self.ambientTemperatureInput)
            thermal_resistance = self.get_float_input(self.thermalResistanceInput)

            # Heat Generation Calculation
            heat_generation = current ** 2 * resistance

            # Thermal Management Calculation
            temperature_rise = heat_generation * thermal_resistance
            final_temperature = ambient_temperature + temperature_rise

            self.resultsLabel.setText(f"Heat Generation (W): {heat_generation}\nFinal Temperature (°C): {final_temperature}")

        except ValueError as e:
            self.resultsLabel.setText(f"Error: {str(e)}")
        except Exception as e:
            self.resultsLabel.setText(f"An unexpected error occurred: {str(e)}")

    def get_float_input(self, input_field):
        text = input_field.text()
        if text == '':
            raise ValueError("Please fill in all required fields.")
        return float(text)
