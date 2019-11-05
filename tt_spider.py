import requests
import re
import os
import time

path = './result_tt' # 文件夹名字，会在脚本当前路径穿件该文件夹，可以修改
base_url = 'https://www.ivsky.com'
time_interval = 0

# 断点重跑
lv1_start = 1 # 大类如下，选择需要跑的起始位，默认1为全部跑
# ['自然风光'，'城市旅游', '动物图片', '植物花卉', '海洋世界', '人物图片', '美食世界',
#  '物品物件', '运动体育', '交通运输', '建筑环境', '装饰装修', '广告设计', '卡通图片', '节日图片', '设计素材', '艺术绘画', '其他类别']

def proxy_rep(targetUrl):
    while True:
        try:
            # 代理服务器
            proxyHost = "http-dyn.abuyun.com"
            proxyPort = "9020"

            # 代理隧道验证信息
            proxyUser = "HE5789T8MP2893JD" # 需要修改
            proxyPass = "B27D12C88B9D7B45" # 需要修改

            proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
              "host" : proxyHost,
              "port" : proxyPort,
              "user" : proxyUser,
              "pass" : proxyPass,
            }

            proxies = {
                "http"  : proxyMeta,
                "https" : proxyMeta,
            }

            headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}


            resp = requests.get(targetUrl, proxies=proxies, headers=headers,timeout=3)
            break
        except:
            print('无效代理ip重试')
            continue
    
    return resp

def mk_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
        
def phrase(url, pattern):
    rep = proxy_rep(targetUrl=url)
    results = re.findall(pattern, rep.text)
    time.sleep(time_interval)
    
    return results

# 先截取在提取
def phrase_double(url, pattern_1, pattern_2):
    rep = proxy_rep(targetUrl=url)
    aim = re.findall(pattern_1, rep.text)
    results = re.findall(pattern_2, aim[0])
    time.sleep(time_interval)
    
    return results

def download_pic(url, path_name):
    with open(path_name,'wb') as f:
        f.write(proxy_rep(targetUrl=url).content)
        
    time.sleep(time_interval)

mk_dir(path=path)    

results_lv1 = phrase(url='https://www.ivsky.com/tupian/', pattern='</li><li class="s.*?"><a href="(/tupian/.*?/)" title=".*?">(.*?)</a>')
results_lv1 = results_lv1[lv1_start-1:]

for result_lv1 in results_lv1:
    lv1_name = result_lv1[1].replace(' ','')
    mk_dir(os.path.join(path,lv1_name))
    
    results_lv2 = phrase_double(url=base_url+result_lv1[0], pattern_1='<div><b>小分类</b>(.*?)</div>', pattern_2='<a href="(/tupian/.*?_t.*?)"  title=".*?">(.*?)</a> ')
    
    for result_lv2 in results_lv2:
        lv2_name = result_lv2[1].replace(' ','')
        mk_dir(os.path.join(path,lv1_name,lv2_name))
        
        start_flag = 0
            
        while True:
            if start_flag == 0:
                try:
                    next_page = phrase(url=base_url+result_lv2[0], pattern='<a class=\'page\-next\' href=\'(.*?)\'>下一页</a></div>')[0]
                except:
                    next_page = ''
                    
                results_lv3 = phrase(url=base_url+result_lv2[0], pattern='<div class="il_img"><a href="(/tupian/.*?html)" title=.*? target="_blank"><img src=.*?jpg" width=.*?height=.*?alt="(.*?)"></a>')
            else:
                results_lv3 = phrase(url=base_url+next_page, pattern='<div class="il_img"><a href="(/tupian/.*?html)" title=.*? target="_blank"><img src=.*?jpg" width=.*?height=.*?alt="(.*?)"></a>')
            
            i = 0
            for result_lv3 in results_lv3:
                lv3_name = result_lv3[1].replace(' ','')
                mk_dir(os.path.join(path,lv1_name,lv2_name,lv3_name))
                url_split = result_lv3[0].split('/')
                pic_name = url_split[3].replace('.html','')

                results_lv4 = phrase(url=base_url+result_lv3[0], pattern='<img id="imgis" src=\'(//img.ivsky.com/img/tupian.*?)\'')
                try:
                    download_pic(url='http:'+results_lv4[0], path_name=os.path.join(path,lv1_name,lv2_name,lv3_name,pic_name+'.jpg'))
                except:
                    pass
                if not os.path.exists(os.path.join(path,lv1_name,lv2_name,lv3_name,'introduce.txt')):
                    introduce_url = base_url+'/'+url_split[1]+'/'+url_split[2]+'/'
                    try:
                        introduce = phrase(url=introduce_url, pattern='>介绍</div><div class="al_p"><p>(.*?)</p>')[0].replace('&nbsp;','')
                    except:
                        introduce = ''
                    with open(os.path.join(path,lv1_name,lv2_name,lv3_name,'introduce.txt'),'w') as f:
                        f.write(introduce)
                i += 1
             
            if next_page == '':
                start_flag = 0
                break
            else:
                start_flag = 1
                try:
                    next_page = phrase(url=base_url+next_page, pattern='<a class=\'page\-next\' href=\'(.*?)\'>下一页</a></div>')[0]
                except:
                    next_page = ''
