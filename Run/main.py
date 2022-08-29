# This is a Gamification_Article Python script.
import json
import time
import pickle
from pathlib import Path

import Common.doc
from Common.show import show_text
import Pre_process.keypraseExtraction as KE


def create_docs_from_json(_path, pickle_file):
    docs = []
    for line in open(_path, 'r'):
        json_str = json.loads(line)
        temp_doc = Common.doc.Doc(json_str['doc_id'], json_str['words'], json_str['sentences'], json_str['sections'],
                                  json_str['ner'],json_str['coref'])
        docs.append(temp_doc)
        with open(pickle_file, 'wb') as f:
            pickle.dump(docs, f)
    return docs


if __name__ == '__main__':

    Start_time = time.time()

    # Make Docs: Offline_phase
    if Path("Docs").is_file() == False:
        path = '../SciREX_dataset/train.jsonl'
        docs = create_docs_from_json(path, "Docs")

    with open('Docs', 'rb') as f:
        docs = pickle.load(f)

    print('time: ', time.time() - Start_time)

    print("coref: ", docs[0].coref)
    # Make Json File: input for game
    ner=docs[0].ner.copy()
    for n in docs[0].ner_with_diff_tag:
        del ner[n]

    dictionary = {
        "doc_id": docs[0].doc_id,
        "title": docs[0].title,
        "category": "SciREX",
        "body": docs[0].body,
        "ner": ner
    }

    # Serializing json
    json_object = json.dumps(dictionary, indent=4)

    # Writing to sample.json
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)

    for d in docs[0].ner:
        print(d, ":", docs[0].ner[d])

    print("\nphrase_with_diff_tag_lengh: ", len(docs[0].ner_with_diff_tag))


    # for p in docs[0].ner_with_diff_tag:  print(p, ": have diffrent tag", docs[0].ner[p])
    # for ke in KE.keyphrase_extract1(docs[0].text):
    #     print(ke)
    #     if ke[1] < 5:
    #         break
    #     # show_text(ke, 'blue')
    # for ke in KE.keyphrase_extract2(docs[0].text):
    #     print(ke)
    #     show_text(ke, 'blue')
    # for ke in KE.keyphrase_extract3(docs[0].text):
    #     print(ke)
    #     show_text(ke, 'blue')
    # # show_text('Hello, World!', 'blue')
    # print('time: ', time.time() - Start_time)
