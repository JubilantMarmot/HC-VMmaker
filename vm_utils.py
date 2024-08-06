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
