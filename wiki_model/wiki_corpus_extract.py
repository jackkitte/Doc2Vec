# -*- coding: utf-8 -*-

import argparse
import random


parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()
random.seed(1)

with open(args.output, 'w', encoding='utf-8') as f_w:
    with open(args.input, 'r', encoding='utf-8') as f_r:
        wiki_corpus_list = f_r.readlines()
        wiki_corpus_extract = random.sample(wiki_corpus_list, 5300000)
        for line in wiki_corpus_extract:
            f_w.write(line)
