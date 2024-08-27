class Sentence:
    def __init__(self, processed_sentence: str, correct_sentence: list, user_sentence: str, fields: int, answers: int) -> None:
        #for show in html
        self.processed_sentence = processed_sentence
        # for comparing output and sentence
        self.correct_sentence = correct_sentence
        # I think need to save and user sentence as what he wrote
        self.user_sentence = user_sentence
        # i forgot
        self.fields = fields
        # how many answers can will be in sentence
        self.answers = answers
    def __str__(self) -> str:
        return f"processed_sentence: {self.processed_sentence} \n sentence: {self.correct_sentence}\n fields: {self.fields}\n answers: {self.answers}"
class Wrong_Answer:
    def __init__(self, index: int, text: str) -> None:
        self.key = text
        self.index = index
    def __str__(self) -> str:
        return f"text: {self.key}\n index: {self.index}"
class Correct_Answer:
    def __init__(self, index: int, phrase: str, key: str) -> None:
        self.index = index
        self.phrase = phrase
        self.key = key
    def __str__(self) -> str:
        return f"text: {self.key}\n index: {self.index}\n phrase: {self.phrase}"


input_index_counter = 0

symbol_word_start = '('
symbol_word_end = ')'
symbol_field = '....'
 
back_slash = '\\'
forward_slash = '/'
count_of_dots_in_Sfield = len(symbol_field)-1

global_list_correct_model = []


def delete_symbol_fields(text_HTML: str, indexs_words_list: list, i: int) -> str:
    length = len(indexs_words_list) - i
    for index in range(length):
        text_HTML.pop(indexs_words_list[len(indexs_words_list)-index-1])
    return text_HTML



def change_name_for_field() -> str:
    global input_index_counter
    input_index_counter += 1
    field = f"<input type='text' class='' name='wrong_word{input_index_counter}' placeholder=\"{'something...'}\" size=\"{len('something...')}\">"
    return field


def processed_sentence_and_save(copy_text: str, sentence) -> str:
    # for count indexes in
    index_indexs_words_list = 0
    count_fields = copy_text.count(symbol_field)
    index = 0 
    #cycle for remember index fields in original text and delete correct answers from processed text
    find_start = False
    # true mean can, false mean can't
    can_or_not = True if count_fields > 0 else False
    start_text = 0
    start_index = 0
    saved_answers = 0
    concat_list = []
    for num_sym, sym in enumerate(copy_text):
        if saved_answers > count_fields or saved_answers == count_fields:
            can_or_not = False
        if sym == symbol_word_start and find_start == False:
            start_index = start_text = num_sym + 1
            find_start = True
        elif ((sym == back_slash or sym == forward_slash) or sym == symbol_word_start) and find_start == True and can_or_not == True and start_index != num_sym:
            # me in future don't forget about .strip() done with correct answer
            # need will make to save indexes of fields of correct sentence in Correct_Answer
            speciment = Correct_Answer(index = 0, phrase = copy_text[start_index:num_sym].strip(), key = 123)
            global_list_correct_model.append(speciment)
            
            # - 1 because i done + 1 to skip first symbol 
            saved_answers += 1
            # + 1 beause not include last symbol
            start_index = num_sym + 1
            index_indexs_words_list += 1
            
            # can_or_not = False if saved_answers == len(indexs_words_list) else True
            '''if sudden wrote empty answer'''
        elif start_index == num_sym and ((sym == back_slash or sym == forward_slash) or sym == symbol_word_start) and find_start == True and can_or_not == True:
            start_index += 1
        elif sym == symbol_word_end and find_start == True:
            if start_index != num_sym and can_or_not == True:
                speciment = Correct_Answer(index = 0, phrase = copy_text[start_index:num_sym].strip(), key = 123)
                global_list_correct_model.append(speciment)
                saved_answers += 1
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


def to_processed_of_text(text: str, sentence: Sentence, index=0) -> Sentence:
    # if not Sentence.pk:
    #     raise ValueError("Task model must be saved before creating Answer_Model.")
    
    indexs_words_list = []
    index = 0

    text_HTML = processed_sentence_and_save(text, sentence).split()
    lenght = len(text_HTML)
    # Обробка тексту для збереження індексів
    while index < lenght:
        word = text_HTML[index]
        if symbol_field in word and index not in indexs_words_list:
            word = word.replace(symbol_field, f" {symbol_field} ").strip()
            text_HTML[index] = word
            text_HTML = " ".join(text_HTML).split()
            addition_index = index + 1 if not word.startswith(symbol_field) else index
            indexs_words_list.append(addition_index)
        lenght = len(text_HTML)
        index += 1
    # while index < len(text_HTML):
    #     word = text_HTML[index]
    #     if symbol_field in word:
    #         word = word.replace(symbol_field, f" {symbol_field} ").strip()
    #         text_HTML[index] = word
    #         text_HTML = " ".join(text_HTML).split()
    #         addition_index = index + 1 if word != symbol_field else index
    #         index+=1
    #         indexs_words_list.append(addition_index)
    #     index += 1

    # Заміна індексів на поля введення
    for i, idx in enumerate(indexs_words_list):
        if i < len(global_list_correct_model):
            field = change_name_for_field()
            text_HTML[idx] = field
        else:
            text_HTML = delete_symbol_fields(text_HTML, indexs_words_list, i)
            break
    
    correct_sentence = text_HTML.copy()

    # Оновлення індексів правильних відповідей
    for i, obj in enumerate(global_list_correct_model):
        obj.index = indexs_words_list[i]
        # obj.save()

    # Оновлення correct_sentence
    for obj in global_list_correct_model:
        correct_sentence[obj.index] = obj.phrase
    
    # Оновлення моделі Sentence
    # Sentence.name = f"UniqueName_{Sentence.name}_{timezone.now()}"
    sentence.correct_sentence = correct_sentence
    sentence.processed_sentence = " ".join(text_HTML)
    sentence.fields = len(indexs_words_list)
    sentence.answers = len(global_list_correct_model)
    
    return sentence
sentence = Sentence(processed_sentence='', correct_sentence=[], user_sentence="it'....s(my name) word which....(/bonk) (\\inner)....", fields=0, answers=0)
print(to_processed_of_text("\
it'....s(my name) word which....(/bonk) (\\inner)sentence(dsa\\1231\\1231)", sentence))
for i in global_list_correct_model:
    print(i)