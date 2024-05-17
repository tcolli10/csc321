import math
from os import write
import string


# def calculate_index_of_coincidence(text):
#     """
#     Calculate the Index of Coincidence (IC) of a given text.

#     Parameters:
#     text (str): The text for which the IC is to be calculated.

#     Returns:
#     float: The Index of Coincidence of the text.
#     """
#     # Filter non-alphabetic characters and convert to uppercase for uniformity.
#     filtered_text = ''.join([char.upper() for char in text if char.isalpha()])

#     # Calculate the frequency of each letter in the text.
#     letter_frequencies = [0] * 26
#     for char in filtered_text:
#         if 'A' <= char <= 'Z':
#             letter_frequencies[ord(char) - ord('A')] += 1

#     # Calculate the total number of characters and the sum of the products of each frequency with frequency-1.
#     n = len(filtered_text)
#     if n < 2:
#         # If there are less than two characters, the IC is 0 because the denominator would be zero.
#         return 0

#     sum_of_products = sum(f * (f - 1) for f in letter_frequencies)

#     # Calculate the IC using the formula.
#     index_of_coincidence = sum_of_products / (n * (n - 1))

#     return index_of_coincidence


def caesar_decrypt(text, shift):
    """Decrypt text by shifting letters by 'shift' amount."""
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) - shift
            if char.islower():
                if shifted < ord('a'):
                    shifted += 26
            elif shifted < ord('A'):
                shifted += 26
            decrypted_text += chr(shifted)
        else:
            decrypted_text += char
    return decrypted_text


def find_key_length(ciphertext):
    max_key_length = 20  # Adjust as needed
    likely_key_length = 1
    highest_avg_ic = 0

    for key_length in range(1, max_key_length + 1):
        avg_ic = sum(calculate_index_of_coincidence(
            ciphertext[i::key_length]) for i in range(key_length)) / key_length
        print(f"Key Length {key_length}: IC = {avg_ic}")
        if avg_ic > highest_avg_ic:
            highest_avg_ic = avg_ic
            likely_key_length = key_length

    return likely_key_length


def crack_vigenere(ciphertext):
    key_length = find_key_length(ciphertext)
    key = []

    # Decrypt each column separately
    for i in range(key_length):
        column_text = ''.join(ciphertext[j] for j in range(
            i, len(ciphertext), key_length))
        freqs = [column_text.count(chr(k + ord('A'))) for k in range(26)]
        max_freq = max(freqs)
        shift = freqs.index(max_freq)
        # Assuming 'E' is the most common letter
        likely_shift = (shift - 4) % 26
        key.append(chr(likely_shift + ord('A')))

    decrypted_text = ''.join(caesar_decrypt(ciphertext[i::key_length], ord(
        key[i % key_length]) - ord('A')) for i in range(key_length))

    return ''.join(key), decrypted_text


def find_most_repeated_patterns(text, min_size=3, max_size=None):
    """
    Find the most repeated substrings within a text, with a minimum and optional maximum size.

    Parameters:
    text (str): The text to analyze.
    min_size (int): The minimum size of the substring to consider.
    max_size (int): The maximum size of the substring to consider, if None, considers up to half the length of the text.

    Returns:
    dict: A dictionary with substrings as keys and their counts as values.
    """
    from collections import defaultdict

    # Set the maximum size of substrings to look for
    if max_size is None:
        max_size = len(text) // 2

    pattern_count = defaultdict(int)

    # Analyze text for repeated patterns of lengths between min_size and max_size
    for size in range(min_size, max_size + 1):
        for start in range(len(text) - size + 1):
            substring = text[start:start + size]
            pattern_count[substring] += 1

    # Filter out substrings that occur only once
    repeated_patterns = {pattern: count for pattern,
                         count in pattern_count.items() if count > 1}

    # Sort patterns by the number of repetitions (most to least)
    sorted_patterns = dict(
        sorted(repeated_patterns.items(), key=lambda item: item[1], reverse=True))

    return sorted_patterns


def find_most_common_length(strings_dict):
    """
    Determine which length of string occurs most frequently in the dictionary.

    Parameters:
    strings_dict (dict): A dictionary where keys are strings and values are the number of occurrences.

    Returns:
    tuple: The most common string length and its total number of occurrences.
    """
    # Dictionary to hold the total occurrences of each length
    length_dict = {}

    # Sum occurrences for each length
    for string, count in strings_dict.items():
        string_length = len(string)
        if string_length in length_dict:
            length_dict[string_length] += count
        else:
            length_dict[string_length] = count

    # Find the length with the maximum total occurrences
    if not length_dict:
        return None  # Return None if the input dictionary is empty
    max_length = max(length_dict, key=length_dict.get)
    max_count = length_dict[max_length]

    return (max_length, max_count)


