from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import mapper, sessionmaker

engine = create_engine('mysql+pymysql://root:root@localhost/telegram_bot', echo=True)

conn = engine.connect()
print(conn.execute('show tables;'))

meta = MetaData()


meta_ex = Table(
   'meta_exams', meta,
   Column('id', Integer, primary_key=True, unique=True),
   Column('exam_id', String(100), unique=True),
   Column('author', String(100)),
   Column('password', String(1000)),
   Column('tasks_num', Integer),
   Column("number_of_res", Integer),
   Column("result_id", Integer, unique=True)
)


class Exam:
   def __init__(self, data):
      self.exam_id = data.text
      self.author = data.from_user.username
      self.password = "root"
      self.tasks_num = 0
      self.number_of_res = 0
      self.result_id = None



class Task:
   def __init__(self, soup, exam_id=0):
      self.exam_id = exam_id
      self.question = str(soup.question[0])
      self.answerlist = str(list(soup.question.answerlist.find_all('item')))
      self.solution = str(soup.solution[0])
      self.exname = str(soup.exname[0])
      self.extype = str(soup.extype[0])
      self.exsolution = str(soup.exsolution[0])
      self.exshuffle = str(soup.exshuffle[0])


tasks = Table(
   "tasks", meta,
   Column('id', Integer, primary_key=True),
   Column('exam_id', String(100)),
   Column('question', String(1000)),
   Column('answerlist', String(1000)),
   Column('solution', String(1000)),
   Column('exname', String(1000)),
   Column('extype', String(1000)),
   Column('exsolution', String(1000)),
   Column('exshuffle', Integer)
)

mapper(Task, tasks)
mapper(Exam, meta_ex)
meta.create_all(engine)

#Session = sessionmaker(bind=engine)
#Session = Session()

#Session.add(Task(soup))
#Session.commit()
