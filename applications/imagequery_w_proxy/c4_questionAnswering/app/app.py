import time
from predict import predict

evidence_list = []
question_list = []

evidence_list.append("Super Bowl 50 was an American football game to determine the champion of the National Football League (NFL) for the 2015 season. The American Football Conference (AFC) champion Denver Broncos defeated the National Football Conference (NFC) champion Carolina Panthers 24-10 to earn their third Super Bowl title. The game was played on February 7, 2016, at Levi's Stadium in the San Francisco Bay Area at Santa Clara, California.")
evidence_list.append("Beanie style with simple design. So cool to wear and make you different. It wears as peak cap and a fashion cap. It is good to match your clothes well during party and holiday, also makes you charming and fashion, leisure and fashion in public and streets. It suits all adults, for men or women. Matches well with your winter outfits so you stay warm all winter long.")
evidence_list.append("Question Answering (QA) is a computer science discipline within the fields of information retrieval and natural language processing (NLP), which is concerned with building systems that automatically answer questions posed by humans in a natural language.")

question_list.append("What day was the game played on?")
question_list.append("Is it for women?")
question_list.append("What is question answering?")

for i in range(len(evidence_list)):
    try:
        evidence = evidence_list[i]
        question = question_list[i]
        start_time = time.time()

        prediction = predict(evidence, question)

        end_time = time.time()
        print('Evidence: {}'.format(evidence))
        print('Question: {}'.format(question))
        print('Answer: {}'.format(prediction))
        print('Time: {:.4f}s'.format(end_time - start_time))
    except Exception as e:
        print(e)



