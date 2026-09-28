from client import LatticeBoltzmannD2Q9

lbm = LatticeBoltzmannD2Q9(nx=16, ny=8, tau=0.8)
lbm.set_cylinder_obstacle(cx=4, cy=4, radius=2)
rho, ux, uy = lbm.step()

print("D2Q9 Lattice Boltzmann Step Completed.")
print(f"Grid: 16x8 | Center Density at (8, 4): {rho[8][4]:.4f}")
