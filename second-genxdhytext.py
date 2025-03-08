import os
import re
import json
import string
import csv
import shutil

dxzwsz='壹贰叁肆伍陆柒捌玖拾'
dxszlist=list(dxzwsz)
xxzwsz='一二三四五六七八九十'
xxszlist=list(xxzwsz)
Upchar='ABCDEFGHIJGKLMNOPQRSTUVWXYZ'
uplist=list(Upchar)
Lowerchar='abcdefghijgklmnopqrstuvwxyz'
lowerlist=list(Lowerchar)
ywzmlist=uplist+lowerlist
albsz='1234567890'
albszlist=list(albsz)

def substring_before(s, delim):
    if not s:
        return ''
    if delim in s:
        return s.partition(delim)[0]
    else:
        return s
def substring_after(s, delim):
    if not s:
        return ''
    if delim in s:
        return s.partition(delim)[2]
    else:
        return ''
def check_nopinyin(word):
    for i in range(len(word)):
        if word[i] in ywzmlist:
            return False
    return True
def get_onlyword(word):
    if '\\u' in word:
        print(word)
        return word
    mword=''
    for i in range(len(word)):
        if word[i] not in albszlist:
            mword=mword+word[i]
    return mword
    
def split_word(word):#处理词语带括号及括号里有顿号情况
    wordList=[]
    word1=substring_before(word, '(')
    
    wordother=substring_after(word, '(')
    if word1:
        if check_nopinyin(wordother):
            wordList.append(word1)
        else:
            
            wordList.append(word)
            print(wordList)
            return wordList
    if wordother and check_nopinyin(wordother):
        wordother=substring_before(wordother, ')')
        wordotherlist=wordother.strip().rstrip().split("、")
        wordList.extend(wordotherlist)
    #print(wordList)    
    return wordList
def save_scgyword(path1,path2):
        """
        从参数path字符串对应的txt文件里读取四川方言词汇、对应普通话词汇、四川方言例句，分别形成三个list并返回
        """
        newlines=[]
        with open(path1, mode="r", encoding="utf-8") as f:
            for line in f.readlines():
                if line:
                    wordinfoList= line.strip().rstrip().split("\t")#每一行按"\t"即Tab键分割成几部分
                    if len(wordinfoList)>1:
                        word_sc=''+wordinfoList[0]
                        word_gy=''+wordinfoList[1]
                        if '(' in word_gy:
                            print(line)
                        newlines.append(word_sc+'\t'+word_gy+'\n')
        with open(path2,"w",encoding="utf-8") as tf:
            tf.writelines(newlines)
        return newlines
def load_data(path,tmp_dict):
        """
        从参数path字符串对应的txt文件里读取四川方言词汇、对应普通话词汇、四川方言例句，分别形成三个list并返回
        """
        tmpdict={}
        newlines=[]
        wordinfoList=[]
        sc = []
        gy = []
        with open(path, mode="r", encoding="utf-8") as f:
            for line in f.readlines():
                if line:
                    wordinfoList= line.strip().rstrip().split("\t")#每一行按"\t"即Tab键分割成几部分
                    if len(wordinfoList)>1:
                        word_sc=''+wordinfoList[0].strip().rstrip()
                        word_gy=''+wordinfoList[1].strip().rstrip()
                        if '。' in word_gy:
                            word_gy=word_gy.replace('。','')
                        word_scList=split_word(word_sc)
                        if word_scList:
                            for i in range(len(word_scList)):
                                word_sc=''+word_scList[i]
                                newlines.append(word_sc+'\t'+word_gy+'\n')
                    else:
                        print('error:该行不完整:'+line)
        lines=newlines
        newlines = []
        newline=''
        lcount=len(lines)
        for i in range(lcount):
            wordinfoList= lines[i].strip().rstrip().split("\t")
            mword=get_onlyword(wordinfoList[0])
            #print(mword)
            gyword=tmpdict.get(mword)
            if not gyword:
                if len(wordinfoList)>1:
                    if getwordcodeinfo(wordinfoList[1],tmp_dict):
                        tmpdict.update({mword:wordinfoList[1]})
                    else:
                        print('error:查不到义类编码信息:'+lines[i])
                else:
                    print('error:该行不完整:'+lines[i])
        return tmpdict
def save_data(zone,cdfy_dict,xdhy_dict):
    newlines=[]
    cdcodeinfo_dict={}
    newlines.append('zone'+'\t'+'word'+'\t'+'code'+'\t'+'Sub_class1'+'\t'+'Sub_class2'+'\t'+'Sub_class3'+'\t'+'Origin'+'\n')
    for key in cdfy_dict.keys():
        #sub_1_clsinfo=tmp_dict.get(key1).get('一级分类')
        cdcode=getcdwordcodeinfo(key,cdfy_dict,xdhy_dict)
        if not cdcodeinfo_dict.get(cdcode[0]):
            cdcodeinfo_dict.update({cdcode[0]:cdcode[1]})
        codeinfoList=cdcode[1].split('->')
        origin='大陆'
        newlines.append(zone+'\t'+key+'\t'+cdcode[0]+'\t'+codeinfoList[0]+'\t'+codeinfoList[1]+'\t'+codeinfoList[2]+'\t'+origin+'\n')
        
    return cdcodeinfo_dict,newlines
