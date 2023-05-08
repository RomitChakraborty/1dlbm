class LatticeBoltzmannSolver:
    def __init__(self, nx, nt, omega, dx=1.0, dt=1.0):
        self.nx = nx      # Number of lattice sites in the x-direction
        self.nt = nt      # Number of time steps to evolve the system
        self.omega = omega   # Relaxation parameter
        self.dx = dx      # Lattice spacing in the x-direction
        self.dt = dt      # Time step size
        
        self.f = np.zeros((3, nx))  # Distribution functions for each velocity direction
        self.rho = np.ones(nx)      # Density of the gas at each lattice site
        self.u = np.zeros(nx)       # Velocity of the gas at each lattice site
        self.epsilon = np.zeros(nx) # Binding energy at each lattice site
        
        # Set up the velocity vectors
        self.c = np.array([0, 1, -1])     # Velocity vectors
        self.w = np.array([1/3, 1/6, 1/6]) # Weights of each velocity vector
        
    def equilibrium_distribution(self):
        """
        Computes the equilibrium distribution function f_eq for the current state of the system
        """
        u_eq = np.zeros((3, self.nx))
        f_eq = np.zeros((3, self.nx))
        
        for i in range(3):
            u_eq[i, :] = self.u + self.c[i]
            f_eq[i, :] = self.w[i] * self.rho * (1 + 3*u_eq[i,:] + 9/2*u_eq[i,:]**2 - 3/2*self.u**2) * np.exp(self.epsilon)
            
        return f_eq
        
    def collision(self):
        """
        Performs a single collision step for the system
        """
        f_eq = self.equilibrium_distribution()
        for i in range(3):
            self.f[i, :] = (1 - self.omega) * self.f[i, :] + self.omega * f_eq[i, :]
            
    def streaming(self):
        """
        Performs a single streaming step for the system
        """
        for i in range(1, self.nx):
            self.f[1, i] = self.f[1, i-1]
        for i in range(self.nx-2, -1, -1):
            self.f[2, i] = self.f[2, i+1]
            
    def update_density_velocity(self):
        """
        Updates the density and velocity of the gas based on the distribution functions
        """
        self.rho = np.sum(self.f, axis=0)
        self.u = (self.f[1, :] - self.f[2, :]) / self.rho
        
    def set_epsilon(self, epsilon):
        """
        Sets the binding energy at each lattice site
        """
        self.epsilon = epsilon
        
    def evolve(self):
        """
        Evolves the system for nt time steps
        """
        for n in range(self.nt):
            self.collision()
            self.streaming()
            self.update_density_velocity()
