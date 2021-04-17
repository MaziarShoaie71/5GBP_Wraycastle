from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from fiveGApp.multiform import MultiFormsView # this is a Mixin from github for Multi fom in a class View
from django.http import JsonResponse, HttpResponse
# ******************************************************************************
from fiveGApp.forms import RunScenarioForm, amfForm, smfForm, ausfForm, nrfForm, pcfForm, udmForm,udrForm, nssfForm, upfForm, gNBForm, ueForm
# ******************************************************************************
from fiveGApp.yamlConfigUpdate import UpdateDoc, findKeyParents, configLoader, configWriter
# ******************************************************************************
from django.conf import settings
from os import path, system, chdir, kill
import os, signal
import subprocess
from django.contrib import messages
import pymongo
import yaml
import subprocess
import time
import json


connectionToMongo = 'mongodb://127.0.0.1:27017/'


class fiveGbpApp(LoginRequiredMixin, MultiFormsView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'fiveGApp/fiveGApp.html'
    form_classes = {'amfForm': amfForm,'smfForm': smfForm, 'ausfForm': ausfForm, 'nrfForm': nrfForm, 'pcfForm': pcfForm, \
                    "udmForm": udmForm, "udrForm": udrForm, "nssfForm": nssfForm, "upfForm":upfForm, 'gNBForm': gNBForm, \
                    "ueForm": ueForm, 'runScenario': RunScenarioForm}


# Covert decimal to aper.OctetString x01x02x03
def octetString(Number, BitLength):
    Bin = format(Number, 'b').zfill(BitLength)
    Sp = ["0x" + hex(int(Bin[i:i+8],2))[2:].zfill(2) for i in range(0, len(Bin), 8)]
    decimalToOctetString = ''.join(Sp).replace('0x','x')
    return decimalToOctetString


def ueUpdater(request):
    PressedButton = request.POST.get('PressedButton')
    imsi = request.POST.get('ue_imsi')
    dnn = request.POST.get('ue_DNN')

    queryDict = request.POST.dict()

    # Save dictionary of inputs a key:value for reset button
    myclient = pymongo.MongoClient(connectionToMongo)
    # mydb = myclient['ue']
    # mycol = mydb["config"]
    # x = mycol.delete_one({"_id": "ue"})
    # mycol.insert_one({"_id": "ue", "data": queryDict})


    # ----------------- To Build in MongoDB -----------------
    builddb = myclient['build']
    buildcol = builddb['config']

    if PressedButton == 'Submit':
        data = request.POST.dict()
        mydb = myclient['ue']
        mycol = mydb["config"]
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "imsi": imsi, "DNN": dnn})

    	# update build db submit
        x = buildcol.update_one({"_id": 2}, {"$set": 
                {
                    "imsi": imsi, 
                    "dnn": dnn, 
                }
            }        
        )

    elif PressedButton == 'Reset':
        mydb = myclient['ue']
        # reset id=2 value and replace with id=1
        mycol = mydb["config"]
        tempdata = mycol.find_one({"_id": 1}, {"_id":0})
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "imsi": tempdata["imsi"], "DNN": tempdata["DNN"]})

        # update/Reset Build DB
        tempdataBuild = buildcol.find_one({"_id": 1}, {"_id":0})
        x = buildcol.update_one({"_id": 2}, {"$set": 
                {
                    "imsi": tempdataBuild["imsi"], 
                    "dnn": tempdataBuild["dnn"], 
                }
            }        
        )


        Defaultdata = mycol.find_one({"_id": "ue"}, {"_id": 0})
        data = Defaultdata.get('data')
        del data['PressedButton']
        del data['csrfmiddlewaretoken']
        
    myclient.close()
    return JsonResponse(data)


def gNBUpdater(request):
    PressedButton = request.POST.get('PressedButton')
    RannnodeName = request.POST.get('gNB_RannnodeName')
    servingPlmnId = request.POST.get('gNB_servingPlmnId')
    gNBId = request.POST.get('gNB_gNBId')
    tac = request.POST.get('gNB_tac')

    queryDict = request.POST.dict()

    # Save dictionary of inputs a key:value for reset button
    myclient = pymongo.MongoClient(connectionToMongo)
    # mydb = myclient['gNB']
    # mycol = mydb["config"]
    # x = mycol.delete_one({"_id": "gNB"})
    # mycol.insert_one({"_id": "gNB", "data": queryDict})

    # ----------------- To Build in MongoDB -----------------
    builddb = myclient['build']
    buildcol = builddb['config']

    # rannnodeName
    rannnodeNameToBuild = RannnodeName

    # plmnid
    plmnid = eval(servingPlmnId)
    mnc = str(plmnid['mnc']) # 93
    mcc = str(plmnid['mcc']) # 208
    plmnidToBuild = "x" + mcc[1] + mcc[0] + "xf" + mcc[2] + "x" + mnc[1] + mnc[0]
    
    # gNBId
    gNBIdToBuild = gNBId

    # tac
    tacToBuild = octetString(int(tac), 24)

    # servingPlmnId
    servingPlmnIdToBuild = mcc + mnc

    # AuthenticationSubs
    AuthenticationSubsToBuild = "5G:mnc0" + mnc + ".mcc" + mcc + ".3gppnetwork.org"
    # -------------------------------------------------------


    if PressedButton == 'Submit':
        data = request.POST.dict()
        mydb = myclient['gNB']
        mycol = mydb["config"]
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "RannnodeName": RannnodeName, "servingPlmnId": servingPlmnId, "tac": tac, "gNBId": gNBId})

        # update build db submit
        x = buildcol.update_one({"_id": 2}, {"$set": 
                {
                    "plmnid": plmnidToBuild, 
                    "rannnodeName": rannnodeNameToBuild,
                    "gNBId": gNBId,
                    "servingPlmnId": servingPlmnIdToBuild,
                    "AuthenticationSubs": AuthenticationSubsToBuild,
                    "tac": tacToBuild,
                }
            }        
        )

    elif PressedButton == 'Reset':
        mydb = myclient['gNB']
        # reset id=2 value and replace with id=1
        mycol = mydb["config"]
        tempdata = mycol.find_one({"_id": 1}, {"_id":0})
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "RannnodeName": tempdata["RannnodeName"], "servingPlmnId": tempdata["servingPlmnId"], "tac": tempdata["tac"], "gNBId": tempdata["gNBId"]})

        Defaultdata = mycol.find_one({"_id": "gNB"}, {"_id": 0})
        data = Defaultdata.get('data')
        del data['PressedButton']
        del data['csrfmiddlewaretoken']
    
        # update/Reset Build DB
        tempdataBuild = buildcol.find_one({"_id": 1}, {"_id":0})
        x = buildcol.update_one({"_id": 2}, {"$set": 
                {
                    "plmnid": tempdataBuild["plmnid"], 
                    "rannnodeName": tempdataBuild["rannnodeName"],
                    "gNBId": tempdataBuild["gNBId"],
                    "servingPlmnId": tempdataBuild["servingPlmnId"],
                    "AuthenticationSubs": tempdataBuild["AuthenticationSubs"],
                    "tac": tempdataBuild["tac"],
                }
            }        
        )

    myclient.close()
    return JsonResponse(data)


