from multiprocessing import Pool

from datetime import datetime

import c0_entryContainer.predict as entry_container
import c1_speechRecognition.predict as speech_recognizer
import c2_imageCaptionGenerator.predict as caption_generator
import c3_nlpMappingGenerator.predict as mapping_generator
import c4_questionAnswering.predict as question_answerer
print("---Modules successfully imported---")


def run_speech_recognition(input_index):
    speech_text = speech_recognizer.predict(input_index)
    return speech_text


def generate_image_caption(input_index):
    captions = caption_generator.predict(input_index)
    return captions


def run(input_index):
    # CONTAINER 0
    input_index = entry_container.predict(input_index)

    # CONTAINER 1, 2: Multi Threading
    p = Pool(1)  # use only one subprocess, run TF session in main process
    returned_result1 = p.apply_async(run_speech_recognition, args=(input_index,))
    # returned_result2 = p.apply_async(generate_image_caption, args=(input_index,))
    result2 = generate_image_caption(input_index)
    p.close()
    p.join()  # p.join()方法会等待所有子进程执行完毕

    result1 = returned_result1.get()[0]
    # result2 = returned_result2.get()[0]

    # CONTAINER 3
    text = result1 + "|" + result2
    result3 = mapping_generator.predict(text)

    # Container 4
    question = "Verb"
    result4 = question_answerer.predict(result3)

    # print("\n1:\tText: " + result1)
    # print("2:\tGenerated captions: " + result2)
    # print("3:\tGenerated mapping: ")
    # items = result3.split('-')
    # nouns = items[0]
    # verbs = items[1]
    # print("\t- Nouns: " + nouns)
    # print("\t- Verb: " + verbs)
    # print("4:\tThe asked question is: " + question)
    # print("\tGenerated answer: " + result4)


if __name__ == "__main__":
    t1 = datetime.utcnow()
    print("\n[INFO]\t", "[main]\t", str(t1))

    for i in range(100):
        run(i)

    t2 = datetime.utcnow()
    print("[INFO]\t", "[main]\t", str(t2))
    print("[INFO]\t", "[main]\t", "Time elapsed: ", (t2-t1).total_seconds(), " seconds.")
