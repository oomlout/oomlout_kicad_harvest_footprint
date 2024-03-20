import os
import copy
import time
import pyautogui
import glob
import yaml

from kiutils.footprint import Footprint

def main(**kwargs):
    filters = kwargs.get("filters", [""])
    overwrite = kwargs.get("overwrite", False)

    global typ
    #typ = "surface"
    typ = "desktop"
    set_mouse_positions(typ)

    #launch kicad window
    if True:
        launch_kicad()
        lauch_footprint_browser()

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
                return_value = harvest_footprint_image(footprint, overwrite)
                count += return_value
                print(f"Harvested {count} footprints")

            if count % 20 == 0:
                print("restaring kicad")    
                close_kicad()
                launch_kicad()
                lauch_footprint_browser()
                count = 1
    
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
    pyautogui.doubleClick(location[0], location[1], duration=duration)
    if wait > 2:
        delay(wait)
    else:
        time.sleep(wait)

def oom_hotkey(key1, key2, wait=1):
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

def oom_typewriter(string, wait=1):
    #type the string
    print(f"Typing {string}")
    pyautogui.typewrite(string)
    if wait > 1:
        delay(wait)
    else:
        time.sleep(wait)

def set_mouse_positions(typ):
    global position_filter_box, position_first_result, position_menu_file, position_menu_view, position_menu_3d_view, position_footprint_browser

    if typ == "desktop":
        position_filter_box = [65,114]
        position_first_result = [92,185]
        position_footprint_browser = [330,268]
        position_menu_file = [18,33]
        position_menu_view = [87,33]
        position_menu_3d_view = [87,33]
    elif typ == "surface":
        position_filter_box = [53,115]
        position_first_result = [110,157]
        position_footprint_browser = [315,204]
        position_menu_file = [18,33]
        position_menu_view = [87,33]
        position_menu_3d_view = [87,33]


def harvest_footprint_image(footprint, overwrite):

    return_value = 0

    print(f"Harvesting {footprint}")

    yaml_file = f"parts/{footprint}/working.yaml"
    cwd = os.getcwd()
    folder_full = f"{cwd}/parts/{footprint}/"
    
    test_file = f"{folder_full}image_3d_iso.png"

    if not os.path.exists(test_file) or overwrite:

        #replace slashes
        folder_full = folder_full.replace("/", "\\")

        details = {}
        with open(yaml_file, 'r') as stream:        
            details = yaml.safe_load(stream)


        #click on the filter box
        oom_click(position_filter_box)
        
        oom_click(position_filter_box)
        

        #select all
        oom_hotkey('ctrl', 'a')
        

        #delete
        oom_press('delete')
        

        footprint_name = details["footprint_string"]["entryName"]
        #type the footprint name
        oom_typewriter(footprint_name)
        

        #doubnle click on first result
        oom_double_click(position_first_result, 5)


        export_kicad_mod(footprint, folder_full, overwrite)
        export_view_as_png(footprint, folder_full, overwrite)
        export_3d_view(footprint, folder_full, overwrite)

        return_value = 1
    return return_value

def export_3d_view(footprint, folder_full, overwrite):
    print(f"Exporting 3d view {footprint}")
    #test iso
    test_file = f"{folder_full}image_3d_iso.png"
    if not os.path.exists(test_file) or overwrite:
        #export
        oom_click(position_menu_view)
        
        #send 3
        oom_typewriter("3", 5)
        #maximize window
        if typ == "desktop":
            pass
            #oom_hotkey('win', 'up')
            

        views = ["top", "bottom", "iso"]

        for view in views:
            test_file = f"{folder_full}image_3d_{view}.png"
            if not os.path.exists(test_file) or overwrite:
                if view == "top":
                    #send z
                    oom_typewriter("z")
                    
                elif view == "bottom":
                    #send shift z
                    oom_typewriter('Z')
                    
                elif view == "iso":
                    #send i
                    oom_typewriter("z")
                    
                    #rot x
                    times = 3
                    for i in range(times):
                        oom_click(position_menu_3d_view)
                        
                        #down 6 times
                        oom_typewriter(["down", "down", "down", "down", "down", "down"])
                        
                        #enter
                        oom_typewriter(["enter"])
                        
                    #rot z
                    times = 2
                    for i in range(times):
                        oom_click(position_menu_3d_view)
                        
                        #down 11 times
                        oom_typewriter(["down", "down", "down", "down", "down", "down", "down", "down", "down", "down", "down"])
                        
                        #enter
                        oom_typewriter(["enter"])
                        

                #export
                
                oom_click(position_menu_file)
                
                #down one
                oom_typewriter(["down"])
                
                #send enter
                oom_typewriter(["enter"] , wait=5)
                #send folder full
                oom_typewriter(folder_full)
                
                #send image_3d_{view}.png
                oom_typewriter(f"image_3d_{view}.png")
                
                #send enter
                oom_typewriter(["enter"])
                
                #send y
                oom_typewriter("y", wait=5)
                #send enter
                oom_typewriter(["enter"], wait=5)
        #clsoe 3d viewer
        #click file
        oom_click(position_menu_file)
        
        #send up
        oom_typewriter(["up"])
        
        #send enter
        oom_typewriter(["enter"], wait=10)

            




