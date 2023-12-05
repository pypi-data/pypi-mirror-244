import jieba

seq1= "你现阶段的目标是？"
seq2=  "不上班还有钱花"

sentence1 = jieba.lcut(seq1)
word2id = {}
word2id["PAD"] = 0  # 补长度 是为了批次处理
len_add = len(word2id)
word2id.update({word:(index+len_add) for index,word in enumerate(set(sentence1))}) 


sentence2 = jieba.lcut(seq2)
len_add = len(word2id)
word2id.update({word:(index+len_add) for index,word in enumerate(set(sentence2))})

sentence = []
sentence.append([ word2id[word]  for word in sentence1])
sentence.append([ word2id[word]  for word in sentence2])

max_seq_len = 6 
index_mat = []
for word_index in sentence:
    word_index = word_index+[word2id["PAD"]]*max_seq_len
    word_index = word_index[:6]
    index_mat.append(word_index)
    
    
print(index_mat)




from tpf.att import Attn 
from tpf.att import MultiHead 
import torch 
from torch import nn
from tpf.nlp.mask import mask_pad

#索引编码并转换shape为[batch_size,seq_len]
B = torch.tensor(index_mat[1]).unsqueeze(dim=0) #B.shape = [1, 6]

#对索引矩阵进行补码
mask = mask_pad(B,padding_index=0)  #mask.shape = [1, 1, 6, 6]

#索引向量化
embed = nn.Embedding(num_embeddings=11,embedding_dim=32,padding_idx=0)
B = embed(B) #B.shape = torch.Size([1, 6, 32])

#求B相对自己的注意力
A=B
mh = MultiHead(in_features=32,out_features=32)
c = mh(B,A,A,mask)
c.shape