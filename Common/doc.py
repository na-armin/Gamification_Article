# https://github.com/allenai/SciREX/blob/master/scirex_dataset/release_data.tar.gz You can also browse the dataset at - https://allenai.github.io/SciREX/
#
# It contains 3 files - {train, dev, test}.jsonl
#
# Each file contains one document per line in format -
# {
#     "doc_id" : str = Document Id as used by Semantic Scholar,
#     "words" : List[str] = List of words in the document,
#     "sentences" : List[Span] = Spans indexing into words array that indicate sentences,
#     "sections" : List[Span] = Spans indexing into words array that indicate sections,
#     "ner" : List[TypedMention] = Typed Spans indexing into words indicating mentions ,
#     "coref" : Dict[EntityName, List[Span]] = Salient Entities in the document and mentions belonging to it,
#     "n_ary_relations" : List[Dict[EntityType, EntityName]] = List of Relations where each Relation is a dictionary with 5 keys (Method, Metric, Task, Material, Score),
#     "method_subrelations" : Dict[EntityName, List[Tuple[Span, SubEntityName]]] = Each Methods may be subdivided into simpler submethods and Submenthods in coref array. For example, DLDL+VGG-Face is broken into two methods DLDL , VGG-Face.
# }
#
# Span = Tuple[int, int] # Inclusive start and Exclusive end index
# TypedMention = Tuple[int, int, EntityType]
# EntityType = Union["Method", "Metric", "Task", "Material"]
# EntityName = str
import numpy as np
import pandas as pd

class Doc:

    def make_body(self, _w, _sent, _sec):
        body = []
        start = 0
        end = -1
        for i in range(len(_sec)):
            sec = []
            for j in range(start, len(_sent)):
                if _sec[i][1] == _sent[j][1]:
                    end = j
                    break
            for sr in _sent[start:end + 1]:
                sec.append(_w[sr[0]:sr[1]])
            body.append(sec)
            start = end + 1
        return body

    def find_index_of_word_in_body(self, _start, _end):
        sec_index = -1
        sent_index = -1
        ind_start = -1
        ind_end = -1
        w_count = 0
        for sec_i, sec in enumerate(self.body):
            for sent_i, sent in enumerate(sec):
                if w_count + len(sent) > _start:
                    sec_index = sec_i
                    sent_index = sent_i
                    ind_start = _start - w_count
                    ind_end = _end - w_count
                    break
                w_count = w_count + len(sent)
            if sec_index > -1: break
        return [sec_index, sent_index, ind_start,ind_end]

    def make_ner_data(self, _ner):
        for n in _ner:
            sec_index, sent_index, ner_start, ner_end = self.find_index_of_word_in_body(n[0], n[1])
            n_text = self.text_in_range(sec_index, sent_index, ner_start, ner_end)
            if n_text not in self.ner:
                self.ner[n_text] = []
            elif self.ner[n_text][-1][4] != n[2]:
                self.ner_with_diff_tag_in_a_doc.add(n_text)
            self.ner[n_text].append([sec_index, sent_index, ner_start, ner_end, n[2]])

    def ner_without_diff_tag(self):
        ner_temp=self.ner.copy()
        for n in self.ner_with_diff_tag_in_a_doc:
            del ner_temp[n]
        return ner_temp

    def make_sentence_label_X_Y(self):
        error_num=0
        x=self.body
        y=[]
        for sec in self.body:
            sec_temp=[]
            for sent in sec:
                    sec_temp.append(["o"] * len(sent))
            y.append(sec_temp)
        ner=self.ner_without_diff_tag()
        for n in ner:
            for span_tag in ner[n]:
                for i in range(span_tag[2],span_tag[3]):
                    try:
                        y[span_tag[0]][span_tag[1]][i]=span_tag[4]
                    except:
                        print(n, span_tag,x[span_tag[0]][span_tag[1]])

        X=[]
        Y=[]
        for i_sec,sec in enumerate(self.body):
            for i_sent,sent in enumerate(sec):
                X.append(x[i_sec][i_sent])
                Y.append(y[i_sec][i_sent])
        data={'token': X,'label': Y}
        df= pd.DataFrame(data=data)
        return df

    def __init__(self, _id=0, _w=[], _sent=[], _sec=[], _ner=[], _coref=[], rel=[]):
        # doc_id : str = Document Id as used by Semantic Scholar,
        self.doc_id = _id
        # body : List[List[List[str]]] = List of sec[List of sent[List of words in the sentence]]
        self.body = self.make_body(_w, _sent, _sec)
        # ner : dic {ner_text: List[TypedMention] = Typed Spans indexing into words indicating mentions}
        # ner_with_diff_tag_in_a_doc : set {'ner_text',..}
        self.ner = {}  # ner : dic {ner_text:[[sec_index, sent_index, ner_start, ner_end,ner_tag]..]}
        self.ner_with_diff_tag_in_a_doc = set()
        self.make_ner_data(_ner)

        self.coref = _coref  # "coref" : Dict[EntityName, List[Span]] = Salient Entities in the document and mentions belonging to it,
        # self.n_ary_relation = rel  # "n_ary_relations" : List[Dict[EntityType, EntityName]] = List of Relations where each Relation is a dictionary with 5 keys (Method, Metric, Task, Material, Score),
        # "method_subrelations" : Dict[EntityName, List[Tuple[Span, SubEntityName]]] = Each Methods may be subdivided into simpler submethods and Submenthods in coref array. For example, DLDL+VGG-Face is broken into two methods DLDL , VGG-Face.

    @property
    def title(self):
        title = ' '.join(self.body[0][0])
        return title

    @property
    def text(self):
        t = ''
        for sec in self.body:
            for sent in sec:
                t = t + ' '.join(sent)
            t = t + '\n'
        return t

    def text_in_range(self, sec_i, sent_i, s, e):
        text = ' '.join(self.body[sec_i][sent_i][s:e])
        return text

    def text_in_sec(self, _sec_index):
        t = ''
        for sent in self.body[_sec_index]:
            t = t + ' '.join(sent)
        t = t + '\n'
        return t



if __name__ == '__main__':
    a = Doc()
