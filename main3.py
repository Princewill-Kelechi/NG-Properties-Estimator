# main.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
from eos_calculations import PengRobinsonEOS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Natural Gas Property Estimator")
        self.setGeometry(300, 200, 400, 400)

        layout = QVBoxLayout()

        # Input fields for temperature, pressure, a, b, Tc, and omega
        self.temp_input = QLineEdit(self)
        self.temp_input.setPlaceholderText("Temperature (K)")
        self.pressure_input = QLineEdit(self)
        self.pressure_input.setPlaceholderText("Pressure (Pa)")
        self.a_input = QLineEdit(self)
        self.a_input.setPlaceholderText("Constant a (J*m^3/mol^2)")
        self.b_input = QLineEdit(self)
        self.b_input.setPlaceholderText("Constant b (m^3/mol)")
        self.Tc_input = QLineEdit(self)
        self.Tc_input.setPlaceholderText("Critical Temperature Tc (K)")
        self.omega_input = QLineEdit(self)
        self.omega_input.setPlaceholderText("Acentric Factor ω")

        # Button for Peng-Robinson EOS calculation
        self.pr_btn = QPushButton("Calculate with Peng-Robinson EOS")
        self.pr_btn.clicked.connect(self.calculate_peng_robinson)

        # Output label
        self.output_label = QLabel("Result: ", self)

        # Add widgets to layout
        layout.addWidget(self.temp_input)
        layout.addWidget(self.pressure_input)
        layout.addWidget(self.a_input)
        layout.addWidget(self.b_input)
        layout.addWidget(self.Tc_input)
        layout.addWidget(self.omega_input)
        layout.addWidget(self.pr_btn)
        layout.addWidget(self.output_label)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def calculate_peng_robinson(self):
        try:
            # Parse user inputs
            temp = float(self.temp_input.text())
            pressure = float(self.pressure_input.text())
            a = float(self.a_input.text())
            b = float(self.b_input.text())
            Tc = float(self.Tc_input.text())
            omega = float(self.omega_input.text())

            # Calculate using Peng-Robinson EOS
            result = PengRobinsonEOS(temp, pressure, a, b, Tc, omega).calculate_properties()
            self.output_label.setText(f"Result: {result}")
        except ValueError:
            self.output_label.setText("Invalid input! Please enter numerical values.")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
