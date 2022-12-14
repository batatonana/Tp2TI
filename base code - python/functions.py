def huffmanCode(lenghts):
    codes = {}
    bl_count = {}
    for i in range(max(lenghts.values())+1):
        bl_count[i] = 0

    for i in lenghts.keys():
	    if(lenghts[i] != 0):
                bl_count[lenghts[i]] += 1
                bl_count[0] = 0

    print("bl_count: ", bl_count)
    code = 0
    next_code = {}
    for i in range(1, max(lenghts.values())+1):
        code = (code + bl_count[i-1]) << 1
        next_code[i] = code
    print("next_code: ", next_code)
    
    for i in bl_count.keys():
        if(bl_count[i] != 0):
            for j in lenghts.keys():
                if(lenghts[j] == i):
                    codes[j] = bin(next_code[i]).split('b')[1]
                    next_code[i] += 1


    return codes

#Fucntion for exercice 4: Getting Hlit_Lens
def search_tree_by_bit(gzip, HCLEN_tree, HLIT):
    n = 0
    HLIT_lenghts = {}
    while n < HLIT:
        bit = gzip.readBits(1)
        pos = HCLEN_tree.nextNode(str(bit))
        if(pos >= 0):
            if(pos == 16):
                repeat = 3
                bit = 0
                for i in range(2):
                    bits = gzip.readBits(1)
                    bits = bits << i
                    bit = bit | bits
                repeat += bit
                for i in range(repeat):
                    HLIT_lenghts[n] = HLIT_lenghts[n-1]
                    n += 1
            elif(pos == 17):
                repeat = 3
                bit = 0
                for i in range(3):
                    bits = gzip.readBits(1)
                    bits = bits << i
                    bit = bit | bits
                repeat += bit
                for i in range(repeat):
                    HLIT_lenghts[n] = 0
                    n+=1
            elif(pos == 18):
                repeat = 11
                bit = 0
                for i in range(7):
                    bits = gzip.readBits(1)
                    bits = bits << i
                    bit = bit | bits
                repeat += bit
                for i in range(repeat):
                    HLIT_lenghts[n] = 0
                    n+=1
            else:
                HLIT_lenghts[n] = pos
                n+=1
            HCLEN_tree.resetCurNode()
    return HLIT_lenghts

def creates_tree(codes):
    tree = HuffmanTree()
    for i in codes.keys():tree.addNode(codes[i], i)
    return tree

def decompress(gzip, HLIT_tree, HDIST_tree):
    output = []
    pos = 0;
    while pos != 256:
        bit = gzip.readBits(1)
        pos = HLIT_tree.nextNode(str(bit))
        if(pos >= 0):
            if(pos < 256):
                output += [pos]
            else:
                size = [0,0]
                if(255<pos<265):
                    size[0] = pos-254
                elif (pos == 285):
                    size[0] = 258
                else:
                    #Algoritm to calculate bits to read
                    toRead = ((pos-265)//4)+1
                    aux = 11 # aux stating value if pos greater or equal to 265
                    for i in range(1, toRead): # Algorithm to calculate the number of bits to read
                        aux += (4 * (2 ** i))
                    aux += ((pos-265)%4*(2**toRead))+gzip.readBits(toRead)
                    size[0] = aux
                # dist = Backwards Distance
                dist = -2
                while dist < 0:
                    # Reads the font and searches HDIST_tree
                    dist = HDIST_tree.nextNode(str(gzip.readBits(1)))
                HDIST_tree.resetCurNode()
                if (dist < 4):
                    size[1] = dist+1
                else:
                    # Calculates the bits to read
                    toRead = ((dist-4)//2)+1
                    aux = 5 # aux stating value if dist greater or equal to 4
                    for i in range(1, toRead): # algorithm to calculate
                        aux += (2 * (2 ** i))
                    aux += ((dist-4)%2)*(2**toRead) + gzip.readBits(toRead)
                    size[1] = aux
                # Reads the font dist backwards and length forward
                start = len(output) - size[1]
                for i in range(size[0]):
                    output += [output[start+i]]
                
            HLIT_tree.resetCurNode()
    return output

def save_to_file(output):
    f = open("Resultado.txt", "wb")
    f.write(bytes(output))
    f.close