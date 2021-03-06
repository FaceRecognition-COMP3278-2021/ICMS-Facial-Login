import urllib
import numpy as np
import mysql.connector
import cv2
import pyttsx3
import pickle
from datetime import datetime, timedelta
import sys
import PySimpleGUI as sg
import smtplib, ssl
from email.mime.text import MIMEText
import webbrowser
from os import system
"""
NOTICE:
THIS FILE IS EXACTLY SAME AS THE ICMS_APP(RUN_THIS_FILE).py, but you can test different functions changing the time and weekday.
To do so, please change the test_today and test below

BEFORE RUNNING THIS FILE:
1. Please connect to your database in this file
2. Please update the database with two queries in this directory: First, final_table(1).sql, THEN final_data(1).sql 
3. Make sure to update the database of your info using INSERT INTO QUERY
4. Please do the face_capture.py changing the name to yours (matching the name in the database)
5. Execute train.py
6. Finally you are ready to run this APP
If you have any issues please contact to Inbum CHONG, u3555335@connect.hku.hk
"""

test_today = "MON" #Later we have to use datetime.today().weekday()
test = "09:20:00" #Later we have to use datetime.now()

# 1 Create database connection
myconn = mysql.connector.connect(host="127.0.0.1", user="root", passwd="dlsqja13", database="icms")
date = datetime.utcnow()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
cursor = myconn.cursor()

# 2 Load recognize and read label from model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("train.yml")

labels = {"person_name": 1}
with open("labels.pickle", "rb") as f:
    labels = pickle.load(f)
    labels = {v: k for k, v in labels.items()}

# create text to speech
engine = pyttsx3.init()
rate = engine.getProperty("rate")
engine.setProperty("rate", 175)

# Define camera and detect face
face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

# 3 Define pysimplegui setting
sg.theme('DarkGreen5')

layout = [
            [sg.Text('3278-ICMS', font=('Helvetica', 16), justification='left')],
            [sg.Text('Welcome to ICMS!', font=('Helvetica', 12))],
            [sg.Text('Press click login if you are an existing user', font=('Helvetica', 12))],
            [sg.Button('Login'), sg.Button('Exit')]
         ]
window = sg.Window('ICMS', layout, margins=(150,50), grab_anywhere=True)

event, values = window.read()   # Read the event that happened and the values dictionary
print(event, values)
if event in (None, 'Exit'):     # If user closeddow with X or if user clicked "Exit" button then exit
    exit()
if event == 'Login':
    win_started = False
window.close()

# When "Login" is pressed --> Do the setting
if not win_started:
    win_started = True
    layout = [
        [sg.Text('Setting', size=(18, 1), font=('Helvetica', 18), justification='left')],
        [sg.Text('Confidence'),
         sg.Slider(range=(0, 100), orientation='h', resolution=1, default_value=50, size=(15, 15), key='confidence')],
        [sg.OK(), sg.Cancel()]
    ]
    win = sg.Window('Attendance System',
                    default_element_size=(21, 1),
                    text_justification='right',
                    auto_size_text=False).Layout(layout)
    event, values = win.Read()
    if event is None or event == 'Cancel':
        exit()
    args = values
    gui_confidence = args["confidence"]
    win_started = False

