
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font
import tkinter.colorchooser
import tempfile
import subprocess
import getpass
import os,sys
import time

class Application(tkinter.Tk):
    COUNT=0
    INTERPRETER=None
    FILE_TYPE=(('all supported', '.*'),('text','.txt'), ('html', '.htm'), ('html', '.html'), ('bash', '.sh'), ('python', '.py'),('perl', '.pl'), ('c', '.c'), ('c++', '.cpp'), ('java', '.java'))
    def __init__(self):
        file = Application.File()
        style=Application.Style()
        compiler=Application.Interpreter()
        super().__init__()
        self.geometry('800x700')
        self.minsize(800,700)
        self.title('PROGRAMMER\'S IDE [Untitled File]')
        #todo menu collection
        file_menu = tkinter.Menu(self,tearoff=False,bg='gray',activebackground='gray')
        file_menu.add_command(label='new', command=lambda:file.newFile(self,text))
        file_menu.add_command(label='open', command=lambda:file.openFile(self,text))
        file_menu.add_command(label='save',command=lambda:file.saveFile(self,text))
        file_menu.add_command(label='save as',command=lambda:file.saveAsFile(text))
        file_menu.add_command(label='quit',command=self.destroy)
        edit_menu=tkinter.Menu(self,tearoff=False,bg='gray',activebackground='gray')
        edit_menu.add_command(label='cut', command=lambda: text.event_generate('<<Cut>>'))
        edit_menu.add_command(label='copy',command=lambda:text.event_generate('<<Copy>>'))
        edit_menu.add_command(label='paste',command=lambda:text.event_generate('<<Paste>>'))
        style_menu=tkinter.Menu(self,tearoff=False,bg='gray',activebackground='gray')
        style_menu.add_command(label='font',command=lambda :style.style(text))
        output_menu=tkinter.Menu(self,tearoff=False,bg='gray',activebackground='gray')
        output_menu.add_command(label='terminal',command=lambda:compiler.output('terminal',execute))
        output_menu.add_command(label='text',command=lambda :compiler.output('text',execute))
        main_menu=tkinter.Menu(self,bg='gray',activebackground='gray')
        main_menu.add_cascade(label='file',menu=file_menu)
        main_menu.add_cascade(label='edit',menu=edit_menu)
        main_menu.add_cascade(label='style',menu=style_menu)
        main_menu.add_cascade(label='output',menu=output_menu)
        main_menu.add_cascade()
        self.updateTime(main_menu)
        # todo text area and scrollbar
        main_frame=tkinter.Frame(self)
        scroll = tkinter.Scrollbar(main_frame)
        scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        text = tkinter.Text(main_frame,selectbackground='green',selectforeground='white',yscrollcommand=scroll.set)
        text.pack(expand=True, fill=tkinter.BOTH)
        text.focus_set()
        scroll.config(command=text.yview)
        main_frame.pack(expand=True, fill=tkinter.BOTH)
        #todo widget for interpreter
        frame=tkinter.Frame(self)
        frame.pack(fill=tkinter.X)
        interpreter=tkinter.Label(frame,text="select interpreter",fg='red',font=", 12 italic",relief=tkinter.SOLID,width=15)
        interpreter.bind('<Button-1>',lambda x:compiler.selectInterpreter(interpreter,execute))
        interpreter.pack(side=tkinter.LEFT,padx=10)
        argument_label=tkinter.Label(frame,text="argument",fg='red',font=", 12 italic")
        argument_label.pack(side=tkinter.LEFT)
        argument=tkinter.Entry(frame,highlightcolor='green',width=50)
        argument.bind('<FocusOut>',lambda event:compiler.validate(event,argument_label))
        argument.pack(side=tkinter.LEFT)
        execute=tkinter.Button(frame,text='terminal',state=tkinter.DISABLED,relief=tkinter.SOLID)
        execute.bind('<Button-1>',lambda event: compiler.execute(self,event,text,file,argument,interpreter, execute))
        execute.bind('<space>',lambda event: compiler.execute(self,event,text,file,argument,interpreter, execute))
        execute.bind('<Return>',lambda event: compiler.execute(self,event,text,file,argument,interpreter, execute))
        execute.bind('<KP_Enter>',lambda event: compiler.execute(self,event,text,file,argument,interpreter, execute))
        execute.pack()
        #todo window configuration
        self.config(menu=main_menu)
        self.bind('<F2>',lambda event:file.newFile(self,text))
        self.bind('<F3>', lambda event: file.openFile(self,text))
        self.bind('<F4>', lambda event: file.saveFile(self,text))
        self.bind('<F5>', lambda event: file.saveAsFile(text))
        self.bind('<F8>', lambda event:execute.focus_set)
        self.bind('<F11>', self.fullScreen)
        self.bind('<F12>',lambda event:self.destroy())
        self.bind('<Alt-f>',lambda event:style.style(text))
        self.mainloop()

    def fullScreen(self, event):
        if Application.COUNT % 2 == 0:
            self.attributes('-fullscreen', True)
        else:
            self.attributes('-fullscreen', False)
        Application.COUNT += 1
    def updateTime(self,main_menu):
        main_menu.entryconfigure(5,label=time.strftime("      %I:%M:%S"))
        main_menu.update_idletasks()
        self.after(1000,lambda:self.updateTime(main_menu))

    class File:
        """all file operational funcionality function"""
        def newFile(self,ref,text):
            text.delete(0.0, tkinter.END)
            ref.title('PROGRAMMER\'S IDE [Untitled File]')
            try:
                del Application.FILE
            except AttributeError:
                pass
        def openFile(self,ref,text):
            data=tkinter.filedialog.askopenfilename(title='open',filetypes=Application.FILE_TYPE)
            if data:
                text.delete(0.0,tkinter.END)
                try:
                    ref.title('PROGRAMMER\'S IDE [{}]'.format(os.path.basename(data)))
                    text.insert(0.0,open(data).read())
                except UnicodeError as ue:
                    tkinter.messagebox.showerror("file error",ue)
                except (TypeError,FileNotFoundError):
                    pass
                Application.FILE = data
        def saveFile(self,ref,text):
            try:
                open(os.path.basename(Application.FILE),'w').write(text.get(0.0,tkinter.END))
            except AttributeError:
                file=tkinter.filedialog.asksaveasfile(title='save',mode='w',filetypes=Application.FILE_TYPE)
                file.write(text.get(0.0,tkinter.END))
                Application.FILE =file.name
                ref.title('PROGRAMMER\'S IDE [{}]'.format(os.path.basename(file.name)))
        def saveAsFile(self,text):
            tkinter.filedialog.asksaveasfile(title='save as',mode='w',filetypes=Application.FILE_TYPE)
    class Style:
        """font appearance related function"""
        def style(self,text):
            font_setting=tkinter.Toplevel()
            font_setting.title("font setting")
            font_setting.geometry('450x350')
            #todo first frame
            first_frame=tkinter.Frame(font_setting)
            first_frame.pack(fill=tkinter.X,ipady=10)
            #list box label
            tkinter.Label(first_frame,text="font name",font=", 12 bold",fg='red').grid(row=0,column=0,sticky=tkinter.W)
            #listbox for font face
            name_list_box = tkinter.Listbox(first_frame,bd=2,bg='yellow',selectbackground='pink',selectforeground='blue')
            name_list_box.grid(row=1,column=0)
            name_list_box.focus_set()
            for index, names in enumerate(tkinter.font.families()):
                name_list_box.insert(index, names)
            #label for font size
            tkinter.Label(first_frame,text="font size",font=", 12 bold",fg='red').grid(row=0,column=1)
            #scale for font size
            scale = tkinter.Scale(first_frame, to=100,fg='green',length=180)
            scale.grid(row=1,column=1)
            #listbox for font type
            inner_frame=tkinter.Frame(first_frame)
            inner_frame.grid(row=1,column=2)
            bold=tkinter.StringVar()
            italic=tkinter.StringVar()
            underline=tkinter.StringVar()
            tkinter.Checkbutton(inner_frame,text='bold',onvalue='bold',offvalue='',variable=bold).pack(anchor=tkinter.W)
            tkinter.Checkbutton(inner_frame, text='italic',variable=italic,onvalue='italic',offvalue='').pack(anchor=tkinter.W)
            tkinter.Checkbutton(inner_frame, text='underline',variable=underline,onvalue='underline',offvalue='').pack(anchor=tkinter.W)
            tkinter.Button(inner_frame,text='font color',fg='white',bg=text['fg'],relief=tkinter.SOLID,command=lambda :self.fontChangesApply(None,text)).pack()
            #second frame
            update_value=tkinter.StringVar()
            second_frame=tkinter.Frame(font_setting)
            second_frame.pack(fill=tkinter.X)
            update_font=tkinter.Entry(second_frame,highlightcolor='green',textvariable=update_value)
            update_font.grid(row=0,column=0,ipadx=80)
            try:
                tkinter.Button(second_frame,text='get',bg='gray',activebackground='gray',command=lambda :self.validate(name_list_box,scale.get(),"{} {} {}".format(bold.get(), italic.get(), underline.get()),update_value)).grid(row=0,column=1)
            except (tkinter.TclError,Exception):
                pass
            tkinter.Button(second_frame,text='apply',bg='green',activebackground='green',command=lambda:self.fontChangesApply(update_value,text)).grid(row=0,column=2)
            font_setting.bind('<Escape>',lambda x:font_setting.destroy())

        def fontChangesApply(self,update_value,text):
            if update_value==None:
                text['fg'] = tkinter.colorchooser.askcolor()[1]
            else:
                value=update_value.get().split(sep=',')
                try:
                    value[1]=int(value[1])
                except (IndexError,ValueError):
                    pass
                text.config(font=value)
        def validate(self,font_name, font_size, font_face,update_value):
            try:
                font_name=font_name.selection_get()
            except tkinter.TclError:
                font_name=''
            update_value.set("{},{},{}".format(font_name,font_size,font_face))


    class Interpreter:
        def selectInterpreter(self,interpreter,execute):
            execute['state'] = tkinter.DISABLED
            try:
                Application.FILE
            except AttributeError:
                tkinter.messagebox.showinfo("can't find","file not opened or save")
            else:
                if sys.platform.lower()=='linux':
                    if Application.FILE.endswith('.py'):
                        Application.INTERPRETER = sys._base_executable
                    elif Application.FILE.endswith('.sh'):
                        Application.INTERPRETER = '/usr/bin/sh'
                    elif Application.FILE.endswith('.c'):
                        Application.INTERPRETER = '/usr/bin/gcc'
                    elif Application.FILE.endswith('.cpp'):
                        Application.INTERPRETER = '/usr/bin/g++'
                elif sys.platform.lower().startswith('win'):
                    Application.INTERPRETER=r'C:\Users\{}\AppData\Local\Programs\Python\Python38\python'.format(getpass.getuser())
                else:
                    Application.INTERPRETER=tkinter.filedialog.askopenfilename()

                if Application.INTERPRETER:
                    execute['state']=tkinter.NORMAL
                    try:
                        interpreter['text']=os.path.basename(Application.INTERPRETER)
                    except TypeError:
                        pass
                    interpreter['fg']='green'
        def validate(self,event,argument_label):
            if len(event.widget.get())>0:
                argument_label['fg']='green'
        def execute(self,ref,event,text,file,argument,interpreter,execute):
            file.saveFile(ref, text)
            self.selectInterpreter(interpreter,execute)

            if event.widget['text']=='terminal':
                if sys.platform.lower() == 'linux':
                    os.chdir(Application.FILE.replace(os.path.basename(Application.FILE),''))
                    os.system("gnome-terminal -e 'bash -c \"{} {} {}; exec bash\"'".format(Application.INTERPRETER,os.path.basename(Application.FILE),argument.get()))
                else:
                    sys.stderr.write("terminal not connected")

            elif event.widget['text']=='text':
                try:
                    #execution phase
                    result=subprocess.Popen("{} '{}' {}".format(Application.INTERPRETER,Application.FILE,argument.get()),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
                    out='execution result'.center(62, '*') + '\n' + str(result.stdout.read(), encoding='utf-8',errors='strict')
                    err=str(result.stderr.read(), encoding='utf-8', errors='strict')
                    if err:
                        result=out+'\n\n' + "ERROR OUTPUT".center(62,'*') + '\n' + err + ''.center(62,'*')
                    else:
                        result=out
                    #output graphic area
                    top_level = tkinter.Toplevel(ref)
                    top_text = tkinter.Text(top_level)
                    top_text.insert(0.0,result)
                    top_text.pack(fill=tkinter.BOTH, expand=True)
                    top_level.bind('<Escape>',lambda x:top_level.destroy())
                except AttributeError:
                    tkinter.messagebox.showinfo("can't find", "file not opened or save")
        def output(self,output_type,execute_button):
            execute_button['text']=output_type


if __name__ == '__main__':
    Application()

