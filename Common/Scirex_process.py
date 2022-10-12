import json
import Common.doc
import pickle
from pathlib import Path

# des_path="../data/"
def make_body(_w, _sent, _sec):
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


def find_index_of_word_in_body(body, _start, _end):
    sec_index = -1
    sent_index = -1
    ind_start = -1
    ind_end = -1
    w_count = 0
    for sec_i, sec in enumerate(body):
        for sent_i, sent in enumerate(sec):
            if w_count + len(sent) > _start:
                sec_index = sec_i
                sent_index = sent_i
                ind_start = _start - w_count
                ind_end = _end - w_count
                break
            w_count = w_count + len(sent)
        if sec_index > -1: break
    return [sec_index, sent_index, ind_start, ind_end]


def make_ner_data(_ner,body):
    ner = {}  # ner : dic {ner_text:[[sec_index, sent_index, ner_start, ner_end,ner_tag]..]}
    ner_with_diff_tag_in_a_doc = set()
    for n in _ner:
        sec_index, sent_index, ner_start, ner_end = find_index_of_word_in_body(body,n[0], n[1])
        n_text = ' '.join(body[sec_index][sent_index][ner_start:ner_end])
        if n_text not in ner:
            ner[n_text] = []
        elif ner[n_text][-1][4] != n[2]:
            ner_with_diff_tag_in_a_doc.add(n_text)
        ner[n_text].append([sec_index, sent_index, ner_start, ner_end, n[2]])
    return ner,ner_with_diff_tag_in_a_doc

def create_docs_from_json(_path, pickle_file):
    docs = []
    for line in open(_path, 'r'):
        json_str = json.loads(line)
        id=json_str['doc_id']
        body=make_body(json_str['words'], json_str['sentences'], json_str['sections'])
        ner,ner_with_diff_tag_in_a_doc=make_ner_data(json_str['ner'],body)
        coref=json_str['coref']
        temp_doc = Common.doc.Doc(id, body,ner,ner_with_diff_tag_in_a_doc, coref)

        docs.append(temp_doc)
    with open(pickle_file, 'wb') as f:
        pickle.dump(docs, f)
    return docs

def Process_scirex(_folderPath):

    if Path("Docs_train").is_file() == False:
        path = _folderPath+ 'train.jsonl'
        create_docs_from_json(path, "Docs_train")

    if Path("Docs_test").is_file() == False:
        path = _folderPath+ 'test.jsonl'
        create_docs_from_json(path, "Docs_test")

    if Path("Docs_dev").is_file() == False:
        path = _folderPath+ 'dev.jsonl'
        create_docs_from_json(path, "Docs_dev")