# Original author: @ubidefeo
from Button import Button

# the following method (function) will be invoked
# when the button changes state
# the Button module expects a callback to handle 
# - pin number
# - event (Button.PRESSED | Button.RELEASED)
# the event contains a string 'pressed' or 'released'
# which can be used in your code to act upon
def button_change(button, event):
    print(f'🔘 Button on pin {button} has been {event}')

# we define a variable which holds a Button
# this Button object will be created using:
# - a pin number (GPIOx)
# - the state at rest (value() is False by default)
# - a callback to invoke when the button changes state (see above)
button_one = Button(25, False, button_change) # GPIO25 = D2 on Nano RP2040 Connect
print()

while(True):
    button_one.update()