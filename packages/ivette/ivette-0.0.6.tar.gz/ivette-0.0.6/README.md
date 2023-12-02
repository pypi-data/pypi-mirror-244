# ivette-client
Python client for Ivette Computational chemistry and Bioinformatics project

## Installation steps

A technical level knowledge of computational chemistry and CLI management is required
to use this program.

This program is made mainly to run in Unix based systems (Linux and maybe MacOs).
If you happen to be using windows (>=10) you can install WSL (windows subsystem 
for Linux) easily via:

  PowerShell:
```bat
wsl --install
```

First off python must be installed, it ussualy comes pre-installed in Linux distros. 
If not, you can install as follows

  bash:
```bash
sudo apt-get update
sudo apt-get install python3.6
```

A few dependencies are required through apt-get.

- mpi4py dep

  bash:
```bash
sudo apt-get install libopenmpi-dev
```

Provided pip is installed (ussualy comes preinstalled along with python).
To install ivette CLI:

  bash:
```bash
pip install ivette-client
```

Adittionaly you must set up the PATH variable to be able to use the command
line interface

  bash:
'''bash
echo "
# IVETTE CLI PATH
export PATH=\$PATH:/home/$USER/.local/bin" >> ~/.bashrc
sudo ~/.bashrc
'''

We highly recommend you to install a computational chemistry software
right away if you dont have any. An easy choice is NWChem which
is avaiable in the linux APT and has plenty of capabilities
at the expense of being slower in comparison with other methods

```bash
sudo apt-get  install nwchem
```

After this step the installation process is done, read the documentation to
get started.

## Want to contribute?
Further documentation is required

## Support
Contact the dev team at:
eduardob1999@gmail.cpom

### Third-Party Dependencies

This project uses the following third-party libraries and dependencies:

- [Library A](https://github.com/authorA/library-a) - Licensed under the MIT License
- [Library B](https://github.com/authorB/library-b) - Licensed under the MIT License
- [Library C](https://github.com/authorC/library-c) - Licensed under the MIT License

