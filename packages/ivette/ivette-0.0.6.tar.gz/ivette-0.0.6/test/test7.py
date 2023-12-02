import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Python client for Ivette Computational chemistry and Bioinformatics project"
    )

    # Adding 'load' flag with a filename argument
    parser.add_argument(
        "load", nargs="?", help="Load a file", metavar="filename", default=None
    )

    # Adding 'run' flag without any additional argument
    parser.add_argument(
        "run", nargs="?", help="Run the program", const=True, default=None
    )

    args = parser.parse_args()

    # Check which flag was provided
    if args.load is not None:
        print(f"Loading file: {args.load}")
    elif args.run is not None:
        print("Running the program")
    else:
        print("An argument must be provided")


if __name__ == "__main__":
    main()
