import tkinter as tk
from tkinter import messagebox, filedialog
import rospy
from clover import srv
from std_srvs.srv import Trigger
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from PIL import Image as PILImg, ImageTk
import threading
from datetime import datetime
import math
import json
import csv

z = float(0)
speed = float(0)
rospy.init_node('flight_control_ui')

bridge= CvBridge()
fbody_cascade = cv2.CascadeClassifier('/home/clover/catkin_ws/code2/haarcascade_fullbody.xml')

latest_img = None
lock = threading.Lock()
video_writer = None
flight_plan = None
running_mode = None

get_telemetry = rospy.ServiceProxy("get_telemetry", srv.GetTelemetry)
navigate_global = rospy.ServiceProxy("navigate_global", srv.NavigateGlobal)
land = rospy.ServiceProxy("land", Trigger)
navigate = rospy.ServiceProxy("navigate", srv.Navigate)

start = get_telemetry()
home_position = [start.lat,start.lon]

#sozdanie csv
def create_telemetry_csv():
    time = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
    filename = f'telemetry_{time}.csv'

    with open(filename ,mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Time','X','Y','Z','Lat','Lon'])
    return filename

#zapis telemetrii
def record_telemetry_to_csv(filename):
    try:
        telem = get_telemetry()
        with open(filename, mode ='a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([
                datetime.now().strftime('%Y-%m-%d_%H_%M_%S'),
                telem.x,
                telem.y,
                telem.z,
                telem.lat,
                telem.lon,
            ])
    except Exception as t :
        status_label.config(text=f'Oshibka zapisi {t}')



#Start zapisi telemetry
def start_telemetry_recording():
    global telemetry_filename
    telemetry_filename = create_telemetry_csv()

    def record_telemetry():
        while True:
            record_telemetry_to_csv(telemetry_filename)
            rospy.sleep(5)
    threading.Thread(target=record_telemetry,daemon = True).start()




def camera_image(msg):
    global latest_img
    with lock:
        latest_img = bridge.imgmsg_to_cv2(msg,'bgr8')

image_sub = rospy.Subscriber('main_camera/image_raw',Image,camera_image,queue_size=1)

def update_image():
    if latest_img is not None:
        with lock:
            img_rgb = cv2.cvtColor(latest_img, cv2.COLOR_BGR2RGB)
            img_pil =PILImg.fromarray(img_rgb)
            img_tk = ImageTk.PhotoImage(image = img_pil)

            camera_label.config(image = img_tk)
            camera_label.image = img_tk

    window.after(100, update_image)


#autoobnov visoti
def update_latitude():
    try:
        telem = get_telemetry()
        latitude = telem.z
        alt_label.config(text=f'Tekusia visote {latitude:.2f} m')
    except:
        alt_label.config(text=f'Aiiia balatb ')
    window.after(1000, update_latitude)

def arrirval_wait(tolerance= 0.2):
    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id = 'navigate_target')
        if math.sqrt(telem.x**2 + telem.y**2 + telem.z**2) < tolerance:
            break
        rospy.sleep(0.45)

def takeoff():
    global z
    global speed
    try:
        if entry_z.get():
            z = float(entry_z.get())
        else:
            z = float(2)
        if entry_speed.get():
            speed = float(entry_speed.get())
        else:
            speed = float(2)
        threading.Thread(target = navigate,args = (0 ,0 ,z ,1 ,0 ,'body' ,True)).start()
    except:
        status_label.config(text='OSIBKA vvtdite kerroktno visotu i skorost')    


def land_drone():
    threading.Thread(target=land).start()
    status_label.config(text='Dron soditcia')

def fly_to_local_coordin():
    global z
    global speed
    try:
        if entry_x.get():
            x = float(entry_x.get())
        else: 
            x = 0
        if entry_y.get():
            y = float(entry_y.get())
        else:
            y = 0
        if entry_z.get():
            z = float(entry_z.get())
        else:
            if z != 0:
                z = float(0)
        if entry_speed.get():
            speed = float(entry_speed.get())
        else: 
            speed = float(1.0)
        
        arrirval_wait()
        threading.Thread(target=navigate, args=(x ,y ,z ,speed ,0 ,'body' ,False)).start()+69
        status_label.config(text=f'Dron dostig {x}, {y}, {z} parametrov' )
    except Exception as t:
        status_label.config(text=f'{t}' )


def fly_to_glob_coordinate():
    try:
        lat = float(entry_lat.get())
        lon = float(entry_lon.get())
        z = float(entry_z.get())
        if entry_z.get():
            z = float(entry_z.get())
        else:
            z = 3
        if entry_speed.get():
            speed = float(entry_speed.get())
        else:
            speed = 1.0
        threading.Thread(target=navigate_global, args=(lat, lon, z, speed, 0, 'map', False)).start()
        status_label.config(text='Dron dostig')
    except:    
        status_label.config(text='vvedite korrctnii znachenIA')