def amfUpdater(request):
    # yamlUpdater function goes here #
    BasefileName = 'amfcfg' # name of reference file
    fileName = 'amfcfg.conf'
    yamlConfigPath = path.join(settings.BASE_DIR, 'yamlConfigFiles/')

    PressedButton = request.POST.get('PressedButton')

    amfName = request.POST.get('amfName')
    sbi_scheme = request.POST.get('sbi_scheme')
    sbi_registerIPv4 = request.POST.get('sbi_registerIPv4')
    sbi_bindingIPv4 = request.POST.get('sbi_bindingIPv4')
    sbi_port = request.POST.get('sbi_port')

    sbi = {
        "scheme": sbi_scheme,
        "registerIPv4": sbi_registerIPv4,
        "bindingIPv4": sbi_bindingIPv4,
        "port": sbi_port
    }
    nrfUri = request.POST.get('nrfUri')
    ngapIpList = request.POST.get('ngapIpList')
    ngapIpList = eval(ngapIpList)
    serviceNameList = request.POST.get('amf_serviceNameList')
    serviceNameList = eval(serviceNameList)
    networkName_full = request.POST.get('amf_general_full')
    networkName_short = request.POST.get('amf_general_short')
    
    # Security
    security_integrityOrder = request.POST.get('amf_security_integrityOrder')
    security_integrityOrder = eval(security_integrityOrder)
    security_cipheringOrder = request.POST.get('amf_security_cipheringOrder')
    security_cipheringOrder = eval(security_cipheringOrder)

    # timers
    t3502 = request.POST.get('amf_timers_t3502')
    t3512 = request.POST.get('amf_timers_t3512')
    non3gppDeregistrationTimer = request.POST.get('amf_timers_non3gppDeregistrationTimer')
    
    # DNN
    supportDnnList = request.POST.get('amf_supportDnnList')
    supportDnnList = eval(supportDnnList)
    queryDict = request.POST.dict()
    keysInData = queryDict.keys()
    


    # --- Start of servedGuamiList --- #
    amf_servedGuamiListCount = len([x for x in keysInData if "amf_servedGuamiList_plmnId" in x])
    servedGuamiList = []
    for i in range(0, amf_servedGuamiListCount):
        plmnId = request.POST.get('amf_servedGuamiList_plmnId-{ix}'.format(ix=i))
        if PressedButton == 'Submit':
            plmnId = eval(plmnId)
        amfId = request.POST.get('amf_servedGuamiList_amfId-{ix}'.format(ix=i))
        
        # print(servedGuamiList)
        servedGuamiList.append({'plmnId': plmnId, 'amfId': amfId})
    servedGuamiList = servedGuamiList
    # --- End of servedGuamiList --- #


    # --- Start of supportTaiList --- #
    amf_supportTaiListCount = len([x for x in keysInData if "amf_supportTaiList_plmnId" in x])
    supportTaiList = []
    for i in range(0, amf_supportTaiListCount):
        plmnId = request.POST.get('amf_supportTaiList_plmnId-{ix}'.format(ix=i))
        if PressedButton == 'Submit':
            plmnId = eval(plmnId)
        tac = request.POST.get('amf_supportTaiList_tac-{ix}'.format(ix=i))
        # print(supportTaiList)
        supportTaiList.append({"plmnId": plmnId, "tac": tac})
    # --- End of supportTaiList --- #


    # --- Start of plmnSupportList --- #
    amf_plmnSupportListCount = len([x for x in keysInData if "amf_plmnSupportList_plmnId" in x])
    plmnSupportList = []
    for i in range(0, amf_plmnSupportListCount):
        plmnId = request.POST.get('amf_plmnSupportList_plmnId-{ix}'.format(ix=i))
        snssaiList = request.POST.get('amf_plmnSupportList_snssaiList-{ix}'.format(ix=i))
        if PressedButton == 'Submit':
            plmnId = eval(plmnId)
            snssaiList = eval(snssaiList)
        # print(plmnSupportList)
        plmnSupportList.append({"plmnId": plmnId, "snssaiList": snssaiList})

    
    # --- End of plmnSupportList --- #


    dataConfig = {
        "info": {
            "version": "1.0.0",
            "description": "AMF initial local configuration"
        },
        "configuration": {
            "amfName": amfName,
            "ngapIpList": ngapIpList,
            "sbi": sbi,
            "serviceNameList": serviceNameList,
            "servedGuamiList": servedGuamiList,
            "supportTaiList": supportTaiList,
            "plmnSupportList": plmnSupportList,
            "supportDnnList": supportDnnList,
            "nrfUri": nrfUri,
            "security": {
                "integrityOrder": security_integrityOrder,
                "cipheringOrder": security_cipheringOrder
            },
            "networkName": {
                "full": networkName_full,
                "short": networkName_short
            },
            "t3502": t3502,
            "t3512": t3512,
            "non3gppDeregistrationTimer": non3gppDeregistrationTimer
        }
    }


    # Save dictionary of inputs a key:value for reset button
    myclient = pymongo.MongoClient(connectionToMongo)
    # mydb = myclient['amf']
    # mycol = mydb["config"]
    # x = mycol.delete_one({"_id": "amf"})
    # mycol.insert_one({"_id": "amf", "data": queryDict})

    if PressedButton == 'Submit':
        data = request.POST.dict()
        configWriter(dataConfig, yamlConfigPath, fileName)

        with open(yamlConfigPath + fileName) as fileConfig:
            docIn = yaml.load(fileConfig, Loader=yaml.BaseLoader)
        print(dataConfig)
        # Save userinput for later use after reload
        mydb = myclient['amf']
        mycol = mydb["config"]
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "amf": dataConfig})

    elif PressedButton == 'Reset':
        mydb = myclient['amf']
        mycol = mydb["config"]
        # reset id=2 value and replace with id=1
        tempdata = mycol.find_one({"_id": 1}, {"amf":1, "_id":0})
        tempdata = tempdata['amf']
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "amf": tempdata})
        # data = mycol.find_one({"_id": "amf"}, {"PressedButton":0, "_id":0, "csrfmiddlewaretoken":0})
        Defaultdata = mycol.find_one({"_id": "amf"}, {"_id": 0, "data": 1})
        data = Defaultdata.get('data')
        del data['PressedButton']
        del data['csrfmiddlewaretoken']
        # data = Defaultdata.pop('PressedButton').pop('csrfmiddlewaretoken')
        print(data)
        updatedData = configLoader(yamlConfigPath, BasefileName)
        configWriter(updatedData, yamlConfigPath, fileName)
    myclient.close()

    return JsonResponse(data)

# ------------------------------------------------------------------------------

