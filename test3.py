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
    QTabWidget,
    QScrollArea,
)
from PySide6.QtCore import Qt


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
            "Methane (CH₄)",
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
            "Neon (Ne)"
        ]

        # Step 1: Gas Component Selection
        self.create_gas_selection_screen()

    def create_gas_selection_screen(self):
        self.clear_layout(self.main_layout)

        # Gas selection screen
        self.gas_selection_group = QGroupBox("Select Gas Components")
        gas_selection_layout = QVBoxLayout()

        # Checkboxes for each component
        self.component_checkboxes = {}
        for component in self.available_components:
            checkbox = QCheckBox(component)
            gas_selection_layout.addWidget(checkbox)
            self.component_checkboxes[component] = checkbox

        self.gas_selection_group.setLayout(gas_selection_layout)

        # Next button
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.create_molar_fraction_screen)

        # Add to main layout
        self.main_layout.addWidget(self.gas_selection_group)
        self.main_layout.addWidget(self.next_button)

    def create_molar_fraction_screen(self):
        # Collect selected components
        self.selected_components = [
            comp
            for comp, checkbox in self.component_checkboxes.items()
            if checkbox.isChecked()
        ]
        if not self.selected_components:
            # If no components are selected, show the selection screen again
            return

        # Create tab widget for the molar fraction input and additional parameters
        self.clear_layout(self.main_layout)
        self.tab_widget = QTabWidget()

        # Molar Fraction Tab
        self.create_molar_fraction_tab()

        # Additional Parameter Tabs
        self.create_additional_parameters_tabs()

        # Add the tab widget and submit button
        self.main_layout.addWidget(self.tab_widget)

        # Submit Button
        self.submit_button = QPushButton("Calculate Properties")
        self.submit_button.clicked.connect(self.calculate_properties)
        self.main_layout.addWidget(self.submit_button)

    def create_molar_fraction_tab(self):
        molar_fraction_tab = QWidget()
        molar_fraction_layout = QFormLayout()

        # Input fields for selected components' molar fractions
        self.molar_fraction_inputs = {}
        for component in self.selected_components:
            molar_input = QLineEdit()
            molar_fraction_layout.addRow(f"{component} Molar Fraction:", molar_input)
            self.molar_fraction_inputs[component] = molar_input

        molar_fraction_tab.setLayout(molar_fraction_layout)
        self.tab_widget.addTab(molar_fraction_tab, "Molar Fractions")

    def create_additional_parameters_tabs(self):
        # Pressure and Temperature Tab
        pressure_temp_tab = QWidget()
        pressure_temp_layout = QFormLayout()

        self.pressure_input = QLineEdit()
        self.temperature_input = QLineEdit()

        pressure_temp_layout.addRow("Pressure (Pa):", self.pressure_input)
        pressure_temp_layout.addRow("Temperature (K):", self.temperature_input)

        pressure_temp_tab.setLayout(pressure_temp_layout)
        self.tab_widget.addTab(pressure_temp_tab, "Pressure & Temperature")

        # EOS and Critical Properties Tab
        additional_params_tab = QWidget()
        additional_params_layout = QFormLayout()

        self.eos_dropdown = QComboBox()
        self.eos_dropdown.addItems(
            ["Peng-Robinson", "Redlich-Kwong", "Soave-Redlich-Kwong"]
        )
        self.critical_pressure_input = QLineEdit()
        self.critical_temperature_input = QLineEdit()
        self.acentric_factor_input = QLineEdit()

        additional_params_layout.addRow("Select EOS:", self.eos_dropdown)
        additional_params_layout.addRow(
            "Critical Pressure (Pa):", self.critical_pressure_input
        )
        additional_params_layout.addRow(
            "Critical Temperature (K):", self.critical_temperature_input
        )
        additional_params_layout.addRow("Acentric Factor:", self.acentric_factor_input)

        additional_params_tab.setLayout(additional_params_layout)
        self.tab_widget.addTab(additional_params_tab, "EOS & Critical Properties")

    def calculate_properties(self):
        # Retrieve molar fractions for each selected component
        molar_fractions = {
            component: self.molar_fraction_inputs[component].text()
            for component in self.selected_components
        }

        # Retrieve pressure, temperature, EOS, and additional parameters
        pressure = self.pressure_input.text()
        temperature = self.temperature_input.text()
        selected_eos = self.eos_dropdown.currentText()
        critical_pressure = self.critical_pressure_input.text()
        critical_temperature = self.critical_temperature_input.text()
        acentric_factor = self.acentric_factor_input.text()

        # Print values (or replace with actual calculation logic)
        print("Selected Components and Molar Fractions:", molar_fractions)
        print("Pressure:", pressure, "Temperature:", temperature)
        print("Selected EOS:", selected_eos)
        print(
            "Critical Pressure:",
            critical_pressure,
            "Critical Temperature:",
            critical_temperature,
            "Acentric Factor:",
            acentric_factor,
        )

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
