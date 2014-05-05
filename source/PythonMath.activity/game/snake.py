import spyral
import copy
import random

headImage = spyral.Image('game/images/snakeHead.png')
bodyImage = spyral.Image('game/images/snakeBody.png')
tailImage = spyral.Image('game/images/snakeTail.png')

class Snake(object):
    def __init__(self, level, headPosition):
        self.x = headPosition[0]
        self.y = headPosition[1]
        self.level = level

        self.snakeTiles = []
        
        head = self.level.GetTile(headPosition[0],headPosition[1])
        head.image = headImage
        head.type = 'obstacle'
        self.snakeTiles.append(head)

        self.bodyLength = random.randint(1,5)
        for i in range(self.bodyLength):
            body = self.level.GetTile(self.x+i+1,self.y)
            body.image = bodyImage
            body.type = 'obstacle'
            self.snakeTiles.append(body)

        tail = self.level.GetTile(self.x+self.bodyLength+1,self.y)
        tail.image = tailImage
        tail.type = 'obstacle'

        self.snakeTiles.append(tail)

        spyral.event.register("input.keyboard.down.*", self.handleKeyboard)
	
    def ResetValues(self,headPosition):
        self.x = headPosition[0]
        self.y = headPosition[1]
        self.snakeTiles = []

        head = self.level.GetTile(headPosition[0],headPosition[1])
        head.image = headImage
        head.type = 'obstacle'
        self.snakeTiles.append(head)
        
        for i in range(self.bodyLength):
            body = self.level.GetTile(self.x+i+1,self.y)
            body.image = bodyImage
            body.type = 'obstacle'
            self.snakeTiles.append(body)

        tail = self.level.GetTile(self.x+self.bodyLength+1,self.y)
        tail.image = tailImage
        tail.type = 'obstacle'

        self.snakeTiles.append(tail)

    def handleKeyboard(self, key):
        if key == 276 or key == 260:
            self.moveLeft()
        elif key == 275 or key == 262:
            self.moveRight()
        elif key == 273 or key == 264:
            self.moveUp()
        elif key == 274 or key == 258:
            self.moveDown()

    def moveLeft(self):
        tileToInspect = self.level.GetTile(self.x,self.y - 1)
        if self.y - 1 > 0 and tileToInspect.type != 'obstacle':
            self.y -= 1
            self.changeTilesFromMovement(tileToInspect);
               
    def moveRight(self):
        tileToInspect = self.level.GetTile(self.x,self.y + 1)
        if self.y + 1 <= self.level.levelWidth and tileToInspect.type != 'obstacle':
            self.y += 1
            self.changeTilesFromMovement(tileToInspect);

    def moveUp(self):
        tileToInspect = self.level.GetTile(self.x - 1,self.y)
        if self.x - 1 > 0 and tileToInspect.type != 'obstacle':
            self.x -= 1
            self.changeTilesFromMovement(tileToInspect);

    def moveDown(self):
        tileToInspect = self.level.GetTile(self.x + 1,self.y)
        if self.x + 1 <= self.level.levelHeight and tileToInspect.type != 'obstacle':
            self.x += 1
            self.changeTilesFromMovement(tileToInspect);

    
    def changeTilesFromMovement(self,tile):

        oldType = tile.type
        oldAmmount = tile.amount

        lipos = []
        li = []
        for i in self.snakeTiles:
            li.append(i.image)
            lipos.append( (i.row, i.col ) )

        self.snakeTiles[0] = self.level.GetTile(self.x,self.y)
        self.snakeTiles[0].image = headImage
        self.snakeTiles[0].type = 'obstacle'

        for i in range(len(self.snakeTiles)):
            if i >= 1:
                self.snakeTiles[i] = self.level.GetTile(lipos[i-1][1]+1,lipos[i-1][0]+1)
                self.snakeTiles[i].image = li[i]
                self.snakeTiles[i].type = 'obstacle'

        self.level.GetTile(lipos[len(lipos)-1][1]+1,lipos[len(lipos)-1][0]+1).InitValues()

        if oldType == 'add':
            for i in range(oldAmmount):
                self.addTile()
        elif oldType == 'subtract':
            self.subtractTile(tile.amount)
        elif oldType == 'gate':
            self.level.goToNextLevel()

    def addTile(self):
        secondToLast = self.snakeTiles[len(self.snakeTiles)-2]
        tail = self.snakeTiles[len(self.snakeTiles)-1]

        directionX = secondToLast.col - tail.col
        directionY = secondToLast.row - tail.row
        
        if directionY == 1:
            self.snakeTiles[len(self.snakeTiles)-1] = self.level.GetTile(self.snakeTiles[len(self.snakeTiles)-1].col+1,self.snakeTiles[len(self.snakeTiles)-1].row)
            self.snakeTiles[len(self.snakeTiles)-1].image = tailImage

            newTile = self.level.GetTile(secondToLast.col+1,secondToLast.row)
            newTile.image = bodyImage
            self.snakeTiles.insert(len(self.snakeTiles)-1,newTile)

        if directionY == -1:
            self.snakeTiles[len(self.snakeTiles)-1] = self.level.GetTile(self.snakeTiles[len(self.snakeTiles)-1].col+1,self.snakeTiles[len(self.snakeTiles)-1].row+2)
            self.snakeTiles[len(self.snakeTiles)-1].image = tailImage

            newTile = self.level.GetTile(secondToLast.col+1,secondToLast.row+2)
            newTile.image = bodyImage
            self.snakeTiles.insert(len(self.snakeTiles)-1,newTile)

        if directionX == -1:
            self.snakeTiles[len(self.snakeTiles)-1] = self.level.GetTile(self.snakeTiles[len(self.snakeTiles)-1].col+2,self.snakeTiles[len(self.snakeTiles)-1].row+1)
            self.snakeTiles[len(self.snakeTiles)-1].image = tailImage
   
            newTile = self.level.GetTile(secondToLast.col+2,secondToLast.row+1)
            newTile.image = bodyImage
            self.snakeTiles.insert(len(self.snakeTiles)-1,newTile)

        if directionX == 1:
            self.snakeTiles[len(self.snakeTiles)-1] = self.level.GetTile(self.snakeTiles[len(self.snakeTiles)-1].col,self.snakeTiles[len(self.snakeTiles)-1].row+1)
            self.snakeTiles[len(self.snakeTiles)-1].image = tailImage
   
            newTile = self.level.GetTile(secondToLast.col,secondToLast.row+1)
            newTile.image = bodyImage
            self.snakeTiles.insert(len(self.snakeTiles)-1,newTile)
            

    def subtractTile(self, times=1):
        for i in range(times):
            #make sure the snake is never smaller than 3 tiles long
            if len(self.snakeTiles) >= 4:
                self.snakeTiles[len(self.snakeTiles)-1].InitValues()
                self.snakeTiles.pop()
                self.snakeTiles[len(self.snakeTiles)-1].image = tailImage