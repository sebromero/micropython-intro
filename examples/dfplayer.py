from machine import Pin, UART
from DFPlayer import DFPlayer

player = DFPlayer(uart=UART(0, tx=Pin("A2"), rx=Pin("A3"), baudrate=9600))
player.next()