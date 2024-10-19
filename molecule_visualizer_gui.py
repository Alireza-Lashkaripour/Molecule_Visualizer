import tkinter as tk
from tkinter import filedialog
from Reader_and_convertor import GeometryReaderAndConverter
from Visualizer import GeometryVisualizer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MoleculeVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Molecule Visualizer and Converter")

        self.reader_converter = GeometryReaderAndConverter()
        self.visualizer = GeometryVisualizer()

        # Input Section
        self.input_label = tk.Label(root, text="Input Geometry")
        self.input_label.grid(row=0, column=0)

        self.geometry_textbox = tk.Text(root, height=10, width=50)
        self.geometry_textbox.grid(row=1, column=0, columnspan=2)

        self.input_format_label = tk.Label(root, text="Input Format (GAMESS or XYZ)")
        self.input_format_label.grid(row=2, column=0)
        self.input_format_var = tk.StringVar(root)
        self.input_format_dropdown = tk.OptionMenu(root, self.input_format_var, "gamess", "xyz")
        self.input_format_dropdown.grid(row=2, column=1)

        self.input_unit_label = tk.Label(root, text="Input Unit (Angstrom or Bohr)")
        self.input_unit_label.grid(row=3, column=0)
        self.input_unit_var = tk.StringVar(root)
        self.input_unit_dropdown = tk.OptionMenu(root, self.input_unit_var, "angstrom", "bohr")
        self.input_unit_dropdown.grid(row=3, column=1)

        self.load_button = tk.Button(root, text="Load Geometry from File", command=self.load_geometry_file)
        self.load_button.grid(row=4, column=0, columnspan=2)

        # Output Section
        self.output_label = tk.Label(root, text="Output Settings")
        self.output_label.grid(row=5, column=0)

        self.output_filename_entry = tk.Entry(root)
        self.output_filename_entry.grid(row=6, column=1)
        self.output_filename_label = tk.Label(root, text="Output File Name")
        self.output_filename_label.grid(row=6, column=0)

        self.output_format_label = tk.Label(root, text="Output Format (GAMESS or XYZ)")
        self.output_format_label.grid(row=7, column=0)
        self.output_format_var = tk.StringVar(root)
        self.output_format_dropdown = tk.OptionMenu(root, self.output_format_var, "gamess", "xyz")
        self.output_format_dropdown.grid(row=7, column=1)

        self.output_unit_label = tk.Label(root, text="Output Unit (Angstrom or Bohr)")
        self.output_unit_label.grid(row=8, column=0)
        self.output_unit_var = tk.StringVar(root)
        self.output_unit_dropdown = tk.OptionMenu(root, self.output_unit_var, "angstrom", "bohr")
        self.output_unit_dropdown.grid(row=8, column=1)

        self.convert_button = tk.Button(root, text="Convert and Visualize", command=self.convert_and_visualize)
        self.convert_button.grid(row=9, column=0, columnspan=2)

        # Visualization Section
        self.fig = plt.figure(figsize=(5, 5))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=10, column=0, columnspan=2)

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

        # Read geometry from the textbox
        geometry_data = self.geometry_textbox.get(1.0, tk.END).strip().splitlines()

        # Create a temporary file from pasted geometry to simulate file input
        with open("temp_geometry.txt", 'w') as temp_file:
            for line in geometry_data:
                temp_file.write(f"{line}\n")

        # Read geometry and convert
        geometry = self.reader_converter.read_geometry("temp_geometry.txt", input_unit)
        self.reader_converter.save_converted_geometry(geometry, output_format, output_file, output_unit)

        # Visualize the geometry
        self.ax.clear()
        self.visualizer.visualize_geometry(geometry, title="Molecule Visualization")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = MoleculeVisualizerApp(root)
    root.mainloop()
