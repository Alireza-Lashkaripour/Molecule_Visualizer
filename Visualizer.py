import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Element_infos import ElementInfo

class GeometryVisualizer:
    def __init__(self):
        self.element_info = ElementInfo()

    def visualize_geometry(self, geometry, title="Molecular Geometry"):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        x_vals = []
        y_vals = []
        z_vals = []
        labels = []

        for atom in geometry:
            x_vals.append(atom['x'])
            y_vals.append(atom['y'])
            z_vals.append(atom['z'])
            labels.append(atom['symbol'])

            ax.scatter(atom['x'], atom['y'], atom['z'], s=100, alpha=0.6)

        for i in range(len(x_vals)):
            ax.text(x_vals[i], y_vals[i], z_vals[i], labels[i], size=12, zorder=1, color='k')

        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_zlabel('Z Coordinate')
        ax.set_title(title)

        plt.show()

    def save_visualization(self, geometry, file_name="geometry_visualization.png", title="Molecular Geometry"):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        x_vals = []
        y_vals = []
        z_vals = []
        labels = []

        for atom in geometry:
            x_vals.append(atom['x'])
            y_vals.append(atom['y'])
            z_vals.append(atom['z'])
            labels.append(atom['symbol'])

            ax.scatter(atom['x'], atom['y'], atom['z'], s=100, alpha=0.6)

        for i in range(len(x_vals)):
            ax.text(x_vals[i], y_vals[i], z_vals[i], labels[i], size=12, zorder=1, color='k')

        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_zlabel('Z Coordinate')
        ax.set_title(title)

        plt.savefig(file_name)
        print(f"Visualization saved to {file_name}")

