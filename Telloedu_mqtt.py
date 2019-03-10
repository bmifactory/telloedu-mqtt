"""
Tello Edu manipulation through MQTT protocol
"""
#import time
#import sys, os
import pygame
from pygame import *
from fly_tello import FlyTello
import paho.mqtt.client as mqtt
#import tellopy
#from subprocess import Popen, PIPE

#For MQTT
MQTT_name = "localhost"
#MQTT_name = "192.168.0.2"
Topic_name = "TelloEDU"

# For tello edu
tello_connected = True
control_mode = True
battery = 0
altitude = 0
speed = 50
duration = 500
dir_flag = 0
updown_flag = 0
rot_flag = False

# Set pygame parameter
fullscreen = False
os.environ['SDL_VIDEO_WINDOW_POS']="%d, %d" % (1360,0)
bg_file_1="Tello_bg_1.jpg"
bg_file_2="Tello_bg_2.jpg"
message_max = 6
message_list = list(range(message_max))
event_log = 0

def init_tello():
    global drone, battery
    my_tellos = list()
    my_tellos.append('0TQDG2KEDB94U4')
    drone = FlyTello(my_tellos, get_status=True)
    drone.pad_detection_on()
    drone.set_pad_detection(direction='downward')
    battery = int(drone.get_status(key='bat', tello=1))
    print('battery is %s' % battery)

def init_pygame():
    global window, background_img, font, fpsClock
    global blackColor, blueColor, whiteColor, greenColor, redColor
    pygame.init()
    font = pygame.font.Font("bgothl.ttf", 20)
    blackColor = pygame.Color(0, 0, 0)
    redColor = pygame.Color(255, 0, 0)
    blueColor = pygame.Color(0, 0, 255)
    whiteColor = pygame.Color(255, 255, 255)
    greenColor = pygame.Color(0, 255, 0)
    window = pygame.display.set_mode((560, 575), pygame.RESIZABLE)
    #window = pygame.display.set_mode((240, 575), pygame.RESIZABLE)
    background_img = pygame.image.load(bg_file_1)
    pygame_update(event_log)
    #fpsClock = pygame.time.Clock()

def init_mqtt():
    # Create MQTT client
    mqttClient = mqtt.Client("Tello1")
    mqttClient.on_connect = on_connect
    mqttClient.on_message = on_message
    # mqttClient.on_message = on_disconnect
    # Connect to MQTT server
    try:
        mqttClient.connect(MQTT_name, 1883, 60)
        print("MQTT Server connected")
        MQTT_connection = 0
        mqttClient.loop_start()
    except:
        print("MQTT Server disconnected")
        MQTT_connection = 1
        pass

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(Topic_name)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global drone, event_log, dir_flag, updown_flag, background_img
    if msg.topic == Topic_name:
        command_str = str(msg.payload)
        print(command_str)
        event_log_update(command_str)
        mqtt_command_img = font.render(command_str, False, whiteColor)
        window.blit(mqtt_command_img, (50, 100))
        if command_str == "b'takeoff'":
            background_img = pygame.image.load(bg_file_2)
            drone.takeoff()
        elif command_str == "b'land'":
            background_img = pygame.image.load(bg_file_1)
            drone.land()
        elif command_str == "b'level1'":
            if dir_flag == 0:
                drone.counter_clockwise(speed)
                pygame.time.wait(2000)
                drone.counter_clockwise(0)
                #drone.right(speed)
                #pygame.time.wait(duration)
                #drone.right(0)
                dir_flag = 1
            elif dir_flag == 1:
                drone.clockwise(speed)
                pygame.time.wait(2000)
                drone.clockwise(0)
                #drone.left(speed)
                #pygame.time.wait(duration)
                #drone.left(0)
                dir_flag = 0
        elif command_str == "b'level2'":
            if battery > 50:
                drone.flip_forward()
            else:
                if dir_flag == 0:
                    drone.counter_clockwise(speed)
                    pygame.time.wait(2000)
                    drone.counter_clockwise(0)
                    dir_flag = 1
                elif dir_flag == 1:
                    drone.clockwise(speed)
                    pygame.time.wait(2000)
                    drone.clockwise(0)
                    dir_flag = 0
        elif command_str == "b'land'":
            drone.land()
        elif command_str == "b'left'":
            drone.left(speed)
            pygame.time.wait(duration)
            drone.left(0)
        elif command_str == "b'right'":
            drone.right(speed)
            pygame.time.wait(duration)
            drone.right(0)
        elif command_str == "b'forward'":
            drone.forward(speed)
            pygame.time.wait(duration)
            drone.forward(0)
        elif command_str == "b'back'":
            drone.backward(speed)
            pygame.time.wait(duration)
            drone.backward(0)
        elif command_str == "b'cw'":
            drone.counter_clockwise(speed)
            pygame.time.wait(duration)
            drone.counter_clockwise(0)
        elif command_str == "b'cw'":
            drone.clockwise(speed)
            pygame.time.wait(duration)
            drone.clockwise(0)
        elif command_str == "b'ccw'":
            drone.counter_clockwise(speed)
            pygame.time.wait(duration)
            drone.counter_clockwise(0)
        elif command_str == "b'up'":
            drone.up(speed)
            pygame.time.wait(duration)
            drone.up(0)
        elif command_str == "b'down'":
            drone.down(speed)
            pygame.time.wait(duration)
            drone.down(0)
        else:
            event_log_update('Wrong comment')

