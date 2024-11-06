import numpy as np
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QCheckBox,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGroupBox,
    QScrollArea,
)
from PySide6.QtCore import Qt

# Constants
R = 8.314  # Gas constant in J/(mol·K)

class GasEstimationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Natural Gas Properties Estimation")
        self.setGeometry(300, 200, 800, 600)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # List of possible gas components
        self.available_components = [
            "Ethane (C₂H₆)",
            "Propane (C₃H₈)",
            "Butane (C₄H₁₀)",
            "Pentane (C₅H₁₂)",
            "Hexane (C₆H₁₄)",
            "Heptane (C₇H₁₆)",
            "Octane (C₈H₁₈)",
            "Nonane (C₉H₂₀)",
            "Decane (C₁₀H₂₂)",
            "Carbon Dioxide (CO₂)",
            "Nitrogen (N₂)",
            "Oxygen (O₂)",
            "Hydrogen (H₂)",
            "Hydrogen Sulfide (H₂S)",
            "Helium (He)",
            "Water Vapor (H₂O)",
            "Benzene (C₆H₆)",
            "Toluene (C₇H₈)",
            "Xylenes (C₈H₁₀)",
            "Ethylene (C₂H₄)",
            "Propylene (C₃H₆)",
            "Carbonyl Sulfide (COS)",
            "Carbon Disulfide (CS₂)",
            "Argon (Ar)",
            "Neon (Ne)",
        ]

        # Step 1: Gas Component Selection
        self.create_gas_selection_screen()

    def create_gas_selection_screen(self):
        # Gas selection screen
        self.gas_selection_group = QGroupBox("Select Gas Components")
        gas_selection_layout = QHBoxLayout()  # Main layout for two columns

        # Create two vertical layouts for stacking components into two columns
        left_column = QVBoxLayout()
        right_column = QVBoxLayout()

        # Checkboxes for each component
        self.component_checkboxes = {}
        half_index = len(self.available_components) // 2

        # Add checkboxes to two columns
        for i, component in enumerate(self.available_components):
            checkbox = QCheckBox(component)
            self.component_checkboxes[component] = checkbox
            if i < half_index:
                left_column.addWidget(checkbox)
            else:
                right_column.addWidget(checkbox)

        # Add left and right columns to the main layout
        gas_selection_layout.addLayout(left_column)
        gas_selection_layout.addLayout(right_column)

        # Set layout for the gas selection group
        self.gas_selection_group.setLayout(gas_selection_layout)

        # Next button
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.create_main_input_screen)

        # Add to main layout
        self.main_layout.addWidget(self.gas_selection_group)
        self.main_layout.addWidget(self.next_button)

    def create_main_input_screen(self):
        # Collect selected components
        self.selected_components = [
            comp
            for comp, checkbox in self.component_checkboxes.items()
            if checkbox.isChecked()
        ]
        if not self.selected_components:
            return

        # Clear the selection screen
        self.clear_layout(self.main_layout)

        # Gas Composition Section with Scroll Area
        gas_composition_group = QGroupBox("Gas Composition")
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_widget = QWidget()
        gas_composition_layout = QFormLayout(scroll_widget)

        # Add input fields for each selected component
        self.molar_fraction_inputs = {}
        for component in self.selected_components:
            molar_input = QLineEdit()
            gas_composition_layout.addRow(f"{component} Molar Fraction:", molar_input)
            self.molar_fraction_inputs[component] = molar_input

        scroll_area.setWidget(scroll_widget)
        layout_with_scroll = QVBoxLayout()
        layout_with_scroll.addWidget(scroll_area)
        gas_composition_group.setLayout(layout_with_scroll)

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
        self.eos_dropdown.addItems(
            ["Peng-Robinson", "Redlich-Kwong", "Soave-Redlich-Kwong"]
        )
        eos_layout.addWidget(QLabel("Select EOS:"))
        eos_layout.addWidget(self.eos_dropdown)

        eos_group.setLayout(eos_layout)

        # Additional Parameters Section
        additional_params_group = QGroupBox("Additional Parameters")
        additional_params_layout = QFormLayout()

        self.critical_pressure_input = QLineEdit()
        self.critical_temperature_input = QLineEdit()
        self.acentric_factor_input = QLineEdit()

        additional_params_layout.addRow(
            "Critical Pressure (Pa):", self.critical_pressure_input
        )
        additional_params_layout.addRow(
            "Critical Temperature (K):", self.critical_temperature_input
        )
        additional_params_layout.addRow("Acentric Factor:", self.acentric_factor_input)

        additional_params_group.setLayout(additional_params_layout)

        # Submit Button
        self.submit_button = QPushButton("Calculate Properties")
        self.submit_button.clicked.connect(self.calculate_properties)

        # Add sections to main layout
        self.main_layout.addWidget(gas_composition_group)
        self.main_layout.addWidget(pressure_temp_group)
        self.main_layout.addWidget(eos_group)
        self.main_layout.addWidget(additional_params_group)
        self.main_layout.addWidget(self.submit_button)

    def calculate_properties(self):
        # Retrieve molar fractions for each selected component
        molar_fractions = {
            component: float(self.molar_fraction_inputs[component].text())
            for component in self.selected_components
        }

        # Retrieve pressure, temperature, EOS, and additional parameters
        pressure = float(self.pressure_input.text())
        temperature = float(self.temperature_input.text())
        critical_pressure = float(self.critical_pressure_input.text())
        critical_temperature = float(self.critical_temperature_input.text())
        acentric_factor = float(self.acentric_factor_input.text())

        # Perform Peng-Robinson calculations
        molar_volume = self.calculate_molar_volume(pressure, temperature, critical_pressure, critical_temperature, acentric_factor)
        compressibility_factor = self.calculate_compressibility_factor(molar_volume, pressure, temperature)
        density = self.calculate_density(molar_volume)
        enthalpy = self.calculate_enthalpy(temperature)
        entropy = self.calculate_entropy(temperature, pressure)

        print(f"Molar Volume: {molar_volume} m³/mol")
        print(f"Compressibility Factor: {compressibility_factor}")
        print(f"Density: {density} kg/m³")
        print(f"Enthalpy: {enthalpy} J/mol")
        print(f"Entropy: {entropy} J/(mol·K)")

    def calculate_molar_volume(self, P, T, Pc, Tc, omega):
        # Implement Peng-Robinson molar volume calculation
        # Example placeholder calculation
        return (R * T) / P

    def calculate_compressibility_factor(self, Vm, P, T):
        # Example placeholder for compressibility factor calculation
        return 1

    def calculate_density(self, Vm):
        # Example placeholder for density calculation
        return 1 / Vm

    def calculate_enthalpy(self, T):
        # Example placeholder for enthalpy calculation
        return T * R

    def calculate_entropy(self, T, P):
        # Example placeholder for entropy calculation
        return T * R / P

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


if __name__ == "__main__":
    app = QApplication([])
    window = GasEstimationApp()
    window.show()
    app.exec()
