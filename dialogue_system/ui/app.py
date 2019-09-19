import tkinter as tk


class App(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self._controller = controller
        self.pack()
        self.createWidgets()

    def talk_btn_down(self, event):
        self._controller.start_listening()

    def talk_btn_up(self, event):
        self._controller.stop_listening()

    def face_btn_down(self, event):
        self._controller.start_face_match()

    def face_btn_up(self, event):
        self._controller.stop_face_match()

    def createWidgets(self):
        self.text_entry = tk.Entry()
        self.text_entry.pack({'side': 'top'})

        self.talk_btn = tk.Button(self)
        self.talk_btn['text'] = 'Mic',
        self.talk_btn.pack({'side': 'bottom'})
        self.talk_btn.bind('<ButtonPress-1>', self.talk_btn_down)
        self.talk_btn.bind('<ButtonRelease-1>', self.talk_btn_up)

        self.face_btn = tk.Button(self)
        self.face_btn['text'] = 'Face',
        self.face_btn.pack({'side': 'bottom'})
        self.face_btn.bind('<ButtonPress-1>', self.face_btn_down)
        self.face_btn.bind('<ButtonRelease-1>', self.face_btn_up)

def run(controller):
    root = tk.Tk()
    app = App(master=root, controller=controller)
    app.mainloop()
