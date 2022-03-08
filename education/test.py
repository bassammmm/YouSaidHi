
# user_1 = User(first_name="Muhammad",last_name="Bassam",email="b@gmail.com",password="$2b$12$/DuLxhoUrZh9x7C3QNSEHe6ekmFdrGsVoQB7PWY5zb19pUNRDegQq",role="TEACHER")
# teacher_1 = Teacher(first_name="Muhammad",last_name="Bassam",email="b@gmail.com",password="$2b$12$/DuLxhoUrZh9x7C3QNSEHe6ekmFdrGsVoQB7PWY5zb19pUNRDegQq")
# user_2 = User(first_name="Safi",last_name="Khan",email="s@gmail.com",password="$2b$12$/DuLxhoUrZh9x7C3QNSEHe6ekmFdrGsVoQB7PWY5zb19pUNRDegQq",role="TEACHER")
# teacher_2 = Teacher(first_name="Safi",last_name="Khan",email="s@gmail.com",password="$2b$12$/DuLxhoUrZh9x7C3QNSEHe6ekmFdrGsVoQB7PWY5zb19pUNRDegQq")
# user_3 = User(first_name="Zarar",last_name="Shah",email="z@gmail.com",password="$2b$12$/DuLxhoUrZh9x7C3QNSEHe6ekmFdrGsVoQB7PWY5zb19pUNRDegQq",role="TEACHER")
# teacher_3 = Teacher(first_name="Zarar",last_name="Shah",email="z@gmail.com",password="$2b$12$/DuLxhoUrZh9x7C3QNSEHe6ekmFdrGsVoQB7PWY5zb19pUNRDegQq")
# user_4 = User(first_name="Abdul",last_name="Sattar",email="edhi@gmail.com",password="$2b$12$/DuLxhoUrZh9x7C3QNSEHe6ekmFdrGsVoQB7PWY5zb19pUNRDegQq",role="TEACHER")
# teacher_4 = Teacher(first_name="Abdul",last_name="Sattar",email="edhi@gmail.com",password="$2b$12$/DuLxhoUrZh9x7C3QNSEHe6ekmFdrGsVoQB7PWY5zb19pUNRDegQq")
# db.session.add(user_1)
# db.session.add(user_2)
# db.session.add(user_3)
# db.session.add(user_4)
# db.session.add(teacher_1)
# db.session.add(teacher_2)
# db.session.add(teacher_3)
# db.session.add(teacher_4)
# db.session.commit()
# teacher_1.id = user_1.id
# teacher_2.id = user_2.id
# teacher_3.id = user_3.id
# db.session.add(teacher_1)
# db.session.add(teacher_2)
# db.session.add(teacher_3)
# db.session.commit()
# course_1 = Course(course_name="Computer",course_code="C001")
# course_2 = Course(course_name="Physics",course_code="C002")
# course_3 = Course(course_name="Psychology",course_code="C003")
# course_4 = Course(course_name="Astronomy",course_code="C004")
# course_5 = Course(course_name="Latin",course_code="C005")
# db.session.add(course_1)
# db.session.add(course_2)
# db.session.add(course_3)
# db.session.add(course_4)
# db.session.add(course_5)
# db.session.commit()
# user_5 = User(first_name="Abdul",last_name="Wadood",email="a@gmail.com",password="$2b$12$/DuLxhoUrZh9x7C3QNSEHe6ekmFdrGsVoQB7PWY5zb19pUNRDegQq",role="STUDENT")
# student = Student(first_name="Abdul",last_name="Wadood",email="a@gmail.com",password="$2b$12$/DuLxhoUrZh9x7C3QNSEHe6ekmFdrGsVoQB7PWY5zb19pUNRDegQq",package="WEEKLY",country="China",language="Cantonese")
# user_6 = User(first_name="Abdul",last_name="Moiz",email="m@gmail.com",password="$2b$12$/DuLxhoUrZh9x7C3QNSEHe6ekmFdrGsVoQB7PWY5zb19pUNRDegQq",role="STUDENT")
# student_2 = Student(first_name="Abdul",last_name="Moiz",email="m@gmail.com",password="$2b$12$/DuLxhoUrZh9x7C3QNSEHe6ekmFdrGsVoQB7PWY5zb19pUNRDegQq",package="MONTHLY",country="China",language="Cantonese")
# user_7 = User(first_name="Usman",last_name="Fawad",email="u@gmail.com",password="$2b$12$/DuLxhoUrZh9x7C3QNSEHe6ekmFdrGsVoQB7PWY5zb19pUNRDegQq",role="STUDENT")
# student_3 = Student(first_name="Usman",last_name="Fawad",email="u@gmail.com",password="$2b$12$/DuLxhoUrZh9x7C3QNSEHe6ekmFdrGsVoQB7PWY5zb19pUNRDegQq",package="MONTHLY",country="China",language="Cantonese")
# db.session.add(user_4)
# db.session.add(user_5)
# db.session.add(user_6)
# db.session.add(student)
# db.session.add(student_2)
# db.session.add(student_3)
# db.session.commit()
# teacher_admin = User(first_name="ADMIN",last_name="FATIMA",email="yousaidhiacc@gmail.com",password="$2b$12$m1StH.7vsPELR0nnfa6ZBuh2HFXYvE9k7eSaIQHePUxNEytJUwVie",role="TEACHER_ADMIN")
# db.session.add(teacher_admin)
# db.session.commit()


