from selenium.webdriver.common.by import By
import time
from webdriver import get_webdriver

web = get_webdriver()  # 全局参数


# 获取当前时间
def get_current_time():
    ticks = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # print(get_current_time(), '[*]>>',)
    return ticks


# 模拟登录
def login():
    username = "16735607384"
    password = "16735607384"
    print(get_current_time(), '[*]>>', "\033[32m开始进行模拟登陆\033[0m")
    login_url = "https://www.xiaolanben.com/login"
    web.get(login_url)
    web.find_element(by=By.XPATH,
                     value='//*[@id="app"]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/input').send_keys(username)
    web.find_element(by=By.XPATH,
                     value='//*[@id="app"]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/input').send_keys(password)
    web.find_element(by=By.XPATH,
                     value='//*[@id="app"]/div/div[2]/div/div[2]/div/div[2]/div[1]/label/span/span/span').click()
    web.find_element(by=By.XPATH, value='//*[@id="app"]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[4]').click()
    print(get_current_time(), '[+]>>', "\033[31m模拟登陆完成\033[0m")
    time.sleep(2)
    cookies = web.get_cookies()  # 获取cookies
    # print(cookies)
    cookie_dic = {dic['name']: dic['value'] for dic in cookies}  # 字典生成式
    cookie_dic = {"userId": cookie_dic['userId'], "token": cookie_dic['token']}  # 小蓝本只需要userId和token就行
    print(cookie_dic)


# 获取最大页数
def get_page(keyword):
    url = f"https://www.xiaolanben.com/search?key={keyword}&page=1"
    web.get(url)
    pages = web.find_element(by=By.XPATH, value='//*[@id="app"]//ul[@class="el-pager"]/li[last()]').text
    # pages = 1
    return int(pages)


# 判断元素是否存在
def check_element_exists(driver, condition, element):
    try:
        if condition == 'class':
            res = driver.find_element_by_class_name(element)
            return res
        elif condition == 'id':
            res = driver.find_element_by_id(element)
            return res
        elif condition == 'xpath':
            # res = driver.find_element_by_xpath(element)
            res = driver.find_element(by=By.XPATH, value=element)
            # print("元素存在", res.text)
            return res.text
    except Exception as e:
        # print("不存在该元素")
        return False


# 获取需要爬取的公司
def get_company(keyword, page, pages):
    print(get_current_time(), '[*]>>', f"\033[32m开始搜索请求关键词---> {keyword} <--- 第{page}/{pages}页\033[0m")
    url = f"https://www.xiaolanben.com/search?key={keyword}&page={page}"
    web.get(url)

    a_list = web.find_elements(by=By.XPATH,
                               value='//*[@id="app"]//section[@class="company-card"]//a[@class="search-company-item"]')
    company_dic = {}
    for a in a_list:
        a_title = a.find_element(by=By.XPATH, value='.//span[@class="title"]').text
        a_href = a.get_attribute("href")
        company_dic[a_title] = a_href  # 字典添加键值对
    # print(a_dic)  # 当前页的企业名称{'河南公司','http://xxx',"河南公司2","http://xxx"}
    return company_dic


# 滑动滚条
def move_roller():
    # 切换到弹出窗口
    window_handles = web.window_handles
    web.switch_to.window(window_handles[-1])
    # 定位到包含内容的元素
    content_div = web.find_element_by_xpath('//*[@id="page-menu-project-info"]/section/div/div/div[2]/div[2]')
    time.sleep(1)

    # 持续滑动滚动条直到加载完成
    while True:
        # 获取当前位置和页面高度
        old_position = web.execute_script("return arguments[0].scrollTop;", content_div)  # 上一次划动的位置
        web.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", content_div)
        time.sleep(2)
        new_position = web.execute_script("return arguments[0].scrollTop;", content_div)  # 下一次划动的位置
        # print(old_position, new_position)
        # 判断是否已经滑动到底部
        if new_position == old_position:
            break


