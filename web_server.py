import network
import socket
from picozero import pico_temp_sensor, pico_led
from machine import Pin, SPI
import max7219
from time import sleep

ssid = '***REMOVED***'
password = '***REMOVED***'

spi = SPI(0,sck=Pin(2),mosi=Pin(3))
cs = Pin(5, Pin.OUT)
display = max7219.Matrix8x8(spi, Pin(5), 1)
display.brightness(5)
display.show()

def connect():
    # connect to wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    print(wlan.ifconfig())
    ip = wlan.ifconfig()[0]
    return ip

def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(temperature, state):
    html = f"""
            <!DOCTYPE html>
            <html>
            <body>
              <form action="./lighton">
                <input type="submit" value="Light on"/>
              </form>
              <form action="./lightoff">
                <input type="submit" value="Light off"/>
              </form>
              <p>LED is {state}</p>
              <p>Temperature is {temperature}</p>
              
            </body>

            </html>
            """
    return str(html)

def serve(connection):
    state = 'OFF'
    pico_led.off()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = request.decode('utf-8')
        try:
            requestParts = request.splitlines()
            
            print(requestParts)
            #print(request.splitlines())
            verb = requestParts[0].split()[0]
            request = requestParts[0].split()[1]
            print(request)
            #print(verb)
        except IndexError:
            pass
        if request == '/lighton?':
            pico_led.on()
            state = 'ON'
        elif request == '/lightoff?':
            pico_led.off()
            state = 'OFF'
        elif 'POST' in verb:
            print('POST')
            body = requestParts[-1]
            print(body)
            if 'Unmuted' in body:
                display.fill_rect(0,0,3,3,1)
            if 'Muted' in body:
                display.fill_rect(0,0,3,3,0)
            if 'On' in body:
                display.line(7,3,7,7,1)
                display.line(6,4,6,6,1)
                display.pixel(5,5,1)
            if 'Off' in body:
                display.line(7,3,7,7,0)
                display.line(6,4,6,7,0)
                display.pixel(5,5,0)
                
        temperature = pico_temp_sensor.temp
        html = webpage(temperature, state)
        client.send(html)
        display.show()
        client.close()

def max7219():
    print("max7219")
    display.pixel(0,7,1)
    display.show()

try:
    max7219()
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
    
