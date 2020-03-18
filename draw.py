import turtle

def drawCellTowers(x1,y1,x2,y2,x3,y3,x,y,color):
  myPen = turtle.Turtle()
  myPen.hideturtle()

  myPen.speed(0)
  
  
  window = turtle.Screen()
  window.bgcolor("#F0F0F0")
  
  r1 = ((x-x1)**2 + (y-y1)**2)**0.5
  r2 = ((x-x2)**2 + (y-y2)**2)**0.5
  r3 = ((x-x3)**2 + (y-y3)**2)**0.5


  myPen.color("#ff5744")
  myPen.penup()
  myPen.goto(x1-5,y1)
  myPen.pendown()
  myPen.goto(x1+5,y1)
  myPen.penup()
  myPen.goto(x1,y1-5)
  myPen.pendown()
  myPen.goto(x1,y1+5)
  myPen.penup()

  myPen.goto(x1,y1-r1)
  myPen.pendown()
  myPen.circle(r1)
  
  myPen.color("#41befc")
  myPen.penup()
  myPen.goto(x2-5,y2)
  myPen.pendown()
  myPen.goto(x2+5,y2)
  myPen.penup()
  myPen.goto(x2,y2-5)
  myPen.pendown()
  myPen.goto(x2,y2+5)
  myPen.penup()
  
  myPen.goto(x2,y2-r2)
  myPen.pendown()
  myPen.circle(r2)
  myPen.penup()
  
  myPen.color("#52bf54")
  myPen.goto(x3-5,y3)
  myPen.pendown()
  myPen.goto(x3+5,y3)
  myPen.penup()
  myPen.goto(x3,y3-5)
  myPen.pendown()
  myPen.goto(x3,y3+5)
  
  myPen.penup()
  myPen.goto(x3,y3-r3)
  myPen.pendown()
  myPen.circle(r3)
  
  myPen.setpos(x,y)
  myPen.dot(5, color)
    

  
  myPen.getscreen().update()
  return x1,y1,r1,x2,y2,r2,x3,y3,r3
