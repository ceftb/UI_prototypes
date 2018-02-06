# import the library
from appJar import gui

# handle button events
def press(button):
    if button == "Add Actor":
        app.stop()
    else:
        usr = app.getEntry("Username")
        pwd = app.getEntry("Password")
        print("User:", usr, "Pass:", pwd)

# create a GUI variable called app
app = gui("Experiment","600x400")
app.setBg("white")
app.setFont(18)
app.setSticky("news")
app.setStretch("both")

app.addButton("NewActor", press)
app.startLabelFrame("Actors", 0,0)
app.setSticky("ew")
app.setStretch("column")
app.addScrolledTextArea("t1")
app.stopLabelFrame()
app.startLabelFrame("Behavior", 0,1)
app.setSticky("ew")
app.setStretch("column")
app.addScrolledTextArea("t2")
app.stopLabelFrame()
app.startLabelFrame("Constraints", 1,0)
app.setSticky("ew")
app.setStretch("column")
app.addScrolledTextArea("t3")
app.stopLabelFrame()
app.startLabelFrame("Timeline", 1,1)
app.setSticky("ew")
app.setStretch("column")
app.stopLabelFrame()

# start the GUI
app.go()
