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


stock_codes = ['601398.SH', '600036.SH', '601939.SH', '601288.SH', '601988.SH', '600276.SH', '601166.SH', '000001.SZ',
               '601088.SH', '601328.SH', '600585.SH', '002142.SZ', '601998.SH', '600016.SH', '601818.SH', '000538.SZ',
               '601360.SH', '601229.SH', '601169.SH', '601006.SH', '600015.SH', '002007.SZ', '600919.SH', '300628.SZ',
               '300408.SZ', '603369.SH', '600426.SH', '300595.SZ', '300529.SZ', '300496.SZ', '600872.SH', '002624.SZ',
               '603638.SH', '600161.SH', '300012.SZ', '600674.SH', '603866.SH', '300357.SZ', '002507.SZ', '600299.SH',
               '002603.SZ', '300726.SZ', '002690.SZ', '603027.SH', '002901.SZ', '002372.SZ', '600529.SH', '600380.SH',
               '002595.SZ', '002756.SZ', '600305.SH', '601997.SH', '002152.SZ', '600867.SH', '002867.SZ', '600563.SH',
               '300623.SZ', '300373.SZ', '603025.SH', '000975.SZ', '300088.SZ', '002643.SZ', '600535.SH', '603868.SH',
               '601128.SH', '300298.SZ', '002626.SZ', '300630.SZ', '300685.SZ', '601965.SH', '601952.SH', '603730.SH',
               '603826.SH', '002262.SZ', '002191.SZ', '300451.SZ', '603305.SH', '002233.SZ', '601000.SH', '300294.SZ',
               '603599.SH', '600933.SH', '002677.SZ', '002320.SZ', '600195.SH', '603416.SH', '002651.SZ', '600908.SH',
               '300735.SZ', '002818.SZ', '002839.SZ', '002293.SZ', '603960.SH', '300443.SZ', '300639.SZ', '600329.SH',
               '300394.SZ', '300696.SZ', '600993.SH', '002275.SZ', '002038.SZ', '002912.SZ', '601801.SH', '002807.SZ',
               '603181.SH', '603323.SH', '300470.SZ', '002833.SZ', '603229.SH', '000650.SZ', '002484.SZ', '300590.SZ',
               '002880.SZ', '300722.SZ', '601858.SH', '603987.SH', '000848.SZ', '000029.SZ', '002884.SZ', '300396.SZ',
               '300196.SZ', '300429.SZ', '300723.SZ', '603110.SH', '603566.SH', '300653.SZ', '600750.SH', '002327.SZ',
               '603556.SH', '601566.SH', '002222.SZ', '300617.SZ', '603096.SH', '002540.SZ', '300684.SZ', '603367.SH',
               '603535.SH', '300127.SZ', '002801.SZ', '603896.SH', '000915.SZ', '300481.SZ', '300259.SZ', '002724.SZ',
               '300559.SZ', '300690.SZ', '300342.SZ', '002550.SZ', '300174.SZ']
stock_infos = [['代码', '名称', '收盘', '总股本', '总市值', '简介', '一级行业', '二级行业', '三级行业', '投资亮点', '风险提示', '盈利预测-同比增长率', '盈利预测-市盈率',
                '盈利预测-每股收益', '盈利预测-PEG', 'ROE', '机构持股-北向资金', '机构持股-基金', '机构持股-券商', '机构持股-QFII', '机构持股-社保', '机构持股-保险',
                'RPS强度-10', 'RPS强度-20', 'RPS强度-60', 'RPS强度-120', 'BOLL强度', '建议估值模型', 'PB', 'PB低估线', 'PB当天', 'PB状态',
                'PB提示', 'PE', 'PE低估', 'PE当天', 'PE状态', 'PE提示', 'ROEs', '分红描述']]
for stock_code in stock_codes:
    stock_infos.append(list(queryStock(stock_code).values()))
    print('输出{}完毕'.format(stock_code))
    delayseconds = random.randrange(1, 30, 1)
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
