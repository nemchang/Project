from tkinter import *
from tkinter import ttk
from tkinter import font
import tkinter.messagebox
#깃 데스크톱 채크용
DataList = [] #xml받아옴

class MainGUI:

    def InputSearchTab(self):#검색탭을 배치할 검색프레임 생성

        self.frame_SearchTab = ttk.Frame(self.window, width=845, height=400, relief=RIDGE) 
        self.image_search = PhotoImage(file = "image/search.png")
        self.tab.add(self.frame_SearchTab,text="검색",image = self.image_search,compound=LEFT) # 검색탭을 검색 프레임에 추가
        # self.label1 = Label(self.frame_SearchTab,text="검색검색")
        # self.label1.place(x=10,y=10) => 탭 프레임의 왼쪽위를 기준으로 x,y 좌표 초기화됨, 즉 왼쪽위끝에 놓으려면 (0,0)으로  프레임에 배치하면 됨

        #시/군 입력
        self.SearchLabel = Label(self.frame_SearchTab, text=" 시/군 입력 ",font= ("한수원 한돋움",13,'bold'),fg ="#F0F0F0",bg = '#005CB2')
        self.SearchLabel.place(x = 10, y = 12)
        # 입력창
        self.searchPlaceInput = StringVar()
        self.SearchEntry = Entry(self.frame_SearchTab, textvariable=self.searchPlaceInput, font= ("한수원 한돋움",13,'bold'), relief='ridge')
        self.SearchEntry.place(x = 105, y = 12)
        # 검색 버튼

        self.SearchButton = Button(self.frame_SearchTab, text= "검색!", command=self.SearchButtonAtion, font= ("한수원 한돋움",13,'bold'),fg ="#F0F0F0",bg = '#005CB2')
        self.SearchButton.place(x = 380, y = 8)
   
    
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

        #검색창 초기화
        self.Value = self.SearchEntry.get()
        #print(self.Value)
        
        #입력한 시/군을 가지고 xml받아와서 검색
        self.SearchFranchise() # 걍 가맹점이 영어로 Franchise였음
    
    def SearchFranchise(self):
        # -*- coding:cp949 -*-
        import urllib
        import http.client
        from xml.dom.minidom import parse, parseString
        
        global DataList
        
        # self.SIGUN_CD = 0
        # DataList.clear()
        # SIGUN_NMList = ['가평군 ', '고양시', '과천시', '광명시', '광주시', '구리시', '군포시', '김포시', '남양주시', '동두천시', '부천시', '성남시', '수원시', '시흥시', '안산시', '안성시', \
        #                 '안양시', '양주시', '양평군', '여주시', '연천군', '오산시', '용인시', '의왕시', '의정부시', '이천시', '파주시', '평택시', '포천시', '하남시', '화성시']
        # SIGUN_CDList = [41820, 41280, 41290, 41210, 41610, 41310, 41410, 41570, 41360, 41250, 41190, 41130, 41110, 41390, 41270, 41550, 41170, 41630, 41830, 41670, 41800, 41370, 41460, 41430,\
        #                 41150, 41500, 41480, 41220, 41650, 41450, 41590]
        # for i in range(len(SIGUN_NMList)):
        #     if self.Value == SIGUN_NMList[i]:
        #         self.SIGUN_CD = SIGUN_CDList[i]
        #주소에 한글을 안넣으려고 한 흔적
        
        #가맹점리스트 스크롤
        self.ListBoxScrollbar = Scrollbar(self.frame_SearchTab) 
        self.ListBoxScrollbar.pack()
        self.ListBoxScrollbar.place(x = 450, y = 45)

        #가맹점리스트 먼저 생성
        self.TempFont = font.Font(self.frame_SearchTab, size=15, weight='bold', family='한수원 한돋움')
        self.ListBox = Text(self.frame_SearchTab, width= 59, height= 24, borderwidth=5, relief='ridge', yscrollcommand=self.ListBoxScrollbar.set)  

        #오픈API 한글로 받는거
        conn = http.client.HTTPConnection("openapi.gg.go.kr")
        hangul_utf8 = urllib.parse.quote(self.Value)
        conn.request("GET", "/RegionMnyFacltStus?KEY=a5ff90a0a64c48ee83f8ff3250b31afd&pIndex=1&pSize=1000&SIGUN_NM="+hangul_utf8) #가게이름
        req = conn.getresponse()
        print(hangul_utf8)
        print(req.status,req.reason)
        #여기서 req.status가 302가 나오는데 이게 뭔질 모르겠네요
        #혹시몰라서 그 서울근린뭐시기 주소로 해봤는데 그거는 되네요
        #두개 차이점이 주소에 한글이 들어가냐 아니냐 인거 같아요
        #교수님이 올려주신 OpenAPI 한글 사용법에 있는 거 똑같이 해봤는데 그것도 302 나오는거 보니까
        #한글에서 문제가 생기고 있는게 아닌가....
        print(req.read().decode('utf-8'))

        # if req.status == 200:
        #     self.ExtractFranchiseData(req.read().decode('utf-8'))
        # else:
        #     print("OpenAPI request has been failed!! please retry")
        
        #print(DataList)
        # self.ListBox.configure(state='normal')
        # self.ListBox.delete(0.0, END)

        # for i in range(len(DataList)):  
        #     self.ListBox.insert(i, "["+(i+1)+"]"+DataList[i]) 

        # self.ListBox.pack()
        # self.ListBox.place(x=10, y=45)
        # self.ListBoxScrollbar.config(command=self.ListBox.yview)

        # self.ListBox.configure(state='disabled') 

    # def ExtractFranchiseData(self, strXml):
    #     from xml.etree import ElementTree
    #     global DataList

    #     tree = ElementTree.fromstring(strXml)
    #     # Acc 엘리먼트를 가져옵니다.
    #     itemElements = list(tree.iter("item"))  # return list type

    #     for item in itemElements:
    #         Franchise_name = item.find("CMPNM_NM")
    #         #일단 가게 이름만 받아옴
    #         if len(Franchise_name.text) > 0:
    #             DataList.append((Franchise_name.text))

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
                        "background": '#F0F0F0', # All except tabs 탭 배경 색상
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
                        "background": [("selected", '#F0F0F0')], # 선택된 탭 버튼 배경색
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

        self.InputSearchTab()
        self.InputBookmarkTab()
        self.InputLogo()

        self.window.mainloop()


MainGUI()