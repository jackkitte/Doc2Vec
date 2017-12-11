# -*- coding: utf-8 -*-
import csv
import gensim


model = gensim.models.Doc2Vec.load('~/AI/OPC/Doc2Vec/Data/model/doc2vec_dmpv.model')
similar_dic = {}
for i in range(1, 754):
    if 'KB{0}対応方法.txt'.format(i) in model.docvecs.doctags:
        similar_dic['KB{0}対応方法.txt'.format(i)] = model.docvecs.most_similar('KB{0}対応方法.txt'.format(i))

header = ['KBName']
for i in range(1, 11):
    header.append('most{0}'.format(i))

with open('Doc2Vec_most_similar10.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for key, value in similar_dic.items():
        value.insert(0, key)
        writer.writerow(value)

'''
pandasを使った方法
この方法だともの凄い簡単だが、idとしているファイル名(KB1対応方法.txt)が
特殊なため、並べ替えが上手くいかない。

import pandas as pd

df = pd.DataFrame(similar_dic)
df.T.to_csv("Doc2Vec_most_similar10.csv")

'''
