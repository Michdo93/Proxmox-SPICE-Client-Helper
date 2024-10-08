import requests
import os
import subprocess
import platform

# Set auth options (Token and Secret)
APITOKEN = ''  # Token (Username@Realm!TokenID)
APISECRET = ''  # Secret for the token

# Set VM ID and Node
VMID = ""
NODE = ""
PROXY = "" # IP or hostname
PORT = 8006

# Create the SPICE proxy request URL
SPICEPROXY_URL = f'https://{PROXY}:{PORT}/api2/json/nodes/{NODE}/qemu/{VMID}/spiceproxy'
print(f"Requesting SPICE proxy from: {SPICEPROXY_URL}")

# Set headers for the request
headers = {
    "Authorization": f"PVEAPIToken={APITOKEN}={APISECRET}"
}

# Set data for the POST request
data = {"proxy": PROXY}

try:
    # Send the request to SPICE proxy
    response = requests.post(SPICEPROXY_URL, headers=headers, data=data, verify=False)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        response_data = response.json().get("data", {})
        
        # Prepare the .vv file content
        vv_content = (
            f"[virt-viewer]\n"
            f"ca={response_data.get('ca', '').replace('\\n', '\\n')}\n"
            f"secure-attention={response_data.get('secure-attention', '')}\n"
            f"proxy={response_data.get('proxy', '')}\n"
            f"title={response_data.get('title', '')}\n"
            f"password={response_data.get('password', '')}\n"
            f"type={response_data.get('type', '')}\n"
            f"host={response_data.get('host', '')}\n"
            f"release-cursor={response_data.get('release-cursor', '')}\n"
            f"tls-port={response_data.get('tls-port', '')}\n"
            f"toggle-fullscreen={response_data.get('toggle-fullscreen', '')}\n"
            f"delete-this-file=0\n"
            f"host-subject={response_data.get('host-subject', '')}\n"
        )

        # Save the SPICE proxy data to a .vv file in the user's home directory
        home_dir = os.path.expanduser("~")  # Get the user's home directory
        vv_file_path = os.path.join(home_dir, "spiceproxy.vv")

        with open(vv_file_path, "w") as file:
            file.write(vv_content)

        print("SPICE proxy file downloaded successfully.")
        print(f"Opening file: {vv_file_path}")

        # Determine the operating system and handle file opening accordingly
        if platform.system() == "Windows":
            # On Windows, use os.startfile to open the file
            os.startfile(vv_file_path)
        elif platform.system() == "Linux":
            # On Linux, open the file with virt-viewer
            try:
                subprocess.run(["virt-viewer", vv_file_path], check=True)
            except FileNotFoundError:
                print("virt-viewer is not installed or not in the system PATH.")
        else:
            print(f"Unsupported operating system: {platform.system()}")

    else:
        print(f"Failed to retrieve SPICE proxy data. HTTP Status Code: {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
