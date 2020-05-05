import os
import time


class Tail:

    def __init__(self, t_file, socket):
        self.t_file = t_file
        self.socket = socket

    def send_updates(self, lines):
        print(lines)
        str = ""
        for line in lines:
            str = str + line + "</br>"
        data = {'data': str}
        self.socket.emit('response', data)

    def follow(self, t=1):
        if os.path.exists(self.t_file):
            perm = "a+"
        else:
            perm = "w+"
        with open(self.t_file, perm) as file_:
            file_.seek(0, 2)
            while True:
                curr_position = file_.tell()
                lines = file_.readlines()
                if not lines or len(lines) == 0:
                    file_.seek(curr_position)
                    time.sleep(t)
                else:
                    self.send_updates(lines)

    def tail(self, n=10, buffer=1024):
        with open(self.t_file) as f:
            f.seek(0, 2)
            l = 1 - f.read(1).count('\n')
            pos = f.tell()
            while l <= n and pos > 0:
                block = min(buffer, pos)
                pos -= block
                f.seek(pos, 0)
                l += f.read(block).count('\n')
            f.seek(pos, 0)
            l = min(l, n)
            lines = f.readlines()[-l:]
        self.send_updates(lines)

# if __name__ == "__main__":
#     tf = Tail("data.txt")
#     tf.tail()