def smfUpdater(request):
    
    # yamlUpdater function goes here #
    BasefileName = 'smfcfg.test' # name of reference file
    fileName = 'smfcfg.single.test.conf'
    yamlConfigPath = path.join(settings.BASE_DIR, 'yamlConfigFiles/')

    PressedButton = request.POST.get('PressedButton')

    smfName = request.POST.get('smfName')

    sbi_scheme = request.POST.get('sbi_scheme')
    sbi_registerIPv4 = request.POST.get('sbi_registerIPv4')
    sbi_bindingIPv4 = request.POST.get('sbi_bindingIPv4')
    sbi_port = request.POST.get('sbi_port')

    sbi = {
        "scheme": sbi_scheme,
        "registerIPv4": sbi_registerIPv4,
        "bindingIPv4": sbi_bindingIPv4,
        "port": sbi_port,
        "tls": {
            "key":"free5gc/support/TLS/smf.key",
            "pem":"free5gc/support/TLS/smf.pem"
        }
    }
    
    nrfUri = request.POST.get('nrfUri')
    serviceNameList = request.POST.get('smf_serviceNameList')
    serviceNameList = eval(serviceNameList)
    pfcp = request.POST.get('smf_pfcp')
    pfcp = eval(pfcp)
    ue_subnet = request.POST.get('smf_ue_subnet')

    queryDict = request.POST.dict()
    keysInData = queryDict.keys()



    # --- Start of snssai_info --- #
    smf_snssai_infoCount = len([x for x in keysInData if "smf_snssai_info_sNssai" in x])
    snssai_info = []
    for i in range(0, smf_snssai_infoCount):
        sNssai = request.POST.get('smf_snssai_info_sNssai-{ix}'.format(ix=i))
        dnnSmfInfoList = request.POST.get('smf_snssai_info_dnnSmfInfoList-{ix}'.format(ix=i))
        if PressedButton == 'Submit':
            sNssai = eval(sNssai)
            dnnSmfInfoList = eval(dnnSmfInfoList)
        snssai_info.append({'sNssai': sNssai, 'dnnSmfInfoList': dnnSmfInfoList})
    # --- End of snssai_info --- #



    # --- Start of userplane_information --- #
    smf_userplane_information_up_nodesCount = len([x for x in keysInData if "smf_userplane_information_up_nodes_name" in x])
    up_nodes = {}
    for i in range(0, smf_userplane_information_up_nodesCount):
        nodeName = request.POST.get('smf_userplane_information_up_nodes_name-{ix}'.format(ix=i))
        nodeData = request.POST.get('smf_userplane_information_up_nodes_node-{ix}'.format(ix=i))
        if PressedButton == 'Submit':
            nodeData = eval(nodeData)
        up_nodes[nodeName] = nodeData

    smf_userplane_information_linksCount = len([x for x in keysInData if "smf_userplane_information_links" in x])
    links = []
    for i in range(0, smf_userplane_information_linksCount):
        lnk = request.POST.get('smf_userplane_information_links-{ix}'.format(ix=i))
        if PressedButton == 'Submit':
            links.append(eval(lnk))
    userplane_information = {"up_nodes": up_nodes, "links": links}
    # --- End of userplane_information --- #

    # --- Start of dnn --- #
    smf_dnnCount = len([x for x in keysInData if "smf_dnn_name" in x])
    dnn = {}
    for i in range(0, smf_dnnCount):
        dnnName = request.POST.get('smf_dnn_name-{ix}'.format(ix=i))
        dnsipv4 = request.POST.get('smf_dnn_ipv4-{ix}'.format(ix=i))
        dnsipv6 = request.POST.get('smf_dnn_ipv6-{ix}'.format(ix=i))
        dnn[dnnName] = {"dns": {"ipv4": dnsipv4, "ipv6": dnsipv6}}
    # --- End of dnn --- #


    # config/test/smfcfg.test.conf is created from config/test/smfcfg.single.test.conf
    # be carefull to rename smfcfg.single.test.conf and replace smfcfg.test.conf 
    dataConfig = {
        "info":{
            "version":"1.0.0",
            "description":"SMF initial local configuration"
        },
        "configuration":{
            "smfName": smfName,
            "sbi": sbi,
            "serviceNameList":serviceNameList,
            "snssai_info": snssai_info,
            "pfcp": pfcp,
            "userplane_information": userplane_information,
            "ue_subnet": ue_subnet,
            "dnn": dnn,
            "nrfUri": nrfUri
        }
    }


    # Save dictionary of inputs a key:value for reset button
    myclient = pymongo.MongoClient(connectionToMongo)
    # mydb = myclient['smf']
    # mycol = mydb["config"]
    # x = mycol.delete_one({"_id": "smf"})
    # mycol.insert_one({"_id": "smf", "data": queryDict})


    if PressedButton == 'Submit':
        data = request.POST.dict()
        configWriter(dataConfig, yamlConfigPath, fileName)

        with open(yamlConfigPath + fileName) as fileConfig:
            docIn = yaml.load(fileConfig, Loader=yaml.BaseLoader)
        # print(dataConfig)

        # Save userinput for later use after reload
        mydb = myclient['smf']
        mycol = mydb["config"]
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "smf": dataConfig})        


    elif PressedButton == 'Reset':
        mydb = myclient['smf']
        # reset id=2 value and replace with id=1
        mycol = mydb["config"]
        tempdata = mycol.find_one({"_id": 1}, {"smf":1, "_id":0})
        tempdata = tempdata['smf']
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "smf": tempdata})
        Defaultdata = mycol.find_one({"_id": "smf"}, {"_id": 0, "data": 1})
        data = Defaultdata.get('data')
        del data['PressedButton']
        del data['csrfmiddlewaretoken']
        print(data)
        updatedData = configLoader(yamlConfigPath, BasefileName)
        configWriter(updatedData, yamlConfigPath, fileName)
    myclient.close()
    return JsonResponse(data)

# ------------------------------------------------------------------------------

def ausfUpdater(request):
    # yamlUpdater function goes here #
    BasefileName = 'ausfcfg' # name of reference file
    fileName = 'ausfcfg.conf'
    yamlConfigPath = path.join(settings.BASE_DIR, 'yamlConfigFiles/')

    PressedButton = request.POST.get('PressedButton')

    ausfName = request.POST.get('ausfName')
    sbi_scheme = request.POST.get('sbi_scheme')
    sbi_registerIPv4 = request.POST.get('sbi_registerIPv4')
    sbi_bindingIPv4 = request.POST.get('sbi_bindingIPv4')
    sbi_port = request.POST.get('sbi_port')
    sbi={
        "scheme": sbi_scheme,
        "registerIPv4": sbi_registerIPv4,
        "bindingIPv4": sbi_bindingIPv4,
        "port": sbi_port
    }
    nrfUri = request.POST.get('nrfUri')
    serviceNameList = request.POST.get('serviceNameList')
    serviceNameList = eval(serviceNameList)
    groupId = request.POST.get('groupId')

    queryDict = request.POST.dict()
    keysInData = queryDict.keys()

    # --- Start of plmnSupportList --- #
    ausf_plmnSupportListCount = len([x for x in keysInData if "ausf_plmnSupportList" in x])
    plmnSupportList = []
    for i in range(0, ausf_plmnSupportListCount):
        plmnId = request.POST.get('ausf_plmnSupportList-{ix}'.format(ix=i))
        if PressedButton == 'Submit':
            plmnId = eval(plmnId)

        plmnSupportList.append(plmnId)
    # --- End of plmnSupportList --- #



    dataConfig = {
        "info":{
            "version":"1.0.0",
            "description":"AUSF initial local configuration"
        },
        "configuration":{
            "sbi":{
                "scheme": sbi_scheme,
                "registerIPv4": sbi_registerIPv4,
                "bindingIPv4": sbi_bindingIPv4,
                "port": sbi_port,
            },
            "serviceNameList": serviceNameList,
			"nrfUri": nrfUri,
            "plmnSupportList": plmnSupportList,
			"groupId": groupId
        }
    }


    # Save dictionary of inputs a key:value for reset button
    myclient = pymongo.MongoClient(connectionToMongo)
    # mydb = myclient['ausf']
    # mycol = mydb["config"]
    # x = mycol.delete_one({"_id": "ausf"})
    # mycol.insert_one({"_id": "ausf", "data": queryDict})


    if PressedButton == 'Submit':
        data = request.POST.dict()
        configWriter(dataConfig, yamlConfigPath, fileName)

        with open(yamlConfigPath + fileName) as fileConfig:
            docIn = yaml.load(fileConfig, Loader=yaml.BaseLoader)
        print(dataConfig)
        # Save userinput for later use after reload
        mydb = myclient['ausf']
        mycol = mydb["config"]
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "ausf": dataConfig})

    elif PressedButton == 'Reset':
        mydb = myclient['ausf']

        # reset id=2 value and replace with id=1
        mycol = mydb["config"]
        tempdata = mycol.find_one({"_id": 1}, {"ausf":1, "_id":0})
        tempdata = tempdata['ausf']
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "ausf": tempdata})
        Defaultdata = mycol.find_one({"_id": "ausf"}, {"_id": 0, "data": 1})
        data = Defaultdata.get('data')
        del data['PressedButton']
        del data['csrfmiddlewaretoken']
        updatedData = configLoader(yamlConfigPath, BasefileName)
        configWriter(updatedData, yamlConfigPath, fileName)

    myclient.close()
    return JsonResponse(data)

# ------------------------------------------------------------------------------

