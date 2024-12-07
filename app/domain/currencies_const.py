# INFO: use constant in set for different naming of currencies
# we need to have this kind of dictionnary
# to manage mispelling of words
# maybe some already existe, idk
REF_USD_WORDS = {
    "usd",
    "dollar",
    "dollars",
    # with accent
    "dollar américain",
    "dollar américains",
    "dollar americains",
    "dollars américains",
    # forgotten accent
    "dollar americain",
    "dollar americains",
    "dollar americains",
    "dollars americains",
    "us dollar",
    "american dollar",
    "us-dollar",
    "$",
}

REF_EUR_WORDS = [
    "eur",
    "eurs",
    "euros",
    "euro",
    "euro européen",
    "€",
]

REF_JPY_WORDS = [
    "jpy",
    "yen",
    "yens japonais",
    "¥",
]

REF_GBP_WORDS = [
    "gbp",
    "livres",
    "livres sterling",
    "£",
]

REF_BGN_WORDS = [
    "bgn",
]

REF_CZK_WORDS = [
    "czk",
]

REF_DKK_WORDS = [
    "dkk",
]

REF_HUF_WORDS = [
    "dkk",
]

REF_PLN_WORDS = [
    "pln",
]

REF_RON_WORDS = [
    "ron",
]

REF_SEK_WORDS = [
    "sek",
]

REF_CHF_WORDS = [
    "chf",
]

REF_ISK_WORDS = [
    "isk",
]

REF_NOK_WORDS = [
    "nok",
]

REF_TRY_WORDS = [
    "try",
]
REF_AUD_WORDS = [
    "aud",
]

REF_BRL_WORDS = [
    "brl",
]
REF_CAD_WORDS = [
    "cad",
]

REF_CNY_WORDS = [
    "cny",
]

REF_HKD_WORDS = [
    "hkd",
]

REF_IDR_WORDS = [
    "idr",
]

REF_ILS_WORDS = [
    "ils",
]

REF_INR_WORDS = [
    "inr",
]

REF_KRW_WORDS = [
    "krw",
]

REF_MXN_WORDS = [
    "pln",
]

REF_MYR_WORDS = [
    "myr",
]

REF_NZD_WORDS = [
    "nzd",
]

REF_PHP_WORDS = [
    "php",
]

REF_SGD_WORDS = [
    "sgd",
]

REF_THB_WORDS = [
    "thb",
]

REF_ZAR_WORDS = [
    "zar",
]

REF_CURRENCIES = {
    "USD": REF_USD_WORDS,
    "EUR": REF_EUR_WORDS,
    "JPY": REF_JPY_WORDS,
    "BGN": REF_BGN_WORDS,
    "CZK": REF_CZK_WORDS,
    "DKK": REF_DKK_WORDS,
    "GBP": REF_GBP_WORDS,
    "HUF": REF_HUF_WORDS,
    "PLN": REF_PLN_WORDS,
    "RON": REF_RON_WORDS,
    "SEK": REF_RON_WORDS,
    "CHF": REF_CHF_WORDS,
    "ISK": REF_ISK_WORDS,
    "NOK": REF_NOK_WORDS,
    "TRY": REF_TRY_WORDS,
    "AUD": REF_AUD_WORDS,
    "BRL": REF_BRL_WORDS,
    "CAD": REF_CAD_WORDS,
    "CNY": REF_CNY_WORDS,
    "HKD": REF_HKD_WORDS,
    "IDR": REF_IDR_WORDS,
    "ILS": REF_ILS_WORDS,
    "INR": REF_INR_WORDS,
    "KRW": REF_KRW_WORDS,
    "MXN": REF_MXN_WORDS,
    "MYR": REF_MYR_WORDS,
    "NZD": REF_NZD_WORDS,
    "PHP": REF_PHP_WORDS,
    "SGD": REF_SGD_WORDS,
    "THB": REF_THB_WORDS,
    "ZAR": REF_ZAR_WORDS,
}


REF_CONVERSIONLINKER = {
    "en",
    "in",
    "=",
    "==",
    "?",
}
