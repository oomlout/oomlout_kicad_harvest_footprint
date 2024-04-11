import os
import copy
import time
import pyautogui
import glob
import yaml
import keyboard

from kiutils.footprint import Footprint

def main(**kwargs):
    filters = kwargs.get("filters", [""])
    overwrite = kwargs.get("overwrite", False)

    global typ
    typ = "surface"
    #typ = "desktop"
    set_mouse_positions(typ)


    #get the list of footprints
    folder_footprints = "parts"
    list_footprint = []
    #get a list of all the directories no recursive
    for dir in os.listdir(folder_footprints):
        list_footprint.append(dir)

    count = 1

    #go through each footprint
    for filter in filters:        
        for footprint in list_footprint:
            #open the footprint in kicad
            print(f"Opening {footprint}")
            if filter in footprint:
                return_value = harvest_footprint_pcb_image(footprint, overwrite)
                count += return_value
                print(f"Harvested {count} footprints")

            if count % 100 == 0:
                #commit the changes using os.system in one call
                git_commit()
                count += 1

            


def git_commit():
    print("Committing changes")
    #pull first
    os.system("git pull")    
    os.system("git add .")
    os.system("git commit -m \"Harvesting footprints\"")
    os.system("git push")

def close_kicad():
    print("Closing KiCad")
    #kill all processes connected to kicad
    os.system("taskkill /f /im kicad.exe")
    delay(10)

def delay(seconds):
    #if seconds is greater than five print the number of dots were waiting for, then print a dot for each second we wait
    if seconds > 5:
        for i in range(seconds):
            print(f">", end="")
        print()
        for i in range(seconds):
            print(".", end="")
            time.sleep(1)
            #if s is pressed stop the delay
            if keyboard.is_pressed("s"):
                print("Stopping delay")
                time.sleep(1)
                break
        print()
    else:
        #print a dot for each second
        if seconds >= 1:
            for i in range(seconds):
                print(".", end="")
                time.sleep(1)
            print()
        else:
            time.sleep(seconds)
        

typ = "desktop"
position_filter_box = [65,114]
position_first_result = [92,185]
position_footprint_browser = [330,268]
position_menu_file = [18,33]
position_menu_view = [87,33]
position_menu_3d_view = [87,33]


def oom_click(location, wait=1, duration=0.5):
    #if surface check and scale the location
    location = copy.deepcopy(location)
    if typ == "surface":
        screen_width, screen_height = pyautogui.size()
        location[0] = int(location[0] / (0.67))
        location[1] = int(location[1] / (0.67))


    #click on the location
    print(f"Clicking {location}")
    #move mouse first
    pyautogui.moveTo(location[0], location[1], duration=duration)
    #then click
    delay(0.5)
    pyautogui.click(location[0], location[1])
    if wait > 2:
        delay(wait)
    else:
        time.sleep(wait)

def oom_double_click(location, wait=1, duration=0.5):
    #click on the location
    print(f"Double Clicking {location}")
    location = copy.deepcopy(location)
    if typ == "surface":
        location[0] = int(location[0] / (0.67))
        location[1] = int(location[1] / (0.67))
    pyautogui.doubleClick(location[0], location[1], duration=duration)
    if wait > 2:
        delay(wait)
    else:
        time.sleep(wait)

def oom_hotkey(key1, key2, wait=2):
    #click on the location
    print(f"Hotkey {key1} {key2}")
    pyautogui.hotkey(key1, key2)
    if wait > 2:
        delay(wait)
    else:
        time.sleep(wait)

def oom_press(key, wait=1):
    #click on the location
    print(f"Pressing {key}")
    pyautogui.press(key)
    if wait > 2:
        delay(wait)
    else:
        time.sleep(wait)

def oom_typewriter(string, wait=2, times=1):
    #type the string
    if times == 1:
        print(f"Typing {string}")
    else:
        print(f"Typing {string} {times} times")
    for i in range(times):        
            pyautogui.typewrite(string, interval=0.05)               
            if times > 1:
                delay(0.25)         
    if wait > 1:
        delay(wait)
    else:
        time.sleep(wait)

