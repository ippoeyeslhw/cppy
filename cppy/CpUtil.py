# coding: utf-8
import win32com
import win32com.client


class CpCybos(object):
    LT_TRADE_REQUEST = 0
    LT_NONTRADE_REQUEST = 1
    LT_SUBSCRIBE = 2

    def __init__(self):
        self.disp = win32com.client.Dispatch('CpUtil.CpCybos')

    def GetIsConnect(self):
        return self.disp.IsConnect

    def GetServerType(self):
        return self.disp.ServerType

    def GetLimitRequestRemainTime(self):
        return self.disp.LimitRequestRemainTime

    def GetLimitRemainCount(self, limitType):
        return self.disp.GetLimitRemainCount(limitType)

class CpStockCode(object):
    def __init__(self):
        self.disp = win32com.client.Dispatch('CpUtil.CpStockCode')

    def CodeToName(self, cod):
        return self.disp.CodeToName(cod)

    def NameToCode(self, nm):
        return self.disp.NameToCode(nm)

    def CodeToFullCode(self, cod):
        return self.disp.CodeToFullCode(cod)

    def FullCodeToName(self, fullcode):
        return self.disp.FullCodeToName(fullcode)

    def FullCodeToCode(self, fullcode):
        return self.disp.FullCodeToCode(fullcode)

    def CodeToIndex(self, code):
        return self.disp.CodeToIndex(code)

    def GetCount(self):
        return self.disp.GetCount()

    def GetData(self, typ, idx):
        return self.disp.GetData(typ, idx)

    def GetPriceUnit(self, code, basePrice, directionUp):
        return self.disp.GetPriceUnit(code, basePrice, directionUp)


