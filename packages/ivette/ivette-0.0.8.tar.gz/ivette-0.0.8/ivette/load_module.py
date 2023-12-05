"""Module for handling input/output operations."""

import itertools
import logging

from .IO_module import (
    create_charge_multiplicity_array,
    create_string_array,
    file_exists,
    get_valid_input,
    verify_file_extension,
    exists,
    cleanUp
)
from .fileIO_module import (
    generate_nwchem_input_from_sdf,
    convert_xyz_to_sdf,
    get_files_with_extension,
    get_word_at_position,
    nwchem_to_xyz,
    replace_start_directive
)
from .supabase_module import insertSpecies, uploadFile, insert_job, upsertJob

logging.getLogger("httpx").setLevel(logging.CRITICAL)

# Available packages:
available_packages = ['NWChem']


def load_job(filename: str):
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
            package = available_packages[get_valid_input(
                f"Software available:\n1 - {available_packages[0]}\nSelect a package: ", 1, 2) - 1]

            if package == available_packages[0]:

                # Validation implementation required
                basis = input("Enter a valid basis set: ")
                functional = input("Enter a valid functional: ")
                charge = input("Enter the system charge: ")
                multiplicity = input("Enter the system multiplicity: ")
                operation = input("Operation: ")
                # Add maxiter, maxcycle, etc.

                job_id = insert_job(name, package, operation, description)
                print("Job id:", job_id)

                generate_nwchem_input_from_sdf(
                    filename,
                    basis,
                    charge,
                    job_id,
                    functional=functional,
                    multiplicity=multiplicity,
                    operation=operation
                )
                print(f"Loading job: {filename.replace('.sdf', '.nw')}")

                uploadFile(filename.replace('.sdf', '.nw'), job_id, 'Job/')
                uploadFile(filename, job_id, 'Species/')

                insertSpecies(filename, job_id)
                upsertJob(job_id, 'pending')

                print("Job loaded successfully")

            else:
                print("Currently, we don't have support for the selected package.")
                raise SystemExit

        elif verify_file_extension(filename, ['.nw']):
            # Argument input
            name = input('Enter the job name: ')
            description = input('Enter a description: ')
            package = available_packages[0]
            print("Loading job:", filename)
            operation = get_word_at_position(filename, 'task', 2)
            job_id = insert_job(name, package, operation, description)

            print("Job id:", job_id)
            replace_start_directive(filename, job_id)
            nwchem_to_xyz(filename, f"{job_id}.xyz")
            convert_xyz_to_sdf(f"{job_id}.xyz", f"{job_id}.sdf")

            uploadFile(filename, job_id, 'Job/')
            uploadFile(f"{job_id}.sdf", job_id, 'Species/')

            insertSpecies(f"{job_id}.sdf", job_id)
            upsertJob(job_id, 'pending')

            cleanUp(job_id)
            print("Job loaded successfully")

        else:

            print("The file extension is not supported.")
            raise SystemExit
        
    else:
        
        print(f"The file {filename} does not exist.")
        raise SystemExit


def load_project(directory: str, extension='.sdf'):
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
            if not check_packages([package], available_packages):
                print(
                    f"Currently, we don't have support for the {package} package.")
                raise SystemExit

        files = get_files_with_extension(directory, extension)
        print("Files with extension", extension,
              "in directory", directory, ":", files)
        basis_sets = create_string_array("Enter basis sets (q to quit): ")
        functionals = create_string_array("Enter functionals (q to quit): ")
        charge_multiplicities = create_charge_multiplicity_array(
            "Enter charge and then multiplicity (q to quit): ")
        operations = create_string_array(
            "Enter operations in the order required (q to quit): ")

        for package in packages:
            if package == available_packages[0]:
                for file, basis, functional, charge_multiplicity, operation in itertools.product(files, basis_sets, functionals, charge_multiplicities, operations):
                    charge, multiplicity = charge_multiplicity
                    print(charge_multiplicities)
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
                    print(
                        f"uploadFile({directory} + {file.replace('.sdf', '.nw')}, id, 'Job/')")
                    print("upsertJob(id, 'pending')")
                    print("Job loaded successfully")
    else:
        print(f"The directory {directory} does not exist.")
        raise SystemExit


def check_packages(packages: list, available_packages: list) -> bool:
    """
    Check if a list of packages is supported.

    Args:
        packages (list): The list of packages to check.
        available_packages (list): The list of available packages.

    Returns:
        bool: True if all packages are supported, False otherwise.
    """
    return all(package in available_packages for package in packages)