def set_mouse_positions(typ):
    global position_filter_box, position_first_result, position_menu_file, position_menu_view, position_menu_3d_view, position_footprint_browser



    if typ == "desktop":
        position_filter_box = [65,114]
        position_first_result = [92,185]
        position_footprint_bro_harvest_fwser = [330,268]
        position_menu_file = [18,33]
        position_menu_view = [87,33]
        position_menu_3d_view = [87,33]
    elif typ == "surface":
        position_filter_box = [53,115]
        position_first_result = [110,187]
        position_footprint_browser = [315,204]
        position_menu_file = [18,33]
        position_menu_view = [87,33]
        position_menu_3d_view = [87,33]


def harvest_footprint_pcb_image(footprint, overwrite):

    return_value = 0

    print(f"Harvesting {footprint}")

    yaml_file = f"parts/{footprint}/working.yaml"
    cwd = os.getcwd()
    folder_full = f"{cwd}/parts/{footprint}/"    
    folder_full = folder_full.replace("//", "/")    
    folder_full = folder_full.replace("/", "\\")
    
    test_file = f"{folder_full}image.sveg"

    file_pcb = f"{folder_full}/working/working.kicad_pcb"
    #replace // with /
    file_pcb = file_pcb.replace("//", "/")
    #replace / with \\
    file_pcb = file_pcb.replace("/", "\\")
    #replace double \\ with single \
    file_pcb = file_pcb.replace("\\\\", "\\")
    length_max = 144

    if (not os.path.exists(test_file) or overwrite)  and os.path.exists(file_pcb):
        

        folder_export_temporary = f"{folder_full}working/temporary" 
        file_export_temporary = f"{folder_export_temporary}/working-brd.svg"
        file_export = f"{folder_full}image.svg"
        #replace slashes
        
        #make the temporary folder
        os.makedirs(folder_export_temporary, exist_ok=True)

        #open the pcb file 
        #print the length of the filename
        print(f"Opening {file_pcb} {len(file_pcb)}")
        os.system(f'start "" "{file_pcb}"')

        #wait for pcbnew to open
        delay(30)

        #click on the filter box
        oom_click(position_menu_file)
        
        #send e
        oom_typewriter("e", wait=1)

        #send down 5 times
        oom_typewriter(["down"], times=5, wait=1)

        #send enter
        oom_typewriter(["enter"], wait=5)

        #send folder temporary
        oom_typewriter(folder_export_temporary.replace("/", "\\"), wait=1)

        #send enter
        oom_typewriter(["enter"], wait=5)

        #send escape
        oom_typewriter(["esc"], wait=5)
        oom_typewriter(["esc"], wait=5)

        #close pcbnew
        oom_click(position_menu_file)
        oom_typewriter(["up"])
        oom_typewriter(["enter"], wait=5)

        #copy temporary file to export file if temporary file exists if not generate an error prompt that times out after ten seconds
        if os.path.exists(file_export_temporary):
            
            command = f'copy "{file_export_temporary}" "{file_export}"'
            #replace /
            command = command.replace("/", "\\")
            print(command)
            os.system(command)
        else:
            print(f"Error exporting image {file_export_temporary} does not exist")
            delay(10)

        #use inkscape to make a pdf version of the svg
        file_export_pdf = f"{folder_full}image.pdf"
        print (f"Exporting {file_export} to {file_export_pdf}")
        os.system(f'inkscape --export-filename "{file_export_pdf}" "{file_export}"')
        return_value = 1

        #remove the temporary folder and contents
        os.system(f'rmdir /s /q "{folder_export_temporary}"')

    return return_value

if __name__ == '__main__':
    kwargs = {}
    filter = [""]
    kwargs["filters"] = filter    
    main(**kwargs)
    #git_commit()