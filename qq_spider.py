import requests
import re
import os
import time

path = './result_hjx' # 文件夹名字，会在脚本当前路径穿件该文件夹，可以修改
base_url = 'https://www.qqtn.com'
time_interval = 1

# 断点重跑
lv1_start = 1 # 大类如下，选择需要跑的起始位，默认1为全部跑
# ['女生图片', '唯美图片', '明星图片', '个性图片', '文字图片', '带字图片', '节日图片', 
#  '背景图片', '可爱图片', '好看的图片', '微信图片', '搞笑图片', '风景图片', '情侣图片', '非主流图片', 
#  '小清新图片', '伤感图片', '爱情图片', '欧美图片', '美女图片', '动态图片', '动漫图片', '卡通图片', 
#  '动物图片', '霸气图片', '帅哥图片', '励志图片', '黑白图片', '背影图片', '悲伤的图片', '猫咪图片', '古风图片', 
#  '闺蜜图片', '圣诞节图片', '婚纱图片', '性感图片', '伤心图片', '生日快乐图片', '亲吻图片', '难过的图片', '早安图片', '晚安图片']


def mk_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
        
def phrase(url, pattern):
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
    rep = requests.get(url, headers=headers)
    rep.encoding = 'gbk'
    results = re.findall(pattern, rep.text)
    time.sleep(time_interval)
    
    return results

def phrase_S(url, pattern):
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
    rep = requests.get(url, headers=headers)
    rep.encoding = 'gbk'
    reg = re.compile(pattern, re.S)
    results = re.findall(reg, rep.text)
    time.sleep(time_interval)
    
    return results

# 先截取在提取
def phrase_double(url, pattern_1, pattern_2):
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
    rep = requests.get(url, headers=headers)
    rep.encoding = 'gbk'
    aim = re.findall(pattern_1, rep.text)
    results = re.findall(pattern_2, aim[0])
    time.sleep(time_interval)
    
    return results

def phrase_double_S(url, pattern_1, pattern_2):
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
    rep = requests.get(url, headers=headers)
    rep.encoding = 'gbk'
    reg = re.compile(pattern_1, re.S)
    aim = re.findall(reg, rep.text)
    results = re.findall(pattern_2, aim[0])
    time.sleep(time_interval)
    
    return results

def download_pic(url, path_name):
    with open(path_name,'wb') as f:
        f.write(requests.get(url).content)
        
    time.sleep(time_interval)

mk_dir(path=path)
results_lv1 = phrase(url='https://www.qqtn.com/tp/t/', pattern='<li><a href="(.*?)" title="(.*?)" target="_blank">.*?</a></li>')
results_lv1 = results_lv1[lv1_start-1:]

for result_lv1 in results_lv1:
    lv1_name = results_lv1[0][1]
    mk_dir(path=os.path.join(path,lv1_name))
    base_article_url = base_url+result_lv1[0].split('_')[0]
    try:
        page_num = int(phrase(url=base_url+result_lv1[0],pattern='>下一页</i> </a> <a href="/tp/.*?_(.*?)\.html" class="tsp_end"><i>尾页</i>')[0])
    except:
        page_num = 0
        
    for i in range(page_num):
        results_lv2 = phrase_double_S(url=base_article_url+'_'+str(i+1)+'.html', pattern_1='<ul class="g-gxlist-imgbox">(.*?)</ul>', pattern_2='<li><a href="(.*?)" target="_blank" title="(.*?)"><img')

        for result_lv2 in results_lv2:
            lv2_name = result_lv2[1]
            mk_dir(path=os.path.join(path,lv1_name,lv2_name))
            
            introduces = phrase_S(url=base_url+result_lv2[0],pattern='<h1>(.*?)</h1>.*?<div class="m\-daodu"><strong> 导读：</strong>(.*?)</div>.*?id="zoom" class="m_qmview".*?<p>(.*?)</p>')
            
            try:
                with open(os.path.join(path,lv1_name,lv2_name,'info.txt'),'w') as f:
                    f.write('标题：'+introduces[0][0]+'\n'+
                           '导读：'+introduces[0][1]+'\n'+
                           '描述文字：'+introduces[0][2])
            except:
                with open(os.path.join(path,lv1_name,lv2_name,'info.txt'),'w') as f:
                    f.write('标题：'+'\n'+
                           '导读：'+'\n'+
                           '描述文字：')
                    
            pic_urls = phrase(url=base_url+result_lv2[0],pattern='<p align="center"><img src="(https.*?)"/></p>')
            
            for pic_url in pic_urls:
                name = pic_url.split('/')[-1]
                try:
                    download_pic(url=pic_url, path_name=os.path.join(path,lv1_name,lv2_name,name))
                except:
                    pass
