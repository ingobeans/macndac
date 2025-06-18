import keyboard.mouse
import keyboard, time, pydirectinput
from datetime import datetime
from ctypes import windll

version = "0.1.9"

# improve accuracy
timeBeginPeriod = windll.winmm.timeBeginPeriod
timeBeginPeriod(1)
pydirectinput.PAUSE=0

# globals
file_data = ""
last = datetime.now()
recording = False

def on_click():
    global file_data, last, recording
    if not recording:
        return
    now = datetime.now()
    elapsed = (now-last)
    file_data += "\nwait:"+str(elapsed.microseconds)
    file_data +="\n"+"click"

keyboard.mouse.on_click(on_click)
def record():
    global file_data, last, recording
    file_data = ""
    recording = True
    
    while True:
        event = keyboard.read_event()
        
        if event.name == "esc":
            break
        now = datetime.now()
        elapsed = (now-last)
        last = now
        file_data += "\nwait:"+str(elapsed.microseconds)
        
        file_data +="\n"+event.event_type+ ":"+event.name
    
    recording = False
    print("done")
    with open("macro.mnd","w") as f:
        f.write(file_data)

def play():
    with open("macro.mnd","r") as f:
        file_data = f.read()
    for index,line in enumerate(file_data.split("\n")):
        if not line:
            continue
        split = line.split(":")
        match split[0]:
            case "wait":
                amt = float(split[1])*0.000001
                time.sleep(amt)
            case "down":
                pydirectinput.keyDown(split[1])
            case "up":
                pydirectinput.keyUp(split[1])
            case "click":
                pydirectinput.leftClick()
            case _ : 
                print(f"bad file at line: {index}")
                quit()

if __name__ == "__main__":
    print(f"macndac {version}")
    match(input("[R]ecord or [P]lay or [H]otkey: ").lower()):
        case "r":
            record()
        case "p":
            play()
        case "h":
            while True:
                event = keyboard.read_event()
                
                if not event.event_type == "down":
                    continue
                if event.name == "r":
                    print("hotkey record")
                    record()
                elif event.name == "p":
                    print("hotkey play")
                    play()
        case _ : 
            print("bad")
            quit()