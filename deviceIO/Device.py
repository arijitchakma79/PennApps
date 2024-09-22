from gpiozero import Button, LED

class Device:
    def __init__(self):
        self.__btn1 = Button(6, pull_up=True)
        self.__btn2 = Button(0, pull_up=True)
        self.__led = LED(21)

        self.__led.off()

    def is_button1_pressed(self):
        return self.__btn1.is_pressed
    
    def is_button2_pressed(self):
        return self.__btn2.is_pressed