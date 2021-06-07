import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from collections import Counter
from pyecharts.charts import Map, Boxplot
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from wordcloud import WordCloud

pd.set_option('display.max_columns', None)  # 显示所有列

# 读取文件
df = pd.read_csv('lagou_recruitment.csv')

# 对基本要求列进行拆分
assert isinstance(df, object)
df['基本要求'] = df['基本要求'].str.replace(' / ', ' ')
df[['薪水1', '职位要求', '学历']] = df['基本要求'].str.split(expand=True)
df.drop('基本要求', axis=1, inplace=True)
df = df.drop(['薪水1'], axis=1)

# 对公司状况列进行拆分
assert isinstance(df, object)
df[['行业', '融资', '人数']] = df['公司状况'].str.split('/', expand=True)
df.drop('公司状况', axis=1, inplace=True)

# 删除有空值的行
df.dropna(axis=0, how='any', inplace=True)

print(df)

# 查看数据概览
df.info()

# 设置中文字体
plt.rcParams['font.family'] = ['Fangsong']
plt.rcParams['axes.unicode_minus'] = False

# 城市岗位分布图
def city_distribution():
    
    # 获取作图数据
    city = list(df['城市'].value_counts().index)
    cityNumber = list(df['城市'].value_counts())

    # 设置画布大小
    plt.figure(figsize=(30,15))

    #设置坐标刻度字体大小
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)

    #画柱状图
    plt.bar(city,cityNumber)
    plt.title('城市岗位分布图',fontsize=40)
    plt.xlabel('城市',fontsize=40)
    plt.ylabel('岗位数',fontsize=40)
    plt.savefig('城市岗位分布图.png')
    plt.show()

# 学历要求百分图
def education_distribution():

    #获取作图数据
    education = list(df['学历'].value_counts().index)
    educationNumber = list(df['学历'].value_counts())

    # 设置画布大小
    plt.figure(figsize=(10,10))

    #画柱状图
    plt.pie(educationNumber,labels=education,explode=(0.1,0,0,0,0),colors=['lightskyblue','yellow','green','orange'],textprops = {'fontsize':30},autopct='%1.2f%%')
    plt.title('学历要求占比图',fontsize=30)
    plt.savefig('学历要求百分图.png')
    plt.show()

# 城市岗位分布地理图
def city_job():
    city_job_drop = df["城市"].dropna()
    # 去除空值
    num_jobarea = Counter(city_job_drop)

    job_area = list(num_jobarea.keys())
    job_num = list(num_jobarea.values())
    city = job_area
    job_num
    data_city = [(city[i], job_num[i]) for i in range(len(city))]
    china_city = (
        Map()
            .add(
            "",
            data_city,
            "china-cities",
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="城市岗位分布地理图"),
            visualmap_opts=opts.VisualMapOpts(
                min_=100,
                max_=200,
                is_piecewise=True
            ),
        )
            .render("城市岗位分布地理图.html")
    )

# 各城市平均薪资对比图
def city_salary_aver():
    # 薪资处理函数
    def pre_salary(data):
        min = int(data.split('-')[0][:-1])
        max = int(data.split('-')[1][:-1])
        return (min+max)*500

    # 数据处理
    df_1  = pd.DataFrame(df['城市'])
    df_2 = df['薪资'].apply(pre_salary)
    df_aver = df_1.assign(平均薪资 = df_2)
    df_aver = df_aver.groupby('城市').agg({'平均薪资':'mean'})
    df_aver = df_aver.sort_values('平均薪资',ascending=False)

    # 获取作图数据
    city = list(df_aver.index)
    salary_aver = list(df_aver['平均薪资'])

    # 画图
    plt.figure(figsize = (30,15))
    plt.bar(city,salary_aver)
    plt.title('各城市数据分析岗平均薪资对比图',fontsize = 40)
    plt.xlabel('城市',fontsize = 45)
    plt.ylabel('薪资',fontsize = 40)
    plt.xticks(fontsize = 25)
    plt.yticks(fontsize = 25)
    plt.savefig('各城市平均薪资对比图.png')
    plt.show()

# 各行业数据分析岗平均薪资对比图
def trade_salary_aver():
    def pre_salary(data):
        min = int(data.split('-')[0][:-1])
        max = int(data.split('-')[1][:-1])
        return (min + max) * 500

    # 数据处理
    df_1 = pd.DataFrame(df['行业'])
    df_2 = df['薪资'].apply(pre_salary)
    df_aver = df_1.assign(平均薪水=df_2)
    df_aver = df_aver.groupby('行业').agg({'平均薪水': 'mean'})
    df_aver = df_aver.sort_values('平均薪水', ascending=False)

    # 获取作图数据
    city = list(df_aver.index)
    salary_aver = list(df_aver['平均薪水'])

    # 画图
    plt.figure(figsize=(30, 15))
    plt.barh(city, salary_aver)
    plt.title('各行业数据分析岗平均薪资对比图', fontsize=40)
    plt.xlabel('薪资', fontsize=40)
    plt.ylabel('行业', fontsize=50)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=2.5)
    plt.savefig('各行业平均薪资对比图.png')
    plt.show()

