from pymystem3 import Mystem
import re
from collections import Counter

from scipy.spatial import distance

first_text = 'texts/first_text.txt'
second_text = 'texts/second_text.txt'
first_content = ''
second_content = ''
first_lines = []
second_lines = []

f_t_array = []
s_t_array = []


def remove_items(current_list, item):
    result_list = [i for i in current_list if i != item]
    return result_list


def get_words_array(current_lines):

    rawtext = current_lines
    m = Mystem()
    parsedtext = ''.join(m.lemmatize(rawtext))
    parsedwords = re.split(r"\.| |; |: |, |\*|\n", parsedtext)
    parsedwords = remove_items(parsedwords, '')
    words_counter = Counter(parsedwords)
    return words_counter.most_common()


print("First Text:")
print()
with open(first_text, "r", encoding='utf-8') as ft:
    first_content = ft.read()
    print(first_content)
print()

print("Second Text:")
print()
with open(second_text, "r", encoding='utf-8') as st:
    second_content = st.read()
    print(second_content)
print()

full_content = first_content + ' ' + second_content

split_regex = re.compile(r'[.|!|?|…]')
full_lines = filter(lambda t: t, [t.strip() for t in split_regex.split(full_content)])
full_words = get_words_array(full_content)
print(full_words)
print()

print("First Text (lemmatized and vectorized):")
print()
with open(first_text, "r", encoding='utf-8') as ft:
    first_content = ft.read()
    split_regex = re.compile(r'[.|!|?|…]')
    first_lines = filter(lambda t: t, [t.strip() for t in split_regex.split(first_content)])
    for f_line in first_lines:
        f_array = []
        m = Mystem()
        parsed_line = ''.join(m.lemmatize(f_line))
        parsed_line_words = re.split(r"\.| |; |: |, |\*|\n", parsed_line)
        parsed_line_words = remove_items(parsed_line_words, '')
        print(parsed_line_words)
        for f_word in full_words:
            if f_word[0] in parsed_line_words:
                f_array.append(parsed_line_words.count(f_word[0]))
            else:
                f_array.append(0)
        f_t_array.append(f_array)
        print(f_array)
print()

print("Second Text (lemmatized and vectorized):")
print()
with open(second_text, "r", encoding='utf-8') as st:
    second_content = st.read()
    split_regex = re.compile(r'[.|!|?|…]')
    second_lines = filter(lambda t: t, [t.strip() for t in split_regex.split(second_content)])
    for s_line in second_lines:
        s_array = []
        m = Mystem()
        parsed_line = ''.join(m.lemmatize(s_line))
        parsed_line_words = re.split(r"\.| |; |: |, |\*|\n", parsed_line)
        parsed_line_words = remove_items(parsed_line_words, '')
        print(parsed_line_words)
        for f_word in full_words:
            if f_word[0] in parsed_line_words:
                s_array.append(parsed_line_words.count(f_word[0]))
            else:
                s_array.append(0)
        s_t_array.append(s_array)
        print(s_array)
print()

current_distance = distance.cosine(f_t_array[0], s_t_array[0])
previous_distance = distance.cosine(f_t_array[0], s_t_array[0])

print("Distance between Zero Sentences ([0] - [0]) - " + str(current_distance))

first_sentence = 0
second_sentence = 0
f_index = 0
s_index = 0

for f_array in f_t_array:
    for s_array in s_t_array:
        current_distance = distance.cosine(f_array, s_array)
        s_index += 1
        if current_distance < previous_distance:
            previous_distance = current_distance
            first_sentence = f_index
            second_sentence = s_index
    f_index += 1
    s_index = 0

print("Current Distance ([" + str(first_sentence) + "] - [" + str(second_sentence) + "]) - " + str(current_distance))
print()
print("First Sentence - " + str(first_sentence))
print("Second Sentence - " + str(second_sentence))

print()
exit_event=input("Press Anything to exit...")