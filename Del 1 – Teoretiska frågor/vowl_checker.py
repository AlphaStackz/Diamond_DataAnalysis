word_input = input("Enter a word: ")

def vowel_checker(word):
    word = word.lower()
    vowels = ["a", "e", "i", "o", "u", "y", "å", "ä", "ö"]
    vowel_counts = {v: 0 for v in vowels}

    for char in word:
        if char in vowel_counts:
            vowel_counts[char] += 1

    return vowel_counts


result = vowel_checker(word_input)

for vowel, count in result.items():
    print(f"{vowel}: {count}")