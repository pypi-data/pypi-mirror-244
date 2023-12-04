# -*- coding: utf-8 -*-

"""
版权：王德宏，北京外国语大学国际商学院
功能：计算CAPM模型贝塔系数的调整值
版本：2.1，2019-7-25
"""

#==============================================================================
#关闭所有警告
import warnings; warnings.filterwarnings('ignore')
from siat.common import *
from siat.translate import *
from siat.grafix import *
from siat.security_prices import *
#==============================================================================
import matplotlib.pyplot as plt

#处理绘图汉字乱码问题
import sys; czxt=sys.platform
if czxt in ['win32','win64']:
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体
    mpfrc={'font.family': 'SimHei'}

if czxt in ['darwin']: #MacOSX
    plt.rcParams['font.family']= ['Heiti TC']
    mpfrc={'font.family': 'Heiti TC'}

if czxt in ['linux']: #website Jupyter
    plt.rcParams['font.family']= ['Heiti TC']
    mpfrc={'font.family':'Heiti TC'}

# 解决保存图像时'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False 
#==============================================================================
def prepare_capm(stkcd,mktidx,start,end):
    """
    函数功能：准备计算一只股票CAPM模型贝塔系数的数据，并标记年度
    输入参数：
    stkcd: 股票代码
    mktidx: 指数代码
    start：使用股票价格数据的开始日期，MM/DD/YYYY
    end：使用股票价格数据的结束日期，MM/DD/YYYY
    输出数据：
    返回数据：带年度标记的可直接用于capm回归的股票收益率数据
    """
        
    #仅用于调试，正式使用前应注释掉
    #stkcd='002504.SZ'; mktidx='000001.SS'
    #start="12/31/2011"; end="12/31/2018"

    #抓取股价和指数
    stock=get_price(stkcd,start,end)
    if stock is None:
        print("  #Error(prepare_capm): no data retrieved from server!")
        return None
    market=get_price(mktidx,start,end)
    if market is None:
        print("  #Error(prepare_capm): no index data retrieved from server!")
        return None    

    #计算日收益率
    import pandas as pd
    stkret=pd.DataFrame(stock['Close'].pct_change())
    mktret=pd.DataFrame(market['Close'].pct_change())

    #合并，去掉空缺
    R=pd.merge(mktret,stkret,how='left',left_index=True,right_index=True)
    R=R.dropna()

    #标记各个年度
    R['Year']=R.index.strftime("%Y")

    #返回带年份的股票收益率序列
    return R

if __name__=='__main__':
    R1=prepare_capm('0700.HK','^HSI','2014-01-01','2018-12-31')

#==============================================================================
#==============================================================================
def get_beta_ML(stkcd,mktidx,yearlist,printout=True,graph=True):
    """
    函数功能：使用ML方法调整一只股票的CAPM模型贝塔系数
    输入参数：
    stkcd: 股票代码
    mktidx: 指数代码
    yearlist：年度列表，列出其中期间的贝塔系数
    输出数据：
    显示CAPM市场模型回归的beta, 以及ML调整后的beta系数
    返回数据:年度CAPM贝塔系数和ML调整后的beta系数
    """

    #仅为测试用，完成后应立即注释掉
    #stkcd='0700.HK'
    #mktidx='^HSI'
    #yearlist=['2015','2016','2017','2018']
    
    Y4=str(int(yearlist[0])-1)
    start=Y4+'-01-01'
    end=yearlist[-1]+'-12-31'    
        
    #读取股价并准备好收益率数据
    try:
        R=prepare_capm(stkcd,mktidx,start,end)
    except:
        print("  #Error(get_beta_ML): Preparing CAPM data failed!")
        return None

    if (R is None):
        print("  #Error(get_beta_ML): server time out")
        return None
    if (len(R) == 0):
        print("  #Error(get_beta_ML): server returned empty data")
        return None
    
    #用于保存beta(CAPM)和beta(ML)
    import pandas as pd
    betas=pd.DataFrame(columns=('Year','Beta(CAPM)','Beta(ML)'))

    #计算Merrill-Lynch方法贝塔系数调整
    from scipy import stats
    for year in yearlist:
        r=R[R['Year']==year]
        if len(r) != 0:
            output=stats.linregress(r['Close_x'],r['Close_y'])
            (beta,alpha,r_value,p_value,std_err)=output
            beta_ML=beta*2.0/3.0+1.0/3.0
            #整齐输出 
            #print(year,"%6.4f "%(beta),"%6.4f "%(beta_ML))

            row=pd.Series({'Year':year,'Beta(CAPM)':beta,'Beta(ML)':beta_ML})
            try:
                betas=betas.append(row,ignore_index=True)
            except:
                betas=betas._append(row,ignore_index=True)

    betas.set_index(["Year"], inplace=True)
    
    if printout == True: printdf_betas(betas,2)
    if graph == True:
        model="贝塔系数的简单调整法"
        draw2_betas(model,mktidx,stkcd,betas)

    return betas

