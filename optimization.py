import numpy as np

class GeometryOptimizer:
    def __init__(self, geometry):
        self.geometry = geometry

    def calculate_bond_length(self, atom1, atom2):
        return np.linalg.norm(np.array([atom1['x'], atom1['y'], atom1['z']]) - np.array([atom2['x'], atom2['y'], atom2['z']]))

    def calculate_bond_angle(self, atom1, atom2, atom3):
        vec1 = np.array([atom1['x'] - atom2['x'], atom1['y'] - atom2['y'], atom1['z'] - atom2['z']])
        vec2 = np.array([atom3['x'] - atom2['x'], atom3['y'] - atom2['y'], atom3['z'] - atom2['z']])
        cos_theta = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        return np.arccos(np.clip(cos_theta, -1.0, 1.0))

    def calculate_energy(self):
        energy = 0
        bond_constant = 1.0
        angle_constant = 0.5
        ideal_bond_angle = np.pi / 2  
        
        # Bond stretching energy
        for i in range(len(self.geometry)):
            for j in range(i + 1, len(self.geometry)):
                bond_length = self.calculate_bond_length(self.geometry[i], self.geometry[j])
                r0 = self.get_ideal_bond_length(self.geometry[i]['symbol'], self.geometry[j]['symbol'])
                energy += 0.5 * bond_constant * (bond_length - r0) ** 2
        
        # Angle bending energy
        for i in range(len(self.geometry)):
            for j in range(i + 1, len(self.geometry)):
                for k in range(j + 1, len(self.geometry)):
                    angle = self.calculate_bond_angle(self.geometry[i], self.geometry[j], self.geometry[k])
                    energy += 0.5 * angle_constant * (angle - ideal_bond_angle) ** 2
        
        return energy

    def optimize(self, learning_rate=0.001, max_steps=1000):
        for step in range(max_steps):
            forces = self.calculate_forces()
            for i, atom in enumerate(self.geometry):
                atom['x'] -= learning_rate * forces[i][0]
                atom['y'] -= learning_rate * forces[i][1]
                atom['z'] -= learning_rate * forces[i][2]

            if step % 100 == 0:
                print(f"Step {step}, Energy: {self.calculate_energy()}")
        return self.geometry

    def calculate_forces(self):
        forces = []
        bond_constant = 1.0
        for i in range(len(self.geometry)):
            force = np.zeros(3)
            for j in range(len(self.geometry)):
                if i != j:
                    bond_length = self.calculate_bond_length(self.geometry[i], self.geometry[j])
                    r0 = self.get_ideal_bond_length(self.geometry[i]['symbol'], self.geometry[j]['symbol'])
                    bond_vector = np.array([self.geometry[i]['x'] - self.geometry[j]['x'],
                                            self.geometry[i]['y'] - self.geometry[j]['y'],
                                            self.geometry[i]['z'] - self.geometry[j]['z']])
                    force += bond_constant * (bond_length - r0) * bond_vector / bond_length
            forces.append(force)
        return forces

    def get_ideal_bond_length(self, atom1_symbol, atom2_symbol):
        bond_lengths = {
            ('C', 'C'): 1.54,
            ('C', 'H'): 1.09,
            ('N', 'N'): 1.45,
            ('C', 'N'): 1.47,
            ('N', 'H'): 1.01,
            ('H', 'H'): 0.74
        }
        return bond_lengths.get((atom1_symbol, atom2_symbol), 1.5)  
