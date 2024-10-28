# import sys
# from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
# from eos_calculations import IdealGasEOS# Separate module for EOS

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Natural Gas Property Estimator")
#         self.setGeometry(300, 200, 400, 300)

#         layout = QVBoxLayout()

#         # Input fields for temperature, pressure, etc.
#         self.temp_input = QLineEdit(self)
#         self.temp_input.setPlaceholderText("Temperature (K)")
#         self.pressure_input = QLineEdit(self)
#         self.pressure_input.setPlaceholderText("Pressure (Pa)")

#         # Buttons for different EOS calculations
#         self.ideal_gas_btn = QPushButton("Calculate with Ideal Gas EOS")
#         self.ideal_gas_btn.clicked.connect(self.calculate_ideal_gas)

#         # Output label
#         self.output_label = QLabel("Result: ", self)

#         # Add widgets to layout
#         layout.addWidget(self.temp_input)
#         layout.addWidget(self.pressure_input)
#         layout.addWidget(self.ideal_gas_btn)
#         layout.addWidget(self.output_label)

#         # Set central widget
#         central_widget = QWidget()
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)

#     def calculate_ideal_gas(self):
#         temp = float(self.temp_input.text())
#         pressure = float(self.pressure_input.text())
#         result = IdealGasEOS(temp, pressure).calculate_properties()
#         self.output_label.setText(f"Result: {result}")

# app = QApplication(sys.argv)
# window = MainWindow()
# window.show()
# sys.exit(app.exec())



# main.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
from eos_calculations import IdealGasEOS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Natural Gas Property Estimator")
        self.setGeometry(300, 200, 800, 600)

        layout = QVBoxLayout()

        # Input fields for temperature, pressure, and molar mass
        self.temp_input = QLineEdit(self)
        self.temp_input.setPlaceholderText("Temperature (K)")
        self.pressure_input = QLineEdit(self)
        self.pressure_input.setPlaceholderText("Pressure (Pa)")
        self.molar_mass_input = QLineEdit(self)
        self.molar_mass_input.setPlaceholderText("Molar Mass (kg/mol)")

        # Button for Ideal Gas EOS calculation
        self.ideal_gas_btn = QPushButton("Calculate with Ideal Gas EOS")
        self.ideal_gas_btn.clicked.connect(self.calculate_ideal_gas)

        # Output label
        self.output_label = QLabel("Result: ", self)

        # Add widgets to layout
        layout.addWidget(self.temp_input)
        layout.addWidget(self.pressure_input)
        layout.addWidget(self.molar_mass_input)
        layout.addWidget(self.ideal_gas_btn)
        layout.addWidget(self.output_label)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def calculate_ideal_gas(self):
        try:
            # Parse user inputs
            temp = float(self.temp_input.text())
            pressure = float(self.pressure_input.text())
            molar_mass = float(self.molar_mass_input.text())

            # Calculate using Ideal Gas EOS
            result = IdealGasEOS(temp, pressure, molar_mass).calculate_properties()
            self.output_label.setText(f"Result: {result}")
        except ValueError:
            self.output_label.setText("Invalid input! Please enter numerical values.")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
