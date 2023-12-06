'''
- check if a string is palindrome
- return top the most popular characters in a string
'''

def check_palindrome(str):
    if len(str) <= 1:
        return False
    str = str.strip().lower().replace(' ', '')
    return str == str[::-1]

def topK(str, K=5):
    d = {}
    str = str.replace(' ', '')
    for x in str:
        d[x] = d.get(x, 0) + 1
    l = [ (v, k) for k, v in d.items()]
    for i, p in enumerate(sorted(l, reverse=True)):
        print(p[0], p[1])
        if i == K-1:
            break

# if __name__ == '__main__':
#     print(check_palindrome('abcbad'))
#     print(topK('Bach khoa Ha Noi'))