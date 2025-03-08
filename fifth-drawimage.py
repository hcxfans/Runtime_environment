import pandas as pd
import matplotlib.pyplot as plt
import os
#import numpy as np
path9= r'.\image\all'
path10= r'.\image\feature'

def row5(starbucks):
    #星巴克数据中前五行的数据
    pd.set_option('display.max_columns', None) # 显示完整的列
    #print("前五行数据：")
    #print(starbucks.head())
    #星巴克旗下的品牌
    #print("本文件方言按地区划分有：\n",starbucks.zone.value_counts())

def howmany(mzone,starbucks,path):

    #只查看四川方言的数据集
    fangyan = starbucks[starbucks.zone==mzone]
    Ori=fangyan.groupby(["Origin"]).size()
                         
    Sub_1 = fangyan.groupby(["Sub_class1"]).size()
    
    #print("方言词语义类分类一大类有：",Sub_1.size,"个类别")

    Sub_1_1 = Sub_1.sort_values(ascending=False)
    #print("排名前九的一大类有：\n",Sub_1_1.head(len(Sub_1)))
    sub_c1=Sub_1_1.head(len(Sub_1))
    #print(sub_c1[1])
    #print("排名倒九的一大类有：\n",Sub_1_1.tail(9))
    
    label_country =mzone
    label1= '义类大一类'
    label2= label1
    #zhuzhuangtu(Sub_1_1, labe_country,labe1)
    path1=path+'\\Eps'
    path2=path+'\\Png'
    if not os.path.exists(path1+f'\\{mzone}'):
        os.mkdir(path1+f'\\{mzone}')
    if not os.path.exists(path2+f'\\{mzone}'):
        os.mkdir(path2+f'\\{mzone}')
    label_o1= '词语来源'
    label_o2= label_o1
    zhuzhuangtu(Ori, label_country,label_o1,label_o2,path1+f'\\{mzone}',path2+f'\\{mzone}')
    mybingtu(Ori, label_country, label_o1,label_o2,path1+f'\\{mzone}',path2+f'\\{mzone}')
    
    zhuzhuangtu(Sub_1, label_country,label1,label2,path1+f'\\{mzone}',path2+f'\\{mzone}')
    mybingtu(Sub_1, label_country, label1,label2,path1+f'\\{mzone}',path2+f'\\{mzone}')
    
    Sub_1_1 = Sub_1.sort_values(ascending=False)
    mList=list(Sub_1_1.head(len(Sub_1_1)).index)
    i=0
    for sub_cls1 in mList:
        i=i+1
        fangyan1= fangyan[fangyan.Sub_class1==sub_cls1]
        Sub_2 = fangyan1.groupby(["Sub_class2"]).size()
        label1= '义类大二类'
        label2= f'“{sub_cls1}”的义类大二类'
        if not os.path.exists(path1+f'\\{mzone}\\{i}_{sub_cls1}'):
            os.mkdir(path1+f'\\{mzone}\\{i}_{sub_cls1}')
        if not os.path.exists(path2+f'\\{mzone}\\{i}_{sub_cls1}'):
            os.mkdir(path2+f'\\{mzone}\\{i}_{sub_cls1}')
        #zhuzhuangtu(Sub_2, label_country,label1)
        zhuzhuangtu(Sub_2, label_country,label1,label2,path1+f'\\{mzone}\\{i}_{sub_cls1}',path2+f'\\{mzone}\\{i}_{sub_cls1}')     
        mybingtu(Sub_2, label_country, label1,label2,path1+f'\\{mzone}\\{i}_{sub_cls1}',path2+f'\\{mzone}\\{i}_{sub_cls1}')
        
        Sub_2_1 = Sub_2.sort_values(ascending=False)
        mList1=list(Sub_2_1.head(len(Sub_2_1)).index)
        j=0
        for sub_cls2 in mList1:
            j=j+1
            fangyan2= fangyan1[fangyan1.Sub_class2==sub_cls2]
            Sub_3 = fangyan2.groupby(["Sub_class3"]).size()
            label1_1= '义类大三类'
            label2_1= f'“{sub_cls1}”下“{sub_cls2}”的义类大三类'
            if not os.path.exists(path1+f'\\{mzone}\\{i}_{sub_cls1}\\{j}_{sub_cls2}'):
                os.mkdir(path1+f'\\{mzone}\\{i}_{sub_cls1}\\{j}_{sub_cls2}')
            if not os.path.exists(path2+f'\\{mzone}\\{i}_{sub_cls1}\\{j}_{sub_cls2}'):
                os.mkdir(path2+f'\\{mzone}\\{i}_{sub_cls1}\\{j}_{sub_cls2}')
            zhuzhuangtu(Sub_3, label_country,label1_1,label2_1,path1+f'\\{mzone}\\{i}_{sub_cls1}\\{j}_{sub_cls2}',path2+f'\\{mzone}\\{i}_{sub_cls1}\\{j}_{sub_cls2}')       
            mybingtu(Sub_3, label_country,label1_1,label2_1,path1+f'\\{mzone}\\{i}_{sub_cls1}\\{j}_{sub_cls2}',path2+f'\\{mzone}\\{i}_{sub_cls1}\\{j}_{sub_cls2}') 
           

