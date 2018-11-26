#-- include('examples/showgrabfullscreen.py') --#
from PIL import ImageGrab

if __name__ == '__main__':

    # grab fullscreen
    im = ImageGrab.grab()

    # save image file
    im.save('screenshot.png')

    # show image in a window
#-#