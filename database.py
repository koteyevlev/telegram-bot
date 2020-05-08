from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import mapper, sessionmaker

engine = create_engine('mysql+pymysql://root:root@localhost/telegram_bot', echo=True)

conn = engine.connect()
print(conn.execute('show tables;'))

meta = MetaData()

tasks = Table(
   'exams', meta,
   Column('id', Integer, primary_key=True),
   Column('question', String(1000)),
   Column('answerlist', String(1000)),
   Column('solution', String(1000)),
   Column('solutionlist', String(1000)),
   Column('exname', String(1000)),
   Column('extype', String(1000)),
   Column('exsolution', String(1000)),
   Column('exshuffle', String(1000)),
)


class Task:
   def __init__(self, soup):
      self.question = "s" #soup.question
      self.answerlist = "r" #soup.question.answerlist.find_all('item')
      self.solution = "e" #soup.solution
      self.solutionlist = "e"
      self.exname = "e" #soup.exname
      self.extype = "e" #soup.extype
      self.exsolution = "e" #soup.exsolution
      self.exshuffle = "e" #soup.exshuffle

mapper(Task, tasks)
meta.create_all(engine)

Session = sessionmaker(bind=engine)
Session = Session()

soup = dict()

Session.add(Task(soup))
Session.commit()
