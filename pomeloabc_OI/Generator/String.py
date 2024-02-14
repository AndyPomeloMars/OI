import random
import pomeloabc_OI.Generator.Const as const
import pomeloabc_OI.Generator.Utils as utils

class String():
    def rand_string(self, size, charset = const.ALPHABET_SMALL):
        if utils.list_like(size):
            size = random.randint(size[0], size[1])
            
        random_string = ""

        for i in range(size):
            random_string += random.choice(charset)
        return random_string
    
    def rand_sentence(self, size, charset = const.ALPHABET_SMALL, word_size = [1, 10], seperator = ", ", end = "."):
        if utils.list_like(size):
            size = random.randint(size[0], size[1])

        rand_sentence = ""

        while size > len(end):
            if word_size[1] > size - len(end):
                tmp = String.rand_string(size - len(end), charset = charset)
            else:
                tmp = String.rand_string(word_size, charset = charset) + seperator
            rand_sentence += tmp 
            size -= len(tmp)

        rand_sentence += end

        return rand_sentence
    
    def rand_paragraph(self, sentence_count, charset = const.ALPHABET_SMALL, word_size = [1, 10], word_seperator = ", ", sentence_size = [1, 20], sentence_end = ".", seperator = " ", end = "\n"):
        if utils.list_like(sentence_count):
            sentence_count = random.randint(sentence_count[0], sentence_count[1])

        rand_paragraph = ""

        while sentence_count:
            rand_paragraph += String.rand_sentence(sentence_size, charset = charset, word_size = word_size, seperator = word_seperator, end = sentence_end) + seperator
            sentence_count -= 1

        rand_paragraph += end

        return rand_paragraph