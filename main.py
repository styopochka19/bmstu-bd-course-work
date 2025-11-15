from calendar import MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY
from datetime import date, datetime, timedelta
from re import match
from tkinter import ttk, Text, DISABLED, INSERT, messagebox

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from monthdelta import monthdelta
from pyodbc import connect
from tkcalendar import Calendar


class MyCalendar(Calendar):
    def __init__(self, master=None, allowed_weekdays=(MONDAY,), **kw):
        self._select_only = allowed_weekdays
        Calendar.__init__(self, master, **kw)
        if self._sel_date and not (self._sel_date.isoweekday() - 1) in allowed_weekdays:
            year, week, wday = self._sel_date.isocalendar()
            next_wday = max(allowed_weekdays, key=lambda d: (d - wday + 1) > 0) + 1
            sel_date = self.date.fromisocalendar(year, week + int(next_wday < wday), next_wday)
            self.selection_set(sel_date)

    def _display_calendar(self):
        Calendar._display_calendar(self)
        for i in range(6):
            for j in range(7):
                if j in self._select_only:
                    continue
                self._calendar[i][j].state(['disabled'])


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cal = None
        self.reg, self.auth = None, None
        self.backButton = None
        self.passLabel, self.passEntry = None, None
        self.logLabel, self.logEntry = None, None
        self.pwdLabel, self.pwdEntry = None, None
        self.surLabel, self.surEntry = None, None
        self.nameLabel, self.nameEntry = None, None
        self.patrLabel, self.patrEntry = None, None
        self.addrLabel, self.addrEntry = None, None
        self.phLabel, self.phEntry = None, None
        self.radiobutton_1, self.radiobutton_2, self.sex = None, None, None
        self.male, self.female = None, None
        self.registerButton, self.registerBox = None, None
        self.authLogLabel, self.authLogEntry = None, None
        self.authPwdLabel, self.authPwdEntry = None, None
        self.authButton, self.authBox = None, None
        self.mypass = None
        self.specializations = ['surgeon', 'neurosurgeon', 'eyesurgeon']
        self.hospMark, self.hospMarkBtn, self.hospRatingVar = None, None, None
        self.docMark, self.docMarkBtn, self.docRatingVar = None, None, None
        self.hospText, self.appText = None, None
        self.btn1, self.btn2, self.btn3, self.btn4, self.btn5 = None, None, None, None, None
        self.backBtn = None
        self.chooseDate, self.chooseTime = None, None
        self.time, self.timetable = None, None
        self.doc, self.docs = None, None
        self.cal, self.choose = None, None
        self.spec, self.specs = None, None
        connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=127.0.0.1,1433;DATABASE=kursach;UID=SA;PWD=reallyStrongPwd123'
        self.conn = connect(connection_string)
        self.cursor = self.conn.cursor()
        self.title("Запись и информация")
        self.geometry(CenterWindowToDisplay(self, 600, 520, self._get_window_scaling()))
        self.openUp1()

    def openUp1(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.title("Вход и регистрация")
        self.geometry(CenterWindowToDisplay(self, 600, 520, self._get_window_scaling()))

        # ----------------------------------------------------------------------------------------------------------------------

        self.auth = ctk.CTkButton(self,
                                  text="Войти",
                                  command=self.authentication)
        self.auth.place(relx=0.5, rely=0.4327, anchor=ctk.CENTER)

        # ----------------------------------------------------------------------------------------------------------------------

        self.reg = ctk.CTkButton(self,
                                 text="Зарегестрироваться",
                                 command=self.registration)
        self.reg.place(relx=0.5, rely=0.5673, anchor=ctk.CENTER)

        # ----------------------------------------------------------------------------------------------------------------------

    def registration(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.backButton = ctk.CTkButton(self, text="Назад", command=self.openUp1)
        self.backButton.grid(row=6, column=0, columnspan=8, padx=20, pady=20, sticky="ew")

        # ----------------------------------------------------------------------------------------------------------------------

        self.passLabel = ctk.CTkLabel(self, text="Паспорт")
        self.passLabel.grid(row=0, column=0,
                            padx=20, pady=20,
                            sticky="ew")

        self.passEntry = ctk.CTkEntry(self)
        self.passEntry.grid(row=0, column=1, columnspan=3,
                            padx=20, pady=20,
                            sticky="ew")

        # ----------------------------------------------------------------------------------------------------------------------

        self.logLabel = ctk.CTkLabel(self, text="Логин")
        self.logLabel.grid(row=1, column=0,
                           padx=20, pady=20,
                           sticky="ew")

        self.logEntry = ctk.CTkEntry(self)
        self.logEntry.grid(row=1, column=1, columnspan=3,
                           padx=20, pady=20,
                           sticky="ew")

        # ----------------------------------------------------------------------------------------------------------------------

        self.pwdLabel = ctk.CTkLabel(self, text="Пароль")
        self.pwdLabel.grid(row=2, column=0,
                           padx=20, pady=20,
                           sticky="ew")

        self.pwdEntry = ctk.CTkEntry(self)
        self.pwdEntry.grid(row=2, column=1, columnspan=3,
                           padx=20, pady=20,
                           sticky="ew")

        # ----------------------------------------------------------------------------------------------------------------------

        self.surLabel = ctk.CTkLabel(self, text="Фамилия")
        self.surLabel.grid(row=3, column=0,
                           padx=20, pady=20,
                           sticky="ew")

        self.surEntry = ctk.CTkEntry(self)
        self.surEntry.grid(row=3, column=1, columnspan=3,
                           padx=20, pady=20,
                           sticky="ew")

        # ----------------------------------------------------------------------------------------------------------------------

        self.nameLabel = ctk.CTkLabel(self, text="Имя")
        self.nameLabel.grid(row=4, column=0,
                            padx=20, pady=20,
                            sticky="ew")

        self.nameEntry = ctk.CTkEntry(self)
        self.nameEntry.grid(row=4, column=1, columnspan=3,
                            padx=20, pady=20,
                            sticky="ew")

        # ----------------------------------------------------------------------------------------------------------------------

        self.patrLabel = ctk.CTkLabel(self, text="Отчество")
        self.patrLabel.grid(row=5, column=0,
                            padx=20, pady=20,
                            sticky="ew")

        self.patrEntry = ctk.CTkEntry(self)
        self.patrEntry.grid(row=5, column=1, columnspan=3,
                            padx=20, pady=20,
                            sticky="ew")

        # ----------------------------------------------------------------------------------------------------------------------

        self.cal = Calendar(self,
                            maxdate=date.today(), selectmode='day',
                            locale='en_US',
                            date_pattern='yyyy-mm-dd',
                            disabledforeground='red',
                            cursor="hand2", background=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1],
                            selectbackground=ctk.ThemeManager.theme["CTkButton"]["fg_color"][1])
        self.cal.grid(row=0, column=4,
                      columnspan=4, rowspan=2,
                      padx=20, pady=20,
                      sticky="ew")

        # ----------------------------------------------------------------------------------------------------------------------

        self.addrLabel = ctk.CTkLabel(self, text="Адрес")
        self.addrLabel.grid(row=2, column=4,
                            padx=20, pady=20,
                            sticky="ew")

        self.addrEntry = ctk.CTkEntry(self)
        self.addrEntry.grid(row=2, column=5, columnspan=3,
                            padx=20, pady=20,
                            sticky="ew")

        # ----------------------------------------------------------------------------------------------------------------------

        self.phLabel = ctk.CTkLabel(self, text="Номер телефона")
        self.phLabel.grid(row=3, column=4,
                          padx=20, pady=20,
                          sticky="ew")

        self.phEntry = ctk.CTkEntry(self)
        self.phEntry.grid(row=3, column=5, columnspan=3,
                          padx=20, pady=20,
                          sticky="ew")

        # ----------------------------------------------------------------------------------------------------------------------

        self.sex = ctk.IntVar(self, 0)

        self.radiobutton_1 = ctk.CTkRadioButton(master=self, text="Мужчина",
                                                variable=self.sex, value=0)
        self.radiobutton_2 = ctk.CTkRadioButton(master=self, text="Женщина",
                                                variable=self.sex, value=1)

        self.radiobutton_1.grid(row=4, column=4, columnspan=2,
                                padx=20, pady=20,
                                sticky="ew")
        self.radiobutton_2.grid(row=4, column=6, columnspan=2,
                                padx=20, pady=20,
                                sticky="ew")

        # ----------------------------------------------------------------------------------------------------------------------

        self.registerButton = ctk.CTkButton(self,
                                            text="Зарегестрироваться",
                                            command=self.regPress)
        self.registerButton.grid(row=5, column=4, columnspan=4,
                                 padx=20, pady=20,
                                 sticky="ew")

        # ----------------------------------------------------------------------------------------------------------------------

    def regPress(self):
        correct = self.regTry()
        if correct:
            self.authentication()
        # else:
        #     self.registration()

    def regTry(self):
        pas = self.passEntry.get()
        log = self.logEntry.get()
        pwd = self.pwdEntry.get()
        sur = self.surEntry.get()
        name = self.nameEntry.get()
        patr = self.patrEntry.get()
        bd = self.cal.get_date()
        addr = self.addrEntry.get()
        ph = self.phEntry.get()
        sex = self.sex.get()

        correct_pas = match("(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}", str(pwd))
        correct_name = match("[A-Za-z]+", str(name))
        correct_sur = match("[A-Za-z]+", str(sur))
        correct_patr = match("[A-Za-z]+", str(patr))
        correct_ph = match("\d{11}", str(ph))

        if not pas or not log or not pwd or not sur or not name or not bd or not addr or not ph:
            messagebox.showwarning(title="Ошибка", message='Ваш пароль должен быть длиной не менее восьми символов, иметь один специальный знак, одну цифру и одну заглавную или строчную букву латинского алфавита!')
            return 0

        if not correct_pas:
            messagebox.showwarning(title="Ошибка", message='Ваш пароль должен быть длиной не менее восьми символов, иметь один специальный знак, одну цифру и одну заглавную или строчную букву латинского алфавита!')
            return 0

        if not correct_name:
            messagebox.showwarning(title="Ошибка", message="Ваше имя должно состоять только из букв латинского алфавита!")
            return 0

        if not correct_sur:
            messagebox.showwarning(title="Ошибка", message="Ваша фамилия должна состоять только из букв латинского алфавита!")
            return 0

        if not correct_patr and patr:
            messagebox.showwarning(title="Ошибка", message="Ваше отчество должно состоять только из букв латинского алфавита!")
            return 0

        if not correct_ph:
            messagebox.showwarning(title="Ошибка", message="Ваш номер телефона должен состоять из 11 цифр!")
            return 0

        if self.cursor.execute(f"select * from Patients where Patient_Passport = '{pas}'").fetchall():
            messagebox.showwarning(title="Ошибка", message="Вы уже зарегестрированы!")
            return 0
        if self.cursor.execute(f"select * from Patients where Patient_Login = '{log}'").fetchall():
            messagebox.showwarning(title="Ошибка", message="Этот логин уже занят!")
            return 0

        if not patr:
            try:
                print(self.cursor.execute(f'''insert into 
                Patients(Patient_Passport, Patient_Login, Patient_Password, Patient_Surname, Patient_Name, Patient_Birthdate, Patient_Address, Patient_Phone_Number, Sex_Id) 
                VALUES
                ('{pas}', '{log}', '{pwd}', '{sur}', '{name}', '{bd}', '{addr}', '{ph}', {sex});'''))
            except Exception as error:
                print(error)
        else:
            try:
                print(self.cursor.execute(f'''insert into 
                Patients(Patient_Passport, Patient_Login, Patient_Password, Patient_Surname, Patient_Name, Patient_Patronymic, Patient_Birthdate, Patient_Address, Patient_Phone_Number, Sex_Id) 
                VALUES
                ('{pas}', '{log}', '{pwd}', '{sur}', '{name}', '{patr}', '{bd}', '{addr}', '{ph}', {sex});'''))
            except Exception as error:
                print(error)

        self.cursor.commit()

        messagebox.showinfo(title="Ошибка", message="Вы успешно зарегестрировались!")
        return 1

    def authentication(self):
        for widget in self.winfo_children():
            widget.destroy()

        # ----------------------------------------------------------------------------------------------------------------------

        self.backButton = ctk.CTkButton(self,
                                        text="Назад",
                                        command=self.openUp1)
        self.backButton.place(relx=0.7333, rely=0.5583,
                              anchor=ctk.CENTER)

        # ----------------------------------------------------------------------------------------------------------------------

        self.authLogLabel = ctk.CTkLabel(self, text="Логин")
        self.authLogLabel.place(relx=0.2, rely=0.4327,
                                anchor=ctk.CENTER)

        self.authLogEntry = ctk.CTkEntry(self)
        self.authLogEntry.place(relx=0.4333, rely=0.4327,
                                anchor=ctk.CENTER)

        # ----------------------------------------------------------------------------------------------------------------------

        self.authPwdLabel = ctk.CTkLabel(self, text="Пароль")
        self.authPwdLabel.place(relx=0.2, rely=0.5583,
                                anchor=ctk.CENTER)

        self.authPwdEntry = ctk.CTkEntry(self)
        self.authPwdEntry.place(relx=0.4333, rely=0.5583,
                                anchor=ctk.CENTER)

        # ----------------------------------------------------------------------------------------------------------------------

        self.authButton = ctk.CTkButton(self,
                                        text="Войти",
                                        command=self.generateResults)
        self.authButton.place(relx=0.7333, rely=0.4327,
                              anchor=ctk.CENTER)

        # ----------------------------------------------------------------------------------------------------------------------

    def generateResults(self):
        correct = self.authTry()
        if correct:
            self.mypass = correct
            self.openUp2()
        else:
            self.authentication()

    def authTry(self):
        log = self.authLogEntry.get()
        pwd = self.authPwdEntry.get()

        correct_pwd = ''

        try:
            correct_pwd = self.cursor.execute(
                f"select Patient_Password, Patient_Passport from Patients WHERE Patient_Login = '{log}'").fetchall()
            if not correct_pwd:
                if CTkMessagebox(title="Info", message="Этого логина не существует!").get() == 'OK':
                    return 0
        except Exception as error:
            print(error)

        rows = pwd == correct_pwd[0][0]
        self.cursor.commit()

        if rows:
            msg = CTkMessagebox(title="Info", message="Аутентификация прошла успешно!")
            if msg.get():
                return correct_pwd[0][1]
            return 0
        else:
            CTkMessagebox(title="Info", message="Неверный пароль!")
            return 0

    def openUp2(self):
        for widget in self.winfo_children():
            widget.destroy()

        # ----------------------------------------------------------------------------------------------------------------------

        self.btn1 = ctk.CTkButton(self,
                                  text="Записаться на прием",
                                  command=self.appoint)
        self.btn1.pack(pady=(145, 20))

        # ----------------------------------------------------------------------------------------------------------------------

        self.btn2 = ctk.CTkButton(self,
                                  text="Мой аккаунт",
                                  command=self.myAccount)
        self.btn2.pack(pady=(0, 20))

        # ----------------------------------------------------------------------------------------------------------------------

        self.btn3 = ctk.CTkButton(self,
                                  text="Мои записи",
                                  command=self.myAppointments)
        self.btn3.pack(pady=(0, 20))

        # ----------------------------------------------------------------------------------------------------------------------

        self.btn4 = ctk.CTkButton(self,
                                  text="Мои госпитализации",
                                  command=self.myHospitalisations)
        self.btn4.pack(pady=(0, 20))

        # ----------------------------------------------------------------------------------------------------------------------

        self.btn5 = ctk.CTkButton(self,
                                  text="Выйти",
                                  command=self.logout)
        self.btn5.pack(pady=(0, 20))

        # ----------------------------------------------------------------------------------------------------------------------

    def appoint(self):
        for widget in self.winfo_children():
            widget.destroy()

        # ----------------------------------------------------------------------------------------------------------------------

        self.backBtn = ctk.CTkButton(self,
                                     text="Назад",
                                     command=self.openUp2)
        self.backBtn.pack(fill=ctk.X,
                          padx=20, pady=20)

        # ----------------------------------------------------------------------------------------------------------------------

        self.spec = ctk.StringVar(value=self.specializations[0])
        self.specs = ctk.CTkOptionMenu(self,
                                       values=self.specializations,
                                       variable=self.spec)
        self.specs.pack(fill=ctk.X, padx=20, pady=13)

        # ----------------------------------------------------------------------------------------------------------------------

        self.cal = MyCalendar(self, allowed_weekdays=(
            MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
                              mindate=date.today(), maxdate=date.today() + monthdelta(1), selectmode='day',
                              locale='en_US',
                              date_pattern='yyyy-mm-dd',
                              disabledforeground='red',
                              cursor="hand2", background=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1],
                              selectbackground=ctk.ThemeManager.theme["CTkButton"]["fg_color"][1])
        self.cal.pack(fill=ctk.X,
                      padx=20, pady=13)

        # ----------------------------------------------------------------------------------------------------------------------

        self.chooseDate = ctk.CTkButton(self,
                                        text="Выбрать дату",
                                        command=self.moveOn)
        self.chooseDate.pack(fill=ctk.X,
                             padx=20, pady=13)

    def moveOn(self):
        if self.time is not None:
            self.time.set('')
        if self.doc is not None:
            self.doc.set('')
        if self.chooseTime is not None:
            try:
                self.chooseTime.destroy()
            except Exception as error:
                print(error)
        if self.timetable is not None:
            try:
                self.timetable.destroy()
            except Exception as error:
                print(error)
        if self.docs is not None:
            try:
                self.docs.destroy()
            except Exception as error:
                print(error)

        # ----------------------------------------------------------------------------------------------------------------------

        wday = ''

        match date.fromisoformat(self.cal.get_date()).weekday():
            case 0:
                wday = 'Monday_'
            case 1:
                wday = 'Tuesday_'
            case 2:
                wday = 'Wednesday_'
            case 3:
                wday = 'Thursday_'
            case 4:
                wday = 'Friday_'

        comm = f"select Worker_Surname, Worker_Name, Worker_Patronymic, Cabinet_Number, Worker_Birthdate, Hospital_Name, t1.Worker_Passport, Average_Mark from Workers t1 join Schedule t2 on t1.Worker_Passport = t2.Worker_Passport where {wday}Start is not null and t1.Position_Name = '{self.spec.get()}'"
        doctors = self.cursor.execute(comm).fetchall()
        doc_info = []
        passports = []
        counter = 1
        for doc in doctors:
            doc_info.append(f'{counter}) ')
            passports.append(doc[6])
            for i in range(4):
                doc_info[-1] += str(doc[i]) + ' '
            doc_info[-1] += f"{(date.today() - doc[4]).days // 365} y.o., "
            doc_info[-1] += f"({str(doc[7])[:3]}) "
            hosp_info = self.cursor.execute(
                f"select Average_Mark, Adress from Hospitals WHERE Hospital_Name = '{doc[5]}'").fetchall()
            doc_info[-1] += f"{doc[5]} ({str(hosp_info[0][0])[:3]}) {hosp_info[0][1]}"
            counter += 1

        self.doc = ctk.StringVar(value='Выбрать врача')
        self.docs = ctk.CTkOptionMenu(self,
                                      values=doc_info,
                                      variable=self.doc,
                                      command=self.docWrapper(passports))
        self.docs.pack(fill=ctk.X,
                       padx=20, pady=13)

        # ----------------------------------------------------------------------------------------------------------------------

    def docWrapper(self, passes):
        def doctor_chosen(choice):
            passport = passes[int(choice.split(')')[0]) - 1]

            comm = f"select Appointment_Datetime from Appointments where Worker_Passport = '{passport}'"
            tmp = self.cursor.execute(comm).fetchall()
            reserved = []
            for i in range(len(tmp)):
                reserved.append(str(datetime.strptime(str(tmp[i][0]), '%Y-%m-%d %H:%M:%S'))[11:16])

            comm = f"select Appointment_Datetime from Appointments where Patient_Passport = '{self.mypass}'"
            tmp = self.cursor.execute(comm).fetchall()
            for i in range(len(tmp)):
                reserved.append(str(datetime.strptime(str(tmp[i][0]), '%Y-%m-%d %H:%M:%S'))[11:16])

            wday = ''

            match date.fromisoformat(self.cal.get_date()).weekday():
                case 0:
                    wday = 'Monday_'
                case 1:
                    wday = 'Tuesday_'
                case 2:
                    wday = 'Wednesday_'
                case 3:
                    wday = 'Thursday_'
                case 4:
                    wday = 'Friday_'

            comm = f"select {wday}Start, {wday}End from Schedule where Worker_Passport = '{passport}'"
            schedule = self.cursor.execute(comm).fetchall()

            start = datetime.strptime(str(schedule[0][0]), '%H:%M:%S')
            end = datetime.strptime(str(schedule[0][1]), '%H:%M:%S')

            times = []
            diff = timedelta(minutes=20)
            while start < end:
                times.append(str(start.time())[:5])
                start += diff

            times = sorted(list(set(times) - set(reserved)))

            # ----------------------------------------------------------------------------------------------------------------------

            self.time = ctk.StringVar(value='Выбрать время')
            self.timetable = ctk.CTkOptionMenu(self,
                                               values=times,
                                               variable=self.time,
                                               command=self.timeWrapper(passport))
            self.timetable.pack(fill=ctk.X,
                                padx=20, pady=13)

            # ----------------------------------------------------------------------------------------------------------------------

        return doctor_chosen

    def timeWrapper(self, passport):
        def time_chosen(choice):
            # ----------------------------------------------------------------------------------------------------------------------

            self.chooseTime = ctk.CTkButton(self,
                                            text="Записаться",
                                            command=self.recordWrapper(passport))
            self.chooseTime.pack(fill=ctk.X,
                                 padx=20, pady=13)

            # ----------------------------------------------------------------------------------------------------------------------

        return time_chosen

    def recordWrapper(self, passport):
        def record():
            comm = f"insert into Appointments(Patient_Passport, Worker_Passport, Appointment_Datetime) values ('{self.mypass}', '{passport}', '{self.cal.get_date()} {self.time.get()}')"
            self.cursor.execute(comm)
            self.cursor.commit()
            self.openUp2()

        return record

    def myAccount(self):
        for widget in self.winfo_children():
            widget.destroy()

        # ----------------------------------------------------------------------------------------------------------------------

        self.backBtn = ctk.CTkButton(self,
                                     text="Назад",
                                     command=self.openUp2)
        self.backBtn.pack(anchor="nw", fill=ctk.X,
                          padx=20, pady=20)

        # ----------------------------------------------------------------------------------------------------------------------

        comm = f"select Patient_Passport, Patient_Surname, Patient_Name, Patient_Patronymic, Patient_Birthdate, Patient_Address, Patient_Phone_Number, Sex_Id from Patients where Patient_Passport = '{self.mypass}'"
        myinfo = self.cursor.execute(comm).fetchall()

        comm = f"select Update_Date,Card_Location from Medcards where Patient_Passport = '{self.mypass}'"
        cardinfo = self.cursor.execute(comm).fetchall()

        text = f"\nПаспортные данные: {myinfo[0][0]}\nФИО: {myinfo[0][1]} {myinfo[0][2]} {myinfo[0][3]}\nДата рождения: {str(myinfo[0][4])}\nАдрес: {myinfo[0][5]}\nНомер телефона: {myinfo[0][6]}\nПол: "
        if myinfo[0][7] == 0:
            text += 'мужчина\n\n'
        else:
            text += 'женщина\n\n'

        if not cardinfo:
            height = 10
            text += 'У вас пока что нет медицинской карты'
        else:
            height = 11
            text += f"Местоположение медицинской карты: {cardinfo[0][1]}\nДата последнего обновления медкарты: {cardinfo[0][0]}"

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill=ctk.BOTH, expand=1)
        my_canvas = ctk.CTkCanvas(main_frame)
        my_canvas.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=1)
        second_frame = ctk.CTkFrame(my_canvas)
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        self.appText = Text(second_frame, height=height)
        self.appText.pack(anchor="nw",
                          padx=17, pady=20)
        self.appText.insert(INSERT, text)
        self.appText.config(state=DISABLED)

    def myAppointments(self):

        for widget in self.winfo_children():
            widget.destroy()

        # ----------------------------------------------------------------------------------------------------------------------

        self.backBtn = ctk.CTkButton(self,
                                     text="Назад",
                                     command=self.openUp2)
        self.backBtn.pack(anchor="nw", fill=ctk.X, padx=20, pady=20)

        # ----------------------------------------------------------------------------------------------------------------------

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill=ctk.BOTH, expand=1)
        my_canvas = ctk.CTkCanvas(main_frame)
        my_canvas.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=1)
        second_frame = ctk.CTkFrame(my_canvas)
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        def printRes(pas, time):
            cmd = f"select Hospital_Name, Cabinet_Number, Worker_Surname, Worker_Name, Worker_Patronymic from Workers where Worker_Passport = '{pas}'"
            app = self.cursor.execute(cmd).fetchall()
            text = f"\nБольница: {app[0][0]}\nКабинет: {app[0][1]}\nВрач: {app[0][2]} {app[0][3]} {app[0][4]}\nДата и время приёма: {str(time)[:16]}"
            self.appText = Text(second_frame, height=6)
            self.appText.pack(padx=10, pady=1)
            self.appText.insert(INSERT, text)
            self.appText.config(state=DISABLED)
            return text

        comm = f"select Worker_Passport, Appointment_Datetime from Appointments where Patient_Passport = '{self.mypass}' order by Appointment_Datetime desc"
        appointments = self.cursor.execute(comm).fetchall()

        counter = 0

        now = datetime.now()

        if appointments and appointments[counter][1] > datetime.now():
            self.appText = Text(second_frame, height=3)
            self.appText.pack(padx=10, pady=(20, 0))
            self.appText.insert(INSERT, '\nПредстоящие посещения:')
            self.appText.config(state=DISABLED)

        while counter < len(appointments):
            appTime = appointments[counter][1]
            if appTime < now:
                break
            printRes(appointments[counter][0], appTime)
            counter += 1

        if counter < len(appointments):
            self.appText = Text(second_frame, height=3)
            self.appText.pack(padx=10, pady=(20, 0))
            self.appText.insert(INSERT, '\nПрошедшие посещения:')
            self.appText.config(state=DISABLED)

        while counter < len(appointments):
            workerPass = appointments[counter][0]
            appTime = appointments[counter][1]
            printRes(workerPass, appTime)

            comm = f"select * from Worker_Review where Patient_Passport = '{self.mypass}' and Appointment_Datetime = '{appTime}'"
            rating = self.cursor.execute(comm).fetchall()
            if not rating:
                # ----------------------------------------------------------------------------------------------------------------------

                self.docRatingVar = ctk.StringVar(value='0')
                self.docMark = ctk.CTkOptionMenu(second_frame,
                                                 values=['0', '1', '2', '3', '4', '5'],
                                                 variable=self.docRatingVar)
                self.docMark.pack(anchor="nw",
                                  padx=10, pady=5)

                # ----------------------------------------------------------------------------------------------------------------------

                self.docMarkBtn = ctk.CTkButton(second_frame,
                                                text="Оценить врача",
                                                command=self.docRateWrapper(workerPass, appTime))
                self.docMarkBtn.pack(anchor="nw",
                                     padx=10, pady=5)

                # ----------------------------------------------------------------------------------------------------------------------

            comm = f"select * from Hospital_Review where Patient_Passport = '{self.mypass}' and Appointment_Datetime = '{appTime}'"
            rating = self.cursor.execute(comm).fetchall()
            if not rating:
                # ----------------------------------------------------------------------------------------------------------------------

                self.hospRatingVar = ctk.StringVar(value='0')
                self.hospMark = ctk.CTkOptionMenu(second_frame,
                                                  values=['0', '1', '2', '3', '4', '5'],
                                                  variable=self.hospRatingVar)
                self.hospMark.pack(anchor="nw",
                                   padx=10, pady=5)

                # ----------------------------------------------------------------------------------------------------------------------

                self.hospMarkBtn = ctk.CTkButton(second_frame,
                                                 text="Оценить больницу",
                                                 command=self.hospRateWrapper(appointments[counter][0], appTime))
                self.hospMarkBtn.pack(anchor="nw",
                                      padx=10, pady=5)

                # ----------------------------------------------------------------------------------------------------------------------

            counter += 1

        y_scrollbar = ctk.CTkScrollbar(main_frame, command=my_canvas.yview)
        y_scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)
        my_canvas.configure(yscrollcommand=y_scrollbar.set)
        my_canvas.bind("<Configure>", lambda e: my_canvas.config(scrollregion=my_canvas.bbox(ctk.ALL)))

    def docRateWrapper(self, pas, time):
        def rate():
            self.docMark.destroy()
            self.docMarkBtn.destroy()
            comm = f"select Amount_Of_Marks, Average_Mark from Workers where Worker_Passport = '{pas}'"
            amount, avg = self.cursor.execute(comm).fetchall()[0]

            comm = f"update Workers set Average_Mark = {(avg * amount + int(self.docRatingVar.get())) / (amount + 1)}, Amount_Of_Marks = {amount + 1} where Worker_Passport = '{pas}'"
            self.cursor.execute(comm)

            comm = f"insert into Worker_Review(Patient_Passport, Rating, Appointment_Datetime) values ('{self.mypass}', {int(self.docRatingVar.get())}, '{time}')"
            self.cursor.execute(comm)

            self.cursor.commit()

        return rate

    def hospRateWrapper(self, name, time):
        def rate():
            self.hospMark.destroy()
            self.hospMarkBtn.destroy()

            comm = f"select Amount_Of_Marks, Average_Mark from Hospitals where Hospital_Name = '{name}'"
            amount, avg = self.cursor.execute(comm).fetchall()[0]

            comm = f"update Hospitals set Average_Mark = {(avg * amount + int(self.hospRatingVar.get())) / (amount + 1)}, Amount_Of_Marks = {amount + 1} where Hospital_Name = '{name}'"
            self.cursor.execute(comm)

            comm = f"insert into Hospital_Review(Patient_Passport, Rating, Appointment_Datetime) values ('{self.mypass}', {int(self.docRatingVar.get())}, '{time}')"
            self.cursor.execute(comm)

            self.cursor.commit()

        return rate

    def myHospitalisations(self):
        for widget in self.winfo_children():
            widget.destroy()

        # ----------------------------------------------------------------------------------------------------------------------

        self.backBtn = ctk.CTkButton(self,
                                     text="Назад",
                                     command=self.openUp2)
        self.backBtn.pack(anchor="nw", fill=ctk.X,
                          padx=20, pady=20)

        # ----------------------------------------------------------------------------------------------------------------------

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill=ctk.BOTH, expand=1)
        my_canvas = ctk.CTkCanvas(main_frame)
        my_canvas.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=1)
        second_frame = ctk.CTkFrame(my_canvas)
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        comm = f"select Worker_Passport, Arrival_Date, Departure_Date from Hospitalisations where Patient_Passport = '{self.mypass}'"
        hospinfo = self.cursor.execute(comm).fetchall()
        for i in range(len(hospinfo)):
            comm = f"select Hospital_Name, Worker_Surname, Worker_name, Worker_Patronymic from Workers where Worker_Passport = '{hospinfo[i][0]}'"
            docinfo = self.cursor.execute(comm).fetchall()
            text = f"\nБольница: {docinfo[0][0]}\nЛечащий врач: {docinfo[0][1]} {docinfo[0][2]} {docinfo[0][3]}\nДата начала: {hospinfo[0][1]}\nДата окончания: {hospinfo[0][2]}"

            comm = f"select Proc_Name, Procedure_Datetime from Procedures where Patient_Passport = '{self.mypass}' and Hospitalisation_Arrival_Date = '{hospinfo[0][1]}'"
            procinfo = self.cursor.execute(comm).fetchall()

            if procinfo:
                text += '\n\n\nПроцедуры:'
            for j in range(len(procinfo)):
                text += f"\n\nНазвание: {procinfo[j][0]}\nВремя: {procinfo[j][1]}"

            height = 6
            if procinfo:
                height += 3 + len(procinfo) * 3

            self.hospText = Text(second_frame, height=height)
            self.hospText.pack(anchor="nw",
                               padx=10, pady=20)
            self.hospText.insert(INSERT, text)
            self.hospText.config(state=DISABLED)

        y_scrollbar = ctk.CTkScrollbar(main_frame, orientation='vertical', command=my_canvas.yview)
        y_scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)
        my_canvas.configure(yscrollcommand=y_scrollbar.set)
        my_canvas.bind("<Configure>", lambda e: my_canvas.config(scrollregion=my_canvas.bbox(ctk.ALL)))

    def logout(self):
        self.mypass = None
        self.openUp1()


def CenterWindowToDisplay(Screen: ctk.CTk, width, height, scale_factor=1.0):
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width / 2) - (width / 2)) * scale_factor)
    y = int(((screen_height / 2) - (height / 1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"


def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")
    app = App()
    app.resizable(width=False, height=False)
    style = ttk.Style(app)
    style.theme_use("default")
    app.mainloop()


if __name__ == "__main__":
    main()