#vozvrat domoi
def fly_home():
    if home_position[0] is None or home_position[1] is None:
        status_label.config(text='Oshibka: net tocki vzleta')
        return
    
    lat,lon = home_position[0], home_position[1]
    if entry_z.get():
        z = float(entry_z.get())
    else:
        z = 3.0
    threading.Thread(target=navigate_global, args=(lat, lon, z, 0, 1, 'map', False)).start()
    status_label.config(text='Vozvrat domoi')


def show_telemetry():
    telem = get_telemetry()
    status_label.config(text=f'Sirota={telem.lat}, Dolgota={telem.lon} ')

def download_plan(filename):
    with open(filename, 'r') as file:
        return json.load(file)
    
def browse_plan():
    filename = filedialog.askopenfilename(filetypes=[('Flying Plan Files', '*.plan')])
    if filename:
        if filename.endswith('.plan'):
            try:
                global flight_plan
                flight_plan = download_plan(filename)
                status_label.config(text=f'{filename} download')
            except:
                messagebox.showerror('ALARM','Ne zagruzhen file')
        else:
            messagebox.showerror('ALARM','Tebe nezen file c .plan')


 

# Остановка записи видео

def stop_video_recording():
    global video_writer
    if video_writer is not None:
        video_writer = None
        messagebox.showinfo("Запись", "Видео успешно сохранено!")
    




#raspoznovanie obj kascadom
def detect_objects():
    global latest_img
    while running_mode =='objects':
        with lock:
            if latest_img is None:
                continue
            img = latest_img.copy()
        
        gray =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        objects = fbody_cascade.detectMultiScale(gray,scaleFactor = 1.05,minNeighbors = 2,minSize = (40, 40))

        for (x,y,w,h) in objects:
            cv2.rectangle(img,(x,y),(x + w,y + h),(0, 255, 0), 2)
        display_image(img)

#Pokaz obrabotannogo img
def display_image(img):
    global video_writer
    img_rgb = cv2.cvtColor(latest_img, cv2.COLOR_BGR2RGB)
    img_pil =PILImg.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(image = img_pil)

    camera_label.config(image = img_tk)
    camera_label.image = img_tk

    if video_writer is not None:
        video_writer.write(img)


#Zapusk rezima raspoznovanie obj
def start_object_detection():
    stop_detection()
    global running_mode
    running_mode = 'objects'
    threading.Thread(target=detect_objects,daemon =True).start()



#Ostanovka rezima
def stop_detection():
    global running_mode
    running_mode = None

#Zapis video
def start_video_recording():
    global video_writer
    
    if video_writer is not None:
        messagebox.showinfo('Zapis','Zapis uzu idet')
        return
    
    time = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
    filename = f'output_{time}.avi'

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(filename, fourcc, 30.0, (320,240))

    def record():
        global latest_img
        while video_writer is not None:
            with lock:
                if latest_img is None:
                    continue
                video_writer.write(latest_img)
            rospy.sleep(0.03)#30 frame/second

    threading.Thread(target=record,daemon= True).start()
    


def fly_by_plan():
    if flight_plan is None:
        messagebox.showerror('ALARM','Plan pleta ne zagruzen')
        return
    def run_flight_plan():
        coordinates = []
        home_lat = flight_plan['mission']['plannedHomePosition'][0]
        home_lon = flight_plan['mission']['plannedHomePosition'][1]

        for item in flight_plan['mission']['items']:
            command = item['command']
            if command == 16:
                coordinates.append((item['params'][4], item['params'][5]))
        print(coordinates)
        for item in flight_plan['mission']['item']:
            command = item['command']
            z = item['params'][6]
            if command == 22:
                if get_telemetry().armed:
                    navigate_global(lat = home_lat, lon =home_lon, z = 3,yaw=math.inf, speed=1,frame_id='map')
                    arrirval_wait()
                    land()
                else:
                    navigate_global(lat = home_lat, lon =home_lon, z = z,yaw=math.inf, speed=1,frame_id='map', auto_arm = True)
                    navigate_global(lat = home_lat, lon =home_lon, z = z,yaw=math.inf, speed=1,frame_id='map')
                    arrirval_wait()
                    for lat,lon in coordinates:
                        navigate_global(lat = lat, lon =lon, yaw=math.inf, speed=1,frame_id='map') 
                        print(lat,lon)
                        arrirval_wait()
            elif command == 20:
                navigate_global(lat = home_lat, lon =home_lon, z = 3,yaw=math.inf, speed=1,frame_id='map')
                arrirval_wait()
            elif command == 21:
                land()        
    threading.Thread(target=run_flight_plan).start()


