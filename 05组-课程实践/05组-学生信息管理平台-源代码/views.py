from tkinter import *
from tkinter import ttk
import sql
from tkinter import messagebox


class InsertFrame(Frame):
    def __init__(self,root):
        super().__init__(root)
        self.id = StringVar()
        self.name = StringVar()
        self.class1 = StringVar()
        self.math = StringVar()
        self.english = StringVar()
        self.computer = StringVar()

        self.status_insert = StringVar()
        self.insert_page()


    def insert_page(self):
        Label(self,text='学号：').grid(row=1,column=1,pady=5)
        self.entry_id = Entry(self,textvariable=self.id)
        self.entry_id.grid(row=1,column=2,pady=5)
        Label(self, text='姓名：').grid(row=2, column=1, pady=5)
        self.entry_name = Entry(self, textvariable=self.name)
        self.entry_name.grid(row=2, column=2, pady=5)
        Label(self, text='班级：').grid(row=3, column=1, pady=5)
        self.entry_class = Entry(self, textvariable=self.class1)
        self.entry_class.grid(row=3, column=2, pady=5)
        Label(self, text='数学：').grid(row=4, column=1, pady=5)
        self.entry_math = Entry(self, textvariable=self.math)
        self.entry_math.grid(row=4, column=2, pady=5)
        Label(self, text='英语：').grid(row=5, column=1, pady=5)
        self.entry_english = Entry(self, textvariable=self.english)
        self.entry_english.grid(row=5, column=2, pady=5)
        Label(self, text='计算机：').grid(row=6, column=1, pady=5)
        self.entry_com = Entry(self, textvariable=self.computer)
        self.entry_com.grid(row=6, column=2, pady=5)

        Button(self,text='清空',command=self.insert_clear).grid(row=7,column=1,pady=10)
        Button(self,text='录入',command=self.insert_data).grid(row=7,column=3,pady=10)

        Label(self,textvariable=self.status_insert).grid(row=8,column=2,padx=10)


    def insert_data(self):
        if not self.id.get():
            self.insert_id=int(0)
        else:
            self.insert_id=int(self.id.get())

        if not self.name.get():
            self.insert_name='NULL'
        else:
            self.insert_name=self.name.get()

        if not self.class1.get():
            self.insert_class='NULL'
        else:
            self.insert_class=self.class1.get()

        if not self.math.get():
            self.insert_math=int(0)
        else:
            self.insert_math=int(self.math.get())

        if not self.english.get():
            self.insert_english=int(0)
        else:
            self.insert_english=int(self.english.get())

        if not self.computer.get():
            self.insert_computer=int(0)
        else:
            self.insert_computer=int(self.computer.get())

        flag,s = sql.check_id(self.insert_id)
        self.status_insert.set(s)
        if flag == False:
            return
        self.insert_total = self.insert_math + self.insert_computer + self.insert_english
        stu = (self.insert_id,self.insert_name,self.insert_class,self.insert_math,self.insert_english
               ,self.insert_computer,self.insert_total)
        sql.insert(stu)


    def insert_clear(self):
        self.entry_id.delete(0,END)
        self.entry_name.delete(0,END)
        self.entry_class.delete(0,END)
        self.entry_math.delete(0,END)
        self.entry_english.delete(0,END)
        self.entry_com.delete(0,END)


