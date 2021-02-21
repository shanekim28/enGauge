import re

test = "<@!812637664159203328> ayy hello"
test2 = "ayy <@!812637664159203328> hello"
test3 = "<@&812637664159203328> ayy hello"

match = re.search("(?<=\<@)(.*)(?=\>)", test3)

userid = ""
if (match):
    userid = match.groups()[0]
    if (userid[0] == '&'):
        return

    if (userid[0] == '!'):
        userid = userid[1:]