import argparse
import MeCab
import re
import unicodedata

parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('few_words')
parser.add_argument('output')
args = parser.parse_args()

few_words = set()
for line in open(args.few_words, "r", encoding="utf-8"):
    dst = re.sub(r'([\[\](){}\\*+.?^$\-|])', r'\\\1', line.strip())
    if dst in ("", "「", "」", "、", "。", "（", "）"):
        continue
    few_words.add(dst)

f = open(args.output, "w", encoding="utf-8")
mecab = MeCab.Tagger(' -d /usr/lib/mecab/dic/mecab-ipadic-neologd')
mecab.parse('')
for line in open(args.input, "r", encoding="utf-8"):
    if line.strip() == "" or line[0] == "<":
        continue
    found = False
    words = line.strip().split(" ")
    if len(words) <= 2:
        continue
    for word in words:
        if word in few_words:
            found = True
            break
    if found:
        continue
    res = mecab.parseToNode(line)
    mecab_words = []
    while res:
        arr = res.feature.split(',')
        res_sub = res
        res = res.next
        if re.match(r'^[0-9]{1,}$', unicodedata.normalize('NFKC', res_sub.surface)): # normalizeで全角数字を半角数字に変換
            continue
        if arr[0] == '記号' or arr[0] == 'BOS/EOS':
            continue
        elif arr[1] == '固有名詞' or arr[1] == '一般':
            mecab_word = res_sub.surface
            mecab_words.append(mecab_word)
        else:
            mecab_word = arr[6]
            if mecab_word == '○': # 全角のゼロは半角にはならないらしい
                continue
            mecab_words.append(mecab_word)
    f.write(' '.join(mecab_words) + '\n')
f.close()
