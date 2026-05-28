"""
Laser Light Propagation in Optical Fibers
==========================================
This simulation shows how light travels through an optical fiber using the principle of Total Internal Reflection (TIR).

Key Concepts:
- Optical fibers have two layers: Core (inner) and Cladding (outer)
- Core has a higher refractive index than Cladding
- When light hits the core-cladding boundary at a shallow enough angle, it reflects completely back into the core — this is called TIR
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
FIBER_LENGTH = 10.0   # Length of the fiber (arbitrary units)
CORE_RADIUS  = 1.0    # Radius of the inner core
CLAD_RADIUS  = 1.5    # Radius of the outer cladding

N_CORE = 1.5          # Refractive index of core (e.g. glass)
N_CLAD = 1.45         # Refractive index of cladding (slightly lower — this is key!)

# Critical angle: light hitting the boundary beyond this angle will be totally reflected
critical_angle_rad = np.arcsin(N_CLAD / N_CORE)
critical_angle_deg = np.degrees(critical_angle_rad)
print(f"Critical angle for Total Internal Reflection: {critical_angle_deg:.2f}°")


# ── Ray Tracing Function ────────────────────────────────────────────────────
def trace_ray(entry_angle_deg, num_bounces=30):
    """
    Trace a single light ray as it bounces through the fiber.

    Parameters:
        entry_angle_deg : angle at which the ray enters the fiber (degrees)
                          measured from the fiber axis (horizontal)
        num_bounces     : maximum number of reflections to simulate

    Returns:
        x_points, y_points : coordinates of the ray path
    """
    angle_rad = np.radians(entry_angle_deg)

    x, y   = 0.0, 0.0
    dx, dy = np.cos(angle_rad), np.sin(angle_rad)

    x_points = [x]
    y_points  = [y]

    for _ in range(num_bounces):
        if dy == 0:
            break  # perfectly horizontal ray — no bouncing

        # Distance to top or bottom core wall
        if dy > 0:
            t = (CORE_RADIUS - y) / dy
        else:
            t = (-CORE_RADIUS - y) / dy

        x_new = x + t * dx
        y_new = y + t * dy

        # Stop if ray has passed the end of the fiber
        if x_new >= FIBER_LENGTH:
            x_points.append(FIBER_LENGTH)
            y_points.append(y + (FIBER_LENGTH - x) / dx * dy)
            break

        # Angle of incidence at the wall (measured from the normal)
        angle_of_incidence = np.degrees(np.arctan2(abs(dx), abs(dy)))

        if angle_of_incidence >= critical_angle_deg:
            dy = -dy   # TIR: bounce back
        else:
            # Ray escapes the core (light loss)
            x_points.append(x_new)
            y_points.append(y_new)
            break

        x, y = x_new, y_new
        x_points.append(x)
        y_points.append(y)

    return x_points, y_points


# ── User Input ──────────────────────────────────────────────────────────────
print(f"\nEnter 3 angles to simulate (in degrees, 1–89).")
print(f"Hint: angles below {critical_angle_deg:.1f}° stay inside the fiber; above will escape.\n")

colors   = ["red", "orange", "purple"]
scenarios = []

for i, color in enumerate(colors, start=1):
    while True:
        try:
            angle = float(input(f"  Enter angle {i}: "))
            if 1 <= angle <= 89:
                if angle < critical_angle_deg:
                    label = f"{angle}° — stays inside (TIR)"
                else:
                    label = f"{angle}° — escapes (no TIR)"
                scenarios.append({"angle": angle, "color": color, "label": label})
                break
            else:
                print("  Please enter a value between 1 and 89.")
        except ValueError:
            print("  Invalid input. Please enter a number.")


# ── Plotting ────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(3, 1, figsize=(12, 10))
fig.suptitle("Laser Light Propagation in an Optical Fiber", fontsize=14, fontweight='bold')

for ax, scenario in zip(axes, scenarios):
    angle = scenario["angle"]
    color = scenario["color"]
    label = scenario["label"]

    # Draw cladding (grey band)
    cladding_top    = patches.Rectangle((0,  CORE_RADIUS), FIBER_LENGTH, CLAD_RADIUS - CORE_RADIUS, color='lightgrey', label='Cladding')
    cladding_bottom = patches.Rectangle((0, -CLAD_RADIUS), FIBER_LENGTH, CLAD_RADIUS - CORE_RADIUS, color='lightgrey')
    ax.add_patch(cladding_top)
    ax.add_patch(cladding_bottom)

    # Draw core (light blue band)
    core = patches.Rectangle((0, -CORE_RADIUS), FIBER_LENGTH, 2 * CORE_RADIUS, color='lightblue', alpha=0.5, label='Core')
    ax.add_patch(core)

    # Draw core boundary lines
    ax.axhline( CORE_RADIUS, color='blue', linewidth=1, linestyle='--', alpha=0.5)
    ax.axhline(-CORE_RADIUS, color='blue', linewidth=1, linestyle='--', alpha=0.5)

    # Trace and draw the ray
    xs, ys = trace_ray(angle)
    ax.plot(xs, ys, color=color, linewidth=2, label=f"Ray at {label}")

    ax.set_xlim(0, FIBER_LENGTH)
    ax.set_ylim(-CLAD_RADIUS - 0.2, CLAD_RADIUS + 0.2)
    ax.set_ylabel("Position (cross-section)")
    ax.legend(loc='upper right', fontsize=9)
    ax.set_title(f"Entry angle: {angle}°  |  Critical angle: {critical_angle_deg:.1f}°", fontsize=10)
    ax.set_yticks([])

axes[-1].set_xlabel("Fiber Length →")

plt.tight_layout()
plt.savefig("optical_fiber_simulation.png", dpi=150, bbox_inches='tight')
plt.show()
print("\nPlot saved as 'optical_fiber_simulation.png'")

# ── Summary ──────────────────────────────────────────────────────────────────
print("\n── Physics Summary ──────────────────────────────────────────────────")
print(f"  Core refractive index    : {N_CORE}")
print(f"  Cladding refractive index: {N_CLAD}")
print(f"  Critical angle (TIR)     : {critical_angle_deg:.2f}°")
print()
print("  Rays below the critical angle bounce and travel the full fiber.")
print("  Rays above the critical angle escape through the cladding.")
