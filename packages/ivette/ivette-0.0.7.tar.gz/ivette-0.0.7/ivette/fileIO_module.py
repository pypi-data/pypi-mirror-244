from openbabel import pybel
from rdkit import Chem
import os

def read_sdf_coordinates(sdf_file):
    """
    Read molecular coordinates from an SDF file.

    Parameters:
    - sdf_file (str): Path to the SDF file.

    Returns:
    - str: XYZ coordinates of the molecular geometry.
    """
    mol_supplier = Chem.SDMolSupplier(sdf_file, removeHs=False)
    mol = next(mol_supplier)
    if mol is not None:
        # Extract atomic coordinates
        coordinates = []
        for atom in mol.GetAtoms():
            pos = mol.GetConformer().GetAtomPosition(atom.GetIdx())
            coordinates.append(
                f"  {atom.GetSymbol()} {pos.x:.8f} {pos.y:.8f} {pos.z:.8f}"
            )

        return "\n".join(coordinates)


def nwchem_to_xyz(nw_filename, xyz_filename):
    """
    Convert NWChem input file to XYZ file.

    Parameters:
    - nw_filename (str): Path to the NWChem input file.
    - xyz_filename (str): Path to the output XYZ file.
    """
    # Read NWChem input file
    with open(nw_filename, 'r') as nw_file:
        nw_lines = nw_file.readlines()

    # Extract atomic coordinates
    atomic_coordinates = []
    start_reading_coordinates = False
    for line in nw_lines:
        if 'geometry' in line.lower():
            start_reading_coordinates = True
        elif 'end' in line.lower() and start_reading_coordinates:
            break
        elif start_reading_coordinates:
            tokens = line.split()
            if len(tokens) >= 4:
                element, x, y, z = tokens[:4]
                atomic_coordinates.append(
                    (element, float(x), float(y), float(z)))

    # Write XYZ file
    with open(xyz_filename, 'w') as xyz_file:
        xyz_file.write(f"{len(atomic_coordinates)}\n")
        xyz_file.write("Converted from NWChem input file\n")
        for atom in atomic_coordinates:
            xyz_file.write(
                f"{atom[0]} {atom[1]:.6f} {atom[2]:.6f} {atom[3]:.6f}\n")


def convert_xyz_to_sdf(input_file, output_file):
    """
    Convert a NWChem input file to a .sdf file using Open Babel.

    Parameters:
    - input_file (str): Path to the input NWChem file.
    - output_file (str): Path to the output .sdf file.
    """
    # Create an Open Babel molecule object
    mol_generator = pybel.readfile("xyz", input_file)
    mol = next(mol_generator)

    # Output the molecule to a .sdf file
    with open(output_file, 'w') as sdf_file:
        sdf_file.write(mol.write("sdf"))


def generate_nwchem_input_from_sdf(
    sdf_file,
    basis_set,
    charge=0,  # Default to neutral charge
    title="Hartree-Fock Calculation",
    mem="200 MB",
    method="dft",
    functional="b3lyp",
    multiplicity=1,  # Default to singlet (closed-shell)
    operation='energy',
    ncycles='200',
):
    """
    Generate NWChem input file for a DFT calculation with an option for a frequency calculation using coordinates from an SDF file.

    Parameters:
    - sdf_file (str): Path to the SDF file containing molecular coordinates.
    - basis_set (str): Basis set to be used in the calculation.
    - charge (int): Charge of the system.
    - title (str): Title for the NWChem input file.
    - method (str): NWChem calculation method (e.g., "scf", "dft", etc.).
    - functional (str): DFT functional to be used in the calculation.
    - multiplicity (int): Multiplicity of the system (1 for singlet, 2 for doublet, etc.).
    - mem (str): Memory to be used per thread.
    """
    molecule = read_sdf_coordinates(sdf_file)

    if molecule is None:
        print("Error: Unable to read molecular coordinates from SDF file.")
        return

    input_content = f"""
start {title}
title "{title}"

memory total {mem}

charge {charge}

geometry units au
{molecule}
end

basis
 * library {basis_set}
end

{method}
  xc {functional}
  mult {multiplicity}
  iterations {ncycles}
end

task {method} {operation}
"""

    with open(sdf_file.replace(".sdf", ".nw"), "w") as file:
        file.write(input_content)


def replace_start_directive(file_path, new_start_directive):
    try:
        # Read the content of the file
        with open(file_path, 'r') as file:
            content = file.read()

        # Find the start directive using a regular expression
        import re
        pattern = re.compile(r'^\s*start\s+\S+', re.MULTILINE)
        match = pattern.search(content)

        if match:
            # Replace the start directive with the new string
            updated_content = content[:match.start(
            )] + f"start {new_start_directive}" + content[match.end():]

            # Write the updated content back to the file
            with open(file_path, 'w') as file:
                file.write(updated_content)

        else:
            print("No start directive found in the file.")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")


def get_files_with_extension(directory: str, extension: str):
    """
    Get a list of files with a specific extension in a directory.

    Args:
        directory (str): The directory path.
        extension (str): The file extension.

    Returns:
        list: A list of file names.
    """
    files = [file for file in os.listdir(
        directory) if file.endswith(extension)]
    return files


def get_word_at_position(file_path, keyword, position):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if keyword in line:
                    # Split the line into words and get the word at the specified position
                    words = line.strip().split()
                    if len(words) > position:
                        return words[position]
                    else:
                        return f"Not enough words in the line for position {position}."

            return f"No '{keyword}' line found in the file."

    except FileNotFoundError:
        return f"File '{file_path}' not found."
