import numpy as np


def get_optimal_psi(phi):
    '''
    calculates optimal Load Coefficient (Psi), given Flow Coefficient (Phi). 

    Theoretical trend predicted by Lewis (based on data of Casey)
    '''

    Psi_opt = 0.185*np.sqrt(4*phi*phi +1)

    return Psi_opt

def get_Max_psi(phi):
    '''
    estimates trend of maximum load coefficient Psi_max

    The admissable design range lies between Psi_opt and Psi_max

    '''
    Psi_max = 0.32 + 0.2*phi

    return Psi_max

