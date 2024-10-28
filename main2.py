# # main.py

# import sys
# from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
# from eos_calculations import VanDerWaalsEOS

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Natural Gas Property Estimator")
#         self.setGeometry(300, 200, 400, 300)

#         layout = QVBoxLayout()

#         # Input fields for temperature, pressure, a, b
#         self.temp_input = QLineEdit(self)
#         self.temp_input.setPlaceholderText("Temperature (K)")
#         self.pressure_input = QLineEdit(self)
#         self.pressure_input.setPlaceholderText("Pressure (Pa)")
#         self.a_input = QLineEdit(self)
#         self.a_input.setPlaceholderText("Constant a (J*m^3/mol^2)")
#         self.b_input = QLineEdit(self)
#         self.b_input.setPlaceholderText("Constant b (m^3/mol)")

#         # Button for Van der Waals EOS calculation
#         self.vdw_btn = QPushButton("Calculate with Van der Waals EOS")
#         self.vdw_btn.clicked.connect(self.calculate_van_der_waals)

#         # Output label
#         self.output_label = QLabel("Result: ", self)

#         # Add widgets to layout
#         layout.addWidget(self.temp_input)
#         layout.addWidget(self.pressure_input)
#         layout.addWidget(self.a_input)
#         layout.addWidget(self.b_input)
#         layout.addWidget(self.vdw_btn)
#         layout.addWidget(self.output_label)

#         # Set central widget
#         central_widget = QWidget()
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)

#     def calculate_van_der_waals(self):
#         try:
#             # Parse user inputs
#             temp = float(self.temp_input.text())
#             pressure = float(self.pressure_input.text())
#             a = float(self.a_input.text())
#             b = float(self.b_input.text())

#             # Calculate using Van der Waals EOS
#             result = VanDerWaalsEOS(temp, pressure, a, b).calculate_properties()
#             self.output_label.setText(f"Result: {result}")
#         except ValueError:
#             self.output_label.setText("Invalid input! Please enter numerical values.")

# app = QApplication(sys.argv)
# window = MainWindow()
# window.show()
# sys.exit(app.exec())




# main.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
from eos_calculations import VanDerWaalsEOS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Natural Gas Property Estimator")
        self.setGeometry(300, 200, 400, 500)

        layout = QVBoxLayout()

        # Input fields for temperature, pressure, constants a and b, and molar mass
        self.temp_input = QLineEdit(self)
        self.temp_input.setPlaceholderText("Temperature (K)")
        self.pressure_input = QLineEdit(self)
        self.pressure_input.setPlaceholderText("Pressure (Pa)")
        self.a_input = QLineEdit(self)
        self.a_input.setPlaceholderText("Constant a (J·m³/mol²)")
        self.b_input = QLineEdit(self)
        self.b_input.setPlaceholderText("Constant b (m³/mol)")
        self.molar_mass_input = QLineEdit(self)
        self.molar_mass_input.setPlaceholderText("Molar Mass (kg/mol)")

        # Button for Van der Waals EOS calculation
        self.vdw_btn = QPushButton("Calculate with Van der Waals EOS")
        self.vdw_btn.clicked.connect(self.calculate_vdw)

        # Output label
        self.output_label = QLabel("Result: ", self)

        # Add widgets to layout
        layout.addWidget(self.temp_input)
        layout.addWidget(self.pressure_input)
        layout.addWidget(self.a_input)
        layout.addWidget(self.b_input)
        layout.addWidget(self.molar_mass_input)
        layout.addWidget(self.vdw_btn)
        layout.addWidget(self.output_label)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def calculate_vdw(self):
        try:
            # Parse user inputs
            temp = float(self.temp_input.text())
            pressure = float(self.pressure_input.text())
            a = float(self.a_input.text())
            b = float(self.b_input.text())
            molar_mass = float(self.molar_mass_input.text())

            # Calculate using Van der Waals EOS
            result = VanDerWaalsEOS(temp, pressure, a, b, molar_mass).calculate_properties()
            self.output_label.setText(f"Result: {result}")
        except ValueError:
            self.output_label.setText("Invalid input! Please enter numerical values.")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
