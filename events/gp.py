import requests
from subprocess import Popen, PIPE, STDOUT
import boto3
import zipfile, os

def backupToZip(folder, zfname):

    cwdpath = os.getcwd() # save original path (*where you run this py file)

    saveToWhere = fr'/tmp/{zfname}.zip'
    zf = zipfile.ZipFile(saveToWhere, mode='w')

    os.chdir(folder) # change to that absolute path

    for foldername, subfolders, filenames in os.walk('./'):
        if not '.git' in foldername:
            for filename in filenames:
                zf.write(os.path.join(foldername, filename))    
    zf.close()

    os.chdir(cwdpath)

    return


def pull_up(account, fname, branch, bucketName):
    """
    Clones through SSH a Github 'branch' from repo = 'fname' from 
    github account = 'account', zips it and uploads it to the 
    S3 bucket with name 'bucketName'.
    """

    clone_cmd = fr'git clone -b {branch} git@github.com:{account}/{fname}.git /tmp/{fname}'
    p1 = Popen(clone_cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

    backupToZip(fr'/tmp/{fname}', fr'{fname}-{branch}')

    Key = fr'/tmp/{fname}-{branch}.zip'
    outPutname = fr'{fname}-{branch}.zip'

    s3 = boto3.client('s3')
    s3.upload_file(Key, bucketName, outPutname)
    boto3.resource('s3').ObjectAcl(bucketName, Key).put(ACL='public-read')

    rm1_cmd = fr'rm -r --force /tmp/{fname}'
    p2 = Popen(rm1_cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

    rm2_cmd = fr'rm /tmp/{fname}-{branch}.zip'
    p3 = Popen(rm2_cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

    return

# if __name__ == '__main__':
#     pull_up(r'dfcastap', r'apipushgo', r'master')

