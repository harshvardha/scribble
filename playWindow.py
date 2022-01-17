import tkinter
from tkinter import colorchooser
class player:
    def __init__(self,rank,name,points,avatar):
        self.rank = rank
        self.name = name
        self.points = points
        self.avatar = avatar
    
    def getRank(self):
        return self.rank
    
    def getName(self):
        return self.name
    
    def getPoints(self):
        return self.points
    
    def getAvatar(self):
        return self.avatar

class listElementStructure(tkinter.Frame):
    def __init__(self,master,background,playerRank,playerName,playerPoint,playerAvatar):
        super().__init__(master = master,bg = 'white')
        self.columnconfigure(0,weight = 1)
        self.columnconfigure(1,weight = 1)
        self.columnconfigure(2,weight = 1)
        self.rowconfigure(0,weight = 1)
        self.master = master
        self.background = background
        self.playerRank = playerRank
        self.playerName = playerName
        self.playerPoint = playerPoint
        self.playerAvatar = playerAvatar
        self.rankLabel = None
        self.pointsLabel = None
        self.createStructure()
    
    def createStructure(self):
        #player rank label
        self.rankLabel = tkinter.Label(
            master = self,text = "#"+self.playerRank,bg = 'white',font = ("Segoe UI",11)
        )
        self.rankLabel.grid(row = 0,column = 0,sticky = (tkinter.W,tkinter.N,tkinter.S))

        #container frame for name label and points label
        containerFrame = tkinter.Frame(
            master = self,bg = 'white'
        )
        containerFrame.grid(row = 0,column = 1,padx = 20,sticky = (tkinter.E,tkinter.W,tkinter.S,tkinter.N))
        containerFrame.columnconfigure(0,weight = 1)
        containerFrame.rowconfigure(0,weight = 1)
        containerFrame.rowconfigure(1,weight = 1)

        #player name label

        nameLabel = tkinter.Label(
            master = containerFrame,text = self.playerName,font = ("Segoe UI",10),bg = 'white'
        )
        nameLabel.grid(row = 0,column = 0)

        #player points label
        self.pointsLabel = tkinter.Label(
            master = containerFrame,text = "Points : "+self.playerPoint,font = ("Segoe UI",10),bg = 'white'
        )
        self.pointsLabel.grid(row = 1,column = 0,sticky = tkinter.N)

        #player avatar label
        playerAvatarImage = tkinter.PhotoImage(file = self.playerAvatar)
        avatarLabel = tkinter.Label(
            master = self,image = playerAvatarImage,bg = 'white'
        )
        avatarLabel.image = playerAvatarImage
        avatarLabel.grid(row = 0,column = 2,sticky = (tkinter.E,tkinter.S,tkinter.N))

    def updatePlayerRank(self,newPlayerRank):
        self.playerRank = newPlayerRank
        self.rankLabel.configure(text = self.playerRank)
    
    def updatePlayerPoints(self,newPlayerPoints):
        self.playerPoint = newPlayerPoints
        self.pointsLabel.configure(text = self.playerPoint)

class playerListFrame(tkinter.Frame):
    def __init__(self,master,background):
        super().__init__(master = master, bg = background)
        self.columnconfigure(0,weight = 1)
        for i in range(10):
            self.rowconfigure(i,weight = 1)
        self.master = master
        self.background = background
        self.row = 0
    
    def addNewPlayers(self,noOfNewPlayers,newPlayersObjectList):
        for i in range(noOfNewPlayers):
            self.row += 1
            newPlayersObjectList[i].grid(row = self.row,column = 0)
    
    def addPlayer(self,playerObject):
        playerObject.grid(row = self.row,column = 0,pady = 5,sticky = (tkinter.E,tkinter.W,tkinter.N,tkinter.S))
        self.row += 1
    
    def removePlayer(self,playerObjectToRemove):
        playerObjectToRemove.destroy()
        self.row -= 1

