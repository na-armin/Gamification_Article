import spacy
import pandas as pd
import Common.show as sh
# from spacy.matcher import Matcher

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

    import spacy  # load spacy
    nlp = spacy.load("en_core_web_lg", disable=['parser', 'tagger', 'ner'])
    # stops = stopwords.words("english")
    def normalize(comment, lowercase, remove_stopwords):
        if lowercase:
            comment = comment.lower()
        comment = nlp(comment)
        lemmatized = list()
        for word in comment:
            lemma = word.lemma_.strip()
            if lemma:
                if not remove_stopwords or (remove_stopwords and lemma.is_stop):
                    lemmatized.append(lemma)
        return " ".join(lemmatized)

    def clean_ner(self):
        # nlp = spacy.load("en_core_sci_scibert")
        nlp = spacy.load('en_core_web_lg')
        ner_temp = self.ner_without_diff_tag()
        keys=list(ner_temp.keys())
        cluster=list(range(len(keys)))

        for i in range(len(keys)):
            if i==cluster[i]:
                n1 = nlp(keys[i].lower())
                print(keys[i], " : ")
                for j in range(i+1,len(keys)):
                    n2 = nlp(keys[j].lower())
                    sim=n1.similarity(n2)
                    if sim > 0.90:
                        print(keys[j],sim)
                        cluster[j]=i
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
    nlp = spacy.load("en_core_web_lg")

    # # m_tool = Matcher(nlp.vocab)
    #
    # p1 = [
    #     [{'TAG': 'NOUN'}, {'TAG': 'NOUN'}],
    #     [{'TAG': 'NOUN'}, {"IS_PUNCT": True}, {'TAG': 'NOUN'}]]
    #     # add more if required
    # m_tool.add('QBF', p1)
    # sentence = nlp(u'feed forward   feed-forward   feedforward')
    # print(sentence.vocab.get_noun_chunks)
    # phrase_matches = m_tool(sentence)
    # print(phrase_matches)
    # for match_id, start, end in phrase_matches:
    #     string_id = nlp.vocab.strings[match_id]
    #     span = sentence[start:end]
    #     print("HHHHHHHH",match_id, string_id, start, end, span.text)
    n1 = nlp("feed forward")
    # print(n1.vector)
    n2 = nlp("feed-forward")
    # print(n1.vector)
    n3 = nlp("feedforward")
    # print(n1.vector)

    print(n1.similarity(n2))
    print(n2.similarity(n3))
    print(n1.similarity(n3))