# teacher = Teacher.query.get(2)
# date = Date(id=1,date="2020-05-19",teacher=teacher)
# slot = Slot(id=1,date=date,slot="06:00-06:30",teacher_time_zone="Asia/Karachi")
# db.session.add(date)
# db.session.add(slot)
# db.session.commit()
# date2 = Date(id=2,date="2020-05-20",teacher=teacher)
# slot2 = Slot(id=2,date=date2,slot="08:00-08:30",teacher_time_zone="Asia/Karachi")
# db.session.add(date2)
# db.session.add(slot2)
# db.session.commit()

# student = Student.query.get(6)
# lesson = Lesson.query.get(1)
# booking_1 = Booking(id=1,date=date,slot=slot,teacher=teacher,student=student,lesson=lesson)
# booking_2 = Booking(id=2,date=date2,slot=slot2,teacher=teacher,student=student,lesson=lesson)
# db.session.add(booking_1)
# db.session.add(booking_2)
# db.session.commit()

# teacher_1 = Teacher.query.get(2)
# teacher_2 = Teacher.query.get(3)
# teacher_3 = Teacher.query.get(4)
# teacher_4 = Teacher.query.get(5)
# date_1 = Date(date="2020-05-21",teacher=teacher_1)
# date_2 = Date(date="2020-05-21",teacher=teacher_2)
# date_3 = Date(date="2020-05-21",teacher=teacher_3)
# date_4 = Date(date="2020-05-21",teacher=teacher_4)
# slot_1 = Slot(date=date_1,slot='02:00-02:30',teacher_time_zone='Asia/Karachi')
# slot_2 = Slot(date=date_1,slot='02:30-03:00',teacher_time_zone='Asia/Karachi')
# slot_3 = Slot(date=date_1,slot='03:00-03:30',teacher_time_zone='Asia/Karachi')
# slot_4 = Slot(date=date_2,slot='02:00-02:30',teacher_time_zone='Asia/Karachi')
# slot_5 = Slot(date=date_2,slot='02:30-03:00',teacher_time_zone='Asia/Karachi')
# slot_6 = Slot(date=date_2,slot='03:00-03:30',teacher_time_zone='Asia/Karachi')
# slot_7 = Slot(date=date_3,slot='03:00-03:30',teacher_time_zone='Asia/Karachi')
# db.session.add(date_1)
# db.session.add(date_2)
# db.session.add(date_3)
# db.session.add(date_4)
# db.session.add(slot_1)
# db.session.add(slot_2)
# db.session.add(slot_3)
# db.session.add(slot_4)
# db.session.add(slot_5)
# db.session.add(slot_6)
# db.session.add(slot_7)
# db.session.commit()






# from education import bcrypt
# print(bcrypt.generate_password_hash('123').decode('utf-8'))


#
# import datetime
# import pytz
# date = datetime.datetime.strptime('2020-05-16 02:00','%Y-%m-%d %H:%M')
# date2 = datetime.datetime.strptime('2020-05-16 08:00','%Y-%m-%d %H:%M')
# nw_yrk_date = date.astimezone(pytz.timezone('America/New_York'))
# nw_yrk_date2 = date2.astimezone(pytz.timezone('America/New_York'))
#
# print(nw_yrk_date2-nw_yrk_date)
# print()


#
# import os
# from shutil import copy2
# source = "C://test//default.jpg"
# dest = "C://test2"
#
# copy2(source,dest)



#
# test = {1:'vassam',2:'asdasd'}
# print(test.1)



# date = Date(date="2019-10-11",teacher_id=2)
# slot = Slot(slot="18:00-18:30",teacher_time_zone="Asia/Karachi")
# slot.date = date
# slot.booked = True
# booking = Booking(student_id=6,teacher_id=2,lesson_id=1)
# booking.date = date
# booking.slot = slot
# booking.lecture_complete = True
# booking.teacher_present = True
# booking.student_present = True
# db.session.add(date)
# db.session.add(slot)
# db.session.add(booking)
# db.session.commit()

# from validate_email import validate_email
# is_valid = validate_email(email_address='bassam@protonmail.com', check_regex=True, check_mx=True)
# print(is_valid)

# import datetime
# print(str(datetime.datetime.today().date()))
#
# first_population = 1000000
# first_infect     = 10
# second_population= 100000
# second_infect = (second_population * first_infect)/first_population
# print(second_infect)

# from education import bcrypt
#
# print(bcrypt.generate_password_hash('fatimazuberi123'))



# print(len("Lesson No. 1 The Letter 'Aa'"))