def save_cdcodedata(cdfy_dict,xdhy_dict):
    cdcode_dict={}
    cdcodestr_dict={}
    
    for key in cdfy_dict.keys():
        #sub_1_clsinfo=tmp_dict.get(key1).get('一级分类')
        cdcode=getcdwordcodeinfo(key,cdfy_dict,xdhy_dict)
        cdwordList=cdcode_dict.get(cdcode[0])
        cdwordstr=cdcodestr_dict.get(cdcode[0])
        if cdwordList:
            cdwordList.append(key)
            cdcode_dict.update({cdcode[0]:cdwordList})
            cdcodestr_dict.update({cdcode[0]:cdwordstr+'、'+key})
        else:
            cdwordList=[]
            cdwordList.append(key)
            cdcode_dict.update({cdcode[0]:cdwordList})
            cdcodestr_dict.update({cdcode[0]:key})
        #newlines.append(key+'\t'+cdcode[0]+'\t'+cdcode[1]+'\n')
        
    return cdcode_dict,cdcodestr_dict
def dict_to_doc(path,cdcodestr_dict):
    newlines=[]
    with open(path, mode="r", encoding="utf-8") as f:
            for line in f.readlines():
                line=line.strip().rstrip()
                if line:
                    newlines.append(line+'\n')
                    if line and len(line)>5:
                        codestr=''+line[-5]+line[-4]+line[-3]+line[-2]+line[-1]
                        codestr=codestr.strip().rstrip()
                        if codestr:
                            tmpinfo=cdcodestr_dict.get(codestr)
                            if tmpinfo:
                                tmpinfo=tmpinfo.strip().rstrip()
                                if tmpinfo:
                                    newlines.append(tmpinfo+'\n')
    
    return newlines
def init_cdfl_count(path):
    code_count_dict={}
    with open(path, mode="r", encoding="utf-8") as f:
            for line in f.readlines():
                line=line.strip().rstrip()
                if line and len(line)>5:
                        codestr=''+line[-5]+line[-4]+line[-3]+line[-2]+line[-1]
                        codestr=codestr.strip().rstrip()
                        if codestr:
                            code_count_dict.update({codestr:0})
    
    return code_count_dict
def fycd_cdfl_count(code_count_dict,cdcode_dict):
    for key3 in cdcode_dict.keys():#获取三分类的词语个数
        sub_count=len(cdcode_dict.get(key3))
        code_count_dict.update({key3:sub_count})
    for key2 in code_count_dict.keys():
        if key2[4]=='0' and key2[3]=='0' and not (key2[2]=='0'and key2[1]=='0'):#key2是二分类，计算二分类的词语个数
           sub_count=0
           for tmp_key in code_count_dict.keys():
               if not (tmp_key[4]=='0' and tmp_key[3]=='0') and key2[2]==tmp_key[2]  and key2[1]==tmp_key[1] and key2[0]==tmp_key[0]:
                   sub_count=sub_count+code_count_dict[tmp_key]
           code_count_dict.update({key2:sub_count})
    for key1 in code_count_dict.keys():
        if key1[4]=='0' and key1[3]=='0' and key1[2]=='0'and key1[1]=='0':#key1是一分类，计算一分类的词语个数
           #print('ok 1')
           sub_count=0
           for tmp_key in code_count_dict.keys():
               if tmp_key[4]=='0' and tmp_key[3]=='0' and not (tmp_key[2]=='0'and tmp_key[1]=='0') and key1[0]==tmp_key[0]:
                   #print('ok 2')
                   sub_count=sub_count+code_count_dict[tmp_key]
           code_count_dict.update({key1:sub_count})
    return code_count_dict   
def getwordcodeinfo(testwd,tmp_dict):
#def wordinsubsubdict(testwd,jsonfile):
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
                            #print(testwd+'的分类编码为：'+wordcode)
                            #print(testwd+'的分类信息为：'+wordinfo)
    #print(testwd)
    #print(result)
    return result
