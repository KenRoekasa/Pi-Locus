import turtle
from random import randint

def drawCellTowers(x1,y1,x2,y2,x3,y3,x,y):
  myPen = turtle.Turtle()
  myPen.hideturtle()

  myPen.speed(0)
  
  
  window = turtle.Screen()
  window.bgcolor("#F0F0F0")
  
  r1 = ((x-x1)**2 + (y-y1)**2)**0.5
  r2 = ((x-x2)**2 + (y-y2)**2)**0.5
  r3 = ((x-x3)**2 + (y-y3)**2)**0.5
  
  myPen.setpos(x,y)
  myPen.dot(20, "blue")
    

  
  myPen.getscreen().update()
  return x1,y1,r1,x2,y2,r2,x3,y3,r3
