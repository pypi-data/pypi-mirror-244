import numpy as np

import torch
import torch.nn as nn

from sklearn.preprocessing import OneHotEncoder


class BaseGenerator:
    """
    BaseGenerator class provides the base of all GANs.

    All GANs derive from BaseGenerator and inherit its methods and properties
    """

    def __init__(self, discriminator, generator, random_state):
        self.dim_ = 0
        self.n_classes_ = 0
        self.device_ = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.random_state_ = random_state

        self.gen_samples_ratio_ = None
        self.x_train_per_class_ = None

        # Class encoder
        self.class_encoder_ = OneHotEncoder()

        # Optional classification model for evaluating the effectiveness of this GAN
        self.test_classifier_ = None

        # Discriminator parameters (object, architecture, optimizer)
        self.D_ = None
        self.D_Arch_ = discriminator
        self.D_optimizer_ = None

        # Generator parameters (object, architecture, optimizer)
        self.G_ = None
        self.G_Arch_ = generator
        self.G_optimizer_ = None

    def display(self):
        self.D_.display()
        self.G_.display()

    def prepare(self, x_train, y_train):
        y_train = self.class_encoder_.fit_transform(y_train.reshape(-1, 1)).toarray()

        train_data = np.concatenate((x_train, y_train), axis=1)
        training_data = torch.from_numpy(train_data).to(torch.float32)

        self.dim_ = x_train.shape[1]
        self.n_classes_ = y_train.shape[1]

        # Determine how to sample the conditional GAN in smart training
        self.gen_samples_ratio_ = [int(sum(y_train[:, c])) for c in range(self.n_classes_)]
        # gen_samples_ratio.reverse()

        # Class specific training data for smart training (KL/JS divergence)
        self.x_train_per_class_ = []
        for y in range(self.n_classes_):
            x_class_data = np.array([x_train[r, :] for r in range(y_train.shape[0]) if y_train[r, y] == 1])
            x_class_data = torch.from_numpy(x_class_data).to(torch.float32).to(self.device_)

            self.x_train_per_class_.append(x_class_data)

        return training_data

    def sample(self, num_samples, y=None):
        if y is None:
            latent_classes = torch.from_numpy(np.random.randint(0, self.n_classes_, num_samples)).to(torch.int64)
            latent_y = nn.functional.one_hot(latent_classes, num_classes=self.n_classes_).to(self.device_)
        else:
            latent_y = nn.functional.one_hot(torch.full(size=(num_samples,), fill_value=y), num_classes=self.n_classes_)

        latent_x = torch.randn((num_samples, self.dim_))

        # concatenate, copy to device, and pass to generator
        latent_data = torch.cat((latent_x, latent_y), dim=1).to(self.device_)

        return self.G_(latent_data)