def getcdcodeinfo(xdhycdinfo):
    xdhycode=xdhycdinfo[0].split(':')
    #print(xdhycode)
    
    xdhyinfo=xdhycdinfo[1].split('->')
    #xdhyinfo=xdhycdinfo[1]
    sub1c={'壹':'1','贰':'2','叁':'3','肆':'4','伍':'5','陆':'6','柒':'7','捌':'8','玖':'9'}
    sub2c={'一':'01','二':'02','三':'03','四':'04','五':'05','六':'06','七':'07','八':'08','九':'09','十':'10','十一':'11','十二':'12','十三':'13','十四':'14'}
    cdfycode=''+sub1c[xdhycode[0]]+sub2c[xdhycode[1]]
    sub3cindex=ord(xdhycode[2])-ord('A')+1
    if sub3cindex>=0 and sub3cindex<10:
        sub3c='0'+chr(ord('0')+sub3cindex)
    else:
        sub3c=str(sub3cindex)
    #print(''+sub1c[xdhycode[0]]+sub2c[xdhycode[1]]+sub3c)
    #print(xdhyinfo[0]+'->'+xdhyinfo[1]+'->'+xdhyinfo[2])
   
    return [''+sub1c[xdhycode[0]]+sub2c[xdhycode[1]]+sub3c,xdhyinfo[0]+'->'+xdhyinfo[1]+'->'+xdhyinfo[2]]
    
def getcdwordcodeinfo(testwd,sc_dict,xdhy_dict):
    tmpcodeinfo=getwordcodeinfo(sc_dict.get(testwd),xdhy_dict)
    #print(testwd)
    #print(tmpcodeinfo)
    xdhycdinfo=tmpcodeinfo[0]
    
    return getcdcodeinfo(xdhycdinfo)

def get_code_word_csv(codeword_dict):
    newlines = []
    for key1 in codeword_dict.keys():
        wordList=codeword_dict.get(key1)
        #print(codeword_dict.get(key1))
        if wordList:
            for i in range(len(wordList)):
                newlines.append(key1+'\t'+wordList[i]+'\n')
        #else:
        #    print(key1+'分类没有任何词语！')
    return newlines

path1= r'.\scfycd'  #首先定义文件夹的路径
path2= r'.\scfyword'  #首先定义文件夹的路径
path6= r'.\tmp'  #首先定义文件夹的路径
path3= r'.\test'  #首先定义文件夹的路径
path4= r'.\out'  #首先定义文件夹的路径
path5= r'.\json'
path7= r'.\oneword'
path8= r'.\head'
path9= r'.\cdfycd'  #首先定义文件夹的路径
file_names_sc = os.listdir(path1) #创建一个所有文件名的列表
file_names_cd = os.listdir(path9) #创建一个所有文件名的列表

if not os.path.exists(path2):
    os.mkdir(path2)
if not os.path.exists(path4):
    os.mkdir(path4)
if not os.path.exists(path5):
    os.mkdir(path5)

with open(path5+'\\'+'myfile.json', encoding="utf-8") as f:
    tmp_dict= json.load(f)

for name in file_names_sc :
    print("正在处理"+name+"文件,请稍候......")
    
    save_scgyword(path1+'\\'+name,path2+'\\'+name)
    with open(path2+'\\'+name, encoding="utf-8") as f:
        mtmpdict=load_data(path2+'\\'+name,tmp_dict)
        with open(path5+'\\'+'myscfile.json', 'w', encoding ='utf8') as json_file:
            json.dump(mtmpdict, json_file, ensure_ascii = False,indent = 6)

for name in file_names_cd:
    print("正在处理"+name+"文件,请稍候......")    
    save_scgyword(path9+'\\'+name,path2+'\\'+name)
    with open(path2+'\\'+name, encoding="utf-8") as f:
        mtmpdict=load_data(path2+'\\'+name,tmp_dict)
        with open(path5+'\\'+'mycdfile.json', 'w', encoding ='utf8') as json_file:
            json.dump(mtmpdict, json_file, ensure_ascii = False,indent = 6)

xdhy_dict={}

with open(path5+'\\'+'myfile.json', encoding="utf-8") as f:
    xdhy_dict= json.load(f)
xdfy_dict={}
with open(path5+'\\'+'myxdfile.json', encoding="utf-8") as f:
    xdfy_dict= json.load(f)
code_count_dict=init_cdfl_count(path8+'\\header.txt')
print('现在生成词语的义类情况，词语较多可能需要较长时间，请耐心等待.......')
xdcodeinfo_dict,newlines=save_data('大陆',xdfy_dict,xdhy_dict)
#xdcodeinfo_dict=dict(sorted(xdcodeinfo_dict.items(), key=lambda x: x[0],reverse=False))
with open(path5+'\\'+'myxdcodeinfofile.json', 'w', encoding ='utf8') as json_file:
    json.dump(xdcodeinfo_dict, json_file, ensure_ascii = False,indent = 6)
with open(path4+'\\'+'现代汉语词汇义类编码文本.csv',"w",encoding="utf-8") as tf:
    tf.writelines(newlines)


    
        
