from tkinter import *
from views import ChangeFrame,DeleteFrame,InsertFrame,SearchFrame,HelpFrame
import  sql
import keyboard

class MainPage:
    def __init__(self,master):
        self.root = master
        self.root.title('学生信息管理系统')
        self.root.geometry('570x290')
        self.create_page()

    def create_page(self):
        self.insert_frame = InsertFrame(self.root)
        self.search_frame = SearchFrame(self.root)
        self.delete_frame = DeleteFrame(self.root)
        self.change_frame = ChangeFrame(self.root)
        self.help_frame = HelpFrame(self.root)

        menubar = Menu(self.root,tearoff=False)

        menubar.add_command(label='录入',command=self.show_insert)

        submenu_search = Menu(menubar)
        submenu_search.add_command(label='降序',command=self.show_ssd,accelerator="Ctrl + J")
        submenu_search.add_separator()
        submenu_search.add_command(label='学号',command=self.show_search_id,accelerator="Ctrl + J")
        submenu_search.add_command(label='总分',command=self.show_search_total,accelerator="Ctrl + T")
        submenu_search.add_command(label='数学',command=self.show_search_math,accelerator="Ctrl + M")
        submenu_search.add_command(label='英语',command=self.show_search_english,accelerator="Ctrl + E")
        submenu_search.add_command(label='计算机',command=self.show_search_computer,accelerator="Ctrl + S")

        keyboard.add_hotkey('ctrl+j',self.show_ssd)
        keyboard.add_hotkey('ctrl+d',self.show_search_id)
        keyboard.add_hotkey('ctrl+t',self.show_search_total)
        keyboard.add_hotkey('ctrl+m',self.show_search_math)
        keyboard.add_hotkey('ctrl+e',self.show_search_english)
        keyboard.add_hotkey('ctrl+s',self.show_search_computer)

        menubar.add_cascade(label='查询',menu=submenu_search)
        menubar.add_command(label='删除',command=self.show_delete)
        menubar.add_command(label='修改',command=self.show_change)
        menubar.add_command(label='帮助',command=self.show_help)
        self.root.config(menu = menubar)

        def xShowMenu(event):
            menubar.post(event.x_root,event.y_root)

        self.root.bind("<Button-3>",xShowMenu)

        self.show_insert()

    def show_ssd(self):
        sql.sort_stu ^=1
        self.show_search()

    def show_search_id(self):
        sql.sort_data = 0
        self.show_search()

    def show_search_total(self):
        sql.sort_data = 1
        self.show_search()

    def show_search_math(self):
        sql.sort_data = 2
        self.show_search()

    def show_search_english(self):
        sql.sort_data = 3
        self.show_search()

    def show_search_computer(self):
        sql.sort_data = 4
        self.show_search()

    def show_insert(self):
        self.insert_frame.pack()
        self.search_frame.pack_forget()
        self.delete_frame.pack_forget()
        self.change_frame.pack_forget()
        self.help_frame.pack_forget()

    def show_search(self):
        self.insert_frame.pack_forget()
        self.delete_frame.pack_forget()
        self.change_frame.pack_forget()
        self.help_frame.pack_forget()
        self.search_frame.pack()
        self.search_frame.show_search()

    def show_delete(self):
        self.delete_frame.pack()
        self.insert_frame.pack_forget()
        self.search_frame.pack_forget()
        self.change_frame.pack_forget()
        self.help_frame.pack_forget()

    def show_change(self):
        self.change_frame.pack()
        self.insert_frame.pack_forget()
        self.search_frame.pack_forget()
        self.delete_frame.pack_forget()
        self.help_frame.pack_forget()
    def show_help(self):
        self.change_frame.pack_forget()
        self.insert_frame.pack_forget()
        self.search_frame.pack_forget()
        self.delete_frame.pack_forget()
        self.help_frame.pack()