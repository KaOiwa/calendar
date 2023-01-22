from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar
import jpholiday
import tkinter as tk
from tkinter import ttk


WEEKDAY_COLOR = (None, "red", *(["black"] * 5), "blue")
A_MONTH = relativedelta(months=1)
MONTH_LIST = list(range(1,13))


class TkCalendar(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.pack()
        today = datetime.today()
        self.date = date(today.year, today.month, 1)
        self.calendar = calendar.Calendar()
        self.calendar.setfirstweekday(6)
    
    def build(self):
        self.build_date()
        self.build_weekdays()
        self.build_days()

    def build_date(self, font=("", 20)):
        frame = tk.Frame(self)
        frame.pack(pady=5)
        #先月ボタン
        prev = tk.Button(frame, text="<", font=font, command=self.prev_month)
        prev.pack(side=tk.LEFT)
        #年月表示
        self.year = tk.Label(frame, text=self.date.year, font=font)
        self.year.pack(side=tk.LEFT)
        slash = tk.Label(frame, text="/", font=font)
        slash.pack(side="left")
        self.month = ttk.Combobox(frame, values=MONTH_LIST, font=font, width=2, state='readonly')
        self.month.set(MONTH_LIST[self.date.month -1])
        self.month.bind('<<ComboboxSelected>>',self.monthbox)
        self.month.pack(side=tk.LEFT)
        #翌月ボタン
        next = tk.Button(frame, text=">", font=font, command=self.next_month)
        next.pack(side=tk.LEFT)
    
    def build_weekdays(self):
        frame = tk.Frame(self)
        frame.pack(pady=5)
        for column, weekday in enumerate("日月火水木金土", 1):
            widget = tk.Button(frame, text=weekday, fg=WEEKDAY_COLOR[column],
                                height=2, width=4, relief="flat")
            widget.grid(column=column, row=1, padx=10, pady=5)
    
    def build_days(self):
        self.days = tk.Frame(self)
        self.days.pack()
        self.update_days()

    def update_days(self):
        for day in self.days.winfo_children():
            day.destroy()
        year, month = self.date.year, self.date.month
        weeks = self.calendar.monthdayscalendar(year, month)
        for row, week in enumerate(weeks, 1):
            for column, day in enumerate(week, 1):
                if day == 0:
                    continue
                color = WEEKDAY_COLOR[column]
                if jpholiday.is_holiday(date(year, month, day)):
                    color = "red"
                widget = tk.Button(self.days, text=day, fg=color,
                                   height=2, width=4, relief="flat")
                widget.grid(column=column, row=row, padx=10, pady=5)

    def update(self):
        self.year["text"] = self.date.year
        self.month.state ='normal'
        self.month.set(MONTH_LIST[self.date.month -1])
        self.month.state ='readonly'
        self.update_days()

    def prev_month(self):
        self.date -= A_MONTH
        self.update()

    def next_month(self):
        self.date += A_MONTH
        self.update()
    
    def monthbox(self,event):
        be_month = int(self.month.get()) - self.date.month
        self.date += relativedelta(months=be_month)
        self.update()




def main():
    root = tk.Tk()
    root.title("calendar")
    root.geometry("600x440")
    tkcalendar = TkCalendar(root)
    tkcalendar.build()
    root.mainloop()

if __name__ == "__main__":
    main()


print("fin")
