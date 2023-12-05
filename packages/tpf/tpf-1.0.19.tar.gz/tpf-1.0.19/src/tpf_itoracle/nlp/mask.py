import numpy as np
import torch

def mask_pad(data,padding_index=0):
    """
    - data.shape = [batch_size,seq_len]
    """
    # b句话,每句话50个词,这里是还没 embed 的，
    # 实指序列这个维度，就算embedding之后，序列的维度也还在
    # data = [b, 50]
    # 判断每个词是不是<PAD>
    mask = data == padding_index
    seq_len = data.shape[1]

    # [b, 50] -> [b, 1, 1, 50]
    mask = mask.reshape(-1, 1, 1, seq_len)

    # 在计算注意力时,是计算50个词和50个词相互之间的注意力,所以是个50*50的矩阵
    # 是pad的列是true,意味着任何词对pad的注意力都是0
    # 但是pad本身对其他词的注意力并不是0
    # 所以是pad的行不是true

    # 复制n次
    # [b, 1, 1, 50] -> [b, 1, 50, 50]
    # 第一个50指50句话，第二个50指每句话50个词
    mask = mask.expand(-1, 1, seq_len, seq_len)

    return mask