import os
from typing import Optional

import torch
from torch.nn import functional as F
from torch import nn
from torch.utils.data import DataLoader, random_split
from torchvision import transforms
from torchvision.datasets import MNIST

import pytorch_lightning as pl

from tl2.launch.launch_utils import update_parser_defaults_from_yaml, global_cfg


class MNISTDataModule(pl.LightningDataModule):
  def __init__(self,
               data_root="datasets/MNIST",
               batch_size=64):
    super().__init__()
    self.data_root = data_root
    self.batch_size = batch_size
    pass
  
  def prepare_data(self):
    # download only
    MNIST(self.data_root, train=True, download=True, transform=transforms.ToTensor())
    MNIST(self.data_root, train=False, download=True, transform=transforms.ToTensor())
    pass
  
  def setup(self,
            stage: Optional[str] = None):
    # transform
    transform = transforms.Compose([transforms.ToTensor()])
    mnist_train = MNIST(self.data_root, train=True, download=False, transform=transform)
    mnist_test = MNIST(self.data_root, train=False, download=False, transform=transform)
    
    # train/val split
    mnist_train, mnist_val = random_split(mnist_train,
                                          [55000, 5000])
    
    # assign to use in dataloaders
    self.train_dataset = mnist_train
    self.val_dataset = mnist_val
    self.test_dataset = mnist_test
    pass
  
  def train_dataloader(self):
    return DataLoader(self.train_dataset, batch_size=self.batch_size)
  
  def val_dataloader(self):
    return DataLoader(self.val_dataset, batch_size=self.batch_size)
  
  def test_dataloader(self):
    return DataLoader(self.test_dataset, batch_size=self.batch_size)


class LitMNIST(pl.LightningModule):
  def __init__(self):
    super().__init__()
    
    # mnist images are (1, 28, 28) (channels, height, width)
    self.layer_1 = nn.Linear(28 * 28, 128)
    self.layer_2 = nn.Linear(128, 256)
    self.layer_3 = nn.Linear(256, 10)
    pass
  
  def forward(self, x):
    batch_size, channels, height, width = x.size()
    
    # (b, 1, 28, 28) -> (b, 1*28*28)
    x = x.view(batch_size, -1)
    x = self.layer_1(x)
    x = F.relu(x)
    x = self.layer_2(x)
    x = F.relu(x)
    x = self.layer_3(x)
    
    x = F.log_softmax(x, dim=1)
    return x

  def configure_optimizers(self):
    return torch.optim.Adam(self.parameters(), lr=1e-3)
  
  def training_step(self,
                    batch,
                    batch_idx):
    x, y = batch
    logits = self(x)
    loss = F.nll_loss(logits, y)
    
    self.log('global_step', self.global_step, prog_bar=True)
    return loss


def main():
  dm = MNISTDataModule()
  model = LitMNIST()
  
  trainer = pl.Trainer(gpus=torch.cuda.device_count(),
                       default_root_dir=f"{global_cfg.tl_outdir}",
                       enable_progress_bar=False,
                       enable_checkpointing=False)
  trainer.fit(model, dm)
  pass


if __name__ == '__main__':
  update_parser_defaults_from_yaml(parser=None)
  main()
