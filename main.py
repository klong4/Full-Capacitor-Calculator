# main.py
from PyQt5 import QtWidgets
from tabs.basic_parameters import BasicParametersTab
from tabs.charging_discharging import ChargingDischargingTab
from tabs.performance_metrics import PerformanceMetricsTab
from tabs.thermal_considerations import ThermalConsiderationsTab
from tabs.lifetime_reliability import LifetimeReliabilityTab
from tabs.application_specific import ApplicationSpecificTab
from tabs.advanced_modeling import AdvancedModelingTab
from tabs.series_circuits import SeriesCircuitsTab
from tabs.parallel_circuits import ParallelCircuitsTab
from tabs.mixed_circuits import MixedCircuitsTab
from tabs.multiple_values import MultipleValuesTab
from tabs.balancing_resistor import BalancingResistorTab
from tabs.cycle_life import CycleLifeTab
from tabs.life_cycles_dod import LifeCyclesDODTAB
from tabs.curve_fitting_module import CurveFittingApp  # Import the CurveFittingApp class


dark_theme = """
    QWidget {
        background-color: #333333;
        color: #E0E0E0;
    }
    QLineEdit, QSpinBox, QComboBox, QTextEdit {
        background-color: #454545;
        color: #E0E0E0;
        border: 1px solid #555555;
    }
    QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QTextEdit:focus {
        border: 1px solid #FF4500;
    }
    QLabel {
        color: #E0E0E0;
    }
    QPushButton {
        background-color: #555555;
        color: #E0E0E0;
        border: 1px solid #555555;
    }
    QPushButton:hover {
        background-color: #666666;
    }
    QPushButton:pressed {
        background-color: #FF4500;
        color: #E0E0E0;
    }
    QTabWidget::pane {
        border: 1px solid #444444;
    }
    QTabBar::tab {
        background: #555555;
    }
    QTabBar::tab:selected {
        background: #FF4500;
    }
"""

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Supercapacitor Calculator")
        
        # Create a tab widget
        self.tabs = QtWidgets.QTabWidget()
        
        # Add tabs for each section
        self.tabs.addTab(BasicParametersTab(), "Basic Parameters")
        self.tabs.addTab(ChargingDischargingTab(), "Charging/Discharging")
        self.tabs.addTab(CycleLifeTab(), "Cycle Life")
        self.tabs.addTab(LifeCyclesDODTAB(), "Depth Of Discharge Life Cycles")
        self.tabs.addTab(CurveFittingApp(), "CurveFittingApp")
        #self.tabs.addTab(SeriesCircuitsTab(), "Series Circuits")
        #self.tabs.addTab(ParallelCircuitsTab(), "Parallel Circuits")
        #self.tabs.addTab(MixedCircuitsTab(), "Mixed Circuits")
        #self.tabs.addTab(BalancingResistorTab(), "Passive Balancing")
        #self.tabs.addTab(PerformanceMetricsTab(), "Performance Metrics")
        #self.tabs.addTab(ThermalConsiderationsTab(), "Thermal Considerations")
        #self.tabs.addTab(LifetimeReliabilityTab(), "Lifetime & Reliability")
        #self.tabs.addTab(ApplicationSpecificTab(), "Application-Specific")
        #self.tabs.addTab(AdvancedModelingTab(), "Advanced Modeling")
        #self.tabs.addTab(MultipleValuesTab(), "Multiple Values")
        
        # Set the tab widget as the central widget
        self.setCentralWidget(self.tabs)
        
        # Show the window
        self.show()

# Run the application
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyleSheet(dark_theme)  # Apply the dark theme
    window = MainWindow()
    app.exec_()
