# -*- coding: utf-8 -*-
"""
本模块功能：投资组合的风险调整收益率教学插件
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2023年11月30日
最新修订日期：2023年11月30日
作者：王德宏 (WANG Dehong, Peter)
作者单位：北京外国语大学国际商学院
作者邮件：wdehong2000@163.com
版权所有：王德宏
用途限制：仅限研究与教学使用！
特别声明：作者不对使用本工具进行证券投资导致的任何损益负责！
"""

#==============================================================================
#关闭所有警告
import warnings; warnings.filterwarnings('ignore')
#==============================================================================
from siat.common import *
from siat.translate import *
from siat.stock import *
from siat.security_prices import *
from siat.sector_china import *
from siat.grafix import *

import pandas as pd
import akshare as ak

import datetime as dt; todaydt=str(dt.date.today())
#==============================================================================
#==============================================================================
if __name__=='__main__':
    ticker='PZU.PL'
    ticker='PZU.WA'
    
    indicators='pe'
    indicators=['pe','pb']
    indicators=['pe','pb','mv']
    
    start='2023-1-1'; end='2023-11-30'
    
    df_pl=get_stock_valuation_pl(ticker,indicators,start,end)
    
def get_stock_valuation_pl(ticker,indicators,start,end):
    """
    功能：抓取一只波兰股票估值信息pe/pb/mv
    """
    currency='PLN'
    million=1000000
    kilo=1000
    # 判断是否波兰股票
    ticker1=ticker.upper()
    result,prefix,suffix=split_prefix_suffix(ticker1)
    if (not result) or (suffix not in ['PL','WA']):
        return None
    iname=codetranslate(ticker)
    
    if isinstance(indicators,str):
        indicators=[indicators]
    
    indicators1=[]
    for i in indicators:
        indicators1=indicators1+[i.upper()]

    #屏蔽函数内print信息输出的类
    import os, sys
    class HiddenPrints:
        def __enter__(self):
            self._original_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout.close()
            sys.stdout = self._original_stdout

    df=None        
    for i in indicators1:
        t=prefix+'_'+i+'.PL'
        with HiddenPrints():
            dft=get_price(t,start,end)
        if dft is None: 
            print("  #Warning(get_stock_valuation_pl): failed to retrieve",t)
            continue
    
        dft['ticker']=ticker1
        dft['name']=iname
        dft['currency']='CNY'
        
        if i=='MV':
            #dft[i]=dft['Close'] * million
            dft[i]=dft['Close'] / kilo
        else:
            dft[i]=dft['Close']
            
        dft1=dft[[i,'name','currency']]
        
        if df is None:
            df=dft1
        else:
            #df=pd.merge(df,dft1,how='inner',left_index=True,right_index=True)
            df=pd.merge(df,dft1,how='outer',left_index=True,right_index=True)
    
    # 去掉多余的name/currency重复列
    if df is None: return None
    collist=list(df)
    if not (('name' in collist) and ('currency' in collist)):
        df.rename(columns={'name_x':'name','currency_x':'currency'},inplace=True)

    collist=list(df)
    collist1=[]
    for c in collist:
        if "_" not in c:
            collist1=collist1+[c]        

    df1=df[collist1]
    
    return df1    


#==============================================================================
if __name__=='__main__':
    ticker='JD'
    
    indicators='pe'
    indicators=['pe','pb']
    indicators=['pe','pb','mv']
    
    start='2023-1-1'; end='2023-11-30'
    
    df_us=get_stock_valuation_us(ticker,indicators,start,end)
    
