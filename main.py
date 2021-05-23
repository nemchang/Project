# # 1,2번

from tkinter import *
import random
witdh=600
height=400
class MainGui:


    def __init__(self):
        window=Tk()
        window.geometry('600x400')
        window.title('스트레스는 지역화폐로 풀자')
        self.imageX=PhotoImage(file='image/x.gif')
        imageLabel=Label(window,image=self.imageX , width=400 )
        imageLabel.place(x=10,y=10)
        self.imageO=PhotoImage(file='image/o.gif')
        # self.imagea=PhotoImage(file='image/empty.gif')

        # frame1=Frame(window,relief="sunken",borderwidth = 5,height=200)
        # frame1.pack(side="top")
        #
        #
        # button1 = Button(frame1, text="프레임1")
        # button1.pack(side="right")
        #
        # button2 = Button(frame1, text="프레임2")
        # button2.pack(side="right")

        # Button(frame, image=self.imagea, text=' ', command=lambda row=i, col=j: self.pressed(row, col)))
        button_serch_window=Button(window, image = self.imageX, width=50,command=self.refresh)
        button_serch_window.place(x=440,y=10)
        button_bookmark=Button(window, image=self.imageO, width=50,command=self.refresh)
        button_bookmark.place(x=520, y=10)
        #Button(window,text='다시생성',command=self.refresh).pack(side=LEFT)
        imageLabel_sido = Label(window, text='시/군 입력') # 이미지로 테투리 표현해야함
        imageLabel_sido.place(x=10,y=70)

        e1 = Entry(window)
        e1.place(x=100,y=70)

        button_serch = Button(window, text='검색', command=self.refresh)
        button_serch.place(x=300,y=70)



        frame2=Frame(window,relief="sunken")
        frame2.size()
        frame2.place(x=100,y=200)

        scrollbar=Scrollbar(frame2)
        scrollbar.pack(side="right",fill="y")
        listbox = Listbox(frame2, yscrollcommand=scrollbar.set)
        for i in range(1, 1001):
            listbox.insert(i, str(i) + "/1000")
        listbox.pack(side="left")

        scrollbar["command"] = listbox.yview

        frame3 = Frame(window, relief="sunken")
        frame3.size()
        frame3.place(x=500, y=200)


        window.mainloop()


    def refresh(self):
        pass

MainGui()

# #3번
#
# from tkinter import *
# import random
#
# witdh = 600
# height = 400
#
#
# class MainGui:
#
#     def __init__(self):
#         window = Tk()
#         window.title('틱택토')
#         self.imageX = PhotoImage(file='image/x.gif')
#         self.imageO = PhotoImage(file='image/o.gif')
#         self.imagea = PhotoImage(file='image/empty.gif')
#         frame = Frame(window)
#         frame.pack()
#         self.matrix = []
#         self.turn=True #True = O
#         self.done=False # endgame
#
#         for i in range(3):
#             self.matrix.append([])  # 2차원리스트 생성
#             for j in range(3):
#                 img=self.imagea
#                 self.matrix[i].append(Button(frame, image=self.imagea,text=' ',command=lambda row=i,col=j:self.pressed(row,col)))
#                 self.matrix[i][j].grid(row=i, column=j)
#         self.explain=StringVar()
#         self.explain.set('플레이어 x 차례')
#         Label(window,textvariable=self.explain).pack()
#         Button(window, text='다시생성', command=self.refresh).pack()
#         window.mainloop()
#
#     def pressed(self,row,col):
#         if not self.done and self.matrix[row][col]['text']==' ':
#             if self.turn==True:
#                 self.matrix[row][col]['image']=self.imageO
#                 self.matrix[row][col]['text'] = 'O'
#             else:
#                 self.matrix[row][col]['image']=self.imageX
#                 self.matrix[row][col]['text'] = 'X'
#             self.turn=not self.turn
#             if self.chcek() =='@':
#                 self.explain.set('비김')
#                 self.done=True
#             elif self.chcek()!=' ':
#                 self.explain.set(self.chcek()+'가 이겻음')
#                 self.done=True
#             else:
#                 if self.turn:
#                     self.explain.set('플레이어 x 차례')
#                 else:
#                     self.explain.set('플레이어 o 차례')
#
#     def refresh(self):
#         for i in range(3):
#             for j in range(3):
#                 self.matrix[i][j]['image'] = self.imagea
#                 self.matrix[i][j]['text'] = ' '
#         self.turn=True
#         self.done=False
#
#     def chcek(self):
#         #이김
#         for i in range(3):
#             ch=self.matrix[i][0]['text']
#             if ch!=' 'and ch == self.matrix[i][1]['text'] and ch==self.matrix[i][2]['text']:
#                 return ch
#             if ch!=' 'and ch == self.matrix[1][i]['text'] and ch==self.matrix[2][i]['text']:
#                 return ch
#         ch=self.matrix[1][1]['text']
#         if ch!=' 'and ch == self.matrix[0][0]['text'] and ch==self.matrix[2][2]['text']:
#             return ch
#         if ch!=' 'and ch == self.matrix[0][2]['text'] and ch==self.matrix[2][0]['text']:
#             return ch
#             # if self.check()
#         #비김
#         flag=True
#         for i in range(3):
#             for j in range(3):
#                 if self.matrix[i][j]['text']==' ':
#                     flag=False
#                     break
#             if flag==False:
#                 break
#
#         if flag:
#             return '@'
#
#         # 승자도 비기지도 않음
#         return ' '
#
#
#
# MainGui()