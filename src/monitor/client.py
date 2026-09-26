import random
x_pos = 0
y_pos = 0
def get_latest_data():
    global x_pos, y_pos
    x_pos += random.uniform(-1.0, 1.0)
    y_pos += random.uniform(-1.0, 1.0)
    return{
        "t":random.uniform(0,30),
        "roll":random.uniform(-5,5),
        "pitch":random.uniform(-5,5),
        "yaw":random.uniform(0,360),
        "x":x_pos,
        "y":y_pos,
        "state":random.choice(["SEARCH","APPROACH","GOAL"]),
        "goal":random.choice([True,False]),
        "color":random.choice(["赤","青","緑",""]),
    }
import tkinter as tk
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(True)
root=tk.Tk()
start_time = 0
mode="LIVE"
history = []
history_index = -1
def stop_playback():
    global mode
    mode = "STOP"
def start_playback():
    global mode
    mode = "LIVE"
def prev_frame():
     print("前へ")
     global history_index
     if history_index > 0:
        history_index -= 1
        data = history[history_index]
        x_value.config(text=f"X : {data['x']:.2f}")
        y_value.config(text=f"Y : {data['y']:.2f}")
        roll_value.config(text=f"Roll : {data['roll']:.1f}")
        pitch_value.config(text=f"Pitch : {data['pitch']:.1f}")
        yaw_value.config(text=f"Yaw : {data['yaw']:.1f}")
def next_frame():
     print("次へ")
     global history_index
     if history_index < len(history)-1:
        history_index += 1
        data = history[history_index]
        x_value.config(text=f"X : {data['x']:.2f}")
        y_value.config(text=f"Y : {data['y']:.2f}")
        roll_value.config(text=f"Roll : {data['roll']:.1f}")
        pitch_value.config(text=f"Pitch : {data['pitch']:.1f}")
        yaw_value.config(text=f"Yaw : {data['yaw']:.1f}")      
txt_file = open("telemetry.txt", "a", encoding="utf-8")
log_file = open("telemetry.log", "a", encoding="utf-8")
current_marker = None
last_px = None
last_py = None
root.title("CanSat状況モニター")
root.attributes("-fullscreen", True)
top_frame=tk.Frame(root,height=50)
top_frame.pack(fill="x")
title_label=tk.Label(top_frame,text="CanSat状況モニター",font=("Arial",20,"bold"))
title_label.pack(side="left")
mode_labe=tk.Label(top_frame,text="モード：ライブ")
mode_labe.pack(side="left")
time_label=tk.Label(top_frame,text="経過：00:00")
time_label.pack(side="right")

main_frame=tk.Frame(root)
main_frame.pack(fill="both",expand=True)
bottom_frame=tk.Frame(root,height=40)
bottom_frame.pack(fill="x",side="bottom")
btn_prev=tk.Button(bottom_frame,text="<< 前へ", command=prev_frame)
btn_play=tk.Button(bottom_frame, text="▶ 再生", command=start_playback)

btn_stop=tk.Button(bottom_frame,text="■ 停止",command=stop_playback)
btn_next=tk.Button(bottom_frame,text="次へ >>",command=next_frame)
btn_prev.pack(side="left",padx=5)
btn_play.pack(side="left",padx=5)
btn_stop.pack(side="left",padx=5)
btn_next.pack(side="left",padx=5)
info_frame=tk.Frame(main_frame,width=400)
info_frame.pack(side="right",fill="y")
info_frame.pack_propagate(False)
def create_frame(parent, title):
    frame = tk.LabelFrame(parent,text=title,font=("Arial", 24))
    frame.pack(fill="x", padx=5, pady=5)
    return frame
pose_frame = create_frame(info_frame, "姿勢")
pos_frame = create_frame(info_frame, "位置")
state_frame = create_frame(info_frame, "探索状態")
color_frame = create_frame(info_frame, "色検出")
goal_frame = create_frame(info_frame, "ゴール検出")
comm_frame = create_frame(info_frame, "通信状況")
comm_value=tk.Label(comm_frame,text="通信OK",font=("Arial",24))
roll_value = tk.Label(pose_frame, text="Roll : ---", font=("Arial",24))
pitch_value = tk.Label(pose_frame, text="Pitch : ---", font=("Arial",24))
yaw_value = tk.Label(pose_frame, text="Yaw : ---", font=("Arial",24))
roll_value.pack(anchor="w")
pitch_value.pack(anchor="w")
yaw_value.pack(anchor="w")

