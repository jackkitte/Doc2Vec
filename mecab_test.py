# -*- coding: utf-8 -*-

import os
import re
import unicodedata
import csv
import MeCab


def create_gensim_dictionary(data_path, mecab_path=None, no_below=2, no_above=0.1):

    if mecab_path is None:
        mecab = MeCab.Tagger("")
    else:
        mecab = MeCab.Tagger(mecab_path)

    mecab.parse('')
    for root, dirs, files in os.walk(data_path):
        print("# morphological analysis")
        docs = {}
        docs_title = {}
        for docname in files:
            docs[docname] = []
            with open(os.path.join(data_path, docname), "r") as f:
                lines = f.readlines()
                docs_title[docname] = lines[0]
                for text in lines:
                    text = re.sub(r'\n', '', text)
                    text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', '', text)
                    res = mecab.parseToNode(text)
                    while res:
                        arr = res.feature.split(",")
                        res_sub = res
                        res = res.next
                        if re.match(r'^[0-9]{1,}$', unicodedata.normalize('NFKC', res_sub.surface)): # normalizeで全角数字を半角数字に変換
                            continue
                        elif arr[0] == '記号' or arr[0] == 'BOS/EOS':
                            continue
                        elif re.match(r'^[A-Za-z]$', res_sub.surface):
                            continue
                        elif re.match(r'^-[0-9]+$', res_sub.surface):
                            continue
                        elif re.match(r'^[0-9]+.{1,3}$', res_sub.surface):
                            continue
                        elif re.match('(.)\\1{1,}', res_sub.surface): # 文字列リテラルの頭にrを付けるとエスケープシーケンスは無効となる
                            continue
                        elif arr[1] == '固有名詞' or arr[1] == '一般':
                            word = res_sub.surface
                            docs[docname].append(word)
                        else:
                            word = arr[6]
                            if word == '○': # 全角のゼロは半角にはならないらしい
                                continue
                            docs[docname].append(word)

    return docs, docs_title

if __name__ == "__main__":

    docs, docs_title = create_gensim_dictionary("/home/tamashiro/AI/OPC/Data/対応方法", mecab_path=" -d /usr/lib/mecab/dic/mecab-ipadic-neologd")
    with open('mecab_dict_list.csv', 'w') as f:
        writer = csv.writer(f)
        for i in range(1, 739):
            if 'KB{0}対応方法.txt'.format(i) in docs.keys():
                docs['KB{0}対応方法.txt'.format(i)].insert(0, 'KB{0}対応方法.txt'.format(i))
                writer.writerow(docs['KB{0}対応方法.txt'.format(i)])
