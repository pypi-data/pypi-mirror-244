# -*- coding: utf-8 -*-
"""
本模块功能：SIAT公共基础函数
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2019年7月16日
最新修订日期：2020年3月28日
作者：王德宏 (WANG Dehong, Peter)
作者单位：北京外国语大学国际商学院
作者邮件：wdehong2000@163.com
版权所有：王德宏
用途限制：仅限研究与教学使用，不可商用！商用需要额外授权。
特别声明：作者不对使用本工具进行证券投资导致的任何损益负责！
"""

#==============================================================================
#关闭所有警告
import warnings; warnings.filterwarnings('ignore')

#==============================================================================
SUFFIX_LIST_CN=['SS','SZ','BJ','NQ']
import pandas as pd
#==============================================================================
#设置全局语言环境
import pickle

def check_language():
    """
    查询全局语言设置
    """
    try:
        with open('siat_language.pkl','rb') as file:
            lang=pickle.load(file)
    except:
        lang='Chinese'
        
    return lang

def set_language(lang='Chinese'):
    """
    修改全局语言设置
    """
    
    if lang in ['English','Chinese']:
        with open('siat_language.pkl','wb') as file:
            pickle.dump(lang,file)
        print("  Global language is set to",lang)
    else:
        print("  Warning: undefined language",lang)
        
    return

def text_lang(txtcn,txten):
    """
    功能：适应双语文字，中文环境返回txtcn，英文环境返回txten
    """
    lang=check_language()
    
    if lang=='Chinese': txt=txtcn
    else: txt=txten
    
    return txt
#==============================================================================

def today():
    """
    返回今日的日期
    """
    import datetime; now=datetime.datetime.now()
    jinri=now.strftime("%Y-%m-%d")
    
    return jinri

if __name__=='__main__':
    today()
#==============================================================================

def now():
    """
    返回今日的日期
    """
    import datetime; dttime=datetime.datetime.now()
    xianzai=dttime.strftime("%Y-%m-%d %H:%M:%S")
    
    return xianzai

if __name__=='__main__':
    now()
#==============================================================================

def hello():
    """
    返回当前环境信息
    """
    #当前系统信息
    import platform
    ossys=platform.system()
    (arch,_)=platform.architecture()
    osver=platform.platform()    
    print(ossys,arch,osver)
    
    #Python版本信息
    import sys
    pyver=sys.version
    pos=pyver.find(' ')
    pyver1=pyver[:pos]
    print("Python",pyver1,end=', ')
    
    #siat版本信息
    import pkg_resources
    siatver=pkg_resources.get_distribution("siat").version    
    print("siat",siatver)
    
    #运行环境
    import sys; pypath=sys.executable
    pos=pypath.rfind('\\')
                     
    pypath1=pypath[:pos]
    print("Located in",pypath1)

    from IPython import get_ipython
    ipy_str = str(type(get_ipython())) 
    if 'zmqshell' in ipy_str:
        print("Working in Jupyter environment")
    else:
        print("NOT in Jupyter environment")
    
    #当前日期时间
    print("Currently",now())
    
    return

if __name__=='__main__':
    hello()
