#coding=gbk
Quarter = ('0331', '0630', '0930', '1231')
hope_dividend_ratio = 0.04
ShareBank = []
share = {}

work_catalog = "c:\PythonWork"
bank_name = "\ShareBank.dat"

TOKEN = 'c27f964551786735a0cebbc26a743d0e18b06e9181f2166632964e37'
url_quotation_before = "http://hq.sinajs.cn/list="

#######################################################
#    dt['bps']                      每股净资产
#    dt['convert']                  转送股
#    dt['convert_ratio']            股份调整率
#    dt['current_ratio']            流动比率
#    dt['dividend']                 历年分红
#    dt['eps']                      基本每股收益
#    dt['industry']                 行业
#    dt['ocfps']                    每股经营活动产生的现金流量净额
#    dt['roe']                      ROE
#    dt['total_share']              总股本
#    dt['profit_dedt_qtrs']         最近几个季度扣除非经常性损益后的净利润
#    dt['profit_dedt_years']        最近几年扣除非经常性损益后的净利润
#    rt['avg_div_rate']             5年平均分红率
#    rt['div_rate']                 5年分红率
#    rt['EPS_ttm']                  EPS_ttm
#    rt['gold_include']             含金量
#    rt['last_year_div']            最新年度分红
#    rt['profit_dedt_acc']          净利润季报增速
#    cp['exp_div_ratio']            预期股息率 =  5年平均分红率  *  EPS_ttm / price
#    cp['div_status']               是否保底分红率小于5年平均分红率
#    cp['hope_div']                 期望的保底分红
#    cp['safe_div']                 保底分红率 = 期望保底分红 /EPS_TTM
#    cp['stk_div_ratio']            当前股息率
#######################################################