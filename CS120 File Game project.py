# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 14:49:39 2023

@author: Braden
"""

import simpleGE, pygame, random


class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()

        self.buttonReset = ButtonReset()
        self.buttonQuit = ButtonQuit()
        self.startPage = StartPage()
        self.yourPlane = YourPlane(self)
        self.enemyPlanes = []

        for i in range(3):
            enemy_plane = EnemyPlane(self)
            self.enemyPlanes.append(enemy_plane)
        
        self.bullet = Bullet(self, self.yourPlane)
        self.bullet = []
        self.health = 5
        self.score = 0
        self.lblHealth = simpleGE.Label()
        self.lblHealth.text = f"HP: {self.health}"
        self.lblHealth.center = (570, 50)
        self.lblHealth.hide()

        self.lblScore = simpleGE.Label()
        self.lblScore.text = f"Score: {self.score}"
        self.lblScore.center = (50, 50)
        self.lblScore.hide()

        self.sprites = [self.yourPlane, self.startPage, self.buttonReset, self.buttonQuit, self.enemyPlanes, self.lblHealth, 
                        self.lblScore, self.bullet]

        self.instructions()

    def instructions(self):
        self.backgroundImage1 = pygame.image.load("Images/Start Page background image.PNG")
        self.backgroundImage1 = pygame.transform.scale(self.backgroundImage1, (640, 480))
        self.background.blit(self.backgroundImage1,(0,0))
        self.buttonQuit.hide()
        self.buttonReset.hide()
        self.startPage.show((320, 240))
        self.yourPlane.hide()
        for sprite in self.enemyPlanes:
            sprite.hide()
            
        for bullet in self.bullet:
            bullet.update()
            self.hide()
        
    
    def pauseGame(self):
        self.backgroundImage3 = pygame.image.load("Images/Game Over background Image.PNG")
        self.backgroundImage3 = pygame.transform.scale(self.backgroundImage3, (640,480))
        self.background.blit(self.backgroundImage3, (0,0))
        self.buttonQuit.show((220, 240))
        self.buttonReset.show((420, 240))
        self.startPage.hide()
        self.yourPlane.hide()
        self.lblHealth.hide()
        self.lblScore.hide()
        for sprite in self.enemyPlanes:
            sprite.hide()
        
        for bullet in self.bullet:
            bullet.update()
            self.hide()
    def playGame(self):
        self.backgroundImage2 = pygame.image.load("Images/deep_ocean_battlemap.png")
        self.backgroundImage2 = pygame.transform.scale(self.backgroundImage2, (640,480))
        self.background.blit(self.backgroundImage2, (0,0))
        self.startPage.hide()
        self.buttonQuit.hide()
        self.buttonReset.hide()
        self.yourPlane.show()
        self.lblHealth.show((570,50))
        self.lblScore.show((50,50))
        for sprite in self.enemyPlanes:
            sprite.show()
            
        for bullet in self.bullet:
            bullet.update()
            self.show()


    def update(self):
        
        if self.startPage.clicked:
            self.playGame()
        if self.buttonQuit.clicked:
            self.stop()
        if self.buttonReset.clicked:
            self.playGame()
        if self.health == 0:
            self.pauseGame()


class YourPlane(simpleGE.SuperSprite):
    
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage('D:/CS120/Images/fighter jet.png')
        self.setSize(100, 100)
        self.setPosition((320, 240))
        self.moveSpeed = 15
        self.y = 400

        self.bullet = Bullet(self, parent = self)    

    def checkEvents(self):
        
        if self.scene.isKeyPressed(pygame.K_d):
            self.x += self.moveSpeed
            self.bullet.fire()
        if self.scene.isKeyPressed(pygame.K_a):
            self.x -= self.moveSpeed
            self.bullet.fire()
        if self.scene.isKeyPressed(pygame.K_w):
            self.y -= self.moveSpeed
            self.bullet.fire()
        if self.scene.isKeyPressed(pygame.K_s):
            self.y += self.moveSpeed
            self.bullet.fire()
                
        self.checkBounds()
        self.checkCollisions()
        
    def checkCollisions(self):
        for enemy_plane in self.scene.enemyPlanes:
            if self.collidesWith(enemy_plane):
                enemy_plane.reset()
          
    def checkBounds(self):
        if self.rect.bottom > self.screen.get_height():
            self.changeYby(-8.5)
            self.setDX(0)
            self.setDY(0)
        if self.rect.top < 0:
            self.changeYby(8.5)
            self.setDX(0)
            self.setDY(0)
        if self.rect.right > self.screen.get_width():
            self.changeXby(-8.5)
            self.setDX(0)
            self.setDY(0)
        if self.rect.left < 0:
            self.changeXby(8.5)
            self.setDX(0)
            self.setDY(0)

    

class Bullet(simpleGE.SuperSprite):
    
    def __init__(self, scene, parent):
        super().__init__(scene)
        self.parent = parent
        self.imageMaster = pygame.Surface((5,5))
        self.imageMaster.fill(pygame.Color("white"))
        self.setBoundAction(self.HIDE)
        self.hide()
    
    def fire(self):
        self.show()
        self.setPosition(self.parent.rect.center)
        self.setMoveAngle(self.parent.rotation)
        self.setSpeed(20)
        
        
    
class EnemyPlane(simpleGE.BasicSprite):
    
    def __init__(self, scene):
        
        super().__init__(scene)
        self.setImage('D:/CS120/Images/enemy fighter jet.png')
        self.setSize(50, 50)
        self.moveSpeed = 1
        self.y = 10
        self.reset()
        
    def reset(self):
        
        newX = random.randint(0, 640)
        self.x = newX
        self.y = 10
        self.dy = 5
        
    def checkEvents(self):
        
        if self.collidesWith(self.scene.yourPlane):
            self.scene.health -= 1
            self.scene.lblHealth.text = f"HP: {self.scene.health}"
            self.reset()
            self.scene.score += 1
            self.scene.lblScore.text = f"Score: {self.scene.score}"
            
    def checkBounds(self):
        
        if self.rect.bottom > self.screen.get_height():
            self.reset()
        if self.rect.top > self.screen.get_height():
            self.reset()
        if self.rect.right > self.screen.get_width():
            self.reset()
        if self.rect.left > self.screen.get_width():
            self.reset()
            

class StartPage(simpleGE.MultiLabel):
    
    def __init__(self):
        super().__init__()
        self.textLines = [
            "This is my fighter jet game",
            "The goal is to destroy enemy planes",
            "Press the WASD keys to move",
            "Press this label to start"
            ]
        self.center = ((320,240))
        self.size = ((320,120))
        
class ButtonQuit(simpleGE.Button):
    
    def __init__(self):
        super().__init__()
        self.text = "Quit"
        self.hide()
        
class ButtonReset(simpleGE.Button):
    
    def __init__(self):
        super().__init__()
        self.text = "Reset"
        self.hide()





def main():
    
    game = Game()
    game.start()

    
if __name__ == "__main__":
    main()
            
            
            
            
            
            