#Interfeise
window = tk.Tk()
window.config(bg ='black')
window.title('settings')
window.geometry('1080x550')
window.resizable(False,False)

tk.Label(window, text = 'Visota vzleta v metrax: ').grid(row = 0, column=0,padx = 20)
entry_z = tk.Entry(window,width= 15,bg= 'silver')
entry_z.grid(row =0, column=1,pady = 10)

tk.Label(window, text = 'Koordinata X:  ').grid(row = 1, column=0, padx = 20)
entry_x = tk.Entry(window,width= 15,bg= 'silver')
entry_x.grid(row =1, column=1,pady = 10)

tk.Label(window, text = 'Koordinata Y:  ').grid(row = 2, column=0, padx = 20)
entry_y = tk.Entry(window,width= 15,bg= 'silver')
entry_y.grid(row =2, column=1,pady = 10)

tk.Label(window, text = 'sirota:  ').grid(row = 3, column=0, padx = 20)
entry_lat = tk.Entry(window,width= 15,bg= 'silver')
entry_lat.grid(row =3, column=1,pady = 10)

tk.Label(window, text = 'dolgota:  ').grid(row = 4, column=0, padx = 20)
entry_lon = tk.Entry(window,width= 15,bg= 'silver')
entry_lon.grid(row =4, column=1,pady = 10)

tk.Label(window, text = 'Skorost m/s:  ').grid(row = 5, column=0, padx = 20)
entry_speed = tk.Entry(window,width= 15,bg= 'silver')
entry_speed.grid(row =5, column=1,pady = 10)

status_label = tk.Label(window, text = 'Tecusie Sostoianie drona',fg='blue')
status_label.grid(row= 10, column=0, columnspan=2 )

alt_label = tk.Label(window, text = 'Tecusie Sostoianie drona',fg='blue')
alt_label.grid(row= 10, column=2, columnspan=2 )


# camera

camera_label = tk.Label(window)
camera_label.grid(row= 0,column=2, rowspan=5,padx = 40, pady=10)

tk.Button(window, text ='Raspoznat obj', width=20, bg='green',fg='white',command=start_object_detection).grid(row=6,column=2,padx =20, pady= 10)
tk.Button(window, text ='Ostonovit', width=20, bg='red',fg='white',command=stop_detection).grid(row=7,column=2)
tk.Button(window, text ='REC', width=20, bg='green',fg='white',command=start_video_recording).grid(row=7,column=3)
tk.Button(window, text ='STOP REC', width=20, bg='green',fg='white', command=stop_video_recording).grid(row=6,column=3)


takeoff_button = tk.Button(window,text = 'Vzlet', width= 20,bg ='green',fg='white'
                           ,activebackground = 'silver', command=takeoff).grid(row=6, column=0,pady =10)

land_button = tk.Button(window,text = 'Posadka', width= 20,bg ='red',fg='white'
                           ,activebackground = 'silver', command=land_drone).grid(row=7, column=0,pady=10) 

glod_fly_button = tk.Button(window,text = 'Glob. coordin', width= 20,bg ='white',fg='black'
                           ,activebackground = 'silver',command=fly_to_glob_coordinate).grid(row=8, column=0,pady=10) 

home_button = tk.Button(window,text = 'Flying Home', width= 20,bg ='white',fg='black'
                           ,activebackground = 'silver',command=fly_home).grid(row=9, column=0,pady=10) 

local_coordinates_buttom = tk.Button(window,text = 'Local.Koordin', width= 20,bg ='white',fg='black'
                           ,activebackground = 'silver',command=fly_to_local_coordin).grid(row=8, column=1,pady=10)

reclam_buttom = tk.Button(window,text = 'Tvoia reklama', width= 20,bg ='white',fg='black'
                           ,activebackground = 'silver' ).grid(row=9, column=1,pady=10)

load_plan_buttom = tk.Button(window,text = 'Zagruzi plan', width= 20,bg ='white',fg='black'
                           ,activebackground = 'silver',command=browse_plan).grid(row=8, column=2,pady=10) 

run_plan_buttom = tk.Button(window,text = 'Active plan', width= 20,bg ='white',fg='black'
                           ,activebackground = 'silver',command=fly_by_plan).grid(row=8, column=3,pady=10) 

#jstalnie knopki
record_telemetry_buttom = tk.Button(window,text = 'Zapis telemetry', width= 20,bg ='white',fg='black'
                           ,activebackground = 'silver', command=start_telemetry_recording).grid(row=6, column=1,pady=10)


window.after(100, update_image)
window.after(1000,update_latitude)
window.mainloop()
