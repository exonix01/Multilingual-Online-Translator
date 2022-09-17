import argparse
import requests
from bs4 import BeautifulSoup


def translate(word, language_from, language_to, number_results=5):
    url_base = 'https://context.reverso.net/translation'
    url1 = f'{language_from.lower()}-{language_to.lower()}'
    url = '/'.join([url_base, url1, word])
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    if not r:
        print(f"Sorry, unable to find {word}")
        return 'Word error'
    soup = BeautifulSoup(r.content, 'html.parser')

    words = []
    sentences = []
    for translate_word in soup.find_all('span', {'class': 'display-term'}):
        words.append(translate_word.text)
    for divs in soup.find_all('div', {'class': 'example'}):
        for sentence in divs.find_all('span', {'class': 'text'}):
            sentences.append(sentence.text.strip())

    print_translate(language_to, word, words, sentences, number_results)


def print_translate(language, word, words, sentences, number_results):
    with open(f'{word}.txt', 'a', encoding='utf-8') as file:
        print_and_save(file, f'{language} Translations:')
        for n, word in enumerate(words):
            if n > number_results - 1:
                break
            print_and_save(file, word)
        print_and_save(file, f'\n{language} Examples:')
        for n, sentence in enumerate(sentences):
            if n > 2 * number_results - 1:
                break
            if n > 0 and n % 2 == 1:
                print_and_save(file, sentence + '\n')
            else:
                print_and_save(file, sentence)


def print_and_save(file, line):
    print(line)
    file.write(line + '\n')


def main():
    languages = ('arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese', 'dutch', 'polish',
                 'portuguese', 'romanian', 'russian', 'turkish')

    parser = argparse.ArgumentParser()
    parser.add_argument('language_from')
    parser.add_argument('language_to')
    parser.add_argument('word')
    args = parser.parse_args()
    language_from = args.language_from.lower()
    language_to = args.language_to.lower()
    word = args.word.lower()

    if language_from not in languages:
        print(f"Sorry, the program doesn't support {language_from}")
        return

    if not (language_to in languages or language_to == 'all'):
        print(f"Sorry, the program doesn't support {language_to}")
        return

    if language_to == 'all':
        for lang in languages:
            if lang == language_from:
                continue
            else:
                result = translate(word, language_from, lang, 1)
                if result == 'Word error':
                    return
    else:
        result = translate(word, language_from, language_to, 5)
        if result == 'Word error':
            return


if __name__ == '__main__':
    main()
