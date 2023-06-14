from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pygame
import customtkinter
import os
import time
from mutagen.mp3 import MP3
import threading



class App:
    def __init__(self, root) -> None:
        
        self.root = root
        self.root.title('BluEye Player')
        self.root.resizable(False,False)
        self.root.geometry('1040x490')
        self.root._set_appearance_mode('dark')
        pygame.init()
        pygame.mixer.init()
        self.trackframeTitle = StringVar()
        self.trackframeTitle.set('Song Track')

        self.track = StringVar()
        self.status = StringVar()

        self.slider_var = DoubleVar()
        self.slider_var.set(100)

        self.btnframeTitle = StringVar()
        self.btnframeTitle.set("Control")

        self.switch_var = customtkinter.StringVar(value="off")
        self.root.iconbitmap(r'./logo-icon.ico')

        
        about_us = customtkinter.CTkLabel(master=self.root, text='© Coded and Designed by Mahmoud Dwidar (github.com/mahmouddwidar)', text_color='gray').place(x=0, y=468)

        # Song Track and status Frame
        label_font = customtkinter.CTkFont(family='roman', size=22, slant='roman', underline=False)
        self.trackframe = customtkinter.CTkFrame(self.root, border_width=2).grid(row=0, column=0, padx=10, pady=10, columnspan=4, sticky='ew')
        trackframeTitle = customtkinter.CTkEntry(master=self.trackframe, textvariable=self.trackframeTitle, fg_color='transparent', justify='center', font=('arial', 24, 'italic',), state='readonly').place(x=260, y=10)
        songtrack = customtkinter.CTkEntry(master=self.trackframe, textvariable=self.track, fg_color='transparent', font=('arial', 24, 'bold'), justify='center', width=640, height=50,text_color='white', bg_color='#343434', state='readonly').place(x=20, y=90,)
        trackstatus = customtkinter.CTkEntry(master=self.trackframe, textvariable=self.status, fg_color='transparent', justify='center', font=('arial', 24, 'bold'), width=140, height=20,text_color='white', bg_color='#343434', state='readonly').place(x=255, y=160)             
        self.lengthlabel = ttk.Label(self.trackframe, text='Total Time - --:--',font=('times new roman', 11, 'bold'), background='#2a2929', foreground='white')
        self.lengthlabel.place(x=420, y=170)  
        self.currenttimelabel = ttk.Label(self.trackframe, text='Current Time - --:--', font=('times new roman', 11, 'bold'), background='#2a2929', foreground='white')
        self.currenttimelabel.place(x=90, y=170)

        # Control Panel Frame
        self.btnframe = customtkinter.CTkFrame(self.root, border_width=2).grid(row=1, column=0, padx=10, pady=0,sticky='sew', columnspan=4)
        btnframeTitle = customtkinter.CTkEntry(master=self.btnframe, textvariable=self.btnframeTitle, fg_color='transparent', justify='center', font=('arial', 24, 'italic',), state='readonly').place(x=260, y=220)
        self.playbtn = customtkinter.CTkButton(master=self.btnframe, text='Play', command=self.playsong).grid(row=1, column=0, padx=20, pady=10)
        self.playbtn = customtkinter.CTkButton(master=self.btnframe, text='Pause', command=self.pausesong).grid(row=1, column=1, padx=10, pady=10)
        self.playbtn = customtkinter.CTkButton(master=self.btnframe, text='Resume', command=self.resume).grid(row=1, column=2, padx=10, pady=10)
        self.playbtn = customtkinter.CTkButton(master=self.btnframe, text='Stop', command=self.stop).grid(row=1, column=3, padx=20, pady=10)
        vol_label = customtkinter.CTkLabel(master=self.btnframe, text='Volume', font=('times new roman', 15, 'bold'), width=140,bg_color='#2a2929',).place(x=520, y=340)
        self.volbtn = customtkinter.CTkSlider(master=self.btnframe, from_=0, to=100, command=self.set_vol, width=140, border_color='transparent', border_width=1,bg_color='#343434',variable=self.slider_var).place(x=520, y=370)
        self.switchbtn = customtkinter.CTkSwitch(master=self.btnframe, text='Loop',font=('times new roman', 15, 'bold'), bg_color='#2a2929', command=self.loop, variable=self.switch_var, onvalue="on", offvalue="off").place(x=400, y=367)
        

        # Song Frame
        self.songsframe = customtkinter.CTkScrollableFrame(master=self.root, label_text='Songs', label_font=('arial', 15, 'bold'), border_width=2,)
        self.songsframe.grid(row=0, column=5, padx=10, pady=10, sticky='ns', columnspan=2, rowspan=2)

        self.playlist = Listbox(self.songsframe,  selectbackground='#005ce6', selectmode=SINGLE, font=('arial', 12, 'bold'), bg='#333333', bd=5, relief=GROOVE, borderwidth=0, highlightthickness=0, height=100,)
        self.playlist.grid(row=0, column=0, sticky='nsew')
        self.playlist.pack(fill=BOTH, expand=True)

        addbtn = customtkinter.CTkButton(master=self.root, text='Add Songs', command=self.add_music,).grid(row=2, column=5, padx=20, pady=10, columnspan=1, rowspan=2, sticky='ew')
        removebtn = customtkinter.CTkButton(master=self.root, text='Remove Song', command=self.remove_song,).grid(row=2, column=6, padx=20, pady=10, rowspan=2, sticky='ew',)
        
    
    def playsong(self):
        self.track.set(self.playlist.get(ACTIVE))
        self.status.set('- Playing')
        play_song = self.playlist.get(ACTIVE)
        pygame.mixer.music.load(play_song)
        pygame.mixer.music.play()
        self.show_details(play_song)

        # Trying to play the other songs Auto.
        # global song_index
        # song_index = list(self.playlist.get(0, 'end')).index(self.playlist.get(ACTIVE))

        # global songs_list
        # songs_list = list(self.playlist.get(song_index, 'end'))


    def pausesong(self):
        self.status.set('- Paused')
        pygame.mixer.music.pause()

    def resume(self):
        self.status.set('- Playing')
        pygame.mixer.music.unpause()

    def stop(self):
        self.status.set('- Stopped')
        pygame.mixer.music.stop()

    def add_music(self):
        path = filedialog.askdirectory()
        if path:
            os.chdir(path)
            songs = os.listdir(path)
            for song in songs:
                self.playlist.insert(END, song)

    def remove_song(self):
        sel_song = self.playlist.curselection()
        sel_song = int(sel_song[0])
        self.playlist.delete(sel_song)

    def set_vol(self, val):
        volume = float(val) / 100
        pygame.mixer.music.set_volume(volume)

    def loop(self):
        if self.switch_var.get() == 'on':
            self.track.set(self.playlist.get(ACTIVE))
            self.status.set('- On Loop')
            play_song = self.playlist.get(ACTIVE)
            pygame.mixer.music.load(play_song)
            pygame.mixer.music.play(-1)
            self.show_details(play_song)
        elif self.switch_var.get() == 'off':
            self.track.set(self.playlist.get(ACTIVE))
            self.status.set('- Playing')
            play_song = self.playlist.get(ACTIVE)
            pygame.mixer.music.load(play_song)
            pygame.mixer.music.play() # Strat the song from the beginning
            self.show_details(play_song)


    def show_details(self, play_song):
        file_data = os.path.splitext(play_song)
        if file_data[1] == '.mp3':
            audio = MP3(play_song)
            total_length = audio.info.length
        else:
            a = pygame.mixer.Sound(play_song)
            total_length = a.get_length()
        mins, secs = divmod(total_length, 60)
        mins = round(mins)
        secs = round(secs)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        self.lengthlabel['text'] = 'Total Time' + ' - ' + timeformat
        t1 = threading.Thread(target=self.start_count, args=(total_length,), daemon=True)
        t1.run()
        
        


    def start_count(self, t):
        paused = False
        current_time = 0

        def update_time():
            nonlocal current_time
            if current_time <= t and pygame.mixer.music.get_busy():
                if not paused:
                    mins, secs = divmod(current_time, 60)
                    mins = round(mins)
                    secs = round(secs)
                    timeformat = '{:02d}:{:02d}'.format(mins, secs)
                    self.currenttimelabel.config(text='Current Time' + ' - ' + timeformat)
                    current_time += 1
            # Schedule the next update after 1 second (1000 milliseconds)
            self.currenttimelabel.after(1000, update_time)

        update_time()





if __name__ == '__main__':  
    root = customtkinter.CTk()
    App(root)
    root.mainloop()