def nrfUpdater(request):
    # yamlUpdater function goes here #
    BasefileName = 'nrfcfg' # name of reference file
    fileName = 'nrfcfg.conf'
    yamlConfigPath = path.join(settings.BASE_DIR, 'yamlConfigFiles/')

    PressedButton = request.POST.get('PressedButton')

    nrfName = request.POST.get('nrfName')
    MongoDBName = request.POST.get('MongoDBName')
    MongoDBUrl = request.POST.get('MongoDBUrl')
    DefaultServiceIP = request.POST.get('DefaultServiceIP')
    sbi_scheme = request.POST.get('sbi_scheme')
    sbi_ipv4Addr = request.POST.get('sbi_ipv4Addr')
    sbi_port = request.POST.get('sbi_port')
    sbi = {
        "scheme": sbi_scheme,
        "ipv4Addr": sbi_ipv4Addr,
        "port": sbi_port
    }
    DefaultPlmnId = request.POST.get('DefaultPlmnId')
    DefaultPlmnId = eval(DefaultPlmnId)
    serviceNameList = request.POST.get('serviceNameList')
    serviceNameList = eval(serviceNameList)

    dataConfig = {
        "info":{
            "version":"1.0.0",
            "description":"NRF initial local configuration"
        },
        "configuration":{
            "MongoDBName": MongoDBName,
            "MongoDBUrl": MongoDBUrl,
            "DefaultServiceIP": DefaultServiceIP,
            "sbi": sbi,
            "DefaultPlmnId":DefaultPlmnId,
            "serviceNameList":serviceNameList
        }
    }

    queryDict = request.POST.dict()
    keysInData = queryDict.keys()    

    # Save dictionary of inputs a key:value for reset button
    myclient = pymongo.MongoClient(connectionToMongo)
    # mydb = myclient['nrf']
    # mycol = mydb["config"]
    # x = mycol.delete_one({"_id": "nrf"})
    # mycol.insert_one({"_id": "nrf", "data": queryDict})
	


    if PressedButton == 'Submit':
        data = request.POST.dict()
        configWriter(dataConfig, yamlConfigPath, fileName)

        with open(yamlConfigPath + fileName) as fileConfig:
            docIn = yaml.load(fileConfig, Loader=yaml.BaseLoader)
        print(dataConfig)
        # Save userinput for later use after reload
        mydb = myclient['nrf']
        mycol = mydb["config"]
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "nrf": dataConfig})

    elif PressedButton == 'Reset':
        mydb = myclient['nrf']

        # reset id=2 value and replace with id=1
        mycol = mydb["config"]
        tempdata = mycol.find_one({"_id": 1}, {"nrf":1, "_id":0})
        tempdata = tempdata['nrf']
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "nrf": tempdata})
        Defaultdata = mycol.find_one({"_id": "nrf"}, {"_id": 0, "data": 1})
        data = Defaultdata.get('data')
        del data['PressedButton']
        del data['csrfmiddlewaretoken']

        updatedData = configLoader(yamlConfigPath, BasefileName)
        configWriter(updatedData, yamlConfigPath, fileName)
    myclient.close()
    return JsonResponse(data)



def nrfConfigLoader(request):
    nf = request.POST.get('nf')
    NFdb = request.POST.get('db')
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    db = client[NFdb]
    col = db["NfProfile"]
    nfdata = col.find_one({"nfType": nf}, {"_id": 0})
    if nfdata:
        status = True
    else:
        status = False
    data = {"nfdata": nfdata, "status": status}
    client.close()
    return JsonResponse(data)

# ------------------------------------------------------------------------------

def udmUpdater(request):
    # yamlUpdater function goes here #
    BasefileName = 'udmcfg' # name of reference file
    fileName = 'udmcfg.conf'
    yamlConfigPath = path.join(settings.BASE_DIR, 'yamlConfigFiles/')

    PressedButton = request.POST.get('PressedButton')

    udmName = request.POST.get('udmName')
    serviceNameList = request.POST.get('serviceNameList')
    sbi_scheme = request.POST.get('sbi_scheme')
    sbi_registerIPv4 = request.POST.get('sbi_registerIPv4')
    sbi_bindingIPv4 = request.POST.get('sbi_bindingIPv4')
    sbi_port = request.POST.get('sbi_port')
    sbi = {
        "scheme": sbi_scheme,
        "registerIPv4": sbi_registerIPv4,
        "bindingIPv4": sbi_bindingIPv4,
        "port": sbi_port,
        "tls":{
            "log":"free5gc/udmsslkey.log",
            "pem":"free5gc/support/TLS/udm.pem",
            "key":"free5gc/support/TLS/udm.key"
        }
    }
    udrclient_scheme = request.POST.get('udrclient_scheme')
    udrclient_ipv4Addr = request.POST.get('udrclient_ipv4Addr')
    udrclient_port = request.POST.get('udrclient_port')
    udrclient = {
        "scheme": udrclient_scheme,
        "ipv4Addr": udrclient_ipv4Addr,
        "port": udrclient_port
    }


    nrfclient_scheme = request.POST.get('nrfclient_scheme')
    nrfclient_ipv4Addr = request.POST.get('nrfclient_ipv4Addr')
    nrfclient_port = request.POST.get('nrfclient_port')
    nrfclient = {
        "scheme": nrfclient_scheme,
        "ipv4Addr": nrfclient_ipv4Addr,
        "port": nrfclient_port
    }

    nrfUri = request.POST.get('nrfUri')

    dataConfig = {
        "info":{
            "version":"1.0.0",
            "description":"NRF initial local configuration"
        },
        "configuration":{
            "serviceNameList": serviceNameList,
            "sbi": sbi,
            "udrclient": udrclient,
            "nrfclient": nrfclient,
            "nrfUri": nrfUri,
            "keys":{
                "udmProfileAHNPublicKey": "5a8d38864820197c3394b92613b20b91633cbd897119273bf8e4a6f4eec0a650",
                "udmProfileAHNPrivateKey": "c53c22208b61860b06c62e5406a7b330c2b577aa5558981510d128247d38bd1d",
                "udmProfileBHNPublicKey": "0472DA71976234CE833A6907425867B82E074D44EF907DFB4B3E21C1C2256EBCD15A7DED52FCBB097A4ED250E036C7B9C8C7004C4EEDC4F068CD7BF8D3F900E3B4",
                "udmProfileBHNPrivateKey": "F1AB1074477EBCC7F554EA1C5FC368B1616730155E0041AC447D6301975FECDA",
            }
        }
    }

    queryDict = request.POST.dict()
    keysInData = queryDict.keys()

    # Save dictionary of inputs a key:value for reset button
    myclient = pymongo.MongoClient(connectionToMongo)
    # mydb = myclient['udm']
    # mycol = mydb["config"]
    # x = mycol.delete_one({"_id": "udm"})
    # mycol.insert_one({"_id": "udm", "data": queryDict})
    
    if PressedButton == 'Submit':
        data = request.POST.dict()
        configWriter(dataConfig, yamlConfigPath, fileName)

        with open(yamlConfigPath + fileName) as fileConfig:
            docIn = yaml.load(fileConfig, Loader=yaml.BaseLoader)
        print(dataConfig)
        # Save userinput for later use after reload
        mydb = myclient['udm']
        mycol = mydb["config"]
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "udm": dataConfig})

    elif PressedButton == 'Reset':
        mydb = myclient['udm']

        # reset id=2 value and replace with id=1
        mycol = mydb["config"]
        tempdata = mycol.find_one({"_id": 1}, {"udm":1, "_id":0})
        tempdata = tempdata['udm']
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "udm": tempdata})
        
        Defaultdata = mycol.find_one({"_id": "udm"}, {"_id": 0, "data": 1})
        data = Defaultdata.get('data')
        del data['PressedButton']
        del data['csrfmiddlewaretoken']

        updatedData = configLoader(yamlConfigPath, BasefileName)
        configWriter(updatedData, yamlConfigPath, fileName)
    myclient.close()
    return JsonResponse(data)
  
# ------------------------------------------------------------------------------

