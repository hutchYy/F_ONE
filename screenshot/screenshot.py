from PIL import ImageGrab
# grab fullscreen
im = ImageGrab.grab()
# save image file
im.save('screenshot.png')