def get_stock_valuation_us(ticker,indicators,start,end):
    """
    功能：抓取一只美股股票估值信息pe/pb/mv
    """
    currency='USD'
    million=1000000
    kilo=1000
    
    # 判断是否美股股票
    ticker1=ticker.upper()
    result,prefix,suffix=split_prefix_suffix(ticker1)
    if result or suffix != '': # 非美股
        return None
    iname=codetranslate(ticker)
    
    if isinstance(indicators,str):
        indicators=[indicators]
    
    indicators1=[]
    for i in indicators:
        indicators1=indicators1+[i.upper()]

    #屏蔽函数内print信息输出的类
    import os, sys
    class HiddenPrints:
        def __enter__(self):
            self._original_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout.close()
            sys.stdout = self._original_stdout

    df=None        
    for i in indicators1:
        t=prefix+'_'+i+'.US'
        with HiddenPrints():
            dft=get_price(t,start,end)
        if dft is None: 
            print("  #Warning(get_stock_valuation_us): failed to retrieve",t)
            continue
            
        dft['ticker']=ticker1
        dft['name']=iname
        dft['currency']='CNY'
        
        if i=='MV':
            #dft[i]=dft['Close'] * million
            dft[i]=dft['Close'] / kilo
        else:
            dft[i]=dft['Close']
        dft1=dft[[i,'name','currency']]
        
        if df is None:
            df=dft1
        else:
            df=pd.merge(df,dft1,how='outer',left_index=True,right_index=True)
    
    # 去掉多余的name/currency重复列
    if df is None: return None    
    collist=list(df)
    if not (('name' in collist) and ('currency' in collist)):
        df.rename(columns={'name_x':'name','currency_x':'currency'},inplace=True)

    collist=list(df)
    collist1=[]
    for c in collist:
        if "_" not in c:
            collist1=collist1+[c]        

    df1=df[collist1]
    
    return df1 

#==============================================================================
if __name__=='__main__':
    ticker='600519.SS'
    ticker='002504.SZ'
    ticker='835579.BJ'
    ticker='00700.HK'
    
    indicators='pe'
    indicators=['pe','pb']
    indicators=['pe','pb','mv']
    
    start='2023-1-1'; end='2023-11-30'
    
    df_cnhk=get_stock_valuation_cn_hk(ticker,indicators,start,end)
    
def get_stock_valuation_cn_hk(ticker,indicators,start,end):
    """
    功能：抓取一只A股或港股股票估值信息pe/pb/mv
    """
    result,startdt,enddt=check_period(start,end)
    
    yi=100000000
    ten=10
    # 判断是否A股或港股股票
    ticker1=ticker.upper()
    result,prefix,suffix=split_prefix_suffix(ticker1)
    if (not result) or (suffix not in ['SS','SZ','BJ','HK']):
        return None
    iname=codetranslate(ticker)
    
    if suffix in ['SS','SZ','BJ']: currency='CNY'
    else: currency='HKD'
    
    if isinstance(indicators,str):
        indicators=[indicators]
    
    indicators1=[]
    for i in indicators:
        indicators1=indicators1+[i.upper()]

    #屏蔽函数内print信息输出的类
    import os, sys
    class HiddenPrints:
        def __enter__(self):
            self._original_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout.close()
            sys.stdout = self._original_stdout

    # 评估时间间隔: 取样日期间隔长短不同，必须做
    delta=date_delta(start,end)
    if delta <= 365:
        period="近一年"
    elif delta <= 365*3:
        period="近三年"
    elif delta <= 365*5:
        period="近五年"
    elif delta <= 365*10:
        period="近十年"  
    else:
        period="全部"

    indicator_list_en=['PE','PB','MV','PCF']
    indicator_list_cn=['市盈率(TTM)','市净率','总市值','市现率']
    # 市现率PCF=股价 / 每股现金流
    # 市销率PS或PSR=股价 / 每股销售额
    df=None       
    for i in indicators1:
        pos=indicator_list_en.index(i)
        t=indicator_list_cn[pos]
        """
        with HiddenPrints():
            if suffix in ['SS','SZ','BJ']:
                dft=ak.stock_zh_valuation_baidu(symbol=prefix,indicator=t,period=period)
            elif suffix in ['HK']:
                dft=ak.stock_hk_valuation_baidu(symbol=prefix,indicator=t,period=period)
        """
        try:
            if suffix in ['SS','SZ','BJ']:
                dft=ak.stock_zh_valuation_baidu(symbol=prefix,indicator=t,period=period)
            elif suffix in ['HK']:
                dft=ak.stock_hk_valuation_baidu(symbol=prefix,indicator=t,period=period)
        except:
            print("  #Warning(get_stock_valuation_cn_hk): failed to retrieve",i,"for",prefix)
            continue
        
        dft['Date']=dft['date'].apply(lambda x: pd.to_datetime(x))
        dft.set_index('Date',inplace=True)
        dft['ticker']=ticker1
        dft['name']=iname
        dft['currency']='CNY'        
        if i=='MV':
            #dft[i]=dft['value'] * yi
            dft[i]=dft['value'] / ten
        else:
            dft[i]=dft['value']
        dftp=dft[(dft.index >= startdt) & (dft.index <= enddt)]
        dft1=dftp[[i,'name','currency']]
        
        if df is None:
            df=dft1
        else:
            df=pd.merge(df,dft1,how='outer',left_index=True,right_index=True)
    
    # 去掉多余的name/currency重复列
    if df is None: return None    
    collist=list(df)
    if not (('name' in collist) and ('currency' in collist)):
        df.rename(columns={'name_x':'name','currency_x':'currency'},inplace=True)

    collist=list(df)
    collist1=[]
    for c in collist:
        if "_" not in c:
            collist1=collist1+[c]        

    df1=df[collist1]
    
    return df1 

