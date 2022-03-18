
class Error:
    def __init__(self, name, details, position):
        self.name = name
        self.details = details
        self.position = position

    def as_string(self):
        result = f'{self.name} : {self.details} \n'
        result += f'  @ File {self.position.fn} , Line {self.position.ln + 1}'
        return result

class IllegalCharectorError(Error):
    def __init__(self,details,position):
        super().__init__('IllegalCharector', details, position)
    


class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

        
    def advance(self, current_char):
        self.idx+=1
        self.col+=1

        if current_char == '\n' :
            self.ln += 1
            self.col = 0

        return self
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)
        
        
"""
Tokens
"""

DIGITS = '0123456789'
TT_INT = 'TT_INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'

class Token:
    def __init__(self,type,value = None):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'


"""
Lexer

"""
class Lexer:
    def __init__(self,fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1,0,-1, fn,text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        
    def make_tokens(self):
        tokens = [];

        while self.current_char != None :
            
            if self.current_char in [' ','\t']:
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                pos = self.pos.copy()
                char = self.current_char
                self.advance()
                return [],IllegalCharectorError( "'"+ char +"'", pos) 
                
        return tokens, None
    
    def make_number(self):
        numstr = ''
        dotcount = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dotcount == 1: break
                dotcount+=1
                
            numstr += self.current_char

            self.advance()
            
        self.pos.idx -= 1
        if dotcount == 0:
            return Token(TT_INT, int(numstr))
        else:
            return Token(TT_FLOAT, float(numstr))

              


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error



    
