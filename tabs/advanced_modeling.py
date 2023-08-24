from PyQt5 import QtWidgets
import numpy as np
from utils.calculations import calculate_total_capacitance, calculate_specific_capacitance, calculate_effective_surface_area

class AdvancedModelingTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        mainLayout = QtWidgets.QHBoxLayout()  # Main horizontal layout

        # Left side layout (for inputs and button)
        leftLayout = QtWidgets.QVBoxLayout()

        # Electrochemical Modeling
        leftLayout.addWidget(QtWidgets.QLabel("Electrochemical Modeling:"))

        # Double Layer Capacitance Input
        self.doubleLayerCapacitanceInput = QtWidgets.QLineEdit()
        leftLayout.addWidget(QtWidgets.QLabel("Double Layer Capacitance (F):"))
        leftLayout.addWidget(self.doubleLayerCapacitanceInput)

        # Pseudocapacitance Input
        self.pseudocapacitanceInput = QtWidgets.QLineEdit()
        leftLayout.addWidget(QtWidgets.QLabel("Pseudocapacitance (F):"))
        leftLayout.addWidget(self.pseudocapacitanceInput)

        # Material Properties
        leftLayout.addWidget(QtWidgets.QLabel("Material Properties:"))

        # Surface Area Input
        self.surfaceAreaInput = QtWidgets.QLineEdit()
        leftLayout.addWidget(QtWidgets.QLabel("Surface Area (m^2):"))
        leftLayout.addWidget(self.surfaceAreaInput)

        # Porosity Input
        self.porosityInput = QtWidgets.QLineEdit()
        leftLayout.addWidget(QtWidgets.QLabel("Porosity:"))
        leftLayout.addWidget(self.porosityInput)

        # Simulation and Optimization
        leftLayout.addWidget(QtWidgets.QLabel("Simulation and Optimization:"))

        # Optimization Target Dropdown
        self.optimizationTargetDropdown = QtWidgets.QComboBox()
        self.optimizationTargetDropdown.addItems(['Energy Density', 'Power Density', 'Lifetime'])
        leftLayout.addWidget(QtWidgets.QLabel("Optimization Target:"))
        leftLayout.addWidget(self.optimizationTargetDropdown)

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
            double_layer_capacitance = self.get_float_input(self.doubleLayerCapacitanceInput)
            pseudocapacitance = self.get_float_input(self.pseudocapacitanceInput)
            surface_area = self.get_float_input(self.surfaceAreaInput)
            porosity = self.get_float_input(self.porosityInput)

            total_capacitance = calculate_total_capacitance(double_layer_capacitance, pseudocapacitance)
            specific_capacitance = calculate_specific_capacitance(total_capacitance, surface_area)
            effective_surface_area = calculate_effective_surface_area(surface_area, porosity)

            results = (
                f"Total Capacitance (F): {total_capacitance}\n"
                f"Specific Capacitance (F/m^2): {specific_capacitance}\n"
                f"Effective Surface Area (m^2): {effective_surface_area}\n"
            )
            self.resultsTextEdit.setText(results)

        except ValueError as e:
            self.resultsTextEdit.setText(f"Error: {str(e)}")
        except Exception as e:
            self.resultsTextEdit.setText(f"An unexpected error occurred: {str(e)}")

    def get_float_input(self, input_field):
        text = input_field.text()
        if text == '':
            raise ValueError("Please fill in all required fields.")
        return float(text)
