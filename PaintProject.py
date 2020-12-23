# Alec Mai
# PaintProject.py
# This is my version of Microsoft Paint with a legend of zelda theme. It has a twelve tools, twelve stamps,
# an undo function, a redo function, a clear function, a load function, a save function. It also displays what tool or
# stamp is currently hovered over or selected. There is also a colour selector function, there is also a display for the
# tool size, stamp size, and what the current colour is. There is also "music", it was supposed to be more pleasant.
from pygame import *
from random import *
from tkinter import *
from math import *


def line(x, y, ox, oy):  # Line is a function that gets all of the integer coordinates on a line (x,y)(ox,oy)
    points = []  # Point holds all of the integer coordinates
    dx = x - ox  # dx holds the difference between the two x values
    dy = y - oy  # dy holds the difference between the two y values
    if dx == 0:  # This if statement ensures that the slope calculation will not divide by zero
        slope = 0
    else:
        slope = dy / dx
    big = max(abs(dx), abs(dy))  # big finds and holds the largest absolute x or y value
    for i in range(big + 1):  # This loop checks to see if each x or y coordinate has a corresponding integer value
        if abs(dx) >= abs(dy):  # This if statement is used when the slope is less than one
            if ox > x:  # This if statement checks to see if the line is drawn in the negative x axis
                cx = ox - i  # cx holds the x coordinate to be checked
                xn = cx - ox  # xn holds the distance between cx and ox
                cy = xn * slope + oy  # cy holds the corresponding y cooridinate to cx
                cyn = int(round(cy, 0))  # cyn holds cy rounded to the nearest unit
            else:
                cx = ox + i
                xn = cx - ox
                cy = xn * slope + oy
                cyn = int(round(cy, 0))
            points.append([cx, cyn])
        elif abs(dy) > abs(dx) and slope != 0:  # This if statement is used when the slope is greater than one
            if oy > y:  # This if statement checks to see if the line is drawn in the negative y axis
                cy = oy - i  # this cy holds the y coordinate to be checked
                yn = cy - oy  # yn holds the distance between cy and oy
                cx = (yn) / slope + ox  # cx holds the corresponding x cooridinate to cy
                cxn = int(round(cx, 0))  # cxn holds cx rounded to the nearest unit
            else:
                cy = oy + i
                yn = cy - oy
                cx = (yn) / slope + ox
                cxn = int(round(cx, 0))
            points.append([cxn, cy])
        else:  # This triggeres when slope is zero
            # These find all the coordinates in straight lines in the x axis
            if oy > y:
                cy = oy - i
                cxn = ox
            else:
                cy = oy + i
                cxn = ox
            points.append([cxn, cy])
    return points


def blur(x, y):  # This function blurs by setting each pixel to the average of the four adjacent pixels
    if x > 250 and x < 1029 and y > 50 and y < 549:  # This if statement keeps the blur within the bounds of the canvas
        p1 = blursurface.get_at((x - 1, y))
        p2 = blursurface.get_at((x + 1, y))
        p3 = blursurface.get_at((x, y - 1))
        p4 = blursurface.get_at((x, y + 1))  # p1-p4 gets the colour of each adjacent pixel
        blurR = (p1[0] + p2[0] + p3[0] + p4[0]) / 4
        blurG = (p1[1] + p2[1] + p3[1] + p4[1]) / 4
        blurB = (p1[2] + p2[2] + p3[2] + p4[2]) / 4  # blurR, blurG, blurB averages each of the RGB values
        screen.set_at((x, y), (blurR, blurG, blurB))


def fill(surf, x, y, colour,
         canvasRect):  # This function fills a certain shape by replacing each pixel that is the same colour as the initial pixel
    pixels = [(x, y)]  # pixels hold each pixel that needs to be checked
    origincolour = surf.get_at((x, y))  # origincolour holds the initial colour
    if origincolour != colour:
        while len(pixels) > 0:
            if canvasRect.collidepoint(pixels[0][0], pixels[0][1]) and surf.get_at(pixels[
                                                                                       0]) == origincolour:  # This if statement replaces the colour of the current pixel and checks the surounding pixels
                surf.set_at((pixels[0]), colour)
                # These check the surrounding pixels using the same function
                pixels.append((pixels[0][0], pixels[0][1] - 1))
                pixels.append((pixels[0][0], pixels[0][1] + 1))
                pixels.append((pixels[0][0] - 1, pixels[0][1]))
                pixels.append((pixels[0][0] + 1, pixels[0][1]))
            del pixels[0]


screen = display.set_mode((1080, 720))  # This draws the screen in pygame

running = True  # running keeps the program running
first = True  # first holds if the selected tool
pressed = False  # pressed and released hold if the mouse haqs been clicked and released
released = False  # pressed and released are used in the undo/redo functions to detect a change on the canvas
polypress = False
polyrelease = False  # polypress and poly release serve the same function as pressed and released, but they are used separately in order to undo an entire shape instead of individual steps
clicked = False  # clicked is used to detect if the mouse has been clicked in order for the projected line in the polygon tool to be drawn
outline = False  # outline holds if the user has clicked on the outline box or not and is used to draw the Rectangle, Ellipse, and Polygon tool filled or in an outline
stopmusic = False  # stopmusic holds if the user has clicked on the mute button or not and is used to mute the "music"
stamp = False  # stamps holds if the user has selected to use tools or stamps
typing = False  # typing holds if the user has began to use the text tool or not

root = Tk()
root.withdraw()
font.init()
init()
mixer.music.load("Music/File Select - The Legend of Zelda.mp3")  # This loads the "music"
mixer.music.play(-1)  # This loops the "music"
undolist = []  # undolist holds all of the screens that might need to be undone
redolist = []  # redolist holds all of the screens that might need to be redone
poly = []  # poly holds the coordinates the user selects when using the polygon tool
string = ''  # string holds the string of text the user inputs while using the text tool

# These variables hold the colours used in the colour pallet
white = [238, 237, 240]
jade = [120, 190, 145]
lightgreen = [13, 146, 99]
green = [14, 81, 53]
black = [0, 16, 36]
curcol = (0, 0, 0, 255)

