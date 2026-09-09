from abc import ABC, abstractmethod
import pandas as pd

class ERPInterface(ABC):

    @abstractmethod
    def get_customers(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_sales(self) -> pd.DataFrame:
        pass
