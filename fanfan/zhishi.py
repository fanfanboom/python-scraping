from urllib.request import urlopen
import json

stockcode = '601166.SH'

html = urlopen('https://www.zsxg.cn/api/v2/capital/info?code={}&yearNum=6'.format(stockcode))
sto = json.loads(html.read())
if sto['message'] == '成功':
    daima = sto['datas']['code']
    mingcheng = sto['datas']['name']
    shoupanjia = sto['datas']['close']
    jianjie = sto['datas']['briefing']

    hangye1 = sto['datas']['industry']
    hangye2 = sto['datas']['industry2']
    hangye3 = sto['datas']['industry3']

    touziliangdian = sto['datas']['comment_new']['positive_new']
    fengxiantishi = sto['datas']['comment_new']['unpositive_new']

    yingliyuce_tongbizengzhanglv = sto['datas']['forGrowthRate']
    yingliyuce_shiyinglv = sto['datas']['forPE']
    yingliyuce_meigushouyi = sto['datas']['forEPS']
    yingliyuce_peg = sto['datas']['forPeg']

    roe = sto['datas']['roe']
    jigouchigu = sto['datas']['instholdpct']['list']

    rpsxiangdu10 = sto['datas']['rpsMap']['rps10_today']
    rpsxiangdu20 = sto['datas']['rpsMap']['rps20_today']
    rpsxiangdu60 = sto['datas']['rpsMap']['rps60_today']
    rpsxiangdu120 = sto['datas']['rpsMap']['rps120_today']

    bollcomment = sto['datas']['boll']['comment']

    guzhi_recommend = sto['datas']['pepbMap']['recommend']

    pb = sto['datas']['pepbMap']['pb']
    pb_digu = sto['datas']['pepbMap']['pbMin']
    pb_dangtian = sto['datas']['pepbMap']['pbY']
    pb_zhuangtai = sto['datas']['pepbMap']['pbStatus']
    pb_tishi = sto['datas']['pepbMap']['pbContent']

    pe = sto['datas']['pepbMap']['pe']
    pe_digu = sto['datas']['pepbMap']['peMin']
    pe_dangtian = sto['datas']['pepbMap']['peY']
    pe_zhuangtai = sto['datas']['pepbMap']['peStatus']
    pe_tishi = sto['datas']['pepbMap']['peContent']

    print(guzhi_recommend)

profithtml = urlopen(
    'https://www.zsxg.cn/api/v2/quarter/profitability?code={}&compareCode=&types=roi%2CprofitMargin'
    '%2CcostMargin%2Cdupont&yearNum=12'.format(stockcode))
profit = json.loads(profithtml.read())
if profit['message'] == '成功':
    roe = profit['datas']['dupont']['roeDupont1']['roe']
    roes = profit['datas']['origin']['roe']
    print(roes)

fenhonghtml = urlopen('https://www.zsxg.cn/api/v2/dividend/get?code={}&yearNum=50'.format(stockcode))
fenhong = json.loads(fenhonghtml.read())
if fenhong['message'] == '成功':
    fenhongmiaoshu = fenhong['datas']['fh']['desc']
    print(fenhongmiaoshu)
