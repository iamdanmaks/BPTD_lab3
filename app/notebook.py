straddling_checkboard = [
    ['а', 'и', 'т', 'е', 'с', 'н', 'о', '', '', ''],
    ['б', 'в', 'г', 'д', 'ж', 'з', 'к', 'л', 'м', 'п'],
    ['р', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы'],
    ['ь', 'э', 'ю', 'я', 'й', 'ё', '', '', '', '']
]


def encode_char(char):
    for i1, r in enumerate(straddling_checkboard):
        try:
            i2 = r.index(char.lower())
            return ((i1 + 7) % 10, (i2 + 1) % 10)
        except ValueError:
            continue


def text2tokens(text):
    if str(text).isdigit():
        return [int(ch) for ch in str(text)]
    tokens = []
    for ch in text:
        token = encode_char(ch)
        if token[0] == 7:
            tokens.append(
                token[1]
            )
        else:
            tokens.append(token[0])
            tokens.append(token[1])
    return tokens


def pad_sequences(message, key, mlen, klen):
    if mlen > klen:
        temp = key
        key = key * (mlen // klen)
        if len(key) < mlen:
            key += temp
            message += [0] * (len(key) - mlen)
    elif mlen < klen:
        message += [0] * abs(mlen - klen)

    return (message, key)


def encode_word(word, key):
    enc_word = text2tokens(word)

    enc_word, key = pad_sequences(
        enc_word, key, len(enc_word), len(key)
    )

    encoded = []
    for i, j in zip(enc_word, key):
        encoded.append(
            (i + j) % 10
        )
    
    return ''.join([str(e) for e in encoded])


def encode(message, key):
    enc_key = text2tokens(key)
    return ' '.join([encode_word(word, enc_key) for word in message.split()])


def decode_word(word, key):
    word = [int(ch) for ch in word]
    
    word, key = pad_sequences(
        word, key, len(word), len(key)
    )

    wlen = len(word)

    decoded = []
    curr_val = (word[0] - key[0]) % 10
    next_val = 0

    for i, (w, k) in enumerate(zip(word, key)):
        if i + 1 != wlen:
            next_val = (word[i + 1] - key[i + 1]) % 10

        if curr_val == 0 and next_val == 0:
            break
        
        decoded.append(curr_val)
        curr_val = next_val
    
    return decoded


def cypher2word(decoded):
    text = []
    i = 0

    while i < len(decoded):
        if decoded[i] > 0 and decoded[i] < 8:
            text.append(
                straddling_checkboard[0][decoded[i] - 1]
            )
            i += 1
        
        else:
            if i == len(decoded) - 1:
                break
            ind = (decoded[i] - 7) % 10
            text.append(
                straddling_checkboard[ind][(decoded[i + 1] - 1) % 10]
            )
            i += 2
    
    return ''.join(text)


def decode(message, key):
    enc_key = text2tokens(key)
    message = [decode_word(word, enc_key) for word in message.split()]
    return ' '.join([cypher2word(part) for part in message])