class drawingArea(tkinter.Frame):
    def __init__(self,master,background):
        super().__init__(master = master, bg = background)
        self.master = master
        self.background = background
        self.columnconfigure(0,weight = 1)
        self.rowconfigure(0,weight = 1)
        self.selectedColor = '#000000'
        self.drawingCanvas = None
        self.createStructure()
    
    def createStructure(self):
        #canvas widget for painting or drawing
        self.drawingCanvas = tkinter.Canvas(
            master = self,bg = 'white',bd = 0
        )
        self.drawingCanvas.grid(row = 0,column = 0,sticky = (tkinter.E,tkinter.W,tkinter.N,tkinter.S))

        #container frame for paint options button
        paintOptionsContainerFrame = tkinter.Frame(
            master = self.master,bg = 'black',bd = 0
        )
        paintOptionsContainerFrame.grid(row = 1,column = 1,sticky = (tkinter.W,tkinter.E,tkinter.S,tkinter.N))
        for i in range(5):
            paintOptionsContainerFrame.columnconfigure(i,weight = 1)
        
        #choose color button
        chooseColotButtonImage = tkinter.PhotoImage(file = 'images/color_palette.png')
        chooseColorButton = tkinter.Button(
            master = paintOptionsContainerFrame,image = chooseColotButtonImage,bg = 'white',bd = 0,activebackground = self.background,
            command = self.openColorChooser
        )
        chooseColorButton.grid(row = 0,column = 0,sticky = (tkinter.W,tkinter.E,tkinter.S,tkinter.N))
        chooseColorButton.image = chooseColotButtonImage

        #paint bucket button
        paintBucketImage = tkinter.PhotoImage(file = 'images/paint_bucket.png')
        paintBucketButton = tkinter.Button(
            master = paintOptionsContainerFrame,image = paintBucketImage,bg = 'white',bd = 0,activebackground = self.background,
            command = self.pourColorOnCanvas
        )
        paintBucketButton.grid(row = 0,column = 1,sticky = (tkinter.W,tkinter.E,tkinter.S,tkinter.N))
        paintBucketButton.image = paintBucketImage

        #paint brush button
        paintBrushImage = tkinter.PhotoImage(file = 'images/paint_brush.png')
        paintBrushButton = tkinter.Button(
            master = paintOptionsContainerFrame,image = paintBrushImage,bg = 'white',bd = 0,activebackground = self.background,
            command = self.draw
        )
        paintBrushButton.grid(row = 0,column = 2,sticky = (tkinter.W,tkinter.E,tkinter.S,tkinter.N))
        paintBrushButton.image = paintBrushImage

        #eraser button
        eraserImage = tkinter.PhotoImage(file = 'images/eraser.png')
        eraserButton = tkinter.Button(
            master = paintOptionsContainerFrame,image = eraserImage,bg = 'white',bd = 0,activebackground = self.background,
            command = self.erase
        )
        eraserButton.grid(row = 0,column = 3,sticky = (tkinter.W,tkinter.E,tkinter.S,tkinter.N))
        eraserButton.image = eraserImage

        #clear all button
        clearAllImage = tkinter.PhotoImage(file = 'images/trash.png')
        clearAllButton = tkinter.Button(
            master = paintOptionsContainerFrame,image = clearAllImage,bg = 'white',bd = 0,activebackground = self.background,
            command = self.clearDrawingArea
        )
        clearAllButton.grid(row = 0,column = 4,sticky = (tkinter.W,tkinter.E,tkinter.S,tkinter.N))
        clearAllButton.image = clearAllImage
    
    def openColorChooser(self):
        self.selectedColor = colorchooser.askcolor()[1]
    
    def pourColorOnCanvas(self):
        self.drawingCanvas.configure(bg = self.selectedColor)
    
    def draw(self):
        self.drawingCanvas.bind("<B1-Motion>",self.mouseMotionDrawing)
    
    def erase(self):
        self.selectedColor = '#ffffff'
        self.drawingCanvas.bind("<B1-Motion>",self.mouseMotionDrawing)
    
    def clearDrawingArea(self):
        self.drawingCanvas.delete("all")
        self.drawingCanvas.configure(bg = 'white')
    
    def mouseMotionDrawing(self,event):
        x = event.x
        y = event.y
        self.drawingCanvas.create_arc(x-1,y-1,x+1,y+1,fill = self.selectedColor,outline = self.selectedColor,width = 10)
    
