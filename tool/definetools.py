
def saveNum(s):
    num = ['0','1','2','3','4','5','6','7','8','9','.']
    return s in num
def not_empty(s):
    return s and s.strip()
def removeTag(s):
    return s.getText()