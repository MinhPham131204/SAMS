import os
import subprocess
from ftp_helper import connect_to_ftp, upload_directory

# FTP server configuration
FTP_HOST = "ftp.akng.io.vn"
FTP_USER = "sams_frontend@sams.akng.io.vn"
FTP_PASS = "Doandanganh123!"
FTP_TARGET_DIR = ""

# Local ReactJS project directory
REACT_PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
BUILD_DIR = os.path.join(REACT_PROJECT_DIR, "build")

def build_react_project():
    """Build the ReactJS project."""
    print("Building ReactJS project...")
    try:
        subprocess.run(["npm", "run", "build"], cwd=REACT_PROJECT_DIR, check=True, shell=True)
        print("Build completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during build: {e}")
        exit(1)

if __name__ == "__main__":
    # Step 1: Build the ReactJS project
    build_react_project()

    # Step 2: Connect to the FTP server
    ftp = connect_to_ftp(FTP_HOST, FTP_USER, FTP_PASS)

    # Step 3: Upload the build directory to the FTP server
    print("Uploading build directory to FTP server...")
    upload_directory(ftp, BUILD_DIR, FTP_TARGET_DIR)

    # Step 4: Close the FTP connection
    ftp.quit()
    print("Upload completed.")