def zhuzhuangtu(data,label_country,label1, label2,path1,path2):
    data=data.sort_values(ascending=False)
    #mdata=data.head(9)
    #plt.figure(figsize=(len(data)+1, len(data)+1))
    #plt.figure(figsize=(max(len(data)+1,6.4), 4.8),dpi=200)
    plt.figure(figsize=(10, 4.8),dpi=200)
    #plt.figure(dpi=200)
    plt.bar(range(len(data)), data.head(len(data)), width=0.5)
    plt.xlabel(label1)
    plt.ylabel('方言词语数量')
    if len(data)>8:
        plt.xticks(range(len(data)), data.head(len(data)).index,rotation=45)
    else:
        plt.xticks(range(len(data)), data.head(len(data)).index)
    for a, b in zip(range(len(data)),data.head(len(data))):
        plt.text(a,b,b, ha='center')
    #for i in range(9):
    #    plt.text(i, mdata, str(mdata[i]), ha='center')
    if label_country=='大陆':
        plt.title(f'现代汉语{label2}词语数量柱状图')
        plt.savefig(path1+f'\\现代汉语-{label2}词语数量柱状图.eps')
        plt.savefig(path2+f'\\现代汉语-{label2}词语数量柱状图.png')
    else:
        plt.title(f'{label_country}方言{label2}词语数量柱状图')
        plt.savefig(path1+f'\\{label_country}方言-{label2}词语数量柱状图.eps', bbox_inches='tight')
        plt.savefig(path2+f'\\{label_country}方言-{label2}词语数量柱状图.png', bbox_inches='tight')
    #plt.show()
    plt.close()

    
    
    
def threezhuzhuangtu(data1,mzone1,data2,mzone2,data3,mzone3, label,path):
    
    fangyan1 = data1[data1.zone==mzone1]
    mdata1 = fangyan1.groupby(["Sub_class1"]).size()
    fangyan2 = data2[data2.zone==mzone2]
    mdata2 = fangyan2.groupby(["Sub_class1"]).size()
    fangyan3 = data3[data3.zone==mzone3]
    mdata3 = fangyan3.groupby(["Sub_class1"]).size()
    
    plt.figure(figsize=(max(len(mdata1)+1,6.4), 4.8),dpi=200)
    #plt.figure()
    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())
    #mng = plt.get_current_fig_manager()
    #mng.full_screen_toggle()
    
    x1=[0,1,2,3,4,5,6,7,8]
    x2=[]
    x3=[]
    for x in x1:
       x2.append(x+0.3)
       x3.append(x+0.6)
    
    plt.bar(x1,mdata1.head(9), width=0.3)
    plt.bar(x2, mdata2.head(9), width=0.3)
    plt.bar(x3, mdata3.head(9), width=0.3)
    #plt.bar(x1, mdata1.head(9), facecolor='lightskyblue',edgecolor='white',width=0.4)
    #plt.bar(x2, mdata2.head(9), facecolor='yellowgreen',edgecolor='white', width=0.4)
    plt.xlabel(label)
    plt.ylabel('方言词语数量')
    plt.xticks(x2, mdata2.head(9).index)
    for a, b in zip(x1,mdata1.head(9)):
        plt.text(a,b,b, ha='center')
    for a, b in zip(x2,mdata2.head(9)):
        plt.text(a,b,b, ha='center')
    for a, b in zip(x3,mdata3.head(9)):
        plt.text(a,b,b, ha='center')
    plt.title(f'{mzone1}现代汉语、{mzone2}方言和{mzone3}方言{label}词语数量柱状图')
    #plt.legend(loc='best',title='图例')
    
    plt.legend( ['现代汉语', '四川方言', '成都方言'], loc='best',title='图例')
    plt.savefig(path+'\\Eps'+f'\\{mzone1}现代汉语、{mzone2}方言和{mzone3}方言{label}词语数量柱状图.eps', bbox_inches='tight')
    plt.savefig(path+'\\Png'+f'\\{mzone1}现代汉语、{mzone2}方言和{mzone3}方言{label}词语数量柱状图.png', bbox_inches='tight')
    plt.show()
    
    
    plt.close()

