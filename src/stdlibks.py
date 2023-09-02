'''
Handles Input Output/File system reading/writing data types, etc
'''

############ IMPORTS ############
import re
############ IMPORTS ############


############ EXPORTED FUNCTIONS ###########

def Display_fn(line: str, os: str):

    ##### TOKENS #####
    DISPLAY_PATTERN = "^Display\s*\(\s*\"(.*?)\"\s*\)$"
    DISPLAY_PATTERN_NONEWLINE = "^Display\s*\(\s*no\s+new\s+line\s*\s*\"(.*?)\"\s*\)$"
    DISPLAY_PATTERN_LITERAL = "^Display\s*\(\s*literal\s*\"(.*?)\"\s*\)$"
    DISPLAY_PATTERN_LITERALNONEWLINE = "^Display\s*\(\s*literal\s+no\s+new\s+line\s*\"(.*?)\"\s*\)$"
    ##### TOKENS #####

    if re.search(DISPLAY_PATTERN, line):
        if os == "linux":
            return f'echo "{re.findall(DISPLAY_PATTERN, line)[0]}"'
        else:
            return f'Write-Output "{re.findall(DISPLAY_PATTERN, line)[0]}"'
    elif re.search(DISPLAY_PATTERN_NONEWLINE, line):
        if os == "linux":
            return f'echo -n "{re.findall(DISPLAY_PATTERN_NONEWLINE, line)[0]}"'
        else:
            return f'Write-Output -NoNewline {re.findall(DISPLAY_PATTERN_NONEWLINE, line)[0]}'
    elif re.search(DISPLAY_PATTERN_LITERAL, line):
        if os == "linux":
            return f'cat << EOF\n{re.findall(DISPLAY_PATTERN_LITERAL, line)[0]}\nEOF'
        else:
            return f'@"\n{re.findall(DISPLAY_PATTERN_LITERAL, line)[0]}\n"@'
    elif re.search(DISPLAY_PATTERN_LITERALNONEWLINE, line):
        if os == "linux":
            return f"echo -n '{re.findall(DISPLAY_PATTERN_LITERALNONEWLINE, line)[0]}'"
        else:
            return f"Write-Output -NoNewline '{re.findall(DISPLAY_PATTERN_LITERALNONEWLINE, line)[0]}'"
    else:
        return "err"



def MakeFile(line: str, os: str):
    #### TOKENS ####
    MAKEFILE_PATTERN = "^MakeFile\s*\(\s*\"(.*?)\"\s*\)$"
    MAKEFILE_PATTERN_FORCE = "^MakeFile\s*\(\s*force\s*\"(.*?)\"\s*\)$"
    #### TOKENS ####

    if re.search(MAKEFILE_PATTERN, line):
        if os == "linux":
            return f'touch "{re.findall(MAKEFILE_PATTERN, line)[0]}"'
        else:
            return 'if (Test-Path "' + re.findall(MAKEFILE_PATTERN, line)[0] + '") {(Get-Item "' + re.findall(MAKEFILE_PATTERN, line)[0] +'").LastWriteTime = Get-Date} else {New-Item "' + re.findall(MAKEFILE_PATTERN, line)[0] + '" -ItemType File}'
    elif re.search(MAKEFILE_PATTERN_FORCE, line):
        if os == "linux":
            return f'rm "{re.findall(MAKEFILE_PATTERN_FORCE, line)[0]}" && touch "{re.findall(MAKEFILE_PATTERN_FORCE, line)[0]}"'
    else:
        return "err"
    

def MakeFolder(line: str, os: str):
    #### TOKENS ####
    MAKEFOLDER_PATTERN = "^MakeFolder\s*\(\s*\"(.*?)\"\s*\)$"
    MAKEFOLDER_PATTERN_FORCE = "^MakeFolder\s*\(\s*force\s*\"(.*?)\"\s*\)$"
    MAKEFOLDER_PATTERN_SUBDIRS = "^MakeFolder\s*\(\s*enable\s+sub\s+dirs\s*\"(.*?)\"\s*\)$"
    #### TOKENS ####

    if re.search(MAKEFOLDER_PATTERN, line):
        if os == "linux":
            return f'mkdir "{re.findall(MAKEFOLDER_PATTERN, line)[0]}"'
        else:
            return f'New-Item -ItemType Directory -Path "{re.findall(MAKEFOLDER_PATTERN, line)[0]}"'
    elif re.search(MAKEFOLDER_PATTERN_FORCE, line):
        if os == "linux":
            return f'rm -rf "{re.findall(MAKEFOLDER_PATTERN_FORCE, line)[0]}" && mkdir "{re.findall(MAKEFOLDER_PATTERN_FORCE, line)[0]}"'
        else:
            return f'Remove-Item -Recurse -Force "{re.findall(MAKEFOLDER_PATTERN_FORCE, line)[0]}"; New-Item -ItemType Directory -Path "{re.findall(MAKEFOLDER_PATTERN_FORCE, line)[0]}"'
    elif re.search(MAKEFOLDER_PATTERN_SUBDIRS, line):
        if os == "linux":
            return f'mkdir -p "{re.findall(MAKEFOLDER_PATTERN_SUBDIRS, line)[0]}"'
        else:
            return f'New-Item -ItemType Directory -Path "{re.findall(MAKEFOLDER_PATTERN_SUBDIRS, line)[0]}"'
    else:
        return "err"
    

def Ask(line: str, os: str):
    ASK_PATTERN = '^Ask\s*\(\s*"(.*?)"\s*,\s*([a-zA-Z_]+)\s*\)$'

    if re.search(ASK_PATTERN, line):
        if os == "linux":
            return f'read -p "{re.findall(ASK_PATTERN, line)[0][0]}" {re.findall(ASK_PATTERN, line)[0][1]}'
        else:
            return f'${re.findall(ASK_PATTERN, line)[0][1]} = Read-Host -Prompt "{re.findall(ASK_PATTERN, line)[0][0]}"'
    else:
        return "err"
    

def Assign(line: str, os: str):
    ASSIGN_PATTERN = '^Assign\s*\(\s*(.*?)\s*,\s*([a-zA-Z_]+)\s*\)$'

    if re.search(ASSIGN_PATTERN, line):
        if os == "linux":
            return f'{re.findall(ASSIGN_PATTERN, line)[0][1]}={re.findall(ASSIGN_PATTERN, line)[0][0]}'
        else:
            return f'{re.findall(ASSIGN_PATTERN, line)[0][1]} = {re.findall(ASSIGN_PATTERN, line)[0][0]}'
    else:
        return "err"
    

def If(line: str, os: str):
    IF_PATTERN = "^If\s*\((.*?)\)\s+then$"
    ELIF_PATTERN = "^If\s+Else\s*\((.*?)\)\s+then$"

    if re.search(IF_PATTERN, line):
        if os == "linux":
            return f'if [ {get_condition(re.findall(IF_PATTERN, line)[0], os)} ]\nthen'
        else:
            return (f'if({get_condition(re.findall(IF_PATTERN, line)[0], os)})' + " {")
        
    elif re.search(ELIF_PATTERN, line):
        if os == "linux":
            return f'elif [ {get_condition(re.findall(ELIF_PATTERN, line)[0], os)} ]\nthen'
        else:
            return ("} " + f'elseif({get_condition(re.findall(ELIF_PATTERN, line)[0], os)})' + " {")
        
    else:
        return "err"
    

def Repeat(line: str, os: str):
    REPEAT_PATTERN = "^Repeat\((.*?)\)$"

    if re.search(REPEAT_PATTERN, line):
        if os == "linux":
            return f'i=0\nwhile [ $i -lt {re.findall(REPEAT_PATTERN, line)[0]} ]\ndo'
        else:
            return f'for($i=0; $i -le {re.findall(REPEAT_PATTERN, line)[0]}; $i=$i+1)' + " {"
    else:
        return "err"
############ EXPORTED FUNCTIONS ###########

############ INTERNAL FUNCTIONS ###########
def get_condition(cond: str, os: str):
    if os == "linux":
        if "&&&" in cond:
            cond = cond.replace("&&&", " ] && [ ")
        if "|||" in cond:
            cond = cond.replace("|||", " ] || [ ")
    else:
        if "&&&" in cond:
            cond = cond.replace("&&&", "&&")
        if "|||" in cond:
            cond = cond.replace("|||", "||")
    return cond

############ INTERNAL FUNCTIONS ###########