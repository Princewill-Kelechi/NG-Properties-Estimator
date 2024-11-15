#  Python Desktop Software built with Pyside6 by Princewill Kelechi Blessing 

#  IN PARTIAL FULFILMENT OF THE REQUIREMENT FOR THE AWARD OF A BACHELOR’S DEGREE IN ENGINEERING. (B.ENG.)
#  PETROLEUM ENGINEERING.

#  Date : October 30 2024


import sys
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QLineEdit, QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from scipy.optimize import fsolve

# This is the gas constant
R = 8.314  # J/(mol·K), 

# These is a Python dictionary that holds the vander waals constant (in SI units) and molar masses for each gas
#These way, when users select gas components, we can look up the needed values of the components here

VDW_CONSTANTS = {
    "Methane (CH4)": {"a": 2.283e5 / 1e6, "b": 0.04278e-3, "MolarMass": 16.04},
    "Ethane (C2H6)": {"a": 5.507e5 / 1e6, "b": 0.0638e-3, "MolarMass": 30.07},
    "Propane (C3H8)": {"a": 8.64e5 / 1e6, "b": 0.0857e-3, "MolarMass": 44.1},
    "Butane (C4H10)": {"a": 1.374e6 / 1e6, "b": 0.118e-3, "MolarMass": 58.12},
    "Pentane (C5H12)": {"a": 1.858e6 / 1e6, "b": 0.146e-3, "MolarMass": 72.15},
    "Hexane (C6H14)": {"a": 2.631e6 / 1e6, "b": 0.173e-3, "MolarMass": 86.18},
    "Heptane (C7H16)": {"a": 3.611e6 / 1e6, "b": 0.200e-3, "MolarMass": 100.2},
    "Octane (C8H18)": {"a": 4.876e6 / 1e6, "b": 0.233e-3, "MolarMass": 114.23},
    "Nonane (C9H20)": {"a": 6.395e6 / 1e6, "b": 0.259e-3, "MolarMass": 128.26},
    "Decane (C10H22)": {"a": 8.299e6 / 1e6, "b": 0.286e-3, "MolarMass": 142.29},
    "Carbon Dioxide (CO2)": {"a": 3.59e5 / 1e6, "b": 0.04267e-3, "MolarMass": 44.01},
    "Nitrogen (N2)": {"a": 1.390e5 / 1e6, "b": 0.03913e-3, "MolarMass": 28.02},
    "Oxygen (O2)": {"a": 1.382e5 / 1e6, "b": 0.03186e-3, "MolarMass": 32.00},
    "Hydrogen (H2)": {"a": 2.476e-1 / 1e6, "b": 0.02661e-3, "MolarMass": 2.016},
    "Hydrogen Sulfide (H2S)": {"a": 4.484e5 / 1e6, "b": 0.04313e-3, "MolarMass": 34.08},
    "Helium (He)": {"a": 0.0341 / 1e6, "b": 0.0237e-3, "MolarMass": 4.003},
    "Water Vapor (H2O)": {"a": 5.537e5 / 1e6, "b": 0.03049e-3, "MolarMass": 18.015},
    "Benzene (C6H6)": {"a": 5.506e6 / 1e6, "b": 0.1065e-3, "MolarMass": 78.11},
    "Toluene (C7H8)": {"a": 6.960e6 / 1e6, "b": 0.1128e-3, "MolarMass": 92.14},
    "Xylenes (C8H10)": {"a": 8.613e6 / 1e6, "b": 0.1243e-3, "MolarMass": 106.17},
    "Ethylene (C2H4)": {"a": 4.560e5 / 1e6, "b": 0.0519e-3, "MolarMass": 28.05},
    "Propylene (C3H6)": {"a": 7.036e5 / 1e6, "b": 0.0631e-3, "MolarMass": 42.08},
    "Carbonyl Sulfide (COS)": {"a": 4.535e5 / 1e6, "b": 0.0485e-3, "MolarMass": 60.07},
    "Carbon Disulfide (CS2)": {"a": 8.074e5 / 1e6, "b": 0.0652e-3, "MolarMass": 76.14},
    "Argon (Ar)": {"a": 1.355e5 / 1e6, "b": 0.03201e-3, "MolarMass": 39.95},
    "Neon (Ne)": {"a": 0.0213 / 1e6, "b": 0.0171e-3, "MolarMass": 20.18},
}

