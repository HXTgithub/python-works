#读文件
def readFile(path, arg):
    try:
        file = open(path, arg, encoding="utf-8")
    except:
        file = open(path, 'w', encoding="utf-8")

    return file
#读文本中的单词
def readWords():
    file = readFile(path, 'r')
    while True:
        line = file.readline()
        if not line:
            break
        word = line.split(' ', 2)
        dict[word[0]] = word[1][:-1]
    file.close()

#单词写入文本
def writeFile(word, dsp):
    file = readFile(path, 'a')
    file.write('{} {}\n'.format(word, dsp))
    file.close()

#更新文件
def modifyFile(word, dsp):
    file = readFile(path, 'r')
    line = file.readlines()
    flen = len(line) - 1
    for i in range(flen):
        if word in line[i]:
            file.close()
            line[i] = '{} {}\n'.format(word, dsp)
            file = readFile(path, 'w')
            file.writelines(line)
            break
    file.close()

#修改单词
def editMode():
    print('*' * 50)
    print('*' * 50)
    while True:
        word = input("(按数字键退出)请输入想添加或修改的单词")
        if word in digits:
            print('*' * 50)
            print('*' * 50)
            return
        try:
            print("该单词已经存在,当前解释是：{}".format(dict[word]))
        except:
            print('您添加的是一个新单词')
        print("-----------------------")
        description = input("输入解释：\n")
        try:
            dict[word] += ',%s' % description
            modifyFile(word, dict[word])
        except KeyError:
            dict[word] = '%s' % description
            writeFile(word, dict[word])
        print('----------------添加完成---------------')
#查询单词
def searchMode():
    print('*' * 50)
    print('*' * 50)
    while True:
        word = input("(按数字键退出)想查的单词：")
        if word in digits:
            print('*' * 50)
            print('*' * 50)
            return
        print("-----------------------------------")
        try:
            print(dict[word])
        except KeyError:
            print('对不起，这个单词未收录')
        print("------------------------------------------")

if __name__ == '__main__':
    dict = {}
    digits = '0123456789'
    path = 'C:\\Users\\HXT\\Desktop\\danci.txt'
    readWords()

    while True:
        print("-------------欢迎使用-------------")
        print("1.查询单词\n2.添加单词\n3.退出\n")
        option = int(input("请输入选择："))
        if option==1:
            searchMode()
        elif option==2:
            editMode()
        else:
            exit()



