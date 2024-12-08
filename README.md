#INFO: It's like a log book, each item are separated by ---------------
# HOW to
first set up the db
    copy app.env in `.env` file.

    Depending on your docker and docker-compose setup you might need to use
    `docker-compose up -d` or `docker compose up -d`
    then  call ```make create-db``` to create the db

then update the db content with 
```poetry run python .\scripts\update_db.py```

then run the server locally: 

    - install poetry
    - poetry install
    - poetry run python '-m' 'uvicorn' 'app.main:app' '--reload'

note for windows user:
    - use ```cmdenv.bat``` to correctly set the env var

# History
# ---------------
I set up my environment:
I start with, imo the most simplified environment
setting up a route for money conversion
get the data from the file and adapt it for conversion
prepare a test file

# ---------------
I add the first version of the parser
I try to use yacc and lex at first with regexp
like :
``` python
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
```
but the instruction specify no regexp
and ply without regexp seems a bit useless ?
so i remove it

# ---------------
I add the final parser with no regex and no ply
Crafted by hand because I need something fast

I implement a parser able to manage prompt mistake thanks to 
app.domain.currencies_const

# ---------------
I had many test
    - working test 
        - "10.32 euros en dollars" default test
        - "10.32 eurs = dollar" other words
        - "10.32 eurs = dollar américains" multiple currency word
        - "10.32 euro européen = dollar américains" multilple currency word in and out
        - "10.32 USD = USD" trade something that isn't euro and ensure correct value
        - "10.3285146196 jpy = jpy" check 2 digit rounding
    - failed test
        - "42" no valid query
        - "10.32 eurs dollar américains" missing element in query
        - "10.32 euro européen = dollar amricains" spell error in currency
        - "10.32 USD USD =" query not correctly ordered

I recommend you to install pytest-cov to have a good idea
of testing coverage

# ---------------
fix dependency order
add more info
prepare data for postgresDB
