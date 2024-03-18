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

    #go through each footprint
    for filter in filters:        
        for footprint in list_footprint:
            #open the footprint in kicad
            print(f"Opening {footprint}")
            if filter in footprint:
                harvest_footprint_image(footprint, overwrite)
    
  

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
        for i in range(seconds):
            print(".", end="")
            time.sleep(1)
        print()


position_filter_box = [65,114]
position_first_result = [92,185]
position_menu_file = [18,33]
position_menu_view = [87,33]
position_menu_3d_view = [87,33]

def harvest_footprint_image(footprint, overwrite):



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
        pyautogui.click(position_filter_box)
        delay(1)

        #select all
        pyautogui.hotkey('ctrl', 'a')
        delay(1)
        #delete
        pyautogui.press('delete')
        delay(1)

        footprint_name = details["footprint_string"]["entryName"]
        #type the footprint name
        pyautogui.typewrite(footprint_name)
        delay(1)

        #doubnle click on first result
        pyautogui.doubleClick(position_first_result)
        delay(5)


        export_kicad_mod(footprint, folder_full, overwrite)
        export_view_as_png(footprint, folder_full, overwrite)
        export_3d_view(footprint, folder_full, overwrite)

def export_3d_view(footprint, folder_full, overwrite):
    print(f"Exporting 3d view {footprint}")
    #test iso
    test_file = f"{folder_full}image_3d_iso.png"
    if not os.path.exists(test_file) or overwrite:
        #export
        pyautogui.click(position_menu_view)
        delay(1)
        #send 3
        pyautogui.typewrite("3")
        delay(5)
        #maximize window
        pyautogui.hotkey('win', 'up')
        delay(2)

        views = ["top", "bottom", "iso"]

        for view in views:
            test_file = f"{folder_full}image_3d_{view}.png"
            if not os.path.exists(test_file) or overwrite:
                if view == "top":
                    #send z
                    pyautogui.typewrite("z")
                    delay(2)
                elif view == "bottom":
                    #send shift z
                    pyautogui.hotkey('Z')
                    delay(2)
                elif view == "iso":
                    #send i
                    pyautogui.typewrite("z")
                    delay(2)
                    #rot x
                    times = 3
                    for i in range(times):
                        pyautogui.click(position_menu_3d_view)
                        delay(1)
                        #down 6 times
                        pyautogui.typewrite(["down", "down", "down", "down", "down", "down"])
                        delay(1)
                        #enter
                        pyautogui.typewrite(["enter"])
                        delay(1)
                    #rot z
                    times = 2
                    for i in range(times):
                        pyautogui.click(position_menu_3d_view)
                        delay(1)
                        #down 11 times
                        pyautogui.typewrite(["down", "down", "down", "down", "down", "down", "down", "down", "down", "down", "down"])
                        delay(1)
                        #enter
                        pyautogui.typewrite(["enter"])
                        delay(1)

                #export
                pyautogui.click(position_menu_file)
                delay(1)
                #down one
                pyautogui.typewrite(["down"])
                delay(1)
                #send enter
                pyautogui.typewrite(["enter"])
                delay(5)
                #send folder full
                pyautogui.typewrite(folder_full)
                delay(1)
                #send image_3d_{view}.png
                pyautogui.typewrite(f"image_3d_{view}.png")
                delay(1)
                #send enter
                pyautogui.typewrite(["enter"])
                delay(2)
                #send y
                pyautogui.typewrite("y")
                delay(5)
                #send enter
                pyautogui.typewrite(["enter"])
                delay(5)
        #clsoe 3d viewer
        #click file
        pyautogui.click(position_menu_file)
        delay(1)
        #send up
        pyautogui.typewrite(["up"])
        delay(1)
        #send enter
        pyautogui.typewrite(["enter"])
        delay(5)

            




def export_kicad_mod(footprint, folder_full, overwrite):
    print(f"Exporting kicad_mod {footprint}")
    test_file = f"{folder_full}footprint_export.kicad_mod"
    if not os.path.exists(test_file) or overwrite:
        #export
        pyautogui.click(position_menu_file)
        delay(1)
        #send e
        pyautogui.typewrite("e")
        delay(1)
        #send enter
        pyautogui.typewrite(["enter"])
        delay(5)
        #send folder full
        pyautogui.typewrite(folder_full)
        delay(1)
        #send footprint_export.kicad_mod
        pyautogui.typewrite("footprint_export.kicad_mod")
        delay(1)
        #send enter
        pyautogui.typewrite(["enter"])
        delay(2)
        #send y
        pyautogui.typewrite("y")
        delay(5)
        #send enter
        pyautogui.typewrite(["enter"])
        delay(5)

def export_view_as_png(footprint, folder_full, overwrite):
    test_file = f"{folder_full}footprint_outline.png"
    if not os.path.exists(test_file) or overwrite:
        print(f"Exporting view as png {footprint}")
        print(f"Exporting {footprint}")
        #export
        pyautogui.click(position_menu_file)
        delay(1)
        #send e
        pyautogui.typewrite("e")
        delay(1)
        #send down
        pyautogui.typewrite(["down"])
        delay(1)
        #send enter
        pyautogui.typewrite(["enter"])
        delay(5)
        #send folder full
        pyautogui.typewrite(folder_full)
        delay(1)
        #send footprint_export.kicad_mod
        pyautogui.typewrite("footprint_outline.png")
        delay(1)
        #send enter
        pyautogui.typewrite(["enter"])
        delay(2)
        #send y
        pyautogui.typewrite("y")
        delay(5)
        #send enter
        pyautogui.typewrite(["enter"])
        delay(5)





        pass

def lauch_footprint_browser():
    print("Launching footprint browser")
    location  = [330,268]
    pyautogui.click(location)
    delay(15)
    #maximize current window
    pyautogui.hotkey('win', 'up')
    delay(2)
    

def launch_kicad():
    print("Launching KiCad")
    app_kicad_8 = "C:/Program Files/KiCad/8.0/bin/kicad.exe"
    # launch kicad use quotes because filename conatins spaces do not wait for it to finish
    os.system(f'start "" "{app_kicad_8}"')
    delay(10)
    #maximize window
    pyautogui.hotkey('win', 'up')
    delay(2)

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