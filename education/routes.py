from flask import render_template,url_for,flash,redirect,request,abort,jsonify  #request is imported for query parameters in routes
from education import app,db,bcrypt,admin,mail
from education.models import *
from education.forms import *
from flask_login import login_user,current_user,logout_user,login_required
from flask_mail import Message
from functools import wraps
import os
import random
import secrets
from PIL import Image
import datetime
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView,expose,AdminIndexView
import pytz
from operator import itemgetter
from shutil import copy2
import copy
import json
import calendar as cal
from werkzeug.datastructures import ImmutableMultiDict
import ast
from validate_email import validate_email
#-----------------------------------------------------------------------------------------------------------------------#
###########################                       MISC FUNCS                       ###################################
#-----------------------------------------------------------------------------------------------------------------------#

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if ((current_user.role != role) and (role != "ANY")):


                return redirect(url_for('unauthorized'))
            return fn(*args, **kwargs)


        return decorated_view


    return wrapper

@app.route('/test',methods=['GET','POST'])
def test():
    return render_template('test.html')

@app.route('/unauthorized',methods=['GET','POST'])
def unauthorized():
    if current_user.role == 'ADMIN':
        page = 'admin.index'
    elif current_user.role == 'STUDENT':
        page = 'student_panel'
    elif current_user.role == 'TEACHER':
        page = 'teacher_panel'
    elif current_user.role == 'TEACHER_ADMIN':
        page = 'teacher_admin_panel'
    return render_template('unauthorized.html',page=page)




def save_picture(form_picture,path):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename) #form_picture is form data, filename will be the name of that file
    picture_fn = random_hex+f_ext
    picture_path = os.path.join(path,picture_fn) #this will get the path of the root directory of the package
    output_size = (800,800)
    i = Image.open(form_picture)
    i.thumbnail(output_size)



    i.save(picture_path) #this will save the picture in the path

    return picture_fn
def save_document(form_document,path):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_document.filename) #form_document is form data, filename will be the name of that file
    document_fn = random_hex+f_ext
    document_path = os.path.join(path,document_fn) #this will get the path of the root directory of the package
    form_document.save(document_path) #this will save the document in the path

    return document_fn


#-----------------------------------------------------------------------------------------------------------------------#
###########################                       HOME PAGE                       ###################################
#-----------------------------------------------------------------------------------------------------------------------#
@app.route('/')
@app.route('/home')
def home():
    teachers = []
    random.shuffle(teachers)
    teachers.append(Teacher.query.get(2))
    teachers.append(Teacher.query.get(4))
    teachers.append(Teacher.query.get(5))
    teachers.append(Teacher.query.get(6))
    courses = Course.query.all()
    random.shuffle(courses)
    course_1 = Course.query.get(1)
    course_2 = Course.query.get(2)
    course_3 = Course.query.get(3)
    course_4 = Course.query.get(4)
    courses = [course_1,course_2,course_3,course_4]

    return render_template('home.html',teachers=teachers,courses=courses)



@app.route('/courses')
def courses():
    courses = Course.query.all()
    teachers = Teacher.query.all()
    lessons = Lesson.query.all()

    all_courses = Course.return_all_obj()
    all_teachers = Teacher.return_all_obj()
    all_lessons = Lesson.return_all_obj()




    return render_template('courses.html',courses = courses,teachers=teachers,lessons=lessons,all_courses=all_courses,all_teachers=all_teachers,all_lessons=all_lessons)

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/contact_message',methods=['GET','POST'])
def contact_message():

    data = dict(request.form)
    email,subject,message = data['email'],data['subject'],data['message']
    msg = Message(subject,sender=email,recipients=['yousaidhiacc@gmail.com'])
    msg.body = "Email : "+email+"\nQuery : "+message
    mail.send(msg)

    return jsonify({'done':True})

@app.route('/teachers')
def teachers():
    teachers = [Teacher.query.get(2),Teacher.query.get(3),Teacher.query.get(4),Teacher.query.get(5),Teacher.query.get(6)]
    all_teachers = Teacher.return_all_obj()
    return render_template('teachers.html',teachers=teachers,all_teachers=all_teachers)


#-----------------------------------------------------------------------------------------------------------------------#
###########################                       REGISTER                            ###################################
#-----------------------------------------------------------------------------------------------------------------------#

