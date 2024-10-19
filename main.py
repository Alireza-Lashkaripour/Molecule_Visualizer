from Reader_and_convertor import GeometryReaderAndConverter
from Visualizer import GeometryVisualizer

def main():
    reader_converter = GeometryReaderAndConverter()
    visualizer = GeometryVisualizer()

    input_file = input("Enter the input file name (with path): ")
    input_unit = input("Enter the unit for the input file (angstrom or bohr): ").lower()
    
    output_format = input("Enter the desired output format (xyz or gamess): ").lower()
    output_file = input("Enter the output file name (with path): ")
    output_unit = input(f"Enter the unit for the output file (angstrom or bohr): ").lower()

    try:
        geometry = reader_converter.read_geometry(input_file, input_unit)
        print(f"Successfully read geometry from {input_file}.")

        reader_converter.save_converted_geometry(geometry, output_format, output_file, output_unit=output_unit)
        print(f"Geometry successfully converted and saved to {output_file}.")

        visualizer.visualize_geometry(geometry, title=f"Original Geometry from {input_file}")
        converted_geometry = reader_converter.read_geometry(output_file, output_unit)
        visualizer.visualize_geometry(converted_geometry, title=f"Converted Geometry ({output_format.upper()})")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
