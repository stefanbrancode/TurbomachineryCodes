import numpy as np
import math
def calculate_recovery_factor(alpha1_deg, beta2_deg, phi):
    """
    Calculates the Recovery Factor (R_R) based on alpha1, beta2, and phi.
    If R_R = 1 (Very Stable), it means that the perturbation was not transmitted to the next stage
    If R_R = 0 (Very Unstable), the perturbation is the same at the outlet as it is at the inlet of the stage
    
    This function assumes the same work coefficient for both stages Phi_1 = Phi_2 

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
