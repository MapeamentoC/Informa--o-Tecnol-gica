import os


def process_text(text, word_freq):
    words = text.split()

    for i, word in enumerate(words):
        if word not in word_freq:
            word_freq[word] = {'center': 0, 'left': {}, 'right': {}}

        word_freq[word]['center'] += 1

        if i > 0:
            left_word = words[i - 1]
            word_freq[word]['left'][left_word] = word_freq[word]['left'].get(
                left_word, 0) + 1

        if i < len(words) - 1:
            right_word = words[i + 1]
            word_freq[word]['right'][right_word] = word_freq[word]['right'].get(
                right_word, 0) + 1


def update_dependency_relationships(word_freq):
    for word, freq in word_freq.items():
        left_words = set(freq['left'].keys())
        right_words = set(freq['right'].keys())
        common_words = left_words.intersection(right_words)

        for common_word in common_words:
            left_dependents = set(word_freq[common_word]['left'].keys())
            right_dependents = set(word_freq[common_word]['right'].keys())

            if word in left_dependents and common_word in right_dependents:
                word_freq[word]['left'][common_word] = word_freq[word]['left'].get(
                    common_word, 0) + 1
                word_freq[common_word]['right'][word] = word_freq[common_word]['right'].get(
                    word, 0) + 1


def filter_dependent_words(word_freq):
    for word, freq in word_freq.items():
        left_sum = sum(freq['left'].values())
        left_mean = left_sum / \
            len(freq['left']) if len(freq['left']) > 0 else 0

        right_sum = sum(freq['right'].values())
        right_mean = right_sum / \
            len(freq['right']) if len(freq['right']) > 0 else 0

        word_freq[word]['left'] = {left_word: left_freq for left_word,
                                   left_freq in freq['left'].items() if left_freq > left_mean}
        word_freq[word]['right'] = {right_word: right_freq for right_word,
                                    right_freq in freq['right'].items() if right_freq > right_mean}


def process_files_in_directory(directory):
    word_freq = {}

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf8") as file:
                text = file.read().lower()
                process_text(text, word_freq)

    update_dependency_relationships(word_freq)
    filter_dependent_words(word_freq)
    return word_freq


def generate_sequences(word_freq, max_sequence_length=8):
    for length in range(2, max_sequence_length + 1):
        generated_sequences = set()  # Conjunto para armazenar as sequências já geradas
        with open(f"sequencias/sequencias_{length}.txt", "w", encoding='utf8') as file:
            for word in word_freq:
                if len(word_freq[word]['left']) >= length - 1 and len(word_freq[word]['right']) >= 1:
                    left_words = list(word_freq[word]['left'].keys())
                    for left_seq in generate_subsequences(left_words, length - 1):
                        right_words = list(word_freq[word]['right'].keys())
                        for right_word in right_words:
                            if right_word in word_freq[left_seq]['right']:
                                sequence = join_words_with_comma(
                                    [left_seq, word, right_word])
                                if sequence not in generated_sequences:
                                    file.write(sequence + "\n")
                                    generated_sequences.add(sequence)


def generate_subsequences(words, length):
    if length == 1:
        return words
    else:
        subsequences = []
        for word in words:
            new_words = [
                word + subsequence for subsequence in generate_subsequences(words, length - 1)]
            subsequences.extend(new_words)
        return subsequences


def join_words_with_comma(words_list):
    return ",".join(words_list)


def main():
    directory = "./"  # Substitua pelo caminho do diretório onde estão os arquivos
    word_frequency = process_files_in_directory(directory)
    generate_sequences(word_frequency)


if __name__ == "__main__":
    main()