def udrUpdater(request):
    # yamlUpdater function goes here #
    BasefileName = 'udrcfg' # name of reference file
    fileName = 'udrcfg.conf'
    yamlConfigPath = path.join(settings.BASE_DIR, 'yamlConfigFiles/')

    PressedButton = request.POST.get('PressedButton')

    udrName = request.POST.get('udrName')
    sNssai = eval(request.POST.get('SmPolicySnssaiData_Snssai'))
    sd = sNssai["sd"]
    sd = 'x' + 'x'.join(sd[i:i+2] for i in range(0, len(sd), 2))
    sst = sNssai["sst"]
    sst = 'x' + sst
    # @todo: To create x01x02x02 and insert to build db

    sbi_scheme = request.POST.get('sbi_scheme')
    sbi_registerIPv4 = request.POST.get('sbi_registerIPv4')
    sbi_bindingIPv4 = request.POST.get('sbi_bindingIPv4')
    sbi_port = request.POST.get('sbi_port')
    sbi = {
        "scheme":sbi_scheme,
        "registerIPv4": sbi_registerIPv4,
        "bindingIPv4": sbi_bindingIPv4,
        "port": sbi_port,
    }
    nrfUri = request.POST.get('nrfUri')

    mongodb_name = request.POST.get('mongodb_name')
    mongodb_url = request.POST.get('mongodb_url')

    mongodb = {
        "name": mongodb_name,
        "url": mongodb_url
    }

    dataConfig = {
        "info":{
            "version":"1.0.0",
            "description":"UDR initial local configuration"
        },
        "configuration":{
            "sbi": sbi,
            "mongodb": mongodb,
            "nrfUri": nrfUri
        }
    }
    
    queryDict = request.POST.dict()
    keysInData = queryDict.keys()

    # Save dictionary of inputs a key:value for reset button
    myclient = pymongo.MongoClient(connectionToMongo)
    # mydb = myclient['udr']
    # mycol = mydb["config"]
    # x = mycol.delete_one({"_id": "udr"})
    # mycol.insert_one({"_id": "udr", "data": queryDict})
    
    # ----------------- To Build in MongoDB -----------------
    builddb = myclient['build']
    buildcol = builddb['config']

    if PressedButton == 'Submit':
        data = request.POST.dict()
        configWriter(dataConfig, yamlConfigPath, fileName)

        with open(yamlConfigPath + fileName) as fileConfig:
            docIn = yaml.load(fileConfig, Loader=yaml.BaseLoader)
        print(dataConfig)
        # Save userinput for later use after reload
        mydb = myclient['udr']
        mycol = mydb["config"]
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "udr": dataConfig})
        x = mycol.update_one({"_id":2}, {'$set': {"udr.extraConfig": {"sNssai": sNssai}}})

        # update build db submit
        x = buildcol.update_one({"_id": 2}, {"$set": 
                {
                    "snssai_sst": sst, 
                    "snssai_sd": sd,
                }
            }        
        )

    elif PressedButton == 'Reset':
        mydb = myclient['udr']
        # reset id=2 value and replace with id=1
        mycol = mydb["config"]
        tempdata = mycol.find_one({"_id": 1}, {"udr":1, "_id":0})
        tempdata = tempdata['udr']
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "udr": tempdata})

        Defaultdata = mycol.find_one({"_id": "udr"}, {"_id": 0, "data": 1})
        data = Defaultdata.get('data')
        del data['PressedButton']
        del data['csrfmiddlewaretoken']

        # update/Reset Build DB
        tempdataBuild = buildcol.find_one({"_id": 1}, {"_id":0})
        x = buildcol.update_one({"_id": 2}, {"$set": 
                {
                    "snssai_sst": tempdataBuild["snssai_sst"], 
                    "snssai_sd": tempdataBuild["snssai_sd"],
                }
            }        
        )
        updatedData = configLoader(yamlConfigPath, BasefileName)
        configWriter(updatedData, yamlConfigPath, fileName)
    myclient.close()
    return JsonResponse(data)

# ------------------------------------------------------------------------------

def pcfUpdater(request):
    # yamlUpdater function goes here #
    BasefileName = 'pcfcfg' # name of reference file
    fileName = 'pcfcfg.conf'
    yamlConfigPath = path.join(settings.BASE_DIR, 'yamlConfigFiles/')

    PressedButton = request.POST.get('PressedButton')

    pcfName = request.POST.get('pcfName')
    defaultBdtRefId = request.POST.get('defaultBdtRefId')
    timeFormat = request.POST.get('timeFormat')
    sbi_scheme = request.POST.get('sbi_scheme')
    sbi_registerIPv4 = request.POST.get('sbi_registerIPv4')
    sbi_bindingIPv4 = request.POST.get('sbi_bindingIPv4')
    sbi_port = request.POST.get('sbi_port')
    sbi = {
        "scheme":sbi_scheme,
        "registerIPv4":sbi_registerIPv4,
        "bindingIPv4":sbi_bindingIPv4,
        "port":sbi_port,
    }    

    nrfUri = request.POST.get('nrfUri')


    queryDict = request.POST.dict()
    keysInData = queryDict.keys()


    
    # --- Start of supportTaiList --- #
    pcf_serviceListCount = len([x for x in keysInData if "pcf_serviceList_serviceName" in x])
    serviceList = []
    for i in range(0, pcf_serviceListCount):
        serviceName = request.POST.get('pcf_serviceList_serviceName-{ix}'.format(ix=i))
        suppFeat = request.POST.get('pcf_serviceList_suppFeat-{ix}'.format(ix=i))
        if suppFeat == 'None':
            serviceList.append({"serviceName": serviceName})
        else:
            serviceList.append({"serviceName": serviceName, "suppFeat": suppFeat})
    # --- End of supportTaiList --- #    

    dataConfig = {
        "info":{
            "version":"1.0.0",
            "description":"NRF initial local configuration"
        },
        "configuration":{
            "pcfName": pcfName,
            "sbi": sbi,
            "timeFormat": timeFormat,
            "defaultBdtRefId":defaultBdtRefId,
            "nrfUri":nrfUri,
            "serviceList": serviceList
        }
    }


    # Save dictionary of inputs a key:value for reset button
    myclient = pymongo.MongoClient(connectionToMongo)
    # mydb = myclient['pcf']
    # mycol = mydb["config"]
    # x = mycol.delete_one({"_id": "pcf"})
    # mycol.insert_one({"_id": "pcf", "data": queryDict})


    if PressedButton == 'Submit':
        data = request.POST.dict()
        configWriter(dataConfig, yamlConfigPath, fileName)

        with open(yamlConfigPath + fileName) as fileConfig:
            docIn = yaml.load(fileConfig, Loader=yaml.BaseLoader)
        # Save userinput for later use after reload
        mydb = myclient['pcf']
        mycol = mydb["config"]
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "pcf": dataConfig})

    elif PressedButton == 'Reset':
        mydb = myclient['pcf']
        # reset id=2 value and replace with id=1
        mycol = mydb["config"]
        tempdata = mycol.find_one({"_id": 1}, {"pcf":1, "_id":0})
        tempdata = tempdata['pcf']
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "pcf": tempdata})

        Defaultdata = mycol.find_one({"_id": "pcf"}, {"_id": 0, "data": 1})
        data = Defaultdata.get('data')
        del data['PressedButton']
        del data['csrfmiddlewaretoken']

        updatedData = configLoader(yamlConfigPath, BasefileName)
        configWriter(updatedData, yamlConfigPath, fileName)
    myclient.close()
    return JsonResponse(data)
# ------------------------------------------------------------------------------

