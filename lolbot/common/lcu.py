import psutil
import os

class ProcessInfo:
    def __init__(self, client_name):
        self.client_name = client_name
        self.current_user = self.get_current_user()
        self.process = self.find_process_by_name(client_name)
        if self.process:
            self.command_line = self.process.cmdline()
        else:
            self.command_line = []

    def get_current_user(self):
        """Retrieve the current username."""
        return os.getlogin()

    def find_process_by_name(self, process_name):
        """Find the process by name and confirm it's run by the current user."""
        for process in psutil.process_iter(['pid', 'name', 'username']):
            if process.info['name'] == process_name and self.is_current_user(process.info['username']):
                return process
        return None

    def is_current_user(self, process_username):
        """Check if the process is run by the current user."""
        return process_username.endswith(f'\\{self.current_user}')

    def get_commandline_arg(self, arg_prefix):
        """Get specific command-line argument value."""
        for arg in self.command_line:
            if arg.startswith(arg_prefix):
                return arg[len(arg_prefix):]
        return None

class LeagueClientInfo(ProcessInfo):
    def __init__(self):
        super().__init__("LeagueClientUx.exe")
        self.remoting_auth_token = self.get_commandline_arg("--remoting-auth-token=")
        self.port = self.get_commandline_arg("--app-port=")

class RiotClientInfo(ProcessInfo):
    def __init__(self):
        super().__init__("RiotClientUx.exe")
        self.remoting_auth_token = self.get_commandline_arg("--remoting-auth-token=")
        self.port = self.get_commandline_arg("--app-port=")
        self.riotclient_auth_token = self.get_commandline_arg("--riotclient-auth-token=")
        self.riotclient_app_port = self.get_commandline_arg("--riotclient-app-port=")