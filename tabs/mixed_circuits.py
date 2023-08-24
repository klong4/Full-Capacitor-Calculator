from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from utils.units import (
    convert_capacitance,
    convert_voltage,
    convert_density
)
from utils.calculations import (
    calculate_total_capacitance_series,
    calculate_total_capacitance_parallel,
    calculate_energy_storage,
    calculate_energy_density
)

class MixedCircuitsTab(QtWidgets.QWidget):
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

        # Number of Capacitors in Series Input
        leftLayout.addWidget(QtWidgets.QLabel("Number of Capacitors in Series:"))
        self.numberOfCapacitorsSeriesInput = QtWidgets.QSpinBox()
        self.numberOfCapacitorsSeriesInput.setMinimum(1)
        self.numberOfCapacitorsSeriesInput.setValue(1)
        leftLayout.addWidget(self.numberOfCapacitorsSeriesInput)

        # Number of Capacitors in Parallel Input
        leftLayout.addWidget(QtWidgets.QLabel("Number of Capacitors in Parallel:"))
        self.numberOfCapacitorsParallelInput = QtWidgets.QSpinBox()
        self.numberOfCapacitorsParallelInput.setMinimum(1)
        self.numberOfCapacitorsParallelInput.setValue(1)
        leftLayout.addWidget(self.numberOfCapacitorsParallelInput)

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

            capacitance = convert_capacitance(float(self.capacitanceInput.text()), self.capacitanceUnitsComboBox.currentText(), "F")  # Extracting capacitance value
            num_capacitors_series = self.numberOfCapacitorsSeriesInput.value()
            num_capacitors_parallel = self.numberOfCapacitorsParallelInput.value()

            # Total Capacitance in Series
            total_capacitance_series = calculate_total_capacitance_series([capacitance] * num_capacitors_series)  # F

            # Total Capacitance in Parallel
            total_capacitance_parallel = calculate_total_capacitance_parallel([total_capacitance_series] * num_capacitors_parallel)  # F

            results = (
                f"Number of Capacitors in Series: {num_capacitors_series}\n"
                f"Number of Capacitors in Parallel: {num_capacitors_parallel}\n"
                f"Total Capacitance in Mixed Circuit (F): {total_capacitance_parallel}\n"
                # ... (rest of the results)
            )
            self.resultsTextEdit.setText(results)

            # Calculations
            calculations = (
                f"Total Capacitance in Series: {capacitance} F / {num_capacitors_series} = {total_capacitance_series} F\n"
                f"Total Capacitance in Parallel: {total_capacitance_series} F * {num_capacitors_parallel} = {total_capacitance_parallel} F\n"
                # ... (rest of the calculations)
            )
            self.calculationsTextEdit.setText(calculations)  # Set the calculations text

        except Exception as e:
            self.resultsTextEdit.setText(f"An unexpected error occurred: {str(e)}")