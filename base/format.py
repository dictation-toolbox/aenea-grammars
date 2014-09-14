import aenea.configuration


def snakeword(text):
    formatted = text[0][0].upper()
    formatted += text[0][1:]
    formatted += ('_' if len(text) > 1 else '')
    formatted += score(text[1:])
    return formatted


def score(text):
    return '_'.join(text)


def camel(text):
    return text[0] + ''.join([word.capitalize() for word in text[1:]])


def proper(text):
    return ''.join(word.capitalize() for word in text)


def relpath(text):
    return '/'.join(text)


def abspath(text):
    return '/' + relpath(text)


def scoperesolve(text):
    return '::'.join(text)


def jumble(text):
    return ''.join(text)


def dotword(text):
    return '.'.join(text)


def dashword(text):
    return '-'.join(text)


def natword(text):
    return ' '.join(text)


def sentence(text):
    return ' '.join([text[0].capitalize()] + text[1:])


def upper(text):
    return [word.upper() for word in text]


def lower(text):
    return [word.lower() for word in text]

# Export format functions as a configurable dictionary
FORMAT = aenea.configuration.make_grammar_commands('base', {
    'snakeword': snakeword,
    'score': score,
    'camel': camel,
    'proper': proper,
    'rel-path': relpath,
    'abs-path': abspath,
    'scope-resolve': scoperesolve,
    'jumble': jumble,
    'dotword': dotword,
    'dashword': dashword,
    'natword': natword,
    'sentence': sentence,
    'upper': upper,
    'natural': lower,
}, 'format.format')

# Export case transformations as a configurable dictionary
CASE = aenea.configuration.make_grammar_commands('base', {
    'upper': upper,
    'lower': lower,
}, 'format.case')
