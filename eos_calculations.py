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




class _PengRobinsonEOS:
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










import numpy as np
from scipy.optimize import fsolve

class PengRobinsonEOS:
    def __init__(self, T, P, Pc, Tc, omega):
        self.T = T  # Temperature in K
        self.P = P  # Pressure in Pa
        self.Pc = Pc  # Critical pressure in Pa
        self.Tc = Tc  # Critical temperature in K
        self.omega = omega  # Acentric factor
        self.R = 8.314  # Gas constant in J/(mol*K)

        # Calculate constants 'a' and 'b' for the component
        self.a = 0.45724 * (self.R ** 2) * (self.Tc ** 2) / self.Pc
        self.b = 0.07780 * self.R * self.Tc / self.Pc

    def calculate_alpha(self):
        # Calculate α(T)
        m = 0.37464 + 1.54226 * self.omega - 0.26992 * self.omega ** 2
        return (1 + m * (1 - np.sqrt(self.T / self.Tc))) ** 2

    def calculate_molar_volume(self):
        alpha = self.calculate_alpha()
        a_alpha = self.a * alpha

        # Define the equation to solve for Vm
        def equation(Vm):
            term1 = (self.R * self.T) / (Vm - self.b)
            term2 = a_alpha / (Vm ** 2 + 2 * self.b * Vm - self.b ** 2)
            return self.P - (term1 - term2)

        # Initial guess for molar volume
        initial_guess = (self.R * self.T) / self.P
        Vm_solution, = fsolve(equation, initial_guess)
        return Vm_solution

    def calculate_compressibility_factor(self, Vm):
        Z = (self.P * Vm) / (self.R * self.T)
        return Z


class PengRobinsonMixture:
    def __init__(self, T, P, components, molar_fractions):
        self.T = T
        self.P = P
        self.components = components  # List of (Pc, Tc, omega) tuples for each component
        self.molar_fractions = molar_fractions  # Dictionary of molar fractions
        self.R = 8.314

        # Calculate mixture properties
        self.a_mix = self.calculate_a_mix()
        self.b_mix = self.calculate_b_mix()

    def calculate_a_mix(self):
        # Calculate mixture a parameter using combining rules
        a_mix = 0
        for i, (Pc_i, Tc_i, omega_i) in enumerate(self.components):
            eos_i = PengRobinsonEOS(self.T, self.P, Pc_i, Tc_i, omega_i)
            for j, (Pc_j, Tc_j, omega_j) in enumerate(self.components):
                eos_j = PengRobinsonEOS(self.T, self.P, Pc_j, Tc_j, omega_j)
                a_ij = np.sqrt(eos_i.a * eos_j.a)
                a_mix += (
                    self.molar_fractions[i]
                    * self.molar_fractions[j]
                    * a_ij
                )
        return a_mix

    def calculate_b_mix(self):
        # Calculate mixture b parameter using linear combination
        b_mix = sum(
            self.molar_fractions[i] * PengRobinsonEOS(self.T, self.P, *self.components[i]).b
            for i in range(len(self.components))
        )
        return b_mix

    def calculate_molar_volume(self):
        # Define the equation to solve for Vm
        def equation(Vm):
            term1 = (self.R * self.T) / (Vm - self.b_mix)
            term2 = self.a_mix / (Vm ** 2 + 2 * self.b_mix * Vm - self.b_mix ** 2)
            return self.P - (term1 - term2)

        # Initial guess for molar volume
        initial_guess = (self.R * self.T) / self.P
        Vm_solution, = fsolve(equation, initial_guess)
        return Vm_solution

    def calculate_compressibility_factor(self, Vm):
        Z = (self.P * Vm) / (self.R * self.T)
        return Z

    def calculate_density(self, Vm):
        # Density (ρ) = molar mass / molar volume
        molar_mass_mix = sum(
            self.molar_fractions[i] * molar_mass
            for i, molar_mass in enumerate([ethane, propane, butane, pentane, nonane, hydrogen]) # Replace with actual molar mass values
        )
        density = molar_mass_mix / Vm  # Density in kg/m³ if molar mass is in g/mol and Vm in m³/mol
        return density

    def calculate_enthalpy(self, T):
        # Placeholder for enthalpy calculation
        # This can be expanded based on specific heat and mixture properties
        return T * self.R

    def calculate_entropy(self, T, P):
        # Placeholder for entropy calculation
        # This can be expanded based on specific entropy and mixture properties
        return T * self.R / P

    def calculate_properties(self):
        Vm = self.calculate_molar_volume()
        Z = self.calculate_compressibility_factor(Vm)
        density = self.calculate_density(Vm)
        enthalpy = self.calculate_enthalpy(self.T)
        entropy = self.calculate_entropy(self.T, self.P)

        return {
            "Molar Volume": Vm,
            "Compressibility Factor": Z,
            "Density": density,
            "Enthalpy": enthalpy,
            "Entropy": entropy,
        }
