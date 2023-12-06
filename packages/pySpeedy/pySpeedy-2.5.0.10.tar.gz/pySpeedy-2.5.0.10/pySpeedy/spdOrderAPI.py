# -*- coding: cp950 -*-
##
# ���O : spdOrderAPI
# �@�� : Allen Lee, Simon Chang
# �\�� : spdOrderAPI�s��Speedy Order Server.���ѹ�x�W�����TWSE/OTC/TAIFEX������䴩.

## @cond DEV
#----------------------------------------------------------------------------
import ctypes, platform, os, sys
#----------------------------------------------------------------------------
if platform.system() == 'Windows':
    print('----- spdOrderAPI detect : Windows platform -----')
    if (sys.maxsize > 2**32) == True:
        print('Load['+os.path.dirname(__file__) + '\pySpeedyAPI_64.dll'+']')
        libSpeedy = ctypes.cdll.LoadLibrary( os.path.dirname(__file__) +  '\pySpeedyAPI_64.dll')
    else:
        print('Load['+os.path.dirname(__file__) + '\pySpeedyAPI.dll'+']')
        libSpeedy = ctypes.cdll.LoadLibrary( os.path.dirname(__file__) +  '\pySpeedyAPI.dll')
elif platform.system() == 'Linux':
    print('----- spdOrderAPI detect : Linux platform -----')
    print('Load['+os.path.dirname(__file__) + '/pySpeedyAPI_64.so'+']')
    libSpeedy = ctypes.cdll.LoadLibrary(os.path.dirname(__file__) + '/pySpeedyAPI_64.so')
#----------------------------------------------------------------------------
#
# prepare for class spdOrderAPI define
#
#----------------------------------------------------------------------------
def spdOrderDummyFun():
    pass
#----------------------------------------------------------------------------
# Declare the callback type
## \hiderefby
Def_pyOrderOnConnected        = ctypes.CFUNCTYPE(None)
## \hiderefby
Def_pyOrderOnDisconnected     = ctypes.CFUNCTYPE(None)
## \hiderefby
Def_pyOrderOnLogonResponse    = ctypes.CFUNCTYPE(None, ctypes.c_bool, ctypes.c_wchar_p)
## \hiderefby
Def_pyOrderOnReplyNewOrder    = ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_double, ctypes.c_wchar_p
                                                     , ctypes.c_long, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p)
## \hiderefby
Def_pyOrderOnReplyCancelOrder = ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_double, ctypes.c_wchar_p, ctypes.c_wchar_p)
## \hiderefby
Def_pyOrderOnReplyReplaceOrder = ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_double, ctypes.c_wchar_p
                                                     , ctypes.c_long, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p)
## \hiderefby
Def_pyOnRejectOrder           = ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p )
## \hiderefby
Def_pyOnFill                  = ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_long, ctypes.c_double, ctypes.c_long, ctypes.c_wchar_p)
# Keep "life cycle" of events function pointer to prevent "access violation"
gOrderFunPtr_OnConnected        = spdOrderDummyFun
gOrderFunPtr_OnDisconnected     = spdOrderDummyFun
gOrderFunPtr_OnLogonResponse    = spdOrderDummyFun
gOrderFunPtr_OnReplyNewOrder    = spdOrderDummyFun
gOrderFunPtr_OnReplyCancelOrder = spdOrderDummyFun
gOrderFunPtr_OnReplyReplaceOrder = spdOrderDummyFun
gOrderFunPtr_OnRejectOrder      = spdOrderDummyFun
gOrderFunPtr_OnFill             = spdOrderDummyFun

