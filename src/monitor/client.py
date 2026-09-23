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
current_marker = None
last_px = None
last_py = None
root.geometry("1000x650")
root.title("CanSat状況モニター")


top_frame=tk.Frame(root,height=50)
top_frame.pack(fill="x")
title_label=tk.Label(top_frame,text="CanSat状況モニター")
title_label.pack(side="left")
mode_labe=tk.Label(top_frame,text="モード：ライブ")
mode_labe.pack(side="left")
time_label=tk.Label(top_frame,text="経過：00:00")
time_label.pack(side="right")

main_frame=tk.Frame(root)
main_frame.pack(fill="both",expand=True)
bottom_frame=tk.Frame(root,height=40)
bottom_frame.pack(fill="x",side="bottom")
btn_prev=tk.Button(bottom_frame,text="<< 前へ")
btn_play=tk.Button(bottom_frame,text="▶ 再生")
btn_stop=tk.Button(bottom_frame,text="■ 停止")
btn_next=tk.Button(bottom_frame,text="次へ >>")
btn_prev.pack(side="left",padx=5)
btn_play.pack(side="left",padx=5)
btn_stop.pack(side="left",padx=5)
btn_next.pack(side="left",padx=5)

info_frame=tk.Frame(main_frame,width=250)
info_frame.pack(side="right",fill="y")
info_frame.pack_propagate(False)
pose_frame=tk.LabelFrame( info_frame, text="姿勢",font=("Arial,18"))
pose_frame.pack(fill="x", padx=5, pady=5)
roll_value=tk.Label(pose_frame,text="Roll : ---",font=("Arial,16"))
pitch_value=tk.Label(pose_frame, text="Pitch : ---",font=("Arial,16"))
yaw_value=tk.Label(pose_frame,text="Yaw : ---",font=("Arial,16"))
roll_value.pack(anchor="w")
pitch_value.pack(anchor="w")
yaw_value.pack(anchor="w")
pos_frame=tk.LabelFrame(info_frame,text="位置",font=("Arial,18"))
pos_frame.pack(fill="x",padx=5, pady=5)
x_value=tk.Label(pos_frame,text="X : ---",font=("Arial,16"))
y_value=tk.Label(pos_frame,text="Y : ---",font=("Arial,16"))
x_value.pack(anchor="w")
y_value.pack(anchor="w")
state_frame=tk.LabelFrame(info_frame,text="探索状態",font=("Arial,18"))
state_frame.pack(fill="x",padx=5,pady=5)
state_value=tk.Label(state_frame,text="---",height=2,font=("Arial,16"))
state_value.pack(fill="x")
goal_frame=tk.LabelFrame(info_frame,text="ゴール検出",font=("Arial,18"))
color_frame = tk.LabelFrame(info_frame, text="色検出",font=("Arial,18"))
color_frame.pack( fill="x",padx=5,pady=5)
color_value = tk.Label(color_frame, text="---",font=("Arial,16"))
color_value.pack(fill="x")
goal_frame.pack(fill="x",padx=5,pady=5)
goal_value=tk.Label(goal_frame, text="---", height=2,font=("Arial,16"))
goal_value.pack(fill="x")
comm_frame=tk.LabelFrame(info_frame,text="通信状況",font=("Arial,18"))
comm_frame.pack(fill="x",padx=5,pady=5)
comm_value=tk.Label(comm_frame,text="通信OK",font=("Arial,16"))

comm_value.pack()
map_area=tk.Canvas(main_frame,width=550, height=570,bg="white")
map_area.pack(side="left",fill="both",expand=True)
current_marker = None
last_px = None
last_py = None
CENTER_X = 325
CENTER_Y = 285
SCALE = 10
map_area.create_oval( CENTER_X-4, CENTER_Y-4, CENTER_X+4, CENTER_Y+4, fill="green")
map_area.create_text( CENTER_X, CENTER_Y-15, text="START")
last_px = None
last_py=None

def update_data():
    global current_marker
    global last_px
    global last_py
    data = get_latest_data()

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