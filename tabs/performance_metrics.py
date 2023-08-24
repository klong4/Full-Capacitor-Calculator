from PyQt5 import QtWidgets

class PerformanceMetricsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()

        # Efficiency Input
        self.efficiencyInput = QtWidgets.QLineEdit()
        layout.addWidget(QtWidgets.QLabel("Efficiency (%):"))
        layout.addWidget(self.efficiencyInput)

        # Power Density Input
        self.powerDensityInput = QtWidgets.QLineEdit()
        layout.addWidget(QtWidgets.QLabel("Power Density (W/L):"))
        layout.addWidget(self.powerDensityInput)

        # Energy Density Input
        self.energyDensityInput = QtWidgets.QLineEdit()
        layout.addWidget(QtWidgets.QLabel("Energy Density (Wh/L):"))
        layout.addWidget(self.energyDensityInput)

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
            efficiency = self.get_float_input(self.efficiencyInput)
            power_density = self.get_float_input(self.powerDensityInput)
            energy_density = self.get_float_input(self.energyDensityInput)

            # Perform specific calculations based on the given inputs
            # For example, you might calculate the overall performance score
            performance_score = (efficiency * power_density * energy_density) ** (1/3)

            self.resultsLabel.setText(f"Performance Score: {performance_score}")

        except ValueError as e:
            self.resultsLabel.setText(f"Error: {str(e)}")
        except Exception as e:
            self.resultsLabel.setText(f"An unexpected error occurred: {str(e)}")

    def get_float_input(self, input_field):
        text = input_field.text()
        if text == '':
            raise ValueError("Please fill in all required fields.")
        return float(text)