# These variables hold the interactive rectangles
canvas = Rect(250, 50, 780, 500)
coloursquarerect = Rect(260, 580, 100, 100)
gradientrect = Rect(380, 640, 160, 20)
savebut = Rect(1040, 48, 30, 30)
loadbut = Rect(1040, 86, 30, 30)
undobut = Rect(248, 10, 30, 30)
redobut = Rect(286, 10, 30, 30)
clearbut = Rect(326, 10, 30, 30)
outlinebut = Rect(48, 640, 20, 20)
mutebut = Rect(48, 670, 20, 20)
toolbut = Rect(60, 20, 80, 20)
stampsbut = Rect(140, 20, 80, 20)

toolsquares = []  # This holds the boundaries of the tool icons
tool = 0  # This holds which icon is currently selected

# These holds the scales
scale = 6  # scale is used for the tools
stampscale = 6

# These load the images used in the colour selector
coloursquareimg = image.load("Images/ColourSquare.jpg")  # This is the colour square
coloursquare = transform.scale(coloursquareimg, (100, 100))
gradientimg = image.load("Images/download.jpg")  # This is the black & white gradient
gradient = transform.scale(gradientimg, (160, 20))

# These load the Logo
logoimg = image.load("Images/PaintLogo.png")
truelogo = transform.scale(logoimg, (260, 155))

# These load the icons for all of the tools
pencilimg = image.load("Images/Icons/Pencil.png")
pencilicon = transform.scale(pencilimg, (60, 60))
eraserimg = image.load("Images/Icons/Eraser.png")
erasericon = transform.scale(eraserimg, (60, 58))
paintbrushimg = image.load("Images/Icons/Paintbrush.png")
paintbrushicon = transform.scale(paintbrushimg, (60, 54))
recttoolimg = image.load("Images/Icons/RectangleOutline.png")
recticon = transform.scale(recttoolimg, (65, 43))
sprayimg = image.load("Images/Icons/SprayPaint.png")
sprayicon = transform.scale(sprayimg, (60, 60))
bucketimg = image.load("Images/Icons/FillBucket.png")
fillicon = transform.scale(bucketimg, (60, 60))
blurfingerimg = image.load("Images/Icons/Blur.jpg")
bluricon = transform.scale(blurfingerimg, (44, 60))
polygonimg = image.load("Images/Icons/Polygon.png")
polygonicon = transform.scale(polygonimg, (60, 47))
ellipseimg = image.load("Images/Icons/EllipseOutline.png")
ellipseicon = transform.scale(ellipseimg, (65, 39))
linetoolimg = image.load("Images/Icons/Line.png")
lineicon = transform.scale(linetoolimg, (60, 54))
highlighterimg = image.load("Images/Icons/HighLighter.png")
highlightericon = transform.scale(highlighterimg, (49, 60))
texttoolimg = image.load("Images/Icons/Letter.png")
texticon = transform.scale(texttoolimg, (60, 59))
saveimg = image.load("Images/Icons/Save.png")
saveicon = transform.scale(saveimg, (20, 20))
loadimg = image.load("Images/Icons/Open.png")
loadicon = transform.scale(loadimg, (20, 20))
undoimg = image.load("Images/Icons/undo.png")
undoicon = transform.scale(undoimg, (20, 20))
redoimg = transform.flip(undoimg, True, False)
redoicon = transform.scale(redoimg, (20, 20))
trashimg = image.load("Images/Icons/TrashCan.png")
clearicon = transform.scale(trashimg, (20, 20))

# These load all of the icons for the stamps
linkimg = image.load("Images/Stamps/Link.png")
linkstamp = transform.scale(linkimg, (60, 60))
zeldaimg = image.load("Images/Stamps/Zelda.png")
zeldastamp = transform.scale(zeldaimg, (60, 60))
ganonimg = image.load("Images/Stamps/Ganon.png")
ganonstamp = transform.scale(ganonimg, (60, 54))
tingleimg = image.load("Images/Stamps/Tingle.png")
tinglestamp = transform.scale(tingleimg, (60, 60))
masterswordimg = image.load("Images/Stamps/Sword.png")
masterswordstamp = transform.scale(masterswordimg, (57, 60))
shieldimg = image.load("Images/Stamps/Shield.png")
shieldstamp = transform.scale(shieldimg, (57, 60))
triforceimg = image.load("Images/Stamps/Triforce.png")
triforcestamp = transform.scale(triforceimg, (60, 60))
cuccoimg = image.load("Images/Stamps/Cucco.png")
cuccostamp = transform.scale(cuccoimg, (60, 43))
grupeeimg = image.load("Images/Stamps/GRupee.png")
grupeestamp = transform.scale(grupeeimg, (42, 60))
brupeeimg = image.load("Images/Stamps/BRupee.png")
brupeestamp = transform.scale(brupeeimg, (39, 60))
yrupeeimg = image.load("Images/Stamps/YRupee.png")
yrupeestamp = transform.scale(yrupeeimg, (39, 60))
rrupeeimg = image.load("Images/Stamps/RRupee.png")
rrupeestamp = transform.scale(rrupeeimg, (40, 60))

