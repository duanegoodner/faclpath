# source code
# shamelessly copied from
# https://itnext.io/containers-terminating-with-grace-d19e0ce34290
# which had shamelessly copied from
# https://stackoverflow.com/a/31464349/2591014

import signal
import time


class GracefulKiller:
    kill_now = False
    signals = {signal.SIGINT: "SIGINT", signal.SIGTERM: "SIGTERM"}

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        print("\nReceived {} signal".format(self.signals[signum]))
        print("Cleaning up resources. End of the program")
        self.kill_now = True


if __name__ == "__main__":
    killer = GracefulKiller()
    print("Running ...")
    while not killer.kill_now:
        time.sleep(1)