def score_by_letter_frequency(text):
    # Expected frequencies for each letter in English language texts
    english_freq = {
        'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702,
        'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153,
        'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507,
        'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056,
        'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150, 'y': 1.974, 'z': 0.074
    }
    # Normalize the frequencies
    total = sum(english_freq.values())
    for letter in english_freq:
        english_freq[letter] /= total

    # Count each letter in the text
    count = {char: text.lower().count(char) for char in english_freq}
    total_letters = sum(count.values())

    # Calculate chi-squared statistic
    chi_squared = 0
    for letter, freq in english_freq.items():
        observed = count[letter]
        expected = freq * total_letters
        if expected > 0:  # Avoid division by zero
            chi_squared += (observed - expected) ** 2 / expected

    return chi_squared


# def vigenere_decrypt(ciphertext, key):
#     """Decrypts the ciphertext using the provided key, ignoring spaces and non-alphabetical characters."""
#     plaintext = []
#     key_length = len(key)
#     # Ensures the key is only alphabetic
#     key_as_int = [ord(i.upper()) - ord('A') for i in key if i.isalpha()]
#     key_index = 0

#     for char in ciphertext:
#         if char.isalpha():  # Process only alphabetic characters
#             # Convert letter to 0-25 range and shift by the corresponding key character, adjusted to 0-25 range
#             # shifted_value = (ord(char.upper()) - ord('A') -
#             #                  key_as_int[key_index % key_length]) % 26
#             shifted_value = (ord(char.upper()) - ord('A') -
#                              key_as_int[key_index % key_length]) % 26
#             decrypted_char = chr(shifted_value + ord('A'))
#             plaintext.append(decrypted_char)
#             key_index += 1  # Move to the next key character only if we've used it
#         else:
#             # Directly append non-alphabetical characters
#             plaintext.append(char)

#     return ''.join(plaintext)

def vigenere_decrypt(ciphertext, key):
    """Decrypts the ciphertext using the provided key, ignoring spaces and non-alphabetical characters."""
    plaintext = []
    key_length = len(key)
    # Ensures the key is only alphabetic and uppercase
    key_as_int = [ord(i.upper()) - ord('A') for i in key if i.isalpha()]
    key_index = 0

    for char in ciphertext:
        if char.isalpha():  # Process only alphabetic characters
            # Determine if the character is uppercase or lowercase
            is_upper = char.isupper()
            # Convert letter to 0-25 range and shift by the corresponding key character, adjusted to 0-25 range
            shifted_value = (ord(char.upper()) - ord('A') -
                             key_as_int[key_index % key_length]) % 26
            decrypted_char = chr(shifted_value + ord('A'))
            # Convert back to the original case
            if not is_upper:
                decrypted_char = decrypted_char.lower()
            plaintext.append(decrypted_char)
            key_index += 1  # Move to the next key character only if we've used it
        else:
            # Directly append non-alphabetical characters
            plaintext.append(char)

    return ''.join(plaintext)


class DecryptedEntry:
    key: str
    decryptedText: str
    score: float

    def __init__(self, key: str, decrypted_text: str, score: float):
        self.key = key
        self.decryptedText = decrypted_text
        self.score = score

    def __repr__(self):
        return f"{self.key}: {self.decrypted_text}, Score: {self.score}"


def insertEntry(newEntry: DecryptedEntry, entries: list[DecryptedEntry]):
    entries.append(newEntry)
    entries.sort(key=lambda entry: entry.score)
    while len(entries) > 50:
        entries.pop(-1)
    return entries


def brute_force_decrypt_vigenere_easy(ciphertext):
    """Attempts to decrypt the given ciphertext with all possible keys of length 3."""
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    bestOptions: list[DecryptedEntry] = []

    # Iterate over every possible key combination of length 5
    for first in alphabet:
        for second in alphabet:
            for third in alphabet:
                for fourth in alphabet:
                    for fifth in alphabet:
                        key = first + second + third + fourth + fifth
                        decrypted_text = vigenere_decrypt(ciphertext, key)
                        newScore = score_by_letter_frequency(decrypted_text)
                        newEntry = DecryptedEntry(
                            key, decrypted_text, newScore)

                        if len(bestOptions) < 50:
                            bestOptions = insertEntry(newEntry, bestOptions)
                        elif bestOptions[4].score > newScore:
                            bestOptions = insertEntry(newEntry, bestOptions)

                        if len(bestOptions) > 50:
                            print('SOMETHING WENT WRONG TOO MANY ENTIRES')
    return bestOptions


def brute_force_decrypt_vigenere_medium(ciphertext):
    """Attempts to decrypt the given ciphertext with all possible keys of length 3."""
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    bestOptions: list[DecryptedEntry] = []

    # Iterate over every possible key combination of length 5
    for first in alphabet:
        for second in alphabet:
            for third in alphabet:
                for fourth in alphabet:
                    for fifth in alphabet:
                        for sixth in alphabet:
                            for seventh in alphabet:
                                for eighth in alphabet:
                                    for ninth in alphabet:
                                        key = first + second + third + fourth + fifth + sixth + seventh + eighth + ninth
                                        decrypted_text = vigenere_decrypt(
                                            ciphertext, key)
                                        newScore = score_by_letter_frequency(
                                            decrypted_text)
                                        newEntry = DecryptedEntry(
                                            key, decrypted_text, newScore)

                                        if len(bestOptions) < 5:
                                            bestOptions = insertEntry(
                                                newEntry, bestOptions)
                                        elif bestOptions[4].score > newScore:
                                            bestOptions = insertEntry(
                                                newEntry, bestOptions)

                                        if len(bestOptions) > 5:
                                            print(
                                                'SOMETHING WENT WRONG TOO MANY ENTIRES')
    return bestOptions