#==============================================================================
if __name__=='__main__':
    ticker='光伏设备(申万)'
    ticker='中证500'
    ticker='801735.SW'
    
    indicators='pe'
    indicators=['pe','pb','div yield']
    indicators=['pe','pb']
    
    start='2023-1-1'; end='2023-11-30'
    
    df_index=get_index_valuation_funddb(ticker,indicators,start,end)
    
def get_index_valuation_funddb(ticker,indicators,start,end):
    """
    功能：抓取一个申万或中证行业估值信息pe/pb/dividend(股息率)
    """
    result,startdt,enddt=check_period(start,end)
    
    # 判断是否申万或中证股票
    ticker1=ticker.upper()
    result,prefix,suffix=split_prefix_suffix(ticker1)
    if result and suffix in ['SW']:
        iname=industry_sw_name(prefix)+"(申万)"
    else:
        iname=ticker1
    
    if isinstance(indicators,str):
        indicators=[indicators]
    
    indicators1=[]
    for i in indicators:
        indicators1=indicators1+[i.upper()]

    indicator_list_en=['PE','PB','DIV YIELD']
    indicator_list_cn=['市盈率','市净率','股息率']
    indicators2=[]
    for i in indicators1:
        if i in indicator_list_en:
            indicators2=indicators2+[i]

    #屏蔽函数内print信息输出的类
    import os, sys
    class HiddenPrints:
        def __enter__(self):
            self._original_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout.close()
            sys.stdout = self._original_stdout

    # 股息率=每股股利 / 股价
    df=None       
    for i in indicators2:
        pos=indicator_list_en.index(i)
        t=indicator_list_cn[pos]
        try:
            with HiddenPrints():
                dft=ak.index_value_hist_funddb(symbol=iname,indicator=t)
        except:
            print("  #Error(get_industry_valuation_sw_zz): failed to retrieve info for industry",ticker)
            industry_list=list(ak.index_value_name_funddb()['指数名称'])
            industry_sw=[]
            industry_zz=[]
            industry_gz=[]
            industry_others=[]
            for i in industry_list:
                if '(申万)' in i:
                    industry_sw=industry_sw+[i]
                elif '中证' in i:
                    industry_zz=industry_zz+[i]
                elif '国证' in i:
                    industry_gz=industry_gz+[i] 
                else:
                    industry_others=industry_others+[i]
            print("  Supported industry indexes:")
            printlist(industry_sw,numperline=5,beforehand='  ',separator=' ')
            printlist(industry_zz,numperline=5,beforehand='  ',separator=' ')
            printlist(industry_gz,numperline=5,beforehand='  ',separator=' ')
            printlist(industry_others,numperline=5,beforehand='  ',separator=' ')
            
            return None
        
        if dft is None: continue
        
        dft['Date']=dft['日期'].apply(lambda x: pd.to_datetime(x))
        dft.set_index('Date',inplace=True)
        dft['name']=iname
        dft['currency']=''
        dft[i]=dft[t]
        dftp=dft[(dft.index >= startdt) & (dft.index <= enddt)]
        
        dft1=dftp[[i,'name','currency']]
        """
        if not (dft1 is None):
            columns=create_tuple_for_columns(dft1,iname)
            dft1.columns=pd.MultiIndex.from_tuples(columns)        
        """
        if df is None:
            df=dft1
        else:
            df=pd.merge(df,dft1,how='outer',left_index=True,right_index=True)
    
    # 去掉多余的name/currency重复列
    if df is None: return None    
    collist=list(df)
    if not (('name' in collist) and ('currency' in collist)):
        df.rename(columns={'name_x':'name','currency_x':'currency'},inplace=True)

    collist=list(df)
    collist1=[]
    for c in collist:
        if "_" not in c:
            collist1=collist1+[c]        

    df1=df[collist1]
    
    return df1 

