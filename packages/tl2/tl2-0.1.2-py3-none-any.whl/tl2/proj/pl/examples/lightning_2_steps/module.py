import os

import torch
from torch import nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, random_split
from torchvision import transforms
from torchvision.datasets import MNIST

import pytorch_lightning as pl

from tl2.launch.launch_utils import update_parser_defaults_from_yaml, global_cfg
from tl2.modelarts import moxing_utils


class LitAutoEncoder(pl.LightningModule):
  def __init__(self):
    super().__init__()
    self.encoder = nn.Sequential(nn.Linear(28 * 28, 64), nn.ReLU(), nn.Linear(64, 3))
    self.decoder = nn.Sequential(nn.Linear(3, 64), nn.ReLU(), nn.Linear(64, 28 * 28))
    pass
  
  def forward(self, x):
    # in lightning, forward defines the prediction/inference actions
    embedding = self.encoder(x)
    return embedding
  
  def training_step(self, batch, batch_idx):
    # training_step defined the train loop.
    # It is independent of forward
    x, y = batch
    x = x.view(x.size(0), -1)
    z = self.encoder(x)
    x_hat = self.decoder(z)
    loss = F.mse_loss(x_hat, x)
    # Logging to TensorBoard by default
    self.log("train_loss", loss)
    return loss
  
  def configure_optimizers(self):
    optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
    return optimizer
  

def main():
  
  update_parser_defaults_from_yaml(parser=None)
  
  dataset = MNIST(global_cfg.data_dir, download=True, transform=transforms.ToTensor())
  train_loader = DataLoader(dataset,
                            batch_size=32,
                            shuffle=True)
  
  # init model
  autoencoder = LitAutoEncoder()

  # most basic trainer, uses good defaults (auto-tensorboard, checkpoints, logs, and more)
  # trainer = pl.Trainer(gpus=8) (if you have GPUs)
  trainer = pl.Trainer(gpus=torch.cuda.device_count(), log_gpu_memory=True)
  trainer.fit(autoencoder, train_loader)
  
  pass
  
if __name__ == '__main__':
  main()