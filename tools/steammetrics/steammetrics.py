# IMPORTS
# from steam_key import *
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from io import BytesIO
import pandas as pd
from pandastable import Table, TableModel, config
import requests
import pickle as pkl
import json
import warnings

# CONSTS
COLOR_1 = '#171A21'
COLOR_2 = '#66C0F4'
COLOR_3 = '#1B2838'
COLOR_4 = '#2A475E'
COLOR_5 = '#C7D5E0'

FONT_1 = ('Impact', 30, 'bold')
FONT_2 = ('impact', 15, 'bold')
FONT_3 = ('Impact', 10)
FONT_4 = ('Impact', 4)

class Tool():
    def __init__(self):
        # DATA
        self.user_info = pd.DataFrame()
        self.user_lib = pd.DataFrame()
        self.user_lib_copy = pd.DataFrame()
        self.query_res = pd.DataFrame()
        self.PARAMETERS = {
            'key': None,
            'steamid': None,
            'format': 'json'
        }

        # GUI
        self.tool_enable = {
            'user_built': False,
            'library_built': False
        }
        self.main_window = Tk()
        self.main_window.title('Steam Metrics')
        self.main_window.config(bd=5, bg=COLOR_1, height=800, width=1200)
        self.main_window.grid()
        self.main_window.grid_propagate(False)

        self.title_label = Label(self.main_window, bg=COLOR_1, bd=1, font=FONT_1, fg=COLOR_5, height=1, width=25, text='Steam Metrics', justify='center')
        self.title_label.grid(row=0, column=0, rowspan=1, columnspan=1)

        self.gui_user_area()
        self.gui_tool_area()
        self.gui_query_area()

        return


    ''' V DATA FUNCTIONS V '''
    def update_params(self):
        if(len(self.uid_entry.get()) != 17):
            self.ubutton_label.config(text='Enter a 17-Digit User ID.')
            return
        try:
            self.PARAMETERS['key'] = self.ukey_entry.get()
            self.PARAMETERS['steamid'] = self.uid_entry.get()
            self.ubutton_label.config(text='Success!')
        except Exception as e:
            print(f'Exception: {e}')
            self.ubutton_label.config(text='Check input.')
        return


    # USER INFO
    def fetch_user_info(self):
        try:
            self.update_params()
            temp_parameters = {
                'key': self.PARAMETERS['key'],
                'steamids': self.PARAMETERS['steamid'],
                'format': 'json'
            }
            response = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/', params=temp_parameters)
            response_str = response.content.decode('utf-8')
            data = json.loads(response_str)
            info = data['response']['players']
            self.user_info = pd.DataFrame(info)
            self.save_user_info()

            upfp_image_response = requests.get(self.user_info['avatarmedium'][0])
            image_data = BytesIO(upfp_image_response.content)
            self.upfp_image = Image.open(image_data)
            self.upfp_image = self.upfp_image.resize((50, 50))
            self.upfp_image_tk = ImageTk.PhotoImage(self.upfp_image)
            self.upfp.config(image=self.upfp_image_tk)

            self.uname.config(text=self.user_info['personaname'][0])
            self.uurl.config(text=self.user_info['profileurl'][0])
            match self.user_info['personastate'][0]:
                case 0:
                    self.ustatus.config(text='Offline')
                case 1:
                    self.ustatus.config(text='Online')
                case 2:
                    self.ustatus.config(text='Busy')
                case 3:
                    self.ustatus.config(text='Away')
                case 4:
                    self.ustatus.config(text='Snooze')
                case 5:
                    self.ustatus.config(text='Looking to Trade')
                case 6:
                    self.ustatus.config(text='Looking to Play')
                case _:
                    self.ustatus.config(text='None')

            self.tool_enable['user_built'] = True
            print(response)
            self.ubutton_label.config(text='Success!')
        except Exception as e:
            print(f'Exception: {e} {response}')
            self.ubutton_label.config(text='Fetch error.')
        return
        

    def save_user_info(self):
        try:
            with open('user_info.pkl', 'wb') as f:
                pkl.dump(self.user_info, f)
            self.ubutton_label.config(text='Success!')
        except Exception as e:
            print(f'Exception: {e}')
            self.ubutton_label.config(text='Save error.')


    def load_user_info(self):
        try:
            with open('user_info.pkl', 'rb') as f:
                self.user_info = pkl.load(f)

            upfp_image_response = requests.get(self.user_info['avatarmedium'][0])
            image_data = BytesIO(upfp_image_response.content)
            self.upfp_image = Image.open(image_data)
            self.upfp_image = self.upfp_image.resize((50, 50))
            self.upfp_image_tk = ImageTk.PhotoImage(self.upfp_image)
            self.upfp.config(image=self.upfp_image_tk)

            self.uname.config(text=self.user_info['personaname'][0])
            self.uurl.config(text=self.user_info['profileurl'][0])
            self.ustatus.config(text='Unknown')

            self.tool_enable['user_built'] = True
            self.ubutton_label.config(text='Success!')
        except Exception as e:
            print(f'Exception: {e}')
            self.ubutton_label.config(text='Load error.')


    # USER LIBRARY
    def build_user_lib(self):
        try:
            self.update_params()
            temp_parameters = self.PARAMETERS.copy()
            temp_parameters['include_played_free_games'], temp_parameters['include_appinfo'] = True, True
            response = requests.get('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/', params=temp_parameters)
            response_str = response.content.decode('utf-8')
            data = json.loads(response_str)
            games = data['response']['games']
            # TODO: IMAGES FOR GAMES
            self.user_lib = pd.DataFrame(games)
            self.build_lib_copy()
            self.save_user_lib()

            self.tool_enable['library_built'] = True
            print(response)
            self.ubutton_label.config(text='Success!')
        except Exception as e:
            print(f'Exception: {e} {response}')
            self.ubutton_label.config(text='Build error.')
        return

    def build_lib_copy(self):
        self.user_lib_copy['ID'] = self.user_lib['appid']
        self.user_lib_copy['Name'] = self.user_lib['name']
        self.user_lib_copy['Total Playtime (hours)'] = self.user_lib['playtime_forever'].apply(lambda x: x/60)
        return

    def save_user_lib(self):
        try:
            with open ('user_lib.pkl', 'wb') as f:
                pkl.dump(self.user_lib, f)
            self.ubutton_label.config(text='Success!')
        except Exception as e:
            print(f'Exception: {e}')
            self.ubutton_label.config(text='Save error.')
        return

    def load_user_lib(self):
        try:
            with open('user_lib.pkl', 'rb') as f:
                self.user_lib = pkl.load(f)
            self.build_lib_copy()
            self.tool_enable['library_built'] = True
            self.ubutton_label.config(text='Success!')
        except Exception as e:
            print(f'Exception: {e}')
            self.ubutton_label.config(text='Load error.')
        return


    #QUERIES
    def q_show_library(self):
        try:
            print(self.user_lib.columns)
            self.q_clear_query_area()
            self.view_table = Table(parent=self.query_area, dataframe=self.user_lib_copy, showtoolbar=False)
            self.view_table.show()
            self.view_table.redraw()
        except Exception as e:
            print(f'Exception: {e}')
            self.ubutton_label.config(text=f'{e}')
        return

    
    def q_show_user_stats(self):
        try:
            # TODO: MAKE THIS NOT USELESS
            self.q_clear_query_area()
            self.view_table = Table(parent=self.query_area, dataframe=self.user_info, showtoolbar=False)
            self.view_table.show()
            self.view_table.redraw()
        except Exception as e:
            print(f'Exception: {e}')
            self.ubutton_label.config(text=f'{e}')
        return


    def q_show_playtime_graph_bygame(self):
        try:
            self.q_clear_query_area()
            self.fig, self.ax = plt.subplots()
            self.user_lib_copy = self.user_lib_copy.sort_values(ascending=False, by=['Total Playtime (hours)'])
            x = self.user_lib_copy['Name'][0:10]
            y = self.user_lib_copy['Total Playtime (hours)'][0:10]
            self.ax.bar(x, y)
            self.ax.set_xlabel('Title')
            self.ax.set_ylabel('Playtime (Hours)')
            plt.xticks(rotation=30, fontsize=8)
            self.view_graph = FigureCanvasTkAgg(self.fig, self.query_area)
            self.view_graph.draw()
            self.view_graph.get_tk_widget().pack()
            self.ubutton_label.config(text='Success!')
        except Exception as e:
            print(f'{e}')
            self.ubutton_label.config(text=f'{e}')
        return


    def q_show_playtime_graph_bysystem(self):
        try:
            self.q_clear_query_area()
            self.fig, self.ax = plt.subplots()
            bar_labels = ['Windows', 'Mac', 'Linux', 'Deck']
            bar_colors = ['tab:red', 'tab:blue', 'tab:orange', 'tab:green']
            x = bar_labels
            y = [self.user_lib['playtime_windows_forever'].sum()/60, self.user_lib['playtime_mac_forever'].sum()/60, self.user_lib['playtime_linux_forever'].sum()/60, self.user_lib['playtime_deck_forever'].sum()/60]
            self.ax.bar(x, y, tick_label=bar_labels, color=bar_colors)
            self.ax.set_xlabel('System')
            self.ax.set_ylabel('Playtime (Hours)')

            self.view_graph = FigureCanvasTkAgg(self.fig, self.query_area)
            self.view_graph.draw()
            self.view_graph.get_tk_widget().pack()
            self.ubutton_label.config(text='Success!')
        except Exception as e:
            print(f'{e}')
            self.ubutton_label.config(text=f'{e}')
        return


    def q_show_playtime_graph_2weeks(self):
        try:
            self.q_clear_query_area()
            self.fig, self.ax = plt.subplots()
            self.user_lib_copy = self.user_lib.copy()
            self.user_lib_copy = self.user_lib_copy.sort_values(ascending=False, by=['playtime_2weeks'])

            x = self.user_lib_copy['name'][0:10]
            y = self.user_lib_copy['playtime_2weeks'][0:10]/60
            self.ax.bar(x, y)
            self.ax.set_xlabel('Title')
            self.ax.set_ylabel('Playtime (2 weeks, hours)')
            plt.xticks(rotation=30, fontsize=8)
            self.view_graph = FigureCanvasTkAgg(self.fig, self.query_area)
            self.view_graph.draw()
            self.view_graph.get_tk_widget().pack()
            self.ubutton_label.config(text='Success!')
            self.build_lib_copy()
        except Exception as e:
            print(f'{e}')
            self.ubutton_label.config(text=f'{e}')
        return


    def q_show_user_achievements(self):
        self.q_clear_query_area()
        # TODO
        return


    def q_select_game(self):
        self.q_clear_query_area()
        # TODO
        return


    def q_show_game_achievements(self):
        self.q_clear_query_area()
        # TODO
        return


    def q_show_game_news(self):
        self.q_clear_query_area()
        # TODO
        return


    def q_show_game_stats(self):
        self.q_clear_query_area()
        # TODO
        return

    def q_show_unplayed_games(self):
        try:
            self.user_lib_copy = self.user_lib_copy[self.user_lib_copy['Total Playtime (hours)'] == 0]
            self.q_show_library()
            self.ubutton_label.config(text=f'{len(self.user_lib_copy)} unplayed games')
            self.build_lib_copy()
        except Exception as e:
            print(f'{e}')
            self.ubutton_label.config(text=f'{e}')
        return


    ''' V GUI FUNCTIONS V '''
    def gui_user_area(self):
        self.user_area = Frame(self.main_window, bg=COLOR_2, bd=4, height=200, width=540) # FRAME
        self.user_area.grid(row=1, column=0, rowspan=2, columnspan=4, padx=5, pady=5)
        self.user_area.grid_propagate(False)

        self.uid_entry = Entry(self.user_area, bg=COLOR_3, bd=1, cursor='xterm', font=FONT_3, fg=COLOR_5, width=25) # ID ENTRY
        # self.uid_entry.insert(0, STEAM_ID) # USING MY ID FOR DEMONSTRATION
        self.uid_entry.insert(0, 'Enter Here')
        self.uid_entry.grid(row=0, column=0, rowspan=1, columnspan=2)
        self.uid_label = Label(self.user_area, bg=COLOR_2, bd=1, font=FONT_3, fg=COLOR_3, height=1, width=25, text='17-digit User ID', justify='left', anchor='w')
        self.uid_label.grid(row=0, column=3, rowspan=1, columnspan=2)

        self.ukey_entry = Entry(self.user_area, bg=COLOR_3, bd=1, cursor='xterm', font=FONT_3, fg=COLOR_5, width=25, show='*') # KEY ENTRY
        # self.ukey_entry.insert(0, API_TOKEN) # USING MY TOKEN FOR DEMONSTRATION
        self.ukey_entry.insert(0, 'xoxo')
        self.ukey_entry.grid(row=1, column=0, rowspan=1, columnspan=2)
        self.ukey_label = Label(self.user_area, bg=COLOR_2, bd=1, font=FONT_3, fg=COLOR_3, height=1, width=25, text='Steam Web API Key', justify='left', anchor='w')
        self.ukey_label.grid(row=1, column=3, rowspan=1, columnspan=2)
        
        self.ubuild = Button(self.user_area, bd=1, bg=COLOR_4, command=self.fetch_user_info, font=FONT_3, fg=COLOR_5, height=1, width=25, text='Fetch User Data') # BUILD USER
        self.ubuild.grid(row=0, column=5, rowspan=1, columnspan=2)

        self.lbuild = Button(self.user_area, bd=1, bg=COLOR_4, command=self.build_user_lib, font=FONT_3, fg=COLOR_5, height=1, width=25, text='Build User Library') # BUILD LIB
        self.lbuild.grid(row=1, column=5, rowspan=1, columnspan=2)

        self.lload = Button(self.user_area, bd=1, bg=COLOR_4, command=self.load_user_lib, font=FONT_3, fg=COLOR_5, height=1, width=25, text='Load User Library') # LOAD LIB
        self.lload.grid(row=2, column=5, rowspan=1, columnspan=2)

        self.uload = Button(self.user_area, bd=1, bg=COLOR_4, command=self.load_user_info, font=FONT_3, fg=COLOR_5, height=1, width=25, text='Load User Data')
        self.uload.grid(row=3, column=5, rowspan=1, columnspan=2)

        self.ubutton_label = Label(self.user_area, bg=COLOR_2, bd=1, font=FONT_3, fg=COLOR_3, height=1, width=25, text='Query Status', justify='center', anchor='center')
        self.ubutton_label.grid(row=4, column=5, rowspan=1, columnspan=2)

        self.upfp_image = Image.open('upfp_ph.png')
        self.upfp_image = self.upfp_image.resize((50, 50))
        self.upfp_image_tk = ImageTk.PhotoImage(self.upfp_image)
        self.upfp = Label(self.user_area, bg=COLOR_3, bd=1, height=50, width=50, image=self.upfp_image_tk) # AVATAR
        self.upfp.grid(row=3, column=0, rowspan=2, columnspan=1, padx=3, pady=3)

        self.uname = Label(self.user_area, bg=COLOR_2, bd=1, font=FONT_3, fg=COLOR_3, height=1, width=25, text='Username', justify='left', anchor='w') # NAME
        self.uname.grid(row=3, column=1, rowspan=1, columnspan=2, padx=3, pady=3)


        self.uurl = Label(self.user_area, bg=COLOR_2, bd=1, font=FONT_3, fg=COLOR_3, height=1, width=50, text='Profile URL', justify='left', anchor='w') # URL
        self.uurl.grid(row=4, column=1, rowspan=1, columnspan=4, padx=3, pady=3)

        self.ustatus = Label(self.user_area, bg=COLOR_2, bd=1, font=FONT_3, fg=COLOR_3, height=1, width=25, text='Status', justify='left', anchor='w') # STATUS
        self.ustatus.grid(row=5, column=1, rowspan=1, columnspan=2, padx=3, pady=3)
        return


    def gui_tool_area(self):
        self.tool_area = Frame(self.main_window, bg=COLOR_2, bd=4, height=400, width=540) # FRAME
        self.tool_area.grid(row=3, column=0, rowspan=4, columnspan=4, padx=5, pady=5)
        self.tool_area.grid_propagate(False)

        self.show_library = Button(self.tool_area, bd=1, bg=COLOR_4, command=self.q_show_library, font=FONT_3, fg=COLOR_5, height=1, width=28, text='Show User Library')
        self.show_library.grid(row=0, column=0, rowspan=1, columnspan=2)

        self.show_user_stats = Button(self.tool_area, bd=1, bg=COLOR_4, command=self.q_show_user_stats, font=FONT_3, fg=COLOR_5, height=1, width=28, text='Show User Stats')
        self.show_user_stats.grid(row=0, column=2, rowspan=1, columnspan=2)

        self.show_playtime_graph_bygame = Button(self.tool_area, bd=1, bg=COLOR_4, command=self.q_show_playtime_graph_bygame, font=FONT_3, fg=COLOR_5, height=1, width=28, text='Show Playtime Graph (Game)')
        self.show_playtime_graph_bygame.grid(row=0, column=4, rowspan=1, columnspan=2)


        self.show_playtime_graph_bysystem = Button(self.tool_area, bd=1, bg=COLOR_4, command=self.q_show_playtime_graph_bysystem, font=FONT_3, fg=COLOR_5, height=1, width=28, text='Show Playtime Graph (System)')
        self.show_playtime_graph_bysystem.grid(row=1, column=0, rowspan=1, columnspan=2)

        self.show_playtime_graph_2weeks = Button(self.tool_area, bd=1, bg=COLOR_4, command=self.q_show_playtime_graph_2weeks, font=FONT_3, fg=COLOR_5, height=1, width=28, text='Show Playtime Graph (2 Weeks)')
        self.show_playtime_graph_2weeks.grid(row=1, column=2, rowspan=1, columnspan=2)

        # self.show_user_achievements = Button(self.tool_area, bd=1, bg=COLOR_4, command=self.q_show_user_achievements, font=FONT_3, fg=COLOR_5, height=1, width=28, text='Show Achievemens (User)')
        # self.show_user_achievements.grid(row=1, column=4, rowspan=1, columnspan=2)

        # self.select_game = Button(self.tool_area, bd=1, bg=COLOR_4, command=self.q_select_game, font=FONT_3, fg=COLOR_5, height=1, width=28, text='Select Game')
        # self.select_game.grid(row=2, column=0, rowspan=1, columnspan=2)

        # self.show_game_achievements = Button(self.tool_area, bd=1, bg=COLOR_4, command=self.q_show_game_achievements, font=FONT_3, fg=COLOR_5, height=1, width=28, text='Show Achievements (Game)')
        # self.show_game_achievements.grid(row=2, column=2, rowspan=1, columnspan=2)

        # self.show_game_news = Button(self.tool_area, bd=1, bg=COLOR_4, command=self.q_show_game_news, font=FONT_3, fg=COLOR_5, height=1, width=28, text='Show Game News')
        # self.show_game_news.grid(row=2, column=4, rowspan=1, columnspan=2)

        # self.show_game_stats = Button(self.tool_area, bd=1, bg=COLOR_4, command=self.q_show_game_stats, font=FONT_3, fg=COLOR_5, height=1, width=28, text='Show Game Stats')
        # self.show_game_stats.grid(row=3, column=0, rowspan=1, columnspan=2)

        self.show_unplayed_games = Button(self.tool_area, bd=1, bg=COLOR_4, command=self.q_show_unplayed_games, font=FONT_3, fg=COLOR_5, height=1, width=28, text='Show Unplayed Games')
        # self.show_unplayed_games.grid(row=3, column=2, rowspan=1, columnspan=2)
        self.show_unplayed_games.grid(row=3, column=0, rowspan=1, columnspan=2)

        self.clear_query_area = Button(self.tool_area, bd=1, bg=COLOR_4, command=self.q_clear_query_area, font=FONT_3, fg=COLOR_5, height=1, width=28, text='Clear Query Area')
        self.clear_query_area.grid(row=4, column=0, rowspan=1, columnspan=2)
        return


    def gui_query_area(self):
        self.query_area = Frame(self.main_window, bg=COLOR_2, bd=4, height=610, width=600) # FRAME
        self.query_area.grid(row=1, column=5, rowspan=6, columnspan=6, padx=5, pady=5)
        self.query_area.grid_propagate(False)
        return

    def q_clear_query_area(self):
        try:
            for c in self.query_area.winfo_children():
                c.destroy()
        except Exception as e:
            print(f'{e}')
            self.ubutton_label.config(text=f'{e}')
        return

# MAIN
with warnings.catch_warnings():
    warnings.simplefilter(action='ignore', category=FutureWarning)

    sm = Tool()

    sm.main_window.mainloop()