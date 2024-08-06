import libvirt
from vm_utils import get_vm_config

def create_vm(conn, name, memory_mb, vcpu_count, disk_size_gb):
    """Creates a VM with the given parameters"""
    xml_desc = get_vm_config(name, memory_mb, vcpu_count, disk_size_gb)
    try:
        conn.createXML(xml_desc, libvirt.VIR_DOMAIN_XML_RECONNECT)
        print(f"VM '{name}' created successfully.")
    except libvirt.libvirtError as e:
        print(f"Failed to create VM: {e}")

def list_vms(conn):
    """Lists all VMs"""
    try:
        vms = conn.listAllDomains()
        if not vms:
            print("No VMs found.")
            return

        print("\nExisting VMs:")
        for vm in vms:
            name = vm.name()
            state = vm.info()[0]  # VM state: 1 = running, 0 = shut off
            state_str = "running" if state == libvirt.VIR_DOMAIN_RUNNING else "shut off"
            print(f"- {name} ({state_str})")
        return vms
    except libvirt.libvirtError as e:
        print(f"Failed to list VMs: {e}")
        return []

def delete_vm(conn, name):
    """Deletes the VM with the given name"""
    try:
        vm = conn.lookupByName(name)
        vm.destroy()
        vm.undefine()
        print(f"VM '{name}' deleted successfully.")
    except libvirt.libvirtError as e:
        print(f"Failed to delete VM: {e}")

def start_vm(conn, name):
    """Starts the VM with the given name"""
    try:
        vm = conn.lookupByName(name)
        if vm.info()[0] == libvirt.VIR_DOMAIN_RUNNING:
            print(f"VM '{name}' is already running.")
        else:
            vm.create()
            print(f"VM '{name}' started successfully.")
    except libvirt.libvirtError as e:
        print(f"Failed to start VM: {e}")

def stop_vm(conn, name):
    """Stops the VM with the given name"""
    try:
        vm = conn.lookupByName(name)
        if vm.info()[0] == libvirt.VIR_DOMAIN_RUNNING:
            vm.shutdown()
            print(f"VM '{name}' is shutting down.")
        else:
            print(f"VM '{name}' is not running.")
    except libvirt.libvirtError as e:
        print(f"Failed to stop VM: {e}")

def restart_vm(conn, name):
    """Restarts the VM with the given name"""
    try:
        vm = conn.lookupByName(name)
        if vm.info()[0] == libvirt.VIR_DOMAIN_RUNNING:
            vm.reboot()
            print(f"VM '{name}' is rebooting.")
        else:
            print(f"VM '{name}' is not running. Starting VM first.")
            vm.create()
            print(f"VM '{name}' started successfully. Restarting now.")
            vm.reboot()
            print(f"VM '{name}' is rebooting.")
    except libvirt.libvirtError as e:
        print(f"Failed to restart VM: {e}")
