from urllib.request import urlopen
import json
import openpyxl
import time
import random


def queryStock(stockcode):
    stock_info = {}
    try:
        html = urlopen('https://www.zsxg.cn/api/v2/capital/info?code={}&yearNum=6'.format(stockcode))
        sto = json.loads(html.read())
        if sto['message'] == '成功':
            stock_info['代码'] = sto['datas']['code']
            stock_info['名称'] = sto['datas']['name']
            stock_info['收盘'] = sto['datas']['close']
            stock_info['总股本'] = str(round(sto['datas']['share_total'] / 100000000, 2)) + '亿股'
            stock_info['总市值'] = str(sto['datas']['total_mv']) + '亿元'
            stock_info['简介'] = sto['datas']['briefing']

            stock_info['一级行业'] = sto['datas']['industry']
            stock_info['二级行业'] = sto['datas']['industry2']
            stock_info['三级行业'] = sto['datas']['industry3']

            touziliangdians = sto['datas']['comment_new']['positive_new']
            stock_info['投资亮点'] = []
            for tzld in touziliangdians:
                stock_info['投资亮点'].append('{}:{}'.format(tzld['tag'], tzld['value']))
            stock_info['投资亮点'] = "".join(stock_info['投资亮点'])
            fengxiantishis = sto['datas']['comment_new']['unpositive_new']
            stock_info['风险提示'] = []
            for fxts in fengxiantishis:
                stock_info['风险提示'].append('{}:{}'.format(fxts['tag'], fxts['value']))
            stock_info['风险提示'] = "".join(stock_info['风险提示'])

            stock_info['盈利预测-同比增长率'] = str(sto['datas']['forGrowthRate'])
            stock_info['盈利预测-市盈率'] = str(sto['datas']['forPE'])
            stock_info['盈利预测-每股收益'] = str(sto['datas']['forEPS'])
            stock_info['盈利预测-PEG'] = str(sto['datas']['forPeg'])

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
            stock_info['ROE'] = profit['datas']['dupont']['roeDupont1']['roe']
            stock_info['ROEs'] = str(profit['datas']['origin']['roe'])

        fenhonghtml = urlopen('https://www.zsxg.cn/api/v2/dividend/get?code={}&yearNum=50'.format(stockcode))
        fenhong = json.loads(fenhonghtml.read())
        if fenhong['message'] == '成功':
            stock_info['分红描述'] = fenhong['datas']['fh']['desc']
    except KeyError as e:
        print('提示：{}数据不全，建议跳过'.format(stockcode) + str(e))
    return stock_info


def excel_w(data):  # 定义一个写入的函数，输入的data是需要写入的数据
    wb = openpyxl.load_workbook('信息表.xlsx')  # 读取excel表格
    ws = wb['Sheet1']
    for x in data:  # 依次把信息写入excel
        ws.append(x)
    savename = '信息表.xlsx'
    wb.save(savename)  # 需要保存excel


stock_codes = ['000001.SZ', '002142.SZ', '002807.SZ', '002839.SZ', '600000.SH', '600015.SH', '600016.SH', '600036.SH',
               '600908.SH', '600919.SH', '601009.SH', '601128.SH', '601166.SH', '601169.SH', '601229.SH', '601288.SH',
               '601328.SH', '601398.SH', '601818.SH', '601939.SH', '601988.SH', '601997.SH', '601998.SH', '603323.SH',
               '601838.SH', '600926.SH', '002936.SZ', '601577.SH', '601860.SH', '002948.SZ', '600928.SH', '002958.SZ',
               '002966.SZ', '601077.SH', '601916.SH', '601658.SH', '601187.SH', '601963.SH']
stock_infos = [['代码', '名称', '收盘', '总股本', '总市值', '简介', '一级行业', '二级行业', '三级行业', '投资亮点', '风险提示', '盈利预测-同比增长率', '盈利预测-市盈率',
                '盈利预测-每股收益', '盈利预测-PEG', 'ROE', '机构持股-北向资金', '机构持股-基金', '机构持股-券商', '机构持股-QFII', '机构持股-社保', '机构持股-保险',
                'RPS强度-10', 'RPS强度-20', 'RPS强度-60', 'RPS强度-120', 'BOLL强度', '建议估值模型', 'PB', 'PB低估线', 'PB当天', 'PB状态',
                'PB提示', 'PE', 'PE低估', 'PE当天', 'PE状态', 'PE提示', 'ROEs', '分红描述']]
for stock_code in stock_codes:
    stock_infos.append(list(queryStock(stock_code).values()))
    delayseconds = random.randrange(2, 10, 1)
    print('延迟{}秒开始......'.format(delayseconds))
    time.sleep(delayseconds)
excel_w(stock_infos)

# try:
#     json.dump(stock_infos, open('{}{}.json'.format(stock, stock_infos['名称']), 'w', encoding='utf-8'),
#               ensure_ascii=False)
#     print('输出{}{}.json完毕'.format(stock, stock_infos['名称']))
# except KeyError as e:
#     print('输出提示：{}信息不全，跳过。'.format(stock))
# delayseconds = random.randrange(2, 10, 1)
# print('延迟{}秒开始......'.format(delayseconds))
# time.sleep(delayseconds)
