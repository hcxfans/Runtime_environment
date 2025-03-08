import os
import re
import json
import string
import csv
import shutil



path1= r'.\cdfyword'  #首先定义文件夹的路径
path2= r'.\scfyword'  #首先定义文件夹的路径
path3= r'.\wz'  #首先定义文件夹的路径


path4= r'.\out'  #首先定义文件夹的路径
path5= r'.\json'

cdfile_names = os.listdir(path1) #创建一个所有文件名的列表
scfile_names = os.listdir(path2) #创建一个所有文件名的列表
testfile_names = os.listdir(path3) #创建一个所有文件名的列表

def getwordcodeinfo(testwd,tmp_dict):
    result=[]
    subcls_1=''
    subcls_2=''
    subcls_3=''
    subcls_4=''
    subcls_5=''
    wordcode=''
    wordinfo=''
    for key1 in tmp_dict.keys():
        sub_1_clsinfo=tmp_dict.get(key1).get('一级分类')
        sub_1_dict=tmp_dict.get(key1).get('data')
        for key2 in sub_1_dict.keys():
            sub_2_clsinfo=sub_1_dict[key2].get('二级分类')
            sub_2_dict=sub_1_dict[key2].get('data')
            for key3 in sub_2_dict.keys():
                sub_3_clsinfo=sub_2_dict[key3].get('三级分类')
                sub_3_dict=sub_2_dict[key3].get('data')
                for key4 in sub_3_dict.keys():
                    sub_4_clsinfo=sub_3_dict[key4].get('四级分类')
                    sub_4_dict=sub_3_dict[key4].get('data')
                    for key5 in sub_4_dict.keys():
                        wordlist=sub_4_dict[key5]
                        if testwd in wordlist:
                            wordcode=key1+':'+key2+':'+key3+':'+key4+':'+key5
                            wordinfo=sub_1_clsinfo+'->'+sub_2_clsinfo+'->'+sub_3_clsinfo+'->'+sub_4_clsinfo
                            result.append([wordcode,wordinfo])
    return result

def test_scgyword():
    testwordList=[]
    cdwordList=[]
    scwordList=[]
    tmp_dict={}
    xdhy_dict={}
    noinfo=[]
    with open(path5+'\\'+'myfile.json', encoding="utf-8") as f:
        tmp_dict= json.load(f)
    with open(path1+'\\'+cdfile_names[0], mode="r", encoding="utf-8") as f:
        for line in f.readlines():
            if line:
                wordinfoList= line.strip().rstrip().split("\t")#每一行按"\t"即Tab键分割成几部分
                if len(wordinfoList)>1:
                    word_sc=''+wordinfoList[1].strip().rstrip()
                    if word_sc:
                        cdwordList.append(word_sc)
    cdwordList=list(set(cdwordList))
    with open(path2+'\\'+scfile_names[0], mode="r", encoding="utf-8") as f:
        for line in f.readlines():
            if line:
                wordinfoList= line.strip().rstrip().split("\t")#每一行按"\t"即Tab键分割成几部分
                if len(wordinfoList)>1:
                    word_sc=''+wordinfoList[1].strip().rstrip()
                    if word_sc:
                        scwordList.append(word_sc)
    scwordList=list(set(scwordList))

    noinfo=[]
    print('四川方言词典总共有'+str(len(scwordList))+'个词语等待测试！')
    print('现在测试四川方言词典里每个词语的语义分类情况，可能需要较长时间，请耐心等待.......')
    for mword in scwordList:
        if not getwordcodeinfo(mword,tmp_dict):
            noinfo.append(mword+'\n')
    print('总共有'+str(len(noinfo))+'个四川方言词典里的词语不在现代汉语分类词典里！具体词语已保存到 现代汉语分类词典没有的四川方言词典词语.txt文件!')
    with open(path4+'\\'+'现代汉语分类词典没有的四川方言词典词语.txt',"w",encoding="utf-8") as tf:
            tf.writelines(noinfo)

    noinfo=[]
    print('成都方言词典总共有'+str(len(cdwordList))+'个词语等待测试！')
    print('现在测试成都方言词典里每个词语的语义分类情况，可能需要较长时间，请耐心等待.......')
    for mword in cdwordList:
        if not getwordcodeinfo(mword,tmp_dict):
            noinfo.append(mword+'\n')
    print('总共有'+str(len(noinfo))+'个成都方言词典里的词语不在现代汉语分类词典里！具体词语已保存到 现代汉语分类词典没有的成都方言词典词语.txt文件!')
    with open(path4+'\\'+'现代汉语分类词典没有的成都方言词典词语.txt',"w",encoding="utf-8") as tf:
            tf.writelines(noinfo)

    noinfo=[]
    print('四川方言词典总共有'+str(len(scwordList))+'个词语等待测试是否在成都方言词典里！')
    print('现在测试四川方言词典里每个词语是否出现在成都方言词典里，可能需要较长时间，请耐心等待.......')
    for mword in scwordList:
        if mword not in cdwordList:
            noinfo.append(mword+'\n')
    print('总共有'+str(len(noinfo))+'个四川方言词典里的词语不在成都方言词典里！具体词语已保存到 成都方言词典没有的四川方言词典词语.txt文件!')
    with open(path4+'\\'+'成都方言词典没有的四川方言词典词语.txt',"w",encoding="utf-8") as tf:
            tf.writelines(noinfo)

    noinfo=[]
    print('成都方言词典总共有'+str(len(cdwordList))+'个词语等待测试是否在四川方言词典里！')
    print('现在测试成都方言词典里每个词语是否出现在四川方言词典里，可能需要较长时间，请耐心等待.......')
    for mword in cdwordList:
        if mword not in scwordList:
            noinfo.append(mword+'\n')
    print('总共有'+str(len(noinfo))+'个成都方言词典里的词语不在四川方言词典里！具体词语已保存到 四川方言词典没有的成都方言词典词语.txt文件!')
    with open(path4+'\\'+'四川方言词典没有的成都方言词典词语.txt',"w",encoding="utf-8") as tf:
            tf.writelines(noinfo)
    

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
    incdwordLines=['四川方言词典的以下词语出现在成都方言词典里：\n']
    outcdwordLines=['四川方言词典的以下词语未出现在成都方言词典里：\n']
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


test_scgyword()
    
        
