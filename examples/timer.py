from machine import Timer, Pin

builtin_led = Pin("LED", Pin.OUT) # LED = GPIO6, Built-in LED on the Nano RP2040 Connect
external_led = Pin("D12", Pin.OUT)
external_led.on()

led_timeout = Timer(-1)
led_interval = Timer(-1)

led_timeout.init(mode=Timer.ONE_SHOT, period=4000, callback=lambda _: external_led.off())
led_interval.init(period=250, callback=lambda _: builtin_led.toggle())
