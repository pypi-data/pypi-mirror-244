import logging
import subprocess
import threading
import time
import os

from .IO_module import (
    setCPU,
    setUp,
    cleanUp,
    check_gamess_installation,
    is_nwchem_installed,
    waiting_message,
)
from .supabase_module import downloadFile, upsertJob, uploadFile

# Info disabling
logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("aiohttp").setLevel(logging.CRITICAL)
logging.getLogger("gql").setLevel(logging.CRITICAL)

# Create a flag to signal when the job is done
job_done = False
job_failed = False


def run_rungms(id, nproc):
    global job_done
    global job_failed

    command = ["rungms tmp/" + id + " 00 " + str(nproc)]  # The last one is ncores

    with open(f"tmp/{id}.out", "w") as output_file:
        try:
            # Run the 'rungms' command and wait for it to complete
            subprocess.run(
                command,
                stdout=output_file,
                stderr=subprocess.STDOUT,
                shell=True,
                check=True,  # This will raise an error if the command returns a non-zero exit code
            )
            upsertJob(id, nproc=0)
            uploadFile(f"{id}.out", id, "Calculation/", localDir="tmp/")
            job_done = True
        except subprocess.CalledProcessError as e:
            if not e.returncode == -2:
                upsertJob(id, "failed", nproc=0)
                uploadFile(f"{id}.out", id, "Calculation/", localDir="tmp/")
            cleanUp(id)
            print(f"\n Job failed with exit code {e.returncode}.")
            job_done = True
            job_failed = True


def run_nwchem(id, nproc=1):
    """
    Run the calculation
    """
    global job_done
    global job_failed

    # The last one is ncores
    command = [
        f"mpirun -np {nproc} --use-hwthread-cpus $NWCHEM_TOP/bin/$NWCHEM_TARGET/nwchem tmp/{id}"]

    with open(f"tmp/{id}.out", "w") as output_file:
        try:
            # Run the 'rungms' command and wait for it to complete
            subprocess.run(
                command,
                stdout=output_file,
                stderr=subprocess.STDOUT,
                shell=True,
                check=True,  # This will raise an error if the command returns a non-zero exit code
            )
            upsertJob(id, nproc=0)
            uploadFile(f"{id}.out", id, "Calculation/", localDir="tmp/")
            job_done = True
        except subprocess.CalledProcessError as e:
            if not e.returncode == -2:
                upsertJob(id, "failed", nproc=0)
                uploadFile(f"{id}.out", id, "Calculation/", localDir="tmp/")
            cleanUp(id)
            print(f"\n Job failed with exit code {e.returncode}.")
            job_done = True
            job_failed = True


def runJob():
    global job_done
    nproc = setCPU()
    print("Press Ctrl + C at any time to exit.")

    # Loop over to run the queue
    while True:
        id, package = setUp()
        downloadFile(id)

        if package == "GAMESS US" and check_gamess_installation:
            # Create a thread to run the 'rungms' command
            rungms_thread = threading.Thread(target=run_rungms, args=(id, nproc))

            try:
                upsertJob(id, "in progress", nproc)
                print(f"Job Id: {id}")
                rungms_thread.start()  # Start the 'rungms' command thread
                while not job_done:
                    waiting_message(package)
                rungms_thread.join()  # Wait for the 'rungms' command thread to finish
                cleanUp(id)
                if not job_failed:
                    print(f"Job completed successfully.")
                job_done = False

            except KeyboardInterrupt:
                upsertJob(id, "interrupted", nproc=0)
                cleanUp(id)
                print(f"Job interrupted.")
                raise SystemExit

        elif package == "NWChem" and is_nwchem_installed:
            # Create a thread to run the 'nwchem' command
            nwchem_thread = threading.Thread(target=run_nwchem, args=(id, nproc))

            try:
                upsertJob(id, "in progress", nproc)
                print(f"Job Id: {id}")
                nwchem_thread.start()  # Start the 'rungms' command thread
                while not job_done:
                    waiting_message(package)
                nwchem_thread.join()  # Wait for the 'rungms' command thread to finish
                cleanUp(id)
                if not job_failed:
                    print(f"Job completed successfully.")
                job_done = False
            except KeyboardInterrupt:
                upsertJob(id, "interrupted", nproc=0)
                cleanUp(id)
                print(f"Job interrupted.")
                raise SystemExit

        else:
            print(f"No package called: {package}. Contact support.")
            raise SystemExit
