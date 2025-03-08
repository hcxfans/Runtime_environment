import os
import re
import json
import string
import csv
import shutil

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
                            wordcode=key1+key2+key3+key4+key5
                            wordinfo=sub_1_clsinfo+'->'+sub_2_clsinfo+'->'+sub_3_clsinfo+'->'+sub_4_clsinfo
                            result.append((wordcode,wordinfo))
                            #print(testwd+'的分类编码为：'+wordcode)
                            #print(testwd+'的分类信息为：'+wordinfo)
    return result

path1= r'.\test'  #首先定义文件夹的路径
path6= r'.\tmp'  #首先定义文件夹的路径
path3= r'.\test'  #首先定义文件夹的路径
path4= r'.\out'  #首先定义文件夹的路径
path5= r'.\json'
file_names = os.listdir(path1) #创建一个所有文件名的列表


dxzwsz='壹贰叁肆伍陆柒捌玖拾'
dxszlist=list(dxzwsz)
xxzwsz='一二三四五六七八九十'
xxszlist=list(xxzwsz)
Upchar='ABCDEFGHIJGKLMNOPQRSTUVWXYZ'
uplist=list(Upchar)
Lowerchar='abcdefghijgklmnopqrstuvwxyz'
lowerlist=list(Lowerchar)
albsz='1234567890'
albszlist=list(albsz)

if not os.path.exists(path4):
    os.mkdir(path4)
if not os.path.exists(path5):
    os.mkdir(path5)
wf1=open(path4+'\\'+'deltext.txt',"w",encoding="utf-8")
wf1.close()
wf1=open(path4+'\\'+'tmptext.txt',"w",encoding="utf-8")
wf1.close()
wf1=open(path4+'\\'+'info.txt',"w",encoding="utf-8")
wf1.close()
#wf1=open(path4+'\\'+'nointext.txt',"w",encoding="utf-8")
#wf1.close()
wnoin=set()
#wf4=open(path4+'\\'+"url_list.txt","w",encoding="utf-8")
#wf4.close()


