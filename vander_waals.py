import numpy as np
from scipy.optimize import fsolve

# Constants and properties of the mixture components (example values)
R = 8.314  # J/(mol·K), universal gas constant
temperature = 300  # K, example temperature
pressure = 5e6     # Pa, example pressure

# Component data: example values for each component
components = [
    {"y": 0.5, "T_c": 190.6, "P_c": 4599000, "M": 0.016},  # Methane
    {"y": 0.5, "T_c": 305.3, "P_c": 4872000, "M": 0.030}   # Ethane
]

# Step 2: Calculate individual Van der Waals constants for each component
for component in components:
    T_c = component["T_c"]
    P_c = component["P_c"]
    component["a"] = (27 / 64) * (R ** 2 * T_c ** 2) / P_c
    component["b"] = (R * T_c) / (8 * P_c)

# Step 3: Apply mixing rules
a_mix = sum(components[i]["y"] * components[j]["y"] * np.sqrt(components[i]["a"] * components[j]["a"])
            for i in range(len(components)) for j in range(len(components)))
b_mix = sum(comp["y"] * comp["b"] for comp in components)
molar_mass_mix = sum(comp["y"] * comp["M"] for comp in components)

# Step 5: Define the Van der Waals cubic equation in Vm
def van_der_waals_eq(Vm):
    return pressure * Vm**3 - (R * temperature) * Vm**2 + (pressure * b_mix + a_mix) * Vm - a_mix * b_mix

# Solve for molar volume Vm
Vm_initial_guess = (R * temperature) / pressure  # Ideal gas estimate
Vm_solution = fsolve(van_der_waals_eq, Vm_initial_guess)[0]

# Step 6: Calculate Compressibility Factor
Z = (pressure * Vm_solution) / (R * temperature)

# Step 7: Calculate Density
density = molar_mass_mix / Vm_solution

print(f"Molar Volume (Vm): {Vm_solution:.4f} m³/mol")
print(f"Compressibility Factor (Z): {Z:.4f}")
print(f"Density (ρ): {density:.6f} kg/m³")
