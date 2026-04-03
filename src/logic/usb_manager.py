import psutil
import os
import platform

class USBManager:
    @staticmethod
    def list_usb_drives():
        usb_drives = []
        for partition in psutil.disk_partitions():
            if 'removable' in partition.opts or USBManager._is_usb(partition.device):
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    usb_drives.append({
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "size": usage.total,
                        "fstype": partition.fstype
                    })
                except:
                    continue
        return usb_drives

    @staticmethod
    def _is_usb(device):
        if platform.system() == "Windows":
            # For Windows, we check if it's a removable drive
            # psutil.disk_partitions(all=False) usually handles this with 'removable'
            return False
        return False

    @staticmethod
    def write_iso_to_usb(iso_path, drive_mountpoint):
        """
        DANGEROUS: Requires admin/root.
        In a real app, we'd use a subprocess call to 'dd' on Linux/macOS
        or a specialized tool/library on Windows.
        """
        if platform.system() == "Windows":
            # Windows implementation (e.g., using a helper or specialized lib)
            return "Windows'ta USB yazma özelliği henüz deneyseldir."
        else:
            # Linux/macOS implementation
            # command = f"sudo dd if={iso_path} of={drive_mountpoint} bs=4M status=progress"
            return f"ISO {drive_mountpoint} adresine yazılmaya hazır. (dd komutu önerilir)"