class playerGuessDisplayFrame(tkinter.Frame):
    def __init__(self, master, background):
        super().__init__(master = master, bg = background)
        self.master = master
        self.columnconfigure(0,weight = 1)
        self.rowconfigure(0,weight = 1)
        self.background = background
        self.createStructure()
    
    def createStructure(self):
        #container frame for labels displaying the guessess made by players
        guesserContainerFrame = tkinter.Frame(
            master  = self,bg = self.background
        )
        guesserContainerFrame.grid(row = 0,column = 0,sticky = (tkinter.W,tkinter.E,tkinter.N))

        #guessing player and player guess labels container frame
        guessContainerFrame = tkinter.Frame(
            master = guesserContainerFrame,bg = self.background
        )
        guessContainerFrame.grid(row = 0,column = 0,sticky = (tkinter.W,tkinter.E,tkinter.S))

        #label displaying guessing player
        guessingPlayerLabel = tkinter.Label(
            master = guessContainerFrame,text = 'Harshvardhan : ',bg = 'grey',font = ("Segoe UI",10,"bold")
        )
        guessingPlayerLabel.grid(row = 0,column = 0,sticky = tkinter.W)

        #player guess label
        playerGuessLabel = tkinter.Label(
            master = guessContainerFrame,text = 'hello',bg = 'grey',font = ("Segoe UI",10)
        )
        playerGuessLabel.grid(row = 0,column = 1,sticky = tkinter.W)

        #entry widget for writing your guess
        guessEntryWidget = tkinter.Entry(
            master = self,bg = 'white',font = ("Segoe UI",10),width = 43
        )
        guessEntryWidget.grid(row = 0,column = 0,sticky = (tkinter.W,tkinter.E,tkinter.S))

class rootWindow(tkinter.Tk):
    def __init__(self, width, height, background, noOfPlayers, listOfPlayerObjects):
        super().__init__()
        self.geometry("%dx%d+250+100"%(width,height))
        self.configure(bg = background)
        self.columnconfigure(1,weight = 1)
        self.rowconfigure(0,weight = 1)
        self.width = width
        self.height = height
        self.background = background
        self.noOfPlayers = noOfPlayers
        self.listOfPlayerObjects = listOfPlayerObjects
        self.playerListUI()
        self.drawingCanvasUI()
        self.wordGuessingUI()

    def playerListUI(self):
        #players list creater
        listFrame = playerListFrame(
            master = self,background = self.background
        )
        listFrame.grid(row = 0,column = 0,pady = 40,padx = 20,sticky = (tkinter.S,tkinter.N))
        for i in range(self.noOfPlayers):
            listElement = listElementStructure(
                master = listFrame,background = '#f2f2f2',playerRank = self.listOfPlayerObjects[i].getRank(),
                playerName = self.listOfPlayerObjects[i].getName(),playerPoint = self.listOfPlayerObjects[i].getPoints(),
                playerAvatar = self.listOfPlayerObjects[i].getAvatar()
            )
            listFrame.addPlayer(listElement)
    
    def drawingCanvasUI(self):
        #initializing drawingArea object to create drawing area for user
        userDrawingArea = drawingArea(
            master = self,background = self.background
        )
        userDrawingArea.grid(row = 0,column = 1,sticky = (tkinter.W,tkinter.E,tkinter.N,tkinter.S),pady = 43)
    
    def wordGuessingUI(self):
        guesser = playerGuessDisplayFrame(
            master = self,background = 'white'
        )
        guesser.grid(row = 0,column = 2,sticky = (tkinter.N,tkinter.S,tkinter.W,tkinter.E),pady = 45,padx = 20)
    
    def updateNoOfPlayers(self,noOfNewPlayers,listOfNewPlayerObjects):
        self.noOfPlayers += noOfNewPlayers
        for i in range(noOfNewPlayers):
            self.listOfPlayerObjects.append(listOfNewPlayerObjects[i])

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getBackground(self):
        return self.background

def main():
    root = rootWindow(
        width = 1000,height = 600,background = "#e9f2f5",noOfPlayers = 10,
        listOfPlayerObjects = [
            player('1','Harshvardhan',"0",'images/female.png'),
            player('2','Jaydev Sharma','100','images/male.png'),
            player('3','Mrityunjay','350','images/female.png'),
            player('4','CountZero','500','images/male.png'),
            player('5','mukul','700','images/male.png'),
            player('6','akshat','750','images/female.png'),
            player('7','lakshya','800','images/female.png'),
            player('8','dev','850','images/female.png'),
            player('9','abhishek','900','images/male.png'),
            player('10','tanish','950','images/male.png')])
    root.mainloop()

main()