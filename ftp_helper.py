import os
from ftplib import FTP

def connect_to_ftp(host, user, password):
    """Connect to the FTP server and return the FTP object."""
    print(f"Connecting to FTP server: {host}...")
    ftp = FTP(host)
    ftp.login(user, password)
    print(f"Connected !")
    return ftp


def upload_file(ftp, local_file_path, remote_file_path):
    """Upload a single file to the FTP server."""
    with open(local_file_path, "rb") as file:
        ftp.storbinary(f"STOR {remote_file_path}", file)
    print(f"Uploaded: {local_file_path} -> {remote_file_path}")


def upload_directory(ftp, local_dir, remote_dir):
    """Recursively upload a directory to the FTP server."""
    if not os.path.isdir(local_dir):
        print(f"Local directory does not exist: {local_dir}")
        return

    # Change to the target directory on the FTP server
    try:
        ftp.cwd(remote_dir)
    except Exception:
        ftp.mkd(remote_dir)
        ftp.cwd(remote_dir)

    for item in os.listdir(local_dir):
        local_path = os.path.join(local_dir, item)
        remote_path = f"{remote_dir}/{item}"

        if os.path.isdir(local_path):
            # Recursively upload subdirectories
            upload_directory(ftp, local_path, remote_path)
        else:
            # Upload files
            upload_file(ftp, local_path, remote_path)
