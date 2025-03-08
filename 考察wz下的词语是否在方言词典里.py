import os
import re
import json
import string
import csv
import shutil



path1= r'.\cdfycd'  #首先定义文件夹的路径
path2= r'.\scfycd'  #首先定义文件夹的路径
path3= r'.\wz'  #首先定义文件夹的路径

path4= r'.\out'  #首先定义文件夹的路径

cdfile_names = os.listdir(path1) #创建一个所有文件名的列表
scfile_names = os.listdir(path2) #创建一个所有文件名的列表
testfile_names = os.listdir(path3) #创建一个所有文件名的列表


if not os.path.exists(path4):
    os.mkdir(path4)





for name in testfile_names:
    print("正在处理"+name+"文件,请稍候......")
    testwordList=[]
    with open(path3+'\\'+name, mode="r", encoding="utf-8") as f:
        for line in f.readlines():
            line=line.strip().rstrip()
            if line:
                testwordList.append(line)
    cdwordList=[]
    with open(path1+'\\'+cdfile_names[0], mode="r", encoding="utf-8") as f:
        for line in f.readlines():
            if line:
                wordinfoList= line.strip().rstrip().split("\t")#每一行按"\t"即Tab键分割成几部分
                if len(wordinfoList)>1:
                    word_sc=''+wordinfoList[0].strip().rstrip()
                    if word_sc:
                        cdwordList.append(word_sc)
    scwordList=[]
    with open(path2+'\\'+scfile_names[0], mode="r", encoding="utf-8") as f:
        for line in f.readlines():
            if line:
                wordinfoList= line.strip().rstrip().split("\t")#每一行按"\t"即Tab键分割成几部分
                if len(wordinfoList)>1:
                    word_sc=''+wordinfoList[0].strip().rstrip()
                    if word_sc:
                        scwordList.append(word_sc)
    incdwordLines=['以下词语出现在成都方言词典里：\n']
    outcdwordLines=['以下词语未出现在成都方言词典里：\n']
    for testword in testwordList:
        if testword in cdwordList:
            incdwordLines.append(testword+'\n')
        else:
            outcdwordLines.append(testword+'\n')
    inscwordLines=['以下词语出现在四川方言词典里：\n']
    outscwordLines=['以下词语未出现在四川方言词典里：\n']
    for testword in testwordList:
        if testword in scwordList:
            inscwordLines.append(testword+'\n')
        else:
            outscwordLines.append(testword+'\n')
    insccdwordLines=['以下词语在四川方言词典和成都方言词典里均有出现：\n']
    outsccdwordLines=['以下词语在四川方言词典和成都方言词典里均未出现：\n']
    inscoutcdwordLines=['以下词语在四川方言词典里出现但在成都方言词典里未出现：\n']
    outscincdwordLines=['以下词语在四川方言词典里未出现但在成都方言词典里出现：\n']
    for testword in testwordList:
        if testword in scwordList and testword in cdwordList:
            insccdwordLines.append(testword+'\n')
        elif (not testword in scwordList) and (not testword in cdwordList):
            outsccdwordLines.append(testword+'\n')
        elif (not testword in scwordList) and testword in cdwordList:
            outscincdwordLines.append(testword+'\n')
        elif testword in scwordList and (not testword in cdwordList):
            inscoutcdwordLines.append(testword+'\n')
    with open(path4+'\\'+'成都方言词典里出现的词语.txt',"w",encoding="utf-8") as tf:
            tf.writelines(incdwordLines)
    with open(path4+'\\'+'未出现在成都方言词典里的词语.txt',"w",encoding="utf-8") as tf:
            tf.writelines(outcdwordLines)
    with open(path4+'\\'+'四川方言词典里出现的词语.txt',"w",encoding="utf-8") as tf:
            tf.writelines(inscwordLines)
    with open(path4+'\\'+'未出现在四川方言词典里的词语.txt',"w",encoding="utf-8") as tf:
            tf.writelines(outscwordLines)
    with open(path4+'\\'+'四川方言词典和成都方言词典均有出现的词语.txt',"w",encoding="utf-8") as tf:
            tf.writelines(insccdwordLines)
    with open(path4+'\\'+'四川方言词典和成都方言词典均未出现的词语.txt',"w",encoding="utf-8") as tf:
            tf.writelines(outsccdwordLines)
    with open(path4+'\\'+'四川方言词典里出现但在成都方言词典里未出现的词语.txt',"w",encoding="utf-8") as tf:
            tf.writelines(inscoutcdwordLines)
    with open(path4+'\\'+'四川方言词典里未出现但在成都方言词典里出现的词语.txt',"w",encoding="utf-8") as tf:
            tf.writelines(outscincdwordLines)



    
        
