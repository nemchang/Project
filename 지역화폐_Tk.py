from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import folium
import webbrowser

#깃 데스크톱 채크용
import urllib
import http.client
import urllib.request


DataList = [] #검색한 가맹점 리스트
is_getInfo = False #검색한 여부

class MainGUI:
    

    def InputSearchTab(self):#검색탭을 배치할 검색프레임 생성

        self.frame_SearchTab = ttk.Frame(self.window, width=845, height=400, relief=RIDGE) 
        self.image_search = PhotoImage(file = "image/search.png")
        self.tab.add(self.frame_SearchTab,text="검색",image = self.image_search,compound=LEFT) # 검색탭을 검색 프레임에 추가
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
   
    
    def InputSaveTab(self):#저장탭을 배치할 검색프레임 생성

        self.frame_SaveTab = ttk.Frame(self.window, width=845, height=380, relief=RIDGE)
        self.image_save = PhotoImage(file = "image/save.png")
        self.tab.add(self.frame_SaveTab, text="저장",image = self.image_save,compound=LEFT) # 저장탭을 저장 프레임에 추가

        self.image_Gmail = PhotoImage(file = "image/Gmail.png")
        self.GmailButton = Button(self.frame_SaveTab,image=self.image_Gmail, command=self.sendGmail, bg = '#005CB2')
        self.GmailButton.place(x = 760, y = 100)

        self.image_telegram = PhotoImage(file = "image/telegram.png")
        self.telegramButton = Button(self.frame_SaveTab,image=self.image_telegram, command=self.sendTelegram, bg = '#005CB2')
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
            print(DataList[i])
            self.ListBox.insert(END,DataList[i][0])
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
            Franchise_name = item.find("CMPNM_NM")#상호명
            Franchise_LOTNO_add = item.find("REFINE_LOTNO_ADDR")#도로명주소
            Franchise_ZIP_CD = item.find("REFINE_ZIP_CD")#우편번호
            Franchise_WGS84_LAT = item.find("REFINE_WGS84_LAT") #위도
            Franchise_WGS84_LOGT = item.find("REFINE_WGS84_LOGT") #경도
            
            #일단 가게 이름만 받아옴
            if len(Franchise_name.text) > 0:
                lst = []
                lst.append(Franchise_name.text)
                lst.append(Franchise_LOTNO_add.text)
                lst.append(Franchise_ZIP_CD.text)
                lst.append(Franchise_WGS84_LAT.text)
                lst.append(Franchise_WGS84_LOGT.text)
                
                DataList.append(lst)
    
    def ShowInfo(self):
        global is_getInfo
        
        #선택한 가게 정보 보기

        if is_getInfo == False: #is_getInfo = False
            is_getInfo = True
        else :
            self.selecLabel_NM.place_forget() #상호명 라벨 초기화
            self.selecLabel_LA.place_forget() #주소 라벨 초기화
            self.selecLabel_ZC.place_forget() #우편번호 라벨 초기화

        self.is_on = False #해당 가맹점 북마크 on-true /off-false
        self.selection = self.ListBox.get(self.ListBox.curselection())
        # print(self.ListBox.index(self.ListBox.curselection()))#셀렉한가게인덱스

        self.selecLabel_NM = Label(self.frame_SearchTab, text="⚜ "+self.selection,font= ("한수원 한돋움",20),bg ="#ffffff",fg = '#005CB2')
        self.selecLabel_NM.place(x = 460, y = 50)

        self.selecLabel_LA = Label(self.frame_SearchTab, text=DataList[self.ListBox.index(self.ListBox.curselection())][1],font= ("한수원 한돋움",9,"underline"),bg ="#ffffff",fg = '#005CB2')
        self.selecLabel_LA.place(x = 460, y = 85)

        if DataList[self.ListBox.index(self.ListBox.curselection())][2] == None:
            self.selecLabel_ZC = Label(self.frame_SearchTab, text="우편번호: - ",font= ("한수원 한돋움",10),bg ="#ffffff",fg = '#005CB2')
            self.selecLabel_ZC.place(x = 460, y = 105)
        else:
            self.selecLabel_ZC = Label(self.frame_SearchTab, text="우편번호: "+DataList[self.ListBox.index(self.ListBox.curselection())][2],font= ("한수원 한돋움",10),bg ="#ffffff",fg = '#005CB2')
            self.selecLabel_ZC.place(x = 460, y = 105)

        ####################################################################################################################################

        self.seleclat = DataList[self.ListBox.index(self.ListBox.curselection())][3] #선택한 가맹점위도
        self.seleclong = DataList[self.ListBox.index(self.ListBox.curselection())][4] #선택한 가맹점경도
        #print(self.seleclong)

        # server = 'dapi.kakao.com'
        # key = 'a31b76e4df2614c2d21a4c20947c3f55'  # 본인 카카오앱키 입력
        # header = {'Authorization': 'KakaoAK ' + key}
        # conn = http.client.HTTPSConnection(server)
        # conn.request("GET", "/v2/local/geo/coord2regioncode.xml?x="+self.seleclong+"&y="+self.seleclat, None, header)
        # req = conn.getresponse()
        #
        # print(req.status, req.reason)
        # # 200 OK 면 정상적으로 읽어온 것이고, 아닌 경우에는 홈페이지에 있는 에러 숫자 참고
        #
        # rb = req.read()
        # print(rb.decode('utf-8'))
        #
        # map_osm.save('osm.html')

        self.save = PhotoImage(file = "image/save2.png")#가맹점 저장 버튼
        self.SaveFranchiseButton = Button(self.frame_SearchTab, image = self.save, borderwidth=0, relief="flat", command = self.SaveFranchise)
        self.SaveFranchiseButton.place(x = 780, y = 8)
    
    def SaveFranchise(self):#가맹점 저장
        pass

    
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
        self.InputSaveTab()
        self.InputLogo()

        self.window.mainloop()


MainGUI()