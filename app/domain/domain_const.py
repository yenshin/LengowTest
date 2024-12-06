# INFO: only use for const data
REF_URLCONVERSION = "http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
REF_XMLNAMESPACE_URL = "http://www.ecb.int/vocabulary/2002-08-01/eurofxref"
REF_XMLNAMESPACE_PREFIX = ""
REF_XMLTARGETNODE = "Cube"

REF_XMLDATE_QUERY = f".//{REF_XMLTARGETNODE}[@time]"
REF_XMLCURRENCIES_QUERY = f".//{REF_XMLTARGETNODE}[@currency]"
# INFO: K as key
REF_XMLCURRENCY_KNAME = "currency"
REF_XMLCURRENCY_KRATE = "rate"
REF_XMLCURRENCY_KDATE = "time"
