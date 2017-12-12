# -*- coding: utf-8 -*-

import re
import unicodedata
import MeCab
import gensim
from gensim.models.doc2vec import LabeledSentence


model = gensim.models.Doc2Vec.load('~/AI/OPC/Doc2Vec/Data/model/doc2vec_dmpv.model')

def split_into_words(doc, name=''):
    mecab = MeCab.Tagger(' -d /usr/lib/mecab/dic/mecab-ipadic-neologd')
    mecab.parse('')
    res = mecab.parseToNode(doc)
    words = []
    while res:
        arr = res.feature.split(',')
        res_sub = res
        res = res.next
        if re.match(r'^[0-9]{1,}$', unicodedata.normalize('NFKC', res_sub.surface)): # normalizeで全角数字を半角数字に変換
            continue
        if arr[0] == '記号' or arr[0] == 'BOS/EOS':
            continue
        elif arr[1] == '固有名詞' or arr[1] == '一般':
            word = res_sub.surface
            words.append(word)
        else:
            word = arr[6]
            if word == '○': # 全角のゼロは半角にはならないらしい
                continue
            words.append(word)
    
    return LabeledSentence(words=words, tags=[name])

def search_similar_texts(words):
    x = model.infer_vector(words)
    most_similar_texts = model.docvecs.most_similar([x])
    for similar_text, similarity in most_similar_texts:
        print('{0} : {1} '.format(similar_text, similarity))

def search_similar_words(words):
    for word in words:
        print()
        print(word + ':')
        for result in model.most_similar(positive=word, topn=10):
            print(result[0])

if __name__ == '__main__':
    while True:
        print('文字列入力:', end='')
        search_str = input()
        words = split_into_words(search_str).words
        search_similar_texts(words)
        search_similar_words(words)
        print('')
        print('---次のクエリをどうぞ---')
        print('')
