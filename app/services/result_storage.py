from main import main

class ResultStorage:
    def __init__(self):
        self.results = None

    def run(self, k: int):
        self.results = main(K=k, n_init=5)
        return self.results

    def clear(self):
        self.results = None

service = ResultStorage()