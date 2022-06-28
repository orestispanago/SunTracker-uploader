import os
import glob
import pysftp
from ftplib import FTP


ftp_ip = ""
ftp_user = ""
ftp_password = ""
ftp_dir = ""


sftp_host = ""
sftp_user = ""
sftp_password = ""
sftp_dir = ""
sftp_subdir = ""
known_hosts_file = ""


local_files = glob.glob('*.csv')

def upload_to_ftp(local_files, ftp_ip, ftp_user, ftp_password, ftp_dir):
    with FTP(ftp_ip, ftp_user, ftp_password) as ftp:
        ftp.cwd(ftp_dir)
        for local_file in local_files:
            with open(local_file, 'rb') as f:
                ftp.storbinary(f'STOR {local_file}', f)  


def upload_to_sftp(local_files, sftp_host, sftp_user, sftp_password, 
                   known_hosts_file, sftp_dir, sftp_subdir):
    cnopts = pysftp.CnOpts(knownhosts=known_hosts_file)
    with pysftp.Connection(sftp_host, username=sftp_user, password=sftp_password, 
                           cnopts=cnopts) as sftp:
        sftp.cwd(sftp_dir)
        if sftp_subdir not in sftp.listdir():
            sftp.mkdir(sftp_subdir)
        sftp.chdir(sftp_subdir)
        for local_file in local_files:
            sftp.put(local_file)

def archive_uploaded(local_files):
    if len(local_files) > 1:
        for local_file in local_files[:-1]:
            os.rename(local_file, f"uploaded/{local_file}")

  
upload_to_ftp(local_files, ftp_ip, ftp_user, ftp_password, ftp_dir)
upload_to_sftp(local_files, sftp_host, sftp_user, sftp_password, 
                known_hosts_file, sftp_dir, sftp_subdir)
archive_uploaded(local_files)
