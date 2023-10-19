import pandas as pd


def get_excel(data, keyword):
    df = pd.DataFrame(data={'tuples': data})

    df['目标公司名称'] = df['tuples'].str['company_name']
    df['公司基础信息'] = df['tuples'].str['company_info']
    df['网站域名信息'] = df['tuples'].str['website_info']
    df['App'] = df['tuples'].str['app_info']
    df['微信公众号'] = df['tuples'].str['wechat_info']
    df['小程序'] = df['tuples'].str['xcx_info']
    df['微博'] = df['tuples'].str['weibo_info']
    # df['其他'] = df['tuples'].str['ort_info']

    # 去除默认的那一列,写入excel
    df.drop(['tuples'], axis=1).to_excel(f"./{keyword}-data.xlsx", sheet_name="results", index=False)