class GasPropertiesEstimator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Natural Gas Properties Estimator (Van der Waals EOS)")
        self.setGeometry(300, 200, 800, 600)
        
        # Main layout of the desktop software
        main_layout = QVBoxLayout()
        
        # The screen where user's can select gas components
        self.gas_selector = QComboBox()
        self.gas_selector.addItems(VDW_CONSTANTS.keys()) # .keys allows the app to have all the values of our dict as values for the dropdown
        
        self.add_gas_button = QPushButton("Add Gas Component") # The button users press to add gas components
        self.add_gas_button.clicked.connect(self.add_gas_component)

        gas_selection_layout = QHBoxLayout()
        gas_selection_layout.addWidget(QLabel("Select Gas Component:"))
        gas_selection_layout.addWidget(self.gas_selector)
        gas_selection_layout.addWidget(self.add_gas_button)
        
        # When users select components, they are added to a Table for components and ratios
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Component", "Molar Ratio"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # The input where users can enter Temperature and pressure of the gas mixture
        self.temp_input = QLineEdit()
        self.pressure_input = QLineEdit()
        temp_press_layout = QHBoxLayout()
        temp_press_layout.addWidget(QLabel("Temperature (K):")) # The Temperature must be imputted in Kelvin
        temp_press_layout.addWidget(self.temp_input)
        temp_press_layout.addWidget(QLabel("Pressure (Pa):"))  # The Pressure must be imputted in Pascals
        temp_press_layout.addWidget(self.pressure_input)
        
        # The button user's press to initalize the Calculation
        self.calculate_button = QPushButton("Calculate Properties")
        self.calculate_button.clicked.connect(self.calculate_properties)

        # The result display 
        self.result_label = QLabel("Results will be displayed here.")
        
        # Here we add all our created widget to the app layout 
        main_layout.addLayout(gas_selection_layout)
        main_layout.addWidget(self.table)
        main_layout.addLayout(temp_press_layout)
        main_layout.addWidget(self.calculate_button)
        main_layout.addWidget(self.result_label)
        
        # Now we would set the main widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        


    #  With these funtion we add gas components, when users click the add components button, these funtion is triggered
    #  and a new row is added to the table with the gas values
    def add_gas_component(self):
        gas = self.gas_selector.currentText()
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(gas))
        self.table.setItem(row, 1, QTableWidgetItem("0.0"))


    #  This is the funtion triggered when the user clicks the calculate button
    def calculate_properties(self):
        # Parse gas components and ratios
        gases = []
        ratios = []
        for row in range(self.table.rowCount()):
            gas = self.table.item(row, 0).text()
            try:
                ratio = float(self.table.item(row, 1).text())
                if not (0.0 < ratio <= 1.0):
                    raise ValueError("Molar ratios must be between 0 and 1") # The molar ratio of the Gas must be == 1
                gases.append(gas)
                ratios.append(ratio)
            except ValueError:
                self.result_label.setText("Error: Invalid molar ratio entered.")   
                return         

        
        total_ratio = sum(ratios)
        ratios = [r / total_ratio for r in ratios]  # Normalize ratios

        # Here we recive the presure and temp inputted by the user and parse it
        T = float(self.temp_input.text())
        P = float(self.pressure_input.text())

        # Calculate mixture properties (a_mix, b_mix)
        a_mix = sum(ratios[i] * ratios[j] * np.sqrt(VDW_CONSTANTS[gases[i]]["a"] * VDW_CONSTANTS[gases[j]]["a"]) 
                    for i in range(len(gases)) for j in range(len(gases)))
        
        b_mix = sum(ratios[i] * VDW_CONSTANTS[gases[i]]["b"] for i in range(len(gases)))
        molar_mass_mix = sum(ratios[i] * VDW_CONSTANTS[gases[i]]["MolarMass"] for i in range(len(gases)))

        # Here we define the Van der Waals equation
        def vander_waals_equation(Vm):
            return (P + a_mix / Vm**2) * (Vm - b_mix) - R * T

        # We solve for the molar volume (Vm)
        Vm_initial_guess = R * T / P
        Vm_solution, = fsolve(vander_waals_equation, Vm_initial_guess)

        # after calculating Vm solution, we use the value to calculate compressibility factor (Z) and density (ρ)
        Z = (P * Vm_solution) / (R * T)
        density = molar_mass_mix / Vm_solution  # in g/m^3

        # Display results
        result_text = (f"Molar Volume (Vm): {Vm_solution:.4f} m³/mol\n"
                       f"Compressibility Factor (Z): {Z:.4f}\n"
                       f"Density (ρ): {density:.4f} g/m³")
        print(result_text)
        self.result_label.setText(result_text)

app = QApplication(sys.argv)
window = GasPropertiesEstimator()
window.show()
sys.exit(app.exec())
