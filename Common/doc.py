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

class Doc:
    def make_body(self,_w, _sent, _sec):
        body=[]
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

    def make_ner_data(self,_ner):
        for n in _ner:
            sec_index = -1
            sent_index = -1
            ner_start = -1
            ner_end = -1
            w_count = 0
            for sec_i, sec in enumerate(self.body):
                for sent_i, sent in enumerate(sec):
                    if w_count + len(sent) > n[0]:
                        sec_index = sec_i
                        sent_index = sent_i
                        ner_start = n[0] - w_count
                        ner_end = n[1] - w_count
                        break
                    w_count = w_count + len(sent)
                if sec_index>-1: break
            new_n=[sec_index, sent_index, ner_start, ner_end, n[2]]
            n_text = self.text_in_range(sec_index, sent_index, ner_start, ner_end)
            if n_text not in self.ner :
                self.ner [n_text] = []
            elif self.ner[n_text][-1][4] != new_n[4]:
                self.ner_with_diff_tag.add(n_text)
            self.ner[n_text].append(new_n)

    def __init__(self, _id=0, _w=[], _sent=[], _sec=[], _ner=[], coref=[], rel=[]):
        # doc_id : str = Document Id as used by Semantic Scholar,
        self.doc_id = _id
        # body : List[List[List[str]]] = List of sec[List of sent[List of words in the sentence]]
        self.body=self.make_body(_w, _sent, _sec)
        # ner : dic{phrase: List[TypedMention] = Typed Spans indexing into words indicating mentions}
        self.ner = {}
        self.ner_with_diff_tag = set()
        self.make_ner_data(_ner)

        # self.coref = coref  # "coref" : Dict[EntityName, List[Span]] = Salient Entities in the document and mentions belonging to it,
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
    def text_in_range(self, i, j, s, e):
        text = ' '.join(self.body[i][j][s:e])
        return text

    def sentence_text(self, _sent_index):
        text = ' '.join(self.body[_sent_index])
        return text


    def first_last_sents_in_sec(self, _sec_index):
        first = -1
        last = -1
        for i, s in enumerate(self.sentences):
            if self.if_section_contains_sent(_sec_index, i):
                if first == -1:
                    first = i
                else:
                    last = i
        return first, last


if __name__ == '__main__':
    a = Doc()
