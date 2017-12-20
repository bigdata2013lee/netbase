#coding=utf-8
###########################################################################
#       
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################

__doc__ = """
接口组件配置获取
"""

from products.dataCollector.plugins.CollectorPlugin import SnmpPlugin,GetTableMap
def repeat(name,names):
    if name in names:
        return False
    else:
        names.append(name)
    return True
class InterfaceMap(SnmpPlugin):
    """
    接口
    """
    maptype = "interface"
    relname = "interfaces"
    modname = "products.netModel.ipInterface"
    deviceProperties = \
                SnmpPlugin.deviceProperties + ('zInterfaceMapIgnoreNames',
                                               'zInterfaceMapIgnoreTypes')

    baseSnmpGetTableMaps = (
        GetTableMap('iftable','.1.3.6.1.2.1.2.2.1',
                {'.1': 'snmpIndex',
                 '.2': 'uname',
                 '.3': 'type',
                 '.4': 'mtu',
                 '.5': 'speed',
                 '.6': 'macAddress',
                 '.7': 'adminStatus',
                 '.8': 'operStatus'}
        ),
        GetTableMap('ipAddrTable', '.1.3.6.1.2.1.4.20.1',
                {'.1': 'ipAddress',
                 '.2': 'snmpIndex',
                 '.3': 'netmask'}
        ),
        GetTableMap('ipNetToMediaTable', '.1.3.6.1.2.1.4.22.1',
                {'.1': 'snmpIndex',
                 '.3': 'ipAddress',
                 '.4': 'type'}
        ),
    )

    snmpGetTableMaps = baseSnmpGetTableMaps

    def process(self,device,results,log):
        """
        解析接口数据
        ＠device:设备对象
        """
        datamaps=[]
        getdata,tabledata = results
        log.debug("%s tabledata = %s" % (device.manageIp,tabledata))
        
        iptable = tabledata.get("ipAddrTable")
        if not iptable:
            iptable = tabledata.get("ipNetToMediaTable")
            if not iptable:
                errMsg="无法得到接口IP地址的数据!"
                log.error(errMsg)
                return errMsg,[]

        iftable = tabledata.get("iftable")
        if iftable is None:
            errMsg="无法获取数据,请检查SNMP配置是否正确!"
            log.error(errMsg)
            return errMsg,[]
        #ifalias = tabledata.get("ifalias", {})
        self.prepIfTable(datamaps, iftable,iptable)
        return "",datamaps

    def prepIfTable(self,datamaps,iftable,iptable):
        """
        解析iftable
        """
        names=[]
        omtable = {}
        for ip, row in iptable.items():
            if not row.has_key("snmpIndex"):
                continue
            if len(ip.split('.')) == 5:
                if row['type'] != 1:
                    continue
                ip = '.'.join(ip.split('.')[1:])
                row['netmask'] = '255.255.255.0'
            strindex = str(row['snmpIndex'])
            if not omtable.has_key(strindex) and not iftable.has_key(strindex):
                continue
            if row.has_key('ipAddress'):
                ip = row['ipAddress']
            if row.has_key('netmask'):
                ip = ip + "/" + str(self.maskToBits(row['netmask'].strip()))
            if not ip.endswith("/0"):
                if omtable.has_key(strindex):
                    omtable[strindex].append(ip)
                else:
                    omtable[strindex]=[ip]

        for ifkey,ifvalue in  iftable.iteritems():
            uname=ifvalue.get("uname","")
            if not repeat(uname,names):continue
            import chardet
            try:
                rs=chardet.detect(uname)
                if rs.get("encoding","utf-8")=="GB2312":
                    ifvalue["uname"]=uname.decode("gb2312")
            except:pass
            
            ifvalue["macAddress"]=self.asmac(ifvalue.get("macAddress",""))
            ifvalue["type"] = self.ifTypes.get(str(ifvalue.get('type', 1)), "Unknown")
            speed=ifvalue.get("speed",1000000000)
            if uname.startswith('bond') and speed == 1e7:
                ifvalue["speed"] = 1000000000
            ifvalue["ipAddress"]="".join(omtable.get(str(ifvalue["snmpIndex"]),[]))
            description=""
            ifvalue["description"]=description
            try:
                rs=chardet.detect(description)
                if rs.get("encoding","utf-8")=="GB2312":
                    ifvalue["description"]=description.decode("gb2312")
            except:
                pass
            ifvalue["uname"]=ifvalue.get("uname").replace("\x00","")
            datamaps.append(ifvalue)
        return datamaps
    
    ifTypes = {'1': 'Other',
     '2': 'regular1822',
     '3': 'hdh1822',
     '4': 'ddnX25',
     '5': 'rfc877x25',
     '6': 'ethernetCsmacd',
     '7': 'iso88023Csmacd',
     '8': 'iso88024TokenBus',
     '9': 'iso88025TokenRing',
     '10': 'iso88026Man',
     '11': 'starLan',
     '12': 'proteon10Mbit',
     '13': 'proteon80Mbit',
     '14': 'hyperchannel',
     '15': 'fddi',
     '16': 'lapb',
     '17': 'sdlc',
     '18': 'ds1',
     '19': 'e1',
     '20': 'basicISDN',
     '21': 'primaryISDN',
     '22': 'propPointToPointSerial',
     '23': 'ppp',
     '24': 'softwareLoopback',
     '25': 'eon',
     '26': 'ethernet-3Mbit',
     '27': 'nsip',
     '28': 'slip',
     '29': 'ultra',
     '30': 'ds3',
     '31': 'sip',
     '32': 'frame-relay',
     '33': 'rs232',
     '34': 'para',
     '35': 'arcnet',
     '36': 'arcnetPlus',
     '37': 'atm',
     '38': 'miox25',
     '39': 'sonet',
     '40': 'x25ple',
     '41': 'iso88022llc',
     '42': 'localTalk',
     '43': 'smdsDxi',
     '44': 'frameRelayService',
     '45': 'v35',
     '46': 'hssi',
     '47': 'hippi',
     '48': 'modem',
     '49': 'aal5',
     '50': 'sonetPath',
     '51': 'sonetVT',
     '52': 'smdsIcip',
     '53': 'propVirtual',
     '54': 'propMultiplexor',
     '55': '100BaseVG',
     '56': 'Fibre Channel',
     '57': 'HIPPI Interface',
     '58': 'Obsolete for FrameRelay',
     '59': 'ATM Emulation of 802.3 LAN',
     '60': 'ATM Emulation of 802.5 LAN',
     '61': 'ATM Emulation of a Circuit',
     '62': 'FastEthernet (100BaseT)',
     '63': 'ISDN',
     '64': 'CCITT V.11_X.21',
     '65': 'CCITT V.36',
     '66': 'CCITT G703 at 64Kbps',
     '67': 'Obsolete G702 see DS1-MIB',
     '68': 'SNA QLLC',
     '69': 'Full Duplex Fast Ethernet (100BaseFX)',
     '70': 'Channel',
     '71': 'Radio Spread Spectrum (802.11)',
     '72': 'IBM System 360_370 OEMI Channel',
     '73': 'IBM Enterprise Systems Connection',
     '74': 'Data Link Switching',
     '75': 'ISDN S_T Interface',
     '76': 'ISDN U Interface',
     '77': 'Link Access Protocol D (LAPD)',
     '78': 'IP Switching Opjects',
     '79': 'Remote Source Route Bridging',
     '80': 'ATM Logical Port',
     '81': 'ATT DS0 Point (64 Kbps)',
     '82': 'ATT Group of DS0 on a single DS1',
     '83': 'BiSync Protocol (BSC)',
     '84': 'Asynchronous Protocol',
     '85': 'Combat Net Radio',
     '86': 'ISO 802.5r DTR',
     '87': 'Ext Pos Loc Report Sys',
     '88': 'Apple Talk Remote Access Protocol',
     '89': 'Proprietary Connectionless Protocol',
     '90': 'CCITT-ITU X.29 PAD Protocol',
     '91': 'CCITT-ITU X.3 PAD Facility',
     '92': 'MultiProtocol Connection over Frame_Relay',
     '93': 'CCITT-ITU X213',
     '94': 'Asymetric Digitial Subscriber Loop (ADSL)',
     '95': 'Rate-Adapt Digital Subscriber Loop (RDSL)',
     '96': 'Symetric Digitial Subscriber Loop (SDSL)',
     '97': 'Very High Speed Digitial Subscriber Loop (HDSL)',
     '98': 'ISO 802.5 CRFP',
     '99': 'Myricom Myrinet',
     '100': 'Voice recEive and transMit (voiceEM)',
     '101': 'Voice Foreign eXchange Office (voiceFXO)',
     '102': 'Voice Foreign eXchange Station (voiceFXS)',
     '103': 'Voice Encapulation',
     '104': 'Voice Over IP Encapulation',
     '105': 'ATM DXI',
     '106': 'ATM FUNI',
     '107': 'ATM IMA',
     '108': 'PPP Multilink Bundle',
     '109': 'IBM IP over CDLC',
     '110': 'IBM Common Link Access to Workstation',
     '111': 'IBM Stack to Stack',
     '112': 'IBM Virtual IP Address (VIPA)',
     '113': 'IBM Multi-Protocol Channel Support',
     '114': 'IBM IP over ATM',
     '115': 'ISO 802.5j Fiber Token Ring',
     '116': 'IBM Twinaxial Data Link Control (TDLC)',
     '117': 'Gigabit Ethernet',
     '118': 'Higher Data Link Control (HDLC)',
     '119': 'Link Access Protocol F (LAPF)',
     '120': 'CCITT V.37',
     '121': 'CCITT X.25 Multi-Link Protocol',
     '122': 'CCITT X.25 Hunt Group',
     '123': 'Transp HDLC',
     '124': 'Interleave Channel',
     '125': 'Fast Channel',
     '126': 'IP (for APPN HPR in IP Networks)',
     '127': 'CATV MAC Layer',
     '128': 'CATV Downstream Interface',
     '129': 'CATV Upstream Interface',
     '130': 'Avalon Parallel Processor',
     '131': 'Encapsulation Interface',
     '132': 'Coffee Pot',
     '133': 'Circuit Emulation Service',
     '134': 'ATM Sub Interface',
     '135': 'Layer 2 Virtual LAN using 802.1Q',
     '136': 'Layer 3 Virtual LAN using IP',
     '137': 'Layer 3 Virtual LAN using IPX',
     '138': 'IP Over Power Lines',
     '139': 'Multi-Media Mail over IP',
     '140': 'Dynamic synchronous Transfer Mode (DTM)',
     '141': 'Data Communications Network',
     '142': 'IP Forwarding Interface',
     '143': 'Multi-rate Symmetric DSL',
     '144': 'IEEE1394 High Performance Serial Bus',
     '145': 'HIPPI-6400',
     '146': 'DVB-RCC MAC Layer',
     '147': 'DVB-RCC Downstream Channel',
     '148': 'DVB-RCC Upstream Channel',
     '149': 'ATM Virtual Interface',
     '150': 'MPLS Tunnel Virtual Interface',
     '151': 'Spatial Reuse Protocol',
     '152': 'Voice Over ATM',
     '153': 'Voice Over Frame Relay',
     '154': 'Digital Subscriber Loop over ISDN',
     '155': 'Avici Composite Link Interface',
     '156': 'SS7 Signaling Link',
     '157': 'Prop. P2P wireless interface',
     '158': 'Frame Forward Interface',
     '159': 'Multiprotocol over ATM AAL5',
     '160': 'USB Interface',
     '161': 'IEEE 802.3ad Link Aggregate',
     '162': 'BGP Policy Accounting',
     '163': 'FRF .16 Multilink Frame Relay',
     '164': 'H323 Gatekeeper',
     '165': 'H323 Voice and Video Proxy',
     '166': 'MPLS',
     '167': 'Multi-frequency signaling link',
     '168': 'High Bit-Rate DSL - 2nd generation',
     '169': 'Multirate HDSL2',
     '170': 'Facility Data Link 4Kbps on a DS1',
     '171': 'Packet over SONET_SDH Interface',
     '172': 'DVB-ASI Input',
     '173': 'DVB-ASI Output',
     '174': 'Power Line Communtications',
     '175': 'Non Facility Associated Signaling',
     '176': 'TR008',
     '177': 'Remote Digital Terminal',
     '178': 'Integrated Digital Terminal',
     '179': 'ISUP',
     '180': 'prop_Maclayer',
     '181': 'prop_Downstream',
     '182': 'prop_Upstream',
     '183': 'HIPERLAN Type 2 Radio Interface',
     '184': 'PropBroadbandWirelessAccesspt2multipt',
     '185': 'SONET Overhead Channel',
     '186': 'Digital Wrapper',
     '187': 'ATM adaptation layer 2',
     '188': 'MAC layer over radio links',
     '189': 'ATM over radio links',
     '190': 'Inter Machine Trunks',
     '191': 'Multiple Virtual Lines DSL',
     '192': 'Long Rach DSL',
     '193': 'Frame Relay DLCI End Point',
     '194': 'ATM VCI End Point',
     '195': 'Optical Channel',
     '196': 'Optical Transport',
     '197': 'Proprietary ATM',
     '198': 'Voice Over Cable Interface',
     '199': 'Infiniband',
     '200': 'TE Link',
     '201': 'Q.2931',
     '202': 'Virtual Trunk Group',
     '203': 'SIP Trunk Group',
     '204': 'SIP Signaling',
     '205': 'CATV Upstream Channel',
     '206': 'Acorn Econet',
     '207': 'FSAN 155Mb Symetrical PON interface',
     '208': 'FSAN622Mb Symetrical PON interface',
     '209': 'Transparent bridge interface',
     '210': 'Interface common to multiple lines',
     '211': 'voice E and M Feature Group D',
     '212': 'voice FGD Exchange Access North American',
     '213': 'voice Direct Inward Dialing',
     '214': 'MPEG transport interface',
     '215': '6to4 interface (DEPRECATED)',
     '216': 'GTP (GPRS Tunneling Protocol)',
     '217': 'Paradyne EtherLoop 1',
     '218': 'Paradyne EtherLoop 2',
     '219': 'Optical Channel Group',
     '220': 'HomePNA ITU-T G.989',
     '221': 'Generic Framing Procedure (GFP)',
     '222': 'Layer 2 Virtual LAN using Cisco ISL',
     '223': 'Acteleis proprietary MetaLOOP High Speed Link',
     '224': 'FCIP Link',
     '225': 'Resilient Packet Ring Interface Type',
     '226': 'RF Qam Interface',
     '227': 'Link Management Protocol',
     '228': 'Cambridge Broadband Limited VectaStar',
     '229': 'CATV Modular CMTS Downstream Interface',
     '230': 'Asymmetric Digital Subscriber Loop Version 2',
     '231': 'MACSecControlled',
     '232': 'MACSecUncontrolled', 
}
