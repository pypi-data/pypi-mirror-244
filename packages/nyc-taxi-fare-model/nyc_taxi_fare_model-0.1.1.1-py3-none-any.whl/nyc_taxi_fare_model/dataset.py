from typing import TYPE_CHECKING, List

import torch
from torch.utils.data import Dataset

if TYPE_CHECKING:
    from pyspark.sql.dataframe import DataFrame


class NycTaxiFareDataset(Dataset):
    def __init__(self, dataframe: 'DataFrame', feature_cols: List[str], label_col: str):
        self.data = dataframe.select(*feature_cols).collect()
        self.labels = dataframe.select(label_col).collect()
        self.input_size = len(self.data[0])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        input_x = torch.tensor(self.data[idx], dtype=torch.float32)
        label = torch.tensor(self.labels[idx], dtype=torch.float32)
        return input_x, label
