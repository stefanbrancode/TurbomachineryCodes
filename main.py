from Compressor import (
    get_compressor_angles,
    plot_velocity_triangles,
    calculate_recovery_factor,
    get_optimal_psi,
    calculate_diffusion_factor,
    get_solidity_from_DF
)

#Example problem 
Phi , R = 0.5 ,0.5
Psi = get_optimal_psi(Phi)
print("Psi =" , Psi)

# Get angles for velocity triangles
angles = get_compressor_angles(R, Psi, Phi)
alpha1, alpha2, beta1, beta2 = angles['alpha1'], angles['alpha2'], angles["beta1"] , angles['beta2']
print(angles)

#plot triangles
#plot_velocity_triangles(alpha1, alpha2, beta1, beta2)

#Choose Diffusion factor 
DF =0.45

#Get solidity from Inverted diffusion Factor equation
sigma = get_solidity_from_DF(DF, alpha2 , alpha1)
print("sigma= ",sigma)

#calculate recovery factor
rr_value = calculate_recovery_factor(alpha1, beta2, Phi)
print(f"Recovery Factor: {rr_value}")

#TODO:USE LieBlein loading factor!!
#incidence should be 3-5 deg, 20 is crazy, 0 is crazy. (negative incidence makes the compressor unstable.)
#how to get efficiency? total-total, look at smith charts.
#before doing CFD, you need to know if ANY part of the blade is in chocked condition. What is the criterion?(Slide 52 Lecture 6 axial compressor, "Inlet Control Volume Analysis")
#The design point should be in the middle of the speedline. The speedline should be chosen thrugh preliminary design such that the Design point(decided by the massflowrate) is in the mid of the speedline.
#Thin airfoil => mechanical failure through dynamic excitations
#Check velocity traingle at the tip. (M1 at the tip will be larger than one in the project)
#incidence angle is computed through the Lip-Line model.
#if M2<1 unstarted regime, bowshock in front.

#Minute 68-70 of lecture 007, matteo talks about choice of degree of reaction in Fan Design
#Extra Criteria for compressor design(compared to turbine)= Stability. If the design of the compressor is unstable, then the CFD will not coverge. 
#Malton softare gives low number of blades due to using the Zwifel criterion under the hood. You should use  Lieblin criterion and diffusion factor. You need to correct the number after doing CFD.

#Multall notes