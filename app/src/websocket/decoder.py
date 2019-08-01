def decode( frame ):
    ''' decode websocket frame based on rfc6455#section-5 '''
    # https://stackoverflow.com/questions/15770079/decode-continuation-frame-in-websocket
    byteArray  = [character for character in frame]
    
    # https://wiki.python.org/moin/BitwiseOperators -> Aca explica lo que hace el & 
    # opCode     = byteArray[0] & 15
    
    datalength = byteArray[1] & 127
    indexFirstMask = 2 
    if datalength == 126:
        indexFirstMask = 4
    elif datalength == 127:
        indexFirstMask = 10
    masks = [m for m in byteArray[indexFirstMask : indexFirstMask+4]]
    indexFirstDataByte = indexFirstMask + 4
    decodedChars = []
    i = indexFirstDataByte
    j = 0
    while i < len(byteArray):
        decodedChars.append( chr(byteArray[i] ^ masks[j % 4]) )
        i += 1
        j += 1

    return ''.join(decodedChars)