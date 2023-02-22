import textstat


def get_readability(text):
    """
    Get readability score for the text.
    :param text: text to analyze
    :return: readability score
    """
    if not text:
        return 0.0
    return textstat.flesch_reading_ease(text)
