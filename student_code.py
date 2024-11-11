from crypt import *
from collections import Counter




symbols = ['b', 'j', '\r', 'J', '”', ')', 'Â', 'É', 'ê', '5', 't', '9', 'Y', '%', 'N', 'B', 'V', '\ufeff', 'Ê', '?',
            '’', 'i', ':', 's', 'C', 'â', 'ï', 'W', 'y', 'p', 'D', '—', '«', 'º', 'A', '3', 'n', '0', 'q', '4', 'e',
            'T', 'È', '$', 'U', 'v', '»', 'l', 'P', 'X', 'Z', 'À', 'ç', 'u', '…', 'î', 'L', 'k', 'E', 'R', '2', '_',
            '8', 'é', 'O', 'Î', '‘', 'a', 'F', 'H', 'c', '[', '(', "'", 'è', 'I', '/', '!', ' ', '°', 'S', '•', '#',
            'x', 'à', 'g', '*', 'Q', 'w', '1', 'û', '7', 'G', 'm', '™', 'K', 'z', '\n', 'o', 'ù', ',', 'r', ']', '.',
            'M', 'Ç', '“', 'h', '-', 'f', 'ë', '6', ';', 'd', 'ô', 'e ', 's ', 't ', 'es', ' d', '\r\n', 'en', 'qu',
            ' l', 're', ' p', 'de', 'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue', 'an', 'te', ' a',
            'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', ' m', 'ce', 'ne', 'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ',
            'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa', 'au', 'el', 'ti', 'st', 'un', 'em',
            'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r', 'ss', 'u ', 'po', 'ro', 'ri', 'pr',
            's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ', 've', 'nc', 'om', ' o', 'je', 'no', 'rt',
            'à ', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', ' à', ' u', "l'", "'a", 'rs',
            'pl', 'é ', '; ', 'ho', 'té', 'ét', 'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i",
            'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']

original_key = gen_key(symbols)
url1 = "https://www.gutenberg.org/ebooks/13846.txt.utf-8"
corpus1 = load_text_from_web(url1)
url2 = "https://www.gutenberg.org/ebooks/4650.txt.utf-8"
corpus2 = load_text_from_web(url2)
corpus = corpus1[10000:30000] + corpus2[10000:30000]
encoded_text = chiffrer(corpus, original_key, original_key)



def decrypt(c):

    chunk_size = 8
    decrypted_text = ""
    for i in range(0, len(c), chunk_size):

        chunk = c[i:i + chunk_size]
        decrypted_text += primary_key.get(chunk, '?')
    return decrypted_text

def calculate_chunk_frequencies(encoded_text):
    chunks = [encoded_text[i:i + 8] for i in range(0, len(encoded_text), 8)]
    chunk_count = Counter(chunks)
    total_chunks = sum(chunk_count.values())
    chunk_frequencies = {chunk: (count / total_chunks) * 100 for chunk, count in chunk_count.items()}
    return chunk_frequencies

def count_symbol_percentages(plain_text, symbols):
    symbol_count = Counter()
    i = 0
    while i < len(plain_text):
        match_found = False
        for symbol in sorted(symbols, key=len, reverse=True):
            if plain_text[i:i + len(symbol)] == symbol:
                symbol_count[symbol] += 1
                i += len(symbol)
                match_found = True
                break
        if not match_found:
            i += 1
    total_matched_symbols = sum(symbol_count.values())
    symbol_percentage = {symbol: (count / total_matched_symbols) * 100 for symbol, count in symbol_count.items()}
    return symbol_percentage


def textTest():
    text_test1 = load_text_from_web("https://www.gutenberg.org/cache/epub/13951/pg13951.txt")[10000:30000]
    text_test2 = load_text_from_web("https://www.gutenberg.org/cache/epub/798/pg798.txt")[10000:30000]
    combined_text = text_test1 + text_test2
    return combined_text


def generate_key_from_closest_match(chunk_frequencies, reference_frequencies, tolerance=0.40):

    key_mapping = {}
    sorted_symbols = sorted(reference_frequencies.items(), key=lambda item: item[1], reverse=True)

    for chunk, chunk_freq in chunk_frequencies.items():
        closest_symbol = None
        smallest_diff = float('inf')

        for symbol, symbol_freq in sorted_symbols:
            difference = abs(chunk_freq - symbol_freq) / symbol_freq
            if difference < smallest_diff and difference <= tolerance:
                smallest_diff = difference
                closest_symbol = symbol
        key_mapping[chunk] = closest_symbol if closest_symbol else '?'

    return key_mapping

reference_text = textTest()
expected_frequencies = count_symbol_percentages(reference_text, symbols)
chunk_frequencies = calculate_chunk_frequencies(encoded_text)
primary_key = generate_key_from_closest_match(chunk_frequencies, expected_frequencies)
decode_text = decrypt(encoded_text)


