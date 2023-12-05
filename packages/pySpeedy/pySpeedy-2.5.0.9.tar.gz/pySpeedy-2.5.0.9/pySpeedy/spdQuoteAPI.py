# -*- coding: cp950 -*-
##  @brief 
#  ���O : spdQuoteAPI
#  �@�� : Allen Lee, Simon Chang
#  �\�� : spdQuoteAPI �s��StarWave Marketdata Server.
#         ���ѹ�x�W�����TWSE/OTC/TAIFEX�污���䴩
#----------------------------------------------------------------------------
import ctypes, platform, os, sys
## @cond  
class spdContract(ctypes.Structure):
    _fields_ = [('BullPx', ctypes.c_double), 
                ('BearPx', ctypes.c_double), 
                ('RefPx', ctypes.c_double), 
                ('ContractMultiplier', ctypes.c_double),
                ('StrikePx', ctypes.c_double), #for Options                
                ('Market', ctypes.c_int),
                ('TradeUnit', ctypes.c_int),
                ('DayTrade', ctypes.c_int),
                ('WarningStock', ctypes.c_int),
                ('TradeFlag', ctypes.c_bool),             
                ('IsWarrant', ctypes.c_bool),             
                ('CallPut', ctypes.c_char)] #for Options
## @endcond      
class ContractInfo:
    ## �ӫ~�򥻸�����O�غc��.        
    def __init__(self,Ex,Sym,Name,MMD, ProdID, Info ):
        ## ����ҦW��(TWSE,OTC,TAIFEX...) 
        self.Exchange = Ex 
        ## �ӫ~�W��.�Ҧp �Ҩ�:2330 ���f:TXFF3
        self.Symbol = Sym 
        ## �ӫ~��ܦW��. �Ҧp �x�n�q
        self.DisplayName = Name 
        ## ���f�ӫ~����~�� YYYYMM
        self.MaturityDate = MMD
        ## �ӫ~���O.�Ҧp �Ҩ�:17(���īO�I); ���f:TXF 
        self.Category =  ProdID
        ## ������
        self.BullPx = Info.BullPx
        ## �^����
        self.BearPx = Info.BearPx
        ## �Ѧһ�
        self.RefPx = Info.RefPx
        ## ��������.�� TXF�@�I 200 
        self.ContractMultiplier = Info.ContractMultiplier
        ## ����v�ӫ~�i����
        self.StrikePx = Info.StrikePx
        ## �����O. �U��ɨϥ� 'fut':���f, 'opt':����v, 'tse':��������(�ҥ��), 'otc':�d�R����(OTC)          
        if Info.Market ==  0:
            self.Market = 'fut'
        elif Info.Market ==  1:
            self.Market = 'opt'
        elif Info.Market ==  2:
            self.Market = 'tse'
        elif Info.Market ==  3:
            self.Market = 'otc'
        elif Info.Market ==  4:
            self.Market = 'ffut'
        elif Info.Market ==  5:
            self.Market = 'fopt'
        else:
            self.Market = 'unknown'
        ## ������. �� �Ѳ��@�i�O1000�� 
        self.TradeUnit = Info.TradeUnit
        ## �ӫ~�O�_�i��� 1:�O 0:�_
        self.TradeFlag = Info.TradeFlag        
        ## ��R���O. 'Yes'��ܬ��i���R���Υ����R�{�ѷ�R�Ҩ�A'OnlyBuy' ��ܬ��i���R���{�ѷ�R�Ҩ�. 'No'��ܬ����i�{�ѷ�R�Ҩ�C
        if Info.DayTrade  == 1:
            self.DayTrade = 'Yes'  
        elif Info.DayTrade  == 2:
            self.DayTrade = 'OnlyBuy'  
        else:
            self.DayTrade = 'No'  
        ## �O���O�v�Ұӫ~
        self.IsWarrant = Info.IsWarrant
        ## ĵ�ܪѥN�X. 0�X���` 1�X�`�N 2�X�B�m 3�X�`�N�γB�m 4�X�A���B�m 5�X�`�N�ΦA���B�m 6�X�u�ʳB�m 7�X�`�N�μu�ʳB�m
        self.WarringStock = Info.WarningStock  
        ## 'Call' ��ܬOcall������v,'Put'��ܬOPut������v.'None'��ܫD����v�ӫ~        
        if Info.CallPut == 'C':
            self.CallPut = 'Call'
        elif  Info.CallPut == 'P':
            self.CallPut = 'Put'
        else:
            self.CallPut = 'None'
    ## �L�X�ӫ~�򥻸��.   
    def Print(self):
        print( '----- [{0}][{1}] -----'.format(self.Exchange, self.Symbol))            
        print( 'Exchange[{0}] '.format(self.Exchange))            
        print( 'Symbol[{0}] '.format(self.Symbol))            
        print( 'Market[{0}] '.format(self.Market))            
        print( 'DisplayName[{0}] '.format(self.DisplayName))            
        print( 'Category[{0}] '.format(self.Category))            
        print( 'BullPx[{0}] '.format(self.BullPx))            
        print( 'BearPx[{0}] '.format(self.BearPx))            
        print( 'RefPx[{0}] '.format(self.RefPx))            
        if self.Market ==  'fut': # TAIFEX Taiwan Futures
            print( 'ContractMultiplier[{0}] '.format(self.ContractMultiplier))            
            print( 'MaturityDate[{0}] '.format(self.MaturityDate))    
            print( 'CallPut[{0}] '.format(self.CallPut))            
            print( 'StrikePx[{0}] '.format(self.StrikePx))            
            print( '----- TW Futures -----' )
        elif  self.Market ==  'opt': # TAIFEX Taiwan Options
            print( 'ContractMultiplier[{0}] '.format(self.ContractMultiplier))            
            print( 'MaturityDate[{0}] '.format(self.MaturityDate))            
            print( 'CallPut[{0}] '.format(self.CallPut))            
            print( 'StrikePx[{0}] '.format(self.StrikePx))            
            print( '----- TW Options -----' )
        elif  self.Market ==  'tse': # TWSE Taiwan equity
            print( 'TradeUnit[{0}] '.format(self.TradeUnit))            
            print( 'DayTrade[{0}] '.format(self.DayTrade))            
            print( 'WarringStock[{0}] '.format(self.WarringStock))            
            print( 'IsWarrant[{0}] '.format(self.IsWarrant))            
            print( '----- TWSE Stocks -----' )
        elif  self.Market ==  'otc': # OTC Taiwan over the counter
            print( 'TradeUnit[{0}] '.format(self.TradeUnit))            
            print( 'DayTrade[{0}] '.format(self.DayTrade))            
            print( 'WarringStock[{0}] '.format(self.WarringStock))            
            print( 'IsWarrant[{0}] '.format(self.IsWarrant))            
            print( '------ OTC Stocks -----' )
        else:
            print( 'TradeUnit[{0}] '.format(self.TradeUnit))            