def upfUpdater(request):
    # yamlUpdater function goes here #
    BasefileName = 'upfcfg.test' # name of reference file
    fileName = 'upfcfg.test.yaml'
    yamlConfigPath = path.join(settings.BASE_DIR, 'yamlConfigFiles/')

    PressedButton = request.POST.get('PressedButton')

    upfName = request.POST.get('upfName')
    debugLevel = request.POST.get('debugLevel')
    ReportCaller = request.POST.get('ReportCaller')

    queryDict = request.POST.dict()
    keysInData = queryDict.keys()
    

    # --- Start of pfcp --- #
    upf_pfcpCount = len([x for x in keysInData if "upf_pfcp" in x])
    pfcp = []
    for i in range(0, upf_pfcpCount):
        pfcp_elem = request.POST.get('upf_pfcp-{ix}'.format(ix=i))
        if PressedButton == 'Submit':
            pfcp_elem = eval(pfcp_elem)
        pfcp.append(pfcp_elem)
    # --- End of pfcp --- #

    # --- Start of gtpu --- #
    upf_gtpuCount = len([x for x in keysInData if "upf_gtpu" in x])
    gtpu = []
    for i in range(0, upf_gtpuCount):
        gtpu_elem = request.POST.get('upf_gtpu-{ix}'.format(ix=i))
        if PressedButton == 'Submit':
            gtpu_elem = eval(gtpu_elem)
        gtpu.append(gtpu_elem)
    # --- End of gtpu --- #



    # --- Start of dnn_list --- #
    upf_dnn_listCount = len([x for x in keysInData if "upf_dnn_list" in x])
    dnn_list = []
    for i in range(0, upf_dnn_listCount):
        dnn_list_elem = request.POST.get('upf_dnn_list-{ix}'.format(ix=i))
        if PressedButton == 'Submit':
            dnn_list_elem = eval(dnn_list_elem)
        dnn_list.append(dnn_list_elem)
    # --- End of dnn_list --- #


    dataConfig = {
        "info":{
            "version":"1.0.0",
            "description":"UPF configuration"
        },
        "configuration":{
            "debugLevel": debugLevel,
            "ReportCaller": ReportCaller,
            "pfcp": pfcp,
            "gtpu": gtpu,
            "dnn_list": dnn_list
        }
    }


    # Save dictionary of inputs a key:value for reset button
    myclient = pymongo.MongoClient(connectionToMongo)
    # mydb = myclient['upf']
    # mycol = mydb["config"]
    # x = mycol.delete_one({"_id": "upf"})
    # mycol.insert_one({"_id": "upf", "data": queryDict})


    if PressedButton == 'Submit':
        data = request.POST.dict()
        configWriter(dataConfig, yamlConfigPath, fileName)

        with open(yamlConfigPath + fileName) as fileConfig:
            docIn = yaml.load(fileConfig, Loader=yaml.BaseLoader)
        # Save userinput for later use after reload
        mydb = myclient['upf']
        mycol = mydb["config"]
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "upf": dataConfig})

    elif PressedButton == 'Reset':
        mydb = myclient['upf']
        # reset id=2 value and replace with id=1
        mycol = mydb["config"]
        tempdata = mycol.find_one({"_id": 1}, {"upf":1, "_id":0})
        tempdata = tempdata['upf']
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "upf": tempdata})

        Defaultdata = mycol.find_one({"_id": "upf"}, {"_id": 0, "data": 1})
        data = Defaultdata.get('data')
        del data['PressedButton']
        del data['csrfmiddlewaretoken']

        updatedData = configLoader(yamlConfigPath, BasefileName)
        configWriter(updatedData, yamlConfigPath, fileName)
    
    myclient.close()
    return JsonResponse(data)

# ------------------------------------------------------------------------------

