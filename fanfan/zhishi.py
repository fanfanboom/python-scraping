from urllib.request import urlopen
import json

stockcode = '300630.SZ'
stock_info = {}
html = urlopen('https://www.zsxg.cn/api/v2/capital/info?code={}&yearNum=6'.format(stockcode))
sto = json.loads(html.read())
if sto['message'] == '成功':
    stock_info['代码'] = sto['datas']['code']
    stock_info['名称'] = sto['datas']['name']
    stock_info['收盘'] = sto['datas']['close']
    stock_info['简介'] = sto['datas']['briefing']

    stock_info['一级行业'] = sto['datas']['industry']
    stock_info['二级行业'] = sto['datas']['industry2']
    stock_info['三级行业'] = sto['datas']['industry3']

    stock_info['投资亮点'] = sto['datas']['comment_new']['positive_new']
    stock_info['风险提示'] = sto['datas']['comment_new']['unpositive_new']

    stock_info['盈利预测-同比增长率'] = sto['datas']['forGrowthRate']
    stock_info['盈利预测-市盈率'] = sto['datas']['forPE']
    stock_info['盈利预测-每股收益'] = sto['datas']['forEPS']
    stock_info['盈利预测-PEG'] = sto['datas']['forPeg']

    stock_info['ROE'] = sto['datas']['roe']
    stock_info['机构持股-北向资金'] = str(round(sto['datas']['instholdpct']['list'][0] * 100, 2)) + '%'
    stock_info['机构持股-基金'] = str(round(sto['datas']['instholdpct']['list'][1] * 100, 2)) + '%'
    stock_info['机构持股-券商'] = str(round(sto['datas']['instholdpct']['list'][2] * 100, 2)) + '%'
    stock_info['机构持股-QFII'] = str(round(sto['datas']['instholdpct']['list'][3] * 100, 2)) + '%'
    stock_info['机构持股-社保'] = str(round(sto['datas']['instholdpct']['list'][4] * 100, 2)) + '%'
    stock_info['机构持股-保险'] = str(round(sto['datas']['instholdpct']['list'][5] * 100, 2)) + '%'

    stock_info['RPS强度-10'] = str(round(sto['datas']['rpsMap']['rps10_today'] * 100, 2)) + '%'
    stock_info['RPS强度-20'] = str(round(sto['datas']['rpsMap']['rps20_today'] * 100, 2)) + '%'
    stock_info['RPS强度-60'] = str(round(sto['datas']['rpsMap']['rps60_today'] * 100, 2)) + '%'
    stock_info['RPS强度-120'] = str(round(sto['datas']['rpsMap']['rps120_today'] * 100, 2)) + '%'

    stock_info['BOLL强度'] = sto['datas']['boll']['comment']

    stock_info['建议估值模型'] = sto['datas']['pepbMap']['recommend']

    stock_info['PB'] = sto['datas']['pepbMap']['pb']
    stock_info['PB低估线'] = sto['datas']['pepbMap']['pbMin']
    stock_info['PB当天'] = sto['datas']['pepbMap']['pbY']
    stock_info['PB状态'] = sto['datas']['pepbMap']['pbStatus']
    stock_info['PB提示'] = sto['datas']['pepbMap']['pbContent']

    stock_info['PE'] = sto['datas']['pepbMap']['pe']
    stock_info['PE低估'] = sto['datas']['pepbMap']['peMin']
    stock_info['PE当天'] = sto['datas']['pepbMap']['peY']
    stock_info['PE状态'] = sto['datas']['pepbMap']['peStatus']
    stock_info['PE提示'] = sto['datas']['pepbMap']['peContent']

profithtml = urlopen(
    'https://www.zsxg.cn/api/v2/quarter/profitability?code={}&compareCode=&types=roi%2CprofitMargin'
    '%2CcostMargin%2Cdupont&yearNum=12'.format(stockcode))
profit = json.loads(profithtml.read())
if profit['message'] == '成功':
    roe = profit['datas']['dupont']['roeDupont1']['roe']
    roes = profit['datas']['origin']['roe']
    # print(roes)

fenhonghtml = urlopen('https://www.zsxg.cn/api/v2/dividend/get?code={}&yearNum=50'.format(stockcode))
fenhong = json.loads(fenhonghtml.read())
if fenhong['message'] == '成功':
    fenhongmiaoshu = fenhong['datas']['fh']['desc']
    # print(fenhongmiaoshu)

print(stock_info)
