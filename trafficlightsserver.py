## Traffic Lights server for coders who don't have the opportunity to reprogram their city traffic light system.

## Pretty poorly made, this is only v1. I'll eventually have cars, sensors, etc.

import tkinter
import socket

root = tkinter.Tk()
root.resizable(False, False)
canvas = tkinter.Canvas(root, width = 500, height = 500)
canvas.pack()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 2000
while 1:
    try:
        sock.bind(("", port))
        break
    except:
        port += 1
sock.listen(20)
print("Bound socket to all addresses on port", port)


#class Car:
#    def __init__(self, canvas, width, height, x, y):
#        self.x = x
#        self.y = y
#        self.width = width
#        self.height = height
#        self.id = canvas.create_rectangle(x - width/2, y - height/2, x + width/2, y + height/2, fill = "brown")
#        self.direction = [0, 1] ## Vector x and y.


def centerRectToCornerRect(x, y, width, height):
    return [x - width/2, y - height/2, x + width/2, y + height/2]

class Intersection: ## Traffic lights and etc
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3
    GREEN = 0
    RED = 1
    YELLOW = 2
    def __init__(self, canvas, x, y, lightDist):
        self.topPos = [x, y - lightDist]
        self.bottomPos = [x, y + lightDist]
        self.rightPos = [x - lightDist, y]
        self.leftPos = [x + lightDist, y]
        self.topID = canvas.create_rectangle(*centerRectToCornerRect(*self.topPos, 10, 10), fill = "green")
        self.bottomID = canvas.create_rectangle(*centerRectToCornerRect(*self.bottomPos, 10, 10), fill = "green")
        self.leftID = canvas.create_rectangle(*centerRectToCornerRect(*self.leftPos, 10, 10), fill = "green")
        self.rightID = canvas.create_rectangle(*centerRectToCornerRect(*self.rightPos, 10, 10), fill = "green")
        self.canvas = canvas
    def set(self, which, col):
        idToEdit = 0
        if which == Intersection.TOP:
            idToEdit = self.topID
        elif which == Intersection.BOTTOM:
            idToEdit = self.bottomID
        elif which == Intersection.LEFT:
            idToEdit = self.leftID
        elif which == Intersection.RIGHT:
            idToEdit = self.rightID
        if col == Intersection.RED:
            self.canvas.itemconfig(idToEdit, fill = "red")
        elif col == Intersection.GREEN:
            self.canvas.itemconfig(idToEdit, fill = "green")
        elif col == Intersection.YELLOW:
            self.canvas.itemconfig(idToEdit, fill = "yellow")
    def reset(self, canvas):
        self.canvas = canvas
        self.topID = canvas.create_rectangle(*centerRectToCornerRect(*self.topPos, 10, 10), fill = "green")
        self.bottomID = canvas.create_rectangle(*centerRectToCornerRect(*self.bottomPos, 10, 10), fill = "green")
        self.leftID = canvas.create_rectangle(*centerRectToCornerRect(*self.leftPos, 10, 10), fill = "green")
        self.rightID = canvas.create_rectangle(*centerRectToCornerRect(*self.rightPos, 10, 10), fill = "green")


class StreetGrid:
    def __init__(self, canvas, streetdist = 100, streetthickness = 10):
        self.intersections = []
        self.roads = []
        self.canvas = canvas
        self.streetdist = streetdist
        self.streetthickness = streetthickness
        self.propagateRoads(5, 5)
        self.intersections = []
        self.edgeIntersections = []
        self.setIntersections(5, 5)
    def propagateRoads(self, width, height):
        for x in range(0, width):
            self.roads.append(self.canvas.create_rectangle((x + 0.5) * self.streetdist - int(self.streetthickness/2), 0, (x + 0.5) * self.streetdist + int(self.streetthickness/2), 500, fill = "beige"))
        for y in range(0, height):
            self.roads.append(self.canvas.create_rectangle(0, (y + 0.5) *  self.streetdist - int(self.streetthickness/2), 500, (y + 0.5) * self.streetdist + int(self.streetthickness/2), fill = "beige"))
    def setIntersections(self, width, height):
        for x in range(0, width):
            for y in range(0, height):
                self.intersections.append(Intersection(canvas, (x + 0.5) * self.streetdist, (y + 0.5) * self.streetdist, 15))
    def getIntersection(self, x, y):
        return self.intersections[y * 5 + x]
    def reset(self, canvas):
        self.canvas = canvas
        self.propagateRoads(5, 5)
        for x in self.intersections:
            x.reset(canvas)
    
streets = StreetGrid(canvas)

def reset():
    root = tkinter.Tk()
    root.resizable(False, False)
    canvas = tkinter.Canvas(root, width = 500, height = 500)
    canvas.pack()
    streets.reset(canvas)

#cars = []
#for x in streets.edgeIntersections:
#    cars.append(Car(canvas, 30, 30, *x))
## I commented all the cars code, this is V1 people.
while 1:
    client = sock.accept()[0] ## Blocking.
    playing = True
    print("Got a connection!")
    while playing:
        d = client.recv(1).decode()
        if d == "S": ## Set light
            x = int.from_bytes(client.recv(1), "little") % 5
            y = int.from_bytes(client.recv(1), "little") % 5
            side = int.from_bytes(client.recv(1), "little")
            color = int.from_bytes(client.recv(1), "little")
            streets.getIntersection(x, y).set(side, color)
        elif d == "U": ## Update
            root.update()
            root.update_idletasks()
        elif d == "E": ## Exit
            client.close()
            playing = False
        elif d == "D": ## Destroy GUI
            root.destroy()
        elif d == "R": ## Reset
            print("Resetting")
            reset()
    print("Lost a client, now I must move on!")