#==============================================================================
def printdf_betas(df,decimal=2):
    """
    功能：整齐地显示数据框的内容，自动调整各列宽度
    """
    #打印时保留的小数点位数
    dec="%."+str(decimal)+"f"
    format=lambda x: dec % x
    df1=df.applymap(format)    
    
    import pandas as pd
    #调整最佳列宽
    old_width = pd.get_option('display.max_colwidth')
    pd.set_option('display.max_colwidth', -1)
    print(df1)
    pd.set_option('display.max_colwidth', old_width)

    return
    
if __name__=='__main__':
    yearlist=gen_yearlist['2010','2019']
    betas=get_beta_ML('AAPL','^GSPC',yearlist)    
    betas2=get_beta_ML('BILI','^GSPC',yearlist)
    betas3=get_beta_ML('0700.HK','^HSI',yearlist)
    yearlist1=['2015','2016','2017','2018']
    betas3=get_beta_ML('0700.HK','^HSI',yearlist1)

#==============================================================================
def draw2_betas(model,scope,ticker,betas):    
    """
    功能：绘制双曲线的贝塔因子变化图
    输入参数：
    model: 模型类型, 任意字符串(例如Merrill-Lynch Beta Adjustment)
    scope: 市场指数, 任意字符串(例如Standard & Poor 500)
    ticker：股票代码
    输出：图形
    """
    #仅用作测试，完成后应注释掉
    #model="Merrill-Lynch Beta Adjustment"
    #scope="Standard & Poor 500"
    #ticker="AAPL"

    #取得股票和指数名字，对于非美股可能耗时较长
    """
    import yfinance as yf
    mktidx= yf.Ticker(scope)
    idxinfo=mktidx.info
    idxname=idxinfo['shortName']
    stkcd=yf.Ticker(ticker)
    stkinfo=stkcd.info
    stkname=stkinfo['shortName']   
    title1="\n"+stkname+"\n"+model+"\n(Benchmark on "+idxname+")"
    """
    title1=codetranslate(ticker)+": "+model+"\n(基于"+codetranslate(scope)+")"
   
    #转换索引类型为DatetimeIndex，便于后续处理
    """
    import pandas as pd
    betas['Date']=betas.index
    betas['Date']=pd.to_datetime(betas['Date'])
    betas.set_index('Date',inplace=True)
    """

    #获得列明
    betalist=betas.columns.values.tolist()
    beta1=betalist[0]
    beta2=betalist[1]

    try:
        plt.plot(betas[beta1],label=beta1,marker='o',color='red')
        plt.plot(betas[beta2],label=beta2,marker='*',linewidth=2,ls='-.',color='blue')
    except:
        print("  #Error(draw2_betas): no available data for drawing!")
        return
    plt.axhline(y=1.0,color='b',linestyle=':',label='市场线')  
    plt.title(title1,fontsize=12,fontweight='bold')
    plt.ylabel("贝塔系数",fontsize=12,fontweight='bold')
    
    plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
    #plt.xticks(rotation=30)
    plt.legend(loc='best')    
    
    import datetime; today = datetime.date.today()
    plt.xlabel("数据来源：新浪，"+str(today))    
    
    plt.show()       
    
    return

if __name__=='__main__':
    model="ML Beta Adjustment"
    scope="SP500"
    ticker="AAPL"
    draw2_betas(model,scope,ticker,betas)


#==============================================================================
def get_beta_SW(stkcd,mktidx,yearlist,printout=True,graph=True):
    """
    函数功能：使用SW方法调整一只股票的CAPM模型贝塔系数
    输入参数：
    stkcd: 股票代码
    mktidx: 指数代码
    yearlist：年度列表，列出其中期间的贝塔系数
    输出数据：显示CAPM市场模型回归的beta, 以及调整后的beta系数
    返回数据：CAPM市场模型回归的beta, 以及调整后的beta系数
    """

    #仅为测试用，完成后应立即注释掉
    #stkcd='0700.HK'
    #mktidx='^HSI'
    #yearlist=['2015','2016','2017','2018']
    
    #生成开始结束日期
    Y4=str(int(yearlist[0])-1)
    start=Y4+'-01-01'
    end=yearlist[-1]+'-12-31'   
        
    #读取股价并准备好收益率数据
    try:
        R=prepare_capm(stkcd,mktidx,start,end)
    except:
        print("  #Error(get_beta_SW): preparing CAPM data failed!")
        return None

    if (R is None):
        print("  #Error(get_beta_SW): server time out")
        return None
    if (len(R) == 0):
        print("  #Error(get_beta_SW): server returned empty data")
        return None

    #用于保存beta(CAPM)和beta(SW)
    import pandas as pd
    betas=pd.DataFrame(columns=('Year','Beta(CAPM)','Beta(SW)'))

    #计算Scholes-William调整
    R['Close_x+1']=R['Close_x'].shift(1)    
    R['Close_x-1']=R['Close_x'].shift(-1)
    R=R.dropna()    #stats.linregress不接受空缺值

    from scipy import stats    
    for year in yearlist:
        r=R[R['Year']==year]
        if len(r) != 0:
            output=stats.linregress(r['Close_x'],r['Close_y'])
            (beta0,alpha,r_value,p_value,std_err)=output

            output=stats.linregress(r['Close_x+1'],r['Close_y'])
            (beta1,alpha,r_value,p_value,std_err)=output 

            output=stats.linregress(r['Close_x-1'],r['Close_y'])
            (beta_1,alpha,r_value,p_value,std_err)=output    

            output=stats.linregress(r['Close_x-1'],r['Close_x'])
            (rou,alpha,r_value,p_value,std_err)=output    

            beta_SW=(beta_1+beta0+beta1)/(1.0+2.0*rou)
            row=pd.Series({'Year':year,'Beta(CAPM)':beta0,'Beta(SW)':beta_SW})
            try:
                betas=betas.append(row,ignore_index=True)
            except:
                betas=betas._append(row,ignore_index=True)
    
    betas.set_index(["Year"], inplace=True)
    
    if printout == True: printdf_betas(betas,2)
    if graph == True:
        model="贝塔系数的Scholes-Williams调整法"
        draw2_betas(model,mktidx,stkcd,betas)
    
    return betas

    
