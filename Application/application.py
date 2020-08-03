from statistic import Statistic
import tkinter as tk
from functools import partial


class Application(tk.Frame):
    # Frames and channel
    right_frame = None
    left_frame = None
    channel = None

    # Light1 controls
    light1_on_id = bytes([67])
    light1_off_id = bytes([66])
    light1_switch: bool = False
    light1_button = None
    light1_stat = None
    light1_label = None
    light1_str_var = None

    # Light2 controls
    light2_on_id = bytes([65])
    light2_off_id = bytes([64])
    light2_switch: bool = False
    light2_button = None
    light2_stat = None
    light2_label = None
    light2_str_var = None

    # Other controls
    manual_mode_id = bytes([1])
    auto_mode_id = bytes([0])
    mode_switch: bool = True
    mode_button = None
    set_timeout_button = None
    enable_timeout_button = None
    enable_timeout_switch = True

    # Automatic Timeout variable
    time_range_start_hour = 23
    time_range_start_min = 00
    time_range_end_hour = 2
    time_range_end_min = 59

    start_hour_entry = None
    end_hour_entry = None

    def __init__(self, master=None, channel=None):
        super().__init__(master)
        self.master = master
        self.channel = channel
        self.pack()
        self.light1_stat = Statistic()
        self.light2_stat = Statistic()
        self.create_widgets()

    def create_widgets(self):
        # Left and Right frame
        self.left_frame = tk.Frame(self)
        self.left_frame.grid(row=0, column=0)
        self.right_frame = tk.Frame(self)
        self.right_frame.grid(row=0, column=1)

        # Quit button
        quit_button = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        quit_button.grid(row=1, column=0, columnspan=2)

        # --------------- FRAME RIGHT --------------------#
        # Light 1 and Light 2 button and label
        self.light1_button = tk.Button(self.left_frame, text="Light 1\n off")
        self.light1_button['command'] = partial(self.light_button_handler, 1)
        self.light1_str_var = tk.StringVar()
        self.light1_label = tk.Label(self.left_frame, textvariable=self.light1_str_var)
        self.light1_str_var.set(self.get_stat_string(self.light1_stat))

        self.light2_button = tk.Button(self.left_frame, text="Light 2\n off")
        self.light2_button['command'] = partial(self.light_button_handler, 2)
        self.light2_str_var = tk.StringVar()
        self.light2_label = tk.Label(self.left_frame, textvariable=self.light2_str_var)
        self.light2_str_var.set(self.get_stat_string(self.light2_stat))

        # Mode button
        self.mode_button = tk.Button(self.left_frame, text="Automatic mode", command=self.mode_button_handler)

        # Element setup
        self.mode_button.grid(row=0, column=0, columnspan=2)
        self.light1_button.grid(row=1, column=0)
        self.light1_label.grid(row=2, column=0)
        self.light2_button.grid(row=1, column=1)
        self.light2_label.grid(row=2, column=1)

        self.light_handler(1, False)
        self.light_handler(2, False)
        self.mode_handler(True)

        # --------------- FRAME LEFT --------------------#
        # Label setup
        tk.Label(self.right_frame, text="Automatic timeout set:").grid(row=0, column=0, columnspan=4)
        tk.Label(self.right_frame, text="From").grid(row=1)
        tk.Label(self.right_frame, text="To").grid(row=2)
        tk.Label(self.right_frame, text=":").grid(row=1, column=2)
        tk.Label(self.right_frame, text=":").grid(row=2, column=2)
        tk.Label(self.right_frame, text="00").grid(row=1, column=3)
        tk.Label(self.right_frame, text="00").grid(row=2, column=3)

        # Timeout entry
        self.start_hour_entry = tk.Entry(self.right_frame, width=3)
        self.start_hour_entry.grid(row=1, column=1)
        self.start_hour_entry.insert(0, str(self.time_range_start_hour))
        self.end_hour_entry = tk.Entry(self.right_frame, width=3)
        self.end_hour_entry.grid(row=2, column=1)
        self.end_hour_entry.insert(0, str(self.time_range_end_hour))

        self.set_timeout_button = tk.Button(self.right_frame, text="Set")
        self.set_timeout_button['command'] = partial(self.set_timeout_handler, self.start_hour_entry, self.end_hour_entry)
        self.set_timeout_button.grid(row=3, column=0, columnspan=4)

        self.enable_timeout_button = tk.Button(self.right_frame, text="Enabled", command=self.enable_timeout_handler)
        self.enable_timeout_button.grid(row=4, column=0, columnspan=4)

    def set_frame_left(self, state: str):
        if state == 'disable':
            self.light1_button.configure(state=state)
            self.light2_button.configure(state=state)
            self.mode_button.configure(state=state)
        if state == 'active':
            self.mode_button.configure(state=state)
            self.mode_handler(self.mode_switch)

    @staticmethod
    def get_stat_string(light_stat: Statistic):
        ret = list()
        ret.append("Usage of the light:\n ")
        ret.append(str(int(light_stat.get_time() / 60)))
        ret.append(" min ")
        ret.append(str(light_stat.get_time() % 60))
        ret.append(" sec\n Total time activation:\n ")
        ret.append(str(int(light_stat.get_time_from_activation() / 60)))
        ret.append(" min ")
        ret.append(str(light_stat.get_time_from_activation() % 60))
        ret.append(" sec")
        return ''.join(ret)

    def light_button_handler(self, light_id):
        if light_id == 1:
            self.light_handler(light_id, not self.light1_switch)
        if light_id == 2:
            self.light_handler(light_id, not self.light2_switch)

    def mode_button_handler(self):
        self.mode_handler(not self.mode_switch)

    def light_handler(self, light_id: int, light_state: bool):
        light_text = list()
        light_text.append("Light ")
        light_text.append(str(light_id))
        light_text.append("\n")
        light_text.append("on" if light_state else "off")
        light_text = ''.join(light_text)

        if light_id == 1:
            self.light1_switch = light_state
            self.light1_button.config(text=light_text)
            self.channel.write(self.light1_on_id if light_state else self.light1_off_id)
            self.light1_stat.start_time() if light_state else self.light1_stat.stop_time()

        if light_id == 2:
            self.light2_switch = light_state
            self.light2_button.config(text=light_text)
            self.channel.write(self.light2_on_id if light_state else self.light2_off_id)
            self.light2_stat.start_time() if light_state else self.light2_stat.stop_time()

    def mode_handler(self, mode_state: bool):
        self.mode_switch = mode_state
        if self.mode_switch:
            self.mode_button.config(text="Automatic mode")
            self.channel.write(self.auto_mode_id)
            state = 'disable'
        else:
            self.mode_button.config(text="Manual mode")
            self.channel.write(self.manual_mode_id)
            state = 'active'

        self.light1_button.configure(state=state)
        self.light2_button.configure(state=state)

    def set_timeout_handler(self, start_hour: tk.Entry, end_hour: tk.Entry):
        start = int(start_hour.get())
        end = int(end_hour.get())
        if 0 <= start <= 24 and 0 <= end <= 24:
            self.time_range_start_hour = start
            self.time_range_end_hour = end

    def enable_timeout_handler(self):
        self.enable_timeout_switch = not self.enable_timeout_switch
        if self.enable_timeout_switch:
            self.set_timeout_button.configure(state='active')
            self.enable_timeout_button.configure(text='Enabled')
            self.start_hour_entry.delete(0, 'end')
            self.end_hour_entry.delete(0, 'end')
            self.start_hour_entry.insert(0, str(self.time_range_start_hour))
            self.end_hour_entry.insert(0, str(self.time_range_end_hour))
        else:
            self.set_timeout_button.configure(state='disable')
            self.enable_timeout_button.configure(text='Disabled')
            self.start_hour_entry.delete(0, 'end')
            self.end_hour_entry.delete(0, 'end')
            self.start_hour_entry.insert(0, '0')
            self.end_hour_entry.insert(0, '0')
