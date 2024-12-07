# INFO: this readme is like a log book last entry at the top

# ---------------
Then I add the first version of the parser
I try to use yacc and lex at first with regexp
like :
    class Lexer:
        tokens = ('NUMBER', 'CURRENCY', 'CONVERT')

        def t_NUMBER(self, t: LexToken) -> LexToken:
            r'\d+(\.\d+)?'
            t.value = float(t.value)  # Convertir en float
            return t

        def t_CURRENCY(self, t: LexToken) -> LexToken:
            r'euros|dollars'
            return t

        def t_CONVERT(self, t: LexToken) -> LexToken:
            r'en'
            return t

        t_ignore = ' \t'
        def t_error(self, t: LexToken):
            print(f"Caractère illégal : {t.value[0]}")
            t.lexer.skip(1)

        def build(self):
            self.lexer = lex.lex(module=self)
but the instruction specify no regexp
and ply without regexp seems a bit useless ?
so i remove it

I recommend you to install pytest-cov to have a good idea
of testing coverage

# ---------------
First I set up my environment:
I start with, imo the most simplified environment
setting up a route for money conversion
get the data from the file and adapt it for conversion
prepare a test file

