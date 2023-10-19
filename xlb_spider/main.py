from xlb_spider import *
from generate_excel import get_excel
from banner import *


def get_keyword():
    keyword = input("请输入需要爬取的关键词===>>> ")
    return keyword


# 主逻辑
def main():
    title()
    keyword = get_keyword()
    login()
    pages = get_page(keyword)
    data = []
    for page in range(1, pages + 1):
        company_dic = get_company(keyword, page, pages)
        for target in company_dic:
            target_url = company_dic[target]
            # target_url = "https://www.xiaolanben.com/company/q72c528294c6d5c37ab07f9eb4b6b9ffc"  # 用这个调试
            row = get_data(target, target_url)  # 爬数据
            data.append(row)
    # 导出excel
    get_excel(data, keyword)
    # 关闭当前窗口
    web.close()
    # # 关闭整个浏览器
    # web.quit()


if __name__ == '__main__':
    main()
