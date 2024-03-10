import csv
import logging
from ftplib import FTP, error_perm

# Configure logging
logging.basicConfig(filename='ftp_delete.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)


def connect_to_ftp(server, username, password, port=2121):  # Added port parameter with default value 21
    try:
        ftp = FTP()
        ftp.connect(host=server, port=port)  # Connect using the specified port
        ftp.login(username, password)
        logging.info('Connected to FTP server successfully')
        return ftp
    except Exception as e:
        logging.error(f'Failed to connect to FTP server: {e}')
        raise

def delete_files_from_ftp(ftp, file_paths):
    for file_path in file_paths:
        try:
            ftp.delete(file_path)
            logging.info(f'File deleted successfully: {file_path}')
        except error_perm as e:
            logging.warning(f'Permission denied when trying to delete {file_path}: {e}')
        except Exception as e:
            logging.error(f'Failed to delete {file_path}: {e}')

def read_csv_file(file_path):
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            file_paths = [row[0] for row in csv_reader]
            logging.info(f'CSV file read successfully: {file_path}')
            return file_paths
    except Exception as e:
        logging.error(f'Failed to read CSV file: {e}')
        raise

def main():
    ftp_server = '192.168.200.207'
    ftp_username = 'Shane'
    ftp_password = 'password'
    ftp_port = 2121  # Example custom port, replace with the actual port number
    csv_file_path = 'files-to-delete.csv'
    
    ftp = None  # Initialize ftp variable to None
    

    try:
        ftp = None  # Initialize ftp variable to None
        file_paths = read_csv_file(csv_file_path)
        # Pass the custom port number when connecting
        ftp = connect_to_ftp(ftp_server, ftp_username, ftp_password, ftp_port)
        delete_files_from_ftp(ftp, file_paths)
    except Exception as e:
        logging.error(f'An error occurred: {e}')
    finally:
        if ftp:  # Check if ftp is not None before trying to close the connection
            ftp.quit()
            logging.info('FTP connection closed')

if __name__ == "__main__":
    main()