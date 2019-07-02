#coding=gbk
Quarter = ('0331', '0630', '0930', '1231')
hope_dividend_ratio = 0.04
ShareBank = []
share = {}

work_catalog = "c:\PythonWork"
bank_name = "\ShareBank.dat"

TOKEN = 'c27f964551786735a0cebbc26a743d0e18b06e9181f2166632964e37'
url_quotation_before = "http://hq.sinajs.cn/list="

######################################################
#    dt['convert']                  ת�͹�
#    dt['current_ratio']            ��������
#    dt['dividend']                 ����ֺ�
#    dt['industry']                 ��ҵ
#    dt['n_income']                 ������
#    dt['ocfps']                    ÿ�ɾ�Ӫ��������ֽ���������
#    dt['total_share']              �ܹɱ�
#    dt['profit_dedt']              �۳��Ǿ����������ľ�����
#    rt['avg_div_rate']             5��ƽ���ֺ���
#    rt['eps']                      ����ÿ������
#    rt['EPS_ttm']                  EPS_ttm
#    rt['convert_rate']             �ɷݵ�����
#    rt['div_rate']                 5��ֺ���
#    rt['gold_include']             ������
#    rt['last_year_div']            ������ȷֺ�
#    rt['profit_dedt_acc']          �����󼾱�����
#    cp['exp_div_ratio']            Ԥ�ڹ�Ϣ�� =  5��ƽ���ֺ���  *  EPS_ttm / price
#    cp['div_status']               �Ƿ񱣵׷ֺ���С��5��ƽ���ֺ���
#    cp['hope_div']                 �����ı��׷ֺ�
#    cp['safe_div']                 ���׷ֺ��� = �������׷ֺ� /EPS_TTM
#    cp['stk_div_ratio']            ��ǰ��Ϣ��
#######################################################