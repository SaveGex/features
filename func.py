class Sentence:
    def __init__(self, sentence: str) -> None:
        self.sentence = sentence
    def __str__(self) -> str:
        return self.sentence


symbol_correct_word_start = '('
symbol_correct_word_end = ')'

global_list_sentences = []

def recours_brackets(text: str, index = 0) -> list:

    correct_answer_list = []
    find_start = False
    word_list = text.split()

    while index < len(word_list):
        word = word_list[index]

        if find_start and (symbol_correct_word_start in word):
            word_list = recours_brackets(' '.join(word_list), index)
            text = ' '.join(word_list)
            continue

        
        if symbol_correct_word_start in word and symbol_correct_word_end in word:
            start_index = word.find(symbol_correct_word_start) + 1  if word.find(symbol_correct_word_start) < len(word) - 1 else 0
            end_index = word.find(symbol_correct_word_end)  if word.find(symbol_correct_word_end) > 0 else len(word)

            if len(word) > 1:
                correct_answer_list.append(word[start_index:end_index].strip(' '))
            word_list.pop(index)
            global_list_sentences.append(Sentence(sentence=' '.join(correct_answer_list)))
            return word_list
            
        
        elif symbol_correct_word_start in word:
            start_index = word.find(symbol_correct_word_start) + 1  if word.find(symbol_correct_word_start) < len(word) - 1 else 0

            if len(word)>1:
                correct_answer_list.append(word[start_index:len(word)].strip(' '))

            word_list.pop(index)
            index-=1
            find_start = True

        elif symbol_correct_word_end in word:
            end_index = word.find(symbol_correct_word_end)  if word.find(symbol_correct_word_end) > 0 else len(word)
            if len(word)>1:
                correct_answer_list.append(word[0:end_index].strip(' '))
            word_list.pop(index)
            index-=1
            global_list_sentences.append(Sentence(sentence=' '.join(correct_answer_list)))
            return word_list
        
        elif find_start:
            correct_answer_list.append(word.strip(' '))
            word_list.pop(index)
            index-=1

        index += 1

print(recours_brackets("\
it's word which.... (my name (bonk  ( inner) ) phrase )"))
for i in global_list_sentences:
    print(i)
