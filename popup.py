#MADED In 02 May 2026-04 May 2026
#Time: 6 Hrs
import webview
import random
error_count=0
with open("Project/assets/json/error_count.json","r") as f:
    error_count=int(f.read())
class API:
    def closewindow(self):
        print("closing")
        webview.windows[0].destroy()
        with open("Project/assets/json/error_count.json","w") as f:
            f.write(str(error_count))

screen_w, screen_h = webview.screens[0].width, webview.screens[0].height

x = int(random.random() * (screen_w - 300))
y = int(random.random() * (screen_h - 250))
api=API()
window = webview.create_window(
    "Error",
    "error.html",
    width=270,
    height=240,
    frameless=True,
    on_top=True,
    x=x,
    y=y,
    js_api=api
)

error_count += 1

webview.start()