import re


# 对str进行转义操作，specialChars为需要转义的字符，默认替换所有特殊字符
def mdEscape(str, specialChars):
    l = specialChars
    if specialChars == None:
        l = re.findall("[^\w\s]", str)
    for i in l:
        str = str.replace(i, "\\" + i)
    return str


def FindAndWriteInFile(sourceFile, outputFile, spaceBetween):
    lines = sourceFile.readlines()
    tab_count = 0
    for line in lines:
        mdFileLine = ""
        # read until <DL><P>
        if re.findall("<DL><P>", line, re.IGNORECASE):
            tab_count += 1
            continue
        elif re.findall("</DL><P>", line, re.IGNORECASE):
            tab_count -= 1
            continue
        else:
            titleList = re.findall(">[^>]+?</H", line, re.IGNORECASE)
            if titleList:
                mdFileLine += ("  " * tab_count) + "+ "
                title = mdEscape(titleList[0][1 : len(titleList[0]) - 3], "[]|")
                mdFileLine += title
            else:
                hrefList = re.findall('<a href=".*?"', line, re.IGNORECASE)
                iconList = re.findall('icon=".*?"', line, re.IGNORECASE)
                titleList = re.findall(">[^>]+?</a>$", line, re.IGNORECASE)

                if titleList:
                    mdFileLine += ("  " * tab_count) + "+ "
                    title = mdEscape(titleList[0][1 : len(titleList[0]) - 4], "[]|")
                    if iconList:
                        icon = iconList[0][6 : len(iconList[0]) - 1]
                        mdFileLine += "![image](" + icon + ")" + ("&nbsp;" * spaceBetween)
                    if hrefList:
                        href = hrefList[0][9 : len(hrefList[0]) - 1]
                        mdFileLine += "[" + title + "]" + "(" + href + ")"

        if mdFileLine != "":
            mdFileLine += "\n"
            outputFile.write(mdFileLine)


bookmark_path = input("Input the bookmark file path:\n")
output_dir = input("Input the output file dir (the file named 'output.md'):\n")
spaceBetween = int(input("Input space number between icon and href:\n"))

try:
    sourceFile = open(bookmark_path, mode="r", encoding="UTF-8")
except FileNotFoundError:
    print("File not found!")
    exit(0)

outputFile = open(output_dir + "/output.md", mode="w", encoding="UTF-8")
FindAndWriteInFile(sourceFile, outputFile, spaceBetween)
outputFile.close()
sourceFile.close()