#==============================================================================
if __name__=='__main__':
    print(is_alphanumeric("abc123"))   # True
    print(is_alphanumeric("abcd123!"))  # False
    print(is_alphanumeric("1234567890")) # True
    print(is_alphanumeric("Hello World")) # False
    print(is_alphanumeric("中证500"))
 
def is_alphanumeric(string):
    import re
    pattern = r'^[a-zA-Z0-9]+$' # 定义正则表达式模式
    
    if re.match(pattern, string):
        return True
    else:
        return False


#==============================================================================
if __name__=='__main__':
    code='H30533.ZZ'
    code='801730.SW'
    
    funddb_name(code)
    

def funddb_name(code):
    """
    翻译指数代码为韭圈儿名称。指数估值专用！
    输入：指数代码。输出：韭圈儿指数名称
    """
    import pandas as pd
    ecdict=pd.DataFrame([
        
        # 申万行业/主题指数
        ['801735.SW','光伏设备(申万)'],
        ['801730.SW','电力设备(申万)'],
        ['801780.SW','银行(申万)'],
        ['801740.SW','国防军工(申万)'],
        ['801720.SW','建筑装饰(申万)'],
        ['801110.SW','家用电器(申万)'],
        ['801102.SW','通信设备(申万)'],
        ['801194.SW','保险Ⅱ(申万)'],
        ['801770.SW','通信(申万)'],
        ['801050.SW','有色金属(申万)'],
        ['801812.SW','中盘指数(申万)'],
        ['801152.SW','生物制品(申万)'],
        ['801811.SW','大盘指数(申万)'],
        ['801970.SW','环保(申万)'],
        ['801120.SW','食品饮料(申万)'],
        ['801170.SW','交通运输(申万)'],
        ['801150.SW','医药生物(申万)'],
        ['801980.SW','美容护理(申万)'],
        ['801160.SW','公用事业(申万)'],
        ['801950.SW','煤炭(申万)'],
        ['801151.SW','化学制药(申万)'],
        ['801130.SW','纺织服饰(申万)'],
        ['801960.SW','石油石化(申万)'],
        ['801890.SW','机械设备(申万)'],
        ['801790.SW','非银金融(申万)'],
        ['801813.SW','小盘指数(申万)'],
        ['801030.SW','基础化工(申万)'],
        ['801193.SW','券商Ⅱ(申万)'],
        ['801210.SW','社会服务(申万)'],
        ['801140.SW','轻工制造(申万)'],
        ['801760.SW','传媒(申万)'],
        ['801710.SW','建筑材料(申万)'],
        ['801080.SW','电子(申万)'],
        ['801040.SW','钢铁(申万)'],
        ['801200.SW','商贸零售(申万)'],        
        ['801017.SW','养殖业(申万)'],        
        ['801180.SW','房地产(申万)'],        
        ['801230.SW','综合(申万)'],
        ['801010.SW','农林牧渔(申万)'],
        ['801880.SW','汽车(申万)'],
        ['801736.SW','风电设备(申万)'],
        ['801750.SW','计算机(申万)'],

        # 沪深交易所行业指数
        ['399976.SZ','CS新能车'],
        ['399995.SZ','中证基建工程'],
        ['399812.SZ','养老产业'],
        ['000986.SS','全指能源'],        
        ['399986.SZ','中证银行'],        
        ['000992.SS','全指金融地产'],        
        ['000991.SS','全指医药'],        
        ['399285.SZ','物联网50'],        
        ['399997.SZ','中证白酒'],        

        ['000987.SS','全指材料'],
        ['000993.SS','全指信息'],
        ['399610.SZ','TMT50'],
        ['399975.SZ','证券公司'],        
        ['399804.SZ','中证体育'],        
        ['000992.SS','全指金融地产'],        
        ['000991.SS','全指医药'],        
        ['399285.SZ','物联网50'],        
        ['399997.SZ','中证白酒'], 
        
        # 中证行业指数
        ['H30533.ZZ','中国互联网50'],
        ['931151.ZZ','光伏产业'],
        ['930614.ZZ','环保50'],
        ['000812.ZZ','细分机械'],
        ['931755.ZZ','SEEE碳中和'],
        ['931719.ZZ','CS电池'],
        ['930771.ZZ','中证新能源'],
        ['930697.ZZ','家用电器'],
        ['000994.ZZ','全指通信'],
        ['931160.ZZ','通信设备'],
        
        ['930820.ZZ','CS高端制'],          
        ['000811.ZZ','细分有色'],  
        ['930632.ZZ','CS稀金属'],  
        ['000986.SS','全指能源'],  
        ['930716.ZZ','CS物流'],  
        ['000990.ZZ','全指消费'],  
        ['930726.ZZ','CS生医'],  
        ['930712.ZZ','CS物联网'],  
        ['930598.ZZ','稀土产业'],  
        ['H30178.ZZ','医疗保健'],  
        
        ['931079.ZZ','5G通信'],  
        ['931456.ZZ','中国教育'],  
        ['931484.ZZ','CS医药创新'],  
        ['H30217.ZZ','医疗器械'],  
        ['H30205.ZZ','饮料指数'],          
        ['000995.ZZ','全指公用'],  
        ['000813.ZZ','细分化工'],  
        ['930651.ZZ','CS计算机'],  
        ['H30199.ZZ','中证全指电力指数'],  
        ['930652.ZZ','CS电子'],#中证电子指数
        
        ['H30202.ZZ','软件指数'],  
        ['931009.ZZ','建筑材料'],  
        ['930713.ZZ','CS人工智'],  
        ['h30184.ZZ','中证全指半导体'],  
        ['000949.ZZ','中证农业'],   
        ['931775.ZZ','中证全指房地产'],  

        
        # 主要市场通用指数
        ['399006.SZ','创业板指'],#创业板指数
        ['^FTSE','英国富时100'],
        ['^HSI','恒生指数'],
        ['000009.SS','上证380'],
        ['^CAC','法国CAC40'],
        ['^RTS','俄罗斯RTS'],
        ['399102.SZ','创业板综'],#创业板综合指数
        ['^VN30','胡志明指数'],
        ['000010.SS','上证180'],
        ['000300.SS','沪深300'],
        
        ['000906.SS','中证800'],
        ['399330.SZ','深证100'],
        ['^BSESN','印度SENSEX30'],
        ['399001.SZ','深证成指'],
        ['000905.SS','中证500'],
        ['000001.SS','上证指数'],
        ['000016.SS','上证50'],
        ['000852.SS','中证1000'],
        ['^N225','日经225'],
        ['399303.SZ','国证2000'],        
        
        ['000903.SS','中证100'],
        ['^SPX','标普500'],['^GSPC','标普500'],
        ['899050.BJ','北证50'],
        ['^KS11','韩国综合指数'],
        ['^DJI','道琼斯工业指数'],
        ['^NDX','纳斯达克100'],
        ['932000.ZZ','中证2000'],#中证规模指数系列
        ['^AXAT','澳洲标普200'],#澳大利亚标普200指数
        
        ], columns=['eword','cword'])

    try:
        cword=ecdict[ecdict['eword']==code]['cword'].values[0]
    except:
        #未查到代码名称，返回原代码
        cword=code
   
    return cword
