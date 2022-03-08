from education import db,login_manager,app
from flask_login import UserMixin
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer #for tokens of id and pass

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    user_time_zone = db.Column(db.String(20),nullable=True)

    def __repr__(self):
        return "({},{},{},{},{})".format(str(self.id), self.fname, self.lname, self.email, self.role)

    def return_dict(self):
        user_dict = {
            'id' : self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'role': self.role,
            'user_time_zone' : self.user_time_zone
        }


        return user_dict

    @classmethod
    def return_all_obj(cls):
        users_dict = {}
        for user in User.query.all():
            users_dict[user.id] = user.return_dict()
        return users_dict



class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    education = db.relationship('Education', backref='teacher', lazy=True)
    age = db.Column(db.Integer,nullable=True)
    one_line_description = db.Column(db.String(100),nullable=True)
    about = db.Column(db.String(500),nullable=True)
    ratings = db.Column(db.String(2),nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    dates = db.relationship('Date', backref='teacher', lazy=True)
    bookings = db.relationship('Booking', backref='teacher', lazy=True)
    completed_lessons = db.Column(db.Integer,nullable=True)
    zoom_link = db.Column(db.String(100), nullable=True)
    account_title = db.Column(db.String(100),nullable=True)
    account_number = db.Column(db.String(100),nullable=True)
    account_bank = db.Column(db.String(100),nullable=True)
    mobile_number = db.Column(db.String(100),nullable=True)
    salaries = db.relationship('TeacherSalary',backref='teacher',lazy=True)

    def return_dict(self):
        teacher_dict = {
            'id' : self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'education': [education.return_dict() for education in self.education],
            'age': '' if self.age==None else self.age,
            'one_line_description':'' if self.one_line_description==None else self.one_line_description,
            'about': '' if self.about==None else self.about,
            'rating': '0' if self.ratings==None else self.ratings,
            'image_file': self.image_file,
            'dates': [date.return_dict() for date in self.dates],
            'bookings': [booking.return_dict() for booking in self.bookings],
            'completed_lessons': '0' if self.completed_lessons==None else self.completed_lessons,
            'zoom_link': '' if self.zoom_link==None else self.zoom_link,
            'account_title': 'None' if self.account_title==None else self.account_title,
            'account_number': 'None' if self.account_number==None else self.account_number,
            'account_bank': 'None' if self.account_bank==None else self.account_bank,
            'mobile_number': 'None' if self.mobile_number==None else self.mobile_number,
            'salaries':[salary.return_dict() for salary in self.salaries]
        }

        return teacher_dict

    @classmethod
    def return_all_obj(cls):
        teachers_dict = {}
        for teacher in Teacher.query.all():
            teachers_dict[teacher.id] = teacher.return_dict()
        return teachers_dict

    def __repr__(self):
        return "({},{})".format(str(self.id), self.first_name+" "+self.last_name)

class TeacherSalary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    year = db.Column(db.Integer,nullable=False)
    month = db.Column(db.Integer,nullable=False)
    salary = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return "TSAL({},{},{},{},{})".format(str(self.id),str(self.teacher_id),str(self.year),str(self.month),str(self.salary))

    def return_dict(self):
        teacher_salary = {
            'id':self.id,
            'teacher_id':self.teacher_id,
            'year':self.year,
            'month':self.month,
            'salary':self.salary
        }
        return teacher_salary

    @classmethod
    def return_all_obj(cls):
        teacher_salary_dict = {}
        for salaries in TeacherSalary.query.all():
            teacher_salary_dict[salaries.id] = salaries.return_dict()
        return teacher_salary_dict

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    education = db.Column(db.String(20), nullable=False)
    education_institution = db.Column(db.String(20), nullable=False)
    def __repr__(self):
        return "({},{},{},{})".format(str(self.id),Teacher.query.get(self.teacher_id).first_name,self.education,self.education_institution)
    def return_dict(self):
        education_dict = {
            'id':self.id,
            'teacher_id': self.teacher_id,
            'education': self.education,
            'education_institution': self.education_institution
        }

        return education_dict

    @classmethod
    def return_all_obj(cls):
        educations_dict = {}
        for education in Education.query.all():
            educations_dict[education.id] = education.return_dict()
        return educations_dict



class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), unique=True, nullable=False)
    course_code = db.Column(db.String(30), unique=True, nullable=False)
    course_image = db.Column(db.String(100), nullable=False, default='default.jpg')
    course_description = db.Column(db.String(500), unique=True, nullable=True)
    lessons = db.relationship('Lesson', backref='course', lazy=True)
    def __repr__(self):
        return "({},{})".format(str(self.id),self.course_name)
    def return_dict(self):
        course_dict = {
            'id': self.id,
            'course_name': self.course_name,
            'course_code': self.course_code,
            'course_image': self.course_image,
            'course_description': '' if self.course_description==None else self.course_description,
            'lessons': [lesson.return_dict() for lesson in self.lessons]
        }
        return course_dict

    @classmethod
    def return_all_obj(cls):
        courses_dict = {}
        for course in Course.query.all():
            courses_dict[course.id] = course.return_dict()
        return courses_dict

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson_name = db.Column(db.String(100), unique=True, nullable=False)
    lesson_code = db.Column(db.String(30), unique=True, nullable=False)
    lesson_image = db.Column(db.String(100), nullable=False, default='default.jpg')
    lesson_homework = db.Column(db.String(100),nullable=True,default='homework.ppt')
    lesson_documents = db.relationship('LessonDocument', backref='lesson', lazy=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    bookings = db.relationship('Booking', backref='lesson', lazy=True)
    def __repr__(self):
        return "({},{})".format(str(self.id),self.lesson_name)

    def return_dict(self):
        lesson_dict = {
            'id':self.id,
            'lesson_name': self.lesson_name,
            'lesson_code': self.lesson_code,
            'lesson_image': self.lesson_image,
            'lesson_homework':self.lesson_homework,
            'lesson_documents': [lesson_doc.return_dict() for lesson_doc in self.lesson_documents],
            'course_id': self.course_id,
            'bookings': [booking.return_dict() for booking in self.bookings]
        }
        return lesson_dict

    @classmethod
    def return_all_obj(cls):
        lessons_dict = {}
        for lesson in Lesson.query.all():
            lessons_dict[lesson.id] = lesson.return_dict()
        return lessons_dict

class LessonDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document = db.Column(db.String(100), nullable=False, default='default.ppt')
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)


    def __repr__(self):
        return "({},{})".format(str(self.id), self.document)

    def return_dict(self):
        lesson_doc_dict = {
            'id': self.id,
            'document': self.document,
            'lesson_id': self.lesson_id
        }
        return lesson_doc_dict

    @classmethod
    def return_all_obj(cls):
        lesson_docs_dict = {}
        for lesson_doc in LessonDocument.query.all():
            lesson_docs_dict[lesson_doc.id] = lesson_doc.return_dict()
        return lesson_docs_dict

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    package = db.Column(db.String(20), nullable=False)
    number_of_lessons_remaining = db.Column(db.Integer,nullable=True)
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg')
    bookings = db.relationship('Booking', backref='student', lazy=True)
    country = db.Column(db.String(50), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    complains = db.relationship('StudentComplain',backref='student',lazy=True)
    payments = db.relationship('PaymentRecord',backref='student',lazy=True)

    def return_dict(self):
        student_dict = {
            'id': self.id,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'email':self.email,
            'password':self.password,
            'package':self.package,
            'number_of_lessons_remaining':self.number_of_lessons_remaining,
            'image_file':self.image_file,
            'bookings':[booking.return_dict() for booking in self.bookings],
            'country':self.country,
            'language':self.language,
            'complains':[complain.return_dict() for complain in self.complains],
            'payments':[payment.return_dict() for payment in self.payments]
        }
        return student_dict

    @classmethod
    def return_all_obj(cls):
        students_dict = {}
        for student in Student.query.all():
            students_dict[student.id] = student.return_dict()
        return students_dict

    def __repr__(self):
        return "S({},{})".format(str(self.id),self.first_name+" "+self.last_name)
        # return self.__dict__
class StudentComplain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=True)
    complain = db.Column(db.String(2000), nullable=False)
    resolved = db.Column(db.Boolean, default=False)
    student_id = db.Column(db.Integer,db.ForeignKey('student.id'), nullable=False)

    def __repr__(self):
        return "SCMP({},{},{})".format(str(self.id),str(self.booking_id),self.resolved)
    def return_dict(self):
        student_complain_dict = {
            'id' : self.id,
            'booking_id': 'none' if self.booking_id==None else self.booking_id,
            'complain': self.complain,
            'resolved': 'false' if self.resolved==False else 'true',
            'student_id': self.student_id
        }
        return student_complain_dict

    @classmethod
    def return_all_obj(cls):
        studentcomplain = {}
        for complain in StudentComplain.query.all():
            studentcomplain[complain.id] = complain.return_dict()
        return studentcomplain


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    date_id = db.Column(db.Integer, db.ForeignKey('date.id'), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('slot.id'), nullable=False)
    lecture_complete = db.Column(db.Boolean,default=False)
    student_present = db.Column(db.Boolean,default=False)
    teacher_present = db.Column(db.Boolean,default=False)
    teacher_feedback = db.Column(db.String(1000),nullable=True)

    def __repr__(self):
        return "B({},{},{},{},{},{})".format(str(self.id),Student.query.get(self.student_id).first_name,Teacher.query.get(self.teacher_id).first_name,Lesson.query.get(self.lesson_id).lesson_name,Date.query.get(self.date_id).date,Slot.query.get(self.slot_id).slot)

    def return_dict(self):
        booking_dict = {
            'id': self.id,
            'student_id': self.student_id,
            'teacher_id': self.teacher_id,
            'lesson_id': self.lesson_id,
            'date_id': self.date_id,
            'slot_id': self.slot_id,
            'lecture_complete': 'false' if self.lecture_complete==False else 'true',
            'student_present': 'false' if self.student_present==False else 'true',
            'teacher_present': 'false' if self.teacher_present==False else 'true',
            'teacher_feedback':'None' if self.teacher_feedback==None else self.teacher_feedback
        }

        return booking_dict

    @classmethod
    def return_all_obj(cls):
        bookings_dict = {}
        for booking in Booking.query.all():
            bookings_dict[booking.id] = booking.return_dict()
        return bookings_dict

