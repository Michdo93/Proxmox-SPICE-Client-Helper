# Proxmox-SPICE-Client-Helper
I use the virt-manager or virt-viewer as Proxmox SPICE client. This helper downloads a current .vv file and then executes it accordingly.

## Installation

### Virt-Viewer

#### Windows

If your client computer runs under windows you have to install:

* [usbredirect](https://www.spice-space.org/download/windows/usbredirect/usbredirect-x64-0.14.0.msi)
* [UsbDK x64](https://www.spice-space.org/download/windows/usbdk/UsbDk_1.0.22_x64.msi) or [UsbDK x86](https://www.spice-space.org/download/windows/usbdk/UsbDk_1.0.22_x86.msi)
* [Virt-Viewer x64](https://releases.pagure.org/virt-viewer/virt-viewer-x64-11.0-1.0.msi) or [Virt-Viewer x86](https://releases.pagure.org/virt-viewer/virt-viewer-x86-10.0-1.0.msi)

#### Linux

If your client computer runs under linux you have to install following:

```
sudo apt update
sudo apt install virt-viewer -y
```

### Python Dependencies

I assume that, regardless of whether Windows or Linux is used, Python 3 and Pip 3 are installed.

```
python3 -m pip install requests
```

The requests library is used to access the `REST API` of Proxmox.

### Proxmox SPICE Client Helper

Open a terminal/shell/cmd:

```
cd ~
git clone https://github.com/Michdo93/Proxmox-SPICE-Client-Helper
```

## Proxmox Configuration

### VM

### User Role

### Token + Secret


## VM Configuration

As example inside a linux VM you have to install:

```
sudo apt update
sudo apt install spice-vdagent spice-webdavd qemu-guest-agent -y
```

`spice-vdagent`: Enables extended SPICE support, such as mouse integration, clipboard and screen resolution.
`spice-webdavd`: Enables file transfer between host and guest via WebDAV.
`qemu-guest-agent`: Offers extended guest integrations (e.g. shutdown via Proxmox).

The spice-vdagent should start automatically after installation, but to be on the safe side you can start and activate the service:

```
sudo systemctl start spice-vdagent
sudo systemctl enable spice-vdagent
```

## Usage

### Windows


### Linux