@app.route("/register",methods=['GET','POST'])
def register():
    # if we click on login after login then it will not work
    if current_user.is_authenticated:
        if current_user.role == 'ADMIN':
            return redirect(url_for('admin.index'))
        elif current_user.role == 'STUDENT':


            return redirect(url_for('teacher_panel'))
        elif current_user.role == 'TEACHER':
            return redirect(url_for('student_panel'))
        elif current_user.role == 'TEACHER_ADMIN':
            return redirect(url_for('teacher_admin_panel'))

    form = RegistrationForm()
    emails = [user.email for user in User.query.all()]
    form.country.choices = [("afghanistan","Afghanistan"),("åland islands","Åland Islands"),("albania","Albania"),("algeria","Algeria"),("american samoa","American Samoa"),("andorra","Andorra"),("angola","Angola"),("anguilla","Anguilla"),("antarctica","Antarctica"),("antigua and barbuda","Antigua and Barbuda"),("argentina","Argentina"),("armenia","Armenia"),("aruba","Aruba"),("australia","Australia"),("austria","Austria"),("azerbaijan","Azerbaijan"),("bahamas","Bahamas"),("bahrain","Bahrain"),("bangladesh","Bangladesh"),("barbados","Barbados"),("belarus","Belarus"),("belgium","Belgium"),("belize","Belize"),("benin","Benin"),("bermuda","Bermuda"),("bhutan","Bhutan"),("bolivia","Bolivia"),("bosnia and herzegovina","Bosnia and Herzegovina"),("botswana","Botswana"),("bouvet island","Bouvet Island"),("brazil","Brazil"),("british indian ocean territory","British Indian Ocean Territory"),("brunei darussalam","Brunei Darussalam"),("bulgaria","Bulgaria"),("burkina faso","Burkina Faso"),("burundi","Burundi"),("cambodia","Cambodia"),("cameroon","Cameroon"),("canada","Canada"),("cape verde","Cape Verde"),("cayman islands","Cayman Islands"),("central african republic","Central African Republic"),("chad","Chad"),("chile","Chile"),("china","China"),("christmas island","Christmas Island"),("cocos (keeling) islands","Cocos (Keeling) Islands"),("colombia","Colombia"),("comoros","Comoros"),("congo","Congo"),("congo, the democratic republic of the","Congo, The Democratic Republic of The"),("cook islands","Cook Islands"),("costa rica","Costa Rica"),("cote d'ivoire","Cote D'ivoire"),("croatia","Croatia"),("cuba","Cuba"),("cyprus","Cyprus"),("czech republic","Czech Republic"),("denmark","Denmark"),("djibouti","Djibouti"),("dominica","Dominica"),("dominican republic","Dominican Republic"),("ecuador","Ecuador"),("egypt","Egypt"),("el salvador","El Salvador"),("equatorial guinea","Equatorial Guinea"),("eritrea","Eritrea"),("estonia","Estonia"),("ethiopia","Ethiopia"),("falkland islands (malvinas)","Falkland Islands (Malvinas)"),("faroe islands","Faroe Islands"),("fiji","Fiji"),("finland","Finland"),("france","France"),("french guiana","French Guiana"),("french polynesia","French Polynesia"),("french southern territories","French Southern Territories"),("gabon","Gabon"),("gambia","Gambia"),("georgia","Georgia"),("germany","Germany"),("ghana","Ghana"),("gibraltar","Gibraltar"),("greece","Greece"),("greenland","Greenland"),("grenada","Grenada"),("guadeloupe","Guadeloupe"),("guam","Guam"),("guatemala","Guatemala"),("guernsey","Guernsey"),("guinea","Guinea"),("guinea-bissau","Guinea-bissau"),("guyana","Guyana"),("haiti","Haiti"),("heard island and mcdonald islands","Heard Island and Mcdonald Islands"),("holy see (vatican city state)","Holy See (Vatican City State)"),("honduras","Honduras"),("hong kong","Hong Kong"),("hungary","Hungary"),("iceland","Iceland"),("india","India"),("indonesia","Indonesia"),("iran, islamic republic of","Iran, Islamic Republic of"),("iraq","Iraq"),("ireland","Ireland"),("isle of man","Isle of Man"),("israel","Israel"),("italy","Italy"),("jamaica","Jamaica"),("japan","Japan"),("jersey","Jersey"),("jordan","Jordan"),("kazakhstan","Kazakhstan"),("kenya","Kenya"),("kiribati","Kiribati"),("korea, democratic people's republic of","Korea, Democratic People's Republic of"),("korea, republic of","Korea, Republic of"),("kuwait","Kuwait"),("kyrgyzstan","Kyrgyzstan"),("lao people's democratic republic","Lao People's Democratic Republic"),("latvia","Latvia"),("lebanon","Lebanon"),("lesotho","Lesotho"),("liberia","Liberia"),("libyan arab jamahiriya","Libyan Arab Jamahiriya"),("liechtenstein","Liechtenstein"),("lithuania","Lithuania"),("luxembourg","Luxembourg"),("macao","Macao"),("macedonia, the former yugoslav republic of","Macedonia, The Former Yugoslav Republic of"),("madagascar","Madagascar"),("malawi","Malawi"),("malaysia","Malaysia"),("maldives","Maldives"),("mali","Mali"),("malta","Malta"),("marshall islands","Marshall Islands"),("martinique","Martinique"),("mauritania","Mauritania"),("mauritius","Mauritius"),("mayotte","Mayotte"),("mexico","Mexico"),("micronesia, federated states of","Micronesia, Federated States of"),("moldova, republic of","Moldova, Republic of"),("monaco","Monaco"),("mongolia","Mongolia"),("montenegro","Montenegro"),("montserrat","Montserrat"),("morocco","Morocco"),("mozambique","Mozambique"),("myanmar","Myanmar"),("namibia","Namibia"),("nauru","Nauru"),("nepal","Nepal"),("netherlands","Netherlands"),("netherlands antilles","Netherlands Antilles"),("new caledonia","New Caledonia"),("new zealand","New Zealand"),("nicaragua","Nicaragua"),("niger","Niger"),("nigeria","Nigeria"),("niue","Niue"),("norfolk island","Norfolk Island"),("northern mariana islands","Northern Mariana Islands"),("norway","Norway"),("oman","Oman"),("pakistan","Pakistan"),("palau","Palau"),("palestinian territory, occupied","Palestinian Territory, Occupied"),("panama","Panama"),("papua new guinea","Papua New Guinea"),("paraguay","Paraguay"),("peru","Peru"),("philippines","Philippines"),("pitcairn","Pitcairn"),("poland","Poland"),("portugal","Portugal"),("puerto rico","Puerto Rico"),("qatar","Qatar"),("reunion","Reunion"),("romania","Romania"),("russian federation","Russian Federation"),("rwanda","Rwanda"),("saint helena","Saint Helena"),("saint kitts and nevis","Saint Kitts and Nevis"),("saint lucia","Saint Lucia"),("saint pierre and miquelon","Saint Pierre and Miquelon"),("saint vincent and the grenadines","Saint Vincent and The Grenadines"),("samoa","Samoa"),("san marino","San Marino"),("sao tome and principe","Sao Tome and Principe"),("saudi arabia","Saudi Arabia"),("senegal","Senegal"),("serbia","Serbia"),("seychelles","Seychelles"),("sierra leone","Sierra Leone"),("singapore","Singapore"),("slovakia","Slovakia"),("slovenia","Slovenia"),("solomon islands","Solomon Islands"),("somalia","Somalia"),("south africa","South Africa"),("south georgia and the south sandwich islands","South Georgia and The South Sandwich Islands"),("spain","Spain"),("sri lanka","Sri Lanka"),("sudan","Sudan"),("suriname","Suriname"),("svalbard and jan mayen","Svalbard and Jan Mayen"),("swaziland","Swaziland"),("sweden","Sweden"),("switzerland","Switzerland"),("syrian arab republic","Syrian Arab Republic"),("taiwan","Taiwan"),("tajikistan","Tajikistan"),("tanzania, united republic of","Tanzania, United Republic of"),("thailand","Thailand"),("timor-leste","Timor-leste"),("togo","Togo"),("tokelau","Tokelau"),("tonga","Tonga"),("trinidad and tobago","Trinidad and Tobago"),("tunisia","Tunisia"),("turkey","Turkey"),("turkmenistan","Turkmenistan"),("turks and caicos islands","Turks and Caicos Islands"),("tuvalu","Tuvalu"),("uganda","Uganda"),("ukraine","Ukraine"),("united arab emirates","United Arab Emirates"),("united kingdom","United Kingdom"),("united states","United States"),("united states minor outlying islands","United States Minor Outlying Islands"),("uruguay","Uruguay"),("uzbekistan","Uzbekistan"),("vanuatu","Vanuatu"),("venezuela","Venezuela"),("viet nam","Viet Nam"),("virgin islands, british","Virgin Islands, British"),("virgin islands, u.s.","Virgin Islands, U.S."),("wallis and futuna","Wallis and Futuna"),("western sahara","Western Sahara"),("yemen","Yemen"),("zambia","Zambia"),("zimbabwe","Zimbabwe")
]
    form.language.choices  = [('cantonese','Cantonese'),('english','English'),('arabic','Arabic'),('chinese','Chinese')]
    if form.validate_on_submit():
        is_valid = validate_email(email_address=form.email.data, check_regex=True, check_mx=True)
        if is_valid:

            hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,password=hashed_pw, role='STUDENT')

            student = Student(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,password=hashed_pw,package="WEEKLY",number_of_lessons_remaining=0,country=form.country.data,language=form.language.data)
            db.session.add(user)
            db.session.add(student)
            db.session.commit()
            student.id = user.id
            db.session.commit()
            os.mkdir(app.root_path + '/static/data/students/' + student.first_name + '_' + student.email)
            copy2(app.root_path + '/static/data/students/default.jpg',app.root_path + '/static/data/students/' + student.first_name + '_' + student.email)
            email, subject, message = 'yousaidhiacc@gmail.com', 'Welcome to yousaidhi.com', '''
            Welcome {}!
                We congratulate you on taking a step towards learning one of the most influential language in the world.
            We are looking forward to teach you English step by step until you become quite fluent in it.

            If you have any issues or queries regarding our website or dashboard, feel free to contact us on yousaidhiacc@gmail.com

            Regards,
            Fatima Zuberi
            Thank you.
            '''.format(student.first_name.title()+' '+student.last_name.title())
            msg = Message(subject, sender=email, recipients=[student.email])
            msg.body = message
            mail.send(msg)
            flash('Account created successfully! Login now.','success')
            return redirect(url_for('login'))
        else:
            flash('Please enter a valid email address!','danger')
            return redirect(url_for('register'))

    return render_template('register.html',title='Register',form=form,emails=emails)


