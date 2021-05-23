from tkinter import *
from tkinter import ttk
from tkinter import font
import tkinter.messagebox
#깃 데스크톱 채크용
import urllib
import http.client

DataList = [] #검색한 가맹점 리스트

class MainGUI:
    

    def InputSearchTab(self):#검색탭을 배치할 검색프레임 생성

        self.frame_SearchTab = ttk.Frame(self.window, width=845, height=400, relief=RIDGE) 
        self.image_search = PhotoImage(file = "image/search.png")
        self.tab.add(self.frame_SearchTab,text="검색",image = self.image_search,compound=LEFT) # 검색탭을 검색 프레임에 추가
        # self.label1 = Label(self.frame_SearchTab,text="검색검색")
        # self.label1.place(x=10,y=10) => 탭 프레임의 왼쪽위를 기준으로 x,y 좌표 초기화됨, 즉 왼쪽위끝에 놓으려면 (0,0)으로  프레임에 배치하면 됨

        #시/군 입력
        self.SearchLabel = Label(self.frame_SearchTab, text=" 시/군 입력 ",font= ("한수원 한돋움",13,'bold'),fg ="#ffffff",bg = '#005CB2')
        self.SearchLabel.place(x = 10, y = 12)
        # 입력창
        self.searchPlaceInput = StringVar()
        self.SearchEntry = Entry(self.frame_SearchTab, textvariable=self.searchPlaceInput,bg = '#F0F0F0', font= ("한수원 한돋움",14,'bold'), relief='ridge')
        self.SearchEntry.place(x = 105, y = 12)
        # 검색 버튼
        self.SearchButton = Button(self.frame_SearchTab, text= "검색!", command=self.SearchButtonAtion,relief="ridge", font= ("한수원 한돋움",13,'bold'),\
                                    fg ="#ffffff",bg = '#005CB2',activebackground='#ffffff',activeforeground="#005CB2" )
        self.SearchButton.place(x = 395, y = 8)
   
    
    def InputBookmarkTab(self):#븍마크탭을 배치할 검색프레임 생성

        self.frame_BookmarkTab = ttk.Frame(self.window, width=845, height=380, relief=RIDGE)
        self.image_bookmark = PhotoImage(file = "image/bookmark.png")
        self.tab.add(self.frame_BookmarkTab, text="북마크",image = self.image_bookmark,compound=LEFT) # 북마크탭을 북마크 프레임에 추가
        # self.label2 = Label(self.frame_SaveTab,text="북마크마크")
        # self.label2.place(x=10,y=10)

        self.image_Gmail = PhotoImage(file = "image/Gmail.png")
        self.GmailButton = Button(self.frame_BookmarkTab,image=self.image_Gmail, command=self.sendGmail, bg = '#005CB2')
        self.GmailButton.place(x = 760, y = 100)

        self.image_telegram = PhotoImage(file = "image/telegram.png")
        self.telegramButton = Button(self.frame_BookmarkTab,image=self.image_telegram, command=self.sendTelegram, bg = '#005CB2')
        self.telegramButton.place(x = 760, y = 200)

    def InputLogo(self):#로고그림추가
        
        self.logo = PhotoImage(file="image/logo.png")
        self.logo_label=Label(self.window, image=self.logo,bd=0)
        self.logo_label.place(x=0, y=0)

        self.Ryon = PhotoImage(file="image/Ryon.png")
        self.logo_label=Label(self.window, image=self.Ryon,bd=0)
        self.logo_label.place(x=480, y=0)

     
    def SearchButtonAtion(self): #검색버튼누르면 돌아가는 함수 
        global DataList
        # 검색창 초기화
        DataList = []
        self.Value = self.SearchEntry.get()
        #print(self.Value)
        
        #입력한 시/군을 가지고 xml받아와서 검색
        self.SearchFranchise() # 걍 가맹점이 영어로 Franchise였음
    
    def SearchFranchise(self):
        # -*- coding:cp949 -*-
        from xml.dom.minidom import parse, parseString

        headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/605.1.15',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
        }
        #가맹점리스트 먼저 생성
        self.ListBox = Listbox(self.frame_SearchTab, width= 33, height= 15, borderwidth=5, relief='ridge',activestyle=DOTBOX, \
                        bg="#005CB2", fg = "#ffffff", selectbackground="#ffffff",selectforeground="#005CB2",selectborderwidth=1,font=("한수원 한돋움",13,'bold'))

        #오픈API 한글로 받는거
        conn = http.client.HTTPSConnection("openapi.gg.go.kr")
        hangul_utf8 = urllib.parse.quote(self.Value)

        conn.request("GET", "/RegionMnyFacltStus?KEY=a5ff90a0a64c48ee83f8ff3250b31afd&pIndex=3&pSize=1000&SIGUN_NM="+hangul_utf8,headers=headers) #가게이름
        req = conn.getresponse()
        print(conn,hangul_utf8)
        print(req.status,req.reason)
        Doc=(req.read().decode('utf-8'))

        if req.status == 200:
            if Doc==None:
                print("에러")
            else:
                self.ExtractFranchiseData(Doc)

        else:
            print("OpenAPI request has been failed!! please retry")
        

        self.ListBox.configure(state='normal')

        for i in range(len(DataList)):
            # print(DataList[i])
            self.ListBox.insert(END,DataList[i])
            # self.ListBox.insert(END, "\n")

        self.ListBox.pack()
        self.ListBox.place(x=10, y=43)

        #선택한 가게 정보 보기 버튼 삽입
        self.ShowButton = Button(self.frame_SearchTab, text= "GET INFO", command=self.ShowInfo, font= ("한수원 한돋움",11,'bold'),\
                                activeforeground ="#F0F0F0",activebackground = '#005CB2',bg='#ffffff',fg="#005CB2", relief='ridge',height=1, width=43)
        self.ShowButton.place(x = 10, y = 370)

    def ExtractFranchiseData(self, Doc):
        from xml.etree import ElementTree

        tree = ElementTree.fromstring(Doc)

        # Acc 엘리먼트를 가져옵니다.
        itemElements = list(tree.iter("row"))  # return list type
        # print(itemElements)
        for item in itemElements:
            Franchise_name = item.find("CMPNM_NM")
            #일단 가게 이름만 받아옴
            if len(Franchise_name.text) > 0:
                DataList.append((Franchise_name.text))
    
    def ShowInfo(self):#선택한 가게 정보 보기
        self.is_on = False #해당 가맹점 북마크 on-true /off-false
        self.selection = self.ListBox.get(self.ListBox.curselection())
        # print(self.selection)
        self.selecLabel = Label(self.frame_SearchTab, text=self.selection,font= ("한수원 한돋움",15,"underline"),bg ="#ffffff",fg = '#000000')
        self.selecLabel.place(x = 460, y = 45)

        self.on = PhotoImage(file = "image/on.png")
        self.off = PhotoImage(file = "image/off.png")
        
        self.BookMarkButton = Button(self.frame_SearchTab, image = self.off, borderwidth=0, relief="flat", command=self.Switch)   
        self.BookMarkButton.place(x = 798, y = 8)
    
    def Switch(self):# 북마크 온/오프
        
        if self.is_on:
            self.BookMarkButton.config(image= self.off)
            self.is_on = False
        else:
            self.BookMarkButton.config(image= self.on)
            self.is_on = True

    
    def sendGmail(self):
        pass
    def sendTelegram(self):
        pass

    def __init__(self): #TK 그리기
        
        self.window = Tk()
        self.window.title("스트레스는 지역화폐로 풀자!")
        self.window.geometry("900x500")
        self.window.configure(bg='#005CB2')

        style = ttk.Style() # 탭 커스텀
        style.theme_create('TAB_THEME', settings={
                ".": {
                    "configure": {
                        "background": '#ffffff', # All except tabs 탭 배경 색상
                        "font": 'red'
                    }
                },
                "TNotebook": {
                    "configure": {
                        "background":'#005CB2', # Your margin color 탭 바 색상
                        "tabmargins": [2, 0, 0, 0], # margins: left, top, right, separator
                        "tabposition" : 'ne'
                    }
                },
                "TNotebook.Tab": {
                    "configure": {
                        "background": '#005CB2', # 선택안된 탭 버튼 색
                        "padding": [10, 10], # 탭 버튼 가로 세로
                        "font" : ('한수원 한돋움', '20', 'bold'),
                        "foreground" : '#005CB2' # 선택된 탭 버튼 글자색
                    },
                    "map": {
                        "background": [("selected", '#ffffff')], # 선택된 탭 버튼 배경색
                        "foreground" : [("selected", '#005CB2')],# 선택된 탭 버튼 글자색
                        "expand": [("selected", [1, 1, 1, 0])] # text margins
                    }
                }
            }
        )
        # '#005CB2' => 윈도우 배경색, 탭 비선택시 탭버튼 색상, 글자색1 (퍼런색)
        # '#F0F0F0' => 탭 배경색, 탭 선택시 탭버튼 색상 , 글자색2 (허연색)
        style.theme_use('TAB_THEME')
            
        # 탭 생성
        self.tab = ttk.Notebook()
        self.tab.pack()
        self.tab.place(x=25,y=25)
        self.ListBox = None

        self.InputSearchTab()
        self.InputBookmarkTab()
        self.InputLogo()

        self.window.mainloop()


MainGUI()