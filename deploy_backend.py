import os
from ftp_helper import connect_to_ftp, upload_directory

print("Kiệt yêu cầu không deploy backend lên FTP nữa mà chỉ chạy ở local thôi. Phiên bản hiện tại trên FTP là tối ưu nhất để mạch Yolobit gửi nhận dữ liệu, nếu deploy bản full lên thì tốc độ load sẽ rất chậm ảnh hưởng đến hoạt động của mạch Yolobit.")

# # FTP server configuration
# FTP_HOST = "ftp.akng.io.vn"
# FTP_USER = "sams_backend@sams.akng.io.vn"
# FTP_PASS = "Doandanganh123!"
# FTP_TARGET_DIR = ""

# # Local backend directory
# LOCAL_BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")

# if __name__ == "__main__":
#     # Step 1: Connect to the FTP server
#     ftp = connect_to_ftp(FTP_HOST, FTP_USER, FTP_PASS)

#     # Step 2: Upload the backend directory to the FTP server
#     print("Uploading backend directory to FTP server...")
#     upload_directory(ftp, LOCAL_BACKEND_DIR, FTP_TARGET_DIR)

#     # Step 3: Close the FTP connection
#     ftp.quit()
#     print("Upload completed.")