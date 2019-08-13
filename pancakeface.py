import pygame
import sys
import math
from point import Point
from pygame.locals import *
import pygame
import sys
import math
from point import Point
from pygame.locals import *
from pygame.color import THECOLORS
pygame.init()
Brack=[0,0,0]
Green=[0,255,0]
Red=[255,0,0]
White=[255,255,255]
size=[[770,260],[850,260],[950,260],[800,370],[925,370],[800,470],[925,470]]
s0="微辣,"
s1="加鸡蛋,"
s2="加薄脆"
text_size=16
screen = pygame.display.set_mode((1280,720),FULLSCREEN,32)
screen.fill(Brack)
pygame.draw.rect(screen,White,[225,235,250,250],0)
text0=pygame.font.Font("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",22)
text=pygame.font.Font("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",text_size)
text_fmt=text0.render("煎 饼 控 制 界 面",1,Brack)
screen.blit(text_fmt,(275,280))
class PancakeFace(object):
    def Choice(self):
        pygame.draw.rect(screen,White,[740,155,350,430],0)
        pygame.draw.rect(screen,Brack,[865,520,100,30],2)
        pygame.draw.rect(screen,Green,[867,522,97,27],0)
        img0=pygame.image.load("a.png")
        screen.blit(img0,(550,80))
        button1=text.render("确    定",1,Brack)
        screen.blit(button1,(892,522))
        for i in range(7):
            pygame.draw.circle(screen,Brack,size[i],10,1)
            pygame.draw.circle(screen,Brack,[770,260],4,0)
            pygame.draw.circle(screen,Brack,[800,370],4,0)
            pygame.draw.circle(screen,Brack,[800,470],4,0)
    def add_log(self,s):
        pygame.draw.rect(screen,White,[740,155,350,430],0)
        text_fmt0=text0.render("煎 饼 机 工 作 状 态",1,Brack)
        screen.blit(text_fmt0,(820,200))
        pygame.draw.rect(screen,[96,96,96],[788,263,254,264],2)
        pygame.draw.rect(screen,[230,230,230],[790,265,250,260],0)
        text_fmt1=text.render(s,1,Brack)
        screen.blit(text_fmt1,(800,280))
    def Main(self):
        global s0,s1,s2
        color=Green
        words="开   始"
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        exit()
                elif event.type == QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pressed_array = pygame.mouse.get_pressed()
                    pos = pygame.mouse.get_pos()
                    a=Point().area([pos[0],pos[1]],[770,260])
                    b=Point().area([pos[0],pos[1]],[850,260])
                    c=Point().area([pos[0],pos[1]],[950,260])
                    d=Point().area([pos[0],pos[1]],[800,370])
                    e=Point().area([pos[0],pos[1]],[925,370])
                    f=Point().area([pos[0],pos[1]],[800,470])
                    g=Point().area([pos[0],pos[1]],[925,470])
                    if 300<=pos[0]<=400 and 400<=pos[1]<=430:
                        for index in range(len(pressed_array)):
                            if pressed_array[index]:
                                if index == 0:
                                    if color==Green:
                                        color=Red
                                        words="取   消"
                                        PancakeFace().Choice()
                                    elif color==Red:
                                        exit()
                    elif a<=10:
                        s0="微辣,"
                        pygame.draw.circle(screen,Brack,[770,260],4,0)
                        pygame.draw.circle(screen,White,[850,260],4,0)
                        pygame.draw.circle(screen,White,[950,260],4,0)
                    elif b<=10:
                        s0="中辣,"
                        pygame.draw.circle(screen,Brack,[850,260],4,0)
                        pygame.draw.circle(screen,White,[770,260],4,0)
                        pygame.draw.circle(screen,White,[950,260],4,0)
                    elif c<=10:
                        s0="特辣,"
                        pygame.draw.circle(screen,Brack,[950,260],4,0)
                        pygame.draw.circle(screen,White,[770,260],4,0)
                        pygame.draw.circle(screen,White,[850,260],4,0)
                    elif d<=10:
                        s1="加鸡蛋,"
                        pygame.draw.circle(screen,Brack,[800,370],4,0)
                        pygame.draw.circle(screen,White,[925,370],4,0)
                    elif e<=10:
                        s1="不加鸡蛋,"
                        pygame.draw.circle(screen,Brack,[925,370],4,0)
                        pygame.draw.circle(screen,White,[800,370],4,0)
                    elif f<=10:
                        s2="加薄脆"
                        pygame.draw.circle(screen,Brack,[800,470],4,0)
                        pygame.draw.circle(screen,White,[925,470],4,0)
                    elif g<=10:
                        s2="加油条"
                        pygame.draw.circle(screen,Brack,[925,470],4,0)
                        pygame.draw.circle(screen,White,[800,470],4,0)
                    elif 865<=pos[0]<=965 and 520<=pos[1]<=550:
                        s="开始制作,"+s0+s1+s2
                        PancakeFace().add_log(s)
            pygame.draw.rect(screen,[0,0,0],[300,400,100,30],2)
            pygame.draw.rect(screen,color,[302,402,97,27],0)
            button=text.render(words,1,Brack)
            screen.blit(button,(330,402))
            pygame.display.update()
PancakeFace().Main()
