# Molecule Visualizer and Converter


This Python-based application allows you to visualize molecular geometries, convert between different formats (GAMESS and XYZ), and explore molecules in 3D with zooming, panning, and full-screen options.
Features:

    Load molecular geometry from files (GAMESS or XYZ formats).
    Convert between formats: GAMESS ↔ XYZ.
    Visualize molecules in 3D with options for displaying bonds (single, double, and triple).
    Zoom in and out using the mouse scroll.
    Toggle full-screen mode for a larger viewing experience.

How to Use:

    Load Geometry:
        Enter the molecular geometry directly in the input text box, or click Load Geometry from File to import a geometry file.
        Supported formats: GAMESS and XYZ.

    Set Input/Output Options:
        Choose the input unit (Angstrom or Bohr) and format (GAMESS or XYZ).
        Specify the output file name and select the desired output format and unit.

    Convert and Visualize:
        Click Convert and Visualize to view the molecule in 3D.
        You can toggle bonds on or off using the "Show Bonds" checkbox.

    Zoom and Full-Screen:
        Zoom in and out with the scroll wheel.
        Click Toggle Fullscreen to enter or exit full-screen mode.

Requirements:

    Python 3.x
    Required packages: matplotlib, tkinter, numpy

Install the required packages:

csharp

pip install matplotlib numpy
sudo apt-get install python3-tk  # For Linux users

Running the Program:

bash

python molecule_visualizer_gui.py
