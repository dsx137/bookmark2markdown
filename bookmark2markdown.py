import re

# 对str进行转义操作，specialChars为需要转义的字符，默认替换所有特殊字符
def mdEscape(str, specialChars):
    l = specialChars
    if specialChars == None:
        l = re.findall("[^\w\s]", str)
    for i in l:
        str = str.replace(i, "\\" + i)
    return str


def FindAndWriteInFile(file, spaceBetween, haveBlankLine):
    outputFile = open("output.md", mode="w", encoding="UTF-8")
    lines = file.readlines()
    for line in lines:
        hrefList = re.findall('<a href=".*?"', line)
        iconList = re.findall('icon=".*?"', line)
        titleList = re.findall(">[^>]+?</a>$", line)
        mdFileLine = ""
        if titleList:
            title = mdEscape(titleList[0][1 : len(titleList[0]) - 4], "[]|")
            if iconList:
                icon = iconList[0][6 : len(iconList[0]) - 1]
                mdFileLine += "![image](" + icon + ")" + ("&nbsp;" * spaceBetween)
            if hrefList:
                href = hrefList[0][9 : len(hrefList[0]) - 1]
                mdFileLine += "[" + title + "]" + "(" + href + ")"
            if mdFileLine != "":
                mdFileLine += "\n\n" if haveBlankLine else "\\\n"
            outputFile.write(mdFileLine)


# path = input("Input the file path:")
path = "bookmark.html"
spaceBetween = int(input("Input spaces between icon and href:"))

haveBlankLine = input("Is there BlankLine between Lines? Y/N")
if haveBlankLine == "Y" or "y":
    haveBlankLine = True
elif haveBlankLine == "N" or "n":
    haveBlankLine = False
else:
    print("Error! And It will be false.")
    haveBlankLine = False

file = open(path, mode="r", encoding="UTF-8")
FindAndWriteInFile(file, spaceBetween, haveBlankLine)
