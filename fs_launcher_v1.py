"""module providing the path function"""
import os
import csv
import threading
import time
from tkinter import StringVar
from tkinter import filedialog
import psutil
import customtkinter

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    """Main class containg the window"""

    def __init__(self):
        super().__init__()

        # configure window
        self.title("Fs Launcher")
        self.geometry(f"{1100}x{580}")
        self.found_p = [0, 0]
        self.is_paths = os.path.isfile("paths.csv")
        self.options = []
        self.thread_main = threading.Thread(target=self.draw_window)
        self.thread_main.start()
        self.fs_fg = 0
        self.st_fg = 0
        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=0)
        self.paths_frame = customtkinter.CTkFrame(
            self, width=self.winfo_width()-140, corner_radius=0)
        self.va_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.ot_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.on_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Fs Launcher", font=customtkinter.CTkFont(size=20,
                                                                               weight="bold"))
        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=[
                                                                           "Dark", "Light", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.steam_there = customtkinter.CTkButton(
            self.paths_frame, text="Search for Steam", command=self.search_steam, fg_color=self.st_fg)
        self.fs_there = customtkinter.CTkButton(
            self.paths_frame, text="Search for MSFS", command=self.search_fs, fg_color=self.fs_fg)
        self.launch = customtkinter.CTkButton(
            self.paths_frame, text="Launch!", command=self.launch_now)

        self.va_list = ["None"]
        self.ot_list = []
        self.on_list = ["None"]

        self.paths = 0

        self.va_radio_var = StringVar(value=self.va_list[0])
        self.on_radio_var = StringVar(value=self.on_list[0])
        self.ot_check_var = customtkinter.StringVar(value="on")

    def draw_window(self):
        """Draws the window and gathers the appropriate data to display"""
        self.is_paths = os.path.isfile("paths.csv")
        if not self.is_paths:
            self.fs_fg = "red3"
            self.st_fg = "red3"
            with open("paths.csv", "w", encoding="utf-8")as startfile:  # creates file
                startfile.close()

        else:
            with open("paths.csv", "r", encoding="utf-8")as checkfile:
                data = csv.reader(checkfile)
                data = list(data)

            for d in data:

                if d[0] == "steam.exe":
                    self.st_fg = "green4"
                    self.found_p[0] = 1

                elif self.found_p[0] != 1:
                    self.st_fg = "red3"
                if d[0] == "FlightSimulator.exe":

                    self.fs_fg = "green4"
                    self.found_p[1] = 1
                elif self.found_p[1] != 1:
                    self.fs_fg = "red3"

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets

        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.update()

        self.paths_frame.grid(row=0, column=1, sticky="nsew",
                              columnspan=3, padx=(20, 0))
        self.paths_frame.grid_columnconfigure(1, weight=1)
        self.paths_frame.grid_columnconfigure(2, weight=1)
        self.paths_frame.grid_columnconfigure(3, weight=1)

        self.va_frame.grid(row=1, column=1, sticky="nsew",
                           padx=(20, 10), pady=20)

        self.ot_frame.grid(row=1, column=2, sticky="nsew", padx=10, pady=20)

        self.on_frame.grid(row=1, column=3, sticky="nsew",
                           padx=(10, 20), pady=20)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu.grid(
            row=6, column=0, padx=20, pady=(10, 10))

        self.steam_there.grid(row=0, column=1, padx=10, pady=(20, 10))

        self.fs_there.grid(row=0, column=3, padx=10, pady=(20, 10))

        self.launch.grid(row=0, column=2, padx=10, pady=(20, 10))

        customtkinter.CTkButton(self.va_frame, text="Add Virtual Airline Apps",
                                command=lambda: self.add_app(1)).pack(pady=10)
        customtkinter.CTkButton(
            self.ot_frame, text="Add Other Apps", command=lambda: self.add_app(2)).pack(pady=10)
        customtkinter.CTkButton(self.on_frame, text="Add Traffic Apps",
                                command=lambda: self.add_app(3)).pack(pady=10)

        with open("paths.csv", "r", newline="", encoding="utf-8")as in_file:
            data = csv.reader(in_file)
            data = list(data)

            self.paths = data

            for path in self.paths:
                if path[1] == "1":

                    self.va_list.append(path)
                if path[1] == "2":
                    self.ot_list.append(path)
                if path[1] == "3":
                    self.on_list.append(path)

        for i, row in enumerate(self.va_list):
            if i == 0:

                customtkinter.CTkRadioButton(self.va_frame, text=row,
                                             variable=self.va_radio_var, value=row).pack(pady=5, anchor="center")
            else:
                customtkinter.CTkRadioButton(self.va_frame, text=row[0][:-4],
                                             variable=self.va_radio_var, value=row).pack(pady=5, anchor="center")

        for i, row in enumerate(self.on_list):
            if i == 0:
                customtkinter.CTkRadioButton(self.on_frame, text=row,
                                             variable=self.on_radio_var, value=row).pack(pady=5, anchor="center")
            else:
                customtkinter.CTkRadioButton(self.on_frame, text=row[0][:-4],
                                             variable=self.on_radio_var, value=row).pack(pady=5, anchor="center")

        for row in self.ot_list:

            switch_var = customtkinter.StringVar(value="off")
            customtkinter.CTkSwitch(self.ot_frame, text=row[0][:-4], command=lambda opt=row: self.toggle_option(opt),
                                    variable=switch_var, onvalue="on", offvalue="off").pack()

    def launch_now(self):
        """runs all programs"""
        to_launch = []

        to_launch = self.options
        if self.va_radio_var.get() != "None":
            to_launch.append([item.strip(" '")
                              for item in self.va_radio_var.get()[1:-1].split(',')])
        if self.on_radio_var.get() != "None":
            to_launch.append([item.strip(" '")
                              for item in self.on_radio_var.get()[1:-1].split(',')])
        for i, app_to_run in enumerate(self.paths):
            if app_to_run[1] == "0" and i != 0 and self.found_p[0] == 1:
                to_launch.append(app_to_run)

        for app_run in to_launch:
            print("launchng", app_run)
            os.startfile(app_run[2])
        if self.found_p[0] == 1:
            print("using steam")
            self.wait_steam()
        self.destroy()
        print("Waiting 10s")
        time.sleep(10)

        print("starting msfs")
        os.startfile(self.paths[0][2])

    def wait_steam(self):
        """waits for steam to run"""
        steam_running = False
        while not steam_running:
            steam_running = self.check_running("steam.exe")
            print(steam_running)
        print("steam running")

    def check_running(self, exe):  # check is steam/ other apps are running
        """returns true if the given app is running on the computer"""
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if process.info['name'] == exe:
                return True
        return False

    def add_app(self, pos):
        """adds an app to the window/ csv file"""
        filepath = filedialog.askopenfilename(initialdir="",
                                              title="Select exe File",
                                              filetypes=[("Executable files", "*.exe"),
                                                         ("Batch files", "*.bat"),
                                                         ("All Types", "*.*")])

        with open("paths.csv", "r", encoding="utf-8")as check_file:
            data = csv.reader(check_file)
            data = list(data)

        already = False
        for datum in data:
            if datum[2] == filepath:
                already = True
                break

        if not already:
            print("Not already selected")
            data.append([filepath.split("/")[-1], pos, filepath])
            print(data)
            file_path = os.path.abspath("paths.csv")
            with open(file_path, "w", newline="", encoding="utf-8")as out_file:
                print("added", data)
                writer = csv.writer(out_file)
                writer.writerows(data)
            with open("data_dump.txt", "a", encoding="utf-8")as dump_file:
                dump_file.write(str(data))

            self.draw_window()

    def toggle_option(self, option):  # private??
        """toggles the option given between on and off"""
        if option in self.options:
            self.options.remove(option)
        else:
            self.options.append(option)

    def search_steam(self):
        """looks for the steam.exe file on the computer"""
        exp_loc_steam = "C:/Program Files (x86)/Steam/steam.exe"

        in_expected_loc_steam = os.path.isfile(exp_loc_steam)
        if not in_expected_loc_steam:

            exp_loc_steam = filedialog.askopenfilename(initialdir="C:/Program Files (x86)/Steam",
                                                       title="Select Steam.exe",
                                                       filetypes=(("Executable files", "steam.exe"),))

        if exp_loc_steam[-9:] == "steam.exe":
            self.steam_there.configure(fg_color="green4")

            with open("paths.csv", "a", newline="", encoding="utf-8")as out_file:
                writer = csv.writer(out_file)
                writer.writerow(
                    [exp_loc_steam.split("/")[-1], 0, exp_loc_steam])

            exp_loc_fs = f"{exp_loc_steam[:-10]}/steamapps/common/MicrosoftFlightSimulator/FlightSimulator.exe"
            if os.path.isfile(exp_loc_fs):
                self.fs_there.configure(fg_color="green4")

                with open("paths.csv", "a", newline="", encoding="utf-8")as out_file:
                    writer = csv.writer(out_file)
                    writer.writerow([exp_loc_fs.split("/")[-1], 0, exp_loc_fs])

    def search_fs(self):
        """searches for flightsimulator.exe"""
        exp_loc_fs = "C:/Program Files (x86)/Steam/steamapps/common/MicrosoftFlightSimulator/FlightSimulator.exe"
        if not os.path.isfile(exp_loc_fs):
            exp_loc_fs = filedialog.askopenfilename(initialdir=exp_loc_fs,
                                                    title="Select FlightSimulator.exe",
                                                    filetypes=(("Executable files", "*.exe"),))
        self.fs_there.configure(fg_color="green4")
        with open("paths.csv", "a", newline="", encoding="utf-8")as out_file:
            writer = csv.writer(out_file)
            writer.writerow([exp_loc_fs.split("/")[-1], 0, exp_loc_fs])

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """sets the given apperance setting to the currnt"""
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":

    app = App()

    app.mainloop()
