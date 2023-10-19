import os,csv,threading,time,psutil
from tkinter import *
from tkinter import filedialog
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Fs Launcher")
        self.geometry(f"{1100}x{580}")
        self.foundP = [0,0]
        self.isPaths = os.path.isfile("paths.csv")
        self.options = []
        self.thread_main = threading.Thread(target=self.draw_window)
        self.thread_main.start()
        

    def draw_window(self):
        self.isPaths = os.path.isfile("paths.csv")
        if not self.isPaths:
            self.FsFg = "red3"
            self.StFg = "red3"
            with open("paths.csv","w")as startfile:
                pass
        else:
            with open("paths.csv","r")as checkfile:
                data = csv.reader(checkfile)
                data = list(data)
            
            for d in data:
                
                if d[0] == "steam.exe":
                    self.StFg = "green4"
                    self.foundP[0] = 1
                    
                elif self.foundP[0] != 1:
                    self.StFg = "red3"
                if d[0] == "FlightSimulator.exe":
                    
                    self.FsFg = "green4"
                    self.foundP[1] = 1
                elif self.foundP[1] != 1:
                    self.FsFg = "red3"

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.update()
        self.paths_frame = customtkinter.CTkFrame(self, width=self.winfo_width()-140, corner_radius=0)
        self.paths_frame.grid(row=0,column=1,sticky="nsew",columnspan=3,padx=(20,0))
        self.paths_frame.grid_columnconfigure(1,weight=1)
        self.paths_frame.grid_columnconfigure(2,weight=1)
        self.paths_frame.grid_columnconfigure(3,weight=1)


        self.va_frame = customtkinter.CTkFrame(self,corner_radius=10)
        self.va_frame.grid(row=1,column=1,sticky="nsew",padx=(20,10),pady=20)
        self.ot_frame = customtkinter.CTkFrame(self,corner_radius=10)
        self.ot_frame.grid(row=1,column=2,sticky="nsew",padx=10,pady=20)
        self.on_frame = customtkinter.CTkFrame(self,corner_radius=10)
        self.on_frame.grid(row=1,column=3,sticky="nsew",padx=(10,20),pady=20)

        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2,weight=1)
        self.grid_columnconfigure(3,weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Fs Launcher", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

     

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark","Light", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.steam_there = customtkinter.CTkButton(self.paths_frame,text="Search for Steam",command=self.searchSteam,fg_color=self.StFg)
        self.steam_there.grid(row=0,column=1,padx=10,pady=(20,10))

        self.FS_there = customtkinter.CTkButton(self.paths_frame,text="Search for MSFS",command=self.searchFS,fg_color=self.FsFg)
        self.FS_there.grid(row=0,column=3,padx=10,pady=(20,10))

        self.Launch = customtkinter.CTkButton(self.paths_frame,text="Launch!",command=self.LaunchNow)
        self.Launch.grid(row=0, column=2,padx=10,pady=(20,10))

        customtkinter.CTkButton(self.va_frame,text="Add Virtual Airline Apps",command= lambda:self.add_app(1)).pack(pady=10)
        customtkinter.CTkButton(self.ot_frame,text="Add Other Apps",command= lambda:self.add_app(2)).pack(pady=10)
        customtkinter.CTkButton(self.on_frame,text="Add Traffic Apps",command= lambda:self.add_app(3)).pack(pady=10)

        with open("paths.csv","r", newline="")as inFile:
            data = csv.reader(inFile)
            data = list(data)
                    
            self.VaList = ["None"]
            self.otLsit= []
            self.onList = ["None"]
        
            self.paths = data
            
            for path in self.paths:
                if path[1] == "1":
                    
                    self.VaList.append(path)
                if path[1] == "2":
                    self.otLsit.append(path)
                if path[1] == "3":
                    self.onList.append(path)

        
        self.va_radio_var = StringVar(value=self.VaList[0])
        for i,row in enumerate(self.VaList):
            if i == 0:

                customtkinter.CTkRadioButton(self.va_frame,text=row,
                                         variable=self.va_radio_var,value=row).pack(pady=5,anchor="center")
            else:
                customtkinter.CTkRadioButton(self.va_frame,text=row[0][:-4],
                                         variable=self.va_radio_var,value=row).pack(pady=5,anchor="center")
            
    
        self.on_radio_var = StringVar(value=self.onList[0])
        for i,row in enumerate(self.onList):
            if i ==0:
                customtkinter.CTkRadioButton(self.on_frame,text=row,
                                            variable=self.on_radio_var,value=row).pack(pady=5,anchor="center")
            else:
                customtkinter.CTkRadioButton(self.on_frame,text=row[0][:-4],
                                            variable=self.on_radio_var,value=row).pack(pady=5,anchor="center")
        
     
        self.ot_check_var = customtkinter.StringVar(value="on")
        for row in self.otLsit:
            

            switch_var = customtkinter.StringVar(value="off")
            customtkinter.CTkSwitch(self.ot_frame,text=row[0][:-4],command=lambda opt = row: self.toggle_option(opt),
                                             variable=switch_var,onvalue="on",offvalue="off").pack()


    def LaunchNow(self):
        toLaunch = []
        
        toLaunch = self.options
        if self.va_radio_var.get() != "None":
            toLaunch.append([item.strip(" '") for item in self.va_radio_var.get()[1:-1].split(',')])
        if self.on_radio_var.get() != "None":
            toLaunch.append([item.strip(" '") for item in self.on_radio_var.get()[1:-1].split(',')])
        for i,app in enumerate(self.paths):
            if app[1] == "0" and i != 0 and self.foundP[0] == 1:
                toLaunch.append(app)

        
        for app in toLaunch:
            print("launchng",app)
            os.startfile(app[2])
        if self.foundP[0] == 1:
            print("using steam")
            self.waitSteam()
        self.destroy()
        print("Waiting 10s")
        time.sleep(10)
        
        print("starting msfs")
        os.startfile(self.paths[0][2])

    def waitSteam(self):
        steamRunning = False
        while not steamRunning:
            steamRunning = self.CheckRunning("steam.exe")
            print(steamRunning)
        print("steam running")


    def CheckRunning(self,exe): # check is steam/ other apps are running
        
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if process.info['name'] == exe:
                return True
        return False
        

    def add_app(self,pos):
        filepath = filedialog.askopenfilename(initialdir="",
                                        title="Select exe File",
                                        filetypes=[("Executable files", "*.exe"),
                                                   ("Batch files", "*.bat"),
                                                   ("All Types","*.*")])
        
        with open("paths.csv","r")as CheckFile:
            data  = csv.reader(CheckFile)
            data = list(data)

        
        already = False
        for datum in data:
            if datum[2] == filepath:
                already = True
                break
        

        if not already:
            print("Not already selected")
            data.append([filepath.split("/")[-1],pos,filepath])
            print(data)
            file_path = os.path.abspath("paths.csv")
            with open(file_path,"w",newline="")as outFile:
                print("added",data)
                writer = csv.writer(outFile)
                writer.writerows(data)
            with open("data_dump.txt","a")as dumpFile:
                dumpFile.write(str(data))
                
            
            self.draw_window()

    def toggle_option(self,option):
        if option in self.options:
            self.options.remove(option)
        else:
            self.options.append(option)
    


    def searchSteam(self):
        expLocSteam = "C:/Program Files (x86)/Steam/steam.exe"
        
        inExpectedLocSteam = os.path.isfile(expLocSteam)
        if not inExpectedLocSteam:
        
            expLocSteam = filedialog.askopenfilename(initialdir="C:/Program Files (x86)/Steam",
                                        title="Select Steam.exe",
                                        filetypes=(("Executable files", "steam.exe"),))
        


        if expLocSteam[-9:] == "steam.exe":
            self.steam_there.configure(fg_color="green4")
            
            with open("paths.csv","a",newline="")as outFile:
                 writer = csv.writer(outFile)
                 writer.writerow([expLocSteam.split("/")[-1],0,expLocSteam])


            expLocFs = f"{expLocSteam[:-10]}/steamapps/common/MicrosoftFlightSimulator/FlightSimulator.exe"
            if os.path.isfile(expLocFs):
                self.FS_there.configure(fg_color="green4")

                with open("paths.csv","a",newline="")as outFile:
                 writer = csv.writer(outFile)
                 writer.writerow([expLocFs.split("/")[-1],0,expLocFs])
                


    def searchFS(self):
        expLocFs = "C:/Program Files (x86)/Steam/steamapps/common/MicrosoftFlightSimulator/FlightSimulator.exe"
        if not os.path.isfile(expLocFs):
            expLocFs = filedialog.askopenfilename(initialdir=expLocFs,
                                        title="Select FlightSimulator.exe",
                                        filetypes=(("Executable files", "*.exe"),))
        self.FS_there.configure(fg_color="green4")
        with open("paths.csv","a",newline="")as outFile:
                 writer = csv.writer(outFile)
                 writer.writerow([expLocFs.split("/")[-1],0,expLocFs])




    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)






if __name__ == "__main__":
    
    app = App()
    
    app.mainloop()