def export_kicad_mod(footprint, folder_full, overwrite):
    print(f"Exporting kicad_mod {footprint}")
    test_file = f"{folder_full}footprint_export.kicad_mod"
    if not os.path.exists(test_file) or overwrite:
        #export
        oom_click(position_menu_file)
        
        #send e
        oom_typewriter("e")
        
        #send enter
        oom_typewriter(["enter"],5)
        
        #send folder full
        oom_typewriter(folder_full)
        
        #send footprint_export.kicad_mod
        oom_typewriter("footprint_export.kicad_mod")
        
        #send enter
        oom_typewriter(["enter"])
        
        #send y
        oom_typewriter("y",5)
        #send enter
        oom_typewriter(["enter"], wait=5)

def export_view_as_png(footprint, folder_full, overwrite):
    test_file = f"{folder_full}footprint_outline.png"
    if not os.path.exists(test_file) or overwrite:
        print(f"Exporting view as png {footprint}")
        print(f"Exporting {footprint}")
        #export
        oom_click(position_menu_file)
        
        #send e
        oom_typewriter("e")
        
        #send down
        oom_typewriter(["down"])
        
        #send enter
        oom_typewriter(["enter"], wait=5)
        
        #send folder full
        oom_typewriter(folder_full)
        
        #send footprint_export.kicad_mod
        oom_typewriter("footprint_outline.png")
        
        #send enter
        oom_typewriter(["enter"])
        
        #send y
        oom_typewriter("y",wait=5)
        #send enter
        oom_typewriter(["enter"], wait=5)





        pass

def lauch_footprint_browser():
    print("Launching footprint browser")
    location  = position_footprint_browser
    oom_click(location, duration=1, wait=20)
    
    #maximize current window
    if typ == "desktop":
        pass
        #oom_hotkey('win', 'up')
        
    

def launch_kicad():
    print("Launching KiCad")
    app_kicad_8 = "C:/Program Files/KiCad/8.0/bin/kicad.exe"
    # launch kicad use quotes because filename conatins spaces do not wait for it to finish
    os.system(f'start "" "{app_kicad_8}"')
    delay(10)
    #maximize window
    if typ == "desktop":
        pass
        #oom_hotkey('win', 'up')
        

def sanitize(string):
    
    replace_list = []
    replace_list.append([" ", "_"])
    replace_list.append(["-", "_"])
    replace_list.append([".", "_"])
    replace_list.append(["(", "_"])
    replace_list.append([")", "_"])
    replace_list.append(["[", "_"])
    replace_list.append(["]", "_"])
    replace_list.append(["{", "_"])
    replace_list.append(["}", "_"])

    for replace in replace_list:
        string = string.replace(replace[0], replace[1])

    #replace any non number or letter with an underscore
    for char in string:
        if not char.isalnum():
            string = string.replace(char, "_")

    #remove douible and triple underscore
    string = string.replace("___", "_")
    string = string.replace("__", "_")
    string = string.replace("__", "_")

    #remove trrailing underscore
    if string[-1] == "_":
        string = string[:-1]

    #make lower
    string = string.lower()
    
    return string

if __name__ == '__main__':
    kwargs = {}
    filter = [""]
    kwargs["filters"] = filter
    main(**kwargs)