# 城市最高薪资岗位
def city_highest_salsry(str):  # str 所查询的城市名
    def pre_salary(data):
        min = int(data.split('-')[0][:-1])
        max = int(data.split('-')[1][:-1])
        return (min + max) * 500

    # 数据处理
    df_diqu = df[df['城市'].isin([str])]
    df_1 = pd.DataFrame(df_diqu['岗位名称'])
    df_2 = df['薪资'].apply(pre_salary)
    df_aver = df_1.assign(平均薪资=df_2)
    df_aver = df_aver.groupby('岗位名称').agg({'平均薪资': 'mean'})
    df_aver = df_aver.sort_values('平均薪资', ascending=False)

    # 获取作图数据
    city = list(df_aver.head(10).index)
    salary_aver = list(df_aver['平均薪资'].head(10))

    # 画图
    plt.figure(figsize=(30, 15))
    plt.barh(city, salary_aver)
    plt.title(str+'市最高薪资岗位', fontsize=40)
    plt.xlabel('岗位名称', fontsize=30)
    plt.ylabel('薪资', fontsize=30)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=8)
    plt.subplots_adjust(left=0.2)
    plt.subplots_adjust(bottom=0.2)
    plt.savefig(str+'市最高薪资岗位图.png')
    plt.show()

# 城市最低薪资招聘信息
def city_lowest_salsry(str1, str2):  # str1 城市名 str2 招聘信息（岗位名称，公司名称，岗位技能，公司福利，职位要求，学历，行业，融资，人数）
    def pre_salary(data):
        min = int(data.split('-')[0][:-1])
        max = int(data.split('-')[1][:-1])
        return (min + max) * 500

    # 数据处理
    df_diqu = df[df['城市'].isin([str1])]
    df_1 = pd.DataFrame(df_diqu[str2])
    df_2 = df['薪资'].apply(pre_salary)
    df_aver = df_1.assign(平均薪资=df_2)
    df_aver = df_aver.groupby(str2).agg({'平均薪资': 'mean'})
    df_aver = df_aver.sort_values('平均薪资', ascending=True)  # ascending=True表示降序排列,ascending=False表示升序排序

    # 获取作图数据
    city = list(df_aver.head(10).index)
    salary_aver = list(df_aver['平均薪资'].head(10))

    # 画图
    plt.figure(figsize=(30, 15))
    plt.barh(city, salary_aver)
    plt.title(str1+'市最低薪资招聘信息', fontsize=40)
    plt.xlabel('薪资', fontsize=30)
    plt.ylabel(str2, fontsize=30)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=8)
    plt.subplots_adjust(left=0.2)
    plt.subplots_adjust(bottom=0.2)
    plt.savefig(str1+'市关于'+str2+'最低薪资招聘信息图.png')
    plt.show()

# 单个城市平均薪资数据分析
def area_data(str1, str2):  # str1 地点 str2 招聘信息（岗位名称，公司名称，岗位技能，公司福利，职位要求，学历，融资，人数）
    def pre_salary(data):
        min = int(data.split('-')[0][:-1])
        max = int(data.split('-')[1][:-1])
        return (min + max) * 500

    # 数据处理
    df_diqu = df[df['地点'].isin([str1])]
    df_1 = pd.DataFrame(df_diqu[str2])
    df_2 = df['薪资'].apply(pre_salary)
    df_aver = df_1.assign(平均薪资=df_2)
    df_aver = df_aver.groupby(str2).agg({'平均薪资': 'mean'})
    df_aver = df_aver.sort_values('平均薪资', ascending=True)  # ascending=True表示降序排列,ascending=False表示升序排序

    # 获取作图数据
    city = list(df_aver.index)
    salary_aver = list(df_aver['平均薪资'])

    # 画图
    plt.figure(figsize=(30, 15))
    plt.bar(city, salary_aver)
    plt.title(str1+'市薪资分析', fontsize=40)
    plt.xlabel(str2, fontsize=30)
    plt.ylabel('薪资', fontsize=30)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=8)
    plt.subplots_adjust(left=0.2)
    plt.subplots_adjust(bottom=0.2)
    plt.savefig(str1+'地区关于'+str2+'数据分析图.png')
    plt.show()

