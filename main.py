import libvirt

def get_vm_config(name, memory_mb, vcpu_count, disk_size_gb):
    """Generates the XML configuration for the VM"""
    memory = memory_mb * 1024  # Convert MB to KiB
    disk_size = disk_size_gb * 1024 * 1024 * 1024  # Convert GB to bytes

    xml = f"""
    <domain type='kvm'>
      <name>{name}</name>
      <memory unit='KiB'>{memory}</memory>
      <vcpu placement='static'>{vcpu_count}</vcpu>
      <os>
        <type arch='x86_64' machine='pc-i440fx-2.9'>hvm</type>
        <boot dev='hd'/>
      </os>
      <devices>
        <disk type='file' device='disk'>
          <driver name='qemu' type='qcow2'/>
          <source file='/var/lib/libvirt/images/{name}.qcow2'/>
          <target dev='vda' bus='virtio'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
        </disk>
        <interface type='network'>
          <mac address='52:54:00:22:33:44'/>
          <source network='default'/>
          <model type='virtio'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
        </interface>
      </devices>
    </domain>
    """
    return xml

def create_vm(conn, name, memory_mb, vcpu_count, disk_size_gb):
    """Creates a VM with the given parameters"""
    xml_desc = get_vm_config(name, memory_mb, vcpu_count, disk_size_gb)
    try:
        # Create the VM
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

def main():
    conn = libvirt.open('qemu:///system')
    if conn is None:
        print('Failed to open connection to qemu:///system')
        return

    while True:
        print("\nVirtual Machine Manager")
        print("1. Create a VM")
        print("2. List VMs")
        print("3. Start a VM")
        print("4. Stop a VM")
        print("5. Restart a VM")
        print("6. Delete a VM")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter the name of the VM: ")
            memory_mb = int(input("Enter the amount of memory in MB: "))
            vcpu_count = int(input("Enter the number of vCPUs: "))
            disk_size_gb = int(input("Enter the disk size in GB: "))
            
            create_vm(conn, name, memory_mb, vcpu_count, disk_size_gb)
        
        elif choice == '2':
            list_vms(conn)
        
        elif choice == '3':
            name = input("Enter the name of the VM to start: ")
            start_vm(conn, name)
        
        elif choice == '4':
            name = input("Enter the name of the VM to stop: ")
            stop_vm(conn, name)
        
        elif choice == '5':
            name = input("Enter the name of the VM to restart: ")
            restart_vm(conn, name)
        
        elif choice == '6':
            name = input("Enter the name of the VM to delete: ")
            delete_vm(conn, name)
        
        elif choice == '7':
            break
        
        else:
            print("Invalid choice, please try again.")

    conn.close()

if __name__ == '__main__':
    main()
