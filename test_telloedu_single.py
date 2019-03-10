from fly_tello import FlyTello
my_tellos = list()

# Define the Tello's we're using, in the order we want them numbered
my_tellos.append('0TQDG2KEDB94U4')

fly = FlyTello(my_tellos, get_status=True)

# Control the flight
#fly.pad_detection_on()
#fly.set_pad_detection(direction='downward')
#fly.get_battery(sync=True)
#fly.print_status()
battery = fly.get_status(key='bat', tello=1)
print(battery)
#fly.takeoff()
    #fly.forward(dist=50)
    #fly.back(dist=50)
#fly.reorient(height=120, pad='m1')
#fly.left(dist=80)
    #fly.flip(direction='left')
#fly.reorient(height=120, pad='m2')
    #fly.curve(x1=50, y1=30, z1=0, x2=100, y2=30, z2=-20, speed=60)
    #fly.curve(x1=-50, y1=-30, z1=0, x2=-100, y2=-30, z2=20, speed=60)
    #fly.reorient(height=100, pad='m1')
#fly.rotate_cw(angle=90, tello=1)
    #fly.straight_from_pad(x=30, y=0, z=75, speed=100, pad='m1')
    #fly.flip(direction='back')
#fly.reorient(height=60, pad='m2')
#fly.land()