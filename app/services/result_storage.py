from main import main

class ResultStorage:
    def __init__(self):
        self.results = None
        self.db_config = None
        self.table_config = None
        self.is_connected = False

    def run(self, k: int):
        self.results = main(K=k, n_init=5)
        return self.results

    def clear(self):
        self.results = None
        self.db_config = None
        self.table_config = None
        self.is_connected = False

    def set_db_config(self, db_config: dict):
        self.db_config = db_config

service = ResultStorage()