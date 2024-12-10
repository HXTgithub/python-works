from tkinter import *
from tkinter import messagebox
import sql
from mainPage import MainPage



class LoginPage:
    def __init__(self,master):
        self.root = master
        self.root.title('登录页面')
        self.root.geometry('300x150')
        self.page = Frame(self.root)
        self.page.pack()
        self.username = StringVar()
        self.password = StringVar()

        # 设计窗体内容：
        Label(self.page,text='账号：').grid(row=1,column=1,pady=5)
        Entry(self.page,textvariable=self.username).grid(row=1,column=2)
        Label(self.page, text='密码：').grid(row=2, column=1, pady=5)
        Entry(self.page, show='*',textvariable=self.password).grid(row=2, column=2)
        Button(self.page,text='注册',command=self.register).grid(row=3,column=1,pady=4)
        Button(self.page,text='登录',command=self.login).grid(row=3,column=2,pady=4)
        Button(self.page,text='退出',command=self.page.quit).grid(row=3,column=3,pady=4)

    def register(self):
        self.page.destroy()
        add_login(self.root)

    def login(self):
        uname = self.username.get()
        pwd = self.password.get()
        flag, message = sql.check_login(uname,pwd)
        if flag:
            self.page.pack_forget()
            MainPage(self.root)
        else: messagebox.showwarning(title= '警告',message = message)


class add_login:
    def __init__(self,master):

        self.page = master

        self.username = StringVar()
        self.passowrd = StringVar()
        self.passowrd_queren = StringVar()
        self.passowrd_root = StringVar()

        self.page.title('注册账号')
        self.page.geometry('300x200')
        self.root = Frame(self.page)
        self.root.pack()

        Label(self.root,text='账号：').grid(row = 1,column= 1)
        Entry(self.root,textvariable=self.username).grid(row=1,column=2)
        Label(self.root, text='密码：').grid(row=2, column=1)
        Entry(self.root,show='*',textvariable=self.passowrd).grid(row=2, column=2)
        Label(self.root,text='确认密码：').grid(row=3, column=1)
        Entry(self.root,show='*',textvariable=self.passowrd_queren).grid(row=3, column=2)
        Label(self.root, text='管理员密匙：').grid(row=4, column=1)
        Entry(self.root,show='*',textvariable=self.passowrd_root).grid(row=4, column=2)
        Button(self.root,text='返回',command=self.login_page).grid(row=5,column=1)
        Button(self.root,text='注册',command=self.examine).grid(row=5,column=2)

    def login_page(self):
        self.root.pack_forget()
        LoginPage(self.page)

    def examine(self):
        self.uname = self.username.get()
        self.pwd = self.passowrd.get()
        self.pwd_qr = self.passowrd_queren.get()
        self.pwd_r = self.passowrd_root.get()
        if len(self.uname) < 5:
            messagebox.showwarning(title='警告',message='账号不符合要求,请输入至少五位字符')
        elif sql.check_username(self.uname) == True:
            messagebox.showwarning(title='警告',message='该账号名已存在')
        elif len(self.pwd) < 8:
            messagebox.showwarning(title='警告',message='密码不符合要求，请输入至少八位密码')
        elif self.pwd != self.pwd_qr:
            messagebox.showwarning(title='警告',message='请保持密码与确认密码一致')
        elif self.pwd_r !='root':
            messagebox.showwarning(title='警告',message='管理员密匙错误')
        else:self.login()

    def login(self):
        sql.add_admin(self.uname,self.pwd)
        self.root.pack_forget()
        MainPage(self.page)


if __name__ == '__main__':
    page = Tk()
    LoginPage(page)
    page.mainloop()