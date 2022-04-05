import re,math
def main():
    text = input("Text: ")
    lett = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    avg_let_per_word = lett / words * 100
    avg_sent = sentences / words * 100
    index = round((0.0588 * avg_let_per_word) - (0.296 * avg_sent) - 15.8)

    if (index < 1):
        print("Before Grade 1")
    elif(index>16):
        print("Grade 16+")
    else:
        print(f'Grade {index}')


def count_words(phrase):
    words = [ s for s in re.split(r'[" ",.?!;]+', phrase) if s != '' ]
    return int(len(words))


def count_letters(phrase):
    pattern = re.compile(r'[a-zA-Z]+')
    matches = re.findall(pattern, phrase)
    return int(len("".join(matches)))


def count_sentences(phrase):
    sentence = [ s for s in re.split(r'[.!?]', phrase)]
    return float(len(sentence)-1)

main()