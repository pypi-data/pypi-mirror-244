# -*- coding: utf-8 -*-
"""
本模块功能：SIAT公共转换函数，证券代码转换，名词中英相互转换
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2021年5月16日
最新修订日期：
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
from siat.common import *
#==============================================================================
def ectranslate(eword):
    """
    翻译证券词汇为证券名称，基于语言环境决定中英文。
    输入：证券词汇英文
    """
    
    lang=check_language()
    if lang == 'English':
        return ectranslate_e(eword)
    else:
        return ectranslate_c(eword)

#==============================================================================
def ectranslate_c(eword):
    """
    翻译英文专业词汇至中文，便于显示或绘图时输出中文而不是英文。
    输入：英文专业词汇。输出：中文专业词汇
    """
    import pandas as pd
    ecdict=pd.DataFrame([
        
        ['implied volatility','隐含波动率'],   
        ['delta','Delta'],['gamma','Gamma'],['theta','Theta'],
        ['vega','Vega'],['rho','Rho'],
        ['Call','看涨期权'],['Put','看跌期权'],
        ['call','看涨期权'],['put','看跌期权'],
        
        ['High','最高价'],['Low','最低价'],['Open','开盘价'],['Close','收盘价'],
        ['Current Price','现时股价'],
        ['Volume','成交量'],['Adj Close','调整收盘价'],['Daily Ret','日收益率'],
        ['Daily Ret%','日收益率%'],['Daily Adj Ret','调整日收益率'],
        ['Daily Adj Ret%','调整日收益率%'],['log(Daily Ret)','对数日收益率'],
        ['log(Daily Adj Ret)','对数调整日收益率'],['Weekly Ret','周收益率'],
        ['Weekly Ret%','周收益率%'],['Weekly Adj Ret','周调整收益率'],
        ['Weekly Adj Ret%','周调整收益率%'],['Monthly Ret','月收益率'],
        ['Monthly Ret%','月收益率%'],['Monthly Adj Ret','月调整收益率'],
        ['Monthly Adj Ret%','月调整收益率%'],['Quarterly Ret','季度收益率'],
        ['Quarterly Ret%','季度收益率%'],['Quarterly Adj Ret','季度调整收益率'],
        ['Quarterly Adj Ret%','季度调整收益率%'],['Annual Ret','年收益率'],
        ['Annual Ret%','年收益率%'],['Annual Adj Ret','年调整收益率'],
        ['Annual Adj Ret%','年调整收益率%'],['Exp Ret','投资收益率'],
        ['Exp Ret%','投资收益率%'],['Exp Adj Ret','持有调整收益率'],
        ['Exp Adj Ret%','持有调整收益率%'],
        
        ['Weekly Price Volatility','周股价波动风险'],
        ['Weekly Adj Price Volatility','周调整股价波动风险'],
        ['Monthly Price Volatility','月股价波动风险'],
        ['Monthly Adj Price Volatility','月调整股价波动风险'],
        ['Quarterly Price Volatility','季股价波动风险'],
        ['Quarterly Adj Price Volatility','季调整股价波动风险'],
        ['Annual Price Volatility','年股价波动风险'],
        ['Annual Adj Price Volatility','年调整股价波动风险'],  
        ['Exp Price Volatility','持有股价波动风险'], 
        ['Exp Adj Price Volatility','持有调整股价波动风险'],
        
        ['Weekly Ret Volatility','周收益率波动风险'],
        ['Weekly Ret Volatility%','周收益率波动风险%'],
        ['Weekly Adj Ret Volatility','周调整收益率波动风险'],
        ['Weekly Adj Ret Volatility%','周调整收益率波动风险%'],
        ['Monthly Ret Volatility','月收益率波动风险'],
        ['Monthly Ret Volatility%','月收益率波动风险%'],
        ['Monthly Adj Ret Volatility','月调整收益波动风险'],
        ['Monthly Adj Ret Volatility%','月调整收益波动风险%'],
        ['Quarterly Ret Volatility','季收益率波动风险'],
        ['Quarterly Ret Volatility%','季收益率波动风险%'],
        ['Quarterly Adj Ret Volatility','季调整收益率波动风险'],
        ['Quarterly Adj Ret Volatility%','季调整收益率波动风险%'],
        ['Annual Ret Volatility','年收益率波动风险'],
        ['Annual Ret Volatility%','年收益率波动风险%'],
        ['Annual Adj Ret Volatility','年调整收益率波动风险'], 
        ['Annual Adj Ret Volatility%','年调整收益率波动风险%'], 
        ['Exp Ret Volatility','投资收益率波动风险'], 
        ['Exp Ret Volatility%','投资收益率波动风险%'],
        ['Exp Adj Ret Volatility','调整投资收益率波动风险'],        
        ['Exp Adj Ret Volatility%','调整投资收益率波动风险%'],
        
        ['Weekly Ret LPSD','周收益率波动损失风险'],
        ['Weekly Ret LPSD%','周收益率波动损失风险%'],
        ['Weekly Adj Ret LPSD','周调整收益率波动损失风险'],
        ['Weekly Adj Ret LPSD%','周调整收益率波动损失风险%'],
        ['Monthly Ret LPSD','月收益率波动损失风险'],
        ['Monthly Ret LPSD%','月收益率波动损失风险%'],
        ['Monthly Adj Ret LPSD','月调整收益波动损失风险'],
        ['Monthly Adj Ret LPSD%','月调整收益波动损失风险%'],
        ['Quarterly Ret LPSD','季收益率波动损失风险'],
        ['Quarterly Ret LPSD%','季收益率波动损失风险%'],
        ['Quarterly Adj Ret LPSD','季调整收益率波动损失风险'],
        ['Quarterly Adj Ret LPSD%','季调整收益率波动损失风险%'],
        ['Annual Ret LPSD','年收益率波动损失风险'],
        ['Annual Ret LPSD%','年收益率波动损失风险%'],
        ['Annual Adj Ret LPSD','年调整收益率波动损失风险'], 
        ['Annual Adj Ret LPSD%','年调整收益率波动损失风险%'], 
        ['Exp Ret LPSD','投资损失风险'], 
        ['Exp Ret LPSD%','投资损失风险%'],
        ['Exp Adj Ret LPSD','调整投资损失风险'],        
        ['Exp Adj Ret LPSD%','调整投资损失风险%'],
        
        ['roll_spread','罗尔价差比率'],['amihud_illiquidity','阿米胡德非流动性'],
        ['ps_liquidity','P-S流动性'],    
        
        ['Gross Domestic Product','国内生产总值'],['GNI','国民总收入'],    
        
        ['zip','邮编'],['sector','领域'],
        ['fullTimeEmployees','全职员工数'],['Employees','全职员工数'],
        ['longBusinessSummary','业务介绍'],['city','城市'],['phone','电话'],
        ['state','州/省'],['country','国家/地区'],['companyOfficers','高管'],
        ['website','官网'],['address1','地址1'],['address2','地址2'],['industry','行业'],
        ['previousClose','上个收盘价'],['regularMarketOpen','正常市场开盘价'],
        ['twoHundredDayAverage','200天均价'],['fax','传真'], 
        ['trailingAnnualDividendYield','年化股息率TTM'],
        ['payoutRatio','股息支付率'],['volume24Hr','24小时交易量'],
        ['regularMarketDayHigh','正常市场日最高价'],
        ['averageDailyVolume10Day','10天平均日交易量'],['totalAssets','总资产'],
        ['regularMarketPreviousClose','正常市场上个收盘价'],
        ['fiftyDayAverage','50天平均股价'],
        ['trailingAnnualDividendRate','年化每股股利金额TTM'],['open','当日开盘价'],
        ['averageVolume10days','10日平均交易量'],['expireDate','失效日'],
        ['yield','收益率'],['dividendRate','每股股利金额'],
        ['exDividendDate','股利除息日'],['beta','贝塔系数'],
        ['startDate','开始日期'],['regularMarketDayLow','正常市场日最低价'],
        ['priceHint','价格提示'],['currency','交易币种'],
        ['trailingPE','市盈率TTM'],['regularMarketVolume','正常市场交易量'],
        ['marketCap','市值'],['averageVolume','平均交易量'],
        ['priceToSalesTrailing12Months','市销率TTM'],
        ['TTM Price to Sales','市销率TTM'],
        ['dayLow','当日最低价'],
        ['ask','卖出价'],['askSize','卖出价股数'],['volume','当日交易量'],
        ['fiftyTwoWeekHigh','52周最高价'],['forwardPE','预期市盈率'],
        ['fiveYearAvgDividendYield','5年平均股息率'],
        ['fiftyTwoWeekLow','52周最低价'],['bid','买入价'],
        ['tradeable','今日是否可交易'],['dividendYield','股息率'],
        ['bidSize','买入价股数'],['dayHigh','当日最高价'],
        ['exchange','交易所'],['shortName','简称'],['longName','全称'],
        ['exchangeTimezoneName','交易所时区'],
        ['exchangeTimezoneShortName','交易所时区简称'],['quoteType','证券类别'],
        ['symbol','证券代码'],['messageBoardId','证券留言板编号'],
        ['market','证券市场'],['annualHoldingsTurnover','一年內转手率'],
        ['enterpriseToRevenue','市售率(EV/Revenue)'],['EV to Revenue','市售率(EV/Revenue)'],        
        ['Price to Book','市净率'],['beta3Year','3年贝塔系数'],
        ['profitMargins','净利润率'],['enterpriseToEbitda','企业价值/EBITDA'],
        ['EV to EBITDA','企业价值倍数（EV/EBITDA)'],
        ['52WeekChange','52周股价变化率'],['morningStarRiskRating','晨星风险评级'],
        ['forwardEps','预期每股收益'],['revenueQuarterlyGrowth','季营收增长率'],
        ['sharesOutstanding','流通在外股数'],['fundInceptionDate','基金成立日'],
        ['annualReportExpenseRatio','年报费用比率'],['bookValue','每股净资产'],
        ['sharesShort','卖空股数'],['sharesPercentSharesOut','卖空股数/流通股数'],
        ['lastFiscalYearEnd','上个财年截止日期'],
        ['heldPercentInstitutions','机构持股比例'],
        ['netIncomeToCommon','归属普通股股东净利润'],['trailingEps','每股收益'],
        ['lastDividendValue','上次股利价值'],
        ['SandP52WeekChange','标普指数52周变化率'],['priceToBook','市净率'],
        ['heldPercentInsiders','内部人持股比例'],['priceToBook','市净率'],
        ['nextFiscalYearEnd','下个财年截止日期'],
        ['mostRecentQuarter','上个财季截止日期'],['shortRatio','空头净额比率'],
        ['sharesShortPreviousMonthDate','上月做空日期'],
        ['floatShares','可交易股数'],['enterpriseValue','企业价值'],
        ['threeYearAverageReturn','3年平均回报率'],['lastSplitDate','上个拆分日期'],
        ['lastSplitFactor','上次拆分比例'],
        ['earningsQuarterlyGrowth','季盈余增长率'],['dateShortInterest','做空日期'],
        ['pegRatio','市盈率与增长比率'],['shortPercentOfFloat','空头占可交易股票比例'],
        ['sharesShortPriorMonth','上月做空股数'],
        ['fiveYearAverageReturn','5年平均回报率'],['regularMarketPrice','正常市场价'],
        ['logo_url','商标图标网址'],     ['underlyingSymbol','曾用代码'],     
        ['timeZoneShortName','时区简称'],['timeZoneFullName','时区全称'],
        ['exchangeName','交易所名称'],['currentPrice','当前价格'],
        ['ratingYear','评估年度'],['ratingMonth','评估月份'],
        ['currencySymbol','币种符号'],['recommendationKey','投资建议'],
        ['totalInsiderShares','内部人持股数'],['financialCurrency','财报币种'],
        ['currentRatio','流动比率'],['quickRatio','速动比率'],
        ['debtToEquity','负债-权益比%'],['ebitdaMargins','EBITDA利润率'],
        ['operatingMargins','经营利润率'],['grossMargins','毛利润率'],
        ['returnOnAssets','资产回报率'],['returnOnEquity','净资产回报率'],
        ['ROA','资产回报率'],['ROE','净资产回报率'],
        ['revenuePerShare','每股销售收入'],['totalCashPerShare','每股总现金'],
        ['revenueGrowth','销售收入增长率'],['earningsGrowth','盈余增长率'],
        ['totalDebt','总负债'],['totalRevenue','总销售收入'],
        ['grossProfits','毛利润'],['ebitda','EBITDA'],
        ['operatingCashflow','经营现金流'],['freeCashflow','自由现金流'],
        ['totalCash','总现金流'],
        ['Total Asset Turnover','总资产周转率'],['Fixed Asset Turnover','固定资产周转率'],
        ['PPE Residual','固定资产成新率'],['Capital Accumulation','资本积累'],
        ['Current Ratio','流动比'],['Quick Ratio','速动比'],['Cash Ratio','现金比'],
        ['Debt Service Coverage','偿债保障比率'],['Debt to Equity','负债-权益比%'],
        ['Debt to Asset','资产负债比'],['Times Interest Earned','利息保障倍数'],
        ['Inventory Turnover','存货周转率'],['Receivable Turnover','应收帐款周转率'],
        ['BasicEPS','基本每股收益'],['Cashflow per Share','每股现金流量'],
        ['Profit Margin','净利润率'],['Gross Margin','毛利润率'],
        ['EBITDA Margin','EBITDA利润率'],['Operating Margin','营业利润率'],
        ['Trailing EPS','每股收益TTM'],['Trailing PE','市盈率TTM'],['Forward PE','预期市盈率'],
        ['Revenue Growth','销售收入增长率'],['Earnings Growth','年度盈余增长率'],
        ['Earnings Quarterly Growth','季度盈余增长率'],
        ['IGR','内部增长率(IGR)'],['SGR','可持续增长率(SGR)'],
        ['Payout Ratio','股利支付率'],
        
        ['overallRisk','总风险指数'],
        ['boardRisk','董事会风险指数'],['compensationRisk','薪酬风险指数'],
        ['shareHolderRightsRisk','股东风险指数'],['auditRisk','审计风险指数'],
        
        ['totalEsg','ESG总分数'],['Total ESG','ESG总分数'],
        ['esgPerformance','ESG业绩评价'],
        ['peerEsgScorePerformance','ESG同业分数'],
        ['environmentScore','环保分数'],['Environment Score','环保分数'],
        ['peerEnvironmentPerform