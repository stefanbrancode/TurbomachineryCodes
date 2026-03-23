# Given duty coefficients, the maximum flow deflection is a function of the solidity and Reynolds number
'''
Process :
1. Select solidity sigma = (s/c)^-1, get Psi(sigma)
2. Assume Re, get Phi(Re)
3. Given outflow angle Beta_2, get f_epsilon(Beta_2)
4. Compute |delta_Beta|*
5.  If |delta_Beta| <= |delta_Beta|* ; |delta_Beta| = |Beta_2 - Beta_1| = absolute flow deflection
        All good, move on with design
    Else
        reselect sigma such that the If check passes
'''


import pandas as pd
from scipy.interpolate import CubicSpline

# 1. Load the data extracted from WebPlotDigitizer
# Assuming your CSV has no header and two columns: X, Y
f_beta = pd.read_csv('Howell/Howell_f_beta2.csv', header=None, names=['Beta2', 'f'])
Phi_Re = pd.read_csv('Howell/Howell_Phi_Re.csv', header=None, names=['Re', 'Phi'])
Phi_Re['Re'] = Phi_Re['Re'] * 1e5 #scale Re by 10^5
Psi_sigmaInverse = pd.read_csv('Howell/Howell_Psi_solidityINVERSE.csv', header=None, names=['sigmaInverse', 'Psi'])

# Sort the data by X just in case the points were clicked out of order
f_beta = f_beta.sort_values(by='Beta2')
Phi_Re = Phi_Re.sort_values(by='Re')
Psi_sigmaInverse = Psi_sigmaInverse.sort_values(by='sigmaInverse')

# 2. Create the function using Cubic Spline Interpolation
# This creates a smooth curve through your points
f_function = CubicSpline(f_beta['Beta2'], f_beta['f'])
Phi_function = CubicSpline(Phi_Re['Re'], Phi_Re['Phi'])
Psi_function = CubicSpline(Psi_sigmaInverse['sigmaInverse'], Psi_sigmaInverse['Psi'])


def Howell_Loading_Criterion (sigma , Re , Beta_2 , Beta_1):
    '''
    Returns True if the Loading Criterion is met, False otherwise
    '''
    Psi = Psi_function(1/sigma)
    Phi = Phi_function(Re)
    f_epsilon = f_function(Beta_2)

    Delta_Beta_Star = Psi * Phi * f_epsilon
    Delta_Beta = abs(Beta_2- Beta_1)

    if(Delta_Beta <= Delta_Beta_Star):
        return True
    else:
        return False