#----------------------------------------------------------------------------
#
# prepare for class spdQuoteAPI define
#
#----------------------------------------------------------------------------
class spdMsgOrderBook(ctypes.Structure):
    ## �e�Uï��s��� 
    # @param BidPrice1~BidPrice5	�̨ζR�@��R����
    # @param BidQty1~BidQty5	�̨ζR�@��R���q
    # @param AskPrice1~AskPrice5	�̨ν�@��椭��
    # @param AskQty1~AskQty5	�̨ν�@��椭�q
    # @param DerivedBidPrice	�l��Bid����.(�ȴ���Ҵ���)
    # @param DerivedBidQty	�l��Bid�ƶq.(�ȴ���Ҵ���)
    # @param DerivedAskPrice	�l��Ask����.(�ȴ���Ҵ���)
    # @param DerivedAskQty	�l��Ask�ƶq.(�ȴ���Ҵ���)
    # @param ����	Derived Bid Ask �̨ε����@�ɥu�|�X�{�b���f�ο���v�ӫ~�A ���ϥ����椧ROD�]Rest of day�^�����t�e�U�o�d�s��t�ΡA �N���ӧO�i���X���������̨Τ@�ɩe�U���q�A�l�͵����e�U�ܸӸ����t�e�U���ݤ��t�@����e�Uï���C �G��ӧO�������榡�e�U�̨Τ��ɶR����q�~�A�|�|�A�h���S�̨Τ@�ɥѸ����t�e�U�l�ͤ��榡�e�U�R����q�C �Ӹ�T�Ѵ���Ҵ��ѡC
    _fields_ = [('BidPrice1', ctypes.c_double), 
                ('BidPrice2', ctypes.c_double), 
                ('BidPrice3', ctypes.c_double), 
                ('BidPrice4', ctypes.c_double),
                ('BidPrice5', ctypes.c_double),
                ('BidQty1', ctypes.c_int), 
                ('BidQty2', ctypes.c_int), 
                ('BidQty3', ctypes.c_int), 
                ('BidQty4', ctypes.c_int), 
                ('BidQty5', ctypes.c_int),
                ('AskPrice1', ctypes.c_double), 
                ('AskPrice2', ctypes.c_double), 
                ('AskPrice3', ctypes.c_double), 
                ('AskPrice4', ctypes.c_double), 
                ('AskPrice5', ctypes.c_double),
                ('AskQty1', ctypes.c_int), 
                ('AskQty2', ctypes.c_int), 
                ('AskQty3', ctypes.c_int), 
                ('AskQty4', ctypes.c_int), 
                ('AskQty5', ctypes.c_int),
                ('DerivedBidPrice', ctypes.c_double),
                ('DerivedBidQty', ctypes.c_int), 
                ('DerivedAskPrice', ctypes.c_double), 
                ('DerivedAskQty', ctypes.c_int)]
                
