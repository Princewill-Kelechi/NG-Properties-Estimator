import numpy as np
from scipy.optimize import fsolve


# class IdealGasEOS:
#     def __init__(self, temp, pressure):
#         self.temp = temp
#         self.pressure = pressure

#     def calculate_properties(self):
#         R = 8.314  # Gas constant in J/(mol*K)
#         volume = (R * self.temp) / self.pressure
#         return f"Volume = {volume:.4f} m^3/mol"


# eos_calculations.py

class IdealGasEOS:
    def __init__(self, temp, pressure, molar_mass):
        self.temp = temp
        self.pressure = pressure
        self.molar_mass = molar_mass
        self.R = 8.314  # J/(mol*K), universal gas constant

    def calculate_molar_volume(self):
        # Calculate molar volume using Ideal Gas EOS
        Vm = (self.R * self.temp) / self.pressure
        return Vm

    def calculate_compressibility_factor(self):
        # For ideal gas, Z = 1
        return 1

    def calculate_density(self):
        # Calculate density using molar mass and molar volume
        Vm = self.calculate_molar_volume()
        density = self.molar_mass / Vm
        return density

    def calculate_properties(self):
        Vm = self.calculate_molar_volume()
        Z = self.calculate_compressibility_factor()
        density = self.calculate_density()
        return f"Molar Volume = {Vm:.4f} m³/mol, Compressibility Factor = {Z}, Density = {density:.6f} kg/m³"


# eos_calculations.py

# class VanDerWaalsEOS:
#     def __init__(self, temp, pressure, a, b):
#         self.temp = temp
#         self.pressure = pressure
#         self.a = a
#         self.b = b
#         self.R = 8.314  # J/(mol*K), universal gas constant

#     def calculate_molar_volume(self):
#         # Solve for molar volume Vm
#         # Rearranged Van der Waals equation: (P + a / Vm^2) * (Vm - b) = RT
 

#         def equation(Vm):
#             return (self.pressure + self.a / Vm**2) * (Vm - self.b) - self.R * self.temp

#         # Provide a reasonable initial guess for fsolve
#         initial_guess = (self.R * self.temp) / self.pressure
#         Vm_solution, = fsolve(equation, initial_guess)
#         return Vm_solution

#     def calculate_properties(self):
#         Vm = self.calculate_molar_volume()
#         return f"Molar Volume = {Vm:.4f} m³/mol"





# eos_calculations.py

class VanDerWaalsEOS:
    def __init__(self, temp, pressure, a, b, molar_mass):
        self.temp = temp
        self.pressure = pressure
        self.a = a
        self.b = b
        self.molar_mass = molar_mass
        self.R = 8.314  # J/(mol*K), universal gas constant

    def calculate_molar_volume(self):
        # Van der Waals equation to solve for Vm
        def vdW_eq(Vm):
            term1 = (self.R * self.temp) / (Vm - self.b)
            term2 = self.a / Vm**2
            return self.pressure - (term1 - term2)

        # Initial guess for Vm based on ideal gas law
        initial_guess = (self.R * self.temp) / self.pressure
        Vm_solution, = fsolve(vdW_eq, initial_guess)
        return Vm_solution

    def calculate_compressibility_factor(self, Vm):
        # Compressibility factor Z = PVm / RT
        Z = (self.pressure * Vm) / (self.R * self.temp)
        return Z

    def calculate_density(self, Vm):
        # Density rho = M / Vm
        density = self.molar_mass / Vm
        return density

    def calculate_properties(self):
        Vm = self.calculate_molar_volume()
        Z = self.calculate_compressibility_factor(Vm)
        density = self.calculate_density(Vm)
        return f"Molar Volume = {Vm:.4f} m³/mol, Compressibility Factor = {Z:.4f}, Density = {density:.6f} kg/m³"




class PengRobinsonEOS:
    def __init__(self, temp, pressure, a, b, Tc, omega):
        self.temp = temp
        self.pressure = pressure
        self.a = a
        self.b = b
        self.Tc = Tc
        self.omega = omega
        self.R = 8.314  # J/(mol*K), universal gas constant

    def calculate_alpha(self):
        # Calculate α(T)
        m = 0.37464 + 1.54226 * self.omega - 0.26992 * self.omega**2
        return (1 + m * (1 - np.sqrt(self.temp / self.Tc)))**2

    def calculate_molar_volume(self):
        alpha = self.calculate_alpha()
        a_alpha = self.a * alpha

        # Define the equation to solve for Vm
        def equation(Vm):
            term1 = (self.R * self.temp) / (Vm - self.b)
            term2 = a_alpha / (Vm**2 + 2 * self.b * Vm - self.b**2)
            return self.pressure - (term1 - term2)

        # Provide an initial guess for fsolve
        initial_guess = (self.R * self.temp) / self.pressure
        Vm_solution, = fsolve(equation, initial_guess)
        return Vm_solution

    def calculate_properties(self):
        Vm = self.calculate_molar_volume()
        return f"Molar Volume = {Vm:.4f} m³/mol"

