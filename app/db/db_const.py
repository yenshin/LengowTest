# INFO: DB Parameter
# I use sqlite because it's job interview project and a real db seems unecessary
DBURLPREFIX = "postgresql+psycopg2:///"

DB_CONVERSION_REF = "http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
DB_CONNECT_ARGS = {"check_same_thread": False}
DB_VERSION_TABLENAME = "version"
