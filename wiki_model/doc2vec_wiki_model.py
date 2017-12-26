import gensim
import smart_open
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input', type=str)
parser.add_argument('--save_model', '-s', default='model', type=str)
args = parser.parse_args()

def read_corpus(fname):
    with smart_open.smart_open(fname, encoding="utf-8") as f:
        for i, line in enumerate(f):
            # For training data, add tags
            yield gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(line, min_len=1), [i])


train_corpus = list(read_corpus(args.input))

model = gensim.models.doc2vec.Doc2Vec(size=400, min_count=10, iter=55)

model.build_vocab(train_corpus)
model.train(train_corpus, total_examples=model.corpus_count, epochs=model.iter)

model.save(args.save_model)