#==============================================================================
def ticker_check(ticker, source="yahoo"):
    """
    检查证券代码，对于大陆证券代码、香港证券代码和东京证券代码进行修正。
    输入：证券代码ticker，数据来源source。
    上交所证券代码后缀为.SS或.SH或.ss或.sh，深交所证券代码为.SZ或.sz
    港交所证券代码后缀为.HK，截取数字代码后4位
    东京证交所证券代码后缀为.T，截取数字代码后4位
    source：yahoo或tushare
    返回：字母全部转为大写。若是大陆证券返回True否则返回False。
    若选择yahoo数据源，上交所证券代码转为.SS；
    若选择tushare数据源，上交所证券代码转为.SH
    """
    #测试用，完了需要注释掉
    #ticker="600519.sh"
    #source="yahoo"
    
    #将字母转为大写
    ticker1=ticker.upper()
    #截取字符串最后2/3位
    suffix2=ticker1[-2:]
    suffix3=ticker1[-3:]
    
    #判断是否大陆证券
    if suffix3 in ['.SH', '.SS', '.SZ']:
        prc=True
    else: prc=False

    #根据数据源的格式修正大陆证券代码
    if (source == "yahoo") and (suffix3 in ['.SH']):
        ticker1=ticker1.replace(suffix3, '.SS')        
    if (source == "tushare") and (suffix3 in ['.SS']):
        ticker1=ticker1.replace(suffix3, '.SH')  

    #若为港交所证券代码，进行预防性修正，截取数字代码后4位，加上后缀共7位
    if suffix3 in ['.HK']:
        ticker1=ticker1[-7:]     

    #若为东交所证券代码，进行预防性修正，截取数字代码后4位，加上后缀共6位
    if suffix2 in ['.T']:
        ticker1=ticker1[-6:]  
    
    #返回：是否大陆证券，基于数据源/交易所格式修正后的证券代码
    return prc, ticker1        

#测试各种情形
if __name__=='__main__':
    prc, ticker=ticker_check("600519.sh","yahoo")
    print(prc,ticker)
    print(ticker_check("600519.SH","yahoo"))    
    print(ticker_check("600519.ss","yahoo"))    
    print(ticker_check("600519.SH","tushare"))    
    print(ticker_check("600519.ss","tushare"))    
    print(ticker_check("000002.sz","tushare"))
    print(ticker_check("000002.sz","yahoo"))
    print(ticker_check("00700.Hk","yahoo"))
    print(ticker_check("99830.t","yahoo"))

#==============================================================================
def tickers_check(tickers, source="yahoo"):
    """
    检查证券代码列表，对于大陆证券代码、香港证券代码和东京证券代码进行修正。
    输入：证券代码列表tickers，数据来源source。
    上交所证券代码后缀为.SS或.SH或.ss或.sh，深交所证券代码为.SZ或.sz
    港交所证券代码后缀为.HK，截取数字代码后4位
    东京证交所证券代码后缀为.T，截取数字代码后4位
    source：yahoo或tushare
    返回：证券代码列表，字母全部转为大写。若是大陆证券返回True否则返回False。
    若选择yahoo数据源，上交所证券代码转为.SS；
    若选择tushare数据源，上交所证券代码转为.SH
    """
    #检查列表是否为空
    if tickers[0] is None:
        print("*** 错误#1(tickers_check)，空的证券代码列表:",tickers)
        return None         
    
    tickers_new=[]
    for t in tickers:
        _, t_new = ticker_check(t, source=source)
        tickers_new.append(t_new)
    
    #返回：基于数据源/交易所格式修正后的证券代码
    return tickers_new

#测试各种情形
if __name__=='__main__':
    tickers=tickers_check(["600519.sh","000002.sz"],"yahoo")
    print(tickers)
#==============================================================================
def check_period(fromdate, todate):
    """
    功能：根据开始/结束日期检查日期与期间的合理性
    输入参数：
    fromdate：开始日期。格式：YYYY-MM-DD
    enddate：开始日期。格式：YYYY-MM-DD
    输出参数：
    validity：期间合理性。True-合理，False-不合理
    start：开始日期。格式：datetime类型
    end：结束日期。格式：datetime类型
    """
    import pandas as pd
    
    #测试开始日期的合理性
    try:
        start=pd.to_datetime(fromdate)
    except:
        print("*** #Error(check_period), invalid date:",fromdate)
        return None, None, None         
    
    #测试结束日期的合理性
    try:
        end=pd.to_datetime(todate)
    except:
        print("  #Error(check_period): invalid date:",todate)
        return None, None, None          
    
    #测试日期期间的合理性
    if start > end:
        print("  #Error(check_period): invalid period: from",fromdate,"to",todate)
        return None, None, None     

    return True, start, end

if __name__ =="__main__":
    check_period('2020-1-1','2020-2-4')
    check_period('2020-1-1','2010-2-4')
    
    start='2020-1-1'; end='2022-12-20'
    result,startpd,endpd=check_period(start,end)

