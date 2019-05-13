def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()

def heroku_mess_request():
    LED = machine.Pin(2, machine.Pin.OUT)
    LED.value(not LED.value())
    http_get("http://***.herokuapp.com/esp")
    print("Data sent\n")
    LED.value(not LED.value())

def heroku_wake_up_request():
    LED = machine.Pin(2, machine.Pin.OUT)
    LED.value(not LED.value())
    http_get("http://***.herokuapp.com/")
    gc.collect()
    LED.value(not LED.value())

def set_wifi_connection(wifis_arr):
    wlan = network.WLAN(network.STA_IF)
    ssid, password, first = '', '', True
    wlan.active(True)
    scanned = wlan.scan()
    for i in scanned:
        for wifi in wifis_arr:
            if(i[0].decode() == wifi[0]):
                if(first):
                    ssid, password, first = wifi[0], wifi[1], False
    if(ssid == ''):
        wlan.active(False)
        return False
    else:
        wlan.connect(ssid, password)
        machine.Pin(2, machine.Pin.OUT).off()
        time.sleep(2)
        machine.Pin(2, machine.Pin.OUT).on()
        time.sleep(1)
        return wlan
def set_wifi_access_point(ssid, passw):
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=passw)
    machine.Pin(2, machine.Pin.OUT).off()
    time.sleep(2)
    machine.Pin(2, machine.Pin.OUT).on()
    time.sleep(1)
    return ap

st = set_wifi_connection([('SSID', 'password')])
ap = set_wifi_access_point('mAccessPoint', 'password')

def flash_button_hander(p):
    LED = machine.Pin(2, machine.Pin.OUT)
    LED.value(not LED.value())
    mess = "LED value is " + str(1 - LED.value())
    print(mess)
    if(1 - LED.value() == 0):
        heroku_wake_up_request()
    gc.collect()
flash_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
flash_button.irq(handler= flash_button_hander, trigger= machine.Pin.IRQ_FALLING)

def sen_hander(p):
    heroku_mess_request()
    print("Something Moving!")

sen = machine.Pin(4, machine.Pin.IN)
sen.irq(handler= sen_hander, trigger= machine.Pin.IRQ_RISING)

min_couter = 0
def timer_callback(t):
    global min_couter
    min_couter += 1
    if(9 < min_couter):
        heroku_wake_up_request()
        min_couter = 0
        print("Heroku wake up request sent")
    else:
        print(min_couter)

tim = machine.Timer(-1)
tim.init(period=60000, mode=machine.Timer.PERIODIC, callback=timer_callback)

heroku_wake_up_request()

gc.collect()