def nssfUpdater(request):
    # yamlUpdater function goes here #
    BasefileName = 'nssfcfg' # name of reference file
    fileName = 'nssfcfg.conf'
    yamlConfigPath = path.join(settings.BASE_DIR, 'yamlConfigFiles/')

    PressedButton = request.POST.get('PressedButton')
    
    nssfName =  request.POST.get('nssfName')
    sbi_scheme = request.POST.get('sbi_scheme')
    sbi_registerIPv4 = request.POST.get('sbi_registerIPv4')
    sbi_bindingIPv4 = request.POST.get('sbi_bindingIPv4')
    sbi_port = request.POST.get('sbi_port')
    sbi = {
        "scheme": sbi_scheme,
        "registerIPv4": sbi_registerIPv4,
        "bindingIPv4": sbi_bindingIPv4,
        "port": sbi_port
    }
    serviceNameList = request.POST.get('serviceNameList')
    nrfUri = request.POST.get('nrfUri')
    supportedPlmnList = request.POST.get('supportedPlmnList')

    queryDict = request.POST.dict()
    keysInData = queryDict.keys()
    




    # --- Start of supportedNssaiInPlmnList --- #
    nssf_supportedNssaiInPlmnListCount = len([x for x in keysInData if "nssf_supportedNssaiInPlmnList_plmnId" in x])
    supportedNssaiInPlmnList = []
    for i in range(0, nssf_supportedNssaiInPlmnListCount):
        plmnId = request.POST.get('nssf_supportedNssaiInPlmnList_plmnId-{ix}'.format(ix=i))
        supportedSnssaiList = request.POST.get('nssf_supportedNssaiInPlmnList_supportedSnssaiList-{ix}'.format(ix=i))

        if PressedButton == 'Submit':
            plmnId = eval(plmnId)
            supportedSnssaiList = eval(supportedSnssaiList)
        # print(supportedSnssaiList)
        supportedNssaiInPlmnList.append({"plmnId": plmnId, "supportedSnssaiList": supportedSnssaiList})
    # --- End of supportedNssaiInPlmnList --- #


    # --- Start of nsiList --- #
    nssf_nsiListCount = len([x for x in keysInData if "nssf_nsiList_snssai" in x])
    nsiList = []
    for i in range(0, nssf_nsiListCount):
        snssai = request.POST.get('nssf_nsiList_snssai-{ix}'.format(ix=i))
        nsiInformationList = request.POST.get('nssf_nsiList_nsiInformationList-{ix}'.format(ix=i))
        if PressedButton == 'Submit':
            snssai = eval(snssai)
            nsiInformationList = eval(nsiInformationList)
        nsiList.append({'snssai': snssai, 'nsiInformationList': nsiInformationList})
    # --- End of nsiList --- #

    # --- Start of amfSetList --- #
    amfSetList = []
    nssf_amfSetListCount = len([x for x in keysInData if "nssf_amfSetList_amfSetId-" in x])
    for i in range(0, nssf_amfSetListCount):
        amfSetId = request.POST.get('nssf_amfSetList_amfSetId-{ix}'.format(ix=i))
        amfList = request.POST.get('nssf_amfSetList_amfList-{ix}'.format(ix=i))
        if PressedButton == 'Submit':
            amfList = eval(amfList)
        nrfAmfSet = request.POST.get('nssf_amfSetList_nrfAmfSet-{ix}'.format(ix=i))
        nssf_amfSetList_supportedNssaiAvailabilityDataCount = int(request.POST.get('nssf_amfSetList_supportedNssaiAvailabilityDataCount-{ix}'.format(ix=i)))
        supportedNssaiAvailabilityData = []
        for j in range(0, nssf_amfSetList_supportedNssaiAvailabilityDataCount):
            nssf_tai = request.POST.get('nssf_amfSetList_supportedNssaiAvailabilityData_tai-{ix}-{jx}'.format(ix=i, jx=j))
            nssf_supportedSnssaiList = request.POST.get('nssf_amfSetList_supportedNssaiAvailabilityData_supportedSnssaiList-{ix}-{jx}'.format(ix=i, jx=j))
            if PressedButton == 'Submit':
                nssf_tai = eval(nssf_tai)  
                nssf_supportedSnssaiList = eval(nssf_supportedSnssaiList)
            supportedNssaiAvailabilityData.append({'tai': nssf_tai, 'supportedSnssaiList': nssf_supportedSnssaiList})

        
        if amfList != "null":
            amfSetList.append({
                'amfSetId': amfSetId,
                'amfList': amfList,
                'nrfAmfSet': nrfAmfSet,
                'supportedNssaiAvailabilityData': supportedNssaiAvailabilityData,
            })
        else:
            amfSetList.append({
                'amfSetId': amfSetId,
                'nrfAmfSet': nrfAmfSet,
                'supportedNssaiAvailabilityData': supportedNssaiAvailabilityData,
            })
    # --- End of amfSetList --- #
    

    # --- Start of amfList --- #
    amfList = []
    nssf_amfListCount = len([x for x in keysInData if "nssf_amfList_nfId-" in x])
    for i in range(0, nssf_amfListCount):
        nfId = request.POST.get('nssf_amfList_nfId-{ix}'.format(ix=i))
        nssf_amfList_supportedNssaiAvailabilityDataCount = int(request.POST.get('nssf_amfList_supportedNssaiAvailabilityDataCount-{ix}'.format(ix=i)))
        supportedNssaiAvailabilityData = []
        for j in range(0, nssf_amfList_supportedNssaiAvailabilityDataCount):
            nssf_tai = request.POST.get('nssf_amfList_supportedNssaiAvailabilityData_tai-{ix}-{jx}'.format(ix=i, jx=j))
            nssf_supportedSnssaiList = request.POST.get('nssf_amfList_supportedNssaiAvailabilityData_supportedSnssaiList-{ix}-{jx}'.format(ix=i, jx=j))
            
            if PressedButton == 'Submit':
                nssf_tai = eval(nssf_tai)
                nssf_supportedSnssaiList = eval(nssf_supportedSnssaiList)
            supportedNssaiAvailabilityData.append({'tai': nssf_tai, 'supportedSnssaiList': nssf_supportedSnssaiList})
        
        amfList.append({'nfId': nfId, 'supportedNssaiAvailabilityData': supportedNssaiAvailabilityData})
    # --- End of amfList --- #

    
    # --- Start of taList --- #
    taList = []
    nssf_taListCount = len([x for x in keysInData if "nssf_taList_tai-" in x])
    for i in range(0, nssf_taListCount):
        nssf_tai = request.POST.get('nssf_taList_tai-{ix}'.format(ix=i))
        accessType = request.POST.get('nssf_taList_accessType-{ix}'.format(ix=i))
        supportedSnssaiList = request.POST.get('nssf_taList_supportedSnssaiList-{ix}'.format(ix=i))        

        if PressedButton == 'Submit':
            nssf_tai = eval(nssf_tai)
            supportedSnssaiList = eval(supportedSnssaiList)
        restrictedSnssaiList = request.POST.get('nssf_taList_restrictedSnssaiList-{ix}'.format(ix=i))


        if restrictedSnssaiList != "None":
            taList.append({
                'tai': nssf_tai,
                'accessType': accessType,
                'supportedSnssaiList': supportedSnssaiList,
                'restrictedSnssaiList': eval(restrictedSnssaiList)
            })
        else:
            taList.append({
                'tai': nssf_tai,
                'accessType': accessType,
                'supportedSnssaiList': supportedSnssaiList,
            })
    # --- End of taList --- #


    # --- Start of mappingListFromPlmn --- #
    mappingListFromPlmn = []
    nssf_mappingListFromPlmnCount = len([x for x in keysInData if "nssf_mappingListFromPlmn_operatorName-" in x])
    for i in range(0, nssf_mappingListFromPlmnCount):
        operatorName = request.POST.get('nssf_mappingListFromPlmn_operatorName-{ix}'.format(ix=i))
        homePlmnId = request.POST.get('nssf_mappingListFromPlmn_homePlmnId-{ix}'.format(ix=i))

        if PressedButton == 'Submit':
            homePlmnId = eval(homePlmnId)
        nssf_mappingListFromPlmn_mappingOfSnssaiCount = int(request.POST.get('nssf_mappingListFromPlmn_mappingOfSnssaiCount-{ix}'.format(ix=i)))
        mappingOfSnssai = []
        for j in range(0, nssf_mappingListFromPlmn_mappingOfSnssaiCount):
            mappingOfSnssaielement = request.POST.get('nssf_mappingListFromPlmn_mappingOfSnssai-{ix}-{jx}'.format(ix=i, jx=j))
            if PressedButton == 'Submit':
                mappingOfSnssaielement = eval(mappingOfSnssaielement)
            mappingOfSnssai.append(mappingOfSnssaielement)
        
        mappingListFromPlmn.append({'operatorName': operatorName, 'homePlmnId': homePlmnId, 'mappingOfSnssai': mappingOfSnssai})
    # --- End of mappingListFromPlmn --- #

    dataConfig = {
        "info":{
            "version":"1.0.0",
            "description":"NSSF initial local configuration"
        },
        "configuration":{
            "nssfName": nssfName,
            "sbi": sbi,
            "serviceNameList": serviceNameList,
            "nrfUri": nrfUri,
            "supportedPlmnList": supportedPlmnList,
            "supportedNssaiInPlmnList": supportedNssaiInPlmnList,
            "nsiList": nsiList,
            "amfSetList": amfSetList,
            "amfList": amfList,
            "taList": taList,
            "mappingListFromPlmn": mappingListFromPlmn
        }
    }
    

    # Save dictionary of inputs a key:value for reset button
    myclient = pymongo.MongoClient(connectionToMongo)
    # mydb = myclient['nssf']
    # mycol = mydb["config"]
    # x = mycol.delete_one({"_id": "nssf"})
    # mycol.insert_one({"_id": "nssf", "data": queryDict})

    if PressedButton == 'Submit':
        data = request.POST.dict()
        configWriter(dataConfig, yamlConfigPath, fileName)

        with open(yamlConfigPath + fileName) as fileConfig:
            docIn = yaml.load(fileConfig, Loader=yaml.BaseLoader)
        print(dataConfig)
        # Save userinput for later use after reload
        mydb = myclient['nssf']
        mycol = mydb["config"]
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "nssf": dataConfig})

    elif PressedButton == 'Reset':
        mydb = myclient['nssf']

        # reset id=2 value and replace with id=1
        mycol = mydb["config"]
        tempdata = mycol.find_one({"_id": 1}, {"nssf":1, "_id":0})
        tempdata = tempdata['nssf']
        x = mycol.delete_one({"_id": 2})
        x = mycol.insert_one({"_id": 2, "nssf": tempdata})

        Defaultdata = mycol.find_one({"_id": "nssf"}, {"_id": 0, "data": 1})
        data = Defaultdata.get('data')
        del data['PressedButton']
        del data['csrfmiddlewaretoken']

        updatedData = configLoader(yamlConfigPath, BasefileName)
        configWriter(updatedData, yamlConfigPath, fileName)
    return JsonResponse(data)

 
# ------------------------------------------------------------------------------


def nodeLogLevelUpdater(request):

    client = pymongo.MongoClient(connectionToMongo)
    db = client['free5GC']
    col = db["config"]
    result = col.find_one({"_id":2}, {"_id":0})
    nodes = result['free5gc']['logger']
    NumOfNodes = len(result['free5gc']['logger'])

    keys = list(nodes.keys())
    dataTotal = []
    for key in keys[:-1]:
        reformatDict = {
            "node": key,
            "debugLevel": nodes.get(key).get('debugLevel'),
            "ReportCaller": nodes.get(key).get('ReportCaller'),
            }
        dataTotal.append(reformatDict)

    

    start = int(request.POST.get('start', 1))
    length = int(request.POST.get('length', 8))
    draw = int(request.POST.get('draw', 1))
    search = request.POST.get('search[value]', '')

    FilteredData = dataTotal
    if len(search) != 0:
        FilteredData = []
        for item in dataTotal:
            if search in item['node'] or search in item['debugLevel'] or search in item['ReportCaller']:
                FilteredData.append(item)

        DataForTablePaginated = FilteredData[start:start+length]

    recordsTotal = len(dataTotal)
    recordsFiltered = len(FilteredData)
    DataForTablePaginated = FilteredData[start:start+length]
    data = {
        "draw": draw,
        "recordsTotal": recordsTotal,
        "recordsFiltered": recordsFiltered,
        "data": DataForTablePaginated
    }



    # print(nodes)
    # data = {}
    client.close()
    return JsonResponse(data)



