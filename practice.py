words = list(input())

def is_vowel(letters):
    return  letters in  ['a','e','i','o','u']


def score_words(words):
    for word in words:
        vowel_count = 0
        for char in word:
            if is_vowel(char):
                vowel_count += 1
            else:
                if vowel_count % 2 == 0:
                    vowel_count += 2
        
    print(vowel_count)
    return vowel_count

score_words(words)

