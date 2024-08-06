# VMManager 1.0

## Overview

This project is a command-line tool for managing virtual machines (VMs) using `libvirt`. It allows you to create, list, start, stop, restart, and delete VMs on a `libvirt`-compatible hypervisor. The tool is designed to work with KVM-based virtual machines and provides a simple interface for common VM management tasks.

## Project Structure

The project is organized into the following files:

- **`main.py`**: The entry point for the application. Contains the command-line interface for interacting with the VM manager.
- **`vm_manager.py`**: Contains functions for managing VMs, such as creating, listing, starting, stopping, restarting, and deleting VMs.
- **`vm_utils.py`**: Contains utility functions for generating the XML configuration required to create a VM.

## Prerequisites

- Python 3.x
- `libvirt` Python bindings (install with `pip install libvirt-python`)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/JubilantMarmot/HC-VMmaker
   cd HC-VMmaker
   ```

2. **Install the required Python packages:**

   ```bash
   pip install libvirt-python
   ```

## Usage

1. **Start the application:**

   ```bash
   python main.py
   ```

2. **Interact with the application:**

   You'll be presented with a menu to choose different VM management operations. Enter the number corresponding to your choice and follow the prompts.

   - **1. Create a VM**: Create a new VM by providing the name, memory size, number of CPUs, and disk size.
   - **2. List VMs**: List all existing VMs with their current state (running or shut off).
   - **3. Start a VM**: Start a VM by providing its name.
   - **4. Stop a VM**: Stop a running VM by providing its name.
   - **5. Restart a VM**: Restart a VM by providing its name. If the VM is not running, it will be started first.
   - **6. Delete a VM**: Delete a VM by providing its name.
   - **7. Exit**: Exit the application.

## Code Structure

- **`main.py`**: Handles user input and interactions. It connects to the `libvirt` hypervisor and calls functions from `vm_manager.py`.
- **`vm_manager.py`**: Contains the core VM management functions such as `create_vm`, `list_vms`, `start_vm`, `stop_vm`, `restart_vm`, and `delete_vm`.
- **`vm_utils.py`**: Provides the `get_vm_config` function to generate XML configuration for creating VMs.

## License

This project is licensed under the MIT License because i want to keep it open source for anyone to use

## Contact

For any questions or issues, please message me on slack- @JubilantMarmot