def nodeLogLevelEditor(request):
    client = pymongo.MongoClient(connectionToMongo)
    db = client['free5GC']
    col = db["config"]    

    node = request.POST.get('node')
    debugLevel = request.POST.get('debugLevel')
    ReportCaller = request.POST.get('ReportCaller')

    dataToMongo = {
            "debugLevel": debugLevel,
            "ReportCaller": ReportCaller,
        }


    data = {
            "node": node,
            "debugLevel": debugLevel,
            "ReportCaller": ReportCaller,
        }


    x = col.update_one({"_id":2}, {'$set': {"free5gc.logger.{}".format(node): dataToMongo}})
    result = col.find_one({"_id": 2}, {"_id": 0})
    dataConfig = result['free5gc']

    BasefileName = 'free5GC' # name of reference file
    fileName = 'free5GC.conf'
    yamlConfigPath = path.join(settings.BASE_DIR, 'yamlConfigFiles/')

    configWriter(dataConfig, yamlConfigPath, fileName)

    # data = {}
    return JsonResponse(data)



def nodeLogLevelReset(request):
    client = pymongo.MongoClient(connectionToMongo)
    db = client['free5GC']
    col = db["config"]

    PressedButton = request.POST.get('PressedButton')

    defaultValues = col.find_one({"_id": 1}, {"_id":0})
    x = col.delete_one({"_id": 2})
    x = col.insert_one({"_id": 2, "free5gc": defaultValues['free5gc']})
    
    result = col.find_one({"_id": 1}, {"_id": 0})
    dataConfig = result['free5gc']

    BasefileName = 'free5GC' # name of reference file
    fileName = 'free5GC.conf'
    yamlConfigPath = path.join(settings.BASE_DIR, 'yamlConfigFiles/')

    configWriter(dataConfig, yamlConfigPath, fileName)

    data = {}
    client.close()
    return JsonResponse(data)    



# ------------------------------------------------------------------------------
from traces.models import GeneratedTracesModel
from fiveGApp.models import RunScenariosModel
from django.db import IntegrityError

def ScenariosRun(request):
    runScenarioSelectId = request.POST.get("runScenarioSelectId")
    TestName = request.POST.get("TestName")
    scenarioName = RunScenariosModel.objects.get(id=runScenarioSelectId).name
    NumOfTraces = GeneratedTracesModel.objects.all().count()
    MaxPossibleTraces = 40

    fiveGTestPath = path.join(settings.BASE_DIR, '../../free5gc/')
    yamlConfigPath = path.join(settings.BASE_DIR, 'yamlConfigFiles/')
    
    fiveGConfigPath1 = path.join(settings.BASE_DIR, '../../free5gc/config/')
    configFileList1 = ['amfcfg.conf', 'ausfcfg.conf', 'nrfcfg.conf', 'nssfcfg.conf','pcfcfg.conf', 'udmcfg.conf', 'udrcfg.conf', 'free5GC.conf']
    
    fiveGConfigPath2 = path.join(settings.BASE_DIR, '../../free5gc/config/test/')
    configFileList2 = ['smfcfg.single.test.conf']

    fiveGConfigPath3 = path.join(settings.BASE_DIR, '../../free5gc/src/upf/build/config/')
    configFileList3 = ['upfcfg.test.yaml']


    for confFile in configFileList1:
        system('cp '+ yamlConfigPath + confFile +' '+ fiveGConfigPath1)

    for confFile in configFileList2:
        system('cp '+ yamlConfigPath + confFile +' '+ fiveGConfigPath2)

    for confFile in configFileList3:
        system('cp '+ yamlConfigPath + confFile +' '+ fiveGConfigPath3)

    if NumOfTraces < MaxPossibleTraces:
        try:
            realFileName = TestName + '.pcap'
            GeneratedTracesModel.objects.create(TestName=TestName, realFileName= realFileName, scenarioName=scenarioName)
            data = {"status": True, "error":"", "ScenarioName": scenarioName}
            nameInScript = list(RunScenariosModel.objects.filter(name=scenarioName).values_list('nameInScript',flat=True))[0]
            TraceSeqDiagramPath = path.join(settings.BASE_DIR, 'analyzer/traces/')
            traceFileName = TraceSeqDiagramPath + TestName + '.pcap'
            print(traceFileName)
            # ************************************************************************
            # for permision to run tcpdump without sudo run below code
            # sudo ../.env/bin/python3 manage.py runserver 0.0.0.0:8080
            # sudo chmod 777 /usr/sbin/tcpdump
            # ************************************************************************
            p = subprocess.Popen(["sudo", "timeout","35","tcpdump","-U", "-i", "any", "-s0","-w", traceFileName],stdout=subprocess.PIPE)
            chdir(fiveGTestPath)
            system('cat /dev/null > logOfScenario.log')
            system('sudo mongo hexout --eval "db.dropDatabase()"')
            system('sudo timeout 35 ./test.sh {ScenarioInTest} | tee logOfScenario.log'.format(ScenarioInTest=nameInScript))
            # system('./test.sh {ScenarioInTest} > logOfScenario.log'.format(ScenarioInTest=nameInScript))
            # system('timeout 30 ./test.sh {ScenarioInTest}'.format(ScenarioInTest=nameInScript))
            print(p.pid)
            cmd = 'sudo kill -2 {pid}'.format(pid=str(p.pid))
            print(str(p.pid))
            # ************************************************************************
            # for permision to run tcpdump without sudo run below code
            # sudo ../.env/bin/python3 manage.py runserver 0.0.0.0:8080
            # sudo chmod 777 /usr/sbin/tcpdump
            # ************************************************************************
            # p.terminate()
            system(cmd)
            system("sudo kill -9 $(ps -aux | grep 'test' | awk '{print $2}')")
            system("sudo kill -9 $(ps -aux | grep 'tcpdump' | awk '{print $2}')")




            # if p.poll() == None:
            #     print("tcpdump process is still alive")
        except IntegrityError:
            data = {"status": False, "error": "Duplicate name for "+scenarioName}
    else:
        data = {"status": False, "error": "Reached maximum number of traces"}
    return JsonResponse(data)


# ------------------------------------------------------------------------------
import re

def LogHandler(request):
    logPath = path.join(settings.BASE_DIR, '../../free5gc/')
    fileName = "logOfScenario.log"
    system("sed -i -e 's/free5gc/Hexout/g'  -e 's/free5GC/HexOut/g' logOfScenario.log")
    logData=[]
    with open(logPath + fileName,'r', encoding = "ISO-8859-1") as fp:
        fData = fp.readlines()
    for line in fData:
        DateOfLine = line[0:20]
        if DateOfLine[-1] == 'Z':
            regex = r"\s(\[.*\])(\[.*\])(\[\S+\])"
            matches = [[aa.group(1), aa.group(2), aa.group(3), aa.end()] for aa in re.finditer(regex, line)]
            logData.append('<div class="row mx-2"> <p class="my-0" style="color: yellow">{i}</p><p class="my-0 mx-2" style="color: #8FF925 "> ---> {j}</p><p class="my-0" style="color: #E74C3C "> {k} </p><p class="my-0" style="color: #D171E6 "> {l}</p><p class="my-0">  {m}</p></div>'.format(i=DateOfLine, j=matches[0][0], k=matches[0][1], l=matches[0][2], m=line[matches[0][3]+5:-1]))
        else:
            logData.append('<div class="row mx-2" style="color: white">{i}</div>'.format(i=line))

    response = HttpResponse(logData)
    return response