if __name__=='__main__':
    yearlist=gen_yearlist('2010','2019')
    betas_AAPL=get_beta_SW('AAPL','^GSPC',yearlist)
    
    model="SW Beta Adjustment"
    scope="SP500"
    ticker="AAPL"
    draw2_betas(model,scope,ticker,betas_AAPL)

#==============================================================================
def get_beta_dimson(stkcd,mktidx,yearlist,printout=True,graph=True):
    """
    函数功能：使用Dimson(1979)方法调整一只股票的CAPM模型贝塔系数
    输入参数：
    stkcd: 股票代码
    mktidx: 指数代码
    yearlist：年度列表，用于计算年度贝塔系数
    输出数据：显示CAPM市场模型回归的beta, 以及调整后的beta系数
    返回数据：CAPM的beta, 以及调整后的beta系数
    """

    #仅为测试用，完成后应立即注释掉
    #stkcd='0700.HK'
    #mktidx='^HSI'
    #yearlist=['2015','2016','2017','2018']
    
    #生成开始结束日期
    Y4=str(int(yearlist[0])-1)
    start=Y4+'-01-01'
    end=yearlist[-1]+'-12-31'  
        
    #读取股价并准备好收益率数据
    try:
        R=prepare_capm(stkcd,mktidx,start,end)
    except:
        print("  #Error(get_beta_dimson): preparing CAPM data failed!")
        return None

    if (R is None):
        print("  #Error(get_beta_dimson): server did not respond")
        return None
    if (len(R) == 0):
        print("  #Error(get_beta_dimson): server returned empty data")
        return None

    #用于保存beta(CAPM)和beta(Dimson)
    import pandas as pd
    betas=pd.DataFrame(columns=('Year','Beta(CAPM)','Beta(Dimson)'))

    #计算Dimson(1979)调整
    R['Close_x+1']=R['Close_x'].shift(1)    
    R['Close_x-1']=R['Close_x'].shift(-1)   
    R=R.dropna()

    from scipy import stats    
    import statsmodels.api as sm
    for year in yearlist:
        r=R[R['Year']==year]
        if len(r) != 0:   
            output=stats.linregress(r['Close_x'],r['Close_y'])
            (beta_capm,alpha,r_value,p_value,std_err)=output               
            
            #三个解释变量
            RX=r[['Close_x-1','Close_x','Close_x+1']]
            X1=sm.add_constant(RX)	#要求回归具有截距项
            Y=r['Close_y']
            model = sm.OLS(Y,X1)	#定义回归模型，X1为多元矩阵
            results = model.fit()	#进行OLS回归

            (alpha,beta_1,beta0,beta1)=results.params	#提取回归系数
            beta_dimson=beta_1+beta0+beta1            

            row=pd.Series({'Year':year,'Beta(CAPM)':beta_capm, \
                           'Beta(Dimson)':beta_dimson})
            try:
                betas=betas.append(row,ignore_index=True)
            except:
                betas=betas._append(row,ignore_index=True)

    betas.set_index(["Year"], inplace=True)

    if printout == True: printdf_betas(betas,2)
    if graph == True:
        model="贝塔系数的Dimson调整法"
        draw2_betas(model,mktidx,stkcd,betas)

    return betas
    
if __name__=='__main__':
    yearlist=gen_yearlist('2010','2019')
    betas_MSFT=get_beta_dimson('MSFT','^GSPC',yearlist)
    
    model="Dimson Beta Adjustment"
    scope="SP500"
    ticker="MSFT"
    draw2_betas(model,scope,ticker,betas_MSFT)

    betas_MSFT2=get_beta_dimson('MSFT','^DJI',yearlist)
    
    model="Dimson Beta Adjustment"
    scope="DJIA"
    ticker="MSFT"
    draw2_betas(model,scope,ticker,betas_MSFT2)

#==============================================================================
#============