#==============================================================================

if __name__=='__main__':
    tickers='PZU.PL'
    tickers='JD'
    tickers='600519.SS'
    tickers='00700.HK'
    tickers='光伏设备(申万)'
    tickers='中证500'
    tickers='801735.SW'
    
    tickers=['PZU.PL','WIG.PL']
    tickers=['PZU.PL','JD','600519.SS','00700.HK','801735.SW','光伏设备(申万)','中证500']
    
    indicators='pe'
    indicators=['pe','pb']
    indicators=['pe','pb','mv']
    
    start='2023-1-1'; end='2023-11-30'
    
    df_mix=get_valuation(tickers,indicators,start,end)

def get_valuation(tickers,indicators,start,end):
    """
    功能：获取估值信息pe/pb/mv
    若tickers为多个，则indicators取第一个
    若tickers为单个，则indicators取所有
    """
    
    if isinstance(tickers,str):
        tickers=[tickers]

    # 若遇到指数，先转换为韭圈儿的行业名称，以免被误认为股票代码
    tickers1=[]
    for t in tickers:
        t1=funddb_name(t)
        tickers1=tickers1+[t1]
        
    if isinstance(indicators,str):
        indicators=[indicators]

    # 若为多个证券代码，则仅取第一个指标        
    if len(tickers)>1:
        indicators1=[indicators[0]]
    else:
        indicators1=indicators
    
    # 百度股市百事通不支持指数估值，遇到指数代码需要先转为名称获取韭圈儿估值数据
    
    
    df=None
    for t in tickers1:
        print("  Searchng valuation info for",t,"......")
        t1=t.upper()
        result,prefix,suffix=split_prefix_suffix(t1)
        iname=codetranslate(t1)
        
        gotit=False
        # A股或港股？
        if not gotit and (result and suffix in ['SS','SZ','BJ','HK']):        
            dft=get_stock_valuation_cn_hk(t1,indicators1,start,end)
            if dft is not None: gotit=True
        
        # 波兰股？
        if not gotit and (result and suffix in ['PL','WA']):
            dft=get_stock_valuation_pl(t1,indicators1,start,end)
            if dft is not None: gotit=True

        # 申万指数代码？
        if not gotit and (result and suffix in ['SW']):
            dft=get_index_valuation_funddb(t1,indicators1,start,end)
            if dft is not None: 
                gotit=True 
                iname=industry_sw_name(t1)
              
        # 美股？
        if not gotit and (not result and (is_alphanumeric(prefix) or '^' in prefix)):
            dft=get_stock_valuation_us(t1,indicators1,start,end)
            if dft is not None: gotit=True
            
       # 行业指数名称？     
        if not gotit and (not result):
           dft=get_index_valuation_funddb(t1,indicators1,start,end)
           if dft is not None: gotit=True
           
        if not gotit:
           print("  #Warning(get_valuation): failed to retrieve info for",t1)
           continue
       
        if not (dft is None):
            columns=create_tuple_for_columns(dft,iname)
            dft.columns=pd.MultiIndex.from_tuples(columns)  
        
        # 合成    
        if df is None:
            df=dft
        else:
            #df=pd.merge(df,dft,how='inner',left_index=True,right_index=True)
            df=pd.merge(df,dft,how='outer',left_index=True,right_index=True)
    
    # 缺失值填充
    if not (df is None):
        #df.fillna(method='backfill',inplace=True)
        df.fillna(method='ffill',inplace=True)
    
    return df


