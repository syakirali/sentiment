import re
import requests
import sqlite3
import pandas as pd
import IPython
from pathlib import Path
from collections import Counter
from IPython.display import HTML, display

ROOT_PATH = Path(__file__).resolve().parent
DEFAULT_QUERY = "SELECT * FROM tweets"

def get_sqlite_data(
    path,
    query=DEFAULT_QUERY,
    limit=None):
  # Create your connection.
  cnx = sqlite3.connect(path)
  if limit is not None:
    query = f'{query} limit {int(limit)}'

  data = pd.read_sql_query(query, cnx)
  cnx.close()
  return data

def save_to_sqlite(f_path, data):
  conn = sqlite3.connect(f_path)
  c = conn.cursor()

  data = [tuple(d) for d in data]

  # Create table
  c.execute('''CREATE TABLE IF NOT EXISTS tweets (
      tweet_id INTEGER,
      text TEXT)''')
  c.executemany("INSERT INTO tweets VALUES (?,?)",data)
  conn.commit()
  conn.close()

def get_emoticon_list():
  emot = [":-)", ":)", ":D", ":o)", ":]", ":3", ":c)", ":>", "=]", "8)"]
  return emot

def load_from_csv(path):
  pd.set_option('display.float_format', lambda x: '%.3f' % x)
  data = pd.read_csv(path)
  return data

def bytearray_to_long(b):
  int.from_bytes(b, byteorder='big', signed=False)

def download_file(url, save_path):
  import requests
  r = requests.get(url, allow_redirects=True)
  open(save_path, 'wb').write(r.content)

def sqlite_to_csv(path, db_name, output):
  import sqlite3
  import csv
  conn = sqlite3.connect(path)
  cursor = conn.cursor()
  cursor.execute(f'select * from {db_name}')
  with open(output, "w") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=",")
    csv_writer.writerow([i[0] for i in cursor.description])
    csv_writer.writerows(cursor)

def get_alarm():
  r = requests.get('https://assets.mixkit.co/sfx/download/mixkit-vintage-warning-alarm-990.wav', allow_redirects=True)
  return r.content
ALARM = get_alarm()

def play_alarm():
  global ALARM
  return IPython.display.Audio(ALARM, autoplay=True)

def term_freq(terms):
  tf = Counter(terms)
  return tf

def progress(value, max=100):
  return HTML("""
    <progress
      value='{value}'
      max='{max}',
      style='width: 100%'
    >
      {value:.1f}
    </progress>
    <div style="text-align: center;">{value:.1f}%</div>
  """.format(value=value, max=max))

def strikeThrough(word):
  return """
    <span style="text-decoration: line-through;">{word}</span>
  """.format(word=word)

def strikeThroughText(word, text):
  regex = re.compile(f'\b{word}\b')
  res = re.sub(regex, strikeThrough(word), text)
  display(HTML(
    "<p>{res}</p>".format(res=res)
  ))

def showChanges(tokens, only=None):
  res = []
  for token in tokens:
      if (
        token.cleaned is not None
        and token.cleaned != token.term
        and (only is None or token in only)):
        res.append(
          strikeThrough(token.term))
        res.append(token.cleaned)
      else:
        res.append(token.term)
  display(HTML(
    "<p>{res}</p>".format(res=" ".join(res))
  ))
