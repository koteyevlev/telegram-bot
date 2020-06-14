from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import mapper, sessionmaker

db_string = 'mysql+pymysql://root:root@localhost/telegram_bot'
#db_string = 'postgres://postgres:root@localhost:5432/tg_bot'
db_string = 'postgres://nkdgmzsbdjxwaf:690f515b258d252b09d2a9b8332465a76da38ce95510e2e7941d646382779c3c@ec2-34-194-198-176.compute-1.amazonaws.com:5432/dck46teb299h2d
'
engine = create_engine(db_string, echo=True)

conn = engine.connect()
#print(conn.execute('\\dt'))

meta = MetaData()

class Exam:
   def __init__(self, data):
      self.exam_id = data.text
      self.author = data.from_user.username
      self.password = "root"
      self.tasks_num = 0
      self.number_of_res = 0


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

class Answers:
   def __init__(self, exam_id, username, answer, correct_answer):
      self.exam_id = exam_id
      self.username = username
      self.answer = answer
      self.correct_answer = correct_answer

class Grades:
   def __init__(self, exam_id, username, number_of_correct_answers, total_answers):
      self.exam_id = exam_id
      self.username = username
      self.number_of_correct_answers = number_of_correct_answers
      self.total_answers = total_answers
      
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

answers = Table(
   "answers", meta,
   Column('id', Integer, primary_key=True),
   Column('exam_id', String(100)),
   Column('username', String(100)),
   Column('answer', Integer),
   Column('correct_answer',  Integer)
)

grades = Table(
   "grades", meta,
   Column('id', Integer, primary_key=True),
   Column('exam_id', String(100)),
   Column('username', String(100)),
   Column('number_of_correct_answers', Integer),
   Column('total_answers', Integer)
)

mapper(Task, tasks)
mapper(Exam, meta_ex)
mapper(Answers, answers)
mapper(Grades, grades)
meta.create_all(engine)


#Session = sessionmaker(bind=engine)
#Session = Session()

#Session.add(Task(soup))
#Session.commit()
