import random


def encode(cadena):
    mapping = {
        "$": "a",
        "@": "e",
        "#": "0",
        "!": "o",
        "&": "1",
        "^": "2",
        "?": "3",
        "-": "4",
        "{": "5",
        "}": "6",
        "[": "7",
        "]": "8",
        "¿": "9",
        "a": "$",
        "e": "@",
        "i": "#",
        "o": "!",
        "u": "%",
        "1": "&",
        "2": "^",
        "3": "?",
        "4": "-",
        "5": "{",
        "6": "}",
        "7": "[",
        "8": "]",
        "9": "¿",
        "q": "i",
        "w": "o",
        "r": "u",
        "t": "q",
        "y": "w",
        "p": "E",
        "s": "r",
        "d": "t",
        "f": "y",
        "g": "u",
        "h": "d",
        "j": "f",
        "k": "g",
        "l": "h",
        "z": "j",
        "x": "k",
        "c": "l",
        "v": "z",
        "b": "x",
        "n": "c",
        "m": "v",
        "0": "€",
        "*": ":",
        "L": "V",
        "M": "I",
        "S": "H",
        "J": "O",
        "R": "T",
        "N": "P",
        "A": "Q",
        "E": "~",
        "G": "F",
        "J": "ñ",
    }

    nueva_cadena = ""
    for caracter in cadena:
        if caracter in mapping:
            nueva_cadena += mapping[caracter]
        else:
            nueva_cadena += caracter

    secret_key = (
        random.choice("df")
        + random.choice("hj")
        + random.choice("$^")
        + random.choice("%")
        + random.choice("#@")
        + random.choice("!?")
        + random.choice("-_")
        + random.choice("&f")
        + random.choice("vb")
        + "."
        + "L0123"
    )
    encrypted = nueva_cadena + "." + secret_key
    return encrypted


def decode(cadena):
    map = {
        "$": "a",
        "@": "e",
        "#": "i",
        "!": "o",
        "%": "u",
        "&": "1",
        "^": "2",
        "?": "3",
        "-": "4",
        "{": "5",
        "}": "6",
        "[": "7",
        "]": "8",
        "¿": "9",
        "a": "$",
        "e": "@",
        "i": "#",
        "o": "!",
        "u": "%",
        "1": "&",
        "2": "^",
        "3": "?",
        "4": "-",
        "5": "{",
        "6": "}",
        "7": "[",
        "8": "]",
        "9": "¿",
        "q": "I",
        "w": "O",
        "r": "U",
        "t": "q",
        "y": "w",
        "p": "E",
        "s": "r",
        "d": "t",
        "f": "y",
        "g": "u",
        "h": "d",
        "j": "f",
        "k": "g",
        "l": "h",
        "z": "j",
        "x": "k",
        "c": "l",
        "v": "z",
        "b": "x",
        "n": "c",
        "m": "v",
        "0": "€",
        "*": ":",
        "L": "V",
        "M": "I",
        "S": "H",
        "J": "O",
        "R": "T",
        "N": "P",
        "A": "Q",
        "E": "~",
        "G": "F",
        "J": "ñ",
    }
    map_inv = {v: k for k, v in map.items()}
    nueva_cadena = ""
    for caracter in cadena:
        if caracter in map_inv:
            nueva_cadena += map_inv[caracter]
        elif caracter == ".":
            break
        else:
            nueva_cadena += caracter

    return nueva_cadena
