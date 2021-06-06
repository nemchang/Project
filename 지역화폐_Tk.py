from tkinter import *
from tkinter import ttk, messagebox
import folium
import webbrowser
from cefpython3 import cefpython as cef
import sys
# import mimetypes
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

import telepot

#깃 데스크톱 채크용
import urllib
import http.client
import urllib.request
import threading

#c++ 연동
import spam
import random







DataList = [] #검색한 가맹점 리스트
is_getInfo = False #검색한 여부
save_List = [] #저장한 가맹점 리스트
tele_List = [] #텔레그램 챗봇용 리스트

# 챗 아이디
chatId = '1841278408'
# 텔레그램 챗 봇
chatBot = telepot.Bot('1887297937:AAGhjXGGZyNY1yUPwRajFiyWj0Y3N0PY_UQ')
#챗봇 이름 : 지역화폐 가맹점 텔레그램 봇 / @local_currency_telegram_bot

class MainGUI:

    # 검색탭을 배치할 검색프레임 생성
    def InputSearchTab(self):

        self.frame_SearchTab = ttk.Frame(self.window, width=845, height=400, relief=RIDGE) 
        self.image_search = PhotoImage(file = "image/search.png")
        self.tab.add(self.frame_SearchTab,text="검색",image = self.image_search,compound=LEFT) # 검색탭을 검색 프레임에 추가
        # self.label1.place(x=10,y=10) => 탭 프레임의 왼쪽위를 기준으로 x,y 좌표 초기화됨, 즉 왼쪽위끝에 놓으려면 (0,0)으로  프레임에 배치하면 됨

        #시/군 입력
        self.SearchLabel = Label(self.frame_SearchTab, text=" 시/군 입력 ",font= ("한수원 한돋움",13,'bold'),fg ="#ffffff",bg = '#005CB2')
        self.SearchLabel.place(x = 5, y = 12)
        # 입력창
        self.searchPlaceInput = StringVar()
        self.SearchEntry = Entry(self.frame_SearchTab, textvariable=self.searchPlaceInput,bg = '#F0F0F0', font= ("한수원 한돋움",14,'bold'), relief='ridge')
        self.SearchEntry.place(x = 100, y = 12)
        # 검색 버튼
        self.SearchButton = Button(self.frame_SearchTab, text= "검색!", command=self.SearchButtonAtion,relief="ridge", font= ("한수원 한돋움",13,'bold'),
                                    fg ="#ffffff",bg = '#005CB2',activebackground='#ffffff',activeforeground="#005CB2" )
        self.SearchButton.place(x = 390, y = 8)

    # 저장탭을 배치할 검색프레임 생성
    def InputSaveTab(self):

        self.frame_SaveTab = ttk.Frame(self.window, width=845, height=380, relief=RIDGE)
        self.image_save = PhotoImage(file = "image/save.png")
        self.tab.add(self.frame_SaveTab, text="저장",image = self.image_save,compound=LEFT) # 저장탭을 저장 프레임에 추가

        self.image_Gmail = PhotoImage(file = "image/Gmail.png")
        self.GmailButton = Button(self.frame_SaveTab,image=self.image_Gmail, command=self.getEmail, bg = '#005CB2')
        self.GmailButton.place(x = 760, y = 100)

        self.image_telegram = PhotoImage(file = "image/telegram.png")
        self.telegramButton = Button(self.frame_SaveTab,image=self.image_telegram, command=self.sendTelegram, bg = '#005CB2')
        self.telegramButton.place(x = 760, y = 200)


        # c++ 용 분류 버튼 생성
        self.image_sort = PhotoImage(file = "image/telegram.png")
        self.sortButton = Button(self.frame_SaveTab,image=self.image_sort, command=self.sort_list, bg = '#005CB2')
        self.sortButton.place(x = 760, y = 300)

        #파이 그래프 생성
        self.c2 = Canvas(self.frame_SaveTab,width=400, height=300, bg='white')
        self.c2.place(x = 350, y = 90)
        self.data2 = [0, 0, 0, 0, 10]
        start = 0
        s = sum(self.data2)

        for i in range(5):
            extent = self.data2[i] / s * 360
            color = self.random_color()
            self.c2.create_arc((0, 0, 300, 300), fill=color, outline='white', start=start, extent=extent)
            start = start + extent
            self.c2.create_rectangle(300, 20 + 20 * i, 300 + 30, 20 + 20 * (i + 1), fill=color)
            self.c2.create_text(300 + 50, 10 + 20 * (i + 1), text=str(self.data2[i]))


    # 로고그림추가
    def InputLogo(self):
        
        self.logo = PhotoImage(file="image/logo.png")
        self.logo_label=Label(self.window, image=self.logo,bd=0)
        self.logo_label.place(x=0, y=0)

        self.Ryon = PhotoImage(file="image/Ryon.png")
        self.logo_label=Label(self.window, image=self.Ryon,bd=0)
        self.logo_label.place(x=480, y=0)

    #검색 버튼 입력 시 수행
    def SearchButtonAtion(self): #검색버튼누르면 돌아가는 함수 
        global DataList
        global is_getInfo
        # 검색창 초기화
        DataList = []
        self.Value = self.SearchEntry.get()
        #print(self.Value)
        
        #입력한 시/군을 가지고 xml받아와서 검색
        self.SearchFranchise() # 걍 가맹점이 영어로 Franchise였음

    #가맹점 검색 및 리스트박스에 출력
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
        self.ListBox = Listbox(self.frame_SearchTab, width= 33, height= 15, borderwidth=3, relief='ridge',activestyle=DOTBOX,
                        bg="#005CB2", fg = "#ffffff", selectbackground="#ffffff",selectforeground="#005CB2",selectborderwidth=1,font=("한수원 한돋움",13,'bold'))

        #오픈API 한글로 받는거
        conn = http.client.HTTPSConnection("openapi.gg.go.kr")
        hangul_utf8 = urllib.parse.quote(self.Value)

        conn.request("GET", "/RegionMnyFacltStus?KEY=a5ff90a0a64c48ee83f8ff3250b31afd&pIndex=3&pSize=20&SIGUN_NM="+hangul_utf8,headers=headers) #가게이름
        req = conn.getresponse()
        # print(conn,hangul_utf8)
        # print(req.status,req.reason)
        Doc =(req.read().decode('utf-8'))

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

        self.ListBox.pack()
        self.ListBox.place(x=5, y=43)

        #선택한 가게 정보 보기 버튼 삽입
        self.ShowButton = Button(self.frame_SearchTab, text= "GET INFO", command=self.ShowInfo, font= ("한수원 한돋움",11,'bold'),
                                activeforeground ="#F0F0F0",activebackground = '#005CB2',bg='#ffffff',fg="#005CB2", relief='ridge',height=1, width=43)
        self.ShowButton.place(x = 5, y = 370)

        # #지도 프레임 추가
        # self.Mapframe = Frame(self.frame_SearchTab, width=340, height=250,bg = "#ffffff")
        # self.Mapframe.place(x=450, y=130)
        # url = 'file:///map.html'
        # self.thread = threading.Thread(target=self.showMap, args=(self.Mapframe, url))
        # self.thread.daemon = True

    #받은 XMl정보를 리스트에 저장
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
            Franchise_INDUTYPE_NM = item.find("INDUTYPE_NM")  # 업종명
            Franchise_cd = item.find("SIGUN_CD")  # 시군코드
            
            #일단 가게 이름만 받아옴
            if len(Franchise_name.text) > 0:
                lst = []
                lst.append(Franchise_name.text)
                lst.append(Franchise_LOTNO_add.text)
                lst.append(Franchise_ZIP_CD.text)
                lst.append(Franchise_WGS84_LAT.text)
                lst.append(Franchise_WGS84_LOGT.text)
                lst.append(Franchise_INDUTYPE_NM.text)
                lst.append(Franchise_cd.text)
                
                DataList.append(lst)

    # cef 처음 한번 만들기
    def showMap(self, frame, url):

        sys.excepthook = cef.ExceptHook
        window_info = cef.WindowInfo(frame.winfo_id())
        window_info.SetAsChild(frame.winfo_id(), [0, 0, 340, 250])
        cef.Initialize()
        print(window_info.windowName)

        self.browser = cef.CreateBrowserSync(window_info, url=url)
        self.browser.LoadUrl(url)
        cef.MessageLoop()

    # cef 갱신
    def LoadUrl(self):
        self.browser.LoadUrl('file:///map.html')

    #GET INFO
    def ShowInfo(self):
        global is_getInfo
        
        #처음 정보받을 때는 bool 바꾸고, 그 이후로는 출력했던 가게 정보들 전부 삭제 (정보 출력 요소 초기화)
        if is_getInfo == False: #is_getInfo = False
            is_getInfo = True
            self.thread.start()
        else :
            self.PrintselecLabel_INDUTYPE.place_forget()#업종별 사진 라벨 초기화
            self.selecLabel_NM.place_forget() #상호명 라벨 초기화
            self.selecLabel_LA.place_forget() #주소 라벨 초기화
            self.selecLabel_ZC.place_forget() #우편번호 라벨 초기화

        #리스트 박스에서 선택중인 가게 이름
        self.selection = self.ListBox.get(self.ListBox.curselection())

        #업종명에 따라 출력 이미지 다르게 저장
        INDUTYPE = DataList[self.ListBox.index(self.ListBox.curselection())][5]
        if "보건" in INDUTYPE or "의원" in INDUTYPE or "약국" in INDUTYPE or "병원" in INDUTYPE:
            if "미용" in INDUTYPE:
                self.INDUTYPE_image = PhotoImage(file="image/beauty.png")
            else:
                self.INDUTYPE_image = PhotoImage(file="image/hospital.png")
        elif "식" in INDUTYPE or "카페" in INDUTYPE or "슈퍼" in INDUTYPE :
            self.INDUTYPE_image = PhotoImage(file="image/food.png")
        elif "여가" in INDUTYPE or"문화" in INDUTYPE or "취미" in INDUTYPE:
            self.INDUTYPE_image = PhotoImage(file="image/play.png")
        elif "학원" in INDUTYPE or "교육" in INDUTYPE:
            self.INDUTYPE_image = PhotoImage(file="image/educate.png")
        elif "레저" in INDUTYPE or "헬스" in INDUTYPE or "스포츠" in INDUTYPE or "레져" in INDUTYPE:
            self.INDUTYPE_image = PhotoImage(file="image/sport.png")
        elif "숙박" in INDUTYPE or "여관" in INDUTYPE:
            self.INDUTYPE_image = PhotoImage(file="image/hotel.png")
        elif "의류" in INDUTYPE:
            self.INDUTYPE_image = PhotoImage(file="image/cloth.png")
        else :
            self.INDUTYPE_image = PhotoImage(file="image/ect.png")

        #업종명에 맞는 이미지라벨 출력
        self.PrintselecLabel_INDUTYPE = Label(self.frame_SearchTab, image = self.INDUTYPE_image,bg ="#ffffff")
        self.PrintselecLabel_INDUTYPE.place(x = 460, y = 50)

        # 가게이름, 주소 , 우편번호 출력
        self.selecLabel_NM = Label(self.frame_SearchTab, text=self.selection,font= ("한수원 한돋움",20),bg ="#ffffff",fg = '#005CB2')
        self.selecLabel_NM.place(x = 495, y = 50)
        if DataList[self.ListBox.index(self.ListBox.curselection())][1] == None:
            self.selecLabel_LA = Label(self.frame_SearchTab,text="주소 : - ",font=("한수원 한돋움", 9), bg="#ffffff", fg='#005CB2')
        else :
            self.selecLabel_LA = Label(self.frame_SearchTab, text=DataList[self.ListBox.index(self.ListBox.curselection())][1],font= ("한수원 한돋움",9,"underline"),bg ="#ffffff",fg = '#005CB2')
        self.selecLabel_LA.place(x = 460, y = 85)
        if DataList[self.ListBox.index(self.ListBox.curselection())][2] == None:
            self.selecLabel_ZC = Label(self.frame_SearchTab, text="우편번호: - ",font= ("한수원 한돋움",10),bg ="#ffffff",fg = '#005CB2')
        else:
            self.selecLabel_ZC = Label(self.frame_SearchTab, text="우편번호: "+DataList[self.ListBox.index(self.ListBox.curselection())][2],font= ("한수원 한돋움",10),bg ="#ffffff",fg = '#005CB2')
        self.selecLabel_ZC.place(x = 460, y = 105)

        # 길찾기 로드뷰 버튼 생성
        self.bb_image = PhotoImage(file="image/roadsign.png")
        self.myplace2selec = Button(self.frame_SearchTab, image = self.bb_image, command = lambda : self.Showkakao(2),bg ="#ffffff")
        self.myplace2selec.place(x = 795, y = 200)
        self.cc_image = PhotoImage(file="image/roadview.png")
        self.selecroadview = Button(self.frame_SearchTab, image = self.cc_image, command = lambda : self.Showkakao(3),bg ="#ffffff")
        self.selecroadview.place(x = 795, y = 260)

        # 가맹점 저장 버튼 생성
        self.save = PhotoImage(file = "image/save3.png")
        self.SaveFranchiseButton = Button(self.frame_SearchTab, image = self.save,bg = '#ffffff' ,borderwidth=0, relief="flat", command = self.SaveFranchise)
        self.SaveFranchiseButton.place(x = 720, y = 6)

        # 위도 경도 받아서 지도 만들기
        self.seleclat = DataList[self.ListBox.index(self.ListBox.curselection())][3] #선택한 가맹점위도
        self.seleclong = DataList[self.ListBox.index(self.ListBox.curselection())][4] #선택한 가맹점경도
        # print(self.seleclong,self.seleclat)
        m = folium.Map(location=[self.seleclat, self.seleclong], zoom_start=20)
        folium.Marker([self.seleclat, self.seleclong], popup=self.selection).add_to(m)
        # html 파일로 저장
        m.save('map.html')
        self.LoadUrl()

    # 가맹점 저장 리스트 만들고 출력
    def SaveFranchise(self):
        global save_List
        lst = []

        lst.append(self.selection)
        if DataList[self.ListBox.index(self.ListBox.curselection())][1] == None :
            lst.append("None")
        else :
            lst.append(DataList[self.ListBox.index(self.ListBox.curselection())][1])
            print(DataList[self.ListBox.index(self.ListBox.curselection())][6])
            lst.append(DataList[self.ListBox.index(self.ListBox.curselection())][6])
        for i in range(len(save_List)):
            if lst[0] == save_List[i][0]:
                messagebox.showerror("Error","이미 저장한 가맹점입니다.")
                return

        save_List.append(lst)



        self.save_ListLabel = Label(self.frame_SaveTab, text=" 저장한 가맹점 리스트 ",font= ("한수원 한돋움",15,'bold'),fg ="#ffffff",bg = '#005CB2')
        self.save_ListLabel.place(x = 120, y = 8)

        self.save_ListBox = Listbox(self.frame_SaveTab, width=33, height=17, borderwidth=5, relief='ridge',
                                        activestyle=DOTBOX,
                                        bg="#FFDE1F", fg="#005CB2", selectbackground="#ffffff",
                                        selectforeground="#005CB2",
                                        selectborderwidth=1, font=("한수원 한돋움", 12, 'bold'))

        for i in range(len(save_List)):
            # print(save_List[i])
            self.save_ListBox.insert(END,"["+str(i+1)+"] "+ save_List[i][0])
            self.save_ListBox.insert(END, save_List[i][1])
            self.save_ListBox.insert(END, " ")

        self.save_ListBox.pack()
        self.save_ListBox.place(x = 10, y = 35)

        print(save_List)

    #길찾기 로드뷰 브라우저 열기
    def Showkakao(self, num):
        if num == 2:
            url = "https://map.kakao.com/link/to/" + self.selection + "," + self.seleclat + "," + self.seleclong
            webbrowser.open(url)
        else:
            url = "https://map.kakao.com/link/roadview/" + self.seleclat + "," + self.seleclong
            webbrowser.open(url)

    #버튼 눌렀을 때 받을 이멜 주소 받기
    def getEmail(self):

        self.email_top = Toplevel(self.window)
        self.email_label = Label(self.email_top, text="받을 메일 주소를 입력")
        self.email_label.place(x=10, y=10)
        self.email_entrybox = Entry(self.email_top, width=25)
        self.email_entrybox.place(x=10, y=35)
        self.email_top.geometry('200x90+200+300')

        self.email_OK = Button(self.email_top, text='확인!', command=self.googleLoginAndSendEmail)
        self.email_OK.place(x=80, y=60)
        self.email_top.deiconify()

    #이멜 모내기
    def googleLoginAndSendEmail(self):

        htmlTxt = self.MakeHtmlDoc()

        senderAddr = "dragonkai7233@gmail.com"

        recipientAddr = ""

        msg = MIMEBase("multipart", "alternative")
        msg['Subject'] = "스트레스는 지역화폐로 풀자! 가맹점 저장 리스트"
        msg['From'] = senderAddr
        msg['To'] = recipientAddr

        # MIME 문서를 생성
        # htmlFD = open(htmlFileName, 'rb')
        # HtmlPart = MIMEText(htmlFD.read(), 'html', _charset='UTF-8')
        # htmlFD.close()

        messagePart = MIMEText(htmlTxt, 'html', _charset='UTF-8')

        # 메세지에 생성한 MIME 문서를 첨부합니다.
        msg.attach(messagePart)

        # 메일 발송하기

        mySmtp = smtplib.SMTP("smtp.gmail.com", 587)
        mySmtp.ehlo()
        mySmtp.starttls()
        mySmtp.ehlo()
        mySmtp.login(senderAddr, "yeonu910716")

        recipientAddr = self.email_entrybox.get()  # 앞에서 받아온 이메일

        mySmtp.sendmail(senderAddr, [recipientAddr], msg.as_string())

        self.email_entrybox.delete(0, 'end')  # 초기화
        self.email_top.withdraw()  # 창삭제
        msg = messagebox.showinfo("EMAIL", "전송 완료!")

        mySmtp.close()

    #구글에 보낼 정보 html로 만들기
    def MakeHtmlDoc(self): # HTML로 변환
        from xml.dom.minidom import getDOMImplementation
        # get Dom Implementation
        impl = getDOMImplementation()

        newdoc = impl.createDocument(None, "html", None)  # DOM 객체 생성
        top_element = newdoc.documentElement
        header = newdoc.createElement('header')
        top_element.appendChild(header)
        # Body 엘리먼트 생성.
        body = newdoc.createElement('body')

        for item in save_List:
            # create 주소 엘리먼트

            # savelist 태그 (엘리먼트) 생성.
            savelist = newdoc.createElement('savelist')
            body.appendChild(savelist)

            # 가맹점 이름
            name = newdoc.createElement('name')
            # create text node
            nameText = newdoc.createTextNode("   가맹점 : " + item[0])
            name.appendChild(nameText)

            body.appendChild(name)

               # 가맹점 주소
            address = newdoc.createElement('address')
            # create text node
            addressText = newdoc.createTextNode("   주소 : " + item[1])
            address.appendChild(addressText)

            body.appendChild(address)

            body.appendChild(savelist)  # line end

        # append Body
        top_element.appendChild(body)

        return newdoc.toxml()

    # 텔레그램 명령어 판단
    def handle(self, msg):
        global chatId, chatBot, tele_List , save_List
        #input = telepot.glance(msg)
        text = msg['text']
        args = text.split(' ')

        if text.startswith('검색') and len(args) > 1:
            self.telegramlist(args[1])
            for data in tele_List:
                chatBot.sendMessage(chatId, '가맹점 : ' + data[0] + '\n주소 : ' + data[1] + '\n우편번호 : ' + str(int(data[2])) + '\n업종명 : ' + data[5])
        elif text.startswith('저장리스트출력') :
            for data in save_List:
                chatBot.sendMessage(chatId, '가맹점 : ' + data[0] + '\n주소 : ' + data[1])
        else :
            chatBot.sendMessage(chatId, '모르는 명령어입니다.\n검색 [시군명] 또는 저장리스트출력 을 입력하세요.')

    # 버튼 입력 시 저장리스트 텔레그램에서 출력
    def sendTelegram(self):

        global chatBot, save_List
        for data in save_List:
            chatBot.sendMessage(chatId, '가맹점 : ' + data[0] + '\n주소 : ' + data[1])

    # c++ 연동 분류
    def sort_list(self):
        
        # 지금 돌아는 가는데 리스트를 잘 못받아서 대기
        
        # global save_List
        # print(save_List)
        # lst=[]
        # for i in range(len(save_List)):
        #     lst.append(save_List[i][2])
        #
        # print(lst[0])
        # print(spam.count(lst,41390))

        self.refesh_Pie()

        # c에서 받아서 지역코드로 분류
        # spam.sort(lst)


        # 갯수를 배열 or 쌍으로 받아서 파이나 바 차트 표현



        pass

    # 텔레그램 봇으로 메세지 보내기
    def sendMessage(self, message):
        global chatBot, chatId
        chatBot.sendMessage(chatId, message)

    # 텔레그램용 openapi 저장 리스트만들기
    def telegramlist(self,text):
        # -*- coding:cp949 -*-
        from xml.dom.minidom import parse, parseString
        from xml.etree import ElementTree
        global tele_List

        tele_List = []

        headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/605.1.15',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
        }
        # 오픈API 한글로 받는거
        conn = http.client.HTTPSConnection("openapi.gg.go.kr")
        hangul_utf8 = urllib.parse.quote(text)

        conn.request("GET",
                     "/RegionMnyFacltStus?KEY=a5ff90a0a64c48ee83f8ff3250b31afd&pIndex=3&pSize=10&SIGUN_NM=" + hangul_utf8,
                     headers=headers)  # 가게이름
        req = conn.getresponse()
        # print(conn,hangul_utf8)
        # print(req.status,req.reason)
        Doc = (req.read().decode('utf-8'))

        if req.status == 200:
            if Doc == None:
                print("에러")
            else:
                tree = ElementTree.fromstring(Doc)

                # Acc 엘리먼트를 가져옵니다.
                itemElements = list(tree.iter("row"))  # return list type
                for item in itemElements:
                    Franchise_name = item.find("CMPNM_NM")  # 상호명
                    Franchise_LOTNO_add = item.find("REFINE_LOTNO_ADDR")  # 도로명주소
                    Franchise_ZIP_CD = item.find("REFINE_ZIP_CD")  # 우편번호
                    Franchise_WGS84_LAT = item.find("REFINE_WGS84_LAT")  # 위도
                    Franchise_WGS84_LOGT = item.find("REFINE_WGS84_LOGT")  # 경도
                    Franchise_INDUTYPE_NM = item.find("INDUTYPE_NM")  # 업종명

                    if len(Franchise_name.text) > 0:
                        lst = []
                        lst.append(Franchise_name.text)
                        lst.append(Franchise_LOTNO_add.text)
                        lst.append(Franchise_ZIP_CD.text)
                        lst.append(Franchise_WGS84_LAT.text)
                        lst.append(Franchise_WGS84_LOGT.text)
                        lst.append(Franchise_INDUTYPE_NM.text)

                        tele_List.append(lst)

    def random_color(self):
        color = '#'
        colors = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        for i in range(6):
            color += colors[random.randint(0, 15)]
        return color

    def refesh_Pie(self):
        print("asd")

        self.data2=[100,100,100,100,100]
        s = sum(self.data2)
        start = 0
        self.c2.destroy()
        self.c2 = Canvas(self.frame_SaveTab,width=400, height=300, bg='white')
        self.c2.place(x = 350, y = 90)
        for i in range(5):
            extent = self.data2[i] / s * 360
            color = self.random_color()
            self.c2.create_arc((0, 0, 300, 300), fill=color, outline='white', start=start, extent=extent)
            start = start + extent
            self.c2.create_rectangle(300, 20 + 20 * i, 300 + 30, 20 + 20 * (i + 1), fill=color)
            self.c2.create_text(300 + 50, 10 + 20 * (i + 1), text=str(self.data2[i]))

        self.c2.place(x = 350, y = 90)
        pass
    # TK 그리기
    def __init__(self):
        
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
        self.seleclat = None #위도
        self.seleclong = None #경도
        #지도 프레임 추가
        self.Mapframe = Frame(self.frame_SearchTab, width=340, height=250,bg = "#ffffff")
        self.Mapframe.place(x=450, y=130)
        url = 'file:///map.html'
        self.thread = threading.Thread(target=self.showMap, args=(self.Mapframe, url))
        self.thread.daemon = True
        chatBot.message_loop(self.handle)

        self.window.mainloop()


MainGUI()