def encode( frame ):
    ''' encode frame based on rfc6455 '''
    bytesFormatted = []
    bytesFormatted.append(129)

    bytesRaw = frame.encode()
    bytesLength = len(bytesRaw)

    if bytesLength <= 125:
        bytesFormatted.append(bytesLength)
    elif 126 <= bytesLength <= 65535:
        bytesFormatted.append(126)
        bytesFormatted.append((bytesLength >> 8) & 255)
        bytesFormatted.append(bytesLength & 255)
    else:
        bytesFormatted.append(127)
        bytesFormatted.append((bytesLength >> 56) & 255)
        bytesFormatted.append((bytesLength >> 48) & 255)
        bytesFormatted.append((bytesLength >> 40) & 255)
        bytesFormatted.append((bytesLength >> 32) & 255)
        bytesFormatted.append((bytesLength >> 24) & 255)
        bytesFormatted.append((bytesLength >> 16) & 255)
        bytesFormatted.append((bytesLength >> 8) & 255)
        bytesFormatted.append(bytesLength & 255)

    bytesFormatted = bytes(bytesFormatted)
    bytesFormatted = bytesFormatted + bytesRaw
    return bytesFormatted