def mybingtu(data, label_country, label1,label2,path1,path2):
    #fangyan = starbucks[starbucks.zone==mzone]
    #Sub_1 = fangyan.groupby(["Sub_class1"]).size()
    #data =data.sort_values(ascending=False)
    
    #plt.figure(figsize=(len(data)+1, len(data)+1))
    plt.figure(dpi=200)
    explode=[]
    for i in range(len(data)):
        explode.append(0.1)

    #explode = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
    plt.pie(data, explode=explode, labels=data.index, autopct='%1.1f%%')

    if label_country=='大陆':
        plt.title(f'现代汉语{label2}词语数量饼图')
        plt.savefig(path1+f'\\现代汉语-{label2}词语数量饼图.eps')
        plt.savefig(path2+f'\\现代汉语-{label2}词语数量饼图.png')
    else:
        plt.title(f'{label_country}方言{label2}词语数量饼图')
        plt.savefig(path1+f'\\{label_country}方言{label2}词语数量饼图.eps', bbox_inches='tight')
        plt.savefig(path2+f'\\{label_country}方言{label2}词语数量饼图.png', bbox_inches='tight')
    #plt.show()
    plt.close()

if __name__ == "__main__":
    plt.rcParams['font.sans-serif'] = ['SimHei']  # z这个好用,解决中文乱码
    plt.rcParams['axes.unicode_minus'] = False
    if not os.path.exists(r'.\image'):
        os.mkdir(r'.\image')
    if not os.path.exists(path9):
        os.mkdir(path9)
    if not os.path.exists(path9+'\\Eps'):
        os.mkdir(path9+'\\Eps')
    if not os.path.exists(path9+'\\Png'):
        os.mkdir(path9+'\\Png')
    starbucks3 = pd.read_csv('out/现代汉语词汇义类编码文本.csv', sep='\t')
    starbucks1 = pd.read_csv('out/四川方言词汇义类编码文本.csv', sep='\t')
    starbucks2 = pd.read_csv('out/成都方言词汇义类编码文本.csv', sep='\t')
    #row5(starbucks1)
    #row5(starbucks2)
    threezhuzhuangtu(starbucks3,'大陆',starbucks1,'四川',starbucks2,'成都', '义类大一类',path9)
    print('正在绘制各词典的柱状图和饼图，绘制的图形保存在image\\all文件夹下，Eps是矢量图，需在Acrobat Pdf软件里打开，Png是标量图，可直接打开。绘制图形比较多，请耐心等待......')
    howmany('四川',starbucks1,path9)
    howmany('成都',starbucks2,path9)
    howmany('大陆',starbucks3,path9)

    if not os.path.exists(path10):
        os.mkdir(path10)
    if not os.path.exists(path10+'\\Eps'):
        os.mkdir(path10+'\\Eps')
    if not os.path.exists(path10+'\\Png'):
        os.mkdir(path10+'\\Png')

    starbucks3 = pd.read_csv('out/现代汉语词汇义类编码文本.csv', sep='\t')
    starbucks1 = pd.read_csv('out/四川方言词汇特征词文本.csv', sep='\t')
    starbucks2 = pd.read_csv('out/成都方言词汇特征词文本.csv', sep='\t')
    threezhuzhuangtu(starbucks3,'大陆',starbucks1,'四川',starbucks2,'成都', '特征词义类大一类',path10)
    print('正在绘制特征词的柱状图和饼图，绘制的图形保存在image\\feature文件夹下，Eps是矢量图，需在Acrobat Pdf软件里打开，Png是标量图，可直接打开。绘制图形比较多，请耐心等待......')
    

    howmany('四川',starbucks1,path10)
    howmany('成都',starbucks2,path10)
    howmany('大陆',starbucks3,path10)
    
