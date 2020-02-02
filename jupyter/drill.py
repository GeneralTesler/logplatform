from IPython.core.magic import register_line_magic

# expose drill client
from pydrill.client import PyDrill
drill=PyDrill(host="drill",port=8047)

# adjust pandas settings
import pandas
pandas.set_option('display.max_colwidth', -1)
pandas.set_option('display.max_rows', None)

import datetime

from pandas.io.json import json_normalize
import json

# drill query wrapper
def drill_query(query):
    res = drill.query(query)
    df = res.to_dataframe().dropna()
    df['@timestamp'] = pandas.to_datetime(df['@timestamp'], utc=True)
    return df

# time based query - returns results from last x minutes
def drill_tquery(query_s, minutes):
    df = query(query_s)
    return df[df['@timestamp']>=datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)-datetime.timedelta(minutes=minutes)]

# Magic functions
@register_line_magic
def query(line):
    return drill_query(line)

@register_line_magic
def tquery(line):
    args = line.split(" ")
    return drill_tquery(" ".join(args[0:len(args)-1]), int(args[-1]))

def winlog_normalize(df):
    return json_normalize(df['winlog'].apply(lambda x: json.loads(x)).tolist())

@register_line_magic
def wquery(line):
    df = query(line)
    return winlog_normalize(df)

@register_line_magic
def twquery(line):
    df = tquery(line)
    return winlog_normalize(df)