class SearchFrame(Frame):
    def __init__(self,root):
        super().__init__(root)

        self.table_search=Frame()
        self.show_table()

    def show_table(self):
        columns = ("id","name","class1","math","english","computer","total")
        columns_values = ("学号","姓名","班级","数学","英语","计算机","总分")
        self.tree_view = ttk.Treeview(self,show='headings',columns = columns)

        for col in columns:
            self.tree_view.column(col,width=80,anchor='center')

        for col,colvalue in zip(columns,columns_values):
            self.tree_view.heading(col,text=colvalue)

        self.tree_view.pack(fill = BOTH,expand = True)
        self.show_search()

        self.class_class = StringVar()
        Entry(self,textvariable=self.class_class).pack(side = LEFT)
        Button(self,text='按班查询',command=self.search_class).pack(side=LEFT)
        Button(self,text='删除',command=self.treeviewClick).pack(side = RIGHT)

        def treeview_sort_column1(tv,col,reverse):
            l = [(tv.set(k,col),k) for k in tv.get_children('')]
            l.sort(key=lambda t:int(t[0]),reverse=reverse)
            for index,(val,k) in enumerate(l):
                tv.move(k,'',index)
            tv.heading(col, command=lambda:treeview_sort_column1(tv,col,not reverse))
            self.tree_color()

        def treeview_sort_column2(tv,col,reverse):
            l = [(tv.set(k,col),k) for k in tv.get_children('')]
            l.sort(reverse=reverse)
            for index,(val,k) in enumerate(l):
                tv.move(k,'',index)
            tv.heading(col,command=lambda: treeview_sort_column2(tv,col,not reverse))
            self.tree_color()

        for i in range(7):
            if i >=1 and i<=2:
                self.tree_view.heading(columns[i],text=columns_values[i],
                                       command=lambda _col=columns[i]: treeview_sort_column2(self.tree_view,_col,
                                                                                             False))
            else:
                self.tree_view.heading(columns[i], text=columns_values[i],
                                       command=lambda _col=columns[i]: treeview_sort_column2(self.tree_view, _col,
                                                                                             False))
        self.tree_view.tag_configure('even',background='lightblue')


    def search_class(self):
        for _ in map(self.tree_view.delete, self.tree_view.get_children('')):
            pass
        if not self.class_class.get():
            self.show_search()
            return
        else:
            self.class_value = self.class_class.get()
            students = sql.search_class(self.class_value)

        index = -1
        for stu in students:
            self.tree_view.insert('',index + 1,values=
            (stu['id'],stu['name'],stu['class'],stu['math'],
            stu['english'],stu['computer'],stu['total']
            ))
        self.tree_color()

    def treeviewClick(self):
        for item in self.tree_view.selection():
            item_text = self.tree_view.item(item,'values')
            sql.delete_id(item_text[0])
            self.show_search()

    def show_search(self):

        for _ in map(self.tree_view.delete,self.tree_view.get_children('')):
            pass
        students = sql.all()
        index = -1
        for stu in students:
            self.tree_view.insert('',index + 1,values=(
                stu['id'],stu['name'],stu['class'],stu['math'],
                stu['english'],stu['computer'],stu['total']
            ))
        self.tree_color()

    def tree_color(self):
        items = self.tree_view.get_children()
        i = 0
        for hiid in items:
            if i/2 != int(i/2):
                tag1=''
            else:
                tag1 = 'even'
            self.tree_view.item(hiid,tag=tag1)
            i += 1


