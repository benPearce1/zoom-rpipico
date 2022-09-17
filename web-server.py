import network
import socket
from picozero import pico_temp_sensor, pico_led
from machine import Pin, SPI
import max7219
from time import sleep

displaySize=4

ssid = ''
password = ''

spi = SPI(0,sck=Pin(2),mosi=Pin(3))
cs = Pin(5, Pin.OUT)
display = max7219.Matrix8x8(spi, Pin(5), displaySize)

display.brightness(3)
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
        pulse()
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
            updateDisplay(body)
            
        temperature = pico_temp_sensor.temp
        html = webpage(temperature, state)
        client.send(html)
        display.show()
        client.close()
        
def pulse():
    display.pixel(31,0,1)
    display.show()
    sleep(0.2)
    display.pixel(31,0,0)
    display.show()
def updateDisplay(data):
    if 'Unmuted' in data:
        showAudio()
    if 'Muted' in data:
        hideAudio()
    if 'On' in data:
        showVideo()
    if 'Off' in data:
        hideVideo()
    
def showAudio():
    audio(True)
    
def hideAudio():
    audio(False)
    
def showVideo():
    video(True)
    
def hideVideo():
    video(False)

def audio(on):
    col = 0
    if on == True:
        col = 1
    if displaySize == 1:
        display.fill_rect(0,0,3,3,col)
    else:
        display.fill_rect(16,4,3,3,col)
        display.fill_rect(21,4,3,3,col)
        display.line(17,2,17,3,col)
        display.line(18,1,21,1,col)
        display.line(22,2,22,3,col)
        
def video(on):
    col = 0
    if on == True:
        col = 1

    if displaySize == 1:
        display.line(7,3,7,7,col)
        display.line(6,4,6,6,col)
        display.pixel(5,5,col)
    else:
        display.fill_rect(0,1,5,6,col)
        display.line(7,1,7,6,col)
        display.line(6,2,6,5,col)
        display.pixel(5,3,col)
        display.pixel(5,4,col)
    
def max7219():
    print("max7219")
    display.pixel(31,7,1)
    display.show()

try:
    max7219()
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
    