wordlist=[]
xdhylines=[]
for name in file_names:
    print("正在处理"+name+"文件,请稍候......")
    #fnamelist=name.split('.')
    #wf_chat=open(path6+'\\'+fnamelist[0]+".chat","w",encoding="utf-8")
    #wf_chat.close()
    sub_1_dict={}
    sub_1_1_dict={}
    sub_2_dict={}
    sub_2_1_dict={}
    sub_3_dict={}
    sub_3_1_dict={}
    sub_4_dict={}
    sub_4_1_dict={}
    sub_5_dict={}
    pre_subcls_1=''
    pre_subcls_2=''
    pre_subcls_3=''
    pre_subcls_4=''
    pre_subcls_5=''
    subcls_1=''
    subcls_2=''
    subcls_3=''
    subcls_4=''
    subcls_5=''
    pre_tmpinfo_1=''
    pre_tmpinfo_2=''
    pre_tmpinfo_3=''
    pre_tmpinfo_4=''
    tmpinfo_1=''
    tmpinfo_2=''
    tmpinfo_3=''
    tmpinfo_4=''
    
    with open(path1+'\\'+name, encoding="utf-8") as f:
        lines=f.readlines()
        lineNo=1
        newlines=[]
        tmplines=[]
        for i in range(len(lines)):
        #for line in lines:
            line=lines[i]
            line=line.strip().rstrip()
            if line:
                #去掉原始文档页眉的编码范围和页码
                if len(line)>6 and line[0] in dxszlist and line[1] in xxszlist:
                    with open(path4+'\\'+'deltext.txt',"a+",encoding="utf-8") as tf:
                        tf.write(line+'\n')
                    
                elif len(line)>6 and line[-6] in dxszlist and line[-5] in xxszlist:
                    with open(path4+'\\'+'deltext.txt',"a+",encoding="utf-8") as tf:
                        tf.write(line+'\n')
                    
                elif len(line)>7 and line[-7] in dxszlist and line[-6] in xxszlist:
                    with open(path4+'\\'+'deltext.txt',"a+",encoding="utf-8") as tf:
                        tf.write(line+'\n')
                elif line[0] in dxszlist:
                    if lines[i+1][0] not in xxszlist:
                        print('error:大写数字后面不是小写:'+line)
                    subcls_1=line[0]
                    tmpinfo=substring_after(line, subcls_1)
                    if pre_tmpinfo_1:#保存已经处理完毕的一级分类数据
                        if sub_5_dict:
                            sub_4_1_dict={}
                            sub_4_1_dict.update({'四级分类':pre_tmpinfo_4})
                            sub_4_1_dict.update({'data':sub_5_dict})
                            sub_4_dict.update({pre_subcls_4:sub_4_1_dict})                    
                        tdict=sorted(sub_4_dict.items(), key=lambda kv: kv[0])
                        sub_4_dict=dict(tdict)
                        
                        if sub_4_dict:
                            sub_3_1_dict={}
                            sub_3_1_dict.update({'三级分类':pre_tmpinfo_3})
                            sub_3_1_dict.update({'data':sub_4_dict})
                            sub_3_dict.update({pre_subcls_3:sub_3_1_dict})
                        tdict=sorted(sub_3_dict.items(), key=lambda kv: kv[0])
                        sub_3_dict=dict(tdict)
                        
                        if sub_3_dict:
                            sub_2_1_dict={}
                            sub_2_1_dict.update({'二级分类':pre_tmpinfo_2})
                            sub_2_1_dict.update({'data':sub_3_dict})
                            sub_2_dict.update({pre_subcls_2:sub_2_1_dict})

                        if sub_2_dict:
                            sub_1_1_dict={}
                            sub_1_1_dict.update({'一级分类':pre_tmpinfo_1})
                            sub_1_1_dict.update({'data':sub_2_dict})
                            sub_1_dict.update({pre_subcls_1:sub_1_1_dict})
                        #print(sub_1_dict)
                    sub_5_dict={}
                    sub_4_dict={}
                    sub_3_dict={}
                    sub_2_dict={}
                    pre_subcls_1=subcls_1
                    pre_tmpinfo_1=tmpinfo
                    newlines.append(line+'\n')
                elif line[0] in xxszlist:
                    if lines[i+1][0] not in uplist:
                        print('error:小写数字后面不是大写字母:'+line)
                    subcls_2=substring_before(line, '、')
                    tmpinfo=substring_after(line, '、')
                    if pre_tmpinfo_2:#保存已经处理完毕的二级分类数据
                        #print(pre_subcls_2+pre_tmpinfo_2)
                        if sub_5_dict:
                            sub_4_1_dict={}
                            sub_4_1_dict.update({'四级分类':pre_tmpinfo_4})
                            sub_4_1_dict.update({'data':sub_5_dict})
                            sub_4_dict.update({pre_subcls_4:sub_4_1_dict})                    
                        tdict=sorted(sub_4_dict.items(), key=lambda kv: kv[0])
                        sub_4_dict=dict(tdict)
                        
                        if sub_4_dict:
                            sub_3_1_dict={}
                            sub_3_1_dict.update({'三级分类':pre_tmpinfo_3})
                            sub_3_1_dict.update({'data':sub_4_dict})
                            sub_3_dict.update({pre_subcls_3:sub_3_1_dict})
                        tdict=sorted(sub_3_dict.items(), key=lambda kv: kv[0])
                        sub_3_dict=dict(tdict)
                        
                        if sub_3_dict:
                            sub_2_1_dict={}
                            sub_2_1_dict.update({'二级分类':pre_tmpinfo_2})
                            sub_2_1_dict.update({'data':sub_3_dict})
                            sub_2_dict.update({pre_subcls_2:sub_2_1_dict})
                        
                        
                        #if wordinsubsubdict('原子弹',sub_3_dict):
                        #    print(sub_2_dict)
                        #if tmpinfo=='建筑物':
                        #    print(sub_2_dict)
                        #print(sub_2_dict)
                    sub_5_dict={}
                    sub_4_dict={}
                    sub_3_dict={}
                    pre_subcls_2=subcls_2
                    pre_tmpinfo_2=tmpinfo
                    newlines.append(line+'\n')
                elif line[0] in uplist:
                    if lines[i+1][0] not in lowerlist:
                        print('error:大写字母后面不是小写字母:'+line)
                    subcls_3=line[0]#新的三级分类开始
                    tmpinfo=substring_after(line, subcls_3)
                    if pre_tmpinfo_3:#保存已经处理完毕的三级分类数据
                        if sub_5_dict:
                            sub_4_1_dict={}
                            sub_4_1_dict.update({'四级分类':pre_tmpinfo_4})
                            sub_4_1_dict.update({'data':sub_5_dict})
                            sub_4_dict.update({pre_subcls_4:sub_4_1_dict})                    
                        tdict=sorted(sub_4_dict.items(), key=lambda kv: kv[0])
                        sub_4_dict=dict(tdict)
                        
                        if sub_4_dict:
                            sub_3_1_dict={}
                            sub_3_1_dict.update({'三级分类':pre_tmpinfo_3})
                            sub_3_1_dict.update({'data':sub_4_dict})
                            sub_3_dict.update({pre_subcls_3:sub_3_1_dict})
                        tdict=sorted(sub_3_dict.items(), key=lambda kv: kv[0])
                        sub_3_dict=dict(tdict)
                        

                        
                        tmpname=subcls_1+'_'+subcls_2+'_'+pre_subcls_3
                        
                        #with open(path5+'\\'+tmpname+'.json', 'w', encoding ='utf8') as json_file:
                        #    json.dump(sub_3_1_dict, json_file, ensure_ascii = False,indent = 6)
                        #if wordinsubdict('原子弹',sub_4_dict):
                        #    print(sub_3_dict)
                        #print(sub_3_dict)
                    sub_5_dict={}
                    sub_4_dict={}
                    pre_subcls_3=subcls_3
                    pre_tmpinfo_3=tmpinfo
                    newlines.append(line+'\n')
                elif line[0] in lowerlist:#新的四级分类开始
                    if lines[i+1][0] not in albszlist:
                        print('error:小写字母后面不是阿拉伯数字:'+line)
                    subcls_4=line[0]
                    tmpinfo=substring_after(line, subcls_4)
                    
                    if pre_tmpinfo_4:#保存已经处理完毕的四级分类数据
                        #print(pre_tmpinfo_4)
                        
                        
                        if sub_5_dict:
                            sub_4_1_dict={}
                            sub_4_1_dict.update({'四级分类':pre_tmpinfo_4})
                            sub_4_1_dict.update({'data':sub_5_dict})
                            sub_4_dict.update({pre_subcls_4:sub_4_1_dict})
                        
                        tdict=sorted(sub_4_dict.items(), key=lambda kv: kv[0])
                        sub_4_dict=dict(tdict)
                        
                    sub_5_dict={}
                    pre_subcls_4=subcls_4
                    pre_tmpinfo_4=tmpinfo
                    newlines.append(line+'\n')
                elif line[0] in albszlist:
                    if line.count('0')>1 or ('11' not in line and line.count('1')>1) or ('22' not in line and line.count('2')>1) or ('33' not in line and line.count('3')>1):
                        print('error:'+line)
                    if len(line)<3:
                        print('第'+str(lineNo)+"行-error:"+line)
                    elif line[1] not in albszlist:
                        print('第'+str(lineNo)+"行-error:"+line)
                    else:#新的五级分类开始
                        subcls_5=line[0]+line[1]
                        tmpdata=substring_after(line, subcls_5)
                        data=tmpdata.split('、')
                        data = [md.strip().rstrip() for md in data]
                        '''
                        mdata=data
                        data=[]
                        for md in mdata:
                            data.append(md.strip().rstrip())
                        '''
                        wordlist.extend(data)
                        sub_5_dict.update({subcls_5:data})
                        #if '原子弹' in data:
                        #    print(sub_5_dict)
                        #print(sub_5_dict)
                        newlines.append(line+'\n')
                else:
                    #print(line[0])
                    newlinecount=len(newlines)
                    newlines[newlinecount-1]=newlines[newlinecount-1].strip().rstrip()+line+'\n'
                    tmplines.append(line+'\n')
                    #print(newlines[newlinecount-1])
                    with open(path4+'\\'+'info.txt',"a+",encoding="utf-8") as tf:
                        tf.write(newlines[newlinecount-1])
            lineNo=lineNo+1
        sub_4_1_dict={}
        sub_4_1_dict.update({'四级分类':pre_tmpinfo_4})
        sub_4_1_dict.update({'data':sub_5_dict})
        sub_4_dict.update({pre_subcls_4:sub_4_1_dict})
        tdict=sorted(sub_4_dict.items(), key=lambda kv: kv[0])
        sub_4_dict=dict(tdict)
        #print(sub_4_dict)
        
        sub_3_1_dict={}
        sub_3_1_dict.update({'三级分类':pre_tmpinfo_3})
        sub_3_1_dict.update({'data':sub_4_dict})
        sub_3_dict.update({pre_subcls_3:sub_3_1_dict})
        tdict=sorted(sub_3_dict.items(), key=lambda kv: kv[0])
        sub_3_dict=dict(tdict)
        #print(sub_3_dict)
        
        sub_2_1_dict={}
        sub_2_1_dict.update({'二级分类':pre_tmpinfo_2})
        sub_2_1_dict.update({'data':sub_3_dict})
        #print(sorted(sub_2_1_dict.items(), key=lambda kv: kv[0]))
        #print(pre_subcls_2+'\n')
        #print(sub_2_1_dict)
        sub_2_dict.update({pre_subcls_2:sub_2_1_dict})
        #tdict=sorted(sub_2_dict.items(), key=lambda kv: kv[0])
        #sub_2_dict=dict(tdict)
        #print(sub_2_dict)
        
        sub_1_1_dict={}
        sub_1_1_dict.update({'一级分类':pre_tmpinfo_1})
        sub_1_1_dict.update({'data':sub_2_dict})
        sub_1_dict.update({pre_subcls_1:sub_1_1_dict})
        #tdict=sorted(sub_1_dict.items(), key=lambda kv: kv[0])
        #sub_1_dict=dict(tdict)
        #print(sub_1_dict)
        with open(path4+'\\'+name,"w",encoding="utf-8") as tf:
            tf.writelines(newlines)
        with open(path4+'\\'+'tmptext.txt',"w",encoding="utf-8") as tf:
            tf.writelines(tmplines)
        #with open(path5+'\\'+name+'.json', 'w', encoding ='utf8') as json_file:
        with open(path5+'\\'+'myfile.json', 'w', encoding ='utf8') as json_file:
            json.dump(sub_1_dict, json_file, ensure_ascii = False,indent = 6)        
            #print(lineitems)