class DeleteFrame(Frame):
    def __init__(self,root):
        super().__init__(root,width = 570,height = 290)

        self.delete_student = StringVar()
        self.status_student = StringVar()

        Label(self,text='请输入需要删除学生的').place(x = 40,y = 60)
        Label(self,text='姓名或者学号').place(x = 64,y = 80)
        Entry(self,textvariable=self.delete_student).place(x = 30,y = 100)
        Button(self,text='按学号查询',command=self.id_delete).place(x = 30,y = 130)
        Button(self,text='按姓名查询',command=self.name_delete).place(x = 110,y = 130)
        Label(self,textvariable=self.status_student).place(x = 45,y = 160)

        self.id = StringVar()
        self.name = StringVar()
        self.class1 = StringVar()
        self.math = StringVar()
        self.english = StringVar()
        self.computer = StringVar()

        Label(self,text='学号：').place(x=300,y=20)
        Label(self,textvariable=self.id).place(x=360,y=20)
        Label(self,text='姓名：').place(x=300,y=50)
        Label(self,textvariable=self.name).place(x=360,y=50)
        Label(self,text='班级：').place(x=300,y=80)
        Label(self,textvariable=self.class1).place(x=360,y=80)
        Label(self,text='数学：').place(x=300,y=110)
        Label(self,textvariable=self.math).place(x=360,y=110)
        Label(self,text='英语：').place(x=300,y=140)
        Label(self,textvariable=self.english).place(x=360,y=140)
        Label(self,text='计算机：').place(x=300,y=170)
        Label(self,textvariable=self.computer).place(x=360,y=170)

        self.status_delete = StringVar()
        Button(self,text='删除',command=self.delete_stu).place(x=340,y=210)
        Label(self,textvariable=self.status_delete).place(x=300,y=250)


    def id_delete(self):
        if self.delete_student.get():
            self.search_user_id = self.delete_student.get()
            flag,stu = sql.search_id(self.search_user_id)
            if flag:
                self.id.set(stu[0][0]),self.name.set(stu[0][1])
                self.class1.set(stu[0][2]),self.math.set(stu[0][3])
                self.english.set(stu[0][4]),self.computer.set(stu[0][5])
                self.status_student.set('数据查询成功')
            else:
                self.status_student.set(stu)
        else:
            self.status_student.set('请输入需要查询的信息')

    def name_delete(self):
        if self.delete_student.get():
            self.search_user_name = self.delete_student.get()
            flag,stu = sql.search_name(self.search_user_name)
            if flag:
                self.id.set(stu[0][0])
                self.name.set(stu[0][1])
                self.class1.set(stu[0][2])
                self.math.set(stu[0][3])
                self.english.set(stu[0][4])
                self.computer.set(stu[0][5])
                self.status_student.set('数据查询成功')
            else:
                self.status_student.set(stu)

        else:
            self.status_student.set('请输入需要查询的信息')

    def delete_stu(self):
        flag,str = sql.delete_id(self.id.get())
        if not self.id.get():
            str = '需要删除信息不能为NULL'
        self.status_delete.set(str)