# These load the labels
pencillabel = image.load("Images/Labels/Tools/Pencillabe.png")
paintlabel = image.load("Images/Labels/Tools/Paintlabel.png")
eraserlabel = image.load("Images/Labels/Tools/Eraserlabel.png")
blurlabel = image.load("Images/Labels/Tools/Blurlabel.png")
spraylabel = image.load("Images/Labels/Tools/Spraylabel.png")
filllabel = image.load("Images/Labels/Tools/Filllabel.png")
highlightlabel = image.load("Images/Labels/Tools/Highlabel.png")
textlabel = image.load("Images/Labels/Tools/Textlabel.png")
rectlabel = image.load("Images/Labels/Tools/Rectlabel.png")
polylabel = image.load("Images/Labels/Tools/Polylabel.png")
ellilabel = image.load("Images/Labels/Tools/Ellipselabel.png")
linelabel = image.load("Images/Labels/Tools/Linelabel.png")
linklabel = image.load("Images/Labels/Stamps/linklabel.png")
zeldalabel = image.load("Images/Labels/Stamps/zeldalabel.png")
gannonlabel = image.load("Images/Labels/Stamps/Gannonlabel.png")
tinglelabel = image.load("Images/Labels/Stamps/Tinglelabel.png")
swordlabel = image.load("Images/Labels/Stamps/Masterswordlabel.png")
shieldlabel = image.load("Images/Labels/Stamps/Shieldlabel.png")
triforcelabel = image.load("Images/Labels/Stamps/Triforcelabel.png")
cuccolabel = image.load("Images/Labels/Stamps/Cuccolabel.png")
grupeelabel = image.load("Images/Labels/Stamps/GRupeelabel.png")
brupeelabel = image.load("Images/Labels/Stamps/BRupeelabel.png")
yrupeelabel = image.load("Images/Labels/Stamps/YRupeelabel.png")
rrupeelabel = image.load("Images/Labels/Stamps/RRupeelabel.png")

# These load the lables for the outline and mute button
calibri = font.SysFont("Calibri", 20, True)
outlinelable = calibri.render("Outline", True, black)
mutelable = calibri.render("Mute", True, black)

# These load the labels for the tool/stamp selector
toolstamp = font.SysFont("Calibri", 18, True)
toollabel = toolstamp.render("Tools", True, black)
stamplabel = toolstamp.render("Stamps", True, black)

# This section draws the GUI
screen.fill(green)
screen.blit(truelogo, (694, 560))
# These draw the Canvas
draw.rect(screen, white, canvas)
draw.rect(screen, black, (248, 48, 784, 504), 3)
# These draw the Colour Selector
draw.rect(screen, jade, (250, 570, 360, 120))
draw.rect(screen, black, (248, 568, 364, 124), 3)
screen.blit(coloursquare, (260, 580))
draw.rect(screen, black, (258, 578, 104, 104), 3)
screen.blit(gradient, (380, 640))
draw.rect(screen, black, (378, 638, 164, 24), 3)
# These draw the Stamps/Tools Menu
draw.rect(screen, jade, (50, 10, 180, 540))
draw.rect(screen, black, (48, 8, 184, 544), 3)
draw.rect(screen, white, toolbut)
draw.rect(screen, black, toolbut, 3)
draw.rect(screen, white, stampsbut)
draw.rect(screen, black, stampsbut, 3)
screen.blit(toollabel, (80, 21))
screen.blit(stamplabel, (152, 21))
# These draw the Tool menu
for i in range(6):
    for n in range(2):
        draw.rect(screen, white, (60 + n * 85, 60 + i * 80, 75, 75))
        draw.rect(screen, black, (60 + n * 85, 60 + i * 80, 75, 75), 3)
        square = (60 + n * 85, 60 + i * 80, 75, 75)
        toolsquares.append(Rect(square))
screen.blit(pencillabel, (48, 570))
draw.rect(screen, black, (48, 570, 184, 40), 3)
# These draw the Save Button
draw.rect(screen, white, savebut)
draw.rect(screen, black, savebut, 3)
screen.blit(saveicon, (1045, 53))
# These draw the Load Button
draw.rect(screen, white, loadbut)
draw.rect(screen, black, loadbut, 3)
screen.blit(loadicon, (1045, 91))
# These draw the Undo Button
draw.rect(screen, white, undobut)
draw.rect(screen, black, undobut, 3)
screen.blit(undoicon, (253, 15))
# These draw the Redo Button
draw.rect(screen, white, redobut)
draw.rect(screen, black, redobut, 3)
screen.blit(redoicon, (291, 15))
# These draw the Clear Button
draw.rect(screen, white, clearbut)
draw.rect(screen, black, clearbut, 3)
screen.blit(clearicon, (331, 15))
# These draw the Toggle Outline Button
draw.rect(screen, white, outlinebut)
draw.rect(screen, black, outlinebut, 3)
screen.blit(outlinelable, (73, 640))
# These draw the Mute Button
draw.rect(screen, white, mutebut)
draw.rect(screen, black, mutebut, 3)
screen.blit(mutelable, (73, 670))

# This initializes the undo list
undoscr = (screen.subsurface(canvas)).copy()
undolist.append(undoscr)

# This holds the background so the current size of the cursor can be displayed
sizebckgrnd = screen.subsurface(Rect(440, 580, 150, 45)).copy()
colourbckgrnd = screen.subsurface(Rect(376, 660, 250, 40)).copy()

# These initialize the Highlighter Tool
cover = Surface((1080, 720)).convert()
cover.set_alpha(55)
cover.set_colorkey((255, 0, 255))

