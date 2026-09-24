from main import main

class ResultStorage:
    def __init__(self):
        self.results = None
        self.db_config = None
        self.table_config = None
        self.is_connected = False
        self.analysis_config = None

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

    def set_table_config(self, table_config: dict):
            self.table_config = table_config

    def set_analysis_config(self, analysis_config: dict):
        self.analysis_config = analysis_config
        
service = ResultStorage()