import libvirt
from vm_manager import create_vm, list_vms, start_vm, stop_vm, restart_vm, delete_vm

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
