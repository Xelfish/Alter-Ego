import paramiko

def sshCommand(pi, command):
    client = openSSH(pi)
    print('started exec of ' + command + '...')
    stdin, stdout, stderr = client.exec_command(command, get_pty=True)
    for line in iter(stdout.readline, ""):
        print(line, end="")
    print('finished.')
    client.close()

def connectToFtp(pi):
    client = openSSH(pi)
    ftp = client.open_sftp()
    return ftp

def openSSH(pi):
    print("connecting: ", pi)
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.connect(pi["ip"], username=pi["user"], password=pi["password"])
    return client

def save_on_ftp(outPi, local_path, remote_path):
    ftp = connectToFtp(outPi)
    ftp.put(local_path, remote_path)
    pass 