## @cond                                 
#----------------------------------------------------------------------------
if platform.system() == 'Windows':
    print('\n----- spdQuoteAPI detect : Windows platform -----')
    if (sys.maxsize > 2**32) == True:
        print('Load['+os.path.dirname(__file__) + '\pySpeedyAPI_64.dll'+']')
        libSpeedy = ctypes.cdll.LoadLibrary( os.path.dirname(__file__) + '\pySpeedyAPI_64.dll')
    else:
        print('Load['+os.path.dirname(__file__) + '\pySpeedyAPI.dll'+']')
        libSpeedy = ctypes.cdll.LoadLibrary( os.path.dirname(__file__) + '\pySpeedyAPI.dll')
elif platform.system() == 'Linux':
    print('\n----- spdQuoteAPI detect : Linux platform -----')
    print('Load['+os.path.dirname(__file__) + '/pySpeedyAPI_64.so'+']')
    libSpeedy = ctypes.cdll.LoadLibrary( os.path.dirname(__file__) + '/pySpeedyAPI_64.so')
#----------------------------------------------------------------------------
def spdQuoteDummyFun():
    pass
#----------------------------------------------------------------------------
# Declare the callback type
Def_pyQuoteOnConnected     = ctypes.CFUNCTYPE(None)
Def_pyQuoteOnDisconnected  = ctypes.CFUNCTYPE(None)
Def_pyQuoteOnLogonResponse =  ctypes.CFUNCTYPE(None, ctypes.c_bool, ctypes.c_wchar_p)
Def_pyQuoteOnContract = ctypes.CFUNCTYPE(None,  ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p,ctypes.POINTER(spdContract))
Def_pyQuoteOnContractDownloadComplete = ctypes.CFUNCTYPE(None, ctypes.c_int)
Def_pyQuoteOnOrderBook     = ctypes.CFUNCTYPE(None, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.POINTER(spdMsgOrderBook))
Def_pyQuoteOnTrade         = ctypes.CFUNCTYPE(None, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_double, ctypes.c_int)
# Keep "life cycle" of events function pointer to prevent "access violation"
gQuoteFunPtr_OnConnected     = spdQuoteDummyFun
gQuoteFunPtr_OnDisconnected  = spdQuoteDummyFun
gQuoteFunPtr_OnLogonResponse = spdQuoteDummyFun
gQuoteFunPtr_OnContract      = spdQuoteDummyFun
gQuoteFunPtr_OnComplete      = spdQuoteDummyFun
gQuoteFunPtr_OnOrderBook     = spdQuoteDummyFun
gQuoteFunPtr_OnTrade         = spdQuoteDummyFun
## @endcond
#----------------------------------------------------------------------------
#
# class spdQuoteAPI
#
#----------------------------------------------------------------------------
class spdQuoteAPI(object):    
    #------------------------------------------------------------------------
    # -- Functions --
    #------------------------------------------------------------------------
    ## �غc�����|�ŧiC�����bPython������ƭ��.
    #  �ëŧi����C��callback function.�õ��U��C���Ҳ�.     
    # @param self ���󥻨� 
    def __init__(self):
        # Functions definition
        # Constructor
        libSpeedy.pyQuoteAdapter_New.argtypes = []
        libSpeedy.pyQuoteAdapter_New.restype = ctypes.c_void_p
        # Delete
        libSpeedy.pyQuoteAdapter_Delete.argtypes = [ctypes.c_void_p]
        libSpeedy.pyQuoteAdapter_Delete.restype = None
        # IsConnected()
        libSpeedy.pyQuoteAdapter_IsConnected.argtypes = [ctypes.c_void_p]
        libSpeedy.pyQuoteAdapter_IsConnected.restype = ctypes.c_bool
        # Logon()
        libSpeedy.pyQuoteAdapter_Logon.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p,ctypes.c_bool]
        libSpeedy.pyQuoteAdapter_Logon.restype = None
        # Subscribe()
        libSpeedy.pyQuoteAdapter_Subscribe.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
        libSpeedy.pyQuoteAdapter_Subscribe.restype = ctypes.c_bool
        # DownloadContracts()
        libSpeedy.pyQuoteAdapter_DownloadContracts.argtypes = [ctypes.c_void_p]
        libSpeedy.pyQuoteAdapter_DownloadContracts.restype = None
        # RegEvents()
        libSpeedy.pyQuoteAdapter_RegEvents.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
        libSpeedy.pyQuoteAdapter_RegEvents.restype = None
        
        # Create pyQuoteAdapter object        
        ## �O�d���API��Handle
        self.Obj = libSpeedy.pyQuoteAdapter_New()
        ## �Ѳ��ӫ~�򥻸��Dictionary.
        self.Stocks = {}
        ## ���f�ӫ~�򥻸��Dictionary.
        self.Futures = {}
        ## ����v�ӫ~�򥻸��Dictionary.
        self.Options = {}
        
        # Keep "life cycle" of events function
        global gQuoteFunPtr_OnConnected, gQuoteFunPtr_OnDisconnected, gQuoteFunPtr_OnLogonResponse, gQuoteFunPtr_OnContract, gQuoteFunPtr_OnComplete, gQuoteFunPtr_OnOrderBook, gQuoteFunPtr_OnTrade
        # Binding events
        gQuoteFunPtr_OnConnected    = Def_pyQuoteOnConnected(self.OnConnected)
        gQuoteFunPtr_OnDisconnected = Def_pyQuoteOnDisconnected(self.OnDisconnected)
        gQuoteFunPtr_OnLogonResponse= Def_pyQuoteOnLogonResponse(self.OnLogonResponse) 
        gQuoteFunPtr_OnContract     = Def_pyQuoteOnContract( self.__OnContract )    
        gQuoteFunPtr_OnComplete     = Def_pyQuoteOnContractDownloadComplete( self.__OnComplete )   
        gQuoteFunPtr_OnOrderBook    = Def_pyQuoteOnOrderBook(self.__OnOrderBook)
        gQuoteFunPtr_OnTrade        = Def_pyQuoteOnTrade(self.OnTrade)
        # Register events to C/C++
        libSpeedy.pyQuoteAdapter_RegEvents(self.Obj, gQuoteFunPtr_OnConnected, gQuoteFunPtr_OnDisconnected, gQuoteFunPtr_OnLogonResponse, gQuoteFunPtr_OnContract, gQuoteFunPtr_OnComplete, gQuoteFunPtr_OnOrderBook, gQuoteFunPtr_OnTrade)
    
    ## �污�D���O�_�s�u 
    # @param self ���󥻨� 
    # @return TRUE ��ܳs�u���\,FALSE �_�u. .		
    def IsConnected(self):
        return libSpeedy.pyQuoteAdapter_IsConnected(self.Obj)

    ## �s�u�n�JStarWave�污�D��.     
    # @param self	���󥻨�.
    # @param IP	�污�D��IP
    # @param Port	�污�D��Port
    # @param ID	StarWave�n�J�b��.
    # @param DownloadContracts �n�J���\��O�_�۰ʤU���ӫ~�򥻸��.�]�i�H�n�J���\��,�D�ʩI�sDownloadContracts().
    # @param Password	StarWave�b�����K�X. 
    def Logon(self, IP, Port,ID,Password,DownloadContracts):        
        libSpeedy.pyQuoteAdapter_Logon(self.Obj, IP.encode(), Port, ID.encode(), Password.encode(), DownloadContracts )
    
    ## �q�\�ӫ~�污 
    # �Ҧp �q�\�x�n�q�污�i�H�I�s ObjQuote.Subscribe( 'TWSE', '2330' )
    # @param Exchange �����
    #| �����   | �N�X     |
    #| ----:    |  :----   |
    #| �ҥ��   | 'TWSE'   |
    #| �d�R���� | 'OTC'    |
    #| �����   | 'TAIFEX' |
    # @param Symbol	 �ӫ~�N�X
    # @return TRUE ��ܭq�\���\,FALSE��ܭq�\����.�W�L�q�\�ƤW��.		
    def Subscribe(self, Exchange, Symbol):
        return libSpeedy.pyQuoteAdapter_Subscribe(self.Obj, Exchange.encode(), Symbol.encode())

    ## �ΰӫ~�򥻸�ƪ���q�\�污 
    # �Ҧp �q�\�x�n�q�污�i�H�I�s ObjQuote.SubscribeContract( ObjQuote.Stocks['2330'] )
    # @param Contract �ӫ~�򥻸�ƪ�����.    
    # @return TRUE ��ܭq�\���\,FALSE��ܭq�\����.�W�L�q�\�ƤW��.		
    def SubscribeContract(self, Contract ):
        return libSpeedy.pyQuoteAdapter_Subscribe(self.Obj, Contract.Exchange.encode(), Contract.Symbol.encode())
     
    ## �n�D�U���ӫ~�򥻸��
    # ��U�������� OnContractDownloadComplete �ƥ�|�Q�I�s.   
    def DownloadContracts(self):
        return libSpeedy.pyQuoteAdapter_DownloadContracts(self.Obj )

    ## �Ѻc��
    def __del__(self):
        pass
    #------------------------------------------------------------------------
    # -- Events --
    # inheritance spdQuoteAPI & implement
    #------------------------------------------------------------------------