class CpCodeMgr(object):
    CPC_MARKET_NULL = 0
    CPC_MARKET_KOSPI = 1
    CPC_MARKET_KOSDAQ = 2
    CPC_MARKET_FREEBOARD = 3
    CPC_MARKET_KRX = 4
    CPC_CONTROL_NONE = 0
    CPC_CONTROL_ATTENTION = 1
    CPC_CONTROL_WARNING = 2
    CPC_CONTROL_DANGER_NOTICE = 3
    CPC_CONTROL_DANGER = 4
    CPC_SUPERVISION_NONE = 0
    CPC_SUPERVISION_NORMAL = 1
    CPC_STOCK_STATUS_NORMAL = 0
    CPC_STOCK_STATUS_STOP = 1
    CPC_STOCK_STATUS_BREAK = 2
    CPC_CAPITAL_NULL = 0
    CPC_CAPITAL_LARGE = 1
    CPC_CAPITAL_MIDDLE = 2
    CPC_CAPITAL_SMALL = 3
    CPC_KOSPI200_NONE = 0
    CPC_KOSPI200_CONSTRUCTIONS_MACHINERY = 1
    CPC_KOSPI200_SHIPBUILDING_TRANSPORTATION = 2
    CPC_KOSPI200_STEELS_METERIALS = 3
    CPC_KOSPI200_ENERGY_CHEMICALS = 4
    CPC_KOSPI200_IT = 5
    CPC_KOSPI200_FINANCE = 6
    CPC_KOSPI200_CUSTOMER_STAPLES = 7
    CPC_KOSPI200_CUSTOMER_DISCRETIONARY = 8
    CPC_KSE_SECTION_KIND_NULL = 0
    CPC_KSE_SECTION_KIND_ST = 1
    CPC_KSE_SECTION_KIND_MF = 2
    CPC_KSE_SECTION_KIND_RT = 3
    CPC_KSE_SECTION_KIND_SC = 4
    CPC_KSE_SECTION_KIND_IF = 5
    CPC_KSE_SECTION_KIND_DR = 6
    CPC_KSE_SECTION_KIND_SW = 7
    CPC_KSE_SECTION_KIND_SR = 8
    CPC_KSE_SECTION_KIND_ELW = 9
    CPC_KSE_SECTION_KIND_ETF = 10
    CPC_KSE_SECTION_KIND_BC = 11
    CPC_KSE_SECTION_KIND_FETF = 12
    CPC_KSE_SECTION_KIND_FOREIGN = 13
    CPC_KSE_SECTION_KIND_FU = 14
    CPC_KSE_SECTION_KIND_OP = 15
    CPC_LAC_NORMAL = 0
    CPC_LAC_EX_RIGHTS = 1
    CPC_LAC_EX_DIVIDEND = 2
    CPC_LAC_EX_DISTRI_DIVIDEND = 3
    CPC_LAC_EX_RIGHTS_DIVIDEND = 4
    CPC_LAC_INTERIM_DIVIDEND = 5
    CPC_LAC_EX_RIGHTS_INTERIM_DIVIDEND = 6
    CPC_LAC_ETC = 99
    CPC_PARPRICE_CHANGE_NONE = 0
    CPC_PARPRICE_CHANGE_DIVIDE = 1
    CPC_PARPRICE_CHANGE_MERGE = 2
    CPC_PARPRICE_CHANGE_ETC = 99

    def __init__(self):
        self.disp = win32com.client.Dispatch('CpUtil.CpCodeMgr')
    def CodeToName(self, code):
        return self.disp.CodeToName(code)
    def GetStockMarginRate(self, code):
        return self.disp.GetStockMarginRate(code)
    def GetStockMemeMin(self, code):
        return self.disp.GetStockMemeMin(code)
    def GetStockIndustryCode(self, code):
        return self.disp.GetStockIndustryCode(code)
    def GetStockMarketKind(self, code):
        return self.disp.GetStockMarketKind(code)
    def GetStockControlKind(self, code):
        return self.disp.GetStockControlKind(code)
    def GetStockSupervisionKind(self, code):
        return self.disp.GetStockSupervisionKind(code)
    def GetStockStatusKind(self, code):
        return self.disp.GetStockStatusKind(code)
    def GetStockCapital(self, code):
        return self.disp.GetStockCapital(code)
    def GetStockFiscalMonth(self, code):
        return self.disp.GetStockFiscalMonth(code)
    def GetStockGroupCode(self, code):
        return self.disp.GetStockGroupCode(code)
    def GetStockKospi200Kind(self, code):
        return self.disp.GetStockKospi200Kind(code)
    def GetStockSectionKind(self, code):
        return self.disp.GetStockSectionKind(code)
    def GetStockLacKind(self, code):
        return self.disp.GetStockLacKind(code)
    def GetStockListedDate(self, code):
        return self.disp.GetStockListedDate(code)
    def GetStockMaxPrice(self, code):
        return self.disp.GetStockMaxPrice(code)
    def GetStockMinPrice(self, code):
        return self.disp.GetStockMinPrice(code)
    def GetStockParPrice(self, code):
        return self.disp.GetStockParPrice(code)
    def GetStockStdPrice(self, code):
        return self.disp.GetStockStdPrice(code)
    def GetStockYdOpenPrice(self, code):
        return self.disp.GetStockYdOpenPrice(code)
    def GetStockYdHighPrice(self, code):
        return self.disp.GetStockYdHighPrice(code)
    def GetStockYdLowPrice(self, code):
        return self.disp.GetStockYdLowPrice(code)
    def GetStockYdClosePrice(self, code):
        return self.disp.GetStockYdClosePrice(code)
    def IsStockCreditEnable(self, code):
        return self.disp.IsStockCreditEnable(code)
    def GetStockParPriceChageType(self, code):
        return self.disp.GetStockParPriceChageType(code)
    def GetStockElwBasketCodeList(self, code):
        return self.disp.GetStockElwBasketCodeList(code)
    def GetStockElwBasketCompList(self, code):
        return self.disp.GetStockElwBasketCompList(code)
    def GetStockListByMarket(self, code):
        return self.disp.GetStockListByMarket(code)
    def GetGroupCodeList(self, code):
        return self.disp.GetGroupCodeList(code)
    def GetGroupName(self, code):
        return self.disp.GetGroupName(code)
    def GetIndustryName(self, code):
        return self.disp.GetIndustryName(code)
    def GetMemberList (self):
        return self.disp.GetMemberList()
    def GetMemberName(self, code):
        return self.disp.GetMemberName(code)
    def GetKosdaqIndustry1List (self):
        return self.disp.GetKosdaqIndustry1List ()
    def GetKosdaqIndustry2List (self):
        return self.disp.GetKosdaqIndustry2List ()
    def GetMarketStartTime(self):
        return self.disp.GetMarketStartTime()
    def GetMarketEndTime(self):
        return self.disp.GetMarketEndTime()

    def isCommonStock(self, code):
        """보통주인지 판별 (우선주일경우 False)
        """
        if code[-1] == '0':
            return True
        return False

    def isSpacStock(self, code):
        """스팩주식여부"""
        nm = self.CodeToName(code)
        # python2.x 인경우  u'스팩'
        if nm.find('스팩') == -1:
            return False
        return True