def pygame_update(message_lane):
    global message_list, window, message_img, background_img, battery
    global attention_duration, attention_value, control_mode, takeoff_flag
    font = pygame.font.Font("bgothl.ttf", 20)
    # font = pygame.font.Font("freesansbold.ttf", 20)
    window.blit(background_img, (0, 0))
    for i in list(range(message_max)):
        if (i < message_lane):
            message_img = font.render("# "+str(message_list[i]), False, blackColor)
            window.blit(message_img, (50, 350 + i * 30))
        elif (i == message_lane):
            message_img = font.render("# "+str(message_list[i]), False, blueColor)
            window.blit(message_img, (50, 350 + i * 30))
        else:
            message_img = font.render("", False, whiteColor)
            window.blit(message_img, (50, 270 + i * 30))
    draw_gauge_bar(49, 309, 0, 4*battery, 10)
    #draw_gauge_bar(30, 309, 0, 2*battery, 18)
    battery_str = '{:.1f}'.format(battery)
    font = pygame.font.Font("bgothl.ttf", 30)
    battery_img = font.render(battery_str+"%", False, blueColor)
    window.blit(battery_img, (30, 260))
    pygame.display.update()

def event_log_update(message):
    global event_log, message_list
    message_list[event_log] = message
    pygame_update(event_log)
    event_log = event_log + 1
    if event_log == message_max:
        event_log = 0

def draw_gauge_bar(center_x, center_y, dir, length, width):
    global redColor
    if dir is 0:
        end_x = center_x + length
        end_y = center_y
    else :
        end_x = center_x
        end_y = center_y - length
    pygame.draw.line(window, redColor, (center_x, center_y), (end_x, end_y), width)

def main():
    global window, background_img, font, control_mode, fpsClock
    global blackColor, blueColor, whiteColor, greenColor
    global drone, speed, duration, rot_flag, battery, takeoff_flag, msg

    init_tello()
    init_pygame()
    init_mqtt()

    quit = False
    while quit is False:
        pygame.time.wait(100)
        # loop with pygame.event.get() is too much tight w/o some sleep
        for event in pygame.event.get():
            if event.type == QUIT:
                quit = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    msg = 'ESC'
                    quit = True
                #elif event.key == K_F1:
                #   control_mode = True
                #   background_img = pygame.image.load(bg_file_open)
                elif event.key == K_t:
                    msg = 'takeoff'
                    background_img = pygame.image.load(bg_file_2)
                    #drone.takeoff()
                    #background_img = pygame.image.load(bg_file_2)
                elif event.key == K_l:
                    msg = 'land'
                    #background_img = pygame.image.load(bg_file_1)
                    #drone.land()
                    background_img = pygame.image.load(bg_file_1)
                    takeoff_flag = False
                elif event.key == K_LEFT:
                    msg = 'left'
                    drone.left(speed)
                elif event.key == K_RIGHT:
                    msg = 'right'
                    drone.right(speed)
                elif event.key == K_UP:
                    msg = 'forward'
                    drone.forward(speed)
                elif event.key == K_DOWN:
                    msg = 'back'
                    drone.backward(speed)
                elif event.key == K_HOME:
                    msg = 'ccw'
                    drone.counter_clockwise(speed)
                elif event.key == K_END:
                    msg = 'cw'
                    drone.clockwise(speed)
                elif event.key == K_PAGEUP:
                    msg = 'up'
                    drone.up(speed)
                elif event.key == K_PAGEDOWN:
                    msg = 'down'
                    drone.down(speed)
                elif event.key == K_r:
                    if rot_flag:
                        msg = 'Rotation stop'
                        drone.clockwise(0)
                        rot_flag = False
                    else:
                        msg = 'Rotation start'
                        drone.clockwise(50)
                        rot_flag = True
                elif event.key == K_f:
                    if battery > 50:
                        msg = 'Flip forward'
                        drone.flip_forward()
                    else:
                        msg = 'Low battery to flip < 50%'
                else:
                    msg = 'Wrong Key'
                event_log_update(msg)

        pygame.display.update()
        # fpsClock.tick(25)
    drone.land()
    exit(1)

if __name__ == '__main__':
    main()