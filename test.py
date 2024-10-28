from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QSlider, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox
from PySide6.QtCore import Qt

class GasEstimationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Natural Gas Properties Estimation")
        self.setGeometry(300, 200, 800, 600)


        # Main layout
        main_layout = QVBoxLayout()

        # Gas Composition Section
        gas_composition_group = QGroupBox("Gas Composition")
        gas_composition_layout = QFormLayout()
        
        # Example gas components with molar fraction input fields
        self.methane_input = QLineEdit()
        self.ethane_input = QLineEdit()
        self.co2_input = QLineEdit()
        
        gas_composition_layout.addRow("Methane (CH₄) Molar Fraction:", self.methane_input)
        gas_composition_layout.addRow("Ethane (C₂H₆) Molar Fraction:", self.ethane_input)
        gas_composition_layout.addRow("Carbon Dioxide (CO₂) Molar Fraction:", self.co2_input)
        
        gas_composition_group.setLayout(gas_composition_layout)

        # Pressure and Temperature Section
        pressure_temp_group = QGroupBox("Pressure and Temperature")
        pressure_temp_layout = QFormLayout()

        self.pressure_input = QLineEdit()
        self.temperature_input = QLineEdit()
        
        pressure_temp_layout.addRow("Pressure (Pa):", self.pressure_input)
        pressure_temp_layout.addRow("Temperature (K):", self.temperature_input)
        
        pressure_temp_group.setLayout(pressure_temp_layout)

        # EOS Selection Section
        eos_group = QGroupBox("Equation of State Selection")
        eos_layout = QHBoxLayout()

        self.eos_dropdown = QComboBox()
        self.eos_dropdown.addItems(["Peng-Robinson", "Redlich-Kwong", "Soave-Redlich-Kwong"])
        eos_layout.addWidget(QLabel("Select EOS:"))
        eos_layout.addWidget(self.eos_dropdown)
        
        eos_group.setLayout(eos_layout)

        # Additional Parameters Section
        additional_params_group = QGroupBox("Additional Parameters")
        additional_params_layout = QFormLayout()

        self.critical_pressure_input = QLineEdit()
        self.critical_temperature_input = QLineEdit()
        self.acentric_factor_input = QLineEdit()
        
        additional_params_layout.addRow("Critical Pressure (Pa):", self.critical_pressure_input)
        additional_params_layout.addRow("Critical Temperature (K):", self.critical_temperature_input)
        additional_params_layout.addRow("Acentric Factor:", self.acentric_factor_input)
        
        additional_params_group.setLayout(additional_params_layout)

        # Submit Button
        self.submit_button = QPushButton("Calculate Properties")
        self.submit_button.clicked.connect(self.calculate_properties)

        # Add sections to main layout
        main_layout.addWidget(gas_composition_group)
        main_layout.addWidget(pressure_temp_group)
        main_layout.addWidget(eos_group)
        main_layout.addWidget(additional_params_group)
        main_layout.addWidget(self.submit_button)

        self.setLayout(main_layout)

    def calculate_properties(self):
        # Extract input values and perform calculations here
        methane_fraction = self.methane_input.text()
        ethane_fraction = self.ethane_input.text()
        co2_fraction = self.co2_input.text()
        pressure = self.pressure_input.text()
        temperature = self.temperature_input.text()
        selected_eos = self.eos_dropdown.currentText()
        critical_pressure = self.critical_pressure_input.text()
        critical_temperature = self.critical_temperature_input.text()
        acentric_factor = self.acentric_factor_input.text()

        # Display or process the input values (print for example purposes)
        print("Gas Composition:")
        print(f"  Methane: {methane_fraction}")
        print(f"  Ethane: {ethane_fraction}")
        print(f"  CO₂: {co2_fraction}")
        print("Conditions:")
        print(f"  Pressure: {pressure} Pa")
        print(f"  Temperature: {temperature} K")
        print(f"Selected EOS: {selected_eos}")
        print("Additional Parameters:")
        print(f"  Critical Pressure: {critical_pressure} Pa")
        print(f"  Critical Temperature: {critical_temperature} K")
        print(f"  Acentric Factor: {acentric_factor}")

        # Placeholder for the actual calculation logic

if __name__ == "__main__":
    app = QApplication([])
    window = GasEstimationApp()
    window.show()
    app.exec()
