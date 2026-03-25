import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Initial duty coefficients
phi_init = 0.5  # Flow coefficient (Cx/U)
psi_init = 0.4  # Work coefficient (ΔCy/U)
R_init = 0.5    # Degree of reaction

# Setup the figure and axis
fig, ax = plt.subplots(figsize=(8, 6))
plt.subplots_adjust(bottom=0.35)
ax.set_aspect('equal')
ax.set_xlim(-1.0, 2.5)
ax.set_ylim(0, 1.5)
ax.set_title("Axial Stage Velocity Triangles (Non-dimensionalized, U=1)")
ax.set_xlabel("Tangential Velocity (Cy/U)")
ax.set_ylabel("Axial Velocity (Cx/U)")
ax.grid(True, linestyle='--', alpha=0.6)

# U vector (constant)
ax.plot([0, 1], [0, 0], 'k-', lw=3, label='U (Blade Speed)')

# Helper to calculate tangential velocities
def calc_cy(phi, psi, R):
    cy1 = 1 - R - psi / 2
    cy2 = 1 - R + psi / 2
    return cy1, cy2

# Draw initial triangles
cy1, cy2 = calc_cy(phi_init, psi_init, R_init)
C1_line, = ax.plot([0, cy1], [0, phi_init], 'b-', lw=2, label='C1 (Absolute Inlet)')
W1_line, = ax.plot([1, cy1], [0, phi_init], 'c-', lw=2, label='W1 (Relative Inlet)')
C2_line, = ax.plot([0, cy2], [0, phi_init], 'r-', lw=2, label='C2 (Absolute Outlet)')
W2_line, = ax.plot([1, cy2], [0, phi_init], 'm-', lw=2, label='W2 (Relative Outlet)')

ax.legend(loc='upper right', fontsize='small')

# Setup sliders
ax_phi = plt.axes([0.15, 0.2, 0.7, 0.03])
ax_psi = plt.axes([0.15, 0.15, 0.7, 0.03])
ax_R   = plt.axes([0.15, 0.1, 0.7, 0.03])

s_phi = Slider(ax_phi, r'$\phi$ (Flow)', 0.1, 1.5, valinit=phi_init)
s_psi = Slider(ax_psi, r'$\psi$ (Work)', 0.1, 1.5, valinit=psi_init)
s_R   = Slider(ax_R, r'$R$ (Reaction)', 0.0, 1.0, valinit=R_init)

# Update function for the sliders
def update(val):
    phi = s_phi.val
    psi = s_psi.val
    R = s_R.val
    
    cy1, cy2 = calc_cy(phi, psi, R)
    
    C1_line.set_data([0, cy1], [0, phi])
    W1_line.set_data([1, cy1], [0, phi])
    C2_line.set_data([0, cy2], [0, phi])
    W2_line.set_data([1, cy2], [0, phi])
    
    # Dynamically scale axes if needed
    ax.set_ylim(0, max(1.5, phi + 0.2))
    ax.set_xlim(min(-1.0, cy1-0.2, cy2-0.2), max(2.5, cy1+0.2, cy2+0.2))
    
    fig.canvas.draw_idle()

s_phi.on_changed(update)
s_psi.on_changed(update)
s_R.on_changed(update)

plt.show()