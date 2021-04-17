from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms.models import model_to_dict

import pymongo

connectionToMongo = 'mongodb://127.0.0.1:27017/'


class amfForm(forms.Form):
    amf_servedGuamiLisCount = forms.CharField(widget=forms.HiddenInput())
    amf_supportTaiLisCount = forms.CharField(widget=forms.HiddenInput())
    amf_plmnSupportLisCount = forms.CharField(widget=forms.HiddenInput())


    def __init__(self, *args, **kwargs):
        super(amfForm, self).__init__(*args, **kwargs)
        myclient = pymongo.MongoClient(connectionToMongo)
        mydb = myclient['amf']
        mycol = mydb["config"]

        # --- Start of Initials --- #
        result = mycol.find_one({"_id":2}, {"amf.configuration":1, "_id":0})
        self.fields['amf_general_amfName'] = forms.CharField(required=False, label="amfName", help_text = "AMF node name", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['amf_general_amfName'].initial = result['amf']['configuration']['amfName']

        self.fields['amf_general_full'] = forms.CharField(required=False, label="Network fullName", help_text = "Network full name", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['amf_general_full'].initial = result['amf']['configuration']['networkName']['full']
        self.fields['amf_general_short'] = forms.CharField(required=False, label="Network shortName", help_text = "Network short name", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['amf_general_short'].initial = result['amf']['configuration']['networkName']['short']

        # --- End of Initials --- #

        # --- Start of serviceNameList --- #
        self.fields['amf_serviceNameList'] = forms.CharField(required=False, label="serviceNameList", help_text = "List of services", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['amf_serviceNameList'].initial = result['amf']['configuration']['serviceNameList']
        # --- End of serviceNameList --- #

        # --- Start of ngapIpList --- #
        self.fields['ngapIpList'] = forms.CharField(required=False, label="ngapIpList", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['ngapIpList'].initial = result['amf']['configuration']['ngapIpList']
        # --- End of ngapIpList --- #

        # --- Start of SBI --- #
        self.fields['sbi_scheme'] = forms.CharField(required=False, label="scheme", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_scheme'].initial = result['amf']['configuration']['sbi']['scheme']

        self.fields['sbi_registerIPv4'] = forms.CharField(required=False, label="registerIPv4", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_registerIPv4'].initial = result['amf']['configuration']['sbi']['registerIPv4']

        self.fields['sbi_bindingIPv4'] = forms.CharField(required=False, label="bindingIPv4", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_bindingIPv4'].initial = result['amf']['configuration']['sbi']['bindingIPv4']

        self.fields['sbi_port'] = forms.CharField(required=False, label="port", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_port'].initial = result['amf']['configuration']['sbi']['port']

        self.fields['nrfUri'] = forms.CharField(required=False, label="nrfUri", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['nrfUri'].initial = result['amf']['configuration']['nrfUri']
        # --- End of SBI --- #

        # --- Start of servedGuamiList --- #
        result = mycol.find_one({"_id":2}, {"amf.configuration.servedGuamiList":1, "_id":0})
        NumOfservedGuamiList = len(result['amf']['configuration']['servedGuamiList'])
        self.fields['amf_servedGuamiLisCount'].initial = NumOfservedGuamiList - 1
        self.fields['amf_servedGuamiLisCount'].widget.attrs['class'] = 'invisible'
        self.fields['amf_servedGuamiLisCount'].widget.attrs['default'] = NumOfservedGuamiList - 1
        
        for i in range(0, NumOfservedGuamiList):
            self.fields['amf_servedGuamiList_plmnId-{i}'.format(i=i)] = forms.CharField(required=False, label="plmnId", widget=forms.TextInput(attrs={'class': "", 'id': 'amf_servedGuamiListElement-{i}'.format(i=i)}))
            self.fields['amf_servedGuamiList_plmnId-{i}'.format(i=i)].initial = result['amf']['configuration']['servedGuamiList'][i]['plmnId']
            self.fields['amf_servedGuamiList_amfId-{i}'.format(i=i)] = forms.CharField(required=False, label="amfId", widget=forms.TextInput(attrs={'class': "", 'id': 'amf_servedGuamiListElement-{i}'.format(i=i)}))
            self.fields['amf_servedGuamiList_amfId-{i}'.format(i=i)].initial = result['amf']['configuration']['servedGuamiList'][i]['amfId']
        # --- Start of servedGuamiList --- #


        # --- Start of supportTaiList --- #
        result = mycol.find_one({"_id":2}, {"amf.configuration.supportTaiList":1, "_id":0})
        NumOfsupportTaiList = len(result['amf']['configuration']['supportTaiList'])
        self.fields['amf_supportTaiLisCount'].initial = NumOfsupportTaiList - 1
        self.fields['amf_supportTaiLisCount'].widget.attrs['class'] = 'invisible'
        self.fields['amf_supportTaiLisCount'].widget.attrs['default'] = NumOfsupportTaiList - 1
        
        for i in range(0, NumOfsupportTaiList):
            self.fields['amf_supportTaiList_plmnId-{i}'.format(i=i)] = forms.CharField(required=False, label="plmnId", widget=forms.TextInput(attrs={'class': "", 'id': 'amf_supportTaiListElement-{i}'.format(i=i)}))
            self.fields['amf_supportTaiList_plmnId-{i}'.format(i=i)].initial = result['amf']['configuration']['supportTaiList'][i]['plmnId']
            self.fields['amf_supportTaiList_tac-{i}'.format(i=i)] = forms.CharField(required=False, label="tac", widget=forms.TextInput(attrs={'class': "", 'id': 'amf_supportTaiListElement-{i}'.format(i=i)}))
            self.fields['amf_supportTaiList_tac-{i}'.format(i=i)].initial = result['amf']['configuration']['supportTaiList'][i]['tac']
        # --- Start of supportTaiList --- #


        # --- Start of plmnSupportList --- #
        result = mycol.find_one({"_id":2}, {"amf.configuration.plmnSupportList":1, "_id":0})
        NumOfplmnSupportList = len(result['amf']['configuration']['plmnSupportList'])
        self.fields['amf_plmnSupportLisCount'].initial = NumOfplmnSupportList - 1
        self.fields['amf_plmnSupportLisCount'].widget.attrs['class'] = 'invisible'
        self.fields['amf_plmnSupportLisCount'].widget.attrs['default'] = NumOfplmnSupportList - 1
        
        for i in range(0, NumOfplmnSupportList):
            self.fields['amf_plmnSupportList_plmnId-{i}'.format(i=i)] = forms.CharField(required=False, label="plmnId", widget=forms.TextInput(attrs={'class': "", 'id': 'amf_plmnSupportListElement-{i}'.format(i=i)}))
            self.fields['amf_plmnSupportList_plmnId-{i}'.format(i=i)].initial = result['amf']['configuration']['plmnSupportList'][i]['plmnId']
            self.fields['amf_plmnSupportList_snssaiList-{i}'.format(i=i)] = forms.CharField(required=False, label="snssaiList", widget=forms.TextInput(attrs={'class': "", 'id': 'amf_plmnSupportListElement-{i}'.format(i=i)}))
            self.fields['amf_plmnSupportList_snssaiList-{i}'.format(i=i)].initial = result['amf']['configuration']['plmnSupportList'][i]['snssaiList']
        # --- Start of plmnSupportList --- #


        # --- Start of supportDnnList --- #
        result = mycol.find_one({"_id":2}, {"amf.configuration.supportDnnList":1, "_id":0})
        self.fields['amf_supportDnnList'] = forms.CharField(required=False, label="supportDnnList", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['amf_supportDnnList'].initial = result['amf']['configuration']['supportDnnList']
        # --- End of supportDnnList --- #

        # --- Start of security --- #
        result = mycol.find_one({"_id":2}, {"amf.configuration.security":1, "_id":0})
        self.fields['amf_security_integrityOrder'] = forms.CharField(required=False, label="integrityOrder", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['amf_security_integrityOrder'].initial = result['amf']['configuration']['security']['integrityOrder']
        self.fields['amf_security_cipheringOrder'] = forms.CharField(required=False, label="cipheringOrder", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['amf_security_cipheringOrder'].initial = result['amf']['configuration']['security']['cipheringOrder']
        # --- End of security --- #
        


        # --- Start of timers --- #
        result = mycol.find_one({"_id":2}, {"amf.configuration":1, "_id":0})
        self.fields['amf_timers_t3502'] = forms.CharField(required=False, label="t3502", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['amf_timers_t3502'].initial = result['amf']['configuration']['t3502']
        self.fields['amf_timers_t3512'] = forms.CharField(required=False, label="t3512", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['amf_timers_t3512'].initial = result['amf']['configuration']['t3512']
        self.fields['amf_timers_non3gppDeregistrationTimer'] = forms.CharField(required=False, label="non3gppDeregTimer", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['amf_timers_non3gppDeregistrationTimer'].initial = result['amf']['configuration']['non3gppDeregistrationTimer']
        # --- End of timers --- #

    def Hidden(self):
        return [field for field in self if field.name in ('amf_servedGuamiLisCount', 'amf_supportTaiLisCount', 'amf_plmnSupportLisCount')]

    def General(self):
        return [field for field in self if 'amf_general' in field.name]

    def SBI(self):
        return [field for field in self if field.name in ('sbi_scheme', 'sbi_registerIPv4', 'sbi_bindingIPv4', 'sbi_port', 'nrfUri')]

    def Transport(self):
        return [field for field in self if field.name in ('ngapIpList')]

    def serviceNameList(self):
        return [field for field in self if field.name in ('amf_serviceNameList')]

    def servedGuamiList(self):
        return [field for field in self if 'amf_servedGuamiList' in field.name]

    def supportTaiList(self):
        return [field for field in self if 'amf_supportTaiList' in field.name]

    def plmnSupportList(self):
        return [field for field in self if 'amf_plmnSupportList' in field.name]

    def supportDnnList(self):
        return [field for field in self if 'amf_supportDnnList' in field.name]

    def Security(self):
        return [field for field in self if 'amf_security' in field.name]

    def Timers(self):
        return [field for field in self if 'amf_timers' in field.name]
        
# ------------------------------------------------------------------------------

class smfForm(forms.Form):
    smf_snssai_infCount = forms.CharField(widget=forms.HiddenInput())
    smf_userplane_information_up_nodeCount = forms.CharField(widget=forms.HiddenInput())
    smf_userplane_information_linkCount = forms.CharField(widget=forms.HiddenInput())
    smf_dnCount = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(smfForm, self).__init__(*args, **kwargs)
        myclient = pymongo.MongoClient(connectionToMongo)
        mydb = myclient['smf']
        mycol = mydb["config"]
    
        # --- Start of Initials --- #
        result = mycol.find_one({"_id":2}, {"smf.configuration":1, "_id":0})
        self.fields['smfName'] = forms.CharField(required=False, label="smfName", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['smfName'].initial = result['smf']['configuration']['smfName']
        # --- End of Initials --- #

        # --- Start of SBI --- #
        self.fields['sbi_scheme'] = forms.CharField(required=False, label="scheme", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_scheme'].initial = result['smf']['configuration']['sbi']['scheme']

        self.fields['sbi_registerIPv4'] = forms.CharField(required=False, label="registerIPv4", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_registerIPv4'].initial = result['smf']['configuration']['sbi']['registerIPv4']

        self.fields['sbi_bindingIPv4'] = forms.CharField(required=False, label="bindingIPv4", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_bindingIPv4'].initial = result['smf']['configuration']['sbi']['bindingIPv4']

        self.fields['sbi_port'] = forms.CharField(required=False, label="port", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_port'].initial = result['smf']['configuration']['sbi']['port']

        self.fields['nrfUri'] = forms.CharField(required=False, label="nrfUri", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['nrfUri'].initial = result['smf']['configuration']['nrfUri']
        # --- End of SBI --- #


        # --- Start of serviceNameList --- #
        self.fields['smf_serviceNameList'] = forms.CharField(required=False, label="serviceNameList", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['smf_serviceNameList'].initial = result['smf']['configuration']['serviceNameList']
        # --- End of serviceNameList --- #

        # --- Start of snssai_info --- #
        result = mycol.find_one({"_id":2}, {"smf.configuration.snssai_info":1, "_id":0})
        NumOfsnssai_info = len(result['smf']['configuration']['snssai_info'])
        self.fields['smf_snssai_infCount'].initial = NumOfsnssai_info - 1
        self.fields['smf_snssai_infCount'].widget.attrs['class'] = 'invisible'
        self.fields['smf_snssai_infCount'].widget.attrs['default'] = NumOfsnssai_info - 1

        for i in range(0, NumOfsnssai_info):
            self.fields['smf_snssai_info_sNssai-{i}'.format(i=i)] = forms.CharField(required=False, label="sNssai", widget=forms.TextInput(attrs={'class': "pt-4", 'id': 'smf_snssai_infoElement-{ix}'.format(ix=i)}))
            self.fields['smf_snssai_info_sNssai-{i}'.format(i=i)].initial = result['smf']['configuration']['snssai_info'][i]['sNssai']
            self.fields['smf_snssai_info_dnnSmfInfoList-{i}'.format(i=i)] = forms.CharField(required=False, label="dnnSmfInfoList", widget=forms.TextInput(attrs={'class': "", 'id': 'smf_snssai_infoElement-{ix}'.format(ix=i)}))
            self.fields['smf_snssai_info_dnnSmfInfoList-{i}'.format(i=i)].initial = result['smf']['configuration']['snssai_info'][i]['dnnSmfInfoList']
        # --- End of snssai_info --- #

        # --- Start of pfcp --- #
        result = mycol.find_one({"_id":2}, {"smf.configuration":1, "_id":0})
        self.fields['smf_pfcp'] = forms.CharField(required=False, label="pfcp", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['smf_pfcp'].initial = result['smf']['configuration']['pfcp']

        result = mycol.find_one({"_id":2}, {"smf.configuration":1, "_id":0})
        self.fields['smf_ue_subnet'] = forms.CharField(required=False, label="ue_subnet", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['smf_ue_subnet'].initial = result['smf']['configuration']['ue_subnet']
        # --- End of pfcp --- #


        # --- Start of userplane_information --- #
        result = mycol.find_one({"_id":2}, {"smf.configuration":1, "_id":0})

        NumOfuserplane_information_up_nodes = len(result['smf']['configuration']['userplane_information']['up_nodes'])
        self.fields['smf_userplane_information_up_nodeCount'].initial = NumOfuserplane_information_up_nodes - 1
        self.fields['smf_userplane_information_up_nodeCount'].widget.attrs['class'] = 'invisible'
        self.fields['smf_userplane_information_up_nodeCount'].widget.attrs['default'] = NumOfuserplane_information_up_nodes - 1

        data = result['smf']['configuration']['userplane_information']['up_nodes']
        keys = list(data.keys())

        for i in range(0, NumOfuserplane_information_up_nodes):
            self.fields['smf_userplane_information_up_nodes_name-{ix}'.format(ix=i)] = forms.CharField(required=False, label="nodeName", widget=forms.TextInput(attrs={'class': "pt-4", 'id': 'smf_userplane_information_up_nodesElement-{ix}'.format(ix=i)}))
            self.fields['smf_userplane_information_up_nodes_name-{ix}'.format(ix=i)].initial = keys[i]
            self.fields['smf_userplane_information_up_nodes_node-{ix}'.format(ix=i)] = forms.CharField(required=False, label="nodeData", widget=forms.TextInput(attrs={'class': "", 'id': 'smf_userplane_information_up_nodesElement-{ix}'.format(ix=i)}))
            self.fields['smf_userplane_information_up_nodes_node-{ix}'.format(ix=i)].initial = data[keys[i]]

        NumOfuserplane_information_links = len(result['smf']['configuration']['userplane_information']['links'])
        self.fields['smf_userplane_information_linkCount'].initial = NumOfuserplane_information_links -1
        self.fields['smf_userplane_information_linkCount'].widget.attrs['class'] = 'invisible'
        self.fields['smf_userplane_information_linkCount'].widget.attrs['default'] = NumOfuserplane_information_links - 1

        for i in range(0, NumOfuserplane_information_links):
            self.fields['smf_userplane_information_links-{ix}'.format(ix=i)] = forms.CharField(required=False, label="links", widget=forms.TextInput(attrs={'class': "pt-4", 'id': 'smf_userplane_information_linksElement-{ix}'.format(ix=i)}))
            self.fields['smf_userplane_information_links-{ix}'.format(ix=i)].initial = result['smf']['configuration']['userplane_information']['links'][i]
        # --- End of userplane_information --- #
    

        # --- Start of dnn --- #
        result = mycol.find_one({"_id":2}, {"smf.configuration":1, "_id":0})
        NumOfdnn = len(result['smf']['configuration']['dnn'])
        self.fields['smf_dnCount'].initial = NumOfdnn - 1
        self.fields['smf_dnCount'].widget.attrs['class'] = 'invisible'
        self.fields['smf_dnCount'].widget.attrs['default'] = NumOfdnn - 1

        data = result['smf']['configuration']['dnn']
        keys = list(data.keys())

        for i in range(0, NumOfdnn):
            self.fields['smf_dnn_name-{ix}'.format(ix=i)] = forms.CharField(required=False, label="dnnName", widget=forms.TextInput(attrs={'class': "pt-4", 'id': 'smf_dnnElement-{ix}'.format(ix=i)}))
            self.fields['smf_dnn_name-{ix}'.format(ix=i)].initial = keys[i]
            self.fields['smf_dnn_ipv4-{ix}'.format(ix=i)] = forms.CharField(required=False, label="dns ipv4", widget=forms.TextInput(attrs={'class': "", 'id': 'smf_dnnElement-{ix}'.format(ix=i)}))
            self.fields['smf_dnn_ipv4-{ix}'.format(ix=i)].initial = data[keys[i]]['dns']['ipv4']
            self.fields['smf_dnn_ipv6-{ix}'.format(ix=i)] = forms.CharField(required=False, label="dns ipv6", widget=forms.TextInput(attrs={'class': "", 'id': 'smf_dnnElement-{ix}'.format(ix=i)}))
            self.fields['smf_dnn_ipv6-{ix}'.format(ix=i)].initial = data[keys[i]]['dns']['ipv6']
        # --- End of dnn --- #



    def Hidden(self):
        return [field for field in self if field.name in ('smf_snssai_infCount', 'smf_userplane_information_up_nodeCount', 'smf_userplane_information_linkCount', 'smf_dnCount')]

    def General(self):
        return [field for field in self if field.name in ('smfName')]

    def SBI(self):
        return [field for field in self if field.name in ('sbi_scheme', 'sbi_registerIPv4', 'sbi_bindingIPv4', 'sbi_port','sbi_tls_key','sbi_tls_pem','nrfUri','serviceNameList')]

    def serviceNameList(self):
        return [field for field in self if field.name in ('smf_serviceNameList')]

    def Pfcp(self):
        return [field for field in self if field.name in ('smf_pfcp')]
    
    def Slicing(self):
        return [field for field in self if 'smf_snssai_info' in field.name]

    # UserPlane_up_nodes are in same UserPlane_links tab
    def UserPlane_up_nodes(self):
        return [field for field in self if 'smf_userplane_information_up_nodes' in field.name]

    def UserPlane_links(self):
        return [field for field in self if 'smf_userplane_information_links' in field.name]
    # UserPlane_up_nodes are in same UserPlane_links tab

    def DNN(self):
        return [field for field in self if 'smf_dnn' in field.name]

    def UeSubnet(self):
        return [field for field in self if 'smf_ue_subnet' in field.name]

# ------------------------------------------------------------------------------

class ausfForm(forms.Form):
    ausf_NumOfplmnSupportLisCount = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(ausfForm, self).__init__(*args, **kwargs)
        myclient = pymongo.MongoClient(connectionToMongo)
        mydb = myclient['ausf']
        mycol = mydb["config"]

        # --- Start of Initials --- #
        result = mycol.find_one({"_id":2}, {"ausf.configuration":1, "_id":0})
        self.fields['ausfName'] = forms.CharField(required=False, label="ausfName", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['ausfName'].initial = "AUSF"

        self.fields['groupId'] = forms.CharField(required=False, label="groupId", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['groupId'].initial = result['ausf']['configuration']['groupId']
        # --- End of Initials --- #


        # --- Start of SBI --- #
        self.fields['sbi_scheme'] = forms.CharField(required=False, label="scheme", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_scheme'].initial = result['ausf']['configuration']['sbi']['scheme']

        self.fields['sbi_registerIPv4'] = forms.CharField(required=False, label="registerIPv4", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_registerIPv4'].initial = result['ausf']['configuration']['sbi']['registerIPv4']

        self.fields['sbi_bindingIPv4'] = forms.CharField(required=False, label="bindingIPv4", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_bindingIPv4'].initial = result['ausf']['configuration']['sbi']['bindingIPv4']

        self.fields['sbi_port'] = forms.CharField(required=False, label="port", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_port'].initial = result['ausf']['configuration']['sbi']['port']

        self.fields['nrfUri'] = forms.CharField(required=False, label="nrfUri", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['nrfUri'].initial = result['ausf']['configuration']['nrfUri']
        # --- End of SBI --- #


        # --- Start of serviceNameList --- #
        self.fields['serviceNameList'] = forms.CharField(required=False, label="serviceNameList", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['serviceNameList'].initial = result['ausf']['configuration']['serviceNameList']
        # --- End of serviceNameList --- #


        # --- Start of plmnSupportList --- #
        NumOfplmnSupportList = len(result['ausf']['configuration']['plmnSupportList'])
        self.fields['ausf_NumOfplmnSupportLisCount'].initial = NumOfplmnSupportList - 1
        self.fields['ausf_NumOfplmnSupportLisCount'].widget.attrs['class'] = 'invisible'
        self.fields['ausf_NumOfplmnSupportLisCount'].widget.attrs['default'] = NumOfplmnSupportList - 1

        for i in range(0, NumOfplmnSupportList):
            self.fields['ausf_plmnSupportList-{ix}'.format(ix=i)] = forms.CharField(required=False, label="plmnSupportList", widget=forms.TextInput(attrs={'class': "", 'id': 'ausf_plmnSupportListElement-{ix}'.format(ix=i)}))
            self.fields['ausf_plmnSupportList-{ix}'.format(ix=i)].initial = result['ausf']['configuration']['plmnSupportList'][i]
        # --- End of plmnSupportList --- #


    def Hidden(self):
       return [field for field in self if field.name in ('ausf_NumOfplmnSupportLisCount')]

    def General(self):
       return [field for field in self if field.name in ('ausfName', 'groupId')]

    def SBI(self):
        return [field for field in self if field.name in ('sbi_scheme', 'sbi_registerIPv4', 'sbi_bindingIPv4', 'sbi_port','nrfUri')]

    def serviceName(self):
        return [field for field in self if field.name in ('serviceNameList')]

    def plmnSupport(self):
        return [field for field in self if 'ausf_plmnSupportList' in field.name]

# ------------------------------------------------------------------------------

class nrfForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(nrfForm, self).__init__(*args, **kwargs)
        myclient = pymongo.MongoClient(connectionToMongo)
        mydb = myclient['nrf']
        mycol = mydb["config"]

        # --- Start of Initials --- #
        result = mycol.find_one({"_id":2}, {"nrf.configuration":1, "_id":0})
        self.fields['nrfName'] = forms.CharField(required=False, label="nrfName", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['nrfName'].initial = "NRF"

        self.fields['DefaultServiceIP'] = forms.CharField(required=False, label="DefaultServiceIP", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['DefaultServiceIP'].initial = result['nrf']['configuration']['DefaultServiceIP']
        # --- End of Initials --- #

        # --- Start of SBI --- #
        self.fields['sbi_scheme'] = forms.CharField(required=False, label="scheme", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_scheme'].initial = result['nrf']['configuration']['sbi']['scheme']

        self.fields['sbi_ipv4Addr'] = forms.CharField(required=False, label="ipv4Addr", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_ipv4Addr'].initial = result['nrf']['configuration']['sbi']['ipv4Addr']

        self.fields['sbi_port'] = forms.CharField(required=False, label="port", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_port'].initial = result['nrf']['configuration']['sbi']['port']
        # --- End of SBI --- #

        # --- Start of DB --- #
        self.fields['MongoDBName'] = forms.CharField(required=False, label="MongoDBName", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['MongoDBName'].initial = result['nrf']['configuration']['MongoDBName']

        self.fields['MongoDBUrl'] = forms.CharField(required=False, label="MongoDBUrl", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['MongoDBUrl'].initial = result['nrf']['configuration']['MongoDBUrl']

        self.fields['sbi_port'] = forms.CharField(required=False, label="port", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_port'].initial = result['nrf']['configuration']['sbi']['port']
        # --- End of DB --- #

        # --- Start of DB --- #
        self.fields['DefaultPlmnId'] = forms.CharField(required=False, label="DefaultPlmnId", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['DefaultPlmnId'].initial = result['nrf']['configuration']['DefaultPlmnId']

        self.fields['serviceNameList'] = forms.CharField(required=False, label="serviceNameList", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['serviceNameList'].initial = result['nrf']['configuration']['serviceNameList']

        # --- End of DB --- #




    def General(self):
           return [field for field in self if field.name in ('nrfName')]

    def SBI(self):
        return [field for field in self if field.name in ('sbi_scheme', 'sbi_ipv4Addr','sbi_port', 'DefaultServiceIP')]

    def DBConfig(self):
        return [field for field in self if field.name in ('MongoDBName', 'MongoDBUrl')]

    def fiveGNetwork(self):
        return [field for field in self if field.name in ('serviceNameList', 'DefaultPlmnId')]

# ------------------------------------------------------------------------------

class udmForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(udmForm, self).__init__(*args, **kwargs)
        myclient = pymongo.MongoClient(connectionToMongo)
        mydb = myclient['udm']
        mycol = mydb["config"]

    
        # --- Start of Initials --- #
        result = mycol.find_one({"_id":2}, {"udm.configuration":1, "_id":0})
        self.fields['udmName'] = forms.CharField(required=False, label="udmName", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['udmName'].initial = "UDM"
        # --- End of Initials --- #


        # --- Start of SBI --- #
        self.fields['sbi_scheme'] = forms.CharField(required=False, label="scheme", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_scheme'].initial = result['udm']['configuration']['sbi']['scheme']

        self.fields['sbi_registerIPv4'] = forms.CharField(required=False, label="registerIPv4", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_registerIPv4'].initial = result['udm']['configuration']['sbi']['registerIPv4']

        self.fields['sbi_bindingIPv4'] = forms.CharField(required=False, label="bindingIPv4", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_bindingIPv4'].initial = result['udm']['configuration']['sbi']['bindingIPv4']

        self.fields['sbi_port'] = forms.CharField(required=False, label="port", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_port'].initial = result['udm']['configuration']['sbi']['port']

        self.fields['nrfUri'] = forms.CharField(required=False, label="nrfUri", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['nrfUri'].initial = result['udm']['configuration']['nrfUri']
        # --- End of SBI --- #
    

        # --- Start of udrclient --- #
        self.fields['udrclient_scheme'] = forms.CharField(required=False, label="scheme", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['udrclient_scheme'].initial = result['udm']['configuration']['udrclient']['scheme']

        self.fields['udrclient_ipv4Addr'] = forms.CharField(required=False, label="ipv4Addr", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['udrclient_ipv4Addr'].initial = result['udm']['configuration']['udrclient']['ipv4Addr']

        self.fields['udrclient_port'] = forms.CharField(required=False, label="port", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['udrclient_port'].initial = result['udm']['configuration']['udrclient']['port']
        # --- End of udrclient --- #

        # --- Start of udrclient --- #
        self.fields['nrfclient_scheme'] = forms.CharField(required=False, label="scheme", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['nrfclient_scheme'].initial = result['udm']['configuration']['nrfclient']['scheme']

        self.fields['nrfclient_ipv4Addr'] = forms.CharField(required=False, label="ipv4Addr", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['nrfclient_ipv4Addr'].initial = result['udm']['configuration']['nrfclient']['ipv4Addr']

        self.fields['nrfclient_port'] = forms.CharField(required=False, label="port", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['nrfclient_port'].initial = result['udm']['configuration']['nrfclient']['port']
        # --- End of udrclient --- #


        # --- Start of serviceNameList --- #
        self.fields['serviceNameList'] = forms.CharField(required=False, label="serviceNameList", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['serviceNameList'].initial = result['udm']['configuration']['serviceNameList']
        # --- End of serviceNameList --- #

    



    def General(self):
        return [field for field in self if field.name in ('udmName')]

    def SBI(self):
        return [field for field in self if field.name in ('sbi_scheme', 'sbi_registerIPv4', 'sbi_bindingIPv4', 'sbi_port', 'nrfUri')]

    def TowardUDR(self):
        return [field for field in self if field.name in ('udrclient_scheme', 'udrclient_ipv4Addr', 'udrclient_port')]

    def TowardNRF(self):
        return [field for field in self if field.name in ('nrfclient_scheme', 'nrfclient_ipv4Addr','nrfclient_port')]

    def fiveGNetwork(self):
        return [field for field in self if field.name in ('serviceNameList')]

# ------------------------------------------------------------------------------

class udrForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(udrForm, self).__init__(*args, **kwargs)
        myclient = pymongo.MongoClient(connectionToMongo)
        mydb = myclient['udr']
        mycol = mydb["config"]

        # --- Start of Initials --- #
        result = mycol.find_one({"_id":2}, {"udr.configuration":1, "_id":0})
        self.fields['udrName'] = forms.CharField(required=False, label="udrName", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['udrName'].initial = "UDR"
        # --- End of Initials --- #

        # --- Start of SBI --- #
        self.fields['sbi_scheme'] = forms.CharField(required=False, label="scheme", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_scheme'].initial = result['udr']['configuration']['sbi']['scheme']

        self.fields['sbi_registerIPv4'] = forms.CharField(required=False, label="registerIPv4", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_registerIPv4'].initial = result['udr']['configuration']['sbi']['registerIPv4']

        self.fields['sbi_bindingIPv4'] = forms.CharField(required=False, label="bindingIPv4", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_bindingIPv4'].initial = result['udr']['configuration']['sbi']['bindingIPv4']

        self.fields['sbi_port'] = forms.CharField(required=False, label="port", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_port'].initial = result['udr']['configuration']['sbi']['port']

        self.fields['nrfUri'] = forms.CharField(required=False, label="nrfUri", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['nrfUri'].initial = result['udr']['configuration']['nrfUri']
        # --- End of SBI --- #        

        # --- Start of mongodb ---#
        self.fields['mongodb_name'] = forms.CharField(required=False, label="DB Name", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['mongodb_name'].initial = result['udr']['configuration']['mongodb']['name']

        self.fields['mongodb_url'] = forms.CharField(required=False, label="DB url", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['mongodb_url'].initial = result['udr']['configuration']['mongodb']['url']
        # --- End of mongodb ---#

        # --- Start of SmPolicySnssaiData ---#
        result = mycol.find_one({"_id":2}, {"udr.extraConfig":1, "_id":0})
        self.fields['SmPolicySnssaiData_Snssai'] = forms.CharField(required=False, label="sNssai", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['SmPolicySnssaiData_Snssai'].initial = result['udr']['extraConfig']['sNssai']
        # --- End of SmPolicySnssaiData ---#


    def General(self):
        return [field for field in self if field.name in ('udrName')]

    def SBI(self):
        return [field for field in self if field.name in ('sbi_scheme', 'sbi_registerIPv4', 'sbi_bindingIPv4', 'sbi_port', 'nrfUri')]

    def Database(self):
        return [field for field in self if field.name in ('mongodb_name', 'mongodb_url')]

    def SmPolicySnssaiData(self):
        return [field for field in self if field.name in ('SmPolicySnssaiData_Snssai')]
# ------------------------------------------------------------------------------

class pcfForm(forms.Form):
    pcf_serviceLisCount = forms.CharField(widget=forms.HiddenInput())
        
    def __init__(self, *args, **kwargs):
        super(pcfForm, self).__init__(*args, **kwargs)
        myclient = pymongo.MongoClient(connectionToMongo)
        mydb = myclient['pcf']
        mycol = mydb["config"]        

        # --- Start of Initials --- #
        result = mycol.find_one({"_id":2}, {"pcf.configuration":1, "_id":0})
        self.fields['pcfName'] = forms.CharField(required=False, label="pcfName", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['pcfName'].initial = result['pcf']['configuration']['pcfName']
        self.fields['timeFormat'] = forms.CharField(required=False, label="timeFormat", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['timeFormat'].initial = result['pcf']['configuration']['timeFormat']
        self.fields['defaultBdtRefId'] = forms.CharField(required=False, label="defaultBdtRefId", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['defaultBdtRefId'].initial = result['pcf']['configuration']['defaultBdtRefId']

        # --- End of Initials --- #

        # --- Start of SBI --- #
        self.fields['sbi_scheme'] = forms.CharField(required=False, label="scheme", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_scheme'].initial = result['pcf']['configuration']['sbi']['scheme']

        self.fields['sbi_registerIPv4'] = forms.CharField(required=False, label="registerIPv4", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_registerIPv4'].initial = result['pcf']['configuration']['sbi']['registerIPv4']

        self.fields['sbi_bindingIPv4'] = forms.CharField(required=False, label="bindingIPv4", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_bindingIPv4'].initial = result['pcf']['configuration']['sbi']['bindingIPv4']

        self.fields['sbi_port'] = forms.CharField(required=False, label="port", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_port'].initial = result['pcf']['configuration']['sbi']['port']

        self.fields['nrfUri'] = forms.CharField(required=False, label="nrfUri", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['nrfUri'].initial = result['pcf']['configuration']['nrfUri']
        # --- End of SBI --- #


        # --- Start of serviceList --- #
        NumOfserviceList = len(result['pcf']['configuration']['serviceList'])
        self.fields['pcf_serviceLisCount'].initial = NumOfserviceList - 1
        self.fields['pcf_serviceLisCount'].widget.attrs['class'] = 'invisible'
        self.fields['pcf_serviceLisCount'].widget.attrs['default'] = NumOfserviceList - 1

        

        for i in range(0, NumOfserviceList):
            serviceList = result['pcf']['configuration']['serviceList'][i]

            self.fields['pcf_serviceList_serviceName-{ix}'.format(ix=i)] = forms.CharField(required=False, label="serviceName", widget=forms.TextInput(attrs={'class': "mt-4", 'id': 'pcfserviceListElement-{ix}'.format(ix=i)}))
            self.fields['pcf_serviceList_serviceName-{ix}'.format(ix=i)].initial = serviceList['serviceName']
            self.fields['pcf_serviceList_suppFeat-{ix}'.format(ix=i)] = forms.CharField(required=False, label="plmnSupportList", widget=forms.TextInput(attrs={'class': "", 'id': 'pcfserviceListElement-{ix}'.format(ix=i)}))
            self.fields['pcf_serviceList_suppFeat-{ix}'.format(ix=i)].initial = serviceList.get('suppFeat', 'None')
        # --- End of serviceList --- #        

    def Hidden(self):
        return [field for field in self if field.name in ('pcf_serviceLisCount')]

    def General(self):
        return [field for field in self if field.name in ('pcfName', 'timeFormat','defaultBdtRefId')]

    def SBI(self):
        return [field for field in self if field.name in ('sbi_scheme', 'sbi_registerIPv4', 'sbi_bindingIPv4', 'sbi_port', 'nrfUri')]

    def fiveGNetwork(self):
        return [field for field in self if 'pcf_serviceList' in field.name]


# ------------------------------------------------------------------------------

class upfForm(forms.Form):
    upf_NumOfpfcpCount = forms.CharField(widget=forms.HiddenInput())
    upf_NumOfgtpuCount = forms.CharField(widget=forms.HiddenInput())
    upf_dnn_lisCount = forms.CharField(widget=forms.HiddenInput())
        
    def __init__(self, *args, **kwargs):
        super(upfForm, self).__init__(*args, **kwargs)
        myclient = pymongo.MongoClient(connectionToMongo)
        mydb = myclient['upf']
        mycol = mydb["config"]

        # --- Start of Initials --- #
        result = mycol.find_one({"_id":2}, {"upf.configuration":1, "_id":0})
        self.fields['upfName'] = forms.CharField(required=False, label="upfName", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['upfName'].initial = "UPF"

        self.fields['debugLevel'] = forms.CharField(required=False, label="debugLevel", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['debugLevel'].initial = result['upf']['configuration']['debugLevel']

        self.fields['ReportCaller'] = forms.CharField(required=False, label="ReportCaller", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['ReportCaller'].initial = result['upf']['configuration']['ReportCaller']
        # --- End of Initials --- #


        # --- Start of pfcp --- #
        NumOfpfcp = len(result['upf']['configuration']['pfcp'])
        self.fields['upf_NumOfpfcpCount'].initial = NumOfpfcp - 1
        self.fields['upf_NumOfpfcpCount'].widget.attrs['class'] = 'invisible'
        self.fields['upf_NumOfpfcpCount'].widget.attrs['default'] = NumOfpfcp - 1

        for i in range(0, NumOfpfcp):
            self.fields['upf_pfcp-{ix}'.format(ix=i)] = forms.CharField(required=False, label="pfcp", widget=forms.TextInput(attrs={'class': "", 'id': 'upf_pfcpElement-{ix}'.format(ix=i)}))
            self.fields['upf_pfcp-{ix}'.format(ix=i)].initial = result['upf']['configuration']['pfcp'][i]
        # --- End of pfcp --- #    


        # --- Start of gtpu --- #
        NumOfgtpu = len(result['upf']['configuration']['gtpu'])
        self.fields['upf_NumOfgtpuCount'].initial = NumOfgtpu - 1
        self.fields['upf_NumOfgtpuCount'].widget.attrs['class'] = 'invisible'
        self.fields['upf_NumOfgtpuCount'].widget.attrs['default'] = NumOfgtpu - 1

        for i in range(0, NumOfgtpu):
            self.fields['upf_gtpu-{ix}'.format(ix=i)] = forms.CharField(required=False, label="gtpu", widget=forms.TextInput(attrs={'class': "", 'id': 'upf_gtpuElement-{ix}'.format(ix=i)}))
            self.fields['upf_gtpu-{ix}'.format(ix=i)].initial = result['upf']['configuration']['gtpu'][i]
        # --- End of gtpu --- #    



        # --- Start of dnn_list --- #
        NumOfdnn_list = len(result['upf']['configuration']['dnn_list'])
        self.fields['upf_dnn_lisCount'].initial = NumOfdnn_list - 1
        self.fields['upf_dnn_lisCount'].widget.attrs['class'] = 'invisible'
        self.fields['upf_dnn_lisCount'].widget.attrs['default'] = NumOfdnn_list - 1

        for i in range(0, NumOfdnn_list):
            self.fields['upf_dnn_list-{ix}'.format(ix=i)] = forms.CharField(required=False, label="DNN List", widget=forms.TextInput(attrs={'class': "", 'id': 'upf_dnn_listElement-{ix}'.format(ix=i)}))
            self.fields['upf_dnn_list-{ix}'.format(ix=i)].initial = result['upf']['configuration']['dnn_list'][i]
        # --- End of dnn_list --- #    

    def Hidden(self):
        return [field for field in self if field.name in ('upf_NumOfpfcpCount', 'upf_NumOfgtpuCount', 'upf_dnn_lisCount')]

    def General(self):
        return [field for field in self if field.name in ('upfName', 'debugLevel', 'ReportCaller')]

    def Pfcp(self):
        return [field for field in self if 'upf_pfcp' in field.name]

    def Gtpu(self):
        return [field for field in self if 'upf_gtpu' in field.name]
    
    def DnnList(self):
        return [field for field in self if 'upf_dnn_list' in field.name]

# ------------------------------------------------------------------------------

class nssfForm(forms.Form):
    nssf_supportedNssaiInPlmnLisCount = forms.CharField(widget=forms.HiddenInput())
    nssf_nsiLisCount = forms.CharField(widget=forms.HiddenInput())
    nssf_taLisCount = forms.CharField(widget=forms.HiddenInput())
    nssf_amfSetLisCount = forms.CharField(widget=forms.HiddenInput())
    nssf_amfLisCount = forms.CharField(widget=forms.HiddenInput())
    nssf_mappingLisFromPlmnCount = forms.CharField(widget=forms.HiddenInput())
    

    def __init__(self, *args, **kwargs):
        super(nssfForm, self).__init__(*args, **kwargs)
        myclient = pymongo.MongoClient(connectionToMongo)
        mydb = myclient['nssf']
        mycol = mydb["config"]
        

        # --- Start of Initials --- #
        result = mycol.find_one({"_id":2}, {"nssf.configuration":1, "_id":0})
        self.fields['nssfName'] = forms.CharField(required=False, label="nssfName", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['nssfName'].initial = result['nssf']['configuration']['nssfName']

        self.fields['serviceNameList'] = forms.CharField(required=False, label="serviceNameList", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['serviceNameList'].initial = result['nssf']['configuration']['serviceNameList']

        self.fields['supportedPlmnList'] = forms.CharField(required=False, label="supportedPlmnList", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['supportedPlmnList'].initial = result['nssf']['configuration']['supportedPlmnList']

        self.fields['sbi_scheme'] = forms.CharField(required=False, label="scheme", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_scheme'].initial = result['nssf']['configuration']['sbi']['scheme']

        self.fields['sbi_registerIPv4'] = forms.CharField(required=False, label="registerIPv4", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_registerIPv4'].initial = result['nssf']['configuration']['sbi']['registerIPv4']

        self.fields['sbi_bindingIPv4'] = forms.CharField(required=False, label="bindingIPv4", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_bindingIPv4'].initial = result['nssf']['configuration']['sbi']['bindingIPv4']

        self.fields['sbi_port'] = forms.CharField(required=False, label="port", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['sbi_port'].initial = result['nssf']['configuration']['sbi']['port']

        self.fields['nrfUri'] = forms.CharField(required=False, label="nrfUri", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['nrfUri'].initial = result['nssf']['configuration']['nrfUri']

        # --- End of Initials --- #




        # --- Start of supportedNssaiInPlmnList --- #
        NumOfsupportedNssaiInPlmnList = len(result['nssf']['configuration']['supportedNssaiInPlmnList'])
        self.fields['nssf_supportedNssaiInPlmnLisCount'].initial = NumOfsupportedNssaiInPlmnList - 1
        self.fields['nssf_supportedNssaiInPlmnLisCount'].widget.attrs['class'] = 'invisible'
        self.fields['nssf_supportedNssaiInPlmnLisCount'].widget.attrs['default'] = NumOfsupportedNssaiInPlmnList - 1

        for i in range(0, NumOfsupportedNssaiInPlmnList):
            self.fields['nssf_supportedNssaiInPlmnList_plmnId-{i}'.format(i=i)] = forms.CharField(required=False, label="plmnId", widget=forms.TextInput(attrs={'class': ""}))
            self.fields['nssf_supportedNssaiInPlmnList_plmnId-{i}'.format(i=i)].initial = result['nssf']['configuration']['supportedNssaiInPlmnList'][i]['plmnId']
            self.fields['nssf_supportedNssaiInPlmnList_supportedSnssaiList-{i}'.format(i=i)] = forms.CharField(required=False, label="supportedSnssaiList")
            self.fields['nssf_supportedNssaiInPlmnList_supportedSnssaiList-{i}'.format(i=i)].initial = result['nssf']['configuration']['supportedNssaiInPlmnList'][i]['supportedSnssaiList']
        # --- End of supportedNssaiInPlmnList --- #


        # --- Start of nsiList --- #
        NumOfnsiList = len(result['nssf']['configuration']['nsiList'])
        self.fields['nssf_nsiLisCount'].initial = NumOfnsiList - 1
        self.fields['nssf_nsiLisCount'].widget.attrs['class'] = 'invisible'
        self.fields['nssf_nsiLisCount'].widget.attrs['default'] = NumOfnsiList - 1
         
        for i in range(0, NumOfnsiList):
            self.fields['nssf_nsiList_snssai-{i}'.format(i=i)] = forms.CharField(required=False, label="snssai", widget=forms.TextInput(attrs={'class': "pt-4", 'id': 'nssf_nsiListElement-{i}'.format(i=i)}))
            self.fields['nssf_nsiList_snssai-{i}'.format(i=i)].initial = result['nssf']['configuration']['nsiList'][i]['snssai']
            self.fields['nssf_nsiList_nsiInformationList-{i}'.format(i=i)] = forms.CharField(required=False, label="nsiInformationList", widget=forms.TextInput(attrs={'class': "", 'id': 'nssf_nsiListElement-{i}'.format(i=i)}))
            self.fields['nssf_nsiList_nsiInformationList-{i}'.format(i=i)].initial = result['nssf']['configuration']['nsiList'][i]['nsiInformationList']
        # --- End of nsiList --- #


        # --- Start of amfSetList --- #
        NumOfamfSetList = len(result['nssf']['configuration']['amfSetList'])
        self.fields['nssf_amfSetLisCount'].initial = NumOfamfSetList - 1
        self.fields['nssf_amfSetLisCount'].widget.attrs['class'] = 'invisible'
        self.fields['nssf_amfSetLisCount'].widget.attrs['default'] = NumOfamfSetList - 1
        
        for i in range(0, NumOfamfSetList):
            self.fields['nssf_amfSetList_amfSetId-{i}'.format(i=i)] = forms.CharField(required=False, label="amfSetIds", widget=forms.TextInput(attrs={'class': "pt-4 border-top", 'id': 'nssf_amfSetListElement-{i}'.format(i=i)}))
            self.fields['nssf_amfSetList_amfSetId-{i}'.format(i=i)].initial = result['nssf']['configuration']['amfSetList'][i]['amfSetId']
            amfListfield = result['nssf']['configuration']['amfSetList'][i].get('amfList', 'None')
            self.fields['nssf_amfSetList_amfList-{i}'.format(i=i)] = forms.CharField(required=False, label="amfList", widget=forms.TextInput(attrs={'class': "", 'id': 'nssf_amfSetListElement-{i}'.format(i=i)}))
            self.fields['nssf_amfSetList_amfList-{i}'.format(i=i)].initial = amfListfield
            self.fields['nssf_amfSetList_nrfAmfSet-{i}'.format(i=i)] = forms.CharField(required=False, label="nrfAmfSet", widget=forms.TextInput(attrs={'class': "", 'id': 'nssf_amfSetListElement-{i}'.format(i=i)}))
            self.fields['nssf_amfSetList_nrfAmfSet-{i}'.format(i=i)].initial = result['nssf']['configuration']['amfSetList'][i]['nrfAmfSet']
            
            # add extra field for number of tail element
            self.fields['nssf_amfSetList_supportedNssaiAvailabilityDataCount-{i}'.format(i=i)] = forms.CharField(required=False, label="Nssai Count", widget=forms.TextInput(attrs={'enablerforadd': "nssfamfSetListsupNssaiAvaiDataEnabler", 'id': 'nssf_amfSetList_supportedNssaiAvailabilityDataCount-{i}'.format(i=i)}))
            self.fields['nssf_amfSetList_supportedNssaiAvailabilityDataCount-{i}'.format(i=i)].initial = len(result['nssf']['configuration']['amfSetList'][i]['supportedNssaiAvailabilityData'])

            # nssf_amfSetList_supportedNssaiAvailabilityDataCount

            NumOfsupportedNssaiAvailabilityData = len(result['nssf']['configuration']['amfSetList'][i]['supportedNssaiAvailabilityData'])
            for j in range(0, NumOfsupportedNssaiAvailabilityData):
                self.fields['nssf_amfSetList_supportedNssaiAvailabilityData_tai-{i}-{j}'.format(i=i,j=j)] = forms.CharField(required=False, label="tai",widget=forms.TextInput(attrs={'class': "", 'id': 'nssf_amfSetListElement-{i}'.format(i=i)}))
                self.fields['nssf_amfSetList_supportedNssaiAvailabilityData_tai-{i}-{j}'.format(i=i,j=j)].initial = result['nssf']['configuration']['amfSetList'][i]['supportedNssaiAvailabilityData'][j]['tai']
                self.fields['nssf_amfSetList_supportedNssaiAvailabilityData_supportedSnssaiList-{i}-{j}'.format(i=i,j=j)] = forms.CharField(required=False, label="supportedSnssaiList",widget=forms.TextInput(attrs={'class': "", 'id': 'nssf_amfSetListElement-{i}'.format(i=i)}))
                self.fields['nssf_amfSetList_supportedNssaiAvailabilityData_supportedSnssaiList-{i}-{j}'.format(i=i,j=j)].initial = result['nssf']['configuration']['amfSetList'][i]['supportedNssaiAvailabilityData'][j]['supportedSnssaiList']
        # --- End of amfSetList --- #


        # --- Start of amfList --- #
        NumOfamfList = len(result['nssf']['configuration']['amfList'])
        self.fields['nssf_amfLisCount'].initial = NumOfamfList - 1
        self.fields['nssf_amfLisCount'].widget.attrs['class'] = 'invisible'
        self.fields['nssf_amfLisCount'].widget.attrs['default'] = NumOfamfList - 1

        for i in range(0, NumOfamfList):
            self.fields['nssf_amfList_nfId-{i}'.format(i=i)] = forms.CharField(required=False, label="nfId", widget=forms.TextInput(attrs={'class': "pt-4 border-top", 'id': 'nssf_amfListElement-{i}'.format(i=i)}))
            self.fields['nssf_amfList_nfId-{i}'.format(i=i)].initial = result['nssf']['configuration']['amfList'][i]['nfId']
            NumOfsupportedNssaiAvailabilityData = len(result['nssf']['configuration']['amfList'][i]['supportedNssaiAvailabilityData'])

            # add extra field for number of tail element
            self.fields['nssf_amfList_supportedNssaiAvailabilityDataCount-{i}'.format(i=i)] = forms.CharField(required=False, label="Nssai Count", widget=forms.TextInput(attrs={'enablerforadd': "nssfamfListsupNssaiAvaiDataEnabler", 'id': 'nssf_amfList_supportedNssaiAvailabilityDataCount-{i}'.format(i=i)}))
            self.fields['nssf_amfList_supportedNssaiAvailabilityDataCount-{i}'.format(i=i)].initial = len(result['nssf']['configuration']['amfList'][i]['supportedNssaiAvailabilityData'])


            for j in range(0, NumOfsupportedNssaiAvailabilityData):
                self.fields['nssf_amfList_supportedNssaiAvailabilityData_tai-{i}-{j}'.format(i=i,j=j)] = forms.CharField(required=False, label="tai",widget=forms.TextInput(attrs={'class': "", 'id': 'nssf_amfListElement-{i}'.format(i=i)}))
                self.fields['nssf_amfList_supportedNssaiAvailabilityData_tai-{i}-{j}'.format(i=i,j=j)].initial = result['nssf']['configuration']['amfList'][i]['supportedNssaiAvailabilityData'][j]['tai']
                self.fields['nssf_amfList_supportedNssaiAvailabilityData_supportedSnssaiList-{i}-{j}'.format(i=i,j=j)] = forms.CharField(required=False, label="supportedSnssaiList",widget=forms.TextInput(attrs={'class': "", 'id': 'nssf_amfListElement-{i}'.format(i=i)}))
                self.fields['nssf_amfList_supportedNssaiAvailabilityData_supportedSnssaiList-{i}-{j}'.format(i=i,j=j)].initial = result['nssf']['configuration']['amfList'][i]['supportedNssaiAvailabilityData'][j]['supportedSnssaiList']
        # --- End of amfList --- #


        # --- Start of taList --- #
        NumOftaList = len(result['nssf']['configuration']['taList'])
        self.fields['nssf_taLisCount'].initial = NumOftaList - 1
        self.fields['nssf_taLisCount'].widget.attrs['class'] = 'invisible'
        self.fields['nssf_taLisCount'].widget.attrs['default'] = NumOftaList - 1

        for i in range(0, NumOftaList):
            self.fields['nssf_taList_tai-{i}'.format(i=i)] = forms.CharField(required=False, label="tai", widget=forms.TextInput(attrs={'class': "pt-4",'id': 'nssf_taListElement-{i}'.format(i=i)}))
            self.fields['nssf_taList_tai-{i}'.format(i=i)].initial = result['nssf']['configuration']['taList'][i]['tai']
            self.fields['nssf_taList_accessType-{i}'.format(i=i)] = forms.CharField(required=False, label="accessType", widget=forms.TextInput(attrs={'class': "", 'id': 'nssf_taListElement-{i}'.format(i=i)}))
            self.fields['nssf_taList_accessType-{i}'.format(i=i)].initial = result['nssf']['configuration']['taList'][i]['accessType']    
            self.fields['nssf_taList_supportedSnssaiList-{i}'.format(i=i)] = forms.CharField(required=False, label="supportedSnssaiList", widget=forms.TextInput(attrs={'class': "", 'id': 'nssf_taListElement-{i}'.format(i=i)}))
            self.fields['nssf_taList_supportedSnssaiList-{i}'.format(i=i)].initial = result['nssf']['configuration']['taList'][i]['supportedSnssaiList']    
            self.fields['nssf_taList_restrictedSnssaiList-{i}'.format(i=i)] = forms.CharField(required=False, label="restrictedSnssaiList", widget=forms.TextInput(attrs={'class': "", 'id': 'nssf_taListElement-{i}'.format(i=i)}))
            nssf_taList_restrictedSnssaiList_initial = result['nssf']['configuration']['taList'][i].get('restrictedSnssaiList', 'None')
            self.fields['nssf_taList_restrictedSnssaiList-{i}'.format(i=i)].initial = nssf_taList_restrictedSnssaiList_initial  
        # --- End of taList --- #


        # --- Start of mappingListFromPlmn --- #
        NumOfmappingListFromPlmn = len(result['nssf']['configuration']['mappingListFromPlmn'])
        self.fields['nssf_mappingLisFromPlmnCount'].initial = NumOfmappingListFromPlmn - 1
        self.fields['nssf_mappingLisFromPlmnCount'].widget.attrs['class'] = 'invisible'
        self.fields['nssf_mappingLisFromPlmnCount'].widget.attrs['default'] = NumOfmappingListFromPlmn - 1
        
        for i in range(0, NumOfmappingListFromPlmn):
            self.fields['nssf_mappingListFromPlmn_operatorName-{i}'.format(i=i)] = forms.CharField(required=False, label="operatorName", widget=forms.TextInput(attrs={'class': "pt-4",'id': 'nssf_mappingListFromPlmnElement-{i}'.format(i=i)}))
            self.fields['nssf_mappingListFromPlmn_operatorName-{i}'.format(i=i)].initial = result['nssf']['configuration']['mappingListFromPlmn'][i]['operatorName']
            self.fields['nssf_mappingListFromPlmn_homePlmnId-{i}'.format(i=i)] = forms.CharField(required=False, label="homePlmnId", widget=forms.TextInput(attrs={'class': "",'id': 'nssf_mappingListFromPlmnElement-{i}'.format(i=i)}))
            self.fields['nssf_mappingListFromPlmn_homePlmnId-{i}'.format(i=i)].initial = result['nssf']['configuration']['mappingListFromPlmn'][i]['homePlmnId']
            
            NumOfmappingOfSnssai = len(result['nssf']['configuration']['mappingListFromPlmn'][i]['mappingOfSnssai'])

            # add extra field for number of tail element
            self.fields['nssf_mappingListFromPlmn_mappingOfSnssaiCount-{i}'.format(i=i)] = forms.CharField(required=False, label="mappingOfSnssai Count", widget=forms.TextInput(attrs={'enablerforadd': "nssfmappingListFromPlmnEnabler", 'id': 'nssf_mappingListFromPlmn_mappingOfSnssaiCount-{i}'.format(i=i)}))
            self.fields['nssf_mappingListFromPlmn_mappingOfSnssaiCount-{i}'.format(i=i)].initial = len(result['nssf']['configuration']['mappingListFromPlmn'][i]['mappingOfSnssai'])

            for j in range(0, NumOfmappingOfSnssai):
                self.fields['nssf_mappingListFromPlmn_mappingOfSnssai-{i}-{j}'.format(i=i, j=j)] = forms.CharField(required=False, label="mappingOfSnssai", widget=forms.TextInput(attrs={'class': "",'id': 'nssf_mappingListFromPlmnElement-{i}'.format(i=i)}))
                self.fields['nssf_mappingListFromPlmn_mappingOfSnssai-{i}-{j}'.format(i=i, j=j)].initial = result['nssf']['configuration']['mappingListFromPlmn'][i]['mappingOfSnssai'][j]
                


        # --- End of mappingListFromPlmn --- #




    def Hidden(self):
        return [field for field in self if field.name in ('nssf_supportedNssaiInPlmnLisCount', 'nssf_nsiLisCount', 'nssf_taLisCount', 'nssf_amfSetLisCount', 'nssf_amfLisCount', 'nssf_mappingLisFromPlmnCount')]

    def General(self):
        return [field for field in self if field.name in ('nssfName')]

    def SBI(self):
        return [field for field in self if field.name in ('sbi_scheme', 'sbi_registerIPv4', 'sbi_bindingIPv4', 'sbi_port', 'nrfUri')]

    def serviceList(self):
        return [field for field in self if field.name in ('serviceNameList')]
    
    def PlmnList(self):
        return [field for field in self if field.name in ('supportedPlmnList')]

    def supportedNssaiInPlmnList(self):
        return [field for field in self if 'nssf_supportedNssaiInPlmnList' in field.name]

    def nsiList(self):
        return [field for field in self if 'nssf_nsiList' in field.name]

    def amfSetList(self):
        return [field for field in self if 'nssf_amfSetList' in field.name]
    
    def amfList(self):
        return [field for field in self if 'nssf_amfList' in field.name]
    
    def taList(self):
        return [field for field in self if 'nssf_taList' in field.name]
    
    def mappingListFromPlmn(self):
        return [field for field in self if 'nssf_mappingListFromPlmn' in field.name]


# ------------------------------------------------------------------------------


class gNBForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(gNBForm, self).__init__(*args, **kwargs)
        myclient = pymongo.MongoClient(connectionToMongo)
        mydb = myclient['gNB']
        mycol = mydb["config"]

        # --- Start of Initials --- #
        result = mycol.find_one({"_id":2}, {"_id":0})
        self.fields['gNB_RannnodeName'] = forms.CharField(required=False, label="RannnodeName", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['gNB_RannnodeName'].initial = result['RannnodeName']

        self.fields['gNB_servingPlmnId'] = forms.CharField(required=False, label="servingPlmnId", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['gNB_servingPlmnId'].initial = result['servingPlmnId']

        self.fields['gNB_gNBId'] = forms.CharField(required=False, label="gNBId", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['gNB_gNBId'].initial = result['gNBId']

        self.fields['gNB_tac'] = forms.CharField(required=False, label="tac", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['gNB_tac'].initial = result['tac']
        # --- End of Initials --- #
    

    def General(self):
        return [field for field in self if field.name in ('gNB_RannnodeName', 'gNB_servingPlmnId', 'gNB_tac', 'gNB_gNBId')]



# ------------------------------------------------------------------------------


class ueForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ueForm, self).__init__(*args, **kwargs)
        myclient = pymongo.MongoClient(connectionToMongo)
        mydb = myclient['ue']
        mycol = mydb["config"]

        # --- Start of Initials --- #
        result = mycol.find_one({"_id":2}, {"_id":0})
        self.fields['ue_imsi'] = forms.CharField(required=False, label="imsi", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['ue_imsi'].initial = result['imsi']

        self.fields['ue_DNN'] = forms.CharField(required=False, label="dnn", widget=forms.TextInput(attrs={'class': ""}))
        self.fields['ue_DNN'].initial = result['DNN']

        # self.fields['ue_sNssai'] = forms.CharField(required=False, label="sNssai", widget=forms.TextInput(attrs={'class': ""}))
        # self.fields['ue_sNssai'].initial = result['sNssai']
        # --- End of Initials --- #

    def General(self):
        return [field for field in self if field.name in ('ue_imsi', 'ue_DNN')]


# ------------------------------------------------------------------------------

from fiveGApp.models import RunScenariosModel
class RunScenarioForm(forms.Form):
    # Scenario Name
    name = forms.ModelChoiceField(queryset = RunScenariosModel.objects.filter(availability=True), widget=forms.TextInput(attrs={'id':'RunScenarioName'}))
    TestName = forms.CharField(max_length=50)
