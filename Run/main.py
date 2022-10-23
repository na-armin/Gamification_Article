# This is a Gamification_Article Python script.
import json
import time
import pickle


import Common.Scirex_process as Sci_dataset
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
        "ner": docs[0].ner_without_diff_tag(),
        "Options": ["Method", "Metric", "Task", "Material"]
    }
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
    # Writing to sample.json
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)
    # endregin Make Json File: input for game

    # train=pd.DataFrame()
    # i=0
    # max_seq_length=0
    # for _doc in docs:
    #     df,max_seq_len=_doc.make_sentence_label_X_Y()
    #     if max_seq_len>max_seq_length:
    #         max_seq_length=max_seq_len
    #     train=train.append(df)
    #     print(i ,":",_doc.doc_id)
    #     i = i + 1
    # print("max_seq_length :",max_seq_length)
    # print(train.token)
    # with open("test_data", 'wb') as f:
    #     pickle.dump(train, f)
    # docs[0].print_text(docs[0].ner_without_diff_tag())

    # ents = KE.keyphrase_extract1(docs[0].text)

    # print("Size of entity find in doc: ", len(ents))
    print("Size of ner find in doc:" , len(docs[0].ner_without_diff_tag()))
    # i = 0
    # for ent in ents:
    #     # print('Entities :', ent, [(ent.text, ent.kb_id_)])
    #     # print(ent._.dbpedia_raw_result['@similarityScore'])
    #     i = i + 1
    # print(i, "entity in the text")
    # print("---------------------")
    # i = 0
    # for ne in docs[0].ner_without_diff_tag():
    #     # print("ne in: ",ne)
    #     for ent in ents:
    #         if ne.lower() ==ent.text.lower():
    #             # print(ent.text, ent.kb_id_)
    #             # print(ent._.dbpedia_raw_result['@similarityScore'])
    #             i = i + 1
    #             break
    # print(i, "entity in the text")

    docs[0].clean_ner()
    # for ke in KE.keyphrase_extract3(docs[0].text):
    #     print(ke)
    #     show_text(ke, 'blue')
    #     show_text('Hello, World!', 'blue')
    # print('time: ', time.time() - Start_time)