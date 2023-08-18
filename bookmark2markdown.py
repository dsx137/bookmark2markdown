import re


# 对str进行转义操作，specialChars为需要转义的字符，默认替换所有特殊字符
def mdEscape(str, specialChars):
    l = specialChars
    if specialChars == None:
        l = re.findall("[^\w\s]", str)
    for i in l:
        str = str.replace(i, "\\" + i)
    return str


def FindAndWriteInFile(sourceFile, outputFile, spaceBetween, haveBlankLine):
    lines = sourceFile.readlines()
    for line in lines:
        hrefList = re.findall('<a href=".*?"', line, re.IGNORECASE)
        iconList = re.findall('icon=".*?"', line, re.IGNORECASE)
        titleList = re.findall(">[^>]+?</a>$", line, re.IGNORECASE)
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


bookmark_path = input("Input the bookmark file path:")
output_dir = input("Input the output file dir (the file named 'output.md'):")
spaceBetween = int(input("Input space number between icon and href:"))

haveBlankLine = input("Is there BlankLine between Lines? Y/N")
if haveBlankLine == "Y" or "y":
    haveBlankLine = True
elif haveBlankLine == "N" or "n":
    haveBlankLine = False
else:
    print("Error! And It will be false.")
    haveBlankLine = False

try:
    sourceFile = open(bookmark_path, mode="r", encoding="UTF-8")
except FileNotFoundError:
    print("File not found!")
    exit(0)

outputFile = open(output_dir + "/output.md", mode="w", encoding="UTF-8")
FindAndWriteInFile(sourceFile, outputFile, spaceBetween, haveBlankLine)
outputFile.close()
sourceFile.close()
