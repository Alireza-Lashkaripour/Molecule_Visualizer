import tkinter as tk
from tkinter import ttk
import numpy as np
from optimization import GeometryOptimizer

class AdvancedOptions:
    def __init__(self, root, visualizer_app):
        self.root = root
        self.visualizer_app = visualizer_app
        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=2, padx=10, pady=10)
        self.create_rotation_controls()
        self.create_color_customization()
        self.create_bond_length_display()
        self.create_export_options()
        self.create_optimization_controls()

    def create_rotation_controls(self):
        rotation_label = ttk.Label(self.frame, text="Rotation Controls")
        rotation_label.grid(row=0, column=0, columnspan=2)
        ttk.Button(self.frame, text="Rotate X", command=lambda: self.rotate_molecule('x')).grid(row=1, column=0)
        ttk.Button(self.frame, text="Rotate Y", command=lambda: self.rotate_molecule('y')).grid(row=1, column=1)
        ttk.Button(self.frame, text="Rotate Z", command=lambda: self.rotate_molecule('z')).grid(row=2, column=0)

    def rotate_molecule(self, axis):
        if axis == 'x':
            self.visualizer_app.ax.view_init(elev=self.visualizer_app.ax.elev + 10, azim=self.visualizer_app.ax.azim)
        elif axis == 'y':
            self.visualizer_app.ax.view_init(elev=self.visualizer_app.ax.elev, azim=self.visualizer_app.ax.azim + 10)
        elif axis == 'z':
            self.visualizer_app.ax.view_init(elev=self.visualizer_app.ax.elev - 10, azim=self.visualizer_app.ax.azim)
        self.visualizer_app.canvas.draw()

    def create_color_customization(self):
        color_label = ttk.Label(self.frame, text="Atom Color Customization")
        color_label.grid(row=3, column=0, columnspan=2)
        self.color_var = tk.StringVar()
        color_options = ['By Element', 'Custom']
        self.color_dropdown = ttk.OptionMenu(self.frame, self.color_var, color_options[0], *color_options)
        self.color_dropdown.grid(row=4, column=0, columnspan=2)
        ttk.Button(self.frame, text="Apply Color", command=self.apply_color_customization).grid(row=5, column=0, columnspan=2)

    def apply_color_customization(self):
        color_option = self.color_var.get()
        if color_option == "By Element":
            colors = {
                'H': 'white', 'C': 'black', 'O': 'red', 'N': 'blue'
            }
            for atom in self.visualizer_app.geometry:
                color = colors.get(atom['symbol'], 'gray')
                self.visualizer_app.ax.scatter(atom['x'], atom['y'], atom['z'], color=color, s=100)
        elif color_option == "Custom":
            custom_color = 'yellow'
            for atom in self.visualizer_app.geometry:
                self.visualizer_app.ax.scatter(atom['x'], atom['y'], atom['z'], color=custom_color, s=100)
        self.visualizer_app.canvas.draw()

    def create_bond_length_display(self):
        ttk.Button(self.frame, text="Display Bond Lengths", command=self.display_bond_lengths).grid(row=6, column=0, columnspan=2)

    def display_bond_lengths(self):
        bond_thresholds = {
            "single": 1.6, "double": 1.3, "triple": 1.2
        }
        atoms = np.array([[atom['x'], atom['y'], atom['z']] for atom in self.visualizer_app.geometry])
        for i in range(len(atoms)):
            for j in range(i + 1, len(atoms)):
                distance = np.linalg.norm(atoms[i] - atoms[j])
                if distance <= bond_thresholds["single"]:
                    x, y, z = (atoms[i] + atoms[j]) / 2
                    self.visualizer_app.ax.text(x, y, z, f"{distance:.2f}", color='black', fontsize=10)
        self.visualizer_app.canvas.draw()

    def create_export_options(self):
        export_label = ttk.Label(self.frame, text="Export Options")
        export_label.grid(row=7, column=0, columnspan=2)
        ttk.Button(self.frame, text="Export Image", command=self.export_image).grid(row=8, column=0)
        ttk.Button(self.frame, text="Save Geometry", command=self.save_geometry).grid(row=8, column=1)

    def export_image(self):
        image_filename = f'{self.visualizer_app.output_filename_entry.get()}_visualization.png'
        self.visualizer_app.fig.savefig(image_filename)

    def save_geometry(self):
        output_file = self.visualizer_app.output_filename_entry.get()
        output_format = self.visualizer_app.output_format_var.get()
        output_unit = self.visualizer_app.output_unit_var.get()
        self.visualizer_app.reader_converter.save_converted_geometry(self.visualizer_app.geometry, output_format, output_file, output_unit)

    def create_optimization_controls(self):
        optimization_label = ttk.Label(self.frame, text="Geometry Optimization")
        optimization_label.grid(row=9, column=0, columnspan=2)
        self.method_var = tk.StringVar()
        methods = ['Simple MM Optimization']
        self.method_dropdown = ttk.OptionMenu(self.frame, self.method_var, methods[0], *methods)
        self.method_dropdown.grid(row=10, column=0, columnspan=2)
        ttk.Button(self.frame, text="Optimize Geometry", command=self.optimize_geometry).grid(row=11, column=0, columnspan=2)

    def optimize_geometry(self):
        optimizer = GeometryOptimizer(self.visualizer_app.geometry)
        optimized_geometry = optimizer.optimize()
        self.visualizer_app.geometry = optimized_geometry
        self.visualizer_app.ax.clear()
        self.visualizer_app.visualize_with_bonds(self.visualizer_app.geometry)
        self.visualizer_app.canvas.draw()
