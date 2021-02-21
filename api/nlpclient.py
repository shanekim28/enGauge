# Simple usage
from stanfordcorenlp import StanfordCoreNLP


def process(sentence):
    nlp = StanfordCoreNLP('http://localhost', port=9000)

    result = nlp.parse(sentence)

    isQuestion = False
    if result.find("SBAR") >= 0 or result.find("SQ") >= 0 or result.find("?") >= 0:
        isQuestion = True

    # Do not forget to close! The backend server will consume a lot memory.
    nlp.close()
    return isQuestion
