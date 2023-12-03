from asyncio import ensure_future
import json
from ctypes import *
import platform
import os
import re
import struct



OS = platform.system()
if OS == "Windows":
    import win32api

class GPF:
    def __init__(self, dataPath="./data"):
        dll_name_gpf = ''
        dll_name_bcc = ''
        self.IsCRFInit =0
        self.IsPOSInit =0
        self.IsBCCInit =0
        self.IsGPFInit =0
        self.hHandleGPF=0
        self.hHandleCRFPOS=0

        if OS == "Windows":
            dll_name_gpf = 'gpflib.dll'
            dll_name_bcc = 'bcclib.dll'
        else:
            dll_name_gpf = 'libgpflib.so'
            dll_name_bcc = 'libbcclib.so'

        self.buf_max_size = 2048*1000
        self.CRFModel="Segment.dat"
        self.CRFTag=""
        self.POSData="idxPOS.dat"

        dll_file_gpf = os.path.join(os.path.dirname(os.path.abspath(__file__)), dll_name_gpf)
        dll_file_bcc = os.path.join(os.path.dirname(os.path.abspath(__file__)), dll_name_bcc)
        cfg_file_gpf = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'GPFconfig.txt')
        cfg_file_bcc = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'BCCconfig.txt')
        cfg_file_parser= os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Parser.lua')
        cfg_file_CRFModel= os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Segment.dat')
        cfg_file_POSData=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'idxPOS.dat')

        self.library_gpf = cdll.LoadLibrary(dll_file_gpf)
        self.library_bcc = cdll.LoadLibrary(dll_file_bcc)

        self.ParserBCC=cfg_file_parser
        self.ConfigGPF= cfg_file_gpf
        self.ConfigBCC= cfg_file_bcc
        self.dataPath= dataPath
        self.buf_max_size = 2048*1000
        self.CRFModel=cfg_file_CRFModel
        self.POSData=cfg_file_POSData
        self.CRFTag=""
        self.RetBuff =create_string_buffer(''.encode(), self.buf_max_size)

        self.library_gpf.GPF_LatticeInit.argtypes = []
        self.library_gpf.GPF_LatticeInit.restype  = c_void_p  
        self.hHandleGPF=self.library_gpf.GPF_LatticeInit();

        self.library_gpf.GPF_CRFPOSInit.argtypes = []
        self.library_gpf.GPF_CRFPOSInit.restype  = c_void_p  
        self.hHandleCRFPOS =self.library_gpf.GPF_CRFPOSInit()


        # https://stackoom.com/question/1VWM
        if OS == "Windows":
            self.dll_close = win32api.FreeLibrary
        elif OS == "Linux":
            try:
                stdlib = CDLL("")
            except OSError:
                stdlib = CDLL("libc.so")
            self.dll_close = stdlib.dlclose
            self.dll_close.argtypes = [c_void_p]

    def __del__(self):
        self.library_gpf.GPF_POSExit();
        self.library_bcc.BCC_Exit();
        self.library_gpf.GPF_CRFExit()
        self.library_gpf.GPF_Term(c_void_p(self.hHandleGPF))
        self.library_gpf.GPF_CRFPOSExit(c_void_p(self.hHandleCRFPOS))

        self.dll_close(self.library_gpf._handle)
        self.dll_close(self.library_bcc._handle)

    def SetGridText(self, text):
        return self.SetText(text)
    
    def SetText(self, text):
        self.library_gpf.GPF_SetText.argtypes = [c_void_p, c_char_p]
        self.library_gpf.GPF_SetText.restype  = c_int
        ret = self.library_gpf.GPF_SetText(self.hHandleGPF, text.encode())
        return ret


    def AddGridJS(self, json_str):
        self.library_gpf.GPF_AddStructure.argtypes = [c_void_p, c_char_p]
        self.library_gpf.GPF_AddStructure.restype  = c_int
        ret = self.library_gpf.GPF_AddStructure(self.hHandleGPF, json_str.encode())
        return ret

    def AddStructure(self, json_str):
        self.library_gpf.GPF_AddStructure.argtypes = [c_void_p, c_char_p]
        self.library_gpf.GPF_AddStructure.restype  = c_int
        ret = self.library_gpf.GPF_AddStructure(self.hHandleGPF, json_str.encode())
        return ret

    def CallService(self, sentence, name):
        self.GPFInit()
        self.library_gpf.GPF_CallService.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_int]
        self.library_gpf.GPF_CallService.restype  = c_int
        str_len = self.library_gpf.GPF_CallService(self.hHandleGPF, name.encode(), sentence.encode(), self.RetBuff, self.buf_max_size)
        ret = string_at(self.RetBuff, str_len)
        return ret.decode()


    def SetTable(self, tableName):
        self.GPFInit()                
        self.library_gpf.GPF_SetLexicon.argtypes = [c_void_p, c_char_p]
        self.library_gpf.GPF_SetLexicon.restype  = c_int
        ret = self.library_gpf.GPF_SetLexicon(self.hHandleGPF, tableName.encode())
        return ret

    def CallTable(self, tableName,Mode=0):
        self.GPFInit()
        if Mode==0:
            self.library_gpf.GPF_AppLexicon.argtypes = [c_void_p, c_char_p]
            self.library_gpf.GPF_AppLexicon.restype  = c_int
            self.library_gpf.GPF_AppLexicon(self.hHandleGPF, tableName.encode())
            return 0
        self.library_gpf.GPF_SetLexicon.argtypes = [c_void_p, c_char_p]
        self.library_gpf.GPF_SetLexicon.restype  = c_int
        ret = self.library_gpf.GPF_SetLexicon(self.hHandleGPF, tableName.encode())
        return ret

    def GetSuffix(self, tableName, sentence):
        self.GPFInit()        
        self.library_gpf.GPF_GetSuffix.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_int]
        self.library_gpf.GPF_GetSuffix.restype  = c_int
        str_len = self.library_gpf.GPF_GetSuffix(self.hHandleGPF, tableName.encode(), sentence.encode(), self.RetBuff, self.buf_max_size)
        ret = string_at(self.RetBuff, str_len)
        return ret.decode()
    
    def GetPrefix(self, tableName, sentence):
        self.GPFInit()                
        self.library_gpf.GPF_GetPrefix.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_int]
        self.library_gpf.GPF_GetPrefix.restype  = c_int
        str_len = self.library_gpf.GPF_GetPrefix(self.hHandleGPF, tableName.encode(), sentence.encode(), self.RetBuff, self.buf_max_size)
        ret = string_at(self.RetBuff, str_len)
        return ret.decode()

    def GetWord(self, UnitNo):
        
        self.library_gpf.GPF_GetWord.argtypes = [c_void_p, c_char_p, c_char_p, c_int]
        self.library_gpf.GPF_GetWord.restype  = c_int
        str_len = self.library_gpf.GPF_GetWord(self.hHandleGPF, UnitNo.encode(), self.RetBuff, self.buf_max_size)
        ret = string_at(self.RetBuff, str_len)
        return ret.decode()

    def RunFSA(self, fsaName, param=""):
        return self.CallFSA(fsaName, param)

    def CallFSA(self, fsaName, param=""):
        self.GPFInit()                
        self.library_gpf.GPF_RunFSA.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_int]
        self.library_gpf.GPF_RunFSA.restype  = c_int

        self.library_gpf.GPF_SetFSAPath.argtypes = [c_void_p, c_char_p, c_int]
        self.library_gpf.GPF_SetFSAPath.restype  = c_int

        len = self.library_gpf.GPF_RunFSA(self.hHandleGPF, fsaName.encode(), param.encode(),self.RetBuff,self.buf_max_size)

        TotalNum=struct.unpack("i",self.RetBuff[0:4])
        offset=4
        for i in range(TotalNum[0]):
            OperationLen=struct.unpack("i",self.RetBuff[offset:offset+4])
            offset+=4
            code=self.RetBuff[offset:offset+OperationLen[0]]
            offset+=OperationLen[0]
            MatchPathLen=struct.unpack("i",self.RetBuff[offset:offset+4])
            offset+=4
            self.library_gpf.GPF_SetFSAPath(self.hHandleGPF, self.RetBuff[offset:offset+MatchPathLen[0]],MatchPathLen[0])
            offset+=MatchPathLen[0]
            exec(code.decode())

        return len

    def GetParam(self, key):
        return self.GetFSAParam(key)

    def GetFSAParam(self, key):
        
        self.library_gpf.GPF_GetParam.argtypes = [c_void_p, c_char_p, c_char_p, c_int]
        self.library_gpf.GPF_GetParam.restype  = c_int
        str_len = self.library_gpf.GPF_GetParam(self.hHandleGPF, key.encode(), self.RetBuff, self.buf_max_size)
        ret = string_at(self.RetBuff, str_len)
        return ret.decode()
    
        
    def GetGrid(self):
        
        self.library_gpf.GPF_GetGrid.argtypes = [c_void_p, c_char_p, c_int]
        self.library_gpf.GPF_GetGrid.restype  = c_int
        str_len = self.library_gpf.GPF_GetGrid(self.hHandleGPF, self.RetBuff, self.buf_max_size)
        if str_len != 0:
            str_ret = string_at(self.RetBuff, str_len)
            json_data = json.loads(str_ret.decode())
            return json_data
        return json.loads("{}")

    def GetGridText(self, begin=0, end=-1):
        return self.GetText(self, begin, end)

    def GetText(self, begin=0, end=-1):
        self.library_gpf.GPF_GetTextByRange.argtypes = [c_void_p, c_int, c_int, c_char_p, c_int]
        self.library_gpf.GPF_GetTextByRange.restype  = c_int
        str_len = self.library_gpf.GPF_GetTextByRange(self.hHandleGPF, begin, end, self.RetBuff, self.buf_max_size)
        ret = string_at(self.RetBuff, str_len)
        return ret.decode()

    def GetGridKV(self, key=""):
        return self.GetGridKVs(key)

    def GetGridKVs(self, key=""):
        self.library_gpf.GPF_GetGridKVs.argtypes = [c_void_p, c_char_p, c_char_p, c_int]
        self.library_gpf.GPF_GetGridKVs.restype  = c_int
        str_len = self.library_gpf.GPF_GetGridKVs(self.hHandleGPF, key.encode(), self.RetBuff, self.buf_max_size)
        if str_len != 0:
            ret = string_at(self.RetBuff, str_len)
            json_data = json.loads(ret.decode())
            return json_data
        return json.loads("{}")

    
    def GetFSAUnit(self, pathNo):
        self.library_gpf.GPF_GetUnitByInt.argtypes = [c_void_p, c_int, c_char_p, c_int]
        self.library_gpf.GPF_GetUnitByInt.restype  = c_int
        str_len = self.library_gpf.GPF_GetUnitByInt(self.hHandleGPF, pathNo, self.RetBuff, self.buf_max_size)
        ret = string_at(self.RetBuff, str_len)
        return ret.decode()

    def GetUnit(self, kv,UnitNo="",UExpress=""):
        return self.GetUnits(kv,UnitNo,UExpress)

    def GetUnits(self, kv,UnitNo="",UExpress=""):
        self.library_gpf.GPF_GetUnitsByKV.argtypes = [c_void_p, c_char_p, c_char_p, c_int]
        self.library_gpf.GPF_GetUnitsByKV.restype  = c_int

        self.library_gpf.GPF_GetUnitsByNo.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
        self.library_gpf.GPF_GetUnitsByNo.restype  = c_int

        if UnitNo == "":
            str_len = self.library_gpf.GPF_GetUnitsByKV(self.hHandleGPF, kv.encode(), self.RetBuff, self.buf_max_size)
        else:
            str_len = self.library_gpf.GPF_GetUnitsByNo(self.hHandleGPF, UnitNo.encode(),UExpress.encode(),kv.encode(), self.RetBuff, self.buf_max_size)

        if str_len != 0:
            ret = string_at(self.RetBuff, str_len)
            json_data = json.loads(ret.decode())
            return json_data
        return 0
   
    def GetUnitKV(self, unitNo, key=""):
        self.GetUnitKVs(unitNo, key)

    def GetUnitKVs(self, unitNo, key=""):
        self.library_gpf.GPF_GetUnitKVs.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_int]
        self.library_gpf.GPF_GetUnitKVs.restype  = c_int
        str_len = self.library_gpf.GPF_GetUnitKVs(self.hHandleGPF, unitNo.encode(), key.encode(), self.RetBuff, self.buf_max_size)
        if str_len != 0:
            ret = string_at(self.RetBuff, str_len)
            json_data = json.loads(ret.decode())
            if key == "Word" or key == "HeadWord" or key == "CharType"or key == "POS":
                return  json_data[0]

            if key == "From" or key == "To":
                return  int(json_data[0])

            return json_data
        return json.loads("{}")

    def GetRelation(self, kv=""):
        self.GetRelations(kv)

    def GetRelations(self, kv=""):
        self.library_gpf.GPF_GetRelations.argtypes = [c_void_p, c_char_p, c_char_p, c_int]
        self.library_gpf.GPF_GetRelations.restype  = c_int
        str_len = self.library_gpf.GPF_GetRelations(self.hHandleGPF, kv.encode(), self.RetBuff, self.buf_max_size)
        if str_len != 0:
            ret = string_at(self.RetBuff, str_len)
            json_data = json.loads(ret.decode())
            return json_data
        return json.loads("{}")

    def GetRelationKV(self, unitNo1, unitNo2, role, key=""):
        return self.GetRelationKV( unitNo1, unitNo2, role, key)

    def GetRelationKVs(self, unitNo1, unitNo2, role, key=""):
        self.library_gpf.GPF_GetRelationKVs.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
        self.library_gpf.GPF_GetRelationKVs.restype  = c_int
        str_len = self.library_gpf.GPF_GetRelationKVs(self.hHandleGPF, unitNo1.encode(), unitNo2.encode(), role.encode(), key.encode(), self.RetBuff, self.buf_max_size)
        if str_len != 0:
            ret = string_at(self.RetBuff, str_len)
            json_data = json.loads(ret.decode())
            return json_data
        return json.loads("{}")

    def GetTableItem(self, tableName, kv=""):
        self.GPFInit()                
        return self.GetTableItems(tableName, kv)

    def GetTableItems(self, tableName, kv=""):
        self.GPFInit()                
        self.library_gpf.GPF_GetTableItems.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_int]
        self.library_gpf.GPF_GetTableItems.restype  = c_int
        str_len = self.library_gpf.GPF_GetTableItems(self.hHandleGPF, tableName.encode(), kv.encode(), self.RetBuff, self.buf_max_size)
        if str_len != 0:
            ret = string_at(self.RetBuff, str_len)
            json_data = json.loads(ret.decode())
            return json_data
        return json.loads("{}")

    def GetTableItemKV(self, tableName, item="", key=""):
        self.GPFInit()                
        return self.GetTableItemKVs(tableName, item, key)

    def GetTableItemKVs(self, tableName, item="", key=""):
        self.GPFInit()                
        self.library_gpf.GPF_GetTableItemKVs.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
        self.library_gpf.GPF_GetTableItemKVs.restype  = c_int
        str_len = self.library_gpf.GPF_GetTableItemKVs(self.hHandleGPF, tableName.encode(), item.encode(), key.encode(), self.RetBuff, self.buf_max_size)
        if str_len != 0:
            ret = string_at(self.RetBuff, str_len)
            json_data = json.loads(ret.decode())
            return json_data
        return json.loads("{}")

    def GetFSANode(self, tag="-1"):
        self.library_gpf.GPF_GetFSANodeByTag.argtypes = [c_void_p, c_char_p, c_char_p, c_int]
        self.library_gpf.GPF_GetFSANodeByTag.restype  = c_int
        PathNo = self.library_gpf.GPF_GetFSANodeByTag(self.hHandleGPF, tag.encode(), self.RetBuff, self.buf_max_size)
        return PathNo

    def AddUnit(self, colNo,text):
        self.library_gpf.GPF_AddUnit.argtypes = [c_void_p, c_int, c_char_p, c_char_p, c_int]
        self.library_gpf.GPF_AddUnit.restype  = c_int
        str_len = self.library_gpf.GPF_AddUnit(self.hHandleGPF, colNo, text.encode(), self.RetBuff, self.buf_max_size)
        ret = string_at(self.RetBuff, str_len)
        return ret.decode()

    def AddUnitKV(self, unitNo, key,val):
        self.library_gpf.GPF_AddUnitKV.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p]
        self.library_gpf.GPF_AddUnitKV.restype  = c_int
        Values=re.split(r"[ ;,\t]",val)
        for Value in Values:
            self.library_gpf.GPF_AddUnitKV(self.hHandleGPF, unitNo.encode(), key.encode(), Value.encode())
        return 1

    def AddGridKV(self, key,val):
        self.library_gpf.GPF_AddGridKV.argtypes = [c_void_p, c_char_p, c_char_p]
        self.library_gpf.GPF_AddGridKV.restype  = c_int
        Values=re.split(r"[ ;,\t]",val)
        for Value in Values:
            self.library_gpf.GPF_AddGridKV(self.hHandleGPF, key.encode(),Value.encode())
        return 0
    
    def AddRelation(self, unitNo1, unitNo2, role):
        self.library_gpf.GPF_AddRelation.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p]
        self.library_gpf.GPF_AddRelation.restype  = c_int
        self.library_gpf.GPF_AddRelation(self.hHandleGPF, unitNo1.encode(), unitNo2.encode(), role.encode())
        return 1

    def AddRelationKV(self, unitNo1, unitNo2, role, key, val):
        self.library_gpf.GPF_AddRelationKV.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
        self.library_gpf.GPF_AddRelationKV.restype  = c_int
        Values=re.split(r"[ ;,\t]",val)
        for Value in Values:
            self.library_gpf.GPF_AddRelationKV(self.hHandleGPF, unitNo1.encode(), unitNo2.encode(), role.encode(), key.encode(), Value.encode(), self.RetBuff, self.buf_max_size)
        return 1

    def IsUnit(self, unitNo, kv):
        self.library_gpf.GPF_IsUnit.argtypes = [c_void_p, c_char_p, c_char_p]
        self.library_gpf.GPF_IsUnit.restype  = c_int
        ret = self.library_gpf.GPF_IsUnit(self.hHandleGPF, unitNo.encode(), kv.encode())
        return ret

    def IsRelation(self, unitNo1, unitNo2, role, kv=""):
        self.library_gpf.GPF_IsRelation.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_char_p]
        self.library_gpf.GPF_IsRelation.restype  = c_int
        ret = self.library_gpf.GPF_IsRelation(self.hHandleGPF, unitNo1.encode(), unitNo2.encode(), role.encode(), kv.encode())
        return ret

    def IsTable(self, tableName, item="", kv=""):
        self.library_gpf.GPF_IsTable.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p]
        self.library_gpf.GPF_IsTable.restype  = c_int
        ret = self.library_gpf.GPF_IsTable(self.hHandleGPF, tableName.encode(), item.encode(), kv.encode())
        return ret

   
    def IndexFSA(self, rule_filename):
        self.library_gpf.GPF_MakeRule.argtypes = [c_char_p]
        self.library_gpf.GPF_MakeRule.restype  = c_int
        ret = self.library_gpf.GPF_MakeRule(rule_filename.encode())
        self.library_gpf.GPF_ReLoad.argtypes = [c_char_p]
        self.library_gpf.GPF_ReLoad.restype  = c_int
        self.library_gpf.GPF_ReLoad(self.ConfigGPF.encode())
        return ret
    
    def Write2File(self, json_data,Idx2):
        RetInf=0
        Out=open(Idx2,"w",encoding="utf8")
        for Table in json_data:
            Items=self.GetTableItems(Table)
            for Item in Items:
                Colls=self.GetTableItemKVs(Table,Item,"Coll")
                for Coll in Colls:
                    CollItems=self.GetTableItemKVs(Table,Item,Coll)
                    if len(CollItems)>0:
                        self.WriteColl2File(Item,Coll,CollItems,Out)
                        RetInf=1
        Out.close()
        return RetInf

    def WriteColl2File(self, Item,Coll,CollItems,Out):
        Line="Table "+Coll+"_"+Item
        print(Line,file=Out)
        for Item in CollItems:
            print(Item,file=Out)
        
    def IndexTable(self, table_filename):
        
        self.library_gpf.GPF_MakeTable.argtypes = [c_char_p, c_char_p, c_int]
        self.library_gpf.GPF_MakeTable.restype  = c_int
        str_len = self.library_gpf.GPF_MakeTable(table_filename.encode(),self.RetBuff,self.buf_max_size)
        self.library_gpf.GPF_ReLoad.argtypes = [c_char_p]
        self.library_gpf.GPF_ReLoad.restype  = c_int
        self.library_gpf.GPF_ReLoad(self.ConfigGPF.encode())
        if str_len != 0 :
            str_ret = string_at(self.RetBuff, str_len)
            json_data = json.loads(str_ret.decode())
            Idx2=os.path.dirname(table_filename)+"/Coll_"+os.path.basename(table_filename)
            if self.Write2File(json_data,Idx2):
                self.IndexTable(Idx2)
            os.remove(Idx2)
            self.library_gpf.GPF_ReLoad.argtypes = [c_char_p]
            self.library_gpf.GPF_ReLoad.restype  = c_int
            self.library_gpf.GPF_ReLoad(self.ConfigGPF.encode())
            return json_data
        return 0

    def GetLog(self):
        
        self.library_gpf.GPF_GetLog.argtypes = [c_void_p, c_char_p, c_int]
        self.library_gpf.GPF_GetLog.restype  = c_int
        str_len=self.library_gpf.GPF_GetLog(self.hHandleGPF,self.RetBuff,self.buf_max_size)
        if str_len != 0:
            str_ret = string_at(self.RetBuff, str_len)
            json_data = json.loads(str_ret.decode())
            return json_data
        return json.loads("{}")

    def Reduce(self,From=0,To=-1,Head=-1):
        
        self.library_gpf.GPF_Reduce.argtypes = [c_void_p, c_int,c_int,c_char_p, c_int]
        self.library_gpf.GPF_Reduce.restype  = c_int
        str_len=self.library_gpf.GPF_Reduce(self.hHandleGPF,From,To,self.RetBuff,self.buf_max_size)
        HeadUnit=self.GetUnit(Head)
        self.library_gpf.GPF_SetHead.argtypes = [c_void_p, c_char_p, c_char_p]
        self.library_gpf.GPF_SetHead.restype  = c_int
        self.library_gpf.GPF_SetHead(self.hHandleGPF,self.RetBuff,HeadUnit)
        ret = string_at(self.RetBuff, str_len)
        return ret.decode()

    def IndexBCC(self, filelistname):
        ret=0
        self.library_bcc.BCC_IndexBCC.argtypes = [c_char_p, c_char_p, c_char_p]
        self.library_bcc.BCC_IndexBCC.restype  = c_int
        if isinstance(filelistname,str):
            ret = self.library_bcc.BCC_IndexBCC(self.ConfigBCC.encode(),filelistname.encode(),self.dataPath.encode())
        else:
            if not os.path.exists(self.dataPath):
                os.mkdir(os.path.abspath(self.dataPath))
            filelist=os.path.join(self.dataPath,"indexlist.tmp")
            Out=open(filelist,"w")
            for File in filelistname:
                print(File,file=Out)    
            Out.close()
            ret = self.library_bcc.BCC_IndexBCC(self.ConfigBCC.encode(),filelist.encode(),self.dataPath.encode())
        return ret

    def CallBCC(self, query,Server=""):
        if Server != "":
            return self.CallService(query,Server)
        if self.IsBCCInit == 0:
            self.library_bcc.BCC_Init.argtypes = [c_char_p]
            self.library_bcc.BCC_Init.restype  = c_int 
            self.IsBCCInit=self.library_bcc.BCC_Init(self.dataPath.encode())
        if self.IsBCCInit == 0:
            return json.loads("{}")
        self.library_bcc.BCC_RunBCC.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p]
        self.library_bcc.BCC_RunBCC.restype  = c_int
        str_len = self.library_bcc.BCC_RunBCC(self.ParserBCC.encode(),self.dataPath.encode(),query.encode(),self.RetBuff)
        ret = string_at(self.RetBuff, str_len)
        return ret.decode()

    def AddBCCKV(self, Key,Val,Server=""):
        Values=re.split(r"[ ;,\t]",Val)
        Val=";".join(Values)
        Query="AddKV({},{})".format(Key,Val)
        return self.CallBCC(Query,Server)

    def GetBCCKV(self, Key="",Server=""):
        if Key=="":
            Query="GetKV()"
        else:
            Query="GetKV({})".format(Key)
        return self.CallBCC(Query,Server)

    def GetBCCKVs(self, Key="",Server=""):
        if Key=="":
            Query="GetKV()"
        else:
            Query="GetKV({})".format(Key)
        return self.CallBCC(Query,Server)

    def ClearBCCKV(self, Key="",Server=""):
        Query="ClearKV()"
        return self.CallBCC(Query,Server)

    def Segment(self,text,table=""):
        if self.IsCRFInit ==0:
            self.library_gpf.GPF_CRFInit.argtypes = [c_char_p,c_char_p]
            self.library_gpf.GPF_CRFInit.restype  = c_int
            self.IsCRFInit = self.library_gpf.GPF_CRFInit(self.CRFModel.encode(),self.CRFTag.encode())

        if self.IsCRFInit == 0:
            return ""                
        ret=""
        if table == "":
            self.library_gpf.GPF_Seg.argtypes = [c_void_p, c_char_p, c_char_p]
            self.library_gpf.GPF_Seg.restype  = c_int
            str_len=self.library_gpf.GPF_Seg(self.hHandleCRFPOS,text.encode(),self.RetBuff,1)
            ret = string_at(self.RetBuff, str_len)
        else:
            self.SetGridText(text)
            self.library_gpf.GPF_GridSegUser.argtypes = [c_void_p, c_char_p, c_char_p,c_int]
            self.library_gpf.GPF_GridSegUser.restype  = c_int
            str_len=self.library_gpf.GPF_GridSegUser(self.hHandleGPF,table.encode(),self.RetBuff,1)
            ret = string_at(self.RetBuff, str_len)
        return ret.decode()  

    def POS(self,text,table=""):
        if self.IsPOSInit ==0:
            self.library_gpf.GPF_POSInit.argtypes = [c_char_p]
            self.library_gpf.GPF_POSInit.restype  = c_int
            self.IsPOSInit = self.library_gpf.GPF_POSInit(self.POSData.encode())
        if self.IsPOSInit == 0:
            return ""
        Ret=self.Segment(text,table)
        self.library_gpf.GPF_POS.argtypes = [c_void_p, c_char_p, c_char_p,c_int]
        self.library_gpf.GPF_POS.restype  = c_int
        str_len=self.library_gpf.GPF_POS(self.hHandleCRFPOS,Ret.encode(),self.RetBuff,1)
        ret = string_at(self.RetBuff, str_len)
        return ret.decode()
    #
    # Others:
    # Command="Context"/"Freq"
    # Number=1000/-1
    # Target="$Q"
    # Service=""
    # WinSize=20
    # Print="Lua"
    # Speedup=1
    def BCC(self,Query,**Others):
        Param=[]
        self.GetBCCQueryInfo(Others,Query,Param)
        return self.CallBCC(Param[0],Param[1])

    #
    # Others:
    # IsWeb=False
    #  Structure=""/POS/Segment/Tree/Dependecy/Chunk
    # Table=""
    def Parse(self,text,**Others):
        Param=[]
        self.GetParseInfo(Others,Param)
        Structure=Param[0]
        IsWeb=Param[1]
        table=Param[2]
        if Structure == "Segment" and IsWeb == False:
            Ret=self.Segment(text,table)
            Words=Ret.split(" ")
            JS={}
            JS["Units"]=Words
            return json.dumps(JS,ensure_ascii=False)
        if Structure == "POS" and IsWeb == False:
            Ret=self.POS(text,table)
            Items=Ret.split(" ")
            JS={}
            JS["Units"]=[]
            JS["POS"]=[]
            for Item in Items:
                WordPOS=Item.split("/")
                if len(WordPOS) == 2:
                    JS["Units"].append(WordPOS[0])
                    JS["POS"].append(WordPOS[1])
            return json.dumps(JS,ensure_ascii=False)
        return self.CallService(text,Structure)

    def GetTable(self):
        self.GPFInit()                
        self.library_gpf.GPF_GetTable.argtypes = [c_void_p, c_char_p, c_int]
        self.library_gpf.GPF_GetTable.restype  = c_int
        str_len = self.library_gpf.GPF_GetTable(self.hHandleGPF, self.RetBuff, self.buf_max_size)
        if str_len != 0:
            ret = string_at(self.RetBuff, str_len)
            json_data = json.loads(ret.decode())
            return json_data
        return json.loads("{}")

    def GetBCCQueryInfo(self,Others,Query,Param):
        Command=""
        if Query.find("\n") != -1:
            BCCQuery=Query
        else:
            Command="Context"
        if Others.get("Command"):
            Command=Others["Command"]
        Number=1000  
        if Others.get("Number"):
            Number=Others["Number"]
        Target="$Q"
        if Others.get("Target"):
            Target=Others["Target"]
        WinSize=20
        if Others.get("WinSize"):
            WinSize=Others["WinSize"]
        Print=""
        if Others.get("Print"):
            Print=Others["Print"]
        Speedup=1
        if Others.get("Speedup"):
            Speedup=Others["Speedup"]
        if Command=="Context":
            if Query.find("{") != -1:
                BCCQuery="{}Context({},{},0)".format(Query,Number,WinSize)
            else:
                BCCQuery="{}{{}}Context({},{},0)".format(Query,Number,WinSize)
        if Command=="Freq":
            if Query.find("{") != -1:
                BCCQuery='{}Freq({},{},0)'.format(Query,Number,Target)
            else:
                BCCQuery='{}{{}}Freq({},{},0)'.format(Query,Number,Target)
            
        if Print=="Lua":
            BCCQuery+=Print
        if Speedup !=1:
            SpeedupCmd="Speedup({})".format(Speedup)
            BCCQuery+=SpeedupCmd
        Param.append(BCCQuery)

        Service=""
        if Others.get("Service"):
            Service=Others["Service"]
        Param.append(Service)

    def GetParseInfo(self,Others,Parm):
        IsWeb=False
        if Others.get("IsWeb"):
            IsWeb=Others["IsWeb"]
        table=""
        if Others.get("Table"):
            table=Others["Table"]
        Structure="Segment"        
        if Others.get("Structure"):
            Structure=Others["Structure"]
        Parm.append(Structure)
        Parm.append(IsWeb)
        Parm.append(table)

    def GPFInit(self):
        if self.IsGPFInit ==0:
            self.library_gpf.GPF_LatticeInit.argtypes = [c_void_p, c_char_p]
            self.library_gpf.GPF_LatticeInit.restype  = c_int
            self.IsGPFInit=self.library_gpf.GPF_DataInit(self.ConfigGPF.encode(), self.dataPath.encode());
        
