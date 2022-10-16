import numpy as np
import pandas as pd
import Common.show as sh

class Doc:

    def __init__(self, _id=0, _body=[], _ner={}, _ner_with_diff_tag_in_a_doc={}, _coref=[]):
        # doc_id : str
        self.doc_id = _id
        # body : List[List[List[str]]] = List of sec[List of sent[List of words in the sentence]]
        self.body = _body
        # ner : dic {ner_text:[[sec_index, sent_index, ner_start, ner_end,ner_tag]..]}
        self.ner = _ner

        # ner_with_diff_tag_in_a_doc : set {'ner_text',..}
        self.ner_with_diff_tag_in_a_doc = _ner_with_diff_tag_in_a_doc

        # "coref" : Dict[EntityName, List[Span]] = Salient Entities in the document and mentions belonging to it,
        self.coref = _coref

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

    def ner_without_diff_tag(self):
        ner_temp = self.ner.copy()
        for n in self.ner_with_diff_tag_in_a_doc:
            del ner_temp[n]
        return ner_temp

    def clean_ner(self):
        ner_temp = self.ner_without_diff_tag()
        for n in ner_temp:
            if

        return ner_temp


    def make_sentence_label_X_Y(self):
        x = self.body
        y = []
        for sec in self.body:
            sec_temp = []
            for sent in sec:
                sec_temp.append(["o"] * len(sent))
            y.append(sec_temp)
        ner = self.ner_without_diff_tag()
        for n in ner:
            for span_tag in ner[n]:
                for i in range(span_tag[2], span_tag[3]):
                    try:
                        y[span_tag[0]][span_tag[1]][i] = span_tag[4]
                    except:
                        print(n, span_tag, x[span_tag[0]][span_tag[1]])

        X = []
        Y = []
        max_seq_length = 0
        for i_sec, sec in enumerate(self.body):
            for i_sent, sent in enumerate(sec):
                if len(x[i_sec][i_sent]) > max_seq_length:
                    max_seq_length = len(x[i_sec][i_sent])
                X.append(x[i_sec])
                Y.append(y[i_sec])
        data = {'token': X, 'label': Y}
        df = pd.DataFrame(data=data)
        return df, max_seq_length

    def print_text(self,entitys):
        t = ''
        for sec in self.body:
            for sent in sec:
                for w in sent:
                    if any(w in s for s in entitys):
                        t = t + ' '+sh.colored_text(w,'blue')
                    else:
                        t = t + ' '+w
            t = t + '\n'
        print(t)
        return
if __name__ == '__main__':
    a = Doc()