# 4 Open the camera and start face recognition
Switch = True
while Switch == True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

    for (x, y, w, h) in faces:
        print(x, w, y, h)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        # predict the id and confidence for faces
        id_, conf = recognizer.predict(roi_gray)

        # If the face is recognized
        if conf >= gui_confidence:
            # print(id_)
            # print(labels[id_])
            font = cv2.QT_FONT_NORMAL
            id = 0
            id += 1
            name = labels[id_]
            current_name = name
            color = (255, 0, 0)
            stroke = 2
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

            # Find the student information in the database.
            select = "SELECT log_id, name FROM Student WHERE name='%s'" % (
                name)
            name = cursor.execute(select)
            result = cursor.fetchall()

            # print(result)
            data = "error"

            for x in result:
                data = x

            # If the student's information is not found in the database
            if data == "error":
                # the student's data is not in the database
                print("The student", current_name, "is NOT FOUND in the database.")

            # If the student's information is found in the database
            else:
                print("succeeded")
                Switch = False
                """
                Implement useful functions here.
                Check the course and classroom for the student.
                    If the student has class room within one hour, the corresponding course materials
                        will be presented in the GUI.
                    if the student does not have class at the moment, the GUI presents a personal class 
                        timetable for the student.
                """

                # update = "UPDATE Student SET login_date=%s WHERE name=%s"
                # val = (date, current_name)
                # cursor.execute(update, val)
                # update = "UPDATE Student SET login_time=%s WHERE name=%s"
                # val = (current_time, current_name)
                # cursor.execute(update, val)
                # myconn.commit()
                #
                # hello = ("Hello ", current_name, "You did attendance today")
                # print(hello)
                # engine.say(hello)

        else:
            color = (255, 0, 0)
            stroke = 2
            font = cv2.QT_FONT_NORMAL
            cv2.putText(frame, "UNKNOWN", (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
            hello = ("Your face is not recognized")
            print(hello)
            engine.say(hello)
            # engine.runAndWait()

    # GUI
    imgbytes = cv2.imencode('.png', frame)[1].tobytes()
    if not win_started:
        win_started = True
        layout = [
            [sg.Text('Attendance System Interface', size=(30, 1))],
            [sg.Image(data=imgbytes, key='_IMAGE_')],
            [sg.Text('Confidence'),
             sg.Slider(range=(0, 100), orientation='h', resolution=1, default_value=50, size=(15, 15),
                       key='confidence')],
            [sg.Exit()]
        ]
        win = sg.Window('Attendance System',
                        default_element_size=(14, 1),
                        text_justification='right',
                        auto_size_text=False).Layout(layout).Finalize()
        image_elem = win.FindElement('_IMAGE_')
    else:
        image_elem.Update(data=imgbytes)

    event, values = win.Read(timeout=20)
    if event is None or event == 'Exit':
        break
    gui_confidence = values['confidence']
win.Close()
"""
After the login is successfully done,
1. Display the login succeeded page
Below are the main home features:
2. If a student has a lecture in one hour, it opens lecture info window
3. If a student has a tutorial in one hour, it opens tutorial info window
4. If a student has no class in one hour, it opens time table window
5-1. Each window have a function 1. Open Zoom Link 2.Options of add and delete courses
5-2. For windows number 2 and 3 above, it offers the function to send upcoming class info to user's email
6. For adding a new course, the selected course must be in database, the student should not enrolling the selected course,
   and should not have a time class with enrolled courses
"""
#Extracting User's student_id from the database
stu_id = "SELECT student_id FROM Student WHERE name='%s'" % (current_name)
student_id = cursor.execute(stu_id)
uid = cursor.fetchall()
for x in uid:
    sid = x

# 1. Login Succeeded Page
file_list_column = [
    [sg.Text("Welcome, " + current_name + " (" + str(sid[0]) + ") !", font=('Helvetica', 14))],
    [sg.Text("Log in time: " + current_time)],
    [sg.Button('Continue'), sg.Button('Exit')]
]
window_login = sg.Window('LoginSucceeded', file_list_column, margins=(150,50), grab_anywhere=True)

event, values = window_login.read()   # Read the event that happened and the values dictionary
if event in (None, 'Exit'):
    exit()
if event == 'Continue':
    Home = False
window_login.close()

# Getting the current day, Get start_time of lectures and tutorials
days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
a = datetime.today().weekday()
current_day = days[a]

test_2 = datetime.strptime(test, "%H:%M:%S")
test_hour = test_2.hour
test_min = test_2.minute

#Obtaining from the database
lec = "SELECT L1.lecture_id, L1.start_time, L1.end_time, L1.lecture_room, L1.online, L2.lecturer, L2.l_email_address, L3.lecture_message, L1.lecture_day FROM Lecture_time L1, Lecture L2, Lecture_message L3, Student_in_Lecture S WHERE L1.lecture_id = S.lecture_id AND L1.lecture_id = L2.lecture_id AND L2.lecture_id = L3.lecture_id AND L1.lecture_day = '%s' AND S.student_id = '%d'" % (
test_today, sid[0])
lec_2 = cursor.execute(lec)
lec_3 = cursor.fetchall()
lec_ls = []
for x in lec_3:
    lec_ls.append(x)
tut = "SELECT L1.tutorial_id, L1.start_time, L1.end_time, L1.tutorial_room, L1.online, L2.tutor, L2.t_email_address, L3.tutorial_message, L1.tutorial_day FROM Tutorial_time L1, Tutorial L2, Tutorial_message L3, Student_in_Tutorial S WHERE L1.tutorial_id = S.tutorial_id AND L1.tutorial_id = L2.tutorial_id AND L2.tutorial_id = L3.tutorial_id AND L1.tutorial_day = '%s' AND S.student_id = '%d'" % (
test_today, sid[0])
tut_2 = cursor.execute(tut)
tut_3 = cursor.fetchall()
tut_ls = []
for x in tut_3:
    tut_ls.append(x)
email = "SELECT S.email_address FROM Student S WHERE S.student_id = '%d'" % (sid[0])
email_2 = cursor.execute(email)
email_3 = cursor.fetchall()
for x in email_3:
    student_email = x

#Main Home Page
if Home == False:
    if len(lec_ls) > 0 or len(tut_ls) > 0:
        for i in range(max(len(lec_ls), len(tut_ls))):
            if len(lec_ls) > i:
                lec_f = lec_ls[i]

            if len(tut_ls) > i:
                tut_f = tut_ls[i]

            if len(lec_ls) > 0:
                upcoming_lec_name = lec_f[0]
                lec_time = str(lec_f[1])
                lec_time_2 = datetime.strptime(lec_time, "%H:%M:%S")
                lec_hour = lec_time_2.hour
                lec_min = lec_time_2.minute
                delta_hour = lec_hour - test_hour
                delta_min = lec_min - test_min

                # Main page When having a lecture
                if delta_hour == 0 and delta_min > 0 and test_today == lec_f[8]:
                    layout_lec_left = [
                        [sg.Text("ICMS HOME\n\n", font=('Helvetica', 24), justification='left')],
                        [sg.Text("You Have An Upcoming Lecture in One Hour!\n", font=('Helvetica', 18))],
                        [sg.Text(upcoming_lec_name, font=('Helvetica', 18))],
                        [sg.Text("Time: " + str(lec_f[1]) + " to" + str(lec_f[2]), font=('Helvetica', 14))],
                        [sg.Text("Venue: " + lec_f[3], font=('Helvetica', 14))],
                        [sg.Text("Zoom Link: ", font=('Helvetica', 14)), sg.Button('Link')],
                        [sg.Text("Lecturer: " + lec_f[5] + "  Lecturer's Email: " + lec_f[6], font=('Helvetica', 14))],
                        [sg.Text("Lecturer's Message: " + lec_f[7], font=('Helvetica', 14))],
                        [sg.Text("Send Above Information to Your Email: ", font=('Helvetica', 14)), sg.Button('Send')],
                    ]
                    layout_lec_right = [
                        [sg.Text("Option\n", font=('Helvetica', 20), justification='left')],
                        [sg.Text("Add new courses:", font=('Helvetica', 16))],
                        [sg.Text("[LECTURE]")],
                        [sg.Text(
                            "Please indicate academic year, course code, and semester in capital letter\nwithout space (i.e. 2021COMP3278S2)")],
                        [sg.Input()],
                        [sg.Text(
                            "Please indicate course code and subclass in capital letter\nwithout space (i.e. COMP3278B)")],
                        [sg.Input()],
                        [sg.Text("[TUTORIAL]")],
                        [sg.Text(
                            "Please indicate course code and subclass of the tutorial in capital letter\nwithout space (i.e. COMP3278BB)")],
                        [sg.Input()],
                        [sg.Button('Add', button_color=('white', 'springgreen4'), key='Add')],
                        [sg.Text("\nDelete courses:", font=('Helvetica', 16))],
                        [sg.Text(
                            "Please indicate academic year, course code, and semester in capital letter\nwithout space (i.e. 2021COMP3278S2)")],
                        [sg.Input()],
                        [sg.Button('Delete', button_color=('white', 'red'), key='Delete')],
                        [sg.Text("\n")],
                        [sg.Button('Exit', button_color=('white', 'black'), key='Exit')]
                    ]
                    layout_lec = [
                        [
                            sg.Column(layout_lec_left),
                            sg.VSeperator(),
                            sg.Column(layout_lec_right),
                        ]
                    ]
                    window_lec = sg.Window('Home_ICMS', layout_lec, margins=(200, 100), grab_anywhere=True)
                    while True:
                        event, values = window_lec.read()
                        if event in (None, 'Exit'):
                            exit()
                        if event == 'Link':
                            webbrowser.open(lec_f[4], new=1)
                        if event == 'Send':
                            text = "Dear %s\n\nThe Lecture Information You have in One Hour:\n%s\nTime: %s to %s\nVenue: %s\nZoom Link: %s\nLecturer: %s\tLecturer's Email: %s\nLecturer's Message: %s\n\n\nHave a Nice Day!\n\nFrom HKU IC Support Team" % \
                                   (current_name, upcoming_lec_name, str(lec_f[1]), str(lec_f[2]), lec_f[3], lec_f[4],
                                    lec_f[5], lec_f[6], lec_f[7])
                            sender_email = "comp3278project@gmail.com"
                            receiver_email = student_email[0]
                            password = "comp3278group"

                            message = MIMEText(text)
                            message["Subject"] = "HKU ICMS System"
                            message["From"] = sender_email
                            message["To"] = receiver_email

                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                                server.login(sender_email, password)
                                server.sendmail(
                                    sender_email, receiver_email, message.as_string()
                                )
                                print("Successfully sent email")
                        if event == 'Add':
                            add_course = (values[1], values[2], values[3])
                            con_satisfied = [False, True,
                                             True]  # 1.No such class [course, lecture, tutorial] 2.Already enrolled 3.Time Clash
                            # First Condition: No such class in all [course, lecture, tutorial]
                            cond_add1 = cursor.execute(
                                "SELECT C.course_id, L.lecture_id, T.tutorial_id FROM Course C, Lecture L, Tutorial T WHERE C.course_id = L.course_id AND C.course_id = T.course_id")
                            condition1 = cursor.fetchall()
                            for x in condition1:
                                if x == add_course:
                                    con_satisfied[0] = True
                            cond_add2 = cursor.execute(
                                "SELECT C.course_id, L.lecture_id, T.tutorial_id FROM Student_enroll_Course C, Student_in_Lecture L, Student_in_Tutorial T WHERE C.course_id = L.course_id AND C.course_id = T.course_id AND C.student_id = '%d'" % (
                                sid[0]))
                            condition2 = cursor.fetchall()
                            for x in condition2:
                                if x[0] == add_course[0] or x[1] == add_course[1] or x[2] == add_course[2]:
                                    con_satisfied[1] = False
                            cond_add3_1 = cursor.execute(
                                "SELECT start_time, end_time, lecture_day FROM Lecture_time WHERE lecture_id = '%s'" %
                                add_course[1])
                            condition3_1 = cursor.fetchall()
                            cond_add3_2 = cursor.execute(
                                "SELECT start_time, end_time, tutorial_day FROM Tutorial_time WHERE tutorial_id = '%s'" %
                                add_course[2])
                            condition3_2 = cursor.fetchall()
                            cond_add3_3 = cursor.execute(
                                "SELECT L.start_time, L.end_time, L.lecture_day FROM Student_in_Lecture S, Lecture_time L WHERE S.lecture_id = L.lecture_id AND S.student_id = '%d'" %
                                sid[0])
                            condition3_3 = cursor.fetchall()
                            cond_add3_4 = cursor.execute(
                                "SELECT L.start_time, L.end_time, L.lecture_day FROM Student_in_Lecture S, Lecture_time L WHERE S.lecture_id = L.lecture_id AND S.student_id = '%d'" %
                                sid[0])
                            condition3_4 = cursor.fetchall()
                            wishlist = []
                            mylist = []
                            for x in condition3_1:
                                wishlist.append(x)
                            for x in condition3_2:
                                wishlist.append(x)
                            for x in condition3_3:
                                mylist.append(x)
                            for x in condition3_4:
                                mylist.append(x)
                            for wish in wishlist:
                                for my in mylist:
                                    for i in range(int(wish[0].seconds / 3600 * 2),
                                                   int((wish[1].seconds + 600) / 3600 * 2)):
                                        if i >= int(my[0].seconds / 3600 * 2) and i <= int(
                                                (my[1].seconds + 600) / 3600 * 2) and wish[2] == my[2]:
                                            con_satisfied[2] = False
                            if con_satisfied == [True, True, True]:
                                add_query1 = cursor.execute(
                                    "INSERT INTO Student_enroll_Course (student_id, course_id) VALUES ('%d', '%s');" % (
                                    sid[0], add_course[0]))
                                add_query2 = cursor.execute(
                                    "INSERT INTO Student_in_Lecture (student_id, course_id, lecture_id) VALUES ('%d', '%s', '%s');" % (
                                        sid[0], add_course[0], add_course[1]))
                                add_query3 = cursor.execute(
                                    "INSERT INTO Student_in_Tutorial (student_id, course_id, tutorial_id) VALUES ('%d', '%s', '%s');" % (
                                        sid[0], add_course[0], add_course[2]))
                                myconn.commit()
                                print(add_course[0] + " is added to your database!")
                            if con_satisfied[0] == False:
                                print("Possible ERROR 1: It seems that such course does not exist.")
                            if con_satisfied[1] == False:
                                print("Possible ERROR 2: You already enrolled in this course")
                            if con_satisfied[2] == False:
                                print("Possible ERROR 3: Time Clash!")
                        if event == 'Delete':
                            del_course = values[4]
                            cond_del = cursor.execute(
                                "SELECT course_id FROM Student_enroll_Course WHERE student_id = '%d'" % (sid[0]))
                            cond_del2 = cursor.fetchall()
                            no_such_lec = True
                            for x in cond_del2:
                                if del_course == x:
                                    no_such_lec = False
                            if no_such_lec:
                                del_query1 = cursor.execute(
                                    "DELETE FROM Student_enroll_Course WHERE student_id = '%d' AND course_id = '%s'" % (
                                    sid[0], del_course))
                                del_query2 = cursor.execute(
                                    "DELETE FROM Student_in_Lecture WHERE student_id = '%d' AND course_id = '%s'" % (
                                        sid[0], del_course))
                                del_query3 = cursor.execute(
                                    "DELETE FROM Student_in_Tutorial WHERE student_id = '%d' AND course_id = '%s'" % (
                                        sid[0], del_course))
                                myconn.commit()
                                print(del_course + " is removed from your database!")
                            elif no_such_lec == False:
                                print("Check your input again!\nOr seems you are not enrolling this course")
                    window_lec.close()
                else:
                    continue

            if len(tut_ls) > 0:
                upcoming_tut_name = tut_f[0]
                tut_time = str(tut_f[1])
                tut_time_2 = datetime.strptime(tut_time, "%H:%M:%S")
                tut_hour = tut_time_2.hour
                tut_min = tut_time_2.minute
                delta2_hour = tut_hour - test_hour
                delta2_min = tut_min - test_min

                # 3. Main Page When having a tutorial
                if delta2_hour == 0 and delta2_min > 0 and test_today == tut_f[8]:
                    layout_tut_left = [
                        [sg.Text("ICMS HOME\n\n", font=('Helvetica', 24), justification='left')],
                        [sg.Text("You Have An Upcoming Tutorial in One Hour!\n", font=('Helvetica', 18))],
                        [sg.Text(upcoming_tut_name, font=('Helvetica', 18))],
                        [sg.Text("Time: " + str(tut_f[1]) + " to" + str(tut_f[2]), font=('Helvetica', 14))],
                        [sg.Text("Venue: " + tut_f[3], font=('Helvetica', 14))],
                        [sg.Text("Zoom Link: ", font=('Helvetica', 14)), sg.Button('Link')],
                        [sg.Text("Lecturer: " + tut_f[5] + "  Lecturer's Email: " + tut_f[6], font=('Helvetica', 14))],
                        [sg.Text("Lecturer's Message: " + tut_f[7], font=('Helvetica', 14))],
                        [sg.Text("Send Above Information to Your Email: ", font=('Helvetica', 14)), sg.Button('Send')],
                    ]
                    layout_tut_right = [
                        [sg.Text("Option\n", font=('Helvetica', 20), justification='left')],
                        [sg.Text("Add new courses:", font=('Helvetica', 16))],
                        [sg.Text("[LECTURE]")],
                        [sg.Text(
                            "Please indicate academic year, course code, and semester in capital letter\nwithout space (i.e. 2021COMP3278S2)")],
                        [sg.Input()],
                        [sg.Text(
                            "Please indicate course code and subclass in capital letter\nwithout space (i.e. COMP3278B)")],
                        [sg.Input()],
                        [sg.Text("[TUTORIAL]")],
                        [sg.Text(
                            "Please indicate course code and subclass of the tutorial in capital letter\nwithout space (i.e. COMP3278BB)")],
                        [sg.Input()],
                        [sg.Button('Add', button_color=('white', 'springgreen4'), key='Add')],
                        [sg.Text("\nDelete courses:", font=('Helvetica', 16))],
                        [sg.Text(
                            "Please indicate academic year, course code, and semester in capital letter\nwithout space (i.e. 2021COMP3278S2)")],
                        [sg.Input()],
                        [sg.Button('Delete', button_color=('white', 'red'), key='Delete')],
                        [sg.Text("\n")],
                        [sg.Button('Exit', button_color=('white', 'black'), key='Exit')]
                    ]
                    layout_tut = [
                        [
                            sg.Column(layout_tut_left),
                            sg.VSeperator(),
                            sg.Column(layout_tut_right),
                        ]
                    ]
                    window_tut = sg.Window('Home_ICMS', layout_tut, margins=(200, 100), grab_anywhere=True)
                    while True:
                        event, values = window_tut.read()
                        if event in (None, 'Exit'):
                            exit()
                        if event == 'Link':
                            webbrowser.open(tut_f[4], new=1)
                        if event == 'Send':
                            text = "Dear %s,\n\nThe Tutorial Information You have in One Hour:\n%s\nTime: %s to %s\nVenue: %s\nZoom Link: %s\nTutor: %s\tTutor's Email: %s\nTutor's Message: %s\n\n\nHave a Nice Day!\n\nFrom HKU IC Support Team" % \
                                   (current_name, upcoming_tut_name, str(tut_f[1]), str(tut_f[2]), tut_f[3], tut_f[4],
                                    tut_f[5], tut_f[6], tut_f[7])
                            sender_email = "comp3278project@gmail.com"
                            receiver_email = student_email[0]
                            password = "comp3278group"

                            message = MIMEText(text)
                            message["Subject"] = "HKU ICMS System"
                            message["From"] = sender_email
                            message["To"] = receiver_email

                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                                server.login(sender_email, password)
                                server.sendmail(
                                    sender_email, receiver_email, message.as_string()
                                )
                                print("Successfully sent email")
                        if event == 'Add':
                            add_course = (values[1], values[2], values[3])
                            con_satisfied = [False, True,
                                             True]  # 1.No such class [course, lecture, tutorial] 2.Already enrolled 3.Time Clash
                            # First Condition: No such class in all [course, lecture, tutorial]
                            cond_add1 = cursor.execute(
                                "SELECT C.course_id, L.lecture_id, T.tutorial_id FROM Course C, Lecture L, Tutorial T WHERE C.course_id = L.course_id AND C.course_id = T.course_id")
                            condition1 = cursor.fetchall()
                            for x in condition1:
                                if x == add_course:
                                    con_satisfied[0] = True
                            cond_add2 = cursor.execute(
                                "SELECT C.course_id, L.lecture_id, T.tutorial_id FROM Student_enroll_Course C, Student_in_Lecture L, Student_in_Tutorial T WHERE C.course_id = L.course_id AND C.course_id = T.course_id AND C.student_id = '%d'" % (
                                sid[0]))
                            condition2 = cursor.fetchall()
                            for x in condition2:
                                if x[0] == add_course[0] or x[1] == add_course[1] or x[2] == add_course[2]:
                                    con_satisfied[1] = False
                            cond_add3_1 = cursor.execute(
                                "SELECT start_time, end_time, lecture_day FROM Lecture_time WHERE lecture_id = '%s'" %
                                add_course[1])
                            condition3_1 = cursor.fetchall()
                            cond_add3_2 = cursor.execute(
                                "SELECT start_time, end_time, tutorial_day FROM Tutorial_time WHERE tutorial_id = '%s'" %
                                add_course[2])
                            condition3_2 = cursor.fetchall()
                            cond_add3_3 = cursor.execute(
                                "SELECT L.start_time, L.end_time, L.lecture_day FROM Student_in_Lecture S, Lecture_time L WHERE S.lecture_id = L.lecture_id AND S.student_id = '%d'" %
                                sid[0])
                            condition3_3 = cursor.fetchall()
                            cond_add3_4 = cursor.execute(
                                "SELECT L.start_time, L.end_time, L.lecture_day FROM Student_in_Lecture S, Lecture_time L WHERE S.lecture_id = L.lecture_id AND S.student_id = '%d'" %
                                sid[0])
                            condition3_4 = cursor.fetchall()
                            wishlist = []
                            mylist = []
                            for x in condition3_1:
                                wishlist.append(x)
                            for x in condition3_2:
                                wishlist.append(x)
                            for x in condition3_3:
                                mylist.append(x)
                            for x in condition3_4:
                                mylist.append(x)
                            for wish in wishlist:
                                for my in mylist:
                                    for i in range(int(wish[0].seconds / 3600 * 2),
                                                   int((wish[1].seconds + 600) / 3600 * 2)):
                                        if i >= int(my[0].seconds / 3600 * 2) and i <= int(
                                                (my[1].seconds + 600) / 3600 * 2) and wish[2] == my[2]:
                                            con_satisfied[2] = False
                            if con_satisfied == [True, True, True]:
                                add_query1 = cursor.execute(
                                    "INSERT INTO Student_enroll_Course (student_id, course_id) VALUES ('%d', '%s');" % (
                                    sid[0], add_course[0]))
                                add_query2 = cursor.execute(
                                    "INSERT INTO Student_in_Lecture (student_id, course_id, lecture_id) VALUES ('%d', '%s', '%s');" % (
                                        sid[0], add_course[0], add_course[1]))
                                add_query3 = cursor.execute(
                                    "INSERT INTO Student_in_Tutorial (student_id, course_id, tutorial_id) VALUES ('%d', '%s', '%s');" % (
                                        sid[0], add_course[0], add_course[2]))
                                myconn.commit()
                                print(add_course[0] + " is added to your database!")
                            if con_satisfied[0] == False:
                                print("Possible ERROR 1: It seems that such course does not exist.")
                            if con_satisfied[1] == False:
                                print("Possible ERROR 2: You already enrolled in this course")
                            if con_satisfied[2] == False:
                                print("Possible ERROR 3: Time Clash!")
                        if event == 'Delete':
                            del_course = values[4]
                            cond_del = cursor.execute(
                                "SELECT course_id FROM Student_enroll_Course WHERE student_id = '%d'" % (sid[0]))
                            cond_del2 = cursor.fetchall()
                            no_such_lec = True
                            for x in cond_del2:
                                if del_course == x:
                                    no_such_lec = False
                            if no_such_lec:
                                del_query1 = cursor.execute(
                                    "DELETE FROM Student_enroll_Course WHERE student_id = '%d' AND course_id = '%s'" % (
                                    sid[0], del_course))
                                del_query2 = cursor.execute(
                                    "DELETE FROM Student_in_Lecture WHERE student_id = '%d' AND course_id = '%s'" % (
                                        sid[0], del_course))
                                del_query3 = cursor.execute(
                                    "DELETE FROM Student_in_Tutorial WHERE student_id = '%d' AND course_id = '%s'" % (
                                        sid[0], del_course))
                                myconn.commit()
                                print(del_course + " is removed from your database!")
                            elif no_such_lec == False:
                                print("Check your input again!\nOr seems you are not enrolling this course")
                    window_tut.close()
                else:
                    continue

    # If no class in one hour
    if (len(lec_ls) == 0 and len(tut_ls) == 0) or (len(lec_ls) > 0 or len(tut_ls) > 0):
        timetable = "Timetable\nWeekday\tStart\tEnd\tCourse\t\tType\n"

        select_stmt = "SELECT L.lecture_day, L.start_time, L.end_time, L.course_id FROM Lecture_time L, Student_in_Lecture S WHERE L.lecture_id=S.lecture_id AND S.student_id='%d'" % \
                      sid[0]
        cursor.execute(select_stmt)
        lecture_tuples_list = cursor.fetchall()

        select_stmt = "SELECT T.tutorial_day, T.start_time, T.end_time, T.course_id FROM Tutorial_time T, Student_in_Tutorial S WHERE T.tutorial_id=S.tutorial_id AND S.student_id='%d'" % \
                      sid[0]
        cursor.execute(select_stmt)
        tutorial_tuples_list = cursor.fetchall()

        tuples_list = []
        for row in lecture_tuples_list:
            tuples_list.append(row)
        for row in tutorial_tuples_list:
            tuples_list.append(row)

        sorted_tuples_list = []
        days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        for day in days:
            for row in tuples_list:
                if row[0] == day:
                    sorted_tuples_list.append(row)

        for row in sorted_tuples_list:
            for i in range(len(row)):
                if i == 0:
                    timetable += row[i] + '\t'
                elif i == len(row) - 1:
                    timetable += row[i][4:12] + '\t'

                    if tuples_list.index(row) <= len(lecture_tuples_list) - 1:
                        timetable += "Lecture" + '\n'
                    else:
                        timetable += "Tutorial" + '\n'
                else:
                    timetable += str(row[i]) + '\t'
        layout_tt_left = [
            [sg.Text("ICMS HOME\n\n", font=('Helvetica', 24), justification='left')],
            [sg.Text("You Have No Upcoming Lecture in One Hour!\n\n", font=('Helvetica', 18))],
            [sg.Text(timetable, font=('Helvetica', 14))]
        ]
        layout_tt_right = [
            [sg.Text("Option\n", font=('Helvetica', 20), justification='left')],
            [sg.Text("Add new courses:", font=('Helvetica', 16))],
            [sg.Text("[LECTURE]")],
            [sg.Text(
                "Please indicate academic year, course code, and semester in capital letter\nwithout space (i.e. 2021COMP3278S2)")],
            [sg.Input()],
            [sg.Text("Please indicate course code and subclass in capital letter\nwithout space (i.e. COMP3278B)")],
            [sg.Input()],
            [sg.Text("[TUTORIAL]")],
            [sg.Text(
                "Please indicate course code and subclass of the tutorial in capital letter\nwithout space (i.e. COMP3278BB)")],
            [sg.Input()],
            [sg.Button('Add', button_color=('white', 'springgreen4'), key='Add')],
            [sg.Text("\nDelete courses:", font=('Helvetica', 16))],
            [sg.Text(
                "Please indicate academic year, course code, and semester in capital letter\nwithout space (i.e. 2021COMP3278S2)")],
            [sg.Input()],
            [sg.Button('Delete', button_color=('white', 'red'), key='Delete')],
            [sg.Text("\n")],
            [sg.Button('Exit', button_color=('white', 'black'), key='Exit')]
        ]
        layout_tt = [
            [
                sg.Column(layout_tt_left),
                sg.VSeperator(),
                sg.Column(layout_tt_right),
            ]
        ]
        window_tt = sg.Window('Home_ICMS', layout_tt, margins=(200, 100), grab_anywhere=True)
        while True:
            event, values = window_tt.read()
            if event in (None, 'Exit'):
                exit()
            if event == 'Add':
                add_course = (values[1], values[2], values[3])
                con_satisfied = [False, True,
                                 True]  # 1.No such class [course, lecture, tutorial] 2.Already enrolled 3.Time Clash
                # First Condition: No such class in all [course, lecture, tutorial]
                cond_add1 = cursor.execute(
                    "SELECT C.course_id, L.lecture_id, T.tutorial_id FROM Course C, Lecture L, Tutorial T WHERE C.course_id = L.course_id AND C.course_id = T.course_id")
                condition1 = cursor.fetchall()
                for x in condition1:
                    if x == add_course:
                        con_satisfied[0] = True
                cond_add2 = cursor.execute(
                    "SELECT C.course_id, L.lecture_id, T.tutorial_id FROM Student_enroll_Course C, Student_in_Lecture L, Student_in_Tutorial T WHERE C.course_id = L.course_id AND C.course_id = T.course_id AND C.student_id = '%d'" % (
                        sid[0]))
                condition2 = cursor.fetchall()
                for x in condition2:
                    if x[0] == add_course[0] or x[1] == add_course[1] or x[2] == add_course[2]:
                        con_satisfied[1] = False
                cond_add3_1 = cursor.execute(
                    "SELECT start_time, end_time, lecture_day FROM Lecture_time WHERE lecture_id = '%s'" %
                    add_course[1])
                condition3_1 = cursor.fetchall()
                cond_add3_2 = cursor.execute(
                    "SELECT start_time, end_time, tutorial_day FROM Tutorial_time WHERE tutorial_id = '%s'" %
                    add_course[2])
                condition3_2 = cursor.fetchall()
                cond_add3_3 = cursor.execute(
                    "SELECT L.start_time, L.end_time, L.lecture_day FROM Student_in_Lecture S, Lecture_time L WHERE S.lecture_id = L.lecture_id AND S.student_id = '%d'" %
                    sid[0])
                condition3_3 = cursor.fetchall()
                cond_add3_4 = cursor.execute(
                    "SELECT L.start_time, L.end_time, L.lecture_day FROM Student_in_Lecture S, Lecture_time L WHERE S.lecture_id = L.lecture_id AND S.student_id = '%d'" %
                    sid[0])
                condition3_4 = cursor.fetchall()
                wishlist = []
                mylist = []
                for x in condition3_1:
                    wishlist.append(x)
                for x in condition3_2:
                    wishlist.append(x)
                for x in condition3_3:
                    mylist.append(x)
                for x in condition3_4:
                    mylist.append(x)
                for wish in wishlist:
                    for my in mylist:
                        for i in range(int(wish[0].seconds / 3600 * 2), int((wish[1].seconds + 600) / 3600 * 2)):
                            if i >= int(my[0].seconds / 3600 * 2) and i <= int((my[1].seconds + 600) / 3600 * 2) and \
                                    wish[2] == my[2]:
                                con_satisfied[2] = False
                if con_satisfied == [True, True, True]:
                    add_query1 = cursor.execute(
                        "INSERT INTO Student_enroll_Course (student_id, course_id) VALUES ('%d', '%s');" % (
                            sid[0], add_course[0]))
                    add_query2 = cursor.execute(
                        "INSERT INTO Student_in_Lecture (student_id, course_id, lecture_id) VALUES ('%d', '%s', '%s');" % (
                            sid[0], add_course[0], add_course[1]))
                    add_query3 = cursor.execute(
                        "INSERT INTO Student_in_Tutorial (student_id, course_id, tutorial_id) VALUES ('%d', '%s', '%s');" % (
                            sid[0], add_course[0], add_course[2]))
                    myconn.commit()
                    print(add_course[0] + " is added to your database!")
                if con_satisfied[0] == False:
                    print("Possible ERROR 1: It seems that such course does not exist.")
                if con_satisfied[1] == False:
                    print("Possible ERROR 2: You already enrolled in this course")
                if con_satisfied[2] == False:
                    print("Possible ERROR 3: Time Clash!")
            if event == 'Delete':
                del_course = values[4]
                cond_del = cursor.execute(
                    "SELECT course_id FROM Student_enroll_Course WHERE student_id = '%d'" % (sid[0]))
                cond_del2 = cursor.fetchall()
                no_such_lec = True
                for x in cond_del2:
                    if del_course == x:
                        no_such_lec = False
                if no_such_lec:
                    del_query1 = cursor.execute(
                        "DELETE FROM Student_enroll_Course WHERE student_id = '%d' AND course_id = '%s'" % (
                            sid[0], del_course))
                    del_query2 = cursor.execute(
                        "DELETE FROM Student_in_Lecture WHERE student_id = '%d' AND course_id = '%s'" % (
                            sid[0], del_course))
                    del_query3 = cursor.execute(
                        "DELETE FROM Student_in_Tutorial WHERE student_id = '%d' AND course_id = '%s'" % (
                            sid[0], del_course))
                    myconn.commit()
                    print(del_course + " is removed from your database!")
                elif no_such_lec == False:
                    print("Check your input again!\nOr seems you are not enrolling this course")
        window_tt.close()

# cap.release()