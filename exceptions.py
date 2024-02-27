class RetryNeeded(Exception):
    def __init__(self):
        super().__init__()
