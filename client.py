"""D2Q9 Lattice Boltzmann Method (LBM) Fluid Flow Engine.
100% Python Standard Library.
"""

class LatticeBoltzmannD2Q9:
    """D2Q9 Lattice Boltzmann BGK fluid flow simulation."""
    def __init__(self, nx=20, ny=10, tau=0.8):
        self.nx = nx
        self.ny = ny
        self.tau = tau
        self.c = [
            (0, 0), (1, 0), (0, 1), (-1, 0), (0, -1),
            (1, 1), (-1, 1), (-1, -1), (1, -1)
        ]
        self.w = [4/9] + [1/9]*4 + [1/36]*4
        self.f = [[[self.w[i] for i in range(9)] for _ in range(ny)] for _ in range(nx)]
        self.solid = [[False]*ny for _ in range(nx)]

    def set_cylinder_obstacle(self, cx, cy, radius):
        for x in range(self.nx):
            for y in range(self.ny):
                if (x - cx)**2 + (y - cy)**2 <= radius**2:
                    self.solid[x][y] = True

    def step(self):
        nx, ny = self.nx, self.ny
        rho = [[0.0]*ny for _ in range(nx)]
        ux = [[0.0]*ny for _ in range(nx)]
        uy = [[0.0]*ny for _ in range(nx)]

        for x in range(nx):
            for y in range(ny):
                if self.solid[x][y]:
                    continue
                r = sum(self.f[x][y])
                rho[x][y] = r
                if r > 1e-12:
                    mx = sum(self.f[x][y][i] * self.c[i][0] for i in range(9))
                    my = sum(self.f[x][y][i] * self.c[i][1] for i in range(9))
                    ux[x][y] = mx / r
                    uy[x][y] = my / r

        f_star = [[[0.0]*9 for _ in range(ny)] for _ in range(nx)]
        for x in range(nx):
            for y in range(ny):
                if self.solid[x][y]:
                    continue
                u2 = ux[x][y]**2 + uy[x][y]**2
                for i in range(9):
                    ci_u = self.c[i][0]*ux[x][y] + self.c[i][1]*uy[x][y]
                    feq = self.w[i] * rho[x][y] * (1.0 + 3.0*ci_u + 4.5*(ci_u**2) - 1.5*u2)
                    f_star[x][y][i] = self.f[x][y][i] - (self.f[x][y][i] - feq) / self.tau

        opp = [0, 3, 4, 1, 2, 7, 8, 5, 6]
        new_f = [[[self.w[i] for i in range(9)] for _ in range(ny)] for _ in range(nx)]
        for x in range(nx):
            for y in range(ny):
                if self.solid[x][y]:
                    continue
                for i in range(9):
                    nx_pos = (x + self.c[i][0]) % nx
                    ny_pos = (y + self.c[i][1]) % ny
                    if self.solid[nx_pos][ny_pos]:
                        new_f[x][y][opp[i]] = f_star[x][y][i]
                    else:
                        new_f[nx_pos][ny_pos][i] = f_star[x][y][i]
        self.f = new_f
        return rho, ux, uy