class Date(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20),nullable=False)
    slots = db.relationship('Slot', backref='date', lazy=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    bookings = db.relationship('Booking', backref='date', lazy=True)

    def __repr__(self):
        return "D({},{},{})".format(str(self.id),self.date,Teacher.query.get(self.teacher_id).first_name)

    def return_dict(self):
        date_dict = {
            'id':self.id,
            'date':self.date,
            'slots':[slot.return_dict() for slot in self.slots],
            'teacher_id':self.teacher_id,
            'bookings':[bookings.return_dict() for bookings in self.bookings]
        }

        return date_dict

    @classmethod
    def return_all_obj(cls):
        dates_dict = {}
        for date in Date.query.all():
            dates_dict[date.id] = date.return_dict()
        return dates_dict


class Slot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slot = db.Column(db.String(20),nullable=False)
    date_id = db.Column(db.Integer, db.ForeignKey('date.id'), nullable=False)
    teacher_time_zone = db.Column(db.String(20),nullable=False)
    booked = db.Column(db.Boolean,default=False)
    bookings = db.relationship('Booking', backref='slot', lazy=True)



    def __repr__(self):
        return "D({},{},{})".format(str(self.id),Date.query.get(self.date_id).date,Teacher.query.get(Date.query.get(self.date_id).teacher_id).first_name,self.booked)

    def return_dict(self):
        slot_dict = {
            'id':self.id,
            'slot':self.slot,
            'date_id':self.date_id,
            'teacher_time_zone': self.teacher_time_zone,
            'booked' : 'false' if self.booked==False else 'true',
            'bookings': [booking.return_dict() for booking in self.bookings]

        }
        return slot_dict

    @classmethod
    def return_all_obj(cls):
        slots_dict = {}
        for slot in Slot.query.all():
            slots_dict[slot.id] = slot.return_dict()
        return slots_dict

class PaymentRecord(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    number_of_lessons = db.Column(db.Integer,nullable=False)
    price = db.Column(db.Integer,nullable=False)
    date = db.Column(db.String(20),nullable=False)



    def __repr__(self):
        return "PR({},{},{},{},{})".format(str(self.id),str(self.student_id),str(self.number_of_lessons),str(self.price),str(self.date))

    def return_dict(self):
        paymentrecord_dict = {
            'id' : self.id,
            'student_id' : self.student_id,
            'number_of_lessons' : self.number_of_lessons,
            'price' : self.price,
            'date' : self.date
        }

        return paymentrecord_dict
    @classmethod
    def return_all_obj(cls):
        payments_dict = {}
        for payment in PaymentRecord.query.all():
            payments_dict[payment.id] = payment.return_dict()
        return payments_dict

class Videos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(500),nullable=False)
    thumbnail = db.Column(db.String(20), nullable=False, default='default.jpg')