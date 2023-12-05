import unicodedata

def string_spaces(string):
    return ' '.join(string.split())


def string_to_ascii(string, enie=False):
    if enie == True:
        string = string.replace("ñ", "#!#").replace("Ñ", "$!$")
        string = unicodedata.normalize('NFKD', string).encode('ascii','ignore').decode('ascii')
        string = string.replace("#!#", "ñ").replace("$!$", "Ñ")
    else:
        string = unicodedata.normalize('NFKD', string).encode('ascii','ignore').decode('ascii')
    return string


def stringmagic(string, case='original', enie=False):
    string = string_spaces(string)
    string = string_to_ascii(string, enie=enie)
    return string