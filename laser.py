"""
Laser Light Propagation in Optical Fibers
==========================================
This simulation shows how light travels through an optical fiber
using the principle of Total Internal Reflection (TIR).

Key Concepts:
- Optical fibers have two layers: Core (inner) and Cladding (outer)
- Core has a higher refractive index than Cladding
- When light hits the core-cladding boundary at a shallow enough angle,
  it reflects completely back into the core — this is called TIR
- Light "bounces" its way from one end of the fiber to the other

THINGS THAT CAN BE CHANGED:
- Refractive indices of core and cladding (N_CORE, N_CLAD)
- Entry angle of the light ray (entry_angle_deg)
- Increase num_bounces for longer fiber simulations  
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ── Fiber & Light Parameters ────────────────────────────────────────────────
FIBER_LENGTH   = 10.0   # Length of the fiber (arbitrary units)
CORE_RADIUS    = 1.0    # Radius of the inner core
CLAD_RADIUS    = 1.5    # Radius of the outer cladding

N_CORE = 3            # Refractive index of core (e.g. glass)
N_CLAD = 1.45           # Refractive index of cladding (slightly lower — this is key!)

# Snell's Law at the core-cladding interface tells us the critical angle.
# Light hitting the boundary at angles GREATER than this will be totally reflected.
critical_angle_rad = np.arcsin(N_CLAD / N_CORE)
critical_angle_deg = np.degrees(critical_angle_rad)
print(f"Critical angle for Total Internal Reflection: {critical_angle_deg:.2f}°")


# ── Ray Tracing Function ────────────────────────────────────────────────────
def trace_ray(entry_angle_deg, num_bounces=30):
    """
    Trace a single light ray as it bounces through the fiber.

    Parameters:
        entry_angle_deg : angle at which the ray enters the fiber (in degrees)
                          measured from the fiber axis (horizontal)
        num_bounces     : maximum number of reflections to simulate

    Returns:
        x_points, y_points : lists of coordinates of the ray path
    """
    angle_rad = np.radians(entry_angle_deg)

    x, y  = 0.0, 0.0        # starting position (left end of fiber)
    dx, dy = np.cos(angle_rad), np.sin(angle_rad)   # direction vector

    x_points = [x]
    y_points  = [y]

    for _ in range(num_bounces):
        # Figure out how far the ray travels before hitting the core wall
        if dy == 0:
            break  # ray is perfectly horizontal — no bouncing

        # Distance to the top (+CORE_RADIUS) or bottom (-CORE_RADIUS) wall
        if dy > 0:
            t = (CORE_RADIUS - y) / dy    # heading upward
        else:
            t = (-CORE_RADIUS - y) / dy   # heading downward

        # Next position after travelling distance t
        x_new = x + t * dx
        y_new = y + t * dy

        # Stop if ray has exited the fiber length
        if x_new >= FIBER_LENGTH:
            x_points.append(FIBER_LENGTH)
            y_points.append(y + (FIBER_LENGTH - x) / dx * dy)
            break

        # Check if Total Internal Reflection happens here
        # Angle of incidence is measured from the NORMAL to the wall (vertical)
        angle_of_incidence = np.degrees(np.arctan2(abs(dx), abs(dy)))
        if angle_of_incidence >= critical_angle_deg:
            # TIR: ray bounces back, y-direction flips
            dy = -dy
        else:
            # Ray escapes the core (light loss — like a damaged fiber)
            x_points.append(x_new)
            y_points.append(y_new)
            break

        x, y = x_new, y_new
        x_points.append(x)
        y_points.append(y)

    return x_points, y_points


# ── Plotting ────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(3, 1, figsize=(12, 10))
fig.suptitle("Laser Light Propagation in an Optical Fiber", fontsize=14, fontweight='bold')

scenarios = [
    {"angle": 5,  "color": "red",    "label": "5° — stays inside (TIR)"},
    {"angle": 10, "color": "orange", "label": "10° — stays inside (TIR)"},
    {"angle": 30, "color": "purple", "label": "30° — escapes (no TIR)"},
]

for ax, scenario in zip(axes, scenarios):
    angle = scenario["angle"]
    color = scenario["color"]
    label = scenario["label"]

    # Draw the cladding layer (grey band)
    cladding_top    = patches.Rectangle((0,  CORE_RADIUS),  FIBER_LENGTH, CLAD_RADIUS - CORE_RADIUS, color='lightgrey', label='Cladding')
    cladding_bottom = patches.Rectangle((0, -CLAD_RADIUS),  FIBER_LENGTH, CLAD_RADIUS - CORE_RADIUS, color='lightgrey')
    ax.add_patch(cladding_top)
    ax.add_patch(cladding_bottom)

    # Draw the core (light blue band)
    core = patches.Rectangle((0, -CORE_RADIUS), FIBER_LENGTH, 2 * CORE_RADIUS, color='lightblue', alpha=0.5, label='Core')
    ax.add_patch(core)

    # Draw the core boundary lines
    ax.axhline( CORE_RADIUS, color='blue', linewidth=1, linestyle='--', alpha=0.5)
    ax.axhline(-CORE_RADIUS, color='blue', linewidth=1, linestyle='--', alpha=0.5)

    # Trace and draw the ray
    xs, ys = trace_ray(angle)
    ax.plot(xs, ys, color=color, linewidth=2, label=f"Ray at {label}")

    # Labels and formatting
    ax.set_xlim(0, FIBER_LENGTH)
    ax.set_ylim(-CLAD_RADIUS - 0.2, CLAD_RADIUS + 0.2)
    ax.set_ylabel("Position (cross-section)")
    ax.legend(loc='upper right', fontsize=9)
    ax.set_title(f"Entry angle: {angle}°  |  Critical angle: {critical_angle_deg:.1f}°", fontsize=10)
    ax.set_yticks([])   # hide y-axis numbers for clarity

axes[-1].set_xlabel("Fiber Length →")

plt.tight_layout()
plt.savefig("optical_fiber_simulation.png", dpi=150, bbox_inches='tight')
plt.show()
print("\nPlot saved as 'optical_fiber_simulation.png' in the current folder")


# ── Summary of Physics ───────────────────────────────────────────────────────
print("\n── Physics Summary ─────────────────────────────────────────────────")
print(f"  Core refractive index    : {N_CORE}")
print(f"  Cladding refractive index: {N_CLAD}")
print(f"  Critical angle (TIR)     : {critical_angle_deg:.2f}°")
print()
print("  Rays entering at angles LESS than the critical angle bounce")
print("  repeatedly and travel the full length of the fiber.")
print()
print("  Rays entering at angles GREATER than the critical angle")
print("  escape through the cladding and are lost.")