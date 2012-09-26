import ply.lex as lex
import pprint

tokens = ('NAME', 'ADDRESS', 'PHONE', 'URL', 'ZAGAT', 'CATEGORY', 'TAGS', 'REVIEW')

def remove_trailing(string):
    while string.endswith(" "):
        string = string[:-1]
    return string

def t_ADDRESS(token):
    r'[0-9A-Za-z #&]+,[ ][A-Za-z]+,[ ][A-Za-z]+'
    token.type = 'ADDRESS'
    return token

def t_PHONE(token):
    r'\([0-9]{3}\)[ ][0-9]{3}-[0-9]{4}'
    token.type = 'PHONE'
    return token

def t_URL(token):
    r'([-A-Za-z0-9]+\.)+(com|org|info|net)'
    token.type = 'URL'
    return token

def t_REVIEW_1(token):
    r'".*"[ ]-[^\n]*'
    token.type = 'REVIEW'
    return token

def t_REVIEW_2(token):
    r'[^\n"]*"[^\n"]+"[^\n"]*'
    token.type = 'REVIEW'
    return token

def t_REVIEW_3(token):
    r'[0-9 ]+review[^\n]*'
    token.type = 'REVIEW'
    return token

def t_REVIEW_4(token):
    r'[^\n]*reviewer[^\n]*'
    token.type = 'REVIEW'
    return token

def t_REVIEW_5(token):
    r'[^\n]*Diners\'[ ]Choice[^\n]*'
    token.type = 'REVIEW'
    return token

def t_CATEGORY(token):
    r'Category:[^\n]+'
    token.type = 'CATEGORY'
    return token

def t_ZAGAT_STATS(token):
    r'[^\n]*(ZAGAT|reviews)[^\n]*'
    token.type = 'ZAGAT'
    return

def t_TAGS(token):
    #r'([A-Za-z0-9\' ]+[ ]:::[ ])+[^:\n]+'
    r'([A-Za-z0-9\' ]+[ ]:::[ ])+[A-Za-z0-9\' ]+'
    token.type = 'TAGS'
    token.value = token.value.split(" ::: ")
    return token

def t_NAME(token):
    r'([^:]:[^:]|[-A-Za-z\' 0-9&,])+'
    token.type = 'NAME'
    token.value = remove_trailing(token.value)
    return token

t_ignore = ' \t\v\r'

def t_error(t):
  print "Lexer: unexpected character " + t.value[0]
  t.lexer.skip(1) 

lexer = lex.lex() 

def run_lexer(input_string):
  lexer.input(input_string)
  result = [ ] 
  while True:
    tok = lexer.token()
    if not tok: break
    result = result + [(tok.type, tok.value)]
  return result

def main():
    f = open('more_raw_philly_data.txt', 'r')
    raw_string = f.read()
    results = (run_lexer(raw_string))
    
if __name__ == '__main__':
    main()