x_value = tk.Label(pos_frame, text="X : ---", font=("Arial",24))
y_value = tk.Label(pos_frame, text="Y : ---", font=("Arial",24))

x_value.pack(anchor="w")
y_value.pack( anchor="w")
state_value = tk.Label(state_frame, text="---", height=2, font=("Arial",24))
state_value.pack(fill="x")

color_value = tk.Label(color_frame, text="---", font=("Arial",24))
color_value.pack(fill="x")

goal_value = tk.Label(goal_frame, text="---", height=2, font=("Arial",24))
goal_value.pack(fill="x")


comm_value.pack()
map_area=tk.Canvas(main_frame,width=400, height=570,bg="white")
map_area.pack(side="left",fill="both",expand=True)
root.update()
current_marker = None
last_px = None
last_py = None
CENTER_X = map_area.winfo_width() // 2 
CENTER_Y = map_area.winfo_height() // 2
SCALE = SCALE = min(map_area.winfo_width(),map_area.winfo_height()) / 400
map_area.create_oval( CENTER_X-4, CENTER_Y-4, CENTER_X+4, CENTER_Y+4, fill="green")
map_area.create_text( CENTER_X, CENTER_Y+20, text="START", font=("Arial",16))
goal_x = 150
goal_y = 100
goal_px = CENTER_X + goal_x * SCALE
goal_py = CENTER_Y - goal_y * SCALE
map_area.create_text( goal_px, goal_py, text="★", font=("Arial",24,"bold"), fill="gold")
map_area.create_text(goal_px,goal_py + 20,text="GOAL",font=("Arial",16))
last_px = None
last_py=None

def update_data():
    global current_marker
    global last_px
    global last_py
    global start_time
    global mode
    global history
    global history_index
    if mode == "STOP":
        root.after(1000, update_data)
        return
    data = get_latest_data()
    history.append(data)
    history_index = len(history) - 1
    start_time += 1
    minutes = start_time // 60
    seconds = start_time % 60

    time_label.config(text=f"経過：{minutes:02d}:{seconds:02d}")
    log_file.write(
    f"X={data['x']:.2f}, "
    f"Y={data['y']:.2f}, "
    f"Roll={data['roll']:.1f}, "
    f"Pitch={data['pitch']:.1f}, "
    f"Yaw={data['yaw']:.1f}, "
    f"State={data['state']}, "
    f"Goal={data['goal']}, "
    f"Color={data['color']}\n")

    log_file.flush()
    txt_file.write(
    f"X={data['x']:.2f}, "
    f"Y={data['y']:.2f}, "
    f"Roll={data['roll']:.1f}, "
    f"Pitch={data['pitch']:.1f}, "
    f"Yaw={data['yaw']:.1f}, "
    f"State={data['state']}, "
    f"Goal={data['goal']}, "
    f"Color={data['color']}\n")

    txt_file.flush()

    if data is None:
        root.after(500, update_data)
        return

    px = CENTER_X + data["x"] * SCALE
    py = CENTER_Y - data["y"] * SCALE

    if last_px is not None:
        map_area.create_line( last_px, last_py, px, py, fill="black", width=2 )
    last_px = px
    last_py = py

    if current_marker is not None:
        map_area.delete(current_marker)

    current_marker = map_area.create_oval( px - 5, py - 5, px + 5,py + 5, fill="red", outline="black")

    x_value.config(text=f"X : {data['x']:.2f}")
    y_value.config(text=f"Y : {data['y']:.2f}")
    roll_value.config(text=f"Roll : {data['roll']:.1f}")
    pitch_value.config(text=f"Pitch : {data['pitch']:.1f}")
    yaw_value.config(text=f"Yaw : {data['yaw']:.1f}")

    state = data["state"]

    if state == "SEARCH":
        state_value.config(text="探索中", bg="lightblue")
    elif state == "APPROACH":
        state_value.config(text="接近中", bg="orange")
    elif state == "GOAL":
        state_value.config(text="到達!", bg="red")
    else:
        state_value.config(text="不明", bg="gray")

    if data["goal"]:
        goal_value.config(
            text="検出!",
            bg="red",
            fg="white"
        )
    else:
        goal_value.config(
            text="---",
            bg="lightgray",
            fg="black"
        )

    if data["color"] == "":
        color_value.config(text="未検出")
    else:
        color_value.config(text=data["color"])

    root.after(1000, update_data)


update_data()
root.mainloop()