# 不同学历平均薪资对比图
def education_salsry():
    def pre_salary(data):
        min = int(data.split('-')[0][:-1])  # 输出'-'之前
        max = int(data.split('-')[1][:-1])  # 输出'-'之后
        return (min + max) * 500

    # 数据处理
    df_1 = pd.DataFrame(df['学历'])
    df_2 = df['薪资'].apply(pre_salary)
    df_aver = df_1.assign(平均薪资=df_2)
    df_aver = df_aver.groupby('学历').agg({'平均薪资': 'mean'})
    df_aver = df_aver.sort_values('平均薪资', ascending=False)

    # 获取作图数据
    city = list(df_aver.index)
    salary_aver = list(df_aver['平均薪资'])

    # 画图
    plt.figure(figsize=(30, 15))
    plt.barh(city, salary_aver)
    plt.title('不同学历平均薪资对比图', fontsize=40)
    plt.xlabel('薪资', fontsize=40)
    plt.ylabel('学历', fontsize=40)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.savefig('不同学历平均薪资对比图.png')
    plt.show()
#education_salsry()
# 不同经验平均薪资分布箱线图
def setbox(df):
    # 处理薪酬数据

    pattern = '\d+'
    # 将字符串转化为列表,薪资取最低值加上区间值得25%，比较贴近现实
    df['薪资'] = df['薪资'].str.findall(pattern)
    #
    avg_salary_list = []
    for k in df['薪资']:
        int_list = [int(n) for n in k]
        avg_salary = int_list[0] + (int_list[1] - int_list[0]) / 4
        avg_salary_list.append(avg_salary)
    df['月薪'] = avg_salary_list

    # 处理工作年限数据

    df['职位要求'] = df['职位要求'].replace({'经验应届毕业生': '1年以下', '经验不限': '1年以下'})
    groupby_workyear = df.groupby(['职位要求'])['月薪']
    count_groupby_workyear = groupby_workyear.count()
    count_groupby_workyear = count_groupby_workyear.reindex(['1年以下', '经验1-3年', '经验3-5年', '经验5-10年'])
    a = count_groupby_workyear.index
    dff = []
    for b in a:
        c = groupby_workyear.get_group(b).values
        dff.append(c)
    c = Boxplot(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    c.add_xaxis(['1年以下', '经验1-3年', '经验3-5年', '经验5-10年']).add_yaxis("薪资k/年", c.prepare_data(dff)
                                                                   ).set_global_opts(
        title_opts=opts.TitleOpts(title="不同经验平均薪资分布对比图"))
    c.render("不同经验平均薪资分布对比图.html")

"""# 不同行业平均薪资对比图(有问题)
def position_salary():
    def pre_salary(data):
        min = int(data.split('-')[0][:-1])  # 输出'-'之前
        max = int(data.split('-')[1][:-1])  # 输出'-'之后
        return (min + max) * 500

    # 数据处理
    df_1 = pd.DataFrame(df['岗位名称'])
    df_2 = df['薪资'].apply(pre_salary)
    df_aver = df_1.assign(平均薪资=df_2)
    df_aver = df_aver.groupby('岗位名称').agg({'平均薪资': 'mean'})
    df_aver = df_aver.sort_values('平均薪资', ascending=False)

    # 获取作图数据
    city = list(df_aver.index)
    salary_aver = list(df_aver['平均薪资'])

    # 画图
    plt.figure(figsize=(30, 15))
    plt.barh(city, salary_aver)
    plt.title('不同岗位平均薪资对比图', fontsize=40)
    plt.xlabel('薪资', fontsize=40)
    plt.ylabel('岗位', fontsize=40)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=5)
    plt.savefig('不同岗位平均薪资对比图.png')
    plt.show()
#position_salary()"""
# 岗位词云
def position_wordcloud():
    # 制作词频
    company = list(df['岗位名称'].value_counts().index)
    companyNumber = list(df['公司名称'].value_counts())
    word_frequency = dict(zip(company, companyNumber))

    # 词云
    wordcloud = WordCloud(font_path='C:/Windows/Fonts/simfang.ttf', mode='RGBA', background_color=None, width=1000,
                          height=800).fit_words(word_frequency)

    # 画图
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()

    # 保存到文件
    wordcloud.to_file('岗位云图.png')
#position_wordcloud()

city_distribution() #城市岗位分布图
education_distribution()    #学历要求百分图
city_job()  #城市岗位分布地理图
city_salary_aver()  #各城市平均薪资对比图
trade_salary_aver() #各行业平均薪资对比图
city_highest_salsry(str)    #某市最高薪资岗位图
city_lowest_salsry(str1, str2)  #某城市最低薪资招聘信息
area_data(str1, str2)   #某市平均薪资招聘信息
education_salsry()  #不同学历平均薪资对比图
setbox(df)  #不同经验平均薪资分布对比图
position_wordcloud()    #岗位云图
