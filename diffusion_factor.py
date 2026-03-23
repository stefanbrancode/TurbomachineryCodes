import math

def calculate_diffusion_factor(alpha2_deg, alpha3_deg, sigma=1.0, component_type='rotor'):
    """
    Calculates the Diffusion Factor (DF) for a compressor blade row.
    
    Formula used:
    DF = (1 - cos(a2)/cos(a3)) + (cos(a2)/(2*sigma)) * (tan(a2) - tan(a3))
    
    Parameters:
    alpha2_deg (float): Inlet flow angle (relative for rotor, absolute for stator).
    alpha3_deg (float): Outlet flow angle (relative for rotor, absolute for stator).
    sigma (float): Solidity (chord/pitch).
    component_type (str): 'rotor' or 'stator' for user context.
    
    Returns:
    float: The calculated Diffusion Factor.
    """
    # Ensure angles are positive as per slide instructions
    a2_rad = math.radians(abs(alpha2_deg))
    a3_rad = math.radians(abs(alpha3_deg))
    
    # Term 1: Flow Diffusion
    # (1 - cos(a2) / cos(a3))
    term_diffusion = 1 - (math.cos(a2_rad) / math.cos(a3_rad))
    
    # Term 2: Blade Loading
    # (cos(a2) / (2 * sigma)) * (tan(a2) - tan(a3))
    term_loading = (math.cos(a2_rad) / (2 * sigma)) * (math.tan(a2_rad) - math.tan(a3_rad))
    
    df = term_diffusion + term_loading
    
    print(f"--- {component_type.upper()} ANALYSIS ---")
    return df
# Example Usage:
# df_rotor = calculate_diffusion_factor(45, 10, sigma=1.2, component_type='rotor')