#-----------------------------------------------------------------------------------------------------------------------#
###########################                       LOGIN LOGOUT                        ###################################
#-----------------------------------------------------------------------------------------------------------------------#
@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'ADMIN':
            return redirect(url_for('admin.index'))
        elif current_user.role == 'TEACHER':

            return redirect(url_for('teacher_panel'))
        elif current_user.role == 'STUDENT':
            return redirect(url_for('student_panel'))
        elif current_user.role == 'TEACHER_ADMIN':
            return redirect(url_for('teacher_admin_panel'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            user.user_time_zone = form.time_zone.data
            db.session.commit()
        except:
            flash('You are not yet registered! Please register first!','danger')
            return redirect(url_for('login'))
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            if current_user.role == 'ADMIN':
                current_user.user_time_zone = form.time_zone.data
                return redirect(url_for('admin.index'))
            elif current_user.role == 'STUDENT':
                current_user.user_time_zone = form.time_zone.data
                return redirect(url_for('student_panel'))
            elif current_user.role == 'TEACHER':
                current_user.user_time_zone = form.time_zone.data
                return redirect(url_for('teacher_panel'))
        flash('Email or Password incorrect!','danger')
        return redirect(url_for('login'))
    return render_template('login.html',form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

#-----------------------------------------------------------------------------------------------------------------------#
###########################                       TEACHER PANEL                       ###################################
#-----------------------------------------------------------------------------------------------------------------------#

@app.route('/teacherpanel',methods=['GET','POST'])
@login_required(role="TEACHER")
def teacher_panel():
    teacher = Teacher.query.get(current_user.id)
    teacher_dict = teacher.return_dict()
    # NOT SURE
    # check if the time has passed for a booking and the status has not yet been changed to lecture taken
    current_time = datetime.datetime.utcnow()
    current_time = current_time.replace(tzinfo=pytz.utc)
    for booking in Booking.query.all():
        booking_time_string = booking.date.date + ' ' + booking.slot.slot.split('-')[1]
        time_zone = booking.slot.teacher_time_zone
        datetime_obj = datetime.datetime.strptime(booking_time_string, '%Y-%m-%d %H:%M')
        new_converted_date_obj = datetime_obj.astimezone(pytz.timezone(time_zone))
        current_time_converted_time_zone = current_time.astimezone(pytz.timezone(time_zone))
        if booking.lecture_complete == False:
            if new_converted_date_obj < current_time_converted_time_zone:
                booking.lecture_complete = True
                # If teacher was present then it will add to the completed lectures of the teacher!
                # if booking.teacher_present == True:
                #     teacher.completed_lessons+=1
                db.session.commit()


    # This is for getting all the undone bookings
    bookings_undone = []
    my_bookings = teacher.bookings
    try:

        # this is done to sort the datetime of bookings according to the latest booking
        booking_with_time = []
        booking_with_time_all = []
        for booking in my_bookings:
            if booking.lecture_complete == False:
                booking_time_string = booking.date.date + ' ' + booking.slot.slot.split('-')[0]
                time_zone = booking.slot.teacher_time_zone

                datetime_obj = datetime.datetime.strptime(booking_time_string, '%Y-%m-%d %H:%M')

                new_converted_date_obj = datetime_obj.astimezone(pytz.timezone(time_zone))

                booking_with_time.append([new_converted_date_obj, booking])
            booking_time_string = booking.date.date + ' ' + booking.slot.slot.split('-')[0]
            time_zone = booking.slot.teacher_time_zone

            datetime_obj = datetime.datetime.strptime(booking_time_string, '%Y-%m-%d %H:%M')

            new_converted_date_obj = datetime_obj.astimezone(pytz.timezone(time_zone))

            booking_with_time_all.append([new_converted_date_obj, booking])
        # sorting list items with dates
        sorted_booking_with_time = sorted(booking_with_time, key=itemgetter(0))
        sorted_all_booking_with_time = sorted(booking_with_time_all, key=itemgetter(0))
        bookings_undone = [x[1] for x in sorted_booking_with_time]
        my_bookings = [x[1] for x in sorted_all_booking_with_time]
        latest_booking = sorted_booking_with_time[0][1].return_dict()

    except:
        latest_booking = {}

    # For use in javascript

    all_bookings = Booking.return_all_obj()
    all_slots = Slot.return_all_obj()
    all_teachers = Teacher.return_all_obj()
    all_course = Course.return_all_obj()
    all_lessons = Lesson.return_all_obj()
    all_dates = Date.return_all_obj()
    all_students = Student.return_all_obj()

    # For use in jinja
    teachers = Teacher.query.all()
    students = Student.query.all()
    courses = Course.query.all()
    lessons = Lesson.query.all()
    slots = Slot.query.all()
    dates = Date.query.all()

    # Coding for set slots calendar
    base = datetime.datetime.strptime("2020-01-01", '%Y-%m-%d')
    slots_2 = [["00:00-00:30",0],["00:30-01:00",0],["01:00-01:30",0],["01:30-02:00",0],["02:00-02:30",0],["02:30-03:00",0],["03:00-03:30",0],["03:30-04:00",0],["04:00-04:30",0],["04:30-05:00",0],["05:00-05:30",0],["05:30-06:00",0],["06:00-06:30",0],["06:30-07:00",0],["07:00-07:30",0],["07:30-08:00",0],["08:00-08:30",0],["08:30-09:00",0],["09:00-09:30",0],["09:30-10:00",0],["10:00-10:30",0],["10:30-11:00",0],["11:00-11:30",0],["11:30-12:00",0],["12:00-12:30",0],["12:30-13:00",0],["13:00-13:30",0],["13:30-14:00",0],["14:00-14:30",0],["14:30-15:00",0],["15:00-15:30",0],["15:30-16:00",0],["16:00-16:30",0],["16:30-17:00",0],["17:00-17:30",0],["17:30-18:00",0],["18:00-18:30",0],["18:30-19:00",0],["19:00-19:30",0],["19:30-20:00",0],["20:00-20:30",0],["20:30-21:00",0],["21:00-21:30",0],["21:30-22:00",0],["22:00-22:30",0],["22:30-23:00",0],["23:00-23:30",0],["23:30-23:59",0]]
    date_list = [[(base+datetime.timedelta(days=x)).strftime("%Y-%m-%d"),copy.deepcopy(slots_2)] for x in range(3656)]

    teacher_dates_list_for_match = [[x.date,[[a.slot,a.booked] for a in x.slots]] for x in teacher.dates]
    for each_date in range(len(date_list)):
        for teacher_date in range(len(teacher_dates_list_for_match)):
            if date_list[each_date][0] == teacher_dates_list_for_match[teacher_date][0]:
                for each_teacher_date_slot in range(len(teacher_dates_list_for_match[teacher_date][1])):
                    for each_date_slot in range(len(date_list[each_date][1])):
                        if teacher_dates_list_for_match[teacher_date][1][each_teacher_date_slot][0] == date_list[each_date][1][each_date_slot][0]:
                            if teacher_dates_list_for_match[teacher_date][1][each_teacher_date_slot][1] == True:
                                date_list[each_date][1][each_date_slot][1] = "Booked"
                            else:
                                date_list[each_date][1][each_date_slot][1] = "Available"
        date_list[each_date][0] = datetime.datetime.strptime(date_list[each_date][0],"%Y-%m-%d").strftime("%m/%d/%Y")
    final_date_list = []
    counter=0
    ref_list = []
    todays_date = datetime.datetime.today().date().strftime("%m/%d/%Y")
    today_index = 0
    c_index = 0
    for each in range(len(date_list)):
        if counter<7:
            ref_list.append(date_list[each])
            counter+=1
            if date_list[each][0] == todays_date:
                today_index=c_index
        else:
            counter=1
            final_date_list.append(ref_list)
            ref_list=[date_list[each]]
            c_index+=1
            if date_list[each][0] == todays_date:
                today_index=c_index


    #For Summary
    summary_bookings_dict = {}
    monthsss = {'01':"January",'02':"February",'03':"March",'04':"April",'05':"May",'06':"June",'07':"July",'08':"August",'09':"September",'10':"October",'11':"November",'12':"December"}
    salaries = teacher.salaries
    for booking in my_bookings:
        date = booking.date.date
        year,month,date = date.split('-')[0],date.split('-')[1],date.split('-')[2]
        salary = None
        if salaries == []:
            pass
        else:
            for each in salaries:
                if each.year == int(year) and each.month == int(month):
                    salary = each
                    break
        if salary == None:
            salary = TeacherSalary(teacher_id=teacher.id, year=int(year), month=int(month), salary=0)
            db.session.add(salary)
            db.session.commit()
        if year in summary_bookings_dict.keys():
            if monthsss[month] in summary_bookings_dict[year].keys():
                summary_bookings_dict[year][monthsss[month]][0].append(booking)
            else:
                summary_bookings_dict[year][monthsss[month]] = [[booking],salary]
        else:
            summary_bookings_dict[year] = {}
            summary_bookings_dict[year][monthsss[month]] = [[booking],salary]

    update_picture_form = EditTeacherProfile()
    if update_picture_form.validate_on_submit():
        teacher = Teacher.query.get(current_user.id)
        try:
            os.remove(app.root_path + '/static/data/teachers/' + teacher.first_name + '_' + teacher.email + '/' + teacher.image_file)
        except:
            pass
        path = app.root_path + '/static/data/teachers/' + teacher.first_name + '_' + teacher.email

        picture_file = save_picture(update_picture_form.picture.data, path)
        teacher.image_file = picture_file
        db.session.commit()
        return redirect(url_for('teacher_panel'))

    return render_template('teacher_panel.html',teacher=teacher,latest_booking=latest_booking,all_bookings=all_bookings,all_slots=all_slots,all_teachers=all_teachers,all_course=all_course,all_lessons=all_lessons,all_dates=all_dates,all_students=all_students,teacher_dict=teacher_dict,teachers=teachers,students=students,courses=courses,lessons=lessons,slots=slots,dates=dates,bookings_undone=bookings_undone,my_bookings=my_bookings,final_date_list=final_date_list,today_index=today_index,summary_bookings_dict=summary_bookings_dict,update_picture_form=update_picture_form)

@app.route('/make_slot_available',methods=['GET','POST'])
@login_required(role="TEACHER")
def make_slot_available():
    data = dict(request.form)
    data = data['selected_slot']
    date_form,slot_form = datetime.datetime.strptime(data.split(',')[0],'%m/%d/%Y').strftime('%Y-%m-%d'),data.split(',')[1]
    teacher = Teacher.query.get(current_user.id)
    date_found = 0
    for each in teacher.dates:
        if date_form==each.date:
            available = 0
            for slots in each.slots:
                if slots.slot == slot_form:
                    available = 1
                    break
            if available == 0:
                slot = Slot(slot=slot_form,date=each,teacher_time_zone='Asia/Karachi')
                db.session.add(slot)
                db.session.commit()
                date_found=1
            else:
                return jsonify({'done': True})
    if date_found==0:
        date = Date(date=date_form,teacher=teacher)
        slot = Slot(slot=slot_form, date=date, teacher_time_zone='Asia/Karachi')
        db.session.add(date)
        db.session.add(slot)
        db.session.commit()

    return jsonify({'done':True})
@app.route('/make_slot_unavailable',methods=['GET','POST'])
@login_required(role="TEACHER")
def make_slot_unavailable():
    data = dict(request.form)
    data = data['selected_slot']
    date_form,slot_form = datetime.datetime.strptime(data.split(',')[0],'%m/%d/%Y').strftime('%Y-%m-%d'),data.split(',')[1]
    teacher = Teacher.query.get(current_user.id)

    for each in teacher.dates:
        if date_form==each.date:
            for slots in each.slots:
                if slots.slot == slot_form:
                    s = Slot.query.get(slots.id)
                    if s.booked:
                        pass
                    else:
                        db.session.delete(s)
                        db.session.commit()




    return jsonify({'done':True})

@app.route('/teacherpanel_zoom_attendace',methods=['GET','POST'])
@login_required(role="TEACHER")
def teacherpanel_zoom_attendace():
    data = dict(request.form)
    booking = Booking.query.get(int(data['booking_id']))
    if booking.teacher_present == False:
        booking.teacher_present = True
        teacher = Teacher.query.get(int(booking.teacher_id))
        if teacher.completed_lessons == None:
            teacher.completed_lessons = 1
        else:
            teacher.completed_lessons+=1
        db.session.commit()

    return jsonify({'done':True})
@app.route('/teacher_edit_name',methods=['GET','POST'])
@login_required(role="TEACHER")
def teacher_edit_name():
    data = dict(request.form)
    t = Teacher.query.get(current_user.id)
    fname = data['first_name']
    lname = data['last_name']
    t.first_name=fname
    t.last_name=lname
    db.session.commit()

    return jsonify({'done':True})
@app.route('/teacher_edit_info',methods=['GET','POST'])
@login_required(role="TEACHER")
def teacher_edit_info():
    data = dict(request.form)
    t = Teacher.query.get(current_user.id)
    desc = data['desc']
    about = data['about']
    zoom = data['zoom']
    acct = data['acct']
    accn = data['accn']
    bankn = data['bankn']
    mobn = data['mobn']

    t.one_line_description=desc
    t.about=about
    t.zoom_link = zoom
    t.account_title = acct
    t.account_number = accn
    t.account_bank = bankn
    t.mobile_number = mobn
    db.session.commit()

    return jsonify({'done':True})

@app.route('/teacherdbchanges',methods=['GET','POST'])
@login_required(role="TEACHER")
def teacherdbchanges():
    data = ImmutableMultiDict(request.form)
    data = data.to_dict(flat=False)

    data = list(data.keys())[0]
    data = json.dumps(data)
    data = json.loads(data)

    data = ast.literal_eval(data)

    json_all_bookings = data['all_bookings']




    all_bookings = Booking.return_all_obj()

    json_all_bookings = {int(k):v for k,v in json_all_bookings.items()}

    if all_bookings==json_all_bookings:
        # print("TRUE")
        return jsonify({'val':True})
    else:
        return jsonify({'val':False})


@app.route('/teacher_feedback',methods=['GET','POST'])
@login_required(role="TEACHER")
def teacher_feedback():
    data = dict(request.form)
    booking_id = int(data['lecture_booking_id'])
    feedback = data['feedback'].strip().title()
    booking = Booking.query.get(booking_id)
    booking.teacher_feedback = feedback
    db.session.commit()
    return jsonify({'val':True})

#-----------------------------------------------------------------------------------------------------------------------#
###########################                       STUDENT PANEL                       ###################################
#-----------------------------------------------------------------------------------------------------------------------#


@app.route('/studentpanel',methods=['GET','POST'])
@login_required(role="STUDENT")
def student_panel():
    #check if any lesson's time is past the current time, and the status has not yet been changed to lecture taken
    current_time = datetime.datetime.utcnow()
    current_time = current_time.replace(tzinfo=pytz.utc)
    for booking in Booking.query.all():
        booking_time_string = booking.date.date + ' ' + booking.slot.slot.split('-')[1]
        time_zone = booking.slot.teacher_time_zone
        datetime_obj = datetime.datetime.strptime(booking_time_string,'%Y-%m-%d %H:%M')
        new_converted_date_obj = datetime_obj.astimezone(pytz.timezone(time_zone))
        current_time_converted_time_zone = current_time.astimezone(pytz.timezone(time_zone))
        if booking.lecture_complete == False:
            if new_converted_date_obj<current_time_converted_time_zone:
                booking.lecture_complete = True
                # student = Student.query.get(current_user.id)
                # if booking.student_present == False:
                #     student.number_of_lessons_remaining -= 1
                db.session.commit()

    student = Student.query.get(current_user.id)

    student_dict = student.return_dict()

    #lessons
    bookings_undone = {}
    my_bookings = student.bookings
    try:
        for each in my_bookings:
            if each.lecture_complete==False:
                bookings_undone[each.id] = each

        #this is done to sort the datetime of bookings according to the latest booking
        booking_with_time = []
        for booking in my_bookings:
            if booking.lecture_complete == False:
                booking_time_string = booking.date.date + ' ' + booking.slot.slot.split('-')[0]
                time_zone = booking.slot.teacher_time_zone

                datetime_obj = datetime.datetime.strptime(booking_time_string,'%Y-%m-%d %H:%M')

                new_converted_date_obj = datetime_obj.astimezone(pytz.timezone(time_zone))

                booking_with_time.append([new_converted_date_obj,booking])

        #sorting list items with dates
        sorted_booking_with_time = sorted(booking_with_time,key=itemgetter(0))

        latest_booking = sorted_booking_with_time[0][1].return_dict()

    except:
        latest_booking = {}

    #For use in javascript

    all_bookings = Booking.return_all_obj()
    all_slots = Slot.return_all_obj()
    all_teachers = Teacher.return_all_obj()
    all_course = Course.return_all_obj()
    all_lessons = Lesson.return_all_obj()
    all_dates = Date.return_all_obj()
    all_students = Student.return_all_obj()
    all_complains = StudentComplain.return_all_obj()
    #modified slots and dates according to student schedule for bookings only!
    #REMEBER!! not to use the slots key within the new timezone dates as that is not update, this is just for reference in html for converted timezones!!!!
    user_timezone_dates = {}
    user_timezone_slots = {}
    user_timezone = current_user.user_time_zone
    user_timezone_booking_dict = {}

    for k,v in all_bookings.items():

        if v['student_id'] == current_user.id:

            booking_time_string = all_dates[v['date_id']]['date'] + ' ' + all_slots[v['slot_id']]['slot'].split('-')[0]
            datetime_obj = datetime.datetime.strptime(booking_time_string,'%Y-%m-%d %H:%M')

            new_converted_date_obj_starting = datetime_obj.astimezone(pytz.timezone(user_timezone))

            new_converted_date_obj_ending = new_converted_date_obj_starting+datetime.timedelta(minutes=30)

            new_converted_date_obj_starting = new_converted_date_obj_starting.strftime('%Y-%m-%d %H:%M')

            new_converted_date_obj_ending = new_converted_date_obj_ending.strftime('%Y-%m-%d %H:%M')

            user_timezone_booking_dict[k] = {"date":new_converted_date_obj_starting.split(' ')[0],"slot":new_converted_date_obj_starting.split(' ')[1]+'-'+new_converted_date_obj_ending.split(' ')[1]}



    teacher_dates = {}
    for teachers in Teacher.query.all():
        teacher_dates[teachers.id] = []

        for dates in teachers.dates:
            date_list = []
            date_list.append(dates.id)
            date_list.append(dates.date)
            date_list.append([])
            for slots in dates.slots:

                if slots.booked:
                    continue
                else:
                    slot = []
                    slot.append(slots.id)
                    slot.append(slots.slot)
                    slot.append(slots.teacher_time_zone)
                    date_list[2].append(slot)
            teacher_dates[teachers.id].append(date_list)

    # For use in jinja
    teachers = Teacher.query.all()
    students = Student.query.all()
    courses = Course.query.all()
    lessons = Lesson.query.all()
    slots = Slot.query.all()
    dates = Date.query.all()
    complains = StudentComplain.query.all()
    videos = Videos.query.all()
    update_form = EditStudentProfile()
    if update_form.validate_on_submit():

        if update_form.picture.data:
            student = Student.query.get(current_user.id)
            try:
                os.remove(app.root_path + '/static/data/students/' + student.first_name + '_'+student.email+'/'+student.image_file)
            except:
                pass
            path = app.root_path + '/static/data/students/' + student.first_name + '_'+student.email

            picture_file = save_picture(update_form.picture.data,path)
            student.image_file = picture_file

        if update_form.password.data and update_form.confirm_password.data:
            hashed_pw = bcrypt.generate_password_hash(update_form.password.data).decode('utf-8')
            current_user.password = hashed_pw
            student.password = hashed_pw
        #
        # current_user.first_name = update_form.first_name.data
        # current_user.last_name = update_form.last_name.data
        #
        #
        # student.first_name = update_form.first_name.data
        # student.last_name = update_form.last_name.data



        db.session.commit()
        return redirect(url_for('student_panel'))
    elif request.method=='GET':
        student = Student.query.get(current_user.id)

        update_form.first_name.data = student.first_name
        update_form.last_name.data = student.last_name

    student = Student.query.get(current_user.id)

    student_b = student.bookings
    my_lessons = []
    for each in student_b:
        my_lessons.append(each.lesson)



    return render_template('student_panel.html',student=student,student_dict=student_dict,latest_booking=latest_booking,all_bookings=all_bookings,all_course=all_course,all_slots=all_slots,all_teachers=all_teachers,all_lessons=all_lessons,all_dates=all_dates,all_students=all_students,user_timezone_booking_dict=user_timezone_booking_dict,teacher_dates = teacher_dates,teachers=teachers,studetns=students,courses=courses,lessons=lessons,slots=slots,dates=dates,update_form=update_form,my_lessons=my_lessons,complains=complains,all_complains=all_complains,videos=videos)


@app.route('/student_lesson_booking',methods=['GET','POST'])
@login_required(role="STUDENT")
def student_lesson_booking():

    try:
        data = dict(request.form)

        lesson_id = data['lesson_id']
        teacher_id = data['teacher_id']
        slot_id = data['slot_id']
        date_id = Slot.query.get(int(slot_id)).date_id
        student_id = current_user.id
        student = Student.query.get(student_id)
        if student.number_of_lessons_remaining==0:
            return jsonify({'lessons':0})
        else:
            for bookings in Booking.query.all():
                if int(slot_id)==int(bookings.slot_id):
                    return jsonify({'booked':1})

            booking = Booking(student_id=student_id,teacher_id=teacher_id,lesson_id=lesson_id,date_id=date_id,slot_id=slot_id)
            slot = Slot.query.get(int(slot_id))
            slot.booked = True
            student.number_of_lessons_remaining-=1
            db.session.add(booking)
            db.session.commit()

            return jsonify({'data':'1'})
    except:
        return jsonify({'data':'0'})

@app.route('/studentpanel_zoom_attendace',methods=['GET','POST'])
@login_required(role="STUDENT")
def studentpanel_zoom_attendace():
    data = dict(request.form)
    booking = Booking.query.get(int(data['booking_id']))
    if booking.student_present == False:
        booking.student_present = True
        student = Student.query.get(int(booking.student_id))
        # student.number_of_lessons_remaining -= 1
        db.session.commit()

    return jsonify({'done':True})

@app.route('/student_after_payment',methods=['GET','POST'])
@login_required(role="STUDENT")
def student_after_payment():
    data = dict(request.form)
    student_id = int(data['student_id'])
    lessons = int(data['lessons'])
    student = Student.query.get(student_id)
    student.number_of_lessons_remaining +=lessons
    db.session.commit()
    price= lessons*3
    date_today = str(datetime.datetime.today().date())

    payment = PaymentRecord(student_id=student_id,number_of_lessons=lessons,price=price,date=date_today)
    db.session.add(payment)
    db.session.commit()
    return jsonify({'done':True})

@app.route('/studentpanel_complain',methods=['GET','POST'])
@login_required(role="STUDENT")
def studentpanel_complain():
    data = dict(request.form)

    booking_id = data['booking_id']
    complain_text = data['complain_text']
    student_id = data['student_id']
    if booking_id=='':
        complain = StudentComplain(complain=complain_text,resolved=False,student_id=int(student_id))
    else:
        complain = StudentComplain(booking_id=int(booking_id),complain=complain_text,resolved=False,student_id=int(student_id))


    db.session.add(complain)

    db.session.commit()
    complain_id = complain.id
    return jsonify({'complain_id':complain_id})

@app.route('/studentdbchanges',methods=['GET','POST'])
@login_required(role="STUDENT")
def studentdbchanges():
    data = ImmutableMultiDict(request.form)
    data = data.to_dict(flat=False)

    data = list(data.keys())[0]
    data = json.dumps(data)
    data = json.loads(data)

    data = ast.literal_eval(data)

    json_all_bookings = data['all_bookings']
    json_all_slots = data['all_slots']
    json_all_dates = data['all_dates']



    all_bookings = Booking.return_all_obj()
    all_slots = Slot.return_all_obj()
    all_dates = Date.return_all_obj()

    json_all_slots = {int(k):v for k,v in json_all_slots.items()}
    json_all_bookings = {int(k):v for k,v in json_all_bookings.items()}
    json_all_dates = {int(k):v for k,v in json_all_dates.items()}
    if (all_slots == json_all_slots) and (all_bookings==json_all_bookings) and (all_dates==json_all_dates):
        return jsonify({'val':True})
    else:
        return jsonify({'val':False})


#-----------------------------------------------------------------------------------------------------------------------#
###########################                       TEACHER ADMIN PANEL                 ###################################
#-----------------------------------------------------------------------------------------------------------------------#
@app.route('/teacheradminpanel',methods=['GET','POST'])
@login_required(role="TEACHER_ADMIN")
def teacher_admin_panel():
    teachers = Teacher.query.all()
    form = TeacherRegistration()
    courses = Course.query.all()
    form2 = AddCourseForm()
    form3 = AddLessonForm()
    form3.course_id.choices = [(x.id, x.course_name.title()) for x in Course.query.all()]
    form4 = AddVideoForm()
    # For use in javascript

    all_bookings = Booking.return_all_obj()
    all_slots = Slot.return_all_obj()
    all_teachers = Teacher.return_all_obj()
    all_course = Course.return_all_obj()
    all_lessons = Lesson.return_all_obj()
    all_dates = Date.return_all_obj()
    all_students = Student.return_all_obj()
    all_complains = StudentComplain.return_all_obj()
    complains = StudentComplain.query.all()
    student_payments = PaymentRecord.query.all()
    monthsss = {'01': "January", '02': "February", '03': "March", '04': "April", '05': "May", '06': "June",
                '07': "July", '08': "August", '09': "September", '10': "October", '11': "November", '12': "December"}
    all_teachers_salary = {}
    for teacher in teachers:
        summary_bookings_dict = {}
        salaries = teacher.salaries
        for booking in teacher.bookings:
            date = booking.date.date
            year, month, date = date.split('-')[0], date.split('-')[1], date.split('-')[2]
            salary = None
            if salaries==[]:
                pass
            else:
                for each in salaries:
                    if each.year == int(year) and each.month == int(month):
                        salary = each
                        break
            if salary==None:
                salary = TeacherSalary(teacher_id=teacher.id,year=int(year),month=int(month),salary=0)
                db.session.add(salary)
                db.session.commit()
            if year in summary_bookings_dict.keys():
                if monthsss[month] in summary_bookings_dict[year].keys():
                    summary_bookings_dict[year][monthsss[month]][0].append(booking)
                else:
                    summary_bookings_dict[year][monthsss[month]] = [[booking],salary]
            else:
                summary_bookings_dict[year] = {}
                summary_bookings_dict[year][monthsss[month]] = [[booking],salary]

        all_teachers_salary[teacher.id] = summary_bookings_dict

    return render_template('teacher_admin_panel.html',teachers=teachers,form=form,courses=courses,form2=form2,form3=form3,form4=form4,all_bookings=all_bookings,all_slots=all_slots,all_teachers=all_teachers,all_course=all_course,all_lessons=all_lessons,all_dates=all_dates,all_students=all_students,all_complains=all_complains,complains=complains,all_teachers_salary=all_teachers_salary,student_payments=student_payments)


@app.route('/register_teacher_admin_panel',methods=['GET','POST'])
@login_required(role="TEACHER_ADMIN")
def register_teacher_admin_panel():

    form = TeacherRegistration()
    if form.validate_on_submit():
        os.mkdir(app.root_path + '/static/data/teachers/' + form.first_name.data + '_' + form.email.data)
        path = app.root_path + '/static/data/teachers/' + form.first_name.data + '_' + form.email.data
        picture_file = ''
        try:
            picture_file = save_picture(form.teacher_image.data,path)
        except:
            pass

        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,password=hashed_pw, role='TEACHER')
        teacher = Teacher(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                          password=hashed_pw,image_file=picture_file,zoom_link=form.zoom_link.data)
        db.session.add(user)
        db.session.add(teacher)
        db.session.commit()
        teacher.id = user.id
        db.session.commit()

        flash('Account created for {}!'.format(form.first_name.data), 'success')
        return redirect(url_for('teacher_admin_panel'))
    flash('Please register again, Error!','danger')
    return redirect(url_for('teacher_admin_panel'))


@app.route('/register_course_teacher_admin_panel',methods=['GET','POST'])
@login_required(role="TEACHER_ADMIN")
def register_course_teacher_admin_panel():
    form2 = AddCourseForm()
    if form2.validate_on_submit():
        try:
            os.mkdir(app.root_path + '/static/data/courses/' + form2.course_code.data.strip().upper())
        except:
            pass
        path = app.root_path + '/static/data/courses/' + form2.course_code.data.strip().upper()
        try:
            picture_file = save_picture(form2.course_image.data,path)
        except Exception as e:
            print(e)
            flash('Please add picture in course!, Error!', 'danger')
            return redirect(url_for('teacher_admin_panel'))
        course = Course(course_code=form2.course_code.data.strip(),course_name=form2.course_name.data.strip(),course_image=picture_file,course_description=form2.course_description.data)

        db.session.add(course)
        db.session.commit()
        flash('Course Created Successfully', 'success')
        return redirect(url_for('teacher_admin_panel'))

    flash('Please add course again, Error!', 'danger')
    return redirect(url_for('teacher_admin_panel'))


@app.route('/register_lesson_teacher_admin_panel',methods=['GET','POST'])
@login_required(role="TEACHER_ADMIN")
def register_lesson_teacher_admin_panel():
    form3 = AddLessonForm()
    form3.course_id.choices = [(x.id,x.course_name.title()) for x in Course.query.all()]
    if form3.validate_on_submit():
        course = Course.query.get(form3.course_id.data)
        os.mkdir(app.root_path + '/static/data/courses/' + course.course_code.strip().upper()+'/'+form3.lesson_code.data.strip())
        path = app.root_path + '/static/data/courses/' + course.course_code.strip().upper()+'/'+form3.lesson_code.data.strip()
        picture_file = save_picture(form3.lesson_image.data,path)

        lesson = Lesson(lesson_name=form3.lesson_name.data.strip(),lesson_code=form3.lesson_code.data.strip(),lesson_image=picture_file,course=course,lesson_homework=form3.lesson_homework.data)
        db.session.add(lesson)
        db.session.commit()

        for each in form3.lesson_documents.data:
            for items in each.values():

                document = LessonDocument(document=items,lesson=lesson)
                lesson.lesson_documents.append(document)
                db.session.add(document)
                db.session.commit()



        flash('Lesson Created Successfully', 'success')
        return redirect(url_for('teacher_admin_panel'))

    flash('Lesson Not Created! Add again','danger')
    return redirect(url_for('teacher_admin_panel'))
@app.route('/teacheradminpanel_delete_teacher',methods=['GET','POST'])
@login_required(role="TEACHER_ADMIN")
def teacheradminpanel_delete_teacher():

    data = dict(request.form)
    teacher = Teacher.query.get(int(data['teacher_id']))
    # print(teacher)
    # db.session.delete(teacher)
    # db.session.commit()


    return jsonify({'done':True})

@app.route('/teacheradminpanel_edit_student_lessons',methods=['GET','POST'])
@login_required(role="TEACHER_ADMIN")
def teacheradminpanel_edit_student_lessons():
    data = dict(request.form)
    student_id = data['student_id']
    new_lessons = int(data['new_num_lessons'])
    student = Student.query.get(int(student_id))
    student.number_of_lessons_remaining = int(new_lessons)
    db.session.commit()
    return jsonify({'val':'True'})
@app.route('/teacheradminpanel_resolve_complain',methods=['GET','POST'])
@login_required(role="TEACHER_ADMIN")
def teacheradminpanel_resolve_complain():
    data = dict(request.form)
    complain_id = int(data['complain_id'])

    complain = StudentComplain.query.get(complain_id)

    complain.resolved = True
    db.session.commit()
    return jsonify({'val':'True'})

@app.route('/teacheradminpanel_update_salary',methods=['GET','POST'])
@login_required(role="TEACHER_ADMIN")
def teacheradminpanel_update_salary():
    data = dict(request.form)
    salary_id = int(data['salary_id'])
    salarynum = int(data['salary'])

    salar = TeacherSalary.query.get(salary_id)
    salar.salary = salarynum
    db.session.commit()

    return jsonify({'val':'True'})

@app.route('/add_video_teacher_admin_panel',methods=['GET','POST'])
@login_required(role="TEACHER_ADMIN")
def add_video_teacher_admin_panel():
    form4 = AddVideoForm()
    if form4.validate_on_submit():
        path = app.root_path + '/static/html_vids/'
        picture_file = save_picture(form4.video_image.data, path)
        video = Videos(name=form4.video_name.data,link=form4.video_link.data,thumbnail=picture_file)
        db.session.add(video)
        db.session.commit()
        flash('Video Added Successfully', 'success')
        return redirect(url_for('teacher_admin_panel'))


    flash('Video Not Added! Add again', 'danger')
    return redirect(url_for('teacher_admin_panel'))
#-----------------------------------------------------------------------------------------------------------------------#
###########################                       TEST PAGE                        ###################################
#-----------------------------------------------------------------------------------------------------------------------#

# @app.route('/test',methods=['GET','POST'])
# def test():
#
#     teacher_dates = [
#
#             ['1','2020-01-10',[['1','02:00-02:30','Pakistan/Karachi'],['2','03:00-03:30','Pakistan/Karachi'],['3','12:00-12:30','Pakistan/Karachi'],['4','16:00-16:30','Pakistan/Karachi']]],
#             ['2','2020-01-11',[['5','07:00-07:30','Pakistan/Karachi'],['6','03:00-03:30','Pakistan/Karachi']]],
#             ['3','2020-01-12',[['7','09:00-09:30','Pakistan/Karachi'],['8','03:00-03:30','Pakistan/Karachi'],['9','12:00-12:30','Pakistan/Karachi'],['10','16:00-16:30','Pakistan/Karachi'],['11','16:00-16:30','Pakistan/Karachi'],['12','16:00-16:30','Pakistan/Karachi']]],
#             ['4','2020-01-13',[['13','21:00-21:30','Pakistan/Karachi'],['14','03:00-03:30','Pakistan/Karachi'],['15','12:00-12:30','Pakistan/Karachi']]],
#             ['5','2020-01-14',[]],
#             ['6','2020-01-15',[['16','05:00-05:30','Pakistan/Karachi'],['17','03:00-03:30','Pakistan/Karachi'],['18','12:00-12:30','Pakistan/Karachi'],['19','16:00-16:30','Pakistan/Karachi']]],
#             ['7','2020-01-16',[['20','23:00-23:30','Pakistan/Karachi'],['21','03:00-03:30','Pakistan/Karachi'],['22','12:00-12:30','Pakistan/Karachi'],['23','16:00-16:30','Pakistan/Karachi']]],
#
#             ['8','2020-01-17',[['24','02:00-02:30','Pakistan/Karachi'],['25','03:00-03:30','Pakistan/Karachi'],['26','12:00-12:30','Pakistan/Karachi'],['27','16:00-16:30','Pakistan/Karachi']]],
#             ['9','2020-01-18',[['28','02:00-02:30','Pakistan/Karachi'],['29','03:00-03:30','Pakistan/Karachi'],['30','12:00-12:30','Pakistan/Karachi'],['31','16:00-16:30','Pakistan/Karachi']]],
#             ['10','2020-01-19',[['20','02:00-02:30','Pakistan/Karachi'],['20','03:00-03:30','Pakistan/Karachi'],['20','12:00-12:30','Pakistan/Karachi'],['20','16:00-16:30','Pakistan/Karachi']]],
#             ['12','2020-01-20',[['20','02:00-02:30','Pakistan/Karachi'],['20','03:00-03:30','Pakistan/Karachi'],['20','12:00-12:30','Pakistan/Karachi'],['20','16:00-16:30','Pakistan/Karachi']]],
#             ['13','2020-01-21',[['20','02:00-02:30','Pakistan/Karachi'],['20','03:00-03:30','Pakistan/Karachi'],['20','12:00-12:30','Pakistan/Karachi'],['20','16:00-16:30','Pakistan/Karachi']]],
#             ['14','2020-01-22',[['20','02:00-02:30','Pakistan/Karachi'],['20','03:00-03:30','Pakistan/Karachi'],['20','12:00-12:30','Pakistan/Karachi'],['20','16:00-16:30','Pakistan/Karachi']]],
#             ['15','2020-01-23',[['20','02:00-02:30','Pakistan/Karachi'],['20','03:00-03:30','Pakistan/Karachi'],['20','12:00-12:30','Pakistan/Karachi'],['20','16:00-16:30','Pakistan/Karachi']]],
#
#             ['16','2020-01-24',[['20','02:00-02:30','Pakistan/Karachi'],['20','03:00-03:30','Pakistan/Karachi'],['20','12:00-12:30','Pakistan/Karachi'],['20','16:00-16:30','Pakistan/Karachi']]],
#             ['17','2020-01-25',[['20','02:00-02:30','Pakistan/Karachi'],['20','03:00-03:30','Pakistan/Karachi'],['20','12:00-12:30','Pakistan/Karachi'],['20','16:00-16:30','Pakistan/Karachi']]],
#             ['18','2020-01-26',[['20','02:00-02:30','Pakistan/Karachi'],['20','03:00-03:30','Pakistan/Karachi'],['20','12:00-12:30','Pakistan/Karachi'],['20','16:00-16:30','Pakistan/Karachi']]],
#             ['19','2020-01-27',[['20','02:00-02:30','Pakistan/Karachi'],['20','03:00-03:30','Pakistan/Karachi'],['20','12:00-12:30','Pakistan/Karachi'],['20','16:00-16:30','Pakistan/Karachi']]],
#             ['20','2020-01-28',[['20','02:00-02:30','Pakistan/Karachi'],['20','03:00-03:30','Pakistan/Karachi'],['20','12:00-12:30','Pakistan/Karachi'],['20','16:00-16:30','Pakistan/Karachi']]],
#             ['21','2020-01-29',[['20','02:00-02:30','Pakistan/Karachi'],['20','03:00-03:30','Pakistan/Karachi'],['20','12:00-12:30','Pakistan/Karachi'],['20','16:00-16:30','Pakistan/Karachi']]],
#             ['22','2020-02-01',[['20','02:00-02:30','Pakistan/Karachi'],['20','03:00-03:30','Pakistan/Karachi'],['20','12:00-12:30','Pakistan/Karachi'],['20','16:00-16:30','Pakistan/Karachi']]],
#
#             ['23','2020-02-02',[['20','02:00-02:30','Pakistan/Karachi'],['20','03:00-03:30','Pakistan/Karachi'],['20','12:00-12:30','Pakistan/Karachi'],['20','16:00-16:30','Pakistan/Karachi']]],
#             ['24','2020-02-03',[['20','02:00-02:30','Pakistan/Karachi'],['20','03:00-03:30','Pakistan/Karachi'],['20','12:00-12:30','Pakistan/Karachi'],['20','16:00-16:30','Pakistan/Karachi']]],
#             ['25','2020-02-04',[['20','02:00-02:30','Pakistan/Karachi'],['20','03:00-03:30','Pakistan/Karachi'],['20','12:00-12:30','Pakistan/Karachi'],['20','16:00-16:30','Pakistan/Karachi']]]
#
#                      ]
#     print(teacher_dates)
#     return render_template('test.html',teacher_dates=teacher_dates)



#-----------------------------------------------------------------------------------------------------------------------#
###########################                       ADMIN PANEL                         ###################################
#-----------------------------------------------------------------------------------------------------------------------#

#
# class MyIndexView(AdminIndexView):
#     def is_accessible(self):
#         return (current_user.is_authenticated and current_user.role == 'ADMIN')
#
#
#
# class RegisterTeacher(BaseView):
#     @expose('/',methods=['GET', 'POST'])
#     def register_teacher(self):
#         form = RegistrationForm()
#
#         if form.validate_on_submit():
#             hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#             user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,password=hashed_pw, role='TEACHER')
#             teacher = Teacher()
#             db.session.add(user)
#             db.session.add(teacher)
#             db.session.commit()
#             teacher.id = user.id
#             db.session.commit()
#             os.mkdir(app.root_path + '/static/data/teachers/' + user.first_name + '_' + user.email)
#             flash('Account created for {}!'.format(form.first_name.data), 'success')
#             return self.render('register_teacher.html',form=form)
#
#         return self.render('register_teacher.html',form=form)
#
# class TeacherView(ModelView):
#     column_list = ('id','image_file')
#     can_create = False
#
# class StudentView(ModelView):
#     column_list = ('id','image_file')
#     can_create = False
#
# class CourseView(ModelView):
#     column_list = ('id','course_name','course_code')
#
# class StudentTeacherCourseView(ModelView):
#     pass
#
# class UserView(ModelView):
#     can_create = False
# class TeacherCourseView(ModelView):
#     can_create = False
#     column_list = ('id','teacher_id','course_id')
#
# admin.add_view(RegisterTeacher(name='Register Teacher', endpoint='register_teacher'))
# admin.add_view(TeacherView(Teacher,db.session))
# admin.add_view(StudentView(Student,db.session))
# admin.add_view(CourseView(Course,db.session))
# admin.add_view(StudentTeacherCourseView(StudentTeacherCourse,db.session))
# admin.add_view(UserView(User,db.session))
# admin.add_view(TeacherCourseView(TeacherCourse,db.session))