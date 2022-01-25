import math


def norm(vec):

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    dot = 0
    for key in vec1:
        if vec2.get(key, None) != None:
            dot += vec1[key] * vec2[key]
    sum_squares1 = 0
    for key in vec1:
        sum_squares1 += vec1[key] ** 2
    sum_squares2 = 0
    for key in vec2:
        sum_squares2 += vec2[key] ** 2

    return dot / math.sqrt(sum_squares1 * sum_squares2)

def build_semantic_descriptors(sentences):
    dict = {}
    for sentence in sentences:
        for word in sentence:
            dict[word] = {}

    for sentence in sentences:
        for word in dict: # every distinct word in dict
            if word in sentence: # if this word isn't in the sentence, don't add anything to its dictionary

                for other_words in dict.fromkeys(sentence):

                    if other_words != word and other_words not in dict[word]:
                        dict[word][other_words] = 1
                    elif other_words != word and other_words in dict[word]:
                        dict[word][other_words] += 1
    return dict

def build_semantic_descriptors_from_files(filenames):
    f = ""
    for file in filenames:
        f += open(file, "r", encoding="latin1").read()
        f += " "
    f = f.lower()

    for char in [",", ":", ";"]:
        f = f.replace(char, "")
    f = f.replace("--"," ").replace("-"," ").replace("\n", " ")
    list_of_sent = f.replace("!", ".").replace("?", ".").split(". ")
    if f[-1][-1] in [",",".",":"]:
        f[-1] = f[-1][:-1]
    words_of_sent = []

    for i in range(len(list_of_sent)):

        words_of_sent.append(list(filter(None,list_of_sent[i].split(" "))))

    return build_semantic_descriptors(words_of_sent)

def test(string):
    string = string.lower()
    for char in [",", ":", ";"]:
        string = string.replace(char, "")
    string = string.replace("--"," ").replace("-"," ").replace("  "," ")
    list_of_sent = string.replace("!", ".").replace("?", ".").replace("\n", ". ").split(". ")
    words_of_sent = []
    for i in range(len(list_of_sent)):

        words_of_sent.append(list(filter(None,list_of_sent[i].split(" "))))
        #list(filter(None,list_of_sent[i])
    # for i in range(len(words_of_sent)):
    #     words_of_sent[i] = list(filter("", words_of_sent[i]))
    return build_semantic_descriptors(words_of_sent)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    # looks at the other words that appear in the context and compares frequency
    largest = -1
    closest_choice = choices[0]
    d = semantic_descriptors
    for i in range(len(choices)):
        if word in d.keys() and choices[i] in d.keys():
            if similarity_fn(d[word], d[choices[i]]) > largest:
                largest = similarity_fn(d[word], d[choices[i]])
                closest_choice = choices[i]
    return closest_choice

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    f = open(filename, "r", encoding="latin1").read().split("\n")
    number_correct = 0
    total_number = 0
    while '' in f:
        f.remove('')
    for line in f:
        line = line.split(" ") #each line is a list of format "question", "option", "option", "option"
        word = line[0]
        correct = line[1]
        choices = line[2:]
        total_number += 1
        if most_similar_word(word, choices, semantic_descriptors, similarity_fn) == correct:
            number_correct += 1
    if total_number != 0:
        return 100*number_correct/total_number
    else:
        return 0


if __name__ == "__main__":
    pass
