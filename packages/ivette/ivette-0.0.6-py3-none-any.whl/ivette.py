"module for parsing"
import argparse

from package.load_module import loadJob, loadProject
from package.run_module import runJob
from package.IO_module import print_color
from package.supabase_module import downloadFile


def main():
    "Main program thread."
    parser = argparse.ArgumentParser(
        description="""Python client for Ivette Computational chemistry and
        Bioinformatics project"""
    )

    # Creating a mutually exclusive group for 'load' and 'run' flags
    group = parser.add_mutually_exclusive_group()

    group.add_argument("--load", help="Load a file", metavar="filename")
    group.add_argument("--project", help="Load a Project", metavar="directory")
    group.add_argument("--job", help="Download a job input", metavar="id")
    group.add_argument("--calc", help="Download a calculation", metavar="id")
    group.add_argument("--run", help="Run the program", action="store_true")

    args = parser.parse_args()

    # Header
    print_color("-" * 40, "32")
    # 32 is the ANSI code for green, 1 makes it bold
    print_color("IVETTE CLI", "32;1")
    print_color("by Eduardo bogado (2023)", "34")  # 34 blue
    print_color("-" * 40, "34")

    # Accessing the values of the mutually exclusive flags
    if args.load:
        loadJob(args.load)
    elif args.project:
        loadProject(args.project)
    elif args.job:
        print(f"Downloading job {args.job}...")
        downloadFile(args.job, "/", "Job/")
    elif args.calc:
        print(f"Downloading calculation {args.calc}...")
        downloadFile(args.calc, "./", "Calculation/")
    elif args.run:
        runJob()
    else:
        runJob()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as exc:
        print_color("\nIVETTE CLI exited gracefully.", "34")
        raise SystemExit from exc