while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False

        if evt.type == MOUSEBUTTONDOWN:
            # These are used in the highlighter tool
            copy = screen.copy()
            cover.fill((255, 0, 255))
            # This increases the scale when the scroll wheel is pushed forwards
            if evt.button == 4:
                scale += 2
                if scale > 250:
                    scale = 250
                stampscale += 2
            # This decreases the scale when the scroll wheel is pulled back
            if evt.button == 5:
                scale -= 2
                if scale <= 0:
                    scale = 2
                stampscale -= 2
                if stampscale < -20:
                    stampscale = -20
        # This detects typing for the text tool
        if evt.type == KEYDOWN and typing:
            if evt.key == K_BACKSPACE:
                string = string[:-1]  # This deletes the previous character when the backspace key is hit
            # This ends all typing
            elif evt.key == K_RETURN:
                typing = False
                string = ''
            # This adds the characters into the string
            else:
                string += evt.unicode

    radius = int(
        scale / 2)  # radius holds the radius for whenever circles are drawn to keep them similar to non-circle widths
    mx, my = mouse.get_pos()  # mx and my hold the mouse position
    mb = mouse.get_pressed()  # mb holds what buttons of the mouse are pressed
    blursurface = screen.copy()  # blursurface holds the surface the blur tool uses to get the colour values of the pixels needed
    bitfont = font.Font("Pixeled.ttf", scale + 5)  # bitfont loads the font used in the text tool
    showsize = calibri.render("Size: " + str(scale), True, black)  # showsize loads the size display
    showstampsize = calibri.render("Stamp Size: " + str(stampscale), True,
                                   black)  # showstampsize loads the stampsize display
    showcolour = calibri.render("Colour: " + str(curcol), True, black)  # showcolour loads the rgb colour display

    # This if statement detects change and saves a screen of the change
    if released and pressed:  # This if statement checks if the mouse hase been pressed the released
        canvasscr = screen.subsurface(canvas)  # canvasscr creates a new surface to record the change
        undoscr = canvasscr.copy()  # undoscr holds a copy of the change in the canvas
        undolist.append(undoscr)  # This adds the change in the canvas to the list of undo-able screens
        redolist = []  # This resets the redo list
        released = False
        pressed = False  # pressed and released are then set to flase in order to prevent over copying of the screen

    # This operates the save button
    if savebut.collidepoint(mx, my):
        draw.rect(screen, lightgreen, savebut, 3)
        if mb[0] == 1:
            result = filedialog.asksaveasfilename()
            if result:
                image.save(screen.subsurface(canvas), result + '.png')
            else:
                pass
    else:
        draw.rect(screen, black, savebut, 3)

    # This operates the load button
    if loadbut.collidepoint(mx, my):
        draw.rect(screen, lightgreen, loadbut, 3)
        if mb[0] == 1:
            result = filedialog.askopenfilename()
            pic = image.load(result)
            if result:
                screen.blit(pic, (250, 50))
    else:
        draw.rect(screen, black, loadbut, 3)

    # This operates the undo button
    if undobut.collidepoint(mx, my):
        draw.rect(screen, lightgreen, undobut, 3)
        if mb[0] == 1 and first:  # This is used to limit undoing to once per click
            pos = len(undolist) - 2  # pos holds the position of the canvas to be displayed in undolist
            screen.blit(undolist[pos], (250, 50))  # This blits the canvas onto the canvas
            # This removes the undone screen and puts it into the redolist
            if len(undolist) > 1:  # This if statement prevents the user from removing the last screen in the list
                redolist.append(undolist[-1])
                undolist.remove(undolist[-1])
            first = False
        elif mb[0] == 0:
            first = True
    else:
        draw.rect(screen, black, undobut, 3)

    # This operates the redo button
    if redobut.collidepoint(mx, my):
        draw.rect(screen, lightgreen, redobut, 3)
        if mb[0] == 1 and first:  # This is used to limit redoing to once per click
            # This removes the redone screen and puts it into the undolist and blits it onto the screen
            if len(redolist) > 0:
                screen.blit(redolist[-1], (250, 50))
                undolist.append(redolist[-1])
                redolist.remove(redolist[-1])
            first = False
        elif mb[0] == 0:
            first = True
    else:
        draw.rect(screen, black, redobut, 3)

    # This operates the clear screen button
    if clearbut.collidepoint(mx, my):
        draw.rect(screen, lightgreen, clearbut, 3)
        if mb[0] == 1:
            draw.rect(screen, white, canvas)
            poly = []  # This resets the coordinate list for the polygon tool
            redolist = []  # This resets the redolist
        # These makes it so that you can undo a clear screen
        if mb[0] == 1:
            pressed = True
        elif pressed and mb[0] == 0:
            released = True
        if released and pressed:
            canvasscr = screen.subsurface(canvas)
            undoscr = canvasscr.copy()
            undolist.append(undoscr)
            redolist = []
            released = False
            pressed = False
    else:
        draw.rect(screen, black, clearbut, 3)

    # This operates the toggle outline button
    if outlinebut.collidepoint(mx, my):
        draw.rect(screen, lightgreen, outlinebut, 3)
        if mb[0] == 1 and not outline:
            outline = True
            draw.line(screen, black, (50, 642), (65, 657), 3)
            draw.line(screen, black, (50, 657), (65, 642), 3)  # The two draw line statements draw an X over the button
            time.wait(100)
        elif mb[0] == 1 and outline:
            outline = False
            draw.rect(screen, white, outlinebut)
            time.wait(100)
    else:
        draw.rect(screen, black, outlinebut, 3)

    # This operates the mute button
    if mutebut.collidepoint(mx, my):
        draw.rect(screen, lightgreen, mutebut, 3)
        if mb[0] == 1 and not stopmusic:
            mixer.music.stop()
            stopmusic = True
            draw.line(screen, black, (50, 672), (65, 687), 3)
            draw.line(screen, black, (50, 687), (65, 672), 3)  # The two draw line statements draw an X over the button
            time.wait(100)
        elif mb[0] == 1 and stopmusic:
            mixer.music.load("Music/File Select - The Legend of Zelda.mp3")
            mixer.music.play(-1)
            stopmusic = False
            draw.rect(screen, white, mutebut)
            time.wait(100)
    else:
        draw.rect(screen, black, mutebut, 3)

    # This operates the tool/stamp selector
    # This checks if tools have been selected
    if toolbut.collidepoint(mx, my):
        draw.rect(screen, lightgreen, toolbut, 3)
        if mb[0] == 1 and stamp:
            stamp = False
    else:
        draw.rect(screen, black, toolbut, 3)
    # This checks if stamps have been selected
    if stampsbut.collidepoint(mx, my):
        draw.rect(screen, lightgreen, stampsbut, 3)
        if mb[0] == 1 and not stamp:
            stamp = True
    else:
        draw.rect(screen, black, stampsbut, 3)

    if stamp:
        draw.rect(screen, lightgreen, stampsbut, 3)
        # These put the stamp icons over the buttons
        for i in range(6):
            for n in range(2):
                draw.rect(screen, white, (60 + n * 85, 60 + i * 80, 75, 75))
                draw.rect(screen, black, (60 + n * 85, 60 + i * 80, 75, 75), 3)
        screen.blit(linkstamp, (67, 66))
        screen.blit(zeldastamp, (153, 67))
        screen.blit(ganonstamp, (67, 148))
        screen.blit(tinglestamp, (150, 145))
        screen.blit(masterswordstamp, (66, 228))
        screen.blit(shieldstamp, (152, 227))
        screen.blit(triforcestamp, (68, 305))
        screen.blit(cuccostamp, (154, 315))
        screen.blit(grupeestamp, (78, 385))
        screen.blit(brupeestamp, (163, 384))
        screen.blit(yrupeestamp, (78, 465))
        screen.blit(rrupeestamp, (163, 465))

    else:
        draw.rect(screen, lightgreen, toolbut, 3)
        # These put the tool icons over the buttons
        for i in range(6):
            for n in range(2):
                draw.rect(screen, white, (60 + n * 85, 60 + i * 80, 75, 75))
                draw.rect(screen, black, (60 + n * 85, 60 + i * 80, 75, 75), 3)
        screen.blit(pencilicon, (67, 67))
        screen.blit(paintbrushicon, (153, 71))
        screen.blit(erasericon, (67, 148))
        screen.blit(bluricon, (160, 145))
        screen.blit(sprayicon, (65, 228))
        screen.blit(fillicon, (152, 227))
        screen.blit(highlightericon, (75, 305))
        screen.blit(texticon, (152, 307))
        screen.blit(recticon, (65, 395))
        screen.blit(polygonicon, (152, 392))
        screen.blit(ellipseicon, (65, 475))
        screen.blit(lineicon, (152, 468))

    # These blit the tool/stamp label that is selected to the screen
    if not stamp:
        if tool == 0:
            screen.blit(pencillabel, (48, 570))
        elif tool == 1:
            screen.blit(paintlabel, (48, 570))
        elif tool == 2:
            screen.blit(eraserlabel, (48, 570))
        elif tool == 3:
            screen.blit(blurlabel, (48, 570))
        elif tool == 4:
            screen.blit(spraylabel, (48, 570))
        elif tool == 5:
            screen.blit(filllabel, (48, 570))
        elif tool == 6:
            screen.blit(highlightlabel, (48, 570))
        elif tool == 7:
            screen.blit(textlabel, (48, 570))
        elif tool == 8:
            screen.blit(rectlabel, (48, 570))
        elif tool == 9:
            screen.blit(polylabel, (48, 570))
        elif tool == 10:
            screen.blit(ellilabel, (48, 570))
        elif tool == 11:
            screen.blit(linelabel, (48, 570))
    elif stamp:
        if tool == 0:
            screen.blit(linklabel, (48, 570))
        elif tool == 1:
            screen.blit(zeldalabel, (48, 570))
        elif tool == 2:
            screen.blit(gannonlabel, (48, 570))
        elif tool == 3:
            screen.blit(tinglelabel, (48, 570))
        elif tool == 4:
            screen.blit(swordlabel, (48, 570))
        elif tool == 5:
            screen.blit(shieldlabel, (48, 570))
        elif tool == 6:
            screen.blit(triforcelabel, (48, 570))
        elif tool == 7:
            screen.blit(cuccolabel, (48, 570))
        elif tool == 8:
            screen.blit(grupeelabel, (48, 570))
        elif tool == 9:
            screen.blit(brupeelabel, (48, 570))
        elif tool == 10:
            screen.blit(yrupeelabel, (48, 570))
        elif tool == 11:
            screen.blit(rrupeelabel, (48, 570))

    # Checks for which square is selected
    for i in range(12):
        if toolsquares[i].collidepoint(mx, my):
            # These blit the tool/stamp label that is hovered over to the screen
            if not stamp:
                if i == 0:
                    screen.blit(pencillabel, (48, 570))
                elif i == 1:
                    screen.blit(paintlabel, (48, 570))
                elif i == 2:
                    screen.blit(eraserlabel, (48, 570))
                elif i == 3:
                    screen.blit(blurlabel, (48, 570))
                elif i == 4:
                    screen.blit(spraylabel, (48, 570))
                elif i == 5:
                    screen.blit(filllabel, (48, 570))
                elif i == 6:
                    screen.blit(highlightlabel, (48, 570))
                elif i == 7:
                    screen.blit(textlabel, (48, 570))
                elif i == 8:
                    screen.blit(rectlabel, (48, 570))
                elif i == 9:
                    screen.blit(polylabel, (48, 570))
                elif i == 10:
                    screen.blit(ellilabel, (48, 570))
                elif i == 11:
                    screen.blit(linelabel, (48, 570))
            elif stamp:
                if i == 0:
                    screen.blit(linklabel, (48, 570))
                elif i == 1:
                    screen.blit(zeldalabel, (48, 570))
                elif i == 2:
                    screen.blit(gannonlabel, (48, 570))
                elif i == 3:
                    screen.blit(tinglelabel, (48, 570))
                elif i == 4:
                    screen.blit(swordlabel, (48, 570))
                elif i == 5:
                    screen.blit(shieldlabel, (48, 570))
                elif i == 6:
                    screen.blit(triforcelabel, (48, 570))
                elif i == 7:
                    screen.blit(cuccolabel, (48, 570))
                elif i == 8:
                    screen.blit(grupeelabel, (48, 570))
                elif i == 9:
                    screen.blit(brupeelabel, (48, 570))
                elif i == 10:
                    screen.blit(yrupeelabel, (48, 570))
                elif i == 11:
                    screen.blit(rrupeelabel, (48, 570))
            if mb[0] == 1:
                tool = i
            draw.rect(screen, lightgreen, (toolsquares[i]), 3)
        else:
            draw.rect(screen, black, (toolsquares[i]), 3)
    draw.rect(screen, lightgreen, toolsquares[tool], 3)
    draw.rect(screen, black, (48, 570, 184, 40), 3)

    # This operates the colour selector
    if coloursquarerect.collidepoint(mx, my) or gradientrect.collidepoint(mx, my):
        if mb[0] == 1:
            curcol = screen.get_at((mx, my))
    draw.rect(screen, curcol, (380, 580, 50, 50))
    draw.rect(screen, black, (378, 578, 54, 54), 3)

    # This shows the size and stampsize
    screen.blit(sizebckgrnd, (440, 576))
    screen.blit(showsize, (440, 576))
    screen.blit(showstampsize, (440, 596))
    # This shows the colour in rgb values
    screen.blit(colourbckgrnd, (376, 660))
    screen.blit(showcolour, (376, 668))

    # Uses the selected tool
    if canvas.collidepoint(mx, my):
        # This is used to keep the drawing within the canvas
        screen.set_clip(canvas)

        # This is used to detect a mouse press and release
        if mb[0] == 1:
            pressed = True
        elif pressed and mb[0] == 0:
            released = True

        if not stamp:
            # These operate the tools
            # This draws a line between the last mouse position and the current mouse position
            if tool == 0:  # Pencil
                if mb[0] == 1:
                    draw.line(screen, curcol, (oldmx, oldmy), (mx, my), 1)

            # This draws circles between the last mouse position and the current mouse position
            if tool == 1:  # Paint Brush
                if mb[0] == 1:
                    coords = line(mx, my, oldmx, oldmy)
                    for i in range(len(coords)):
                        draw.circle(screen, curcol, coords[i], radius)

            # This draws white circles between the last mouse position and the current mouse position
            if tool == 2:  # Eraser
                if mb[0] == 1:
                    coords = line(mx, my, oldmx, oldmy)
                    for i in range(len(coords)):
                        draw.circle(screen, white, coords[i], radius)

            # This uses the blur function to blur a square around the mouse position
            if tool == 3:  # Blur
                if mb[0] == 1:
                    for i in range(radius):
                        for j in range(radius):
                            blur(mx - i, my - j)
                            blur(mx - i, my + j)
                            blur(mx + i, my + j)
                            blur(mx + i, my - j)

            # This randomly draws pixels in a circle
            if tool == 4:  # Spray Paint
                if mb[0] == 1:
                    rx = randint((mx - radius), (mx + radius))  # rx holds a random x coordinate within the circle
                    ry = randint((my - radius), (my + radius))  # ry holds a random y coordinate within the circle
                    if ((rx - mx) ** 2 + (
                        ry - my) ** 2) > radius ** 2:  # This checks to see if the (rx,ry) coordinate is within the circle
                        pass
                    else:
                        screen.set_at((rx, ry), curcol)

            # This uses the fill function to replace a selected colour
            if tool == 5:  # Fill
                if mb[0] == 1:
                    mcol = screen.get_at((mx, my))  # mcol holds the colour that is to be replaced
                    fill(screen, mx, my, curcol, canvas)

            # This draws transparent circles between the last mouse position and the current mouse position
            if tool == 6:  # Highlighter
                if mb[0] == 1:
                    coords = line(mx, my, oldmx, oldmy)
                    for i in coords:
                        draw.circle(cover, curcol, i,
                                    radius)  # This draws circles onto a separate surface to make each circle uniformly transparent
                if mb[2] == 1:
                    coords = line(mx, my, oldmx, oldmy)
                    for i in coords:
                        draw.circle(cover, white, i,
                                    radius)  # This draws circles onto a separate surface to make each circle uniformly transparent
                # This blits the transparent circles onto the canvas
                if 1 in mb:
                    screen.blit(copy, (0, 0))
                    screen.blit(cover, (0, 0))

            # This detects keyboard presses and blits the coresponding characters onto the screen
            if tool == 7:  # Text
                if mb[0] == 1:
                    typing = True
                    if first:  # This if statement saves the screen before changes are made so the change can move about the screen
                        back = screen.copy()  # back holds the screen before the change
                        first = False
                if typing:
                    screen.blit(back, (0, 0))
                    text = bitfont.render(string, True, curcol)  # This loads the typed in string
                    height = text.get_height()  # This gets the height of the string
                    screen.blit(text, (mx + 10, my - height / 2))  # This blits the string onto the screen
                elif mb[0] == 0:
                    first = True

            # This draws a rectangel from the original coordinates to the current mouse position
            if tool == 8:  # Draw Rectangle
                if mb[0] == 1:
                    if first:  # This if statement saves the screen before changes are made and the original coordinates
                        back = screen.copy()
                        omx = mx
                        omy = my
                    offset = int(round((scale / 2), 0))  # This holds the offset for the sides of the outlined rectangle
                    screen.blit(back, (0, 0))
                    rec = Rect(omx, omy, mx - omx, my - omy)
                    rec.normalize()
                    # This draws an outlined rectangle
                    if outline:
                        # This draws the rectangle when the area is less than the side widths
                        if rec[2] < scale or rec[3] < scale:
                            # This checks which direction the rectangle is drawn in the x axis
                            if omx > mx:
                                # This checks which direction the rectangle is drawn in the y axis
                                if omy > my:
                                    draw.rect(screen, curcol, (omx, omy + offset, mx - omx, my - omy - offset * 2))
                                else:
                                    draw.rect(screen, curcol, (omx, omy - offset, mx - omx, my - omy + offset * 2))
                            else:
                                # This checks which direction the rectangle is drawn in the y axis
                                if omy > my:
                                    draw.rect(screen, curcol, (omx, omy + offset, mx - omx, my - omy - offset * 2))
                                else:
                                    draw.rect(screen, curcol, (omx, omy - offset, mx - omx, my - omy + offset * 2))
                        # This draws an outlined rectangle
                        else:
                            # This checks which direction the rectangle is drawn in the x axis
                            if omx > mx:
                                # This checks which direction the rectangle is drawn in the y axis
                                if omy > my:
                                    draw.line(screen, curcol, (omx - offset, omy - offset), (omx - offset, my), scale)
                                    draw.line(screen, curcol, (omx, omy), (mx, omy), scale)
                                    draw.line(screen, curcol, (omx, my), (mx, my), scale)
                                    draw.line(screen, curcol, (mx + (offset - 1), omy), (mx + (offset - 1), my), scale)
                                else:
                                    draw.line(screen, curcol, (omx - offset, omy - (offset - 1)), (omx - offset, my),
                                              scale)
                                    draw.line(screen, curcol, (omx, omy), (mx, omy), scale)
                                    draw.line(screen, curcol, (omx, my), (mx, my), scale)
                                    draw.line(screen, curcol, (mx + (offset - 1), omy), (mx + (offset - 1), my), scale)
                            else:
                                # This checks which direction the rectangle is drawn in the y axis
                                if omy > my:
                                    draw.line(screen, curcol, (omx + offset - 1, omy - offset), (omx + offset - 1, my),
                                              scale)
                                    draw.line(screen, curcol, (omx, omy), (mx, omy), scale)
                                    draw.line(screen, curcol, (omx, my), (mx, my), scale)
                                    draw.line(screen, curcol, (mx - offset, omy), (mx - offset, my), scale)
                                else:
                                    draw.line(screen, curcol, (omx + offset - 1, omy - (offset - 1)),
                                              (omx + offset - 1, my), scale)
                                    draw.line(screen, curcol, (omx, omy), (mx, omy), scale)
                                    draw.line(screen, curcol, (omx, my), (mx, my), scale)
                                    draw.line(screen, curcol, (mx - offset, omy), (mx - offset, my), scale)
                    # This draws a filled rectangles
                    elif not outline:
                        draw.rect(screen, curcol, (omx, omy, mx - omx, my - omy))
                    first = False
                elif mb[0] == 0:
                    first = True

            # This takes coordinates from the user and draws a polygon
            if tool == 9:  # Draw Polygon
                if mb[0] == 1:
                    polypress = True
                    clicked = True  # clicked holds if coordinate selection has begun
                elif mb[0] == 0:
                    polyrelease = True
                # polypress and polyrelease are used to limit coordinae selection to once per click
                # This operates the coordinate selection
                if polypress and polyrelease:
                    poly.append([mx, my])
                    omx = mx
                    omy = my
                    back = screen.copy()
                    polypress = False
                    polyrelease = False
                    pressed = False
                    released = False  # pressed and released are set to false because entire shapes are to be undone not individual coordinates
                # This finishes the polgon and resets the polygon coordinates
                elif mb[2] == 1 and len(poly) > 2:
                    poly.append([mx, my])
                    # This connects the last coordinate to the first coordinate
                    coords = line(mx, my, poly[0][0], poly[0][1])
                    for i in range(len(coords)):
                        draw.circle(screen, curcol, coords[i], radius)
                    # This draws a polygon without fill
                    if outline:
                        draw.polygon(screen, curcol, poly, scale)
                    # This draw a polygon with fill
                    elif not outline:
                        draw.polygon(screen, curcol, poly)
                    # This resets the polygon tool
                    poly = []
                    clicked = False
                    polypress = False
                    polyrelease = False
                    pressed = True
                    released = True  # pressed and released are set to true to allow the shape to be undone
                # This draws a line from the previous coordinate to the current mouse position
                if mb[0] == 0 and clicked:
                    screen.blit(back, (0, 0))
                    coords = line(mx, my, omx, omy)
                    for i in range(len(coords)):
                        draw.circle(screen, curcol, coords[i], radius)

            # This draws a circle from the original coordinates to the current mouse position
            if tool == 10:  # Draw Ellipse
                if mb[0] == 1:
                    if first:  # This if statement saves the screen before changes are made and the original coordinates
                        back = screen.copy()
                        omx = mx
                        omy = my
                    screen.blit(back, (0, 0))
                    dx = mx - omx  # dx holds the distance from the original x coordinate to the current x coordinate
                    dy = my - omy  # dy holds the distance from the original y coordinate to the current y coordinate
                    elipserect = (
                    Rect(omx, omy, dx, dy))  # elipserect holds the rectangle the ellipse will be drawn inside
                    elipserect.normalize()
                    # This draws an outlined ellipse
                    if outline:
                        # This draws the ellipse when the area is less than the side widths
                        if elipserect[2] < 2 * scale or elipserect[3] < 2 * scale:
                            draw.ellipse(screen, curcol, elipserect)
                        # This draws an outlined ellipse
                        else:
                            # Five ellipses are drawn to cover the holes in a single ellipse
                            draw.ellipse(screen, curcol, elipserect, scale)
                            draw.ellipse(screen, curcol,
                                         (elipserect[0] - 1, elipserect[1], elipserect[2], elipserect[3]), scale)
                            draw.ellipse(screen, curcol,
                                         (elipserect[0], elipserect[1] - 1, elipserect[2], elipserect[3]), scale)
                            draw.ellipse(screen, curcol,
                                         (elipserect[0] + 1, elipserect[1], elipserect[2], elipserect[3]), scale)
                            draw.ellipse(screen, curcol,
                                         (elipserect[0], elipserect[1] + 1, elipserect[2], elipserect[3]), scale)
                    # This draws a filled ellipse
                    elif not outline:
                        draw.ellipse(screen, curcol, elipserect)
                    first = False
                elif mb[0] == 0:
                    first = True

            # This draws a straight line between two coordinates
            if tool == 11:  # Draw straight line
                if mb[0] == 1:
                    if first:  # This if statement saves the screen before changes are made and the original coordinates
                        back = screen.copy()
                        omx = mx
                        omy = my
                        first = False
                    screen.blit(back, (0, 0))
                    # This draws a line from the previous coordinate to the current mouse position
                    coords = line(mx, my, omx, omy)
                    for i in range(len(coords)):
                        draw.circle(screen, curcol, coords[i], radius)
                elif mb[0] == 0:
                    first = True

        elif stamp:

            # These re-size the stamps according to the stampscale
            blitlinkstamp = transform.scale(linkimg, (60 + stampscale, 60 + stampscale))
            blitzeldastamp = transform.scale(zeldaimg, (60 + stampscale, 60 + stampscale))
            blitganonstamp = transform.scale(ganonimg, (60 + stampscale, 54 + int(stampscale * 1.11)))
            blittinglestamp = transform.scale(tingleimg, (60 + stampscale, 60 + stampscale))
            blitmasterswordstamp = transform.scale(masterswordimg, (57 + int(stampscale * 0.95), 60 + stampscale))
            blitshieldstamp = transform.scale(shieldimg, (57 + int(stampscale * 0.95), 60 + stampscale))
            blittriforcestamp = transform.scale(triforceimg, (60 + stampscale, 60 + stampscale))
            blitcuccostamp = transform.scale(cuccoimg, (60 + stampscale, 43 + int(stampscale * 0.7167)))
            blitgrupeestamp = transform.scale(grupeeimg, (42 + int(stampscale * 0.7), 60 + stampscale))
            blitbrupeestamp = transform.scale(brupeeimg, (39 + int(stampscale * 0.65), 60 + stampscale))
            blityrupeestamp = transform.scale(yrupeeimg, (39 + int(stampscale * 0.65), 60 + stampscale))
            blitrrupeestamp = transform.scale(rrupeeimg, (40 + int(stampscale * 0.6667), 60 + stampscale))

            # These operate the stamp bliting
            if tool == 0:  # Link
                if mb[0] == 1:
                    if first:
                        back = screen.copy()
                        first = False
                    screen.blit(back, (0, 0))
                    screen.blit(blitlinkstamp,
                                (mx - int(blitlinkstamp.get_width() / 2), my - int(blitlinkstamp.get_height() / 2)))
                elif mb[0] == 0:
                    first = True

            if tool == 1:  # Zelda
                if mb[0] == 1:
                    if first:
                        back = screen.copy()
                        first = False
                    screen.blit(back, (0, 0))
                    screen.blit(blitzeldastamp,
                                (mx - int(blitzeldastamp.get_width() / 2), my - int(blitzeldastamp.get_height() / 2)))
                elif mb[0] == 0:
                    first = True

            if tool == 2:  # Ganon
                if mb[0] == 1:
                    if first:
                        back = screen.copy()
                        first = False
                    screen.blit(back, (0, 0))
                    screen.blit(blitganonstamp,
                                (mx - int(blitganonstamp.get_width() / 2), my - int(blitganonstamp.get_height() / 2)))
                elif mb[0] == 0:
                    first = True

            if tool == 3:  # Tingle
                if mb[0] == 1:
                    if first:
                        back = screen.copy()
                        first = False
                    screen.blit(back, (0, 0))
                    screen.blit(blittinglestamp,
                                (mx - int(blittinglestamp.get_width() / 2), my - int(blittinglestamp.get_height() / 2)))
                elif mb[0] == 0:
                    first = True

            if tool == 4:  # Master Sword
                if mb[0] == 1:
                    if first:
                        back = screen.copy()
                        first = False
                    screen.blit(back, (0, 0))
                    screen.blit(blitmasterswordstamp, (
                    mx - int(blitmasterswordstamp.get_width() / 2), my - int(blitmasterswordstamp.get_height() / 2)))
                elif mb[0] == 0:
                    first = True

            if tool == 5:  # Shield
                if mb[0] == 1:
                    if first:
                        back = screen.copy()
                        first = False
                    screen.blit(back, (0, 0))
                    screen.blit(blitshieldstamp,
                                (mx - int(blitshieldstamp.get_width() / 2), my - int(blitshieldstamp.get_height() / 2)))
                elif mb[0] == 0:
                    first = True

            if tool == 6:  # Triforce
                if mb[0] == 1:
                    if first:
                        back = screen.copy()
                        first = False
                    screen.blit(back, (0, 0))
                    screen.blit(blittriforcestamp, (
                    mx - int(blittriforcestamp.get_width() / 2), my - int(blittriforcestamp.get_height() / 2)))
                elif mb[0] == 0:
                    first = True

            if tool == 7:  # Cucco
                if mb[0] == 1:
                    if first:
                        back = screen.copy()
                        first = False
                    screen.blit(back, (0, 0))
                    screen.blit(blitcuccostamp,
                                (mx - int(blitcuccostamp.get_width() / 2), my - int(blitcuccostamp.get_height() / 2)))
                elif mb[0] == 0:
                    first = True

            if tool == 8:  # Green Rupee
                if mb[0] == 1:
                    if first:
                        back = screen.copy()
                        first = False
                    screen.blit(back, (0, 0))
                    screen.blit(blitgrupeestamp,
                                (mx - int(blitgrupeestamp.get_width() / 2), my - int(blitgrupeestamp.get_height() / 2)))
                elif mb[0] == 0:
                    first = True

            if tool == 9:  # Blue Rupee
                if mb[0] == 1:
                    if first:
                        back = screen.copy()
                        first = False
                    screen.blit(back, (0, 0))
                    screen.blit(blitbrupeestamp,
                                (mx - int(blitbrupeestamp.get_width() / 2), my - int(blitbrupeestamp.get_height() / 2)))
                elif mb[0] == 0:
                    first = True

            if tool == 10:  # Yellow Rupee
                if mb[0] == 1:
                    if first:
                        back = screen.copy()
                        first = False
                    screen.blit(back, (0, 0))
                    screen.blit(blityrupeestamp,
                                (mx - int(blityrupeestamp.get_width() / 2), my - int(blityrupeestamp.get_height() / 2)))
                elif mb[0] == 0:
                    first = True

            if tool == 11:  # Red Rupee
                if mb[0] == 1:
                    if first:
                        back = screen.copy()
                        first = False
                    screen.blit(back, (0, 0))
                    screen.blit(blitrrupeestamp,
                                (mx - int(blitrrupeestamp.get_width() / 2), my - int(blitrrupeestamp.get_height() / 2)))
                elif mb[0] == 0:
                    first = True

    oldmx = mx  # oldmx holds the previous x coordinate
    oldmy = my  # oldmy holds the previous y coordinate
    screen.set_clip(None)  # This resets the clip
    display.flip()
quit()
