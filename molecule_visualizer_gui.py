import tkinter as tk
from tkinter import filedialog, ttk
from Reader_and_convertor import GeometryReaderAndConverter
from Visualizer import GeometryVisualizer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class MoleculeVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Molecule Visualizer and Converter")

        self.reader_converter = GeometryReaderAndConverter()
        self.visualizer = GeometryVisualizer()

        # Input Section
        self.input_label = ttk.Label(root, text="Input Geometry", padding=10)
        self.input_label.grid(row=0, column=0, columnspan=2)

        self.geometry_textbox = tk.Text(root, height=10, width=50)
        self.geometry_textbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.input_format_label = ttk.Label(root, text="Input Format (GAMESS or XYZ)", padding=5)
        self.input_format_label.grid(row=2, column=0)
        self.input_format_var = tk.StringVar(root)
        self.input_format_dropdown = ttk.OptionMenu(root, self.input_format_var, "gamess", "gamess", "xyz")
        self.input_format_dropdown.grid(row=2, column=1, padx=5)

        self.input_unit_label = ttk.Label(root, text="Input Unit (Angstrom or Bohr)", padding=5)
        self.input_unit_label.grid(row=3, column=0)
        self.input_unit_var = tk.StringVar(root)
        self.input_unit_dropdown = ttk.OptionMenu(root, self.input_unit_var, "bohr", "bohr", "angstrom")
        self.input_unit_dropdown.grid(row=3, column=1, padx=5)

        self.load_button = ttk.Button(root, text="Load Geometry from File", command=self.load_geometry_file)
        self.load_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Output Section
        self.output_label = ttk.Label(root, text="Output Settings", padding=10)
        self.output_label.grid(row=5, column=0, columnspan=2)

        self.output_filename_entry = ttk.Entry(root, width=30)
        self.output_filename_entry.grid(row=6, column=1, padx=5)
        self.output_filename_label = ttk.Label(root, text="Output File Name", padding=5)
        self.output_filename_label.grid(row=6, column=0)

        self.output_format_label = ttk.Label(root, text="Output Format (GAMESS or XYZ)", padding=5)
        self.output_format_label.grid(row=7, column=0)
        self.output_format_var = tk.StringVar(root)
        self.output_format_dropdown = ttk.OptionMenu(root, self.output_format_var, "xyz", "xyz", "gamess")
        self.output_format_dropdown.grid(row=7, column=1, padx=5)

        self.output_unit_label = ttk.Label(root, text="Output Unit (Angstrom or Bohr)", padding=5)
        self.output_unit_label.grid(row=8, column=0)
        self.output_unit_var = tk.StringVar(root)
        self.output_unit_dropdown = ttk.OptionMenu(root, self.output_unit_var, "angstrom", "angstrom", "bohr")
        self.output_unit_dropdown.grid(row=8, column=1, padx=5)

        self.convert_button = ttk.Button(root, text="Convert and Visualize", command=self.convert_and_visualize)
        self.convert_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

        # Bond Display Option
        self.show_bonds_var = tk.IntVar(value=1)
        self.show_bonds_checkbox = ttk.Checkbutton(root, text="Show Bonds", variable=self.show_bonds_var)
        self.show_bonds_checkbox.grid(row=10, column=0, columnspan=2)

        # Visualization Section
        self.fig = plt.figure(figsize=(5, 5))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=11, column=0, columnspan=2)

    def load_geometry_file(self):
        file_path = filedialog.askopenfilename()
        with open(file_path, 'r') as file:
            geometry_data = file.read()
        self.geometry_textbox.delete(1.0, tk.END)
        self.geometry_textbox.insert(tk.END, geometry_data)

    def convert_and_visualize(self):
        input_unit = self.input_unit_var.get()
        input_format = self.input_format_var.get()
        output_unit = self.output_unit_var.get()
        output_format = self.output_format_var.get()
        output_file = self.output_filename_entry.get()

        geometry_data = self.geometry_textbox.get(1.0, tk.END).strip().splitlines()

        with open("temp_geometry.txt", 'w') as temp_file:
            for line in geometry_data:
                temp_file.write(f"{line}\n")

        geometry = self.reader_converter.read_geometry("temp_geometry.txt", input_unit)
        self.reader_converter.save_converted_geometry(geometry, output_format, output_file, output_unit)

        self.ax.clear()
        self.visualize_with_bonds(geometry)
        self.canvas.draw()

    def visualize_with_bonds(self, geometry):
        atoms = np.array([[atom['x'], atom['y'], atom['z']] for atom in geometry])
        labels = [atom['symbol'] for atom in geometry]

        self.ax.scatter(atoms[:, 0], atoms[:, 1], atoms[:, 2], s=100, color='b')

        for i in range(len(atoms)):
            self.ax.text(atoms[i, 0], atoms[i, 1], atoms[i, 2], labels[i], size=12, zorder=1, color='k')

        if self.show_bonds_var.get():
            self.draw_bonds(atoms)

    def draw_bonds(self, atoms):
        bond_threshold = 1.5  # Adjust this for bond lengths
        for i in range(len(atoms)):
            for j in range(i + 1, len(atoms)):
                distance = np.linalg.norm(atoms[i] - atoms[j])
                if distance <= bond_threshold:
                    self.ax.plot([atoms[i, 0], atoms[j, 0]],
                                 [atoms[i, 1], atoms[j, 1]],
                                 [atoms[i, 2], atoms[j, 2]], 'r-', lw=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = MoleculeVisualizerApp(root)
    root.mainloop()
