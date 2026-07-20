from pathlib import Path

from customtkinter import *
from PL.pl_Daroo import AppDaroo

BASE_DIR = Path(__file__).resolve().parent
ICON_PATH = BASE_DIR / "assets" / "icons" / "bottle_drugs.ico"

if __name__ == "__main__":
    # اول ظاهر و رنگ
    set_appearance_mode("dark")
    set_default_color_theme("green")

    # پنجره اصلی
    screen = CTk()
    screen.geometry("1350x700+0+0")
    screen.title("داروخانه دکتر فریدونی")
    screen.iconbitmap(str(ICON_PATH))

    # اجرای برنامه
    appDaroo = AppDaroo(screen)

    screen.mainloop()