xdhy_dict={}
for mword in wordlist:
    mword=mword.strip().rstrip()
    xdhy_dict.update({mword:mword})
    #xdhylines.append(mword+'\t'+mword+'\n')
        #print(mword+'不在json文件里！\n')
with open(path5+'\\'+'myxdfile.json', 'w', encoding ='utf8') as json_file:
            json.dump(xdhy_dict, json_file, ensure_ascii = False,indent = 6)
'''
tmp_dict={}
xdhy_dict={}
noinfo=[]
with open(path5+'\\'+'myfile.json', encoding="utf-8") as f:
    tmp_dict= json.load(f)

print('现在测试每个词语的语义分类情况，可能需要较长时间，请耐心等待.......')
for mword in wordlist:
    if mword=='糜':
        print(getwordcodeinfo(mword,tmp_dict))
    if not getwordcodeinfo(mword,tmp_dict):
        noinfo.append(mword+'\n')
    else:
        mword=mword.strip().rstrip()
        xdhy_dict.update({mword:mword})
        xdhylines.append(mword+'\t'+mword+'\n')
        #print(mword+'不在json文件里！\n')
with open(path5+'\\'+'myxdfile.json', 'w', encoding ='utf8') as json_file:
            json.dump(xdhy_dict, json_file, ensure_ascii = False,indent = 6)
with open(path4+'\\'+'nointext.txt',"w",encoding="utf-8") as tf:
            tf.writelines(noinfo)

#测试一词多义
#print(getwordcodeinfo('糜',tmp_dict))
                    
#keys1 = [key for key in tmp_dict]
#print(keys)
'''
    
        
