from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,SelectField,FieldList,FormField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from education.models import *


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8,max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    country = SelectField("Country",choices=[('pakistan','Pakistan'),('china','China'),('taiwan','Taiwan'),('hong kong','Hong Kong')])
    language = SelectField("Language",choices=[('cantonese','Cantonese'),('english','English'),('arabic','Arabic'),('mandarin','Mandarin')])

    submit = SubmitField('Complete Registration')



    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please choose a different one.')

class TeacherRegistration(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    teacher_image = FileField('Teacher Image', validators=[FileAllowed(['jpeg', 'jpg', 'png'])])
    zoom_link = StringField('Zoom Link', validators=[DataRequired()])

    submit = SubmitField('Complete Registration')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please choose a different one.')

class LoginForm(FlaskForm):
    email    = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    time_zone = StringField('timezone',validators=[DataRequired()])
    submit = SubmitField('Login')

class TestForm(FlaskForm):
    name=StringField('FirstName')
    last=StringField('LastName')
    submit = SubmitField('Login')

class AddCourseForm(FlaskForm):
    course_name = StringField('Course Name', validators=[DataRequired(), Length(min=2, max=100)])
    course_code = StringField('Course Code', validators=[DataRequired(), Length(min=2, max=30)])
    course_description = TextAreaField('Course Description', validators=[DataRequired(), Length(min=2, max=500)])
    course_image = FileField('Course Main Image',validators=[FileAllowed(['jpeg','jpg','png'])])
    submit = SubmitField('Add Course')
    def validate_course_code(self,course_code):
        course = Course.query.filter_by(course_code=course_code.data).first()
        if course:
            raise ValidationError('Course code already registered! Select A different Code!')
    def validate_course_name(self,course_name):
        course = Course.query.filter_by(course_name=course_name.data).first()
        if course:
            raise ValidationError('Course name already registered! Select A different Code!')

class AddLessonDocument(FlaskForm):
    class Meta:
        csrf = False
    lesson_document = StringField('Lesson Document Link',validators=[DataRequired()])


class AddLessonForm(FlaskForm):
    course_id = SelectField("Course",coerce=int)
    lesson_name = StringField('Lesson Name', validators=[DataRequired(), Length(min=2, max=100)])
    lesson_code = StringField('Lesson Code', validators=[DataRequired(), Length(min=2, max=30)])
    lesson_image = FileField('Lesson Main Image',validators=[DataRequired(),FileAllowed(['jpeg','jpg','png'])])
    lesson_homework = StringField('Lesson Homework Link')
    lesson_documents = FieldList(FormField(AddLessonDocument), min_entries=1)
    submit = SubmitField('Add Lesson')

class AddVideoForm(FlaskForm):
    video_name = StringField('Video Name',validators=[DataRequired(),Length(min=5,max=200)])
    video_link = StringField('Video Link',validators=[DataRequired(),Length(min=10,max=500)])
    video_image = FileField('Video Thumbnail',validators=[FileAllowed(['jpeg','jpg','png'])])
    submit = SubmitField('Add Video')


class EditStudentProfile(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpeg', 'jpg', 'png'])])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')

    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Update Account')
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already registered. Please choose a different one.')

class EditTeacherProfile(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpeg', 'jpg', 'png'])])
    submit = SubmitField('Update Picture')