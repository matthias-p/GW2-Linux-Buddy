import os
import subprocess
import time
from pathlib import Path
from typing import Union, Callable
import shutil

from game_utils.exceptions.process_already_running_exception import ProcessAlreadyRunningException
from game_utils.exceptions.process_not_running_exception import ProcessNotRunningException


class Client:
    def __init__(self, name: str, wineprefix_path: Path, gamelauncher_path: Path):
        self.name = name
        self.wineprefix_path = wineprefix_path
        self.gamelauncher_path = gamelauncher_path

        self.process: Union[subprocess.Popen, None] = None

        if not wineprefix_path.exists():
            wineprefix_path.mkdir()

    def launch(self, arguments=None, wait_for_exit=False):
        if self.process is not None:
            raise ProcessAlreadyRunningException(f"Process is running with PID={self.process.pid}")

        if arguments is None:
            arguments = []

        self.process = subprocess.Popen(["wine", self.gamelauncher_path] + arguments,
                                        env=dict(os.environ, WINEPREFIX=self.wineprefix_path),
                                        stderr=subprocess.DEVNULL)

        if wait_for_exit:
            self.process.wait()

    def stop(self):
        if self.process is None:
            raise ProcessNotRunningException("Process is not running")

        self.process.terminate()

    def poll_status(self, callback: Callable) -> int:
        if self.process is None:
            raise ProcessNotRunningException("Process is not Running")

        process_code = self.process.poll()
        while process_code is None:
            time.sleep(.5)
            process_code = self.process.poll()

        self.process = None
        callback(self)
        return process_code

    def remove(self):
        if self.process is not None:
            self.process.terminate()
        if self.wineprefix_path.exists():
            shutil.rmtree(self.wineprefix_path)
