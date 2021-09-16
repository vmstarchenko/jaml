from .environment import JimlEnvironment


class EnvOptions:
    def __init__(self):
        self._values = {}
        self._env = None
        self.update({})

    def update(self, values):
        self._values.update(values)
        self._env = JimlEnvironment(**self._values)

    def get_values(self):
        return self._values

    def get_env(self):
        return self._env


config = EnvOptions()
