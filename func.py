class Sentence:
    def __init__(self, processed_sentence: str, sentence: str, fields: int, answers: int) -> None:
        #for show in html
        self.processed_sentence = processed_sentence
        # for comparing output and sentence
        self.sentence = sentence
        # i forgot
        self.fields = fields
        # how many answers can will be in sentence
        self.answers = answers
    def __str__(self) -> str:
        return f"processed_sentence: {self.processed_sentence}, \n sentence: {self.sentence}\n fields: {self.fields}\n answers: {self.answers}"
class Wrong_Answer:
    def __init__(self, index: int, text: str) -> None:
        self.text = text
        self.index = index
    def __str__(self) -> str:
        return f"text: {self.text}\n index: {self.index}"
class Correct_Answer:
    def __init__(self, index: int, phrase: str, text: str) -> None:
        self.index = index
        self.phrase = phrase
        self.text = text
    def __str__(self) -> str:
        return f"text: {self.text}\n index: {self.index}\n phrase: {self.phrase}"


input_index_counter = 0
def fields_count() -> str:
    global input_index_counter
    input_index_counter += 1
    field = f"<input type='text' class='' name='wrong_word{input_index_counter}' placeholder=\"{'something...'}\" size=\"{len('something...')}\">"
    return field
symbol_word_start = '('
symbol_word_end = ')'
symbol_field = '....'
 
back_slash = '\\'
forward_slash = '/'
count_of_dots_in_Sfield = len(symbol_field)-1
global_list_sentences = []

def to_processed_of_text(text: str, index = 0) -> list:

    word_list = text.split()
    index = 0

    indexs_words_list = []

    #cycle for change dots on fields
    plus_words = 1
    while index < len(word_list):
        word = word_list[index]
        if word.find(symbol_field) != -1:

            field = fields_count()

            change_index = index
            if len(word) != len(symbol_field):
                change_index += plus_words
                plus_words += 1

            start_text = word.find(symbol_field)
            end_index = start_text + len(symbol_field) - 1 
            word_split = [sym for sym in word]
            for _ in range(count_of_dots_in_Sfield):
                word_split.pop(start_text)
            
            word_split[start_text] = field
            word = ''.join(word_split)

            # need prepear sentence for correct indexes
            word_list[index] = word

            
            indexs_words_list.append(change_index)
            
            # Wrong_Answer(index, field)
        index += 1
    # for count indexes in
    index_indexs_words_list = 0
    index = 0 
    #cycle for remember index fields in original text and delete correct answers from processed text
    find_start = False
    # true mean can, false mean can't
    can_or_not = True
    start_text = 0
    start_index = 0
    saved_answers = 0
    for num_sym, sym in enumerate(text):
        if sym == symbol_word_start and find_start == False and can_or_not == True:
            start_index = start_text = num_sym + 1
            find_start = True
        elif ((sym == back_slash or sym == forward_slash) or sym == symbol_word_start) and find_start == True and can_or_not == True:
            # me in future don't forget about .strip() done with correct answer
            # need will make to save indexes of fields of correct sentence in Correct_Answer
            speciment = Correct_Answer(index = index_indexs_words_list, phrase = text[start_index:num_sym].strip(), text = text)
            global_list_sentences.append(speciment)
            
            # - 1 because i done + 1 to skip first symbol 
            saved_answers += 1
            # + 1 beause not include last symbol
            start_index = num_sym + 1
            index_indexs_words_list += 1
            
            can_or_not = False if saved_answers == index_indexs_words_list else True
            # can_or_not = False if saved_answers == len(indexs_words_list) else True
        elif sym == symbol_word_end and find_start == True:
            find_start = False
            text = text[:start_text-1] + text[num_sym + 1:]
            pass
        elif sym == symbol_word_end and find_start == False:
            text = text[:start_text-1] + text[start_text:]
            pass

            
            

    return global_list_sentences

print(to_processed_of_text("\
it's word which.... (my name/bonk \\inner\\/phrase/())...."))
for i in global_list_sentences:
    print(i)