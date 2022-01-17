import tkinter
from tkinter import ttk
from threading import Thread
class privateLobbyConfigWindow(tkinter.Tk):
    players = []
    def __init__(self,width,height,background,lobbyCode):
        super().__init__()
        self.geometry("%dx%d+250+100"%(width,height))
        self.configure(bg = background)
        self.columnconfigure(0,weight = 1)
        self.columnconfigure(1,weight = 1)
        self.rowconfigure(0,weight = 5)
        self.rowconfigure(1,weight = 1)
        self.width = width
        self.height = height
        self.background = background
        self.lobbyCode = lobbyCode
        self.roundTime = -1
        self.noOfRounds = -1
        self.avatarContainerFrame = None
        self.lobbySettingsUI()
        self.playersInterfaceUI()
        self.mainloop()
    
    def lobbySettingsUI(self):
        #container frame for settings part
        settingsContainer = tkinter.Frame(
            master = self,bg = "white"
        )
        settingsContainer.grid(row = 0,column = 0)
        settingsContainer.columnconfigure(0,weight = 1)
        settingsContainer.rowconfigure(0,weight = 1)
        settingsContainer.rowconfigure(1,weight = 1)
        settingsContainer.rowconfigure(2,weight = 1)
        settingsContainer.rowconfigure(3,weight = 1)

        #lobby settings header
        lobbySettingsLabel = tkinter.Label(
            master = settingsContainer,text = "Lobby Settings",bg = "white",font = ("Segoe UI",17)
        )
        lobbySettingsLabel.grid(row = 0,column = 0)

        #rounds selection list box and label container frame
        roundsContainerFrame = tkinter.Frame(
            master = settingsContainer,bg = "white",bd = 0
        )
        roundsContainerFrame.grid(row = 1,column = 0,padx = 20)
        roundsContainerFrame.columnconfigure(0,weight = 1)

        #rounds label
        roundsLabel = tkinter.Label(
            master = roundsContainerFrame,text = "Rounds",bg = "white",font = ("Segoe UI",13,"bold"),fg = "#00ccff"
        )
        roundsLabel.grid(row = 0,column = 0,sticky = tkinter.W)

        #rounds combobox
        roundsStringVar = tkinter.StringVar
        roundsCombobox = ttk.Combobox(
            master = roundsContainerFrame,width = 30,textvariable = roundsStringVar,state = 'readonly',exportselection = 0,
            font = ("Segoe UI",17)
        )
        roundsCombobox.grid(row = 1,column = 0)
        roundsCombobox['values'] = ('2','3','4','5','6','7','8','9','10')
        roundsCombobox.bind("<<ComboboxSelected>>",self.getRounds)

        #draw time in seconds label and combobox container
        drawTimeContainer = tkinter.Frame(
            master = settingsContainer,bg = "white",bd = 0
        )
        drawTimeContainer.grid(row = 2,column = 0,pady = 20,padx = 20)
        drawTimeContainer.columnconfigure(0,weight = 1)

        #draw time label
        drawTimeLabel = tkinter.Label(
            master = drawTimeContainer,text = "Draw time in seconds",bg = "white",font = ("Segoe UI",13,"bold"),
            fg = "#00ccff"
        )
        drawTimeLabel.grid(row = 0,column = 0,sticky = tkinter.W)

        #draw time combobox
        drawTimeVariable = tkinter.StringVar()
        drawTimeCombobox = ttk.Combobox(
            master = drawTimeContainer,width = 30,textvariable = drawTimeVariable,state = 'readonly',exportselection = 0,
            font = ("Segoe UI",17)
        )
        drawTimeCombobox.grid(row = 1,column = 0)
        drawTimeCombobox['values'] = ('30','40','50','60','70','80','90','100','110','120','130')
        drawTimeCombobox.bind("<<ComboboxSelected>>",self.getDrawTime)

        #start game button
        startGameButton = tkinter.Button(
            master = settingsContainer,text = "Start Game",bg = "#84ff00",bd = 0,font = ("Segoe UI",15),
            activebackground = "#2aad37",command = self.sendLobbyConfigToServer
        )
        startGameButton.grid(row = 3,column = 0,sticky = (tkinter.W,tkinter.E,tkinter.S),padx = 20,pady = 5)
    
    def playersInterfaceUI(self):
        #players avatar container frame
        self.avatarContainerFrame = tkinter.Frame(
            master = self,bg = self.background
        )
        self.avatarContainerFrame.grid(row = 0,column = 1)

        #players header label
        playersHeaderLabel = tkinter.Label(
            master = self.avatarContainerFrame,text = "Players",font = ("Segoe UI",20)
        )
        playersHeaderLabel.grid(row = 0,column = 0,columnspan = 2)

        #lobby code label
        lobbyCodeLabel = tkinter.Label(
            master = self,width = 20,text = "Hover over for lobby code",bg = "white",font = ("Segoe UI",20)
        )
        lobbyCodeLabel.grid(row = 1,column = 0,columnspan = 2,sticky = tkinter.N)
        lobbyCodeLabel.bind("<Enter>",self.showLobbyCode)
        lobbyCodeLabel.bind("<Leave>", self.hideLobbyCode)
    
    @classmethod
    def addPlayers(cls):
        pass
    
    @classmethod
    def addPlayersToUi(cls, selfObject):
        clmn = 0
        rw = 1
        while(True):
            if(len(cls.players)>0):
                for player in cls.players:
                    if(player["avatar"]=="male"):
                        maleAvatarImage = tkinter.PhotoImage(file = "images/male_avatar.png")
                        maleAvatarLabel = tkinter.Label(
                            master = selfObject.avatarContainerFrame,image = maleAvatarImage,text = "boy",compound = tkinter.TOP,font = ("Segoe UI",10,"bold")
                        )
                        if(clmn<5):
                            maleAvatarLabel.grid(row = rw,column = clmn)
                        else:
                            maleAvatarLabel.grid(row = rw,column = clmn)
                            clmn = 0
                            rw += 1
                        maleAvatarLabel.image = maleAvatarImage
                    elif(player["avatar"]=="female"):
                        femaleAvatarImage = tkinter.PhotoImage(file = "images/female_avatar.png")
                        femaleAvatarLabel = tkinter.Label(
                            master = selfObject.avatarContainerFrame,image = femaleAvatarImage,text = "girl",compound = tkinter.TOP,font = ("Segoe UI",10,"bold")
                        )
                        if(clmn<5):
                            femaleAvatarLabel.grid(row = rw,column = clmn)
                        else:
                            femaleAvatarLabel.grid(row = rw,column = clmn)
                            clmn = 0
                            rw += 1
                        femaleAvatarLabel.image = femaleAvatarImage

    def getRounds(self, event):
        self.noOfRounds = event.widget.get()
    
    def getDrawTime(self, event):
        self.roundTime = event.widget.get()
    
    def sendLobbyConfigToServer(self):
        lobbyConfigs = {
            "messageType" : "private lobby configurations",
            "roundTime" : self.roundTime,
            "noOfRounds" : self.noOfRounds
        }
        self.serverConnection.requestMessage = lobbyConfigs
        serverResponse = self.serverConnection.sendRequestToServer()
        print(serverResponse["message"])
    
    def showLobbyCode(self,event):
        event.widget.configure(text = self.lobbyCode)
    
    def hideLobbyCode(self,event):
        event.widget.configure(text = "Hover over for lobby code")

    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def getBackgroundColor(self):
        return self.background

# def main():
#     root = rootWindow(width = 1000,height = 600,background = "#e9f2f5")
#     root.mainloop()

# main()