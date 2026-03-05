import math
import numpy as np
import matplotlib.pyplot as plt

def get_compressor_angles(R, psi, phi):
    """
    Calculates axial compressor velocity triangle angles from dimensionless parameters.
    
    Parameters:
    R (float): Degree of reaction
    psi (float): Stage loading coefficient
    phi (float): Flow coefficient
    
    Returns:
    dict: Angles alpha1, alpha2, beta1, beta2 in degrees.
    """
    
    # 1. Calculate tan(alpha1) from the R equation
    tan_alpha1 = (1 - R - (psi / 2)) / phi
    
    # 2. Calculate tan(beta2) from the psi equation
    # psi = -phi*tan_alpha1 + phi*tan_beta2 + 1  => phi*tan_beta2 = psi - 1 + phi*tan_alpha1
    tan_beta2 = (psi - 1 + (phi * tan_alpha1)) / phi
    
    # 3. Calculate remaining tangents from kinematic relations
    tan_beta1 = tan_alpha1 - (1 / phi)
    tan_alpha2 = tan_beta2 + (1 / phi)
    
    # Convert all to degrees
    angles = {
        "alpha1": math.degrees(math.atan(tan_alpha1)),
        "alpha2": math.degrees(math.atan(tan_alpha2)),
        "beta1": math.degrees(math.atan(tan_beta1)),
        "beta2": math.degrees(math.atan(tan_beta2))
    }
    
    return angles


def plot_overlapping_triangles_quiver(alpha1, alpha2, beta1, beta2):
    """
    Plots the inlet and outlet velocity triangles using quiver for robust arrow rendering.
    Angles in degrees, measured from the axial direction.
    """
    # Convert degrees to radians
    a1, a2 = np.radians(alpha1), np.radians(alpha2)
    b1, b2 = np.radians(beta1), np.radians(beta2)
    
    # Normalize Axial Velocity Vx = 1
    vx = 1.0
    
    # Tangential components
    vt1, vt2 = vx * np.tan(a1), vx * np.tan(a2)
    wt1, wt2 = vx * np.tan(b1), vx * np.tan(b2)
    u_val = vt1 - wt1  # Blade speed
    
    plt.figure(figsize=(10, 8))
    
    # Data structure for quiver: [X_origin], [Y_origin], [U_direction], [V_direction]
    # Station 1 (Inlet) - Solid
    plt.quiver([0, u_val], [0, 0], [vt1, wt1], [vx, vx], 
               angles='xy', scale_units='xy', scale=1, color=['red', 'blue'], 
               label=['V1 (Abs)', 'W1 (Rel)'], width=0.015)
    
    # Station 2 (Outlet) - Dashed/Lighter
    plt.quiver([0, u_val], [0, 0], [vt2, wt2], [vx, vx], 
               angles='xy', scale_units='xy', scale=1, color=['darkred', 'darkblue'], 
               alpha=0.5, label=['V2 (Abs)', 'W2 (Rel)'], width=0.01)
    
    # Blade Speed U
    plt.quiver([0], [0], [u_val], [0], 
               angles='xy', scale_units='xy', scale=1, color='green', 
               label='Blade Speed (U)', width=0.02)

    # Adding labels directly near the tips for clarity
    plt.text(vt1, vx, r'$V_1$', color='red', fontsize=12, fontweight='bold')
    plt.text(vt2, vx, r'$V_2$', color='darkred', fontsize=12, fontweight='bold')
    
    # Formatting
    plt.axhline(0, color='black', lw=1)
    plt.axvline(0, color='black', lw=0.5, linestyle='--')
    plt.title("Axial Compressor Velocity Triangles")
    plt.xlabel("Tangential Velocity ($V_θ$)")
    plt.ylabel("Axial Velocity ($V_x$)")
    
    # Adjust limits to see the whole triangle
    padding = 0.5
    plt.xlim(min(0, vt1, vt2, u_val) - padding, max(0, vt1, vt2, u_val) + padding)
    plt.ylim(-0.2, 1.3)
    
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper right')
    plt.gca().set_aspect('equal')
    
    plt.show()



def calculate_recovery_factor(alpha1_deg, beta2_deg, phi):
    """
    Calculates the Recovery Factor (R_R) based on alpha1, beta2, and phi.
    
    Parameters:
    alpha1_deg (float): Inlet absolute flow angle in degrees.
    beta2_deg (float): Outlet relative flow angle in degrees.
    phi (float): Flow coefficient.
    
    Returns:
    float: The calculated Recovery Factor (R_R).
    """
    # Convert angles from degrees to radians
    a1 = math.radians(alpha1_deg)
    b2 = math.radians(beta2_deg)
    
    # Pre-calculate common trigonometric values for readability
    cos_a1_sq = math.cos(a1)**2
    cos_b2_sq = math.cos(b2)**2
    tan_a1 = math.tan(a1)
    tan_b2 = math.tan(b2)
    
    # Term 1: (cos² β2 * tan β2) / phi
    term1 = (cos_b2_sq * tan_b2) / phi
    
    # Term 2: (cos² α1 * cos² β2 * tan α1 * tan β2) / phi²
    term2 = (cos_a1_sq * cos_b2_sq * tan_a1 * tan_b2) / (phi**2)
    
    # Term 3: (cos² α1 * tan α1) / phi
    term3 = (cos_a1_sq * tan_a1) / phi
    
    # Final Recovery Factor calculation
    rr = term1 - term2 + term3
    
    return rr


def get_optimal_psi(phi):

    optimal_psi = 0.185*np.sqrt(4*phi*phi +1)

    return optimal_psi


# Get angles for velocity triangles
angles = get_compressor_angles(R=0.5, psi=0.275, phi=0.55)
alpha1, alpha2, beta1, beta2 = angles['alpha1'], angles['alpha2'], angles["beta1"] , angles['beta2']
print(angles)

#plot triangles
plot_overlapping_triangles_quiver(alpha1, alpha2, beta1, beta2)

#calculate recovery factor
rr_value = calculate_recovery_factor(alpha1, beta2, phi=0.55)
print(f"Recovery Factor: {rr_value}")


#Next steps:
rotor_reflection = beta1- beta2 #TODO: USE Beta angles if you calculate RR for rotor.

#TODO:USE LieBlein loading factor!!
#incidence should be 3-5 deg, 20 is crazy, 0 is crazy. (negative incidence makes the compressor unstable.)
#how to get efficiency? total-total, look at smith charts.
#before doing CFD, you need to know if ANY part of the blade is in chocked condition. What is the criterion?(Slide 52 Lecture 6 axial compressor, "Inlet Control Volume Analysis")
#The design point should be in the middle of the speedline. The speedline should be chosen thrugh preliminary design such that the Design point(decided by the massflowrate) is in the mid of the speedline.
#Thin airfoil => mechanical failure through dynamic excitations
#Check velocity traingle at the tip. (M1 at the tip will be larger than one in the project)
#incidence angle is computed through the Lip-Line model.
#if M2<1 unstarted regime, bowshock in front.

