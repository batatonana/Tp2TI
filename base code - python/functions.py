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