def brute_force_decrypt_vigenere_medium(ciphertext):
    """Attempts to decrypt the given ciphertext with all possible keys of length 3."""
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    bestOptions: list[DecryptedEntry] = []

    # Iterate over every possible key combination of length 5
    for first in alphabet:
        for second in alphabet:
            for third in alphabet:
                for fourth in alphabet:
                    for fifth in alphabet:
                        for sixth in alphabet:
                            for seventh in alphabet:
                                for eighth in alphabet:
                                    for ninth in alphabet:
                                        for tenth in alphabet:
                                            for eleventh in alphabet:
                                                for twelth in alphabet:
                                                    for thirteenth in alphabet:
                                                        key = first + second + third + fourth + fifth + sixth + \
                                                            seventh + eighth + ninth + tenth + eleventh + twelth + thirteenth
                                                        decrypted_text = vigenere_decrypt(
                                                            ciphertext, key)
                                                        newScore = score_by_letter_frequency(
                                                            decrypted_text)
                                                        newEntry = DecryptedEntry(
                                                            key, decrypted_text, newScore)

                                                        if len(bestOptions) < 5:
                                                            bestOptions = insertEntry(
                                                                newEntry, bestOptions)
                                                        elif bestOptions[4].score > newScore:
                                                            bestOptions = insertEntry(
                                                                newEntry, bestOptions)

                                                        if len(bestOptions) > 5:
                                                            print(
                                                                'SOMETHING WENT WRONG TOO MANY ENTIRES')
    return bestOptions


def calculate_ic(text):
    frequency = [0] * 26
    for char in text:
        if char in string.ascii_uppercase:
            frequency[ord(char) - ord('A')] += 1
    n = len(text)
    ic = sum(f * (f - 1) for f in frequency) / (n * (n - 1)) if n > 1 else 0
    return ic


def get_text_columns(text, key_length):
    columns = ['' for _ in range(key_length)]
    for i, char in enumerate(text):
        if char in string.ascii_uppercase:
            columns[i % key_length] += char
    return columns


def find_key_length(ciphertext, max_key_length):
    ciphertext = ''.join(filter(str.isalpha, ciphertext)).upper()
    ics = []
    for key_length in range(1, max_key_length + 1):
        columns = get_text_columns(ciphertext, key_length)
        avg_ic = sum(calculate_ic(col) for col in columns) / key_length
        ics.append((key_length, avg_ic))
    # The key length with the highest average IC is most likely to be the correct key length
    likely_key_length = max(ics, key=lambda x: x[1])[0]
    return likely_key_length, ics


def __main__():
    file = input("Enter the file name to decrypt by vigenere : ")
    filePath = "./encrypted/" + file
    fileToDecrypt = open(filePath, "r")
    text = fileToDecrypt.read()
    if file == 'vigenere_easy_encrypt.txt':
        bestFound = brute_force_decrypt_vigenere_easy(text)
        for i in range(len(bestFound)):
            print(
                f'option {i + 1}\nkey: {bestFound[i].key}\ntext: {bestFound[i].decryptedText}\nscore: {bestFound[i].score}\n\n')

    # outfile = open('vAnswer1.txt', 'w')
    # # print(f'ioc: {calculate_index_of_coincidence(text)}')
    # pats = find_most_repeated_patterns(text)
    # print(text)
    # print(f'likely key length: {find_most_common_length(pats)}')
    # for pattern, count in pats.items():
        # print(f"{pattern}: {count}")
    # # print(vigenere_decrypt('zhd lkjjh', 'SDF'))

    # # key, decrypted_text = crack_vigenere(text)
    # # print("Estimated Key:", key)
    # # print("Decrypted Text:", decrypted_text)

    # max_key_length = 15
    # likely_key_length, ics = find_key_length(text, max_key_length)

    # print(f"Likely key length: {likely_key_length}")
    # print("Key length and their corresponding IC values:")
    # for key_length, ic_value in ics:
    #     print(f"Key Length: {key_length}, IC: {ic_value:.4f}")

    # print(vigenere_decrypt(text, 'MFXJT'))

    # bestFound: list[DecryptedEntry] = brute_force_decrypt_vigenere(text)
    # for i in range(len(bestFound)):
    #     print(
    #         f'option {i + 1}\nkey: {bestFound[i].key}\ntext: {bestFound[i].decryptedText}\nscore: {bestFound[i].score}\n\n')
    # # 'mfxjt'
    # print(vigenere_decrypt(text, 'mjt'))
    # fileToDecrypt.close()


if __name__ == "__main__":
    __main__()
