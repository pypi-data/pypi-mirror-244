from thefuzz import fuzz


def split(
    words: str | list[str],
    reference: list[str],
    preserve_newlines: bool = False,
    max_neighbours=5,
    match_region=500,
) -> list[str]:
    """Split a string or group a collection of words into a list by matching another
    list of similar words, to create accurate subtitles from the actual script and
    inaccurate (generated) subtitles.

    Example:

        >>> split("this must be a good thing", reference=["this", "is", "a", "good", "thing"])
        ['this', 'must be', 'a', 'good', 'thing']

        >>> split("this is a good thing", reference=["this", "must", "be", "a", "good", "thing"])
        ['this', '', 'is', 'a', 'good', 'thing']

        >>> split("a big foo bar", ["a", "big", "ff"])
        ['a', 'big', 'foo bar']

        >>> split("line1.\\n\\nline2.\\nline3.", reference=["1", "2", "3"], preserve_newlines=True)
        ['line1.\\n\\n', 'line2.\\n', 'line3.']
    """

    if isinstance(words, str):
        if preserve_newlines:
            lines = f"{words}\n".splitlines()
            lines_count = len(lines)
            words = []
            for i, line in enumerate(lines):
                words.extend(line.split())
                if words and i < lines_count - 1:
                    words[-1] += "\n"
        else:
            words = words.split()

    result = []
    actual_index = 0

    for i, _ in enumerate(reference):
        best_ratio = 0
        word = ""

        if result and len(reference[i:]) > len(words[actual_index:]):
            remaining_words = " ".join(words[actual_index + 1 : match_region])
            remaining_ref = " ".join(reference[i + 1 : match_region])
            skipped_ref = " ".join(reference[i + 2 : match_region])
            if fuzz.ratio(skipped_ref, remaining_words) > fuzz.ratio(
                remaining_ref, remaining_words
            ):
                result.append(word)
                continue

        for j, actual_word in enumerate(
            words[actual_index : actual_index + max_neighbours]
        ):
            if actual_word == reference[i]:
                word = actual_word
                actual_index += 1
                break

            if j != 0:
                actual_word = " " + actual_word

            new_word = word + actual_word
            remaining_ref = " ".join(reference[i + 1 : match_region])
            remaining_words = " ".join(words[actual_index + 1 : match_region])
            ratio = fuzz.ratio(remaining_ref, remaining_words)
            if ratio > best_ratio:
                best_ratio = ratio
                word = new_word
                actual_index += 1
            else:
                break

        result.append(word)

    if result and result[-1] == "":
        result[-1] = " ".join(words[actual_index:])

    return result
