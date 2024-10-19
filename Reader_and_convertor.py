import os
from Element_infos import ElementInfo

class GeometryReaderAndConverter:
    def __init__(self):
        self.element_info = ElementInfo()

    def read_geometry(self, file_path, input_unit='bohr'):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist.")
        
        with open(file_path, 'r') as f:
            lines = f.readlines()

        if lines[0].strip().isdigit():
            return self._read_xyz_format(lines, input_unit)
        elif any('CARBON' in line or 'NITROGEN' in line or 'HYDROGEN' in line for line in lines):
            return self._read_gamess_format(lines, input_unit)
        else:
            raise ValueError("Unsupported geometry format.")

    def _read_xyz_format(self, lines, input_unit):
        geometry = []
        for line in lines[2:]:
            parts = line.split()
            element_symbol = parts[0]
            x, y, z = map(float, parts[1:4])
            atomic_number = self.element_info.get_atomic_number_from_symbol(element_symbol)
            if input_unit == 'bohr':  # Convert from angstrom to bohr
                x, y, z = self._convert_units(x, y, z, 'angstrom', 'bohr')
            geometry.append({"atomic_number": atomic_number, "symbol": element_symbol, "x": x, "y": y, "z": z})
        return geometry

    def _read_gamess_format(self, lines, input_unit):
        geometry = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 5:
                element_name = parts[0]
                atomic_number = self.element_info.get_atomic_number_from_symbol(element_name[:1])
                x, y, z = map(float, parts[2:5])
                if input_unit == 'angstrom':  # Convert from bohr to angstrom
                    x, y, z = self._convert_units(x, y, z, 'bohr', 'angstrom')
                geometry.append({"atomic_number": atomic_number, "symbol": element_name[:1], "x": x, "y": y, "z": z})
        return geometry

    def convert_to_format(self, geometry, target_format, output_unit='angstrom'):
        if target_format.lower() == 'xyz':
            return self._convert_to_xyz(geometry, output_unit)
        elif target_format.lower() == 'gamess':
            return self._convert_to_gamess(geometry, output_unit)
        else:
            raise ValueError(f"Unsupported target format: {target_format}")

    def _convert_to_xyz(self, geometry, output_unit):
        lines = [f"{len(geometry)}", "Converted to XYZ format"]
        for atom in geometry:
            x, y, z = self._convert_units(atom['x'], atom['y'], atom['z'], 'bohr', output_unit)
            lines.append(f"{atom['symbol']} {x:.6f} {y:.6f} {z:.6f}")
        return "\n".join(lines)

    def _convert_to_gamess(self, geometry, output_unit):
        lines = ["Converted to GAMESS format"]
        for atom in geometry:
            x, y, z = self._convert_units(atom['x'], atom['y'], atom['z'], 'angstrom', output_unit)
            element_name = self.element_info.get_element_info(atom['atomic_number'])["name"].upper()
            lines.append(f"{element_name} {atom['atomic_number']}.0 {x:.6f} {y:.6f} {z:.6f}")
        return "\n".join(lines)

    def _convert_units(self, x, y, z, from_unit, to_unit):
        conversion_factor = 1.8897259886
        if from_unit == to_unit:
            return x, y, z
        elif from_unit == 'angstrom' and to_unit == 'bohr':
            return x * conversion_factor, y * conversion_factor, z * conversion_factor
        elif from_unit == 'bohr' and to_unit == 'angstrom':
            return x / conversion_factor, y / conversion_factor, z / conversion_factor
        else:
            raise ValueError(f"Unsupported unit conversion: {from_unit} to {to_unit}")

    def save_converted_geometry(self, geometry, target_format, file_path, output_unit='angstrom'):
        converted_geometry = self.convert_to_format(geometry, target_format, output_unit)
        with open(file_path, 'w') as f:
            f.write(converted_geometry)
        print(f"Geometry saved to {file_path}")
