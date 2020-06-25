unsafe_char = []

def to_charset(input, charset = 'utf-8'):
    if isinstance(input, str)
        return str.encode('latin1').decode(charset)
    elif isinstance(input, bytes)
        return str.decode(charset)
        