#==============================================================================
def date_adjust(basedate, adjust=0):
    """
    功能：将给定日期向前或向后调整特定的天数
    输入：基础日期，需要调整的天数。
    basedate: 基础日期。
    adjust：需要调整的天数，负数表示向前调整，正数表示向后调整。
    输出：调整后的日期。
    """
    #检查基础日期的合理性
    import pandas as pd    
    try:
        bd=pd.to_datetime(basedate)
    except:
        print("  #Error(date_adjust): invalid:",basedate)
        return None

    #调整日期
    from datetime import timedelta
    nd = bd+timedelta(days=adjust)    
    
    #重新提取日期
    newdate=nd.date()   
    return str(newdate)
 
if __name__ =="__main__":
    basedate='2020-3-17' 
    adjust=-365    
    newdate = date_adjust(basedate, adjust)
    print(newdate)    

#==============================================================================
if __name__ =="__main__":
    portfolio={'Market':('US','^GSPC'),'EDU':0.4,'TAL':0.3,'TEDU':0.2}

def decompose_portfolio(portfolio):
    """
    功能：将一个投资组合字典分解为股票代码列表和份额列表
    投资组合的结构：{'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    输入：投资组合
    输出：市场，市场指数，股票代码列表和份额列表
    """
    #从字典中提取信息
    keylist=list(portfolio.keys())
    scope=portfolio[keylist[0]][0]
    mktidx=portfolio[keylist[0]][1]
    
    slist=[]
    plist=[]
    for key,value in portfolio.items():
        slist=slist+[key]
        plist=plist+[value]
    stocklist=slist[1:]    
    portionlist=plist[1:]

    return scope,mktidx,stocklist,portionlist    

if __name__=='__main__':
    portfolio1={'Market':('US','^GSPC'),'EDU':0.4,'TAL':0.3,'TEDU':0.2}
    scope,mktidx,tickerlist,sharelist=decompose_portfolio(portfolio1)
    _,_,tickerlist,sharelist=decompose_portfolio(portfolio1)

def portfolio_name(portfolio):
    """
    功能：解析一个投资组合的名字
    输入：投资组合
    输出：投资组合的自定义名称，未定义的返回"投资组合"
    注意：为了维持兼容性，特此定义此函数
    """
    #从字典中提取信息
    keylist=list(portfolio.keys())
    try:
        name=portfolio[keylist[0]][2]
    except:
        name="投资组合"

    return name    

if __name__=='__main__':
    portfolio={'Market':('US','^GSPC','我的组合001'),'EDU':0.4,'TAL':0.3,'TEDU':0.2}
    portfolio_name(portfolio)
    
#==============================================================================
def calc_monthly_date_range(start,end):
    """
    功能：返回两个日期之间各个月份的开始和结束日期
    输入：开始/结束日期
    输出：两个日期之间各个月份的开始和结束日期元组对列表
    """
    #测试用
    #start='2019-01-05'
    #end='2019-06-25'    
    
    import pandas as pd
    startdate=pd.to_datetime(start)
    enddate=pd.to_datetime(end)

    mdlist=[]
    #当月的结束日期
    syear=startdate.year
    smonth=startdate.month
    import calendar
    sdays=calendar.monthrange(syear,smonth)[1]
    from datetime import date
    slastday=pd.to_datetime(date(syear,smonth,sdays))

    if slastday > enddate: slastday=enddate
    
    #加入第一月的开始和结束日期
    import bisect
    bisect.insort(mdlist,(startdate,slastday))
    
    #加入结束月的开始和结束日期
    eyear=enddate.year
    emonth=enddate.month
    efirstday=pd.to_datetime(date(eyear,emonth,1))   
    if startdate < efirstday:
        bisect.insort(mdlist,(efirstday,enddate))
    
    #加入期间内各个月份的开始和结束日期
    from dateutil.relativedelta import relativedelta
    next=startdate+relativedelta(months=+1)
    while next < efirstday:
        nyear=next.year
        nmonth=next.month
        nextstart=pd.to_datetime(date(nyear,nmonth,1))
        ndays=calendar.monthrange(nyear,nmonth)[1]
        nextend=pd.to_datetime(date(nyear,nmonth,ndays))
        bisect.insort(mdlist,(nextstart,nextend))
        next=next+relativedelta(months=+1)
    
    return mdlist

