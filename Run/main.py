# This is a Gamification_Article Python script.
import json
import time
import pickle
from pathlib import Path

import pandas as pd
import Common.Scirex_process as Sci_dataset
import Common.doc
from Common.show import show_text
import Pre_process.keypraseExtraction as KE

if __name__ == '__main__':

    Start_time = time.time()
    # region Make Docs: Offline_phase

    Sci_dataset.Process_scirex("../SciREX_dataset/")
    # endregion Make Docs: Offline_phase

    print('time: ', time.time() - Start_time)

    with open('Docs_train', 'rb') as f:
        docs = pickle.load(f)

    # region Make Json File: input for game

    dictionary = {
        "doc_id": docs[0].doc_id,
        "title": docs[0].title,
        "category": "SciREX",
        "body": docs[0].body,
        "ner": docs[0].ner_without_diff_tag()
    }
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
    # Writing to sample.json
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)
    # endregin Make Json File: input for game

    train=pd.DataFrame()
    i=0
    max_seq_length=0
    for _doc in docs:
        df,max_seq_len=_doc.make_sentence_label_X_Y()
        if max_seq_len>max_seq_length:
            max_seq_length=max_seq_len
        train=train.append(df)
        print(i ,":",_doc.doc_id)
        i = i + 1
    print("max_seq_length :",max_seq_length)
    print(train.token)
    with open("test_data", 'wb') as f:
        pickle.dump(train, f)
    # for d in docs[0].ner:
    #     print(d, ":", docs[0].ner[d])
    #
    # phrase_with_tag_lengh = 0
    # for d in docs:
    #     phrase_with_tag_lengh = phrase_with_tag_lengh + len(d.ner)
    # print("\nphrase_with_tag: ", phrase_with_tag_lengh)
    #
    # phrase_with_diff_tag_lengh = 0
    # for d in docs:
    #     phrase_with_diff_tag_lengh = phrase_with_diff_tag_lengh+ len(d.ner_with_diff_tag_in_a_doc)
    # print("\nphrase_with_diff_tag_lengh: ",phrase_with_diff_tag_lengh)
    #
    # print(len(docs))
    #
    # # for p in docs[0].ner_with_diff_tag:  print(p, ": have diffrent tag", docs[0].ner[p])
    # for ke in KE.keyphrase_extract1(docs[0].text):
    #     print(ke)
    #     if ke[1] < 5:
    #         break
        # show_text(ke, 'blue')
    # for ke in KE.keyphrase_extract2(docs[0].text):
    #     print(ke)
    #     show_text(ke, 'blue')
    # for ke in KE.keyphrase_extract3(docs[0].text):
    #     print(ke)
    #     show_text(ke, 'blue')
    # # show_text('Hello, World!', 'blue')
    # print('time: ', time.time() - Start_time)