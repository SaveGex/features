class Sentence:
    def __init__(self, processed_sentence: str, sentence: list, user_sentence: str, fields: int, answers: int) -> None:
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
    concat_list = []
    for num_sym, sym in enumerate(copy_text):
        if sym == symbol_word_start and find_start == False and can_or_not == True:
            start_index = start_text = num_sym + 1
            find_start = True
        elif ((sym == back_slash or sym == forward_slash) or sym == symbol_word_start) and find_start == True and can_or_not == True and start_index != num_sym:
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
            '''if sudden wrote empty answer'''
        elif start_index == num_sym and ((sym == back_slash or sym == forward_slash) or sym == symbol_word_start) and find_start == True and can_or_not == True:
            start_index += 1
        elif sym == symbol_word_end and find_start == True:
            if start_index != num_sym:
                speciment = Correct_Answer(index = None, phrase = copy_text[start_index:num_sym].strip(), text = copy_text)
                global_list_sentences.append(speciment)
            else:
                start_index += 1
            find_start = False
            concat_list.append({"to": start_text-1,
                                "from": num_sym + 1
                                })
            pass
        elif sym == symbol_word_end and find_start == False:
            concat_list.append({"to": start_text-1,
                                "from": start_text
                                })
            pass
        
    for dict_obj in reversed(concat_list):
        copy_text = copy_text[:dict_obj["to"]] + copy_text[dict_obj["from"]:]
    return copy_text


def processed_sentence_without_save(copy_text: str) -> str:
    #cycle for remember index fields in original text and delete correct answers from processed text
    find_start = False
    # true mean can, false mean can't
    can_or_not = True
    start_text = 0
    concat_list = []
    for num_sym, sym in enumerate(copy_text):
        if sym == symbol_word_start and find_start == False and can_or_not == True:
            start_index = start_text = num_sym + 1
            find_start = True
        elif sym == symbol_word_end and find_start == True:
            find_start = False
            concat_list.append({"to": start_text-1,
                                "from": num_sym + 1
                                })
            pass
        elif sym == symbol_word_end and find_start == False:
            concat_list.append({"to": start_text-1,
                                "from": start_text
                                })
            pass
    for dict_obj in reversed(concat_list):
        copy_text = copy_text[:dict_obj["to"]] + copy_text[dict_obj["from"]:]
    return copy_text


def to_processed_of_text(text: str, index = 0) -> list:

    
    
    text_HTML = processed_sentence_and_save(text).split()
    correct_sentence = []
    index = 0

    indexs_words_list = []

    # make proceed sentence for showing in html
    plus_words = 0
    while index < len(text_HTML):
        word = text_HTML[index]
        if word.find(symbol_field) != -1:
            
            word = word.replace(symbol_field, f" {symbol_field} ").strip()
            text_HTML[index] = word
            text_HTML = " ".join(text_HTML).split()
            addition_index = index + 1 if word != symbol_field else index
            index = index + 1

            # field = change_name_for_field()

            # # need prepear sentence for correct indexes
            # text_split_copy[addition_index] = field

            indexs_words_list.append(addition_index)
            
            
            # Wrong_Answer(index, field)
        index += 1
    # sentence with values filds instead correct words
    correct_sentence = text_HTML.copy()
    #processed sentence fields
    for index in indexs_words_list:
        field = change_name_for_field()
        text_HTML[index] = field


    '''make correct sentence for comparing with user sentence'''
    index_indexs_words_list = 0
    for object in global_list_sentences:
        # there is a stub in the processed_sentence function
        object.index = indexs_words_list[index_indexs_words_list]
        index_indexs_words_list += 1
    
    for object in global_list_sentences:
        correct_sentence[object.index] = object.phrase
    global_list_sentences.append(correct_sentence)

    speciment = Sentence(processed_sentence = text_HTML, sentence = correct_sentence, user_sentence = None, fields = text.count(symbol_field), answers = len(global_list_sentences))

    return speciment

print(to_processed_of_text("\
it'....s(my name) word which....(/bonk) (\\inner)...."))
for i in global_list_sentences:
    print(i)