if __name__=='__main__':
    mdp1=calc_monthly_date_range('2019-01-01','2019-06-30')
    mdp2=calc_monthly_date_range('2000-01-01','2000-06-30')   #闰年
    mdp3=calc_monthly_date_range('2018-09-01','2019-03-31')   #跨年
    
    for i in range(0,len(mdp1)):
        start=mdp1[i][0]
        end=mdp1[i][1]
        print("start =",start,"end =",end)


#==============================================================================
def calc_yearly_date_range(start,end):
    """
    功能：返回两个日期之间各个年度的开始和结束日期
    输入：开始/结束日期
    输出：两个日期之间各个年度的开始和结束日期元组对列表
    """
    #测试用
    #start='2013-01-01'
    #end='2019-08-08'    
    
    import pandas as pd
    startdate=pd.to_datetime(start)
    enddate=pd.to_datetime(end)

    mdlist=[]
    #当年的结束日期
    syear=startdate.year
    from datetime import date
    slastday=pd.to_datetime(date(syear,12,31))

    if slastday > enddate: slastday=enddate
    
    #加入第一年的开始和结束日期
    import bisect
    bisect.insort(mdlist,(startdate,slastday))
    
    #加入结束年的开始和结束日期
    eyear=enddate.year
    efirstday=pd.to_datetime(date(eyear,1,1))   
    if startdate < efirstday:
        bisect.insort(mdlist,(efirstday,enddate))
    
    #加入期间内各个年份的开始和结束日期
    from dateutil.relativedelta import relativedelta
    next=startdate+relativedelta(years=+1)
    while next < efirstday:
        nyear=next.year
        nextstart=pd.to_datetime(date(nyear,1,1))
        nextend=pd.to_datetime(date(nyear,12,31))
        bisect.insort(mdlist,(nextstart,nextend))
        next=next+relativedelta(years=+1)
    
    return mdlist

if __name__=='__main__':
    mdp1=calc_yearly_date_range('2013-01-05','2019-06-30')
    mdp2=calc_yearly_date_range('2000-01-01','2019-06-30')   #闰年
    mdp3=calc_yearly_date_range('2018-09-01','2019-03-31')   #跨年
    
    for i in range(0,len(mdp1)):
        start=mdp1[i][0]
        end=mdp1[i][1]
        print("start =",start,"end =",end)

#==============================================================================

def sample_selection(df,start,end):
    """
    功能：根据日期范围start/end选择数据集df的子样本，并返回子样本
    """
    flag,start2,end2=check_period(start,end)
    df_sub=df[df.index >= start2]
    df_sub=df_sub[df_sub.index <= end2]
    
    return df_sub
    
if __name__=='__main__':
    portfolio={'Market':('US','^GSPC'),'AAPL':1.0}
    market,mktidx,tickerlist,sharelist=decompose_portfolio(portfolio)
    start='2020-1-1'; end='2020-3-31'
    pfdf=get_portfolio_prices(tickerlist,sharelist,start,end)
    start2='2020-1-10'; end2='2020-3-18'
    df_sub=sample_selection(pfdf,start2,end2)    
    
#==============================================================================
def init_ts():
    """
    功能：初始化tushare pro，登录后才能下载数据
    """
    import tushare as ts
    #设置token
    token='49f134b05e668d288be43264639ac77821ab9938ff40d6013c0ed24f'
    pro=ts.pro_api(token)
    
    return pro
