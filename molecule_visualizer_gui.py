import tkinter as tk
from tkinter import filedialog, ttk
from Reader_and_convertor import GeometryReaderAndConverter
from Visualizer import GeometryVisualizer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from advanced_options import AdvancedOptions

class MoleculeVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Molecule Visualizer and Converter")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TLabel", font=("Helvetica", 12))
        self.style.configure("TButton", font=("Helvetica", 10))
        self.style.configure("TEntry", font=("Helvetica", 10))

        self.reader_converter = GeometryReaderAndConverter()
        self.visualizer = GeometryVisualizer()

        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, padx=10, pady=10)

        self.input_label = ttk.Label(self.frame, text="Input Geometry")
        self.input_label.grid(row=0, column=0, columnspan=2, sticky="W")

        self.geometry_textbox = tk.Text(self.frame, height=10, width=50)
        self.geometry_textbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.input_format_label = ttk.Label(self.frame, text="Input Format (GAMESS or XYZ)")
        self.input_format_label.grid(row=2, column=0, sticky="W")
        self.input_format_var = tk.StringVar(self.frame)
        self.input_format_dropdown = ttk.OptionMenu(self.frame, self.input_format_var, "gamess", "gamess", "xyz")
        self.input_format_dropdown.grid(row=2, column=1, padx=5)

        self.input_unit_label = ttk.Label(self.frame, text="Input Unit (Angstrom or Bohr)")
        self.input_unit_label.grid(row=3, column=0, sticky="W")
        self.input_unit_var = tk.StringVar(self.frame)
        self.input_unit_dropdown = ttk.OptionMenu(self.frame, self.input_unit_var, "bohr", "bohr", "angstrom")
        self.input_unit_dropdown.grid(row=3, column=1, padx=5)

        self.load_button = ttk.Button(self.frame, text="Load Geometry from File", command=self.load_geometry_file)
        self.load_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.output_label = ttk.Label(self.frame, text="Output Settings")
        self.output_label.grid(row=5, column=0, columnspan=2, sticky="W", pady=10)

        self.output_filename_entry = ttk.Entry(self.frame, width=30)
        self.output_filename_entry.grid(row=6, column=1, padx=5)
        self.output_filename_label = ttk.Label(self.frame, text="Output File Name")
        self.output_filename_label.grid(row=6, column=0, sticky="W")

        self.output_format_label = ttk.Label(self.frame, text="Output Format (GAMESS or XYZ)")
        self.output_format_label.grid(row=7, column=0, sticky="W")
        self.output_format_var = tk.StringVar(self.frame)
        self.output_format_dropdown = ttk.OptionMenu(self.frame, self.output_format_var, "xyz", "xyz", "gamess")
        self.output_format_dropdown.grid(row=7, column=1, padx=5)

        self.output_unit_label = ttk.Label(self.frame, text="Output Unit (Angstrom or Bohr)")
        self.output_unit_label.grid(row=8, column=0, sticky="W")
        self.output_unit_var = tk.StringVar(self.frame)
        self.output_unit_dropdown = ttk.OptionMenu(self.frame, self.output_unit_var, "angstrom", "angstrom", "bohr")
        self.output_unit_dropdown.grid(row=8, column=1, padx=5)

        self.convert_button = ttk.Button(self.frame, text="Convert and Visualize", command=self.convert_and_visualize)
        self.convert_button.grid(row=9, column=0, columnspan=2, padx=5, pady=10)

        self.show_bonds_var = tk.IntVar(value=1)
        self.show_bonds_checkbox = ttk.Checkbutton(self.frame, text="Show Bonds", variable=self.show_bonds_var)
        self.show_bonds_checkbox.grid(row=10, column=0, columnspan=2)

        self.fig = plt.figure(figsize=(7, 7))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=11, column=0, columnspan=2, padx=10, pady=10)

        self.canvas.mpl_connect('scroll_event', self.zoom)

        self.zoom_factor = 1.0
        self.create_fullscreen_button()

        self.advanced_options = AdvancedOptions(root, self)

    def create_fullscreen_button(self):
        self.fullscreen_button = ttk.Button(self.frame, text="Toggle Fullscreen", command=self.toggle_fullscreen)
        self.fullscreen_button.grid(row=12, column=0, columnspan=2, pady=10)

    def toggle_fullscreen(self):
        is_fullscreen = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not is_fullscreen)
        self.canvas.get_tk_widget().config(width=self.root.winfo_width(), height=self.root.winfo_height())
        self.canvas.draw()

    def zoom(self, event):
        if event.button == 'up':
            self.zoom_factor *= 1.1
        elif event.button == 'down':
            self.zoom_factor /= 1.1

        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        zlim = self.ax.get_zlim()

        self.ax.set_xlim([x * self.zoom_factor for x in xlim])
        self.ax.set_ylim([y * self.zoom_factor for y in ylim])
        self.ax.set_zlim([z * self.zoom_factor for z in zlim])

        self.canvas.draw()

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

        if not output_file:
            print("Please provide a valid output file name.")
            return

        geometry_data = self.geometry_textbox.get(1.0, tk.END).strip().splitlines()

        with open("temp_geometry.txt", 'w') as temp_file:
            for line in geometry_data:
                temp_file.write(f"{line}\n")

        self.geometry = self.reader_converter.read_geometry("temp_geometry.txt", input_unit)
        self.reader_converter.save_converted_geometry(self.geometry, output_format, output_file, output_unit)

        self.ax.clear()
        self.visualize_with_bonds(self.geometry)
        self.canvas.draw()

    def visualize_with_bonds(self, geometry):
        atoms = np.array([[atom['x'], atom['y'], atom['z']] for atom in geometry])
        labels = [atom['symbol'] for atom in geometry]

        self.ax.scatter(atoms[:, 0], atoms[:, 1], atoms[:, 2], s=100, color='b')

        for i in range(len(atoms)):
            self.ax.text(atoms[i, 0], atoms[i, 1], atoms[i, 2], labels[i], size=12, zorder=1, color='k')

        if self.show_bonds_var.get():
            self.draw_bonds(atoms)

        max_range = np.ptp(atoms, axis=0).max()
        mid_x, mid_y, mid_z = np.mean(atoms, axis=0)
        self.ax.set_xlim(mid_x - max_range / 2, mid_x + max_range / 2)
        self.ax.set_ylim(mid_y - max_range / 2, mid_y + max_range / 2)
        self.ax.set_zlim(mid_z - max_range / 2, mid_z + max_range / 2)

    def draw_bonds(self, atoms):
        bond_thresholds = {
            "single": 1.6,
            "double": 1.3,
            "triple": 1.2,
        }

        for i in range(len(atoms)):
            for j in range(i + 1, len(atoms)):
                distance = np.linalg.norm(atoms[i] - atoms[j])

                if distance <= bond_thresholds["triple"]:
                    self.ax.plot([atoms[i, 0], atoms[j, 0]],
                                 [atoms[i, 1], atoms[j, 1]],
                                 [atoms[i, 2], atoms[j, 2]], 'r-', lw=4)
                elif distance <= bond_thresholds["double"]:
                    self.ax.plot([atoms[i, 0], atoms[j, 0]],
                                 [atoms[i, 1], atoms[j, 1]],
                                 [atoms[i, 2], atoms[j, 2]], 'g-', lw=3)
                elif distance <= bond_thresholds["single"]:
                    self.ax.plot([atoms[i, 0], atoms[j, 0]],
                                 [atoms[i, 1], atoms[j, 1]],
                                 [atoms[i, 2], atoms[j, 2]], 'b-', lw=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = MoleculeVisualizerApp(root)
    root.mainloop()

