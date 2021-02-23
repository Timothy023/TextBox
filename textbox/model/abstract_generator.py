# @Time   : 2020/11/5
# @Author : Junyi Li, Gaole He
# @Email  : lijunyi@ruc.edu.cn

# UPDATE:
# @Time   : 2021/1/30
# @Author : Tianyi Tang
# @Email  : steventang@ruc.edu.cn

"""
textbox.model.abstract_generator
##################################
"""

import numpy as np
import torch
import torch.nn as nn

from textbox.utils import ModelType


class AbstractModel(nn.Module):
    r"""Base class for all models
    """

    def calculate_loss(self, corpus):
        r"""Calculate the training loss for a batch data.

        Args:
            corpus (Corpus): Corpus class of the batch.

        Returns:
            torch.Tensor: Training loss, shape: []
        """
        raise NotImplementedError

    def generate(self, corpus):
        r"""Predict the texts conditioned on a noise or sequence.

        Args:
            corpus (Corpus): Corpus class of the batch.

        Returns:
            torch.Tensor: Generated text, shape: [batch_size, max_len]
        """
        raise NotImplementedError

    def calculate_nll_test(self, eval_data):
        r"""Calculate the negative log-likelihood of the batch.

        Args:
            eval_data (Corpus): Corpus class of the batch.

        Returns:
            torch.FloatTensor: NLL_test of eval data
        """
        raise NotImplementedError

    def __str__(self):
        """
        Model prints with number of trainable parameters
        """
        model_parameters = filter(lambda p: p.requires_grad, self.parameters())
        params = sum([np.prod(p.size()) for p in model_parameters])
        return super().__str__() + '\nTrainable parameters: {}'.format(params)


class UnconditionalGenerator(AbstractModel):
    """This is a abstract general unconditional generator. All the unconditional model should implement this class.
    The base general unconditional generator class provide the basic parameters information.
    """
    type = ModelType.UNCONDITIONAL

    def __init__(self, config, dataset):
        super(AbstractModel, self).__init__()

        self.vocab_size = len(dataset.idx2token)

        # load parameters info
        self.batch_size = config['train_batch_size']
        self.device = config['device']


class Seq2SeqGenerator(AbstractModel):
    """This is a abstract general seq2seq generator. All the seq2seq model should implement this class.
    The base general seq2seq generator class provide the basic parameters information.
    """
    type = ModelType.SEQ2SEQ

    def __init__(self, config, dataset):
        super(AbstractModel, self).__init__()

        if hasattr(dataset, "source_idx2token"):
            self.source_vocab_size = len(dataset.source_idx2token)
            self.target_vocab_size = len(dataset.target_idx2token)
        else:
            self.vocab_size = len(dataset.idx2token)

        # load parameters info
        self.batch_size = config['train_batch_size']
        self.device = config['device']


class GenerativeAdversarialNet(UnconditionalGenerator):
    """This is a abstract general generative adversarial network. All the GAN model should implement this class.
    The base general generative adversarial network class provide the basic parameters information.
    """
    type = ModelType.GAN

    def __init__(self, config, dataset):
        super(GenerativeAdversarialNet, self).__init__(config, dataset)

    def calculate_g_train_loss(self, corpus):
        r"""Calculate the generator training loss for a batch data.

        Args:
            corpus (Corpus): Corpus class of the batch.

        Returns:
            torch.Tensor: Training loss, shape: []
        """
        raise NotImplementedError

    def calculate_d_train_loss(self, real_data, fake_data):
        r"""Calculate the discriminator training loss for a batch data.

        Args:
            real_data (torch.LongTensor): Real data of the batch, shape: [batch_size, max_seq_length]
            fake_data (torch.LongTensor): Fake data of the batch, shape: [batch_size, max_seq_length]

        Returns:
            torch.Tensor: Training loss, shape: []
        """
        raise NotImplementedError

    def calculate_g_adversarial_loss(self):
        r"""Calculate the adversarial generator training loss for a batch data.

        Returns:
            torch.Tensor: Training loss, shape: []
        """
        raise NotImplementedError

    def sample(self, sample_num):
        r"""Sample sample_num padded fake data generated by generator.

        Args:
            sample_num (int): The number of padded fake data generated by generator.

        Returns:
            torch.LongTensor: Fake data generated by generator, shape: [sample_num, max_seq_length]
        """
        raise NotImplementedError


class AttributeGenerator(AbstractModel):
    """This is a abstract general attribute generator. All the attribute model should implement this class.
    The base general attribute generator class provide the basic parameters information.
    """
    type = ModelType.ATTRIBUTE

    def __init__(self, config, dataset):
        super(AbstractModel, self).__init__()

        self.vocab_size = len(dataset.idx2token)
        self.attribute_size = [len(a2t) for a2t in dataset.idx2attribute]
        self.attribute_num = len(self.attribute_size)

        # load parameters info
        self.batch_size = config['train_batch_size']
        self.device = config['device']