#====================_unlev
            cflb=fac[fac['fsdate']==d]['CFLB%'].values[0]            

            row=pd.Series({'Date':d,'Beta(CAPM)':beta_capm, \
                           'Beta(Unlevered)':beta_hamada,'CFLB%':cflb})
            try:
                betas=betas.append(row,ignore_index=True)
            except:
                betas=betas._append(row,ignore_index=True)
    betas.set_index(["Date"], inplace=True)

    #打印
    import datetime as dt; today=dt.date.today()
    if printout == True: 
        pd.set_option('display.max_columns', 1000)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_colwidth', 1000)
        print("\n=有杠杆（CAPM）对比无杠杆（Unlevered）贝塔系数=")
        print(betas)
        print("\n*** 数据来源：新浪，"+str(today))
    
    #绘图：两种杠杆对比图，CFLB图
    if graph == True:
        if len(betas)<=1: 
            print("  #Notice(get_beta_hamada_china): too few info for graphics of",stkcd)
            return betas
        
        #图1：绘制Hamada对比图
        titletxt=codetranslate(stkcd)+"：CAPM/无杠杆贝塔系数对比"
        import datetime; today = datetime.date.today()
        footnote="注: 基于"+codetranslate(mktidx)
        footnote2="\n数据来源: 新浪,"+str(today)
        #draw2_betas(model,mktidx,stkcd,betas)
        plot_2lines(betas,'Beta(CAPM)','CAPM贝塔系数', \
                betas,'Beta(Unlevered)','无杠杆贝塔系数', \
                '贝塔系数',titletxt,footnote+footnote2,hline=1,vline=0,resample_freq='H')
        
        #图2：绘制CFLB单图
        """
        plt.plot(betas['CFLB%'],marker='o',color='red',lw=3,label='CFLB%')
        """
        #均值
        cflb_avg=betas['CFLB%'].mean()
        cflb_avg_txt='，CFLB%均值为'+str(round(cflb_avg,1))+'%'
        """
        plt.axhline(y=cflb_avg,color='b',linestyle=':',label=cflb_avg_txt)
        
        #plt.title(title1,fontsize=12,fontweight='bold')
        plt.title(title1)
        #plt.ylabel("CFLB %",fontsize=12,fontweight='bold')
        plt.xlabel(footnote+footnote2)
        
        plt.grid(ls='-.')
        #查看可用的样式：print(plt.style.available)
        #样式：bmh(好),classic,ggplot(好，图大)，tableau-colorblind10，
        #样式：seaborn-bright，seaborn-poster，seaborn-whitegrid
        plt.style.use('bmh')
        plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
        plt.legend(loc='best')
        plt.show(); plt.close()
        """
        titletxt=codetranslate(stkcd)+": 财务杠杆对于贝塔系数的贡献度(CFLB)"
        plot_line(betas,'CFLB%','CFLB%','财务杠杆对于贝塔系数的贡献度%',titletxt, \
                  footnote+cflb_avg_txt+footnote2,power=6)
        
        #图3：绘制CFLB+财务杠杆双图
        df1=betas; df2=fac.set_index(["fsdate"])
        ticker1=ticker2=stkcd
        colname1='CFLB%'; colname2='lev ratio'
        label1='CFLB%'; label2='财务杠杆'
        titletxt=codetranslate(stkcd)+": CFLB与财务杠杆之间的关系"
        footnote='注: 这里的财务杠杆使用的是负债/所有者权益'
        
        plot_line2_twinx(df1,ticker1,colname1,label1,df2,ticker2,colname2,label2, \
        titletxt,footnote+footnote2)
        
        #图4：绘制CFLB+税率双图
        #df1=betas; df2=fac.set_index(["fsdate"])
        #ticker1=ticker2=stkcd
        colname1='CFLB%'; colname2='tax rate'
        label1='CFLB%'; label2='实际税率'
        titletxt=codetranslate(stkcd)+": CFLB与税率之间的关系"
        footnote='注: 这里使用的是实际税率'
        
        plot_line2_twinx(df1,ticker1,colname1,label1,df2,ticker2,colname2,label2, \
        titletxt,footnote+footnote2)
            
    return betas
    
if __name__=='__main__':
    betas1=get_beta_hamada_china('000002.SZ','399001.SZ','2010-1-1','2021-12-31','annual')

#==============================================================================
#==============================================================================
#==============================================================================












    