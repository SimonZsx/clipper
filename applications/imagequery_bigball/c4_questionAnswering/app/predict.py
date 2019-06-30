from datetime import datetime
"""
This is the preliminary version of Questiona Answering System. 
We are not using AI here but just use simple logic. 
The reason is that the context where we need to generate answer from is
short and simple and there are not too much information. Answering with 
logic already provides good enough result.
"""

def predict(mapping):
    t1 = datetime.utcnow()
    print("[INFO]\t[c4]\t{}".format(str(t1)))

    split = mapping.split('-')
    noun_str = split[0]
    verb_str = split[1]

    question = "verb"
    question = question.lower()
    if question == "verb":
      answer = verb_str
    elif question == "noun":
      answer = noun_str
    else:
      answer = "Unable to analyze..."

    t2 = datetime.utcnow()
    print("[INFO]\t[c4]\t{}".format(str(t2)))
    print("[INFO]\t[c4]\tTime elapsed: {:.10f} seconds.".format(str((t2-t1).total_seconds())) )

    return answer