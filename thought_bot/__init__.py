def an_or_a(word):
    """
    take a single word and decide if its an or a grammatically.
    :param word:
    :rtype: str
    """
    vowels = ["a", "e", "i", "o", "u"]
    if word[0].lower() in vowels:
        return "an"
    else:
        return "a"