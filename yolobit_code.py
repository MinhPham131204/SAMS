
# Import các thư viện cần thiết
import urequests
import gc
import ujson
from yolobit import *
from aiot_lcd1602 import LCD1602
from yolobit_wifi import *
from aiot_dht20 import DHT20

# Đăng ký trống các sự kiện nhấn nút 
button_a.on_pressed = None
button_b.on_pressed = None
button_a.on_pressed_ab = button_b.on_pressed_ab = -1

# Đăng ký các chân GPIO cho các thiết bị
aiot_lcd1602 = LCD1602()
aiot_lcd1602.clear()
aiot_dht20 = DHT20()

# Hàm hỗ trợ hiển thị LCD
def showLCD(msg, line_idx = 0):
    print(msg)
    aiot_lcd1602.move_to(0, line_idx)
    aiot_lcd1602.putstr(f"{msg}{" " * (16-len(msg))}")

# Hàm upload dữ liệu cảm biến lên server và download trạng thái thiết bị
def auto_update_all_status():
    global http_response,aiot_dht20

    # Lấy dữ liệu cảm biến
    aiot_dht20.read_dht20()
    temperatue = aiot_dht20.dht20_temperature()
    humidity = aiot_dht20.dht20_humidity()
    light = round(translate((pin1.read_analog()), 0, 4095, 0, 100))
    soil_moisture = round(translate((pin0.read_analog()), 0, 4095, 0, 100))
    stats = f"{temperatue}-{humidity}-{light}-{soil_moisture}"
    # Cập nhật trạng thái cảm biến lên LCD
    showLCD(stats, 0)
    
    # Gửi dữ liệu lên server
    print("Sending data to server...")
    postData = {"temp":temperatue,"hum":humidity,"lig":light,"soil":soil_moisture}
    gc.collect()
    http_response = urequests.post(
        "http://sams.akng.io.vn/enviroment/update",
        data=None,
        json=(postData),
    )

    # Nhận trạng thái thiết bị từ server
    response = ujson.loads(http_response.text)
    fan_state = [device['state'] for device in response['data'] if device['device_name'] == 'mini_fan'][0]
    pump_state = [device['state'] for device in response['data'] if device['device_name'] == 'water_pump'][0]
    # Set trạng thái thiết bị
    pin10.write_analog(round(translate(fan_state * 50, 0, 100, 0, 1023)))
    pin14.write_analog(round(translate(pump_state * 70, 0, 100, 0, 1023)))
    # Cập nhật trạng thái thiết bị lên LCD
    showLCD(f"FAN:{"ON" if fan_state == 1 else "OFF"}-PUMP:{"ON" if pump_state == 1 else "OFF"}", 1)


# Vùng hàm chính
if True:
    showLCD("Init...")
    display.scroll("!")
    
    showLCD("Connect wifi...")
    wifi_name = "ACLAB"
    wifi_pwd = "ACLAB2023"
    wifi.connect_wifi(wifi_name, wifi_pwd)
    showLCD("Connected!")
    
    while True:
        auto_update_all_status()
