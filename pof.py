import random

# generusly donated by Stack Overflow @Boubakr (lol)
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# they're objects so i'll be expanded more easily.
class part:
    def __init__(self, name, isHighlight = False, code = "", var="", color = "", visible = True):
        self.visible = visible
        self.code = code
        self.color = color
        self.isHighlight  = isHighlight
        self.var = var
        self.name = name

# colors in fish shell scripting
colors = "> black, red, green, yellow, blue, magenta, cyan, white, brblack, \n> brred, brgreen, bryellow, brblue, brmagenta, brcyan, brwhite"

themecode = "" # fish sccripting for the theme
fishprompt = "" # to be in fish_prompt fucntion in .fish file
welcomeMSG  = """
Fish O' Plenty
==============
This is a simple tool to allow you to create your own fish shell themes!
My Github: https://github.com/AggamR
"""
print(welcomeMSG)

# everything that the theme consists of (very limited, but it will be expanded...) 
components = [
    part("command syntax highlight", True, code = "set fish_color_command <COLOR>"),
    part("argument syntax highlight", True, code = "set fish_color_param <COLOR>"),
    part("error syntax highlight",True, code = "set fish_color_error <COLOR>"),
    part("[", var = "\"[\""),
    part("user", var = "$USER"),
    part("@", var = "\"@\""),
    part("machine name", code = "set machineName (cat /proc/sys/kernel/hostname)", var = "$machineName"),
    part(":", var = "\": \""),
    part("Working Directory", code = "set cwd (string replace /home/$USER \"~\" $PWD)", var = "$cwd"),
    part("]", var = "\"]\""),
    part("Root Indication ($, #)", code = "set sign \"\"\n\tif [ \"$USER\" = \"root\" ]\n\t\tset sign \"# \"\n\telse\n\t\tset sign '$ '\n\tend", var = "$sign")
]

for component in components:
    print(f"{color.BOLD}{color.RED}====={color.YELLOW}====={color.GREEN}====={color.CYAN}====={color.BLUE}====={color.PURPLE}====={color.END}")
    print(f"{color.BOLD}Component: \"{component.name}\"{color.END}")
    
    if not component.isHighlight:
        validVis = False # fail-safe for bool(int())
        while not validVis:
            try:
                component.visible = bool(int(input(f"Do you want this component to be visible({color.RED}0{color.END}/{color.GREEN}1{color.END})? ")))
                validVis = True
            except:
                pass
            
        if not component.visible:
            component.code = "" # makes less IF statements later
            continue
    
    print(f"> available colors are: \n{colors}")
    while (component.color not in colors.replace("\n","").replace("> ","").split(", ")) or (component.color == " "):
        component.color = input(f"please enter a valid color for this component: ")
        #random color
        if component.color == "r":
            component.color = colors.split(", ")[random.randint(0,len(colors.split(", "))-1)]
            
    if component.isHighlight:
        themecode += f"{component.code}\n".replace("<COLOR>",component.color)
        
#making of code
varsSetup = "" # setup of vars like "cwd"
finalLine = "echo " #the final line, the "echo".
for component in components:
    if not component.isHighlight and component.visible:
        varsSetup += f"\t{component.code}\n" 
        finalLine += f"(set_color {component.color}){component.var}"

themecode += (f"\nfunction fish_prompt\n{varsSetup}\n\t{finalLine}\nend")

# saving of code
vaildInp = False # fail-safe for int()
toConf = ""
while not vaildInp:
    toConf = input("It's ready!\nShould I config your shell, or save it for you as a file? (1=conf, 0=save) ")
    try:
        toConf = int(toConf)
        vaildInp = True
    except:
        pass

if int(toConf):
    usr = input("what is your user's name? ")
    with open(f"/home/{usr}/.config/fish/functions/fish_prompt.fish", "w") as f:
        f.write(themecode)
    print(f"done!\nconfig file saved to: /home/{usr}/.config/fish/functions/fish_prompt.fish")
else:
    with open("fish_prompt.fish", "w") as f:
        f.write(themecode)
    print(f"done!\nconfig file saved to: fish_prompt.fish")
