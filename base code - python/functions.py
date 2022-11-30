def huffmanCode(lenghts):
    #Slide 34 algorithm
    temp = {}
    codes = {}
    bl_count = {}
    for i in range(max(lenghts.values())+1):
        bl_count[i] = 0

    for i in lenghts.keys():
	    if(lenghts[i] != 0):
                bl_count[lenghts[i]] += 1
                bl_count[0] = 0

    code = 0
    next_code = {}
    for i in range(1, max(lenghts.values())+1):
        code = (code + bl_count[i-1]) << 1
        next_code[i] = code
    
    for i in bl_count.keys():
        if(bl_count[i] != 0):
            for j in lenghts.keys():
                if(lenghts[j] == i):
                    codes[j] = bin(next_code[i]).split('b')[1]
                    next_code[i] += 1

    #Fills the binary code with zeros where it is suposed to be
    for i in codes.keys():
        if(len(codes[i]) < lenghts[i]):
            codes[i] = (lenghts[i] - len(codes[i])) * "0" + codes[i]

    for i in sorted(list(codes.keys())):
        temp[i] = codes[i]
    codes =temp

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
