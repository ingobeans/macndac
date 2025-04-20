import keyboard, time, pydirectinput
from datetime import datetime
from ctypes import windll

version = "0.1.7"

# improve accuracy
timeBeginPeriod = windll.winmm.timeBeginPeriod
timeBeginPeriod(1)
pydirectinput.PAUSE=0

def record():
    file_data = ""
    last = datetime.now()
    while True:
        event = keyboard.read_event()
        if event.name == "esc":
            break
        now = datetime.now()
        elapsed = (now-last)
        last = now
        file_data += "\nwait:"+str(elapsed.microseconds)
        
        file_data +="\n"+event.event_type+ ":"+event.name
    
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
                print(f"sleep for {amt}")
                time.sleep(amt)
            case "down":
                pydirectinput.keyDown(split[1])
            case "up":
                pydirectinput.keyUp(split[1])
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
                if event.name == "r":
                    print("hotkey record")
                    record()
                elif event.name == "p":
                    print("hotkey play")
                    play()
                elif event.name == "esc":
                    quit()
        case _ : 
            print("bad")
            quit()