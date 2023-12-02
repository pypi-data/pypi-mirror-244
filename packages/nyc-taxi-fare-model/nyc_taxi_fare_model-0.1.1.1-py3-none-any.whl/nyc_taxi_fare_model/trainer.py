from typing import TYPE_CHECKING, Dict, List
import json

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm
import mlflow
from mlflow.models.signature import infer_signature
from mlflow.entities.model_registry.model_version import ModelVersion
from torchmetrics.regression import MeanSquaredError, R2Score

from nyc_taxi_fare_model.dataset import NycTaxiFareDataset
from nyc_taxi_fare_model.model import NycTaxiFareRegressionModel

if TYPE_CHECKING:
    from pyspark.sql.dataframe import DataFrame


def get_data_loader(df: 'DataFrame', feature_cols: List[str], label_cols: str, batch_size=128, shuffle=True):
    train_dataset = NycTaxiFareDataset(df, feature_cols, label_cols)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=shuffle)
    return train_loader, train_dataset


def evaluate(model, test_loader) -> ('torch.Tensor', 'torch.Tensor'):
    mse_eval = MeanSquaredError()
    r2_eval = R2Score()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    with torch.no_grad():
        model.eval()

        labels_all = torch.Tensor([])
        pred_all = torch.Tensor([])
        labels_all = labels_all.to(device)
        pred_all = pred_all.to(device)

        for inputs, labels in tqdm(test_loader):
            inputs, labels = inputs.to(device), labels.to(device)

            pred = model(inputs)
            pred_squeezed = pred.squeeze(dim=1)
            labels_squeezed = labels.squeeze(dim=1)
            labels_all = torch.cat([labels_all, labels_squeezed])
            pred_all = torch.cat([pred_all, pred_squeezed])

        mse = mse_eval(pred, labels)
        mlflow.log_metric("MSE", mse)

        r2 = r2_eval(pred, labels)
        mlflow.log_metric("r_squared", r2)

        return inputs, pred


def train_model(
        df: 'DataFrame',
        feature_cols: list,
        label_col: str,
        experiment_name: str,
        model_name: str,
        model_hyperparams: Dict | str
        ) -> ModelVersion:

    print(f'Data shape: {df.count()} rows, {len(df.columns)} columns')

    if isinstance(model_hyperparams, str):
        model_hyperparams: Dict = json.loads(model_hyperparams)

    print(f'Feature columns: {feature_cols}')
    print(f'Label column: {label_col}')
    print(f'Model hyperparams: {model_hyperparams}')

    batch_size = model_hyperparams.get('batch_size', 128)

    df_split = df.randomSplit([0.8, 0.2])
    train_loader, train_ds = get_data_loader(df_split[0], feature_cols, label_col, batch_size, shuffle=True)
    test_loader, _ = get_data_loader(df_split[1], feature_cols, label_col, batch_size, False)

    input_size = train_ds.input_size

    model = NycTaxiFareRegressionModel(input_size)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    optimizer = optim.Adam(model.parameters(), lr=model_hyperparams.get('learning_rate', 0.001))
    criterion = nn.MSELoss()

    num_epochs = model_hyperparams.get('num_epochs', 10)
    # Training run
    mlflow.autolog(log_models=False)

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0

        for inputs, labels in tqdm(train_loader):
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            mlflow.log_metric("Train Loss", running_loss)

        train_loss = running_loss / len(train_loader)
        print(f'Epoch [{epoch + 1}/{num_epochs}] Train Loss: {train_loss:.4f}')
        mlflow.log_metric("Epoch Train Loss", running_loss)

    input_x, pred = evaluate(model, test_loader)
    input_example = df.select(feature_cols).limit(5).toPandas()
    output_example = df.select(label_col).limit(5).toPandas()

    # infer signature
    signature = infer_signature(input_example, output_example)

    artifact_path = "model"

    mlflow.pytorch.log_model(
        model,
        artifact_path=artifact_path,
        signature=signature,
        input_example=input_example,
        pip_requirements=[
            "tqdm==4.66",
            "torchmetrics==1.2.0",
            "nyc-taxi-fare-model"
        ]
    )

    return {}
