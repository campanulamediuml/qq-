def main(a):
    func_list = [func_1(a),func_2(a)]
    for func in func_list:
        if func != None:
            break
    return func
         
        

def func_1(a):
    if a == 1:
        result = 'it is func_1'
        return result
    

def func_2(a):
    if a == 2:
        result = 'it is func_2'
        return result
    
def func_1(a):
    if a == 3:
        result = 'it is func_3'
        return result
    

def func_1(a):
    if a == 4:
        result = 'it is func_4'
        return result
    