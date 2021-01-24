class StdinListenerThread(object):
    def __init__(self, porthole):
        self._porthole = porthole
        self._prompt = ":: "

    def run(self):
        while True:
            try:
                line = input().strip()
                if line != "":
                    self._porthole.set_code(line)
            except EOFError:
                break

    def set_prompt(self, str):
        self._prompt = set
