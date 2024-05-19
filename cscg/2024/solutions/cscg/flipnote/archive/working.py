import paramiko
import paramiko.auth_strategy

class AuthStrategy(paramiko.auth_strategy.AuthStrategy):

    def __init__(self, ssh_config, username):
        super().__init__(ssh_config)
        self.username = username

    def get_sources(self):
        yield paramiko.auth_strategy.NoneAuth(self.username)

hostname = 'hostname'
username = 'user'

hostname = "challenge.cscg.live"
username = "4f415a69cde0b525fa04242b-1024-flipnote"

ssh_config = paramiko.SSHConfig()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

auth_strategy = AuthStrategy(ssh_config, username)
ssh.connect(hostname, auth_strategy=auth_strategy,port = 2222)
stdin, stdout, stderr = ssh.exec_command('ls -l /')
print(stdout.read().decode())
