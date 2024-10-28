# Gemini


import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
)

class GasPropertyEstimator(QWidget):
    def __init__(self):
        super().__init__()

        # Create layout
        main_layout = QVBoxLayout()

        # Gas Composition Section
        composition_layout = QHBoxLayout()
        composition_label = QLabel("Gas Composition (Molar Fractions):")
        composition_layout.addWidget(composition_label)
        # ... Add QLineEdit fields for each component

        # Pressure and Temperature Section
        pt_layout = QHBoxLayout()
        pressure_label = QLabel("Pressure (bar):")
        pressure_input = QLineEdit()
        temperature_label = QLabel("Temperature (K):")
        temperature_input = QLineEdit()
        pt_layout.addWidget(pressure_label)
        pt_layout.addWidget(pressure_input)
        pt_layout.addWidget(temperature_label)
        pt_layout.addWidget(temperature_input)

        # EOS Selection
        eos_layout = QHBoxLayout()
        eos_label = QLabel("Equation of State:")
        eos_combo = QComboBox()
        eos_combo.addItems(["Peng-Robinson", "Redlich-Kwong"])
        eos_layout.addWidget(eos_label)
        eos_layout.addWidget(eos_combo)

        # Additional Parameters (optional)
        # ... Add more layouts and widgets as needed

        # Submit Button
        submit_button = QPushButton("Calculate")

        # Add layouts to main layout
        main_layout.addLayout(composition_layout)
        main_layout.addLayout(pt_layout)
        main_layout.addLayout(eos_layout)
        # ... Add additional layouts
        main_layout.addWidget(submit_button)

        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GasPropertyEstimator()
    window.show()
    sys.exit(app.exec_())