## @cond                                 
    def __OnOrderBook(self, Exchange, Symbol, MsgTime, Msg):
        self.OnOrderBook(Exchange, Symbol, MsgTime, Msg[0])
        pass    

    def __OnContract(self, Ex, Sym, Name,MaturityDate, Category, Info ):        
        NewContract = ContractInfo( Ex, Sym, Name,MaturityDate, Category, Info[0] )
        if Info[0].Market ==  0:    # TAIFEX Taiwan Futures
           self.Futures[ Sym ] =  NewContract
        elif  Info[0].Market ==  1: # TAIFEX Taiwan Options
           self.Options[ Sym ] =  NewContract
        else:                       # TWSE/OTC Taiwan Stocks
           self.Stocks[ Sym ] =  NewContract
        pass

    def __OnComplete(self, Contracts ):
        print( 'Total Contract Count [{0}] '.format(Contracts))                    
        self.OnContractDownloadComplete()
        pass
## @endcond
    ## �s�u������Event 
    # @param self ���󥻨�. 
    def OnConnected(self):
        pass

    ## Event �o���_�u 
    # @param self ���󥻨�. 
    def OnDisconnected(self):
        pass

    ## �n�J���G�^�Ъ�Event 
    # @param self ���󥻨�. 
    # @param IsSucceed	�O�_���\ True:���\ False:���� 
    # @param ReplyString �n�J�T�� 
    def OnLogonResponse(self, IsSucceed, ReplyString):
        pass     
    
    ## �q���ӫ~�򥻸�ƤU��������Event ,����i�H��Stocks,Futures,Options�o�X��Dictionary����ӫ~�򥻸��
    # @param self ���󥻨�. 
    def OnContractDownloadComplete(self):        
        pass

    ## Event �e�Uï��s
    # @param self ���󥻨�. 
    # @param Exchange �����
    #| �����   | �N�X     |
    #| ----:    |  :----   |
    #| �ҥ��   | 'TWSE'   |
    #| �d�R���� | 'OTC'    |
    #| �����   | 'TAIFEX' |
    # @param Symbol �ӫ~�N�X 
    # @param MsgTime ��Ʈɶ� �榡�� HH:MM:SS.mmm 
    # @param Msg ���ɦ污��� structure�� class spdMsgOrderBook 
    def OnOrderBook(self, Exchange, Symbol, MsgTime, Msg):
        pass

    ## Event ����H�� 
    # @param self ���󥻨�. 
    # @param Exchange ����� 
    #| �����   | �N�X     |
    #| ----:    |  :----   |
    #| �ҥ��   | 'TWSE'   |
    #| �d�R���� | 'OTC'    |
    #| �����   | 'TAIFEX' |
    # @param Symbol	�ӫ~�N�X 		
    # @param MatchTime	����ɶ� �榡�� HH:MM:SS.mmm 
    # @param MatchPrice	�������
    # @param MatchQty	����ƶq
    def OnTrade(self, Exchange, Symbol, MatchTime, MatchPrice, MatchQty):
        pass
#----------------------------------------------------------------------------
