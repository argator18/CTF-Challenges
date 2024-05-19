import os
import selectors
import shutil
import signal
import socketserver
import subprocess
import tempfile
from os import fdopen

TIMEOUT = 60 * 10  # timeout after ten minutes


class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.sendall(
            f"[?] Please provide the boot disk in hex format.\n".encode()
        )
        self.request.sendall(f'[*] End your input with "EOF"\n'.encode())

        buffer = b""
        while b"EOF" not in buffer:
            buffer += self.request.recv(1024)
        buffer = buffer.replace(b"EOF", b"").lower()
        try:
            buffer = bytes(list(filter(lambda x: chr(x) in "0123456789abcdef", buffer)))

            data = bytes.fromhex(buffer.decode())
        except:
            self.request.sendall(f"[!] Invalid input... bye!\n".encode())
            return

        fd, disk_path = tempfile.mkstemp()
        with fdopen(fd, "wb") as f:
            f.write(data)

        # make sure we use the fresh vars every time
        shutil.copy("OVMF_VARS.fd", "OVMF_VARS_CURRENT.fd")
        os.chmod("OVMF_VARS_CURRENT.fd", 0o660)

        cmd = [
            "/usr/bin/qemu-system-x86_64",
            "-cpu",
            "max",
            "-machine",
            "q35",
            "-drive",
            "if=pflash,format=raw,readonly=on,unit=0,file=OVMF_CODE.fd",
            "-drive",
            "if=pflash,format=raw,unit=1,file=OVMF_VARS_CURRENT.fd",
            "-drive",
            f"file={disk_path},if=none,id=disk1,format=raw",
            "-device",
            "ide-hd,drive=disk1,bootindex=1",
            "-monitor",
            "none",
            "-display",
            "none",
            "-nographic",
        ]

        self.request.sendall(f"[*] Starting qemu, good luck!\n".encode())

        signal.signal(
            signal.SIGALRM,
            lambda _n, _f: [self.request.sendall(b"[!] Timed out..\n"), exit(1)],
        )
        signal.alarm(TIMEOUT)
        subprocess.call(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=self.request.fileno(),
            stderr=self.request.fileno(),
        )


with socketserver.ForkingTCPServer(("0.0.0.0", 1024), Handler) as server:
    server.allow_reuse_address = True
    with selectors.PollSelector() as selector:
        selector.register(server, selectors.EVENT_READ)
        while True:
            ready = selector.select(0.5)
            if ready:
                server._handle_request_noblock()
