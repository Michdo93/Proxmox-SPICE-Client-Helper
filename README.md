# Proxmox-SPICE-Client-Helper
I use the virt-manager or virt-viewer as Proxmox SPICE client. This helper downloads a current .vv file and then executes it accordingly.

> [!NOTE]  
> You may want to make several VMs executable in this way. You then have to create each VM individually and for each VM you then need a new restricted user in Proxmox and a new API token for this new user. The Python script must then also be copied and adapted several times for each VM. The same applies to the batch/shell/bash script.

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

### Datacenter

You want two things: on the one hand, a restricted user who can only operate the VM and, on the other, that he does not connect to the web interface if possible. In other words, they should not be able to log in using a password. It is therefore advisable to use the API token. The script can only be used to obtain access data for the REST API, but not to log in to the web interface. He does not know the correct login data. This also means that they cannot change the account password and you can continue to administer this account.

#### Users

First you have to create a new user. To do this, first click on `Datacenter`, then on `Permissions` and then on `Users`. By clicking on the `Add` button you can create your new user. Inside `User name` you can choose the name of your user. In my example I used `limiteduser`. Then you have to select `Proxmox VE authentication server` as `Realm`. This is needes because the user should be limited to only control the VM and he needs an access via the REST API. You can fill in the remaining fields as you wish or leave them blank.

![Users](https://raw.githubusercontent.com/Michdo93/test2/refs/heads/main/proxmox_datacenter_users.png)

#### API Tokens

In the next step, click on `Datacenter`, then also on `Permissions` and then on `API Tokens`. Then click on the `Add` button. As `User` you have to choose your user. In my case I used `limiteduser@pve`. Please notice that you have to choose `<user_name>@<realm>`. You can then assign a name for the `Token ID`. If you want, you can specify under 'Expire' when this token expires. I have simply selected `Never`. If you now click on `Add`, a `Secret` will appear in the next step, which you should copy and keep safe. Maybe just use a password manager like KeePass to store the secret of the token. You may also need several user accounts, so it doesn't hurt to keep them somewhere safe.

![API Tokens](https://raw.githubusercontent.com/Michdo93/test2/refs/heads/main/proxmox_datacenter_api_tokens.png)

#### Roles

In the next step, click on `Datacenter`, then also on `Permissions` and then on `Roles`. After that you click on `Create`. For `Name` I choosed `VMViewer` but you can name it like you want. I found the name to be the most obvious and self-explanatory. On `Privileges` you select `VM.Audit`, `VM.Console` and `VM.PowerMgmt`. After adding the role it looks like this:

![Roles](https://raw.githubusercontent.com/Michdo93/test2/refs/heads/main/proxmox_datacenter_roles.png)

### VM

#### Hardware

At first you have to select your VM and go to `Hardware`. Make sure that `Display` is set to `SPICE`. I left the `BIOS` on the `Default (SeaBIOS)` setting, also Machine with `Default (i440fx)`. In my configuration the `SCSI Controller` is set to `VirtIO SCSI single`. I think you can customize your VM to your desire. Then I clicked on the `Add` button and choose `USB device`. There you have to select `Spice Port`. Maybe you will create two or three USB devices. Then I added an `Audi Device` by also clicking at first on the `Add` button and selected then `Audio device`. As `Audio Device` I selected `ich9-intel-hda` and as `Backend Driver` I selected `SPICE`. Maybe you have to choose a similar configuration.

![Hardware](https://raw.githubusercontent.com/Michdo93/test2/refs/heads/main/proxmox_vm_hardware.png)

#### Options

In the next step you will click on `Options`. Make sure that `Start at boot` is activated, because later you will not login to Proxmox and start the VM manually if the server will reboot.

![Options](https://raw.githubusercontent.com/Michdo93/test2/refs/heads/main/proxmox_vm_options.png)

#### Permissions

In the last step you will click on the `Permissions` tab. Then you click `Add` and choose `API Token Permission`. In the next step you will select your `API token` (in my examle `limiteduser@pve!limiteduser-token`) on `API Token` and inside `Role` you choose `VMViewer`. After that you click on `Add`. Then you also had to add the `User Permission` by clicking again on `Add`. For `User` you have then to select your user (in my case `limiteduser@pve`) and inside `Role` you choose `VMViewer`. It is important that you add both permissions, otherwise running the VM will not work. At the end this looks like this.

![Permissions](https://raw.githubusercontent.com/Michdo93/test2/refs/heads/main/proxmox_vm_permissions.png)

## VM Configuration (inside the VM)

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

## Customize the Python Script

At the top of the Python script you can configure and customize the following:

```
# Set auth options (Token and Secret)
APITOKEN = ''  # Token (Username@Realm!TokenID)
APISECRET = ''  # Secret for the token

# Set VM ID and Node
VMID = ""
NODE = ""
PROXY = "" # IP or hostname
PORT = 8006
```

In my example the `VMID` was `102` and the `NODE` was `pve`.

## Usage

As example it will look like this:

![Example](https://raw.githubusercontent.com/Michdo93/test2/refs/heads/main/proxmox_virt_viewer.png)

### Windows


### Linux