## @endcond
#----------------------------------------------------------------------------
#
# class spdOrderAPI
#
#----------------------------------------------------------------------------
class spdOrderAPI():
    #------------------------------------------------------------------------
    # Functions
    #------------------------------------------------------------------------
    # �غc�����|�ŧiC�����bPython������ƭ��.
    # �ëŧi����C��callback function.�õ��U��C���Ҳ�. 
    # @param self ���󥻨� 
    def __init__(self):
        # Functions definition
        # Constructor
        libSpeedy.pyOrderAdapter_New.argtypes = []
        libSpeedy.pyOrderAdapter_New.restype = ctypes.c_void_p
        # Delete
        libSpeedy.pyOrderAdapter_Delete.argtypes = [ctypes.c_void_p]
        libSpeedy.pyOrderAdapter_Delete.restype = None
        # IsConnected()
        libSpeedy.pyOrderAdapter_IsConnected.argtypes = [ctypes.c_void_p]
        libSpeedy.pyOrderAdapter_IsConnected.restype = ctypes.c_bool
        # Connect()
        libSpeedy.pyOrderAdapter_Connect.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
        libSpeedy.pyOrderAdapter_Connect.restype = None
        #EnAbleCA
        libSpeedy.pyOrderAdapter_EnableCA.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p]
        libSpeedy.pyOrderAdapter_EnableCA.restype = ctypes.c_bool
        # Logon()
        libSpeedy.pyOrderAdapter_Logon.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        libSpeedy.pyOrderAdapter_Logon.restype = None
        # LogonProxy()
        libSpeedy.pyOrderAdapter_LogonProxy.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        libSpeedy.pyOrderAdapter_LogonProxy.restype = None
        # SetAccount()
        libSpeedy.pyOrderAdapter_SetAccount.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        libSpeedy.pyOrderAdapter_SetAccount.restype = None
        # Disconnect()
        libSpeedy.pyOrderAdapter_Disconnect.argtypes = [ctypes.c_void_p]
        libSpeedy.pyOrderAdapter_Disconnect.restype = None
        # SendNewOrder()
        libSpeedy.pyOrderAdapter_SendNewOrder.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double,
                                                          ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        libSpeedy.pyOrderAdapter_SendNewOrder.restype = ctypes.c_int
        # SendCancelOrder()
        libSpeedy.pyOrderAdapter_SendCancelOrder.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
                                                             ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p]
        libSpeedy.pyOrderAdapter_SendCancelOrder.restype = ctypes.c_int
        # SendReplaceOrder()
        libSpeedy.pyOrderAdapter_SendReplaceOrder.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p,
                                                           ctypes.c_double, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]
        libSpeedy.pyOrderAdapter_SendReplaceOrder.restype = ctypes.c_int
        # RegEvents()
        libSpeedy.pyOrderAdapter_RegEvents.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
                                                       ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
        libSpeedy.pyOrderAdapter_RegEvents.restype = None

        libdir = os.path.dirname(__file__) 
        CurDir = os.path.abspath(os.getcwd())
        
        # Create pyOrderAdapter object
        os.chdir( libdir )        
        self.Obj = libSpeedy.pyOrderAdapter_New()
        os.chdir( CurDir )
        print("Package install directory: {0}".format(libdir))
        print("Current working directory: {0}".format(CurDir))

        # Keep "life cycle" of events function
        global gOrderFunPtr_OnConnected, gOrderFunPtr_OnDisconnected, gOrderFunPtr_OnLogonResponse, gOrderFunPtr_OnReplyNewOrder
        global gOrderFunPtr_OnReplyCancelOrder, gOrderFunPtr_OnReplyReplaceOrder, gOrderFunPtr_OnRejectOrder, gOrderFunPtr_OnFill
        # Binding events
        gOrderFunPtr_OnConnected         = Def_pyOrderOnConnected(self.OnConnected)
        gOrderFunPtr_OnDisconnected      = Def_pyOrderOnDisconnected(self.OnDisconnected)
        gOrderFunPtr_OnLogonResponse     = Def_pyOrderOnLogonResponse(self.OnLogonResponse)
        gOrderFunPtr_OnReplyNewOrder     = Def_pyOrderOnReplyNewOrder(self.OnReplyNewOrder)
        gOrderFunPtr_OnReplyCancelOrder  = Def_pyOrderOnReplyCancelOrder(self.OnReplyCancelOrder)
        gOrderFunPtr_OnReplyReplaceOrder = Def_pyOrderOnReplyReplaceOrder(self.OnReplyReplaceOrder)
        gOrderFunPtr_OnRejectOrder       = Def_pyOnRejectOrder(self.OnRejectOrder)
        gOrderFunPtr_OnFill              = Def_pyOnFill(self.OnFill)
        # Register events to C/C++
        libSpeedy.pyOrderAdapter_RegEvents(self.Obj, gOrderFunPtr_OnConnected, gOrderFunPtr_OnDisconnected, gOrderFunPtr_OnLogonResponse, gOrderFunPtr_OnReplyNewOrder,
                                           gOrderFunPtr_OnReplyCancelOrder, gOrderFunPtr_OnReplyReplaceOrder, gOrderFunPtr_OnRejectOrder, gOrderFunPtr_OnFill)
    
    ##�s�u��Speedy�U��D��
    # @param self	���󥻨�
    # @param IP	�U��D��IP
    # @param Port	�U��D��Port
    # @param TimeoutSec	�]�w�s�u�O�ɬ�� 
    def Connect(self, IP, Port, TimeoutSec):
        libSpeedy.pyOrderAdapter_Connect(self.Obj, IP.encode(), Port, TimeoutSec)
        
    ## �U��D���O�_�s�u 
    # @param self ���󥻨� 
    # @return TRUE ��ܳs�u���\,FALSE �_�u.		                                         
    def IsConnected(self):
        return libSpeedy.pyOrderAdapter_IsConnected(self.Obj)
        
    ## �ϥβĤT�责�Ѫ�ñ�� API 
    # @param self ���󥻨� 
    # @param APICode �ĤT��ñ�� API �N�X, 1:�Τ@FSC ActiveX API 2:���I MLSecurities ActiveX API  
    # @param �����ѧO��T�A�q�`�O�Τᨭ���Ҧr��
    # @param self ���󥻨� 
    # @return TRUE ��ܦ��\���Jñ�� API,FALSE ���J����.		                                         
    def EnableCA(self, APICode, CommonName):
        return libSpeedy.pyOrderAdapter_EnableCA(self.Obj, APICode, CommonName.encode())
    
    ## �n�JSpeedy�U��D��. 
    # @param self ���󥻨� .
    # @param ID	Speedy�n�J�b��.
    # @param Password	Speedy�b�����K�X.
    # @param Account	����b��.
    def Logon(self, ID, Password, Account):
        libSpeedy.pyOrderAdapter_Logon(self.Obj, ID.encode(), Password.encode(), Account.encode())
    
    ## �n�JSpeedy Proxy�U��D�� 
    # @param self ���󥻨� 		
    # @param ID	�D���b�� 
    # @param Password �D���b�����K�X
    # @param Account����b��       
    #
    def LogonProxy(self, ID, Password, Account):
        libSpeedy.pyOrderAdapter_LogonProxy(self.Obj, ID.encode(), Password.encode(), Account.encode())
    
    ## �]�w����b�� 
    # @param self ���󥻨� 	
    # @param Exchange	�����  ���ݬ��j�g�r�� 
    #| �����   | �N�X     |
    #| ----:    |  :----   |
    #| �ҥ��   | 'TWSE'   |
    #| �d�R���� | 'OTC'    |
    #| �����   | 'TAIFEX' |
    # @param BrokerID	��өδ��ӥN��
    # @param Account	����b��
    #
    def SetAccount(self, Exchange, BrokerID, Account):
        libSpeedy.pyOrderAdapter_SetAccount(self.Obj, Exchange.encode(), BrokerID.encode(), Account.encode())
        
    ## �P�U��D���_�u 
    # @param self ���󥻨� 	
    def Disconnect(self):
        libSpeedy.pyOrderAdapter_Disconnect(self.Obj)
        
    ## �ǰe�s����O    
    # @param self ���󥻨�.
    # @param Market	�����O  ���ݬ��p�g�r��.
    #| �����O   | �N�X   |
    #| ----:    |  :---- |
    #| �������� | 'tse'  |
    #| �d�R���� | 'otc'  |
    #| ���f���� | 'fut'  |
    #| ����v   | 'opt'  |
    # @param UDD �ϥΪ̹B�Ϊ��r��, �b�H�UEvent �o�ͮɷ|�a�^, OnReplyNewOrder, OnRejectOrder, OnFill, ����:128�H��.
    # @param Symbol �ӫ~�N�X
    # @param Price ����
    # @param Side �R��O, ��B��:Buy, ��S��:Sell, ���ݬ��j�g�r��.
    # @param OrderQty �e�U�ƶq
    # @param OrderType �e�U�覡. ���ݬ��j�g�r��.
    #| �N�X | ����   |
    #| ----:|  :---- |
    #| 'L'  | Limit order, ������.  |
    #| 'M'  | Market order, ������.  |
    #| 'P'  | Market with protection, �@�w�d�򥫻���,�ȴ���Ҥ䴩. |
    # @param TimeInForce �e�U���� ��R��:ROD, ��I��:IOC, ��F��:FOK, ���ݬ��j�g�r��.
    # @param TWSEOrdType TWSE/OTC Order type. 
    #| �N�X | ����   |
    #| ----:|  :---- |
    #| '0'  | regular trading Via Securities Finance.  |
    #| '1'  | Purchase on Margin.  |
    #| '2'  | Short Sell. Via Securities Firms conduct Margin Lending.  |
    #| '3'  | Purchase on Margin.  |
    #| '4'  | Short Sell.  |
    #| '5'  | SBL Short Sell type 5  |
    #| '6'  | SBL Short Sell type 5  |
    # @return NID ���ߤ@��ID,����s��^���ɽгz�LNID�����^���, �YNID�^0��ܱa�J��즳�~ 
    #
    def SendNewOrder(self, Market, UDD, Symbol, Price, Side, OrderQty, OrderType, TimeInForce, TWSEOrdType ):
        return libSpeedy.pyOrderAdapter_SendNewOrder(self.Obj, Market.encode(), UDD.encode(), Symbol.encode(), Price,
                                                     Side.encode(), OrderQty, OrderType.encode(), TimeInForce.encode(), TWSEOrdType.encode())
    ## �e�X�R����O 
    # @param self	���󥻨�.
    # @param Market	�����O  ���ݬ��p�g�r��.
    #| �����O   | �N�X   |
    #| ----:    |  :---- |
    #| �������� | 'tse'  |
    #| �d�R���� | 'otc'  |
    #| ���f���� | 'fut'  |
    #| ����v   | 'opt'  |
    # @param UDD	�ϥΪ̹B�Ϊ��r��, �b�H�UEvent �o�ͮɷ|�a�^, OnReplyNewOrder, OnRejectOrder, OnFill, ����:128�H��.
    # @param Symbol	�ӫ~�N�X
    # @param Price	����
    # @param Side	�R��O, ��B��:Buy, ��S��:Sell, ���ݬ��j�g�r��.
    # @param OrderID	����Һݳ渹 
    # @return NID ���ߤ@��ID,����R��^���ɽгz�LNID�����^��e�U��, �YNID�^0��ܱa�J��즳�~.
    #
    def SendCancelOrder(self, Market, UDD, Symbol, Price, Side, OrderID):
        return libSpeedy.pyOrderAdapter_SendCancelOrder(self.Obj, Market.encode(), UDD.encode(), Symbol.encode(), Price, Side.encode(), OrderID.encode())

    ## �e�X�����O 
    # @param self	���󥻨�.
    # @param Market	�����O  ���ݬ��p�g�r��.
    #| �����O   | �N�X   |
    #| ----:    |  :---- |
    #| �������� | 'tse'  |
    #| �d�R���� | 'otc'  |
    #| ���f���� | 'fut'  |
    #| ����v   | 'opt'  |
    # @param UDD	�ϥΪ̹B�Ϊ��r��, �b�H�UEvent �o�ͮɷ|�a�^, OnReplyNewOrder, OnRejectOrder, OnFill, ����:128�H��.
    # @param Symbol	�ӫ~�N�X
    # @param OrderID	��檺����Һݳ渹
    # @param Side	�R��O, ��B��:Buy, ��S��:Sell, ���ݬ��j�g�r��.
    # @param Price	���� �����������(��q�ɶ�0)
    # @param OrderQty	�e�U�ƶq ����q(����ɶ�0)
    # @param OrderType	�e�U�覡, ���ݬ��j�g�r��.
    #| �N�X | ����   |
    #| ----:|  :---- |
    #| 'L'  | Limit order, ������.  |
    #| 'M'  | Market order, ������.  |
    #| 'P'  | Market with protection, �@�w�d�򥫻���,�ȴ���Ҥ䴩. |
    # @param TimeInForce	�e�U���� ��R��:ROD, ��I��:IOC, ��F��:FOK, ���ݬ��j�g�r��.
    # @return NID ���ߤ@��ID,������^���ɽгz�LNID�����^��e�U��, �YNID�^0��ܱa�J��즳�~.
    #
    def SendReplaceOrder(self, Market, UDD, Symbol, OrderID, Side, Price, OrderQty, OrderType, TimeInForce):
        return libSpeedy.pyOrderAdapter_SendReplaceOrder(self.Obj, Market.encode(), UDD.encode(), Symbol.encode(), OrderID.encode(), Side.encode(), Price,
                                                      OrderQty, OrderType.encode(), TimeInForce.encode())        
    #------------------------------------------------------------------------
    # Events
    # inheritance spdOrderAPI & implement
    #------------------------------------------------------------------------
    ## �s�u���\�� Event
    # @param self ���󥻨�.
    def OnConnected(self):
        pass

    ## �o���_�u�� Event
    # @param self ���󥻨�.
    def OnDisconnected(self):
        pass

    ## �n�J���G�^�Ъ� Event 
    # @param self  ���󥻨�.
    # @param IsSucceed	�O�_���\.  True:���\ False:���� 
    # @param ReplyString Server�^�_���n�J�T�� 
    def OnLogonResponse(self, IsSucceed, ReplyString):
        pass

    ## Event �s��^��     
    # @param self	���󥻨�.
    # @param NID	�����渹
    # @param UDD	SendNewOrder�ұa��User Define Data
    # @param Symbol	�ӫ~�N�X
    # @param Price	����
    # @param Side	�R��O��B��:Buy ��S��:Sell
    # @param OrderQty	�e�U�ƶq
    # @param OrderType	�e�U�覡
    #| �N�X | ����   |
    #| ----:|  :---- |
    #| 'L'  | Limit order, ������.  |
    #| 'M'  | Market order, ������.  |
    #| 'P'  | Market with protection, �@�w�d�򥫻���,�ȴ���Ҥ䴩. |
    # @param TimeInForce	�e�U����R��:ROD,��I��:IOC,��F��:FOK
    # @param OrderID	����Һݳ渹 
    def OnReplyNewOrder(self, NID, UDD, Symbol, Price, Side, OrderQty, OrderType, TimeInForce, OrderID):
        pass

    ## Event �R��^��
    # @param self	���󥻨�.
    # @param NID	�����渹
    # @param UDD	SendCancelOrder�ұa��User Define Data
    # @param Symbol	�ӫ~�N�X
    # @param Price	����
    # @param Side	�R��O��B��:Buy ��S��:Sell
    # @param OrderID	����Һݳ渹 
    def OnReplyCancelOrder(self, NID, UDD, Symbol, Price, Side, OrderID):
        pass

    ## Event ���^�� 
    # @param self	���󥻨�.
    # @param NID	�����渹
    # @param UDD	SendNewOrder�ұa��User Define Data
    # @param Symbol	�ӫ~�N�X
    # @param Price	����᪺����(��q�ɬ�0)
    # @param Side	�R��O��B��:Buy ��S��:Sell
    # @param OrderQty	��q�᪺�q(����ɬ�0)
    # @param OrderType	�e�U�覡
    #| �N�X | ����   |
    #| ----:|  :---- |
    #| 'L'  | Limit order, ������.  |
    #| 'M'  | Market order, ������.  |
    #| 'P'  | Market with protection, �@�w�d�򥫻���,�ȴ���Ҥ䴩. |
    # @param TimeInForce	�e�U����R��:ROD,��I��:IOC,��F��:FOK
    # @param OrderID	����Һݳ渹 
    def OnReplyReplaceOrder(self, NID, UDD, Symbol, Price, Side, OrderQty, OrderType, TimeInForce, OrderID):
        pass

    ## Event  �e�U���Ѧ^�� 
    # @param self	���󥻨�.
    # @param NID	�����渹
    # @param UDD	SendNewOrder �� SendCancelOrder �� SendReplaceOrder �ұa��User Define Data.
    # @param ActionFrom	�e�U�������O 'N':Reject New Order,��C��:Reject Cancel Order,��R��: Reject Replace Order
    # @param ErrCode	���~�N��
    # @param ErrMsg	���~�T�� 
    def OnRejectOrder(self, NID, UDD, ActionFrom, ErrCode, ErrMsg):
        pass

    ## Event ����^��
    # @param self	���󥻨�.
    # @param NID	�����渹
    # @param UDD	SendNewOrder�ұa��User Define Data
    # @param OrderID	����Һݳ渹
    # @param ReportSequence	�^���Ǹ�
    # @param FillPrice	�������
    # @param FillQty	����q
    # @param FillTime	����ɶ� �ҥ��:HHMMSSmm, �����:HHMMSSmmm 
    def OnFill(self, NID, UDD, OrderID, ReportSequence, FillPrice, FillQty, FillTime):
        pass
#----------------------------------------------------------------------------

