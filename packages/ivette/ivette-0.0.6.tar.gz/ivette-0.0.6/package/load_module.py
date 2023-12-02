import os
import itertools
import logging
from .IO_module import file_exists, get_valid_input, verify_file_extension, exists
from .fileIO_module import generate_nwchem_input_from_sdf
from .supabase_module import insertSpecies, uploadFile, insertJob, upsertJob

logging.getLogger("httpx").setLevel(logging.CRITICAL)

# Available packages:
availablePackages = ['NWChem']


def loadJob(filename: str):
    """
    Load a job from a file.

    Args:
        filename (str): The name of the file.

    Raises:
        SystemExit: If the file does not exist or the package is not supported.
    """
    if file_exists(filename, "./"):
        if verify_file_extension(filename, ['.sdf']):
            print("The file is recognized as a .sdf")
            print("An .nw input file will be created.")

            # Argument input
            name = input('Enter the job name: ')
            description = input('Enter a description: ')
            package = availablePackages[get_valid_input(f"Software available:\n1 - {availablePackages[0]}\nSelect a package: ", 1, 2) - 1]

            if package == availablePackages[0]:

                # Validation implementation required
                basis = input("Enter a valid basis set: ")
                functional = input("Enter a valid functional: ")
                charge = input("Enter the system charge: ")
                multiplicity = input("Enter the system multiplicity: ")
                operation = input("Operation: ")
                # Add maxiter, maxcycle, etc.

                id = insertJob(name, package, description)
                print("Job id:", id)

                generate_nwchem_input_from_sdf(
                    filename,
                    basis,
                    charge,
                    id,
                    functional=functional,
                    multiplicity=multiplicity,
                    operation=operation
                )
                print(f"Loading job: {filename.replace('.sdf', '.nw')}")

                uploadFile(filename.replace('.sdf', '.nw'), id, 'Job/')
                uploadFile(filename, id, 'Species/')

                insertSpecies(filename, id)
                upsertJob(id, 'pending')

                print("Job loaded successfully")
                
            else:
                print("Currently we don't have support for the selected package.")
                raise SystemExit
        else:
            # Argument input
            name = input('Enter the job name: ')
            description = input('Enter a description: ')
            package = availablePackages[get_valid_input(f"Software available:\n1 - {availablePackages[0]}\nSelect a package: ", 1, 2) - 1]
            print("Loading job:", filename)
            id = insertJob(name, package, description)
            print("Job id:", id)
            uploadFile(filename, id, 'Job/')
            # A conversion to sdf is required to upload specie
            upsertJob(id, 'pending')
            print("Job loaded successfully")
    else:
        print(f"The file {filename} does not exist.")
        raise SystemExit


def loadProject(directory: str, extension='.sdf'):
    """
    Load a project from a directory.

    Args:
        directory (str): The directory path.
        extension (str, optional): The file extension to filter. Defaults to '.sdf'.

    Raises:
        SystemExit: If the directory does not exist or the package is not supported.
    """
    if not directory.endswith('/'):
        directory += '/'

    if exists(directory):
        name = input('Enter the project name: ')
        description = input('Enter the project description: ')
        packages = create_string_array("Enter the packages (q to quit): ")

        for package in packages:
            if not check_packages([package], availablePackages):
                print(f"Currently we don't have support for the {package} package.")
                raise SystemExit

        files = get_files_with_extension(directory, extension)
        print("Files with extension", extension, "in directory", directory, ":", files)
        basisSets = create_string_array("Enter basis sets (q to quit): ")
        functionals = create_string_array("Enter functionals (q to quit): ")
        chargeMultiplicities = create_charge_multiplicity_array("Enter charge and then multiplicity (q to quit): ")
        operations = create_string_array("Enter operations in the order required (q to quit): ")

        for package in packages:
            if package == availablePackages[0]:
                for file, basis, functional, charge_multiplicity, operation in itertools.product(files, basisSets, functionals, chargeMultiplicities, operations):
                    charge, multiplicity = charge_multiplicity
                    print(chargeMultiplicities)
                    generate_nwchem_input_from_sdf(
                        directory + file,
                        basis,
                        charge,
                        name,
                        functional=functional,
                        multiplicity=multiplicity,
                        operation=operation
                    )
                    print(f"Loading job: {file.replace('.sdf', '.nw')}")
                    print(f"insertJob({name}, {package}, {description} etc)")
                    print("Job id: id")
                    print(f"uploadFile({directory} + {file.replace('.sdf', '.nw')}, id, 'Job/')")
                    print("upsertJob(id, 'pending')")
                    print("Job loaded successfully")
    else:
        print(f"The directory {directory} does not exist.")
        raise SystemExit


def get_files_with_extension(directory: str, extension: str):
    """
    Get a list of files with a specific extension in a directory.

    Args:
        directory (str): The directory path.
        extension (str): The file extension.

    Returns:
        list: A list of file names.
    """
    files = []
    for file in os.listdir(directory):
        if file.endswith(extension):
            files.append(file)
    return files


def create_string_array(prompt: str) -> list:
    """
    Create a list of strings from user input.

    Args:
        prompt (str): The prompt message.

    Returns:
        list: A list of strings.
    """
    string_array = []
    while True:
        string = input(prompt)
        if string == 'q':
            break
        string_array.append(string)
    return string_array


def check_packages(packages: list, availablePackages: list) -> bool:
    """
    Check if a list of packages is supported.

    Args:
        packages (list): The list of packages to check.
        availablePackages (list): The list of available packages.

    Returns:
        bool: True if all packages are supported, False otherwise.
    """
    return all(package in availablePackages for package in packages)


def create_charge_multiplicity_array(prompt: str) -> list:
    """
    Create a list of charge-multiplicity pairs from user input.

    Args:
        prompt (str): The prompt message.

    Returns:
        list: A list of charge-multiplicity pairs.
    """
    charge_multiplicity_array = []
    while True:
        charge = input("Enter charge (q to quit): ")
        if charge == 'q':
            break
        multiplicity = input("Enter multiplicity: ")
        charge_multiplicity_array.append([charge, multiplicity])
    return charge_multiplicity_array
