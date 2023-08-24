from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class LifetimeReliabilityTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        mainLayout = QtWidgets.QHBoxLayout()  # Main horizontal layout

        # Left side layout (for inputs and button)
        leftLayout = QtWidgets.QVBoxLayout()

        # Cycle Life Input
        self.cycleLifeInput = QtWidgets.QLineEdit()
        self.cycleLifeInput.setToolTip("Number of cycles the capacitor can perform before failure.")
        leftLayout.addWidget(QtWidgets.QLabel("Cycle Life (cycles):"))
        leftLayout.addWidget(self.cycleLifeInput)

        # Operating Temperature Input
        self.temperatureInput = QtWidgets.QLineEdit()
        self.temperatureInput.setToolTip("Operating temperature of the capacitor in degrees Celsius.")
        leftLayout.addWidget(QtWidgets.QLabel("Operating Temperature (°C):"))
        leftLayout.addWidget(self.temperatureInput)

        # Stress Factors Inputs
        self.stressFactorsInputs = []
        self.stressFactorsUnits = []
        stressFactorsLayout = QtWidgets.QVBoxLayout()
        for factor, tooltip in [("Voltage", "Voltage stress factor in Volts."),
                               ("Current", "Current stress factor in Amps."),
                               ("Power", "Power stress factor in Watts.")]:
            factorLayout = QtWidgets.QHBoxLayout()
            factorInput = QtWidgets.QLineEdit()
            factorInput.setToolTip(tooltip)
            factorUnit = QtWidgets.QComboBox()
            factorUnit.addItems(["Volts", "Amps", "Watts"] if factor != "Power" else ["Watts"])
            factorLayout.addWidget(QtWidgets.QLabel(f"{factor} Stress Factor:"))
            factorLayout.addWidget(factorInput)
            factorLayout.addWidget(factorUnit)
            stressFactorsLayout.addLayout(factorLayout)
            self.stressFactorsInputs.append(factorInput)
            self.stressFactorsUnits.append(factorUnit)

        leftLayout.addLayout(stressFactorsLayout)

        # Calculate Button
        calculateButton = QtWidgets.QPushButton("Calculate Reliability")
        calculateButton.clicked.connect(self.calculate_reliability)
        leftLayout.addWidget(calculateButton)

        # Results Display
        self.resultsLabel = QtWidgets.QLabel()
        leftLayout.addWidget(self.resultsLabel)

        mainLayout.addLayout(leftLayout)

        # Right side layout (for plot)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        mainLayout.addWidget(self.canvas)

        # X and Y Axis Dropdowns
        self.xAxisDropdown = QtWidgets.QComboBox()
        self.xAxisDropdown.addItems(["Cycle Life", "Temperature", "Stress Factors"])  # Add options as needed
        self.yAxisDropdown = QtWidgets.QComboBox()
        self.yAxisDropdown.addItems(["Failure Rate", "Reliability"])  # Add options as needed
        leftLayout.addWidget(QtWidgets.QLabel("X Axis:"))
        leftLayout.addWidget(self.xAxisDropdown)
        leftLayout.addWidget(QtWidgets.QLabel("Y Axis:"))
        leftLayout.addWidget(self.yAxisDropdown)

        self.setLayout(mainLayout)

    def calculate_reliability(self):
        try:
            cycle_life = float(self.cycleLifeInput.text())
            temperature = float(self.temperatureInput.text())
            stress_factors = [float(input_field.text()) for input_field in self.stressFactorsInputs]

            # Example calculation for reliability based on Arrhenius equation
            activation_energy = 0.7  # Example value, in eV
            k_boltzmann = 8.617e-5    # Boltzmann constant, in eV/K
            reference_temp = 298     # Reference temperature, in K

            failure_rates = [stress_factor * (cycle_life ** -0.5) *
                            (2 ** ((activation_energy / k_boltzmann) * (1 / reference_temp - 1 / (temperature + 273))))
                            for stress_factor in stress_factors]

            # Plotting the connected dot chart
            self.ax.plot(stress_factors, failure_rates, marker='o')
            self.ax.set_xlabel(self.xAxisDropdown.currentText())
            self.ax.set_ylabel(self.yAxisDropdown.currentText())
            self.canvas.draw()

            self.resultsLabel.setText(f"Predicted Failure Rates: {failure_rates}")

        except ValueError:
            self.resultsLabel.setText("Please fill in all required fields.")
        except Exception as e:
            self.resultsLabel.setText(f"An unexpected error occurred: {str(e)}")