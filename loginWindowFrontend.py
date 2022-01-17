import tkinter
from clientConnection import connectToServer
from client import privateLobbyPlayer
from privateLobbyConfigurationWindow import privateLobbyConfigWindow
class loginWindow(tkinter.Tk):
    def __init__(self,width,height,background):
        super().__init__()
        self.geometry("%dx%d+250+100"%(width,height))
        self.configure(bg = background)
        self.title("login")
        self.columnconfigure(0,weight = 1)
        self.rowconfigure(0,weight = 1)
        self.rowconfigure(2,weight = 1)
        self.width = width
        self.height = height
        self.background = background
        self.nameEntryField = -1
        self.avatar = ''
        self.radioButtonState = tkinter.IntVar()
        self.gettingDestroyed = False
        self.widgetAssembler()
        self.mainloop()

    def widgetAssembler(self):
        #container frame for name label and entry field
        nameContainerFrame = tkinter.Frame(
            master = self,bg = self.background,bd = 0
        )
        nameContainerFrame.grid(row = 0,column = 0,sticky = tkinter.S)

        #enter your name label
        nameLabel = tkinter.Label(
            master = nameContainerFrame,text = "Enter your name",bg = self.background,font = ("Segoe UI",20)
        )
        nameLabel.grid(row = 0,column = 0,pady = 17)

        #enter your name entry field
        self.nameEntryField = tkinter.Entry(
            master = nameContainerFrame,bg = "#ffffff",width = 50,font = ("Segoe UI",17),highlightthickness = 2,
            highlightcolor = "#0073ff",highlightbackground = self.background
        )
        self.nameEntryField.grid(row = 1,column = 0)

        #avatar radiobutton container frame
        avatarContainerFrame = tkinter.Frame(
            master = self, bg = self.background, bd = 0
        )
        avatarContainerFrame.grid(row = 1, column = 0)
        avatarContainerFrame.columnconfigure(0,weight = 1)
        avatarContainerFrame.columnconfigure(1,weight = 1)

        #male avatar radio button
        maleAvatarImage = tkinter.PhotoImage(file = "images/male.png")
        maleAvatarRadioButton = tkinter.Radiobutton(
            master = avatarContainerFrame, bg = self.background, bd = 0,
            image = maleAvatarImage, text = "Male", compound = tkinter.TOP,
            variable = self.radioButtonState, value = 1, command = self.maleRadioButton
        )
        maleAvatarRadioButton.grid(row = 0, column = 0, sticky = tkinter.W)
        maleAvatarRadioButton.image = maleAvatarImage

        #female avatar radio button
        femaleAvatarImage = tkinter.PhotoImage(file = "images/female.png")
        femaleAvatarRadioButton = tkinter.Radiobutton(
            master = avatarContainerFrame, bg = self.background, bd = 0,
            image = femaleAvatarImage, text = "female", compound = tkinter.TOP,
            variable = self.radioButtonState, value = 2, command = self.femaleRadioButton
        )
        femaleAvatarRadioButton.grid(row = 0, column = 1, sticky = tkinter.E)
        femaleAvatarRadioButton.image = femaleAvatarImage

        #container frame for public and private lobby button
        buttonContainerFrame = tkinter.Frame(
            master = self,bg = self.background,bd = 0
        )
        buttonContainerFrame.grid(row = 2,column = 0,sticky = (tkinter.W,tkinter.E,tkinter.N))
        buttonContainerFrame.columnconfigure(0,weight = 1)
        buttonContainerFrame.rowconfigure(0,weight = 1)

        #button for public lobby
        publicLobbyButton = tkinter.Button(
            master = buttonContainerFrame,text = "Start game",bg = "#84ff00",bd = 0,font = ("Segoe UI",15),width = 50,
            activebackground = "#2aad37", command = self.initializePublicLobby
        )
        publicLobbyButton.grid(row = 0,column = 0,pady = 20)

        #button for creating private lobby
        privateLobbyButton = tkinter.Button(
            master = buttonContainerFrame,text = "Create a private lobby",bg = "#00ccff",bd = 0,width = 50,font = ("Segoe UI",15),
            activebackground = "#23aacc", command = self.initializePrivateLobby
        )
        privateLobbyButton.grid(row = 1,column = 0)

        #join private lobby button
        joinPrivateLobbyButton = tkinter.Button(
            master = buttonContainerFrame, text = "Join a private lobby", bg = "#ff0073", bd = 0,
            width = 50, font = ("Segoe UI",15), activebackground = "#c42f72",command = self.joinPrivateLobby
        )
        joinPrivateLobbyButton.grid(row = 2, column = 0,pady = 20)
    
    def maleRadioButton(self):
        if(self.radioButtonState.get()==1):
            self.avatar = "male"
    
    def femaleRadioButton(self):
        if(self.radioButtonState.get()==1):
            self.avatar = "female"
    
    def initializePublicLobby(self):
        message = {
            "name": self.nameEntryField.get(),
            "avatar": self.avatar
        }
        connectToServer.createRequestMessage(messageType="join a public lobby", messageDictionary=message)
        self.gettingDestroyed = True
    
    def initializePrivateLobby(self):
        message = {
            "name": self.nameEntryField.get(),
            "avatar": self.avatar
        }
        connectToServer.createRequestMessage(messageType="create a private lobby", messageDictionary=message)
        self.gettingDestroyed = True

    def joinPrivateLobby(self):
        message = {
            "name": self.nameEntryField.get(),
            "avatar": self.avatar,
            "lobbyCode": 000000
        }
        connectToServer.createRequestMessage(messageType="join a private lobby", messageDictionary=message)
        self.gettingDestroyed = True
    
    def isGettingDestroyed(self):
        return self.gettingDestroyed
        
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def getBackgroundColor(self):
        return self.background