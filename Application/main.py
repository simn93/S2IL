from application import Application
import tkinter as tk
from serial import  serial_for_url #Serial, 
import time


def check_timeout():
    curr_time = time.localtime()
    curr_hour = curr_time.tm_hour

    if app.time_range_start_hour < app.time_range_end_hour:
        in_interval = app.time_range_start_hour <= curr_hour < app.time_range_end_hour
    else:
        in_interval = not (app.time_range_start_hour > curr_hour >= app.time_range_end_hour)

    global timeout_mode

    if in_interval and not timeout_mode and app.enable_timeout_switch:
        app.mode_handler(False)
        app.light_handler(1, False)
        app.light_handler(2, False)
        app.set_frame_left('disable')
        timeout_mode = True

    if timeout_mode and (not in_interval or not app.enable_timeout_switch):
        app.set_frame_left('active')
        timeout_mode = False

    app.after(1000, check_timeout)
    app.update_idletasks()


def serial_read():
    b = channel.read()
    bi = int.from_bytes(b'\x00' + b, "big")
    # print(bi)
    if b != b'':
        if bi == 64:
            if app.light2_switch:
                app.light_handler(2, False)
        if bi == 65:
            if not app.light2_switch:
                app.light_handler(2, True)
        if bi == 66:
            if app.light1_switch:
                app.light_handler(1, False)
        if bi == 67:
            if not app.light1_switch:
                app.light_handler(1, True)

    app.after(100, serial_read)
    app.update_idletasks()


def update_label_loop():
    app.light1_str_var.set(app.get_stat_string(app.light1_stat))
    app.light2_str_var.set(app.get_stat_string(app.light2_stat))

    app.after(500, update_label_loop)
    app.update_idletasks()


# channel = Serial('COM3', 9600, timeout=1)
channel = serial_for_url('loop://', 9600, timeout=1)
timeout_mode = False

root = tk.Tk()
root.title('Sil')
app = Application(master=root, channel=channel)
app.after(1000, serial_read)
app.after(1000, check_timeout)
app.after(1000, update_label_loop)
app.mainloop()
