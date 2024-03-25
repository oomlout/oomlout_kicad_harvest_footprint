import os
import copy
import time
import pyautogui
import glob
import yaml

from kiutils.footprint import Footprint

def main(**kwargs):
    filters = kwargs.get("filters", [""])
    
    #get the list of footprints
    folder_footprints_8 = "C:/Program Files/KiCad/8.0/share/kicad/footprints"

    list_footprint = []
    #get a list of all .kicad_mod files in the folder recursively using glob
    for file in glob.glob(folder_footprints_8 + "/**/*.kicad_mod", recursive=True):
        list_footprint.append(file)

    #go through each footprint
    for filter in filters:        
        for footprint in list_footprint:
            #open the footprint in kicad
            print(f"Opening {footprint}")
            if filter in footprint:
                directory = harvest_footprint_kiutils(footprint)
                create_pcb_file(directory)

def create_pcb_file(directory):
    file_pcb_source = "source/kicad_empty_board/working.kicad_pcb"
    file_pcb_destination = f"{directory}/working/working.kicad_pcb"
    file_footprint_source = f"{directory}/footprint.kicad_mod"

    from kiutils.board import Board
    from kiutils.footprint import Footprint
    from kiutils.items.common import Position
    from kiutils.items.fpitems import FpText

    from os import path

    # Load board file and footprint file
    board = Board().from_file(file_pcb_source)
    footprint = Footprint().from_file(file_footprint_source)

    # Set new footprint's position
    footprint.position = Position(X=0, Y=0)

    
    # Append footprint to board and save board
    board.footprints.append(footprint)
    # make directory for working
    os.makedirs(f"{directory}/working", exist_ok=True)
    board.to_file(file_pcb_destination)

    pass

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

def harvest_footprint_kiutils(file_footprint):



    print(f"Harvesting {file_footprint}")
    #open the footprint in kicad
    #load the footprint with kiutils
    try: 
        footprint = Footprint().from_file(file_footprint)
        
        
        #get library name it is the name of the .pretty folder
        library_name = os.path.basename(os.path.dirname(file_footprint))    
        library_name = sanitize(library_name.replace(".pretty", ""))

        footprint_name = os.path.basename(file_footprint)
        footprint_name = sanitize(footprint_name.replace(".kicad_mod", ""))

        #get the footprint name
        part_details = {}
        part_details["description"] = "eda" 
        part_details["classification"] = "kicad_footprint"
        part_details["type"] = "kicad_default"
        part_details["size"] = ""
        part_details["color"] = ""
        part_details["description_main"] = library_name
        part_details["description_extra"] = footprint_name
        part_details["manufacturer"] = ""
        part_details["part_number"] = ""
        part_details["short_name"] = ""
        
        param_order = ["description", "classification", "type", "size", "color", "description_main", "description_extra", "manufacturer", "part_number", "short_name"]

        footprint_id = ""
        for param in param_order:
            footprint_id += part_details[param] + "_"
        footprint_id = sanitize(footprint_id)   

        part_details["footprint_id"] = footprint_id
        part_details["id"] = footprint_id

        directory = f"parts/{footprint_id}"
        os.makedirs(directory, exist_ok=True)
        

            
        #copy the footprint kicad_mod file to footprint.kicad_mod
        os.system(f'copy "{file_footprint}" "{directory}/footprint.kicad_mod"')
        
        #make a version of footprint, go through each value and convert it to a string
        footprint_copy = copy.deepcopy(footprint)
        for key in footprint_copy.__dict__:
            if type(footprint_copy.__dict__[key]) is not str:
                footprint_copy.__dict__[key] = str(footprint_copy.__dict__[key])
        
        part_details["footprint_string"] = footprint_copy.__dict__

        #dump part_details to yaml file to working.yaml
        with open(f"{directory}/working.yaml", "w") as file:
            yaml.dump(part_details, file)

        pass
    except Exception as e:
        print(f"Error loading {file_footprint}")
        print(e)
        return    
    
    return directory

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