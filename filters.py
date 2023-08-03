import re
from langdetect import detect, LangDetectException
from profanity_check import predict

class TextFilter(object):
    def __init__(self) -> None:
        self.regex = {
            "phone_number" : re.compile(r"(\+?\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}"),
            "email" : re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
            "ssn" : re.compile(r"^(?!666|000|9\d{2})\d{3}-(?!00)\d{2}-(?!0000)\d{4}$"),
            "address" : re.compile(r"^\\d{1,5}\\s[A-z]{1,2}[a-z]*\\s[A-z]{2,}\\s[A-z]{2,}\\s*\\d{5}(?:[-\\s]\\d{4})?$")
        }

    def contains_privacy(self, sentence):
        red_flags = []
        if not sentence or len(sentence) == 0:
            return red_flags
        for rule in self.regex:
            if self.regex[rule].search(sentence) != None:
                red_flags.append(rule)
        return red_flags

    def is_language(self, sentence, language):
        if not sentence or len(sentence) == 0:
            return False
        try:
            lang = detect(sentence)
            return lang[:2] == language[:2]
        except LangDetectException:
            return True
    
    def is_offsensive(self, sentence):
        if not sentence or len(sentence) == 0:
            return False
        profanity_predect = predict([sentence])
        return profanity_predect[0] > 0