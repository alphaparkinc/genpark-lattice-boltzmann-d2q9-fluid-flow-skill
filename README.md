# genpark-lattice-boltzmann-d2q9-fluid-flow-skill

Agent Skill implementing the **D2Q9 Lattice Boltzmann Method (LBM)** with BGK relaxation collision operator and bounce-back obstacle boundary conditions.

## Architectural Overview
```mermaid
flowchart TD
    Macro["Macroscopic Variables (Rho, u)"] --> Eq["Equilibrium Distribution f_i^(eq)"]
    Eq --> Collide["BGK Collision: f_i* = f_i - (f_i - f_eq)/tau"]
    Collide --> Stream["Lattice Streaming to 9 Neighbor Cells"]
    Stream --> Bounce["Bounce-Back at Obstacle Walls"]
    Bounce --> Macro
```
