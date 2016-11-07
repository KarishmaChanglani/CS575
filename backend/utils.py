class Try:
    def __init__(self, func):
        self.value = self.error = None
        try:
            self.value = func()
        except BaseException as e:
            self.error = e

    @property
    def success(self):
        # Keyed off of error because func could return None
        return self.error is None

    @property
    def failure(self):
        return self.error is not None

    def map(self, func):
        if self.success:
            try:
                self.value = func(self.value)
            except BaseException as e:
                self.error = e
