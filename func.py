class Sentence:
    def __init__(self, processed_sentence: str, sentence: str, user_sentence: str, fields: int, answers: int) -> None:
        #for show in html
        self.processed_sentence = processed_sentence
        # for comparing output and sentence
        self.sentence = sentence
        # I think need to save and user sentence as what he wrote
        self.user_sentence = user_sentence
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

symbol_word_start = '('
symbol_word_end = ')'
symbol_field = '....'
 
back_slash = '\\'
forward_slash = '/'
count_of_dots_in_Sfield = len(symbol_field)-1

global_list_sentences = []


def change_name_for_field() -> str:
    global input_index_counter
    input_index_counter += 1
    field = f"<input type='text' class='' name='wrong_word{input_index_counter}' placeholder=\"{'something...'}\" size=\"{len('something...')}\">"
    return field


def processed_sentence_and_save(copy_text: str) -> str:
    # for count indexes in
    index_indexs_words_list = 0
    count_fields = copy_text.count(symbol_field)
    index = 0 
    #cycle for remember index fields in original text and delete correct answers from processed text
    find_start = False
    # true mean can, false mean can't
    can_or_not = True
    start_text = 0
    start_index = 0
    saved_answers = 0
    for num_sym, sym in enumerate(copy_text):
        if sym == symbol_word_start and find_start == False and can_or_not == True:
            start_index = start_text = num_sym + 1
            find_start = True
        elif ((sym == back_slash or sym == forward_slash) or sym == symbol_word_start) and find_start == True and can_or_not == True:
            # me in future don't forget about .strip() done with correct answer
            # need will make to save indexes of fields of correct sentence in Correct_Answer
            speciment = Correct_Answer(index = None, phrase = copy_text[start_index:num_sym].strip(), text = copy_text)
            global_list_sentences.append(speciment)
            
            # - 1 because i done + 1 to skip first symbol 
            saved_answers += 1
            # + 1 beause not include last symbol
            start_index = num_sym + 1
            index_indexs_words_list += 1
            
            can_or_not = False if saved_answers == count_fields else True
            # can_or_not = False if saved_answers == len(indexs_words_list) else True
        elif sym == symbol_word_end and find_start == True:
            find_start = False
            copy_text = copy_text[:start_text-1] + copy_text[num_sym + 1:]
            pass
        elif sym == symbol_word_end and find_start == False:
            copy_text = copy_text[:start_text-1] + copy_text[start_text:]
            pass
    return copy_text


def processed_sentence_without_save(copy_text: str) -> str:
    #cycle for remember index fields in original text and delete correct answers from processed text
    find_start = False
    # true mean can, false mean can't
    can_or_not = True
    start_text = 0
    for num_sym, sym in enumerate(copy_text):
        if sym == symbol_word_start and find_start == False and can_or_not == True:
            start_index = start_text = num_sym + 1
            find_start = True
        elif sym == symbol_word_end and find_start == True:
            find_start = False
            copy_text = copy_text[:start_text-1] + copy_text[num_sym + 1:]
            pass
        elif sym == symbol_word_end and find_start == False:
            copy_text = copy_text[:start_text-1] + copy_text[start_text:]
            pass
    return copy_text


def to_processed_of_text(text: str, index = 0) -> list:

    
    
    text_split_copy = processed_sentence_and_save(text).split()
    correct_sentence = processed_sentence_without_save(text).split()
    index = 0

    indexs_words_list = []

    # make proceed sentence for showing in html
    plus_words = 0
    while index < len(text_split_copy):
        word = text_split_copy[index]
        if word.find(symbol_field) != -1:
            
            word = word.replace(symbol_field, f" {symbol_field} ").strip()
            text_split_copy[index] = word
            text_split_copy = " ".join(text_split_copy).split()
            addition_index = index + 1 if word != symbol_field else index
            index = index + 1

            # field = change_name_for_field()

            # # need prepear sentence for correct indexes
            # text_split_copy[addition_index] = field

            indexs_words_list.append(addition_index)
            
            
            # Wrong_Answer(index, field)
        index += 1
    #processed sentence fields
    for index in indexs_words_list:
        field = change_name_for_field()
        text_split_copy[index] = field


    '''make correct sentence for comparing with user sentence'''
    index_indexs_words_list = 0
    for object in global_list_sentences:
        # there is a stub in the processed_sentence function
        object.index = indexs_words_list[index_indexs_words_list]
        index_indexs_words_list += 1
    
    for object in global_list_sentences:
        text_split_copy[object.index] = object.phrase
    global_list_sentences.append(text_split_copy)



    return global_list_sentences

print(to_processed_of_text("\
it'....s word which.... (my name/bonk \\inner\\/phrase/())...."))
for i in global_list_sentences:
    print(i)