# 爬取数据    # 这里需要有个新思路  就是直接先判断有没查看更多,有就打开直接爬,没有就不打开爬
def get_data(target, target_url):
    print(get_current_time(), '[*]>>',
          f"\033[32m开始爬取--->{target}<---{target_url}\033[0m")  # target是键  a_dic[target]是值
    web.get(target_url)

    # ############################公司基础信息#########################
    try:
        company_info = web.find_element(by=By.XPATH, value='//div[@class="d-flex fz-12 gray-3"]').text
        print(get_current_time(), '[+]>>', "\033[31m获取到公司基础信息: \033[0m")
        print(company_info)
    except:
        company_info = ""

    # # 定位项目信息
    # time.sleep(1)
    # web.find_element(by=By.XPATH, value='//*[@id="menu-project-info"]').click()

    # ############################ Apps  ############################
    app_str_info = ""
    try:
        web.find_element(by=By.XPATH, value='//*[@id="tab-app"]').click()  # 点击app功能

        # 判断有没有查看更多
        if check_element_exists(web, condition="xpath", element='//*[@id="pane-app"]/p/span'):
            web.find_element(by=By.XPATH, value='//*[@id="pane-app"]/p/span').click()  # 点击查看更多
            move_roller()  # 滑动滚条

        a_list = web.find_elements(by=By.XPATH,
                                   value='//*[@id="page-menu-project-info"]/section/div/div/div[2]/div[2]/article/div/a')
        for a in a_list:
            app_name = a.find_element(by=By.XPATH,
                                      value='./div[@class="content"]/p[@class="name"]/span').text
            # app_href = ""  # 后续添加更详细的信息爬取
            # app_list.append(app_name)
            app_str_info = app_name + "\n" + app_str_info

    except:
        pass
    if app_str_info != "":
        print(get_current_time(), '[+]>>', "\033[31m获取到App信息: \033[0m")
        print(app_str_info.replace("\n", "、"))

    # ##################################### 新媒体 #####################################
    web.refresh()  # 刷新
    wechat_str_info = ""
    xcx_str_info = ""
    weibo_str_info = ""
    ort_str_info = ""
    try:
        web.find_element(by=By.XPATH, value='//*[@id="tab-media"]').click()

        # 判断有没有查看更多
        if check_element_exists(web, condition="xpath", element='//*[@id="pane-media"]/p/span'):
            web.find_element(by=By.XPATH, value='//*[@id="pane-media"]/p/span').click()  # 点击查看更多
            move_roller()  # 滑动滚条

        # a_lst = web.find_elements(by=By.XPATH, value='//*[@id="pane-media"]/div/a')
        a_lst = web.find_elements(by=By.XPATH,
                                  value='//*[@id="page-menu-project-info"]/section/div/div/div[2]/div[2]/article/div/a')
        for a in a_lst:
            media_name = a.find_element(by=By.XPATH, value='.//div[@class="media-item-name"]/p').text
            media_href = a.get_attribute("href")
            # 通过href判断是小程序还是公众号还是微博
            if "media/wechat" in media_href:
                # wechat_lst.append(media_name)
                wechat_str_info = media_name + "\n" + wechat_str_info
            elif "media/xcx" in media_href:
                # xcx_lst.append(media_name)
                xcx_str_info = media_name + "\n" + xcx_str_info
            elif "weibo.com" in media_href:
                # weibo_lst.append(media_name)
                weibo_str_info = media_name + "\n" + weibo_str_info
            else:
                # ort_lst.append(media_name)
                ort_str_info = media_name + "\n" + ort_str_info

    except:
        pass
    if wechat_str_info != "":
        print(get_current_time(), '[+]>>', "\033[31m获取到微信公众号信息: \033[0m")
        print(wechat_str_info.replace("\n", "、"))
    if xcx_str_info != "":
        print(get_current_time(), '[+]>>', "\033[31m获取到小程序信息: \033[0m")
        print(xcx_str_info.replace("\n", "、"))
    if weibo_str_info != "":
        print(get_current_time(), '[+]>>', "\033[31m获取到微博信息: \033[0m")
        print(weibo_str_info.replace("\n", "、"))
    if ort_str_info != "":
        print(get_current_time(), '[+]>>', "\033[31m获取到其他新媒体信息: \033[0m")
        print(ort_str_info.replace("\n", "、"))

    # ##########################################  网站  ##########################################
    web.refresh()  # 刷新
    # website_list = []
    website_str_info = ""
    try:
        web.find_element(by=By.XPATH, value='//*[@id="tab-website"]').click()
        # 判断有没有查看更多
        if check_element_exists(web, condition="xpath", element='//*[@id="pane-website"]/p/span'):
            web.find_element(by=By.XPATH, value='//*[@id="pane-website"]/p/span').click()  # 点击查看更多
            # web.find_element(by=By.XPATH, value='//*[@id="tab-2"]').click()  # 点击切换标签
            move_roller()  # 滑动滚条
        a_lst = web.find_elements(by=By.XPATH,
                                  value='//*[@id="page-menu-project-info"]/section/div/div/div[2]/div[2]/article/div/a')
        # website_dic = {}
        for a in a_lst:
            website_name = a.find_element(by=By.XPATH, value='.//div[@class="website-item-name"]/p').text
            website_href = a.get_attribute("href")
            # website_dic[website_name] = website_href
            website_str_info = f"{website_name}: {website_href}" + "\n" + website_str_info
        # website_list.append(website_dic)
    except:
        pass
    # if website_list != [] and website_list != [{}]:
    if website_str_info != "":
        print(get_current_time(), '[+]>>', "\033[31m获取到网站域名信息:  \033[0m")
        print(website_str_info)

    row = {"company_name": target, "company_info": company_info, "app_info": app_str_info,
           "wechat_info": wechat_str_info,
           "xcx_info": xcx_str_info, "weibo_info": weibo_str_info, "ort_info": ort_str_info,
           "website_info": website_str_info}

    return row
