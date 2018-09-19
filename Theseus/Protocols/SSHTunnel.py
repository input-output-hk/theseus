import os
import select
import threading
import paramiko
import socketserver as SocketServer
import logging

__author__ = 'Amias Channer <amias.channer@iohk.io> for IOHK'
__doc__ = 'SSH Tunnel'
__all__ = ['SSHTunnel']


class SSHTunnel:
    """ SSH Tunnel - provides an ssh tunnel to connect your tests with a remote instance

    Our API is only available on 127.0.0.1 to protect it from the internet , this means if you want to access a remote
    instance you will need an SSH Tunnel to make it appear like its on 127.0.0.1.

    Args:
        user(str): username for the ssh connection
        host(str): hostname for the ssh connection
        port(str): port for the ssh connection (usually 22)
        localport(int): local port for the ssh forward to forward from
        remoteport(int): remote port for the ssh forward to forward to
        localhost(str):  local host for the ssh forward to forward from, defaults to 127.0.0.1
        remotehost(str): remote host for the ssh forward to forward to , defaults to 127.0.0.1


    Returns:
        SSHTunnel: a fully operating SSH tunnel.

    The tunnel will not accept passwords , you have to configure ssh keys in your OS underneath.
    This is much safer than putting login credentials in the tests.

    When you load this class the tunnel will be started and will run in a Thread.
    The Thread will run until either the connection drops or this the object goes out of scope.

    You will need to call the stop_tunnel method to shutdown your tunnel otherwise your test wont exit
    Hopefully this will be fixed soon and that wiil become a noop

    """
    def __init__(self,  user: str, host: str, port: int=22, localport: int=8090,
                 remoteport: int=8090,  localhost: str='127.0.0.1', remotehost: str='127.0.0.1'):

        # params for initial ssh to endpoint
        self._user = user
        self._host = host
        self._port = port

        # params for forwarding config
        self._localport = localport
        self._remoteport = remoteport
        self._remotehost = remotehost
        self._localhost = localhost

        self.logger = logging.getLogger('theseus.ssh-tunnel')

        self.client = paramiko.SSHClient()

        self.client.set_log_channel('theseus.ssh-tunnel')
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.load_system_host_keys()
        self.client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))

        self.thread = threading.Thread()
        self.server = ForwardServer
        self.start_tunnel()

    def __del__(self):
        self.logger.info('ssh tunnel exit')
        self.stop_tunnel()

    def start_tunnel(self):
        """ Start SSHTunnel - starts the ssh connection and tunnel

        This method is called at the end of this objects initialisation.
        This method accepts no parameters as the connection is already configured.
        If you have changed your SSH keys you will need to restart this object before they show up.
        """
        self.logger.info("Connecting to : {0}".format(self.host))
        try:
            self.client.connect(
                self.host,
                port=self._port,
                username=self.user,
            )
        except Exception as e:
            self.logger.error("Failed to connect: {0}".format(e))
            return

        local = "{0}:{1}".format(self._localhost, self._localport)
        remote = "{0}:{1}".format(self._remotehost, self._remoteport)

        self.logger.info("Configuring SSHTunnel: {0} to {1}".format(local, remote))
        try:
            self.forward_tunnel()
        except KeyboardInterrupt:
            self.logger.error("C-c: Port forwarding stopped.")
            return

    def stop_tunnel(self):
        """ Stop SSHTunnel - stop the ssh connection and tunnel """
        # this runs in a try catch encase
        self.logger.info("Attempting to close sshtunnel")
        try:
            temp = self.server
            temp.server_close()
            self.client.close()
        except Exception as e:
            self.logger.error('Something bad happened during shutdown of the ssh tunnel: {0}'.format(e))

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def localport(self):
        return self._localport

    @localport.setter
    def localport(self, value):
        self._localport = value

    @property
    def remoteport(self):
        return self._remoteport

    @remoteport.setter
    def remoteport(self, value):
        self._remoteport = value

    @property
    def remotehost(self):
        return self._remotehost

    @remotehost.setter
    def remotehost(self, value):
        self._remotehost = value

    @property
    def localhost(self):
        return self._localhost

    @localhost.setter
    def localhost(self, value):
        self._localhost = value

    def forward_tunnel(self):
        # this is a little convoluted, but lets me configure things for the Handler
        # object.  (SocketServer doesn't give Handlers any way to access the outer
        # server normally.)
        transport = self.client.get_transport()
        remote_host = self.remotehost
        remote_port = self.remoteport

        class SubHander(Handler):
            self.logger = logging.getLogger('theseus.ssh-sub-handler')
            chain_host = remote_host
            chain_port = remote_port
            ssh_transport = transport

        self.server = ForwardServer(("", self.localport), SubHander)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()


class ForwardServer(SocketServer.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def server_close(self):
        self.__shutdown_request = True


class Handler(SocketServer.BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        # add a logger then run the super class passing on all args
        self.logger = logging.getLogger('theseus.ssh_handler')
        super().__init__(*args, **kwargs)

    def handle(self):
        try:
            chan = self.ssh_transport.open_channel(
                "direct-tcpip",
                (self.chain_host, self.chain_port),
                self.request.getpeername(),
            )
        except Exception as e:
            self.logger.error(
                "Incoming request to %s:%d failed: %s"
                % (self.chain_host, self.chain_port, repr(e))
            )
            return
        if chan is None:
            self.logger.error(
                "Incoming request to %s:%d was rejected by the SSH server."
                % (self.chain_host, self.chain_port)
            )
            return

        self.logger.debug(
            "Connected!  SSHTunnel open %r -> %r -> %r"
            % (
                self.request.getpeername(),
                chan.getpeername(),
                (self.chain_host, self.chain_port),
            )
        )
        while True:
            r, w, x = select.select([self.request, chan], [], [])
            if self.request in r:
                data = self.request.recv(1024)
                if len(data) == 0:
                    break
                chan.send(data)
            if chan in r:
                data = chan.recv(1024)
                if len(data) == 0:
                    break
                self.request.send(data)

            if self.server._BaseServer__is_shut_down.is_set():
                self.logger.debug('Closing tunnel due to shutdown request.')
                break

        peername = self.request.getpeername()
        chan.close()
        self.request.close()
        self.logger.debug("SSHTunnel closed from %r" % (peername,))