#==============================================================================
if __name__=='__main__':
    tickers='PZU.PL'
    indicators='PE'
    start='2023-1-1'; end='2023-11-30'
    loc1='best'
    
    tickers='PZU.PL'
    indicators=['PE','PB']
    start='2023-1-1'; end='2023-11-30'
    twinx=True
    loc1='lower left'; loc2='upper right'
    
    tickers=['JD','PDD']
    indicators='PE'
    start='2023-1-1'; end='2023-11-30'
    twinx=True
    loc1='lower left'; loc2='upper right'
    
    tickers=['600519.SS','000858.SZ']
    indicators='PE'
    start='2023-1-1'; end='2023-11-30'
    twinx=True
    loc1='lower left'; loc2='upper right'
    
    tickers=['JD','PDD','BABA']
    indicators='PE'
    start='2023-1-1'; end='2023-11-30'
    loc1='best'
    
    tickers='JD'
    indicators=['PE','PB','MV']
    start='2023-1-1'; end='2023-11-30'
    loc1='best'

def security_valuation(tickers,indicators,start,end, \
                       twinx=False,loc1='best',loc2='best', \
                       graph=True,annotate=False):
    """
    功能：绘制估值走势
    """
    
    # 获取估值信息
    df=get_valuation(tickers,indicators,start,end)
    if df is None:
        print("  #Warning(security_valuation): retrieved none of",indicators,"for",tickers)
        return None

    if not graph: return df

    # 判断估值信息结构
    names=[]
    indicators=[]
    
    mcollist=list(df)
    for mc in mcollist:
        if mc[0] not in ['name','currency']:
            indicators=indicators+[mc[0]]
            names=names+[mc[1]]
    
    names1=list(set(names))
    indicators1=list(set(indicators))
    
    name_num=len(names1)
    indicator_num=len(indicators1)

    import datetime
    # 绘制一条线+均值/中位数虚线
    if name_num * indicator_num == 1:
        i=indicators1[0]
        t=names1[0]
        df2=df[i]
        df2.rename(columns={t:i},inplace=True)
        
        df2['平均值']=df2[i].mean()
        df2['中位数']=df2[i].median()
        
        titletxt="证券估值走势："+t   
        
        footnote1="注：PE为市盈率，PB为市净率，MV为总市值(十亿交易所所在地货币单位)"
        todaydt = datetime.date.today()
        footnote9="数据来源: baidu/stooq/funddb/swhysc，"+str(todaydt)
        footnote=footnote1+'\n'+footnote9
        
        ylabeltxt=i
        
        draw_lines(df2,y_label=ylabeltxt,x_label=footnote, \
                   axhline_value=0,axhline_label='', \
                   title_txt=titletxt,data_label=False, \
                   resample_freq='D',loc=loc1)        
        
        return df
        
    # 绘制双线: 一只证券，两个指标。允许twinx双轴绘图
    if name_num == 1 and indicator_num == 2: 
        t=names1[0]
        i1=indicators1[0]; i2=indicators1[1]
        df2_1=df[i1]; df2_2=df[i2]
        df2_1.rename(columns={t:i1},inplace=True)
        df2_2.rename(columns={t:i2},inplace=True)
        
        titletxt="证券估值走势对比："+t   
        
        footnote1="注：PE为市盈率，PB为市净率，MV为总市值(十亿交易所所在地货币单位)"
        todaydt = datetime.date.today()
        footnote9="数据来源: baidu/stooq/funddb/swhysc，"+str(todaydt)
        footnote=footnote1+'\n'+footnote9
        
        colname1=label1=i1
        colname2=label2=i2
        
        plot_line2(df2_1,'',colname1,label1, \
                   df2_2,'',colname2,label2, \
                   ylabeltxt='',titletxt=titletxt,footnote=footnote, \
                   twinx=twinx, \
                   resample_freq='D',loc1=loc1,loc2=loc2, \
                   color1='red',color2='blue')
        return df
   
    # 绘制双线: 两只证券，一个指标。允许twinx双轴绘图
    if name_num == 2 and indicator_num == 1:
        t1=names1[0]; t2=names1[1]
        i=indicators1[0]
        df2_1=pd.DataFrame(df[i,t1])[i]; df2_2=pd.DataFrame(df[i,t2])[i]
        df2_1.rename(columns={t1:i},inplace=True)
        df2_2.rename(columns={t2:i},inplace=True)
        
        titletxt="证券估值走势对比："+i   
        
        footnote1="注：PE为市盈率，PB为市净率，MV为总市值(十亿交易所所在地货币单位)"
        todaydt = datetime.date.today()
        footnote9="数据来源: baidu/stooq/funddb/swhysc，"+str(todaydt)
        footnote=footnote1+'\n'+footnote9
        
        colname1=i; label1=t1
        colname2=i; label2=t2
        
        if twinx:
            ylabeltxt=''
        else:
            ylabeltxt=i
        
        plot_line2(df2_1,'',colname1,label1, \
                   df2_2,'',colname2,label2, \
                   ylabeltxt=ylabeltxt,titletxt=titletxt,footnote=footnote, \
                   twinx=twinx, \
                   resample_freq='D',loc1=loc1,loc2=loc2, \
                   color1='red',color2='blue')

        return df                
   
    # 绘制多线：多只证券，一个指标。简单多线绘图
    if name_num > 2 and indicator_num == 1: 
        i=indicators1[0]
        df2=df[i]
        
        titletxt="证券估值走势："+i   
        
        footnote1="注：PE为市盈率，PB为市净率，MV为总市值(十亿交易所所在地货币单位)"
        todaydt = datetime.date.today()
        footnote9="数据来源: baidu/stooq/funddb/swhysc，"+str(todaydt)
        footnote=footnote1+'\n'+footnote9
        
        ylabeltxt=i
        
        draw_lines(df2,y_label=ylabeltxt,x_label=footnote, \
                   axhline_value=0,axhline_label='', \
                   title_txt=titletxt,data_label=False, \
                   resample_freq='D',loc=loc1,annotate=annotate)        
        
        return df        
   
    # 绘制多线：一只证券，多个指标。简单多线绘图
    if name_num == 1 and indicator_num > 2: 
        t=names1[0]
        df2=None
        for i in indicators1:
            dft=pd.DataFrame(df[i,t])[i]
            dft.rename(columns={t:i},inplace=True)
            
            if df2 is None:
                df2=dft
            else:
                df2=pd.merge(df2,dft,left_index=True,right_index=True)
        
        titletxt="证券估值走势："+t   
        
        footnote1="注：PE为市盈率，PB为市净率，MV为总市值(十亿交易所所在地货币单位)"
        todaydt = datetime.date.today()
        footnote9="数据来源: baidu/stooq/funddb/swhysc，"+str(todaydt)
        footnote=footnote1+'\n'+footnote9
        
        ylabeltxt=''
        
        draw_lines(df2,y_label=ylabeltxt,x_label=footnote, \
                   axhline_value=0,axhline_label='', \
                   title_txt=titletxt,data_label=False, \
                   resample_freq='D',loc=loc1,annotate=annotate)        
        
        return df 
                
        
        
#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================

