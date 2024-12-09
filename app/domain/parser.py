from dataclasses import dataclass
from enum import Enum, IntEnum, auto
from typing import Dict

from app.domain import currencies_const
from app.domain.model.currency_rate import CurrencyRate
from app.domain.model_manager import DataManager
from app.tools.logger import Logger, LogType
from app.tools.singleton import Singleton


class TokenType(Enum):
    NUMBER = auto()
    CURRENCY = auto()
    LINKER = auto()


# INFO: this is used to avoid doing blabl[i] without knowig wht is i about
class TokenListId(IntEnum):
    # INFO: we need to start at 0, other wise first auto = 1
    SRC_NUMBER = 0
    SRC_CURRENCY = auto()
    LINKER = auto()
    DST_CURRENCY = auto()


@dataclass
class Token:
    type: TokenType
    value: str | float | None


# INFO : lexical analysis.
class _Lexer(metaclass=Singleton):
    def find_currency_code(self, words, i):
        """
        try to find currency code, from index i
        get the code and the number of found word
        """
        for code, names in currencies_const.REF_CURRENCIES.items():
            # check if corresponding to currencies
            # ensure to take the longest one
            longest_name = 0
            for name in names:
                name_words = name.split()
                name_size = len(name_words)
                if longest_name < name_size and words[i : i + name_size] == name_words:
                    longest_name = name_size
            if longest_name > 0:
                return code, longest_name
        return None, 0

    def generate_currency_token(self, currency_code):
        token = Token(
            type=TokenType.CURRENCY,
            value=currency_code,
        )
        return token

    def tokenize(self, input_text):
        # INFO: lower case to avoid useless parsing
        input_text = input_text.lower()

        # INFO: split into words
        words = input_text.split()
        tokens = []

        float_found = False
        linker_found = False
        src_curr_found = False
        dst_curr_found = False
        i = 0
        while i < len(words):
            if float_found is False:
                # ensure we found a float
                number = 0.0
                try:
                    number = float(words[i])
                except ValueError:
                    # if not continue parsing
                    raise Exception(f"first word need to be a number: {words[i]}")
                token = Token(
                    type=TokenType.NUMBER,
                    value=number,
                )
                tokens.append(token)
                float_found = True
                i += 1
                continue

            # INFO: find linker, add it to check order of words
            # multiple word not managed
            if linker_found is False:
                if words[i] in currencies_const.REF_CONVERSIONLINKER:
                    linker_found = True
                    token = Token(
                        type=TokenType.LINKER,
                        value=words[i],
                    )
                    tokens.append(token)
                    i += 1
                    continue

            # INFO: try to find if words match currency (code, name ou adjective)
            currency_code, words_used = self.find_currency_code(words, i)
            if words_used <= 0:
                raise Exception(f"unidentified currency word : {words[i]}")
            elif src_curr_found is False:
                tokens.append(self.generate_currency_token(currency_code))
                src_curr_found = True
            elif dst_curr_found is False:
                tokens.append(self.generate_currency_token(currency_code))
                dst_curr_found = True
            else:
                raise Exception(f"too many currency found: {words[i]}")
            i += words_used

        if (
            not float_found
            or not src_curr_found
            or not linker_found
            or not dst_curr_found
        ):
            errData = f"{float_found} {linker_found} {linker_found} {linker_found}"
            raise Exception(f"parse failed: unknown reason \n\t{errData}")
        return tokens


# INFO : Manage syntax analysis
class _Parser(metaclass=Singleton):
    def __init__(self):
        self.lexer = _Lexer()

    def __transform_result(
        self, tokens, currencies: Dict[str, CurrencyRate]
    ) -> str | None:
        data_mgr = DataManager()  # singleton
        src_amount = tokens[TokenListId.SRC_NUMBER].value
        dst_amount = 0.0
        src_curr = tokens[TokenListId.SRC_CURRENCY].value
        dst_curr = tokens[TokenListId.DST_CURRENCY].value

        eur_amount = src_amount
        # INFO: 1 / rate because it's reverse
        if src_curr != "EUR":
            eur_amount = src_amount * 1.0 / currencies[dst_curr].rate
        dst_amount = eur_amount * currencies[dst_curr].rate

        # INFO: only output amount is 2 digit max
        answer = f"{src_amount} {src_curr} = {dst_amount:.2f} {dst_curr}"
        return answer

    def parse(self, data: str, currencies: Dict[str, CurrencyRate]) -> str | None:
        tokens = self.lexer.tokenize(data)
        # INFO: validation verification
        if (
            len(tokens) == 4
            and tokens[TokenListId.SRC_NUMBER].type == TokenType.NUMBER
            and tokens[TokenListId.SRC_CURRENCY].type == TokenType.CURRENCY
            and tokens[TokenListId.LINKER].type == TokenType.LINKER
            and tokens[TokenListId.DST_CURRENCY].type == TokenType.CURRENCY
        ):
            return self.__transform_result(tokens, currencies)
        print("syntax error")
        return None


def parse_query(input_query: str, currencies: Dict[str, CurrencyRate]) -> str | None:
    toReturn = None
    try:
        # INFO: not just allocate once because it's a singleton
        parser = _Parser()
        toReturn = parser.parse(input_query, currencies)
    except Exception as e:
        additionnalInfo: str = str(e)
        Logger.push_log(LogType.ERROR, "parse failed", additionnalInfo)
    finally:
        return toReturn
