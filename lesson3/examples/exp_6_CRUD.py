"""
Для того, чтобы свободно чувствовать себя с любой БД
необходимо овладеть операциями CRUD:

C - Create
R - Retrieve
U - Update
D - Delete

"""

from exp_7 import User, sess


# create
user_2 = User("Пётр", "Петров", "pass_Petrov")
user_3 = user_2
user_4 = user_2
sess.add(user_2)
sess.add(user_3)
sess.add(user_4)
sess.commit()
#
# # # Retrieve
result = sess.query(User).filter_by(name='Пётр')
print('rows count: ', result.count())
print('rows data: ', result.all())

# Update 1 row
print(result.first().password)
result.first().password += '1'
sess.commit()
print(result.first().password)

# Update multiple lines simultaneously var #1
for row in result.all():
    row.password += "1"
sess.commit()
# print(result.all())

# Update multiple lines simultaneously variant #2
result.update({User.password: 555})
sess.commit()

# Delete
result = sess.query(User).filter_by(name='Иван')
total = sess.query(User)

print('count before delete: ', total.count())
print('rows before delete: ', total.all())
result.delete()
sess.commit()
print('count after delete: ', total.count())
print('rows after delete: ', total.all())

"""
**************************** ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ *************************************
Более подробно о всех командах и методах можно прочитать в англоязычном
https://www.sqlalchemy.org/
или в русскоязычном описании SQAlchemy
https://lectureswww.readthedocs.io/6.www.sync/2.codding/9.databases/2.sqlalchemy/
********************************************************************************************
"""