class ChangeFrame(Frame):
    def __init__(self,root):
        super().__init__(root,width=570,height = 290)
        self.change_student = StringVar()
        self.status_student = StringVar()
        self.status_name = StringVar()

        self.id = StringVar()
        self.name = StringVar()
        self.class1 = StringVar()
        self.math = StringVar()
        self.english = StringVar()
        self.computer = StringVar()

        self.id_change_before = StringVar()
        self.name_change_before = StringVar()
        self.class1_change_before = StringVar()
        self.math_change_before = StringVar()
        self.english_change_before = StringVar()
        self.computer_change_before = StringVar()

        self.insert_page()

    def insert_page(self):
        Label(self,text='请输入需要查询学生的').place(x=40,y=60)
        Label(self,text='姓名或学号').place(x=64,y=80)
        Entry(self,textvariable=self.change_student).place(x=30,y=100)
        Button(self,text='按学号查询',command=self.id_change).place(x=30,y=130)
        Button(self,text='按姓名查询',command=self.name_change).place(x=110,y=130)
        Label(self,textvariable=self.status_student).place(x=45,y=160)

        Label(self,text='学号：').place(x=240,y=20)
        Label(self,textvariable=self.id_change_before).place(x=320,y=20)
        self.entry_id = Entry(self,textvariable=self.id)
        self.entry_id.place(x=380,y=20)

        Label(self,text='姓名：').place(x=240,y=50)
        Label(self,textvariable=self.name_change_before).place(x=315,y=50)
        self.entry_name = Entry(self,textvariable=self.name)
        self.entry_name.place(x=380,y=50)

        Label(self, text='班级：').place(x=240, y=80)
        Label(self, textvariable=self.class1_change_before).place(x=315, y=80)
        self.entry_class = Entry(self, textvariable=self.class1)
        self.entry_class.place(x=380, y=80)

        Label(self, text='数学：').place(x=240, y=110)
        Label(self, textvariable=self.math_change_before).place(x=315, y=110)
        self.entry_math = Entry(self, textvariable=self.math)
        self.entry_math.place(x=380, y=110)

        Label(self, text='英语：').place(x=240, y=140)
        Label(self, textvariable=self.english_change_before).place(x=315, y=140)
        self.entry_english = Entry(self, textvariable=self.english)
        self.entry_english.place(x=380, y=140)

        Label(self, text='计算机：').place(x=240, y=170)
        Label(self, textvariable=self.computer_change_before).place(x=315, y=170)
        self.entry_computer = Entry(self, textvariable=self.computer)
        self.entry_computer.place(x=380, y=170)

        Button(self,text='修改',command=self.create_user).place(x=320,y=220)

        Label(self,textvariable=self.status_name).place(x=305,y=250)


    def id_change(self):
        if self.change_student.get():
            self.search_user_id = self.change_student.get()
            flag,stu = sql.search_id(self.search_user_id)
            if flag:
                self.change_info(stu)
                self.status_student.set('数据查询成功')
            else:
                self.status_student.set(stu)
        else:
            self.status_student.set('请输入需要查询的信息')

    def name_change(self):
        if self.change_student.get():
            self.search_user_name = self.change_student.get()
            flag,stu=sql.search_name(self.search_user_name)
            if flag:
                self.change_info(stu)
                self.status_student.set('数据查询成功')
            else:
                self.status_student.set(stu)
        else:
            self.status_student.set('请输入需要查询的信息')

    def change_info(self,stu):
        self.id.set(stu[0][0])
        self.name.set(stu[0][1])
        self.class1.set(stu[0][2])
        self.math.set(stu[0][3])
        self.english.set(stu[0][4])
        self.computer.set(stu[0][5])
        self.id_change_before.set(stu[0][0])
        self.name_change_before.set(stu[0][1])
        self.class1_change_before.set(stu[0][2])
        self.math_change_before.set(stu[0][3])
        self.english_change_before.set(stu[0][4])
        self.computer_change_before.set(stu[0][5])

    def create_user(self):
        if not self.id.get():
            self.insert_id = int(0)
            self.status_name.set('请输入修改的学号')
            return
        else:
            self.insert_id=int(self.id.get())

        if not self.name.get():
            self.insert_name = 'NULL'
        else:
            self.insert_name = self.name.get()

        if not self.class1.get():
            self.insert_class1 = 'NULL'
        else:
            self.insert_class1 = self.class1.get()

        if not self.math.get():
            self.insert_math = int(0)
        else:
            self.insert_math = int(self.math.get())

        if not self.english.get():
            self.insert_english = int(0)
        else:
            self.insert_english = int(self.english.get())

        if not self.computer.get():
            self.insert_computer = int(0)
        else:
            self.insert_computer= int(self.computer.get())
        sql.delete_id(self.id_change_before.get())
        self.insert_total = self.insert_math + self.insert_english + self.insert_computer
        stu = (self.insert_id,self.insert_name,self.insert_class1,self.insert_math,
               self.insert_english,self.insert_computer,self.insert_total)
        sql.insert(stu)

        self.status_name.set('数据修改成功')


class HelpFrame(Frame):
    def __init__(self,root):
        super().__init__(root)
        Label(self,text='关于录入界面').pack()
        Label(self, text='可以录入所有信息为空的信息，但不建议，且学号具有唯一性').pack()
        Label(self, text=' ').pack()
        Label(self, text='关于查询界面').pack()
        Label(self,text='默认为升序排列，可以根据学生的各类信息进行排列，并能通过快捷键以及鼠标右键实现一定的功能').pack()
        Label(self, text='可以查看班级信息以及可以选择信息进行删除').pack()
        Label(self, text=' ').pack()
        Label(self, text='关于删除界面').pack()
        Label(self, text='可以根据学号或者姓名对学生信息进行删除，学号是唯一的').pack()
        Label(self, text=' ').pack()
        Label(self, text='关于修改界面').pack()
        Label(self,text='可以通过学号或者姓名来查询学学生信息，但查询名字只会出现第一位学生，按下修改键出现提示即成功').pack()