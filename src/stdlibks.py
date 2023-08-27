'''
Handles Input Output/File system reading/writing
'''

############ IMPORTS ############
import re
############ IMPORTS ############


############ EXPORTED FUNCTIONS ###########

def Display_fn(line: str, os: str):

    ##### TOKENS #####
    DISPLAY_PATTERN = "^Display\s*\(\s*\"(.*?)\"\s*\)"
    DISPLAY_PATTERN_NONEWLINE = "^Display\s*\(\s*no\s+new\s+line\s*\s*\"(.*?)\"\s*\)"
    DISPLAY_PATTERN_LITERAL = "^Display\s*\(\s*literal\s*\"(.*?)\"\s*\)"
    DISPLAY_PATTERN_LITERALNONEWLINE = "^Display\s*\(\s*literal\s+no\s+new\s+line\s*\"(.*?)\"\s*\)"
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

############ EXPORTED FUNCTIONS ###########
