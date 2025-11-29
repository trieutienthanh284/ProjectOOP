from tkinter import *
from models import Stakeholder, Employee

root = Tk()
root.title("Quản lý nhân viên")
root.minsize(height = 630, width = 650)

Label(root, text = 'Quản lý nhân viên', fg = 'red', font = ('Cambria', 20), width = 40).grid(row = 0)
listbox = Listbox(root, width = 140, height = 28)
listbox.grid(row = 1, columnspan= 2)
Label(root, text = 'Mã nhân viên').grid(row = 2, column = 0)
Entry(root, width = 30).grid(row = 2, column = 1)
Label(root, text = 'Tên').grid(row = 3, column = 0)
Entry(root, width = 30).grid(row = 3, column = 1)
Label(root, text = 'Số điện thoại').grid(row = 4, column = 0)
Entry(root, width = 30).grid(row = 4, column = 1)
Label(root, text = 'CCCD').grid(row = 5, column = 0)
Entry(root, width = 30).grid(row = 5, column = 1)
button = Frame(root)
Button(button, text = 'Thêm').pack(side = LEFT)
Button(button, text = 'Xóa').pack(side = LEFT)
Button(button, text = 'Sửa').pack(side = LEFT)
Button(button, text = 'Thoát', command = root.quit).pack(side = LEFT)
button.grid(row = 6, column = 1)


root.mainloop()