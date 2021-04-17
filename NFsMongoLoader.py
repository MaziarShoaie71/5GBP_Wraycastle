import pymongo
import yaml

myclient = pymongo.MongoClient('mongodb://127.0.0.1:27017/')

amffileName="/vagrant/config/amfcfg.conf"
ausffileName="/vagrant/config/ausfcfg.conf"
nrffileName="/vagrant/config/nrfcfg.conf"
nssffileName="fiveGbp/yamlConfigFiles/nssfcfg.conf"
pcffileName="/vagrant/config/pcfcfg.conf"
smffileName="/vagrant/config/smfcfg.conf"
udmfileName="/vagrant/config/udmcfg.conf"
upffileName="/vagrant/upfcfg.test.yaml"
free5GCName = "/vagrant/config/free5GC.conf"

# ---------------------------------------------------------------# 

with open(amffileName) as fileConfig:
    docIn = yaml.load(fileConfig, Loader=yaml.BaseLoader)

mydb = myclient['amf']
mycol = mydb["config"]
x = mycol.delete_one({"_id":1})
x = mycol.delete_one({"_id":2})
x = mycol.insert_one({"_id": 1, "amf": docIn})
x = mycol.insert_one({"_id": 2, "amf": docIn})

# ---------------------------------------------------------------# 

with open(ausffileName) as fileConfig:
    docIn = yaml.load(fileConfig, Loader=yaml.BaseLoader)

mydb = myclient['ausf']
mycol = mydb["config"]
x = mycol.delete_one({"_id":1})
x = mycol.delete_one({"_id":2})
x = mycol.insert_one({"_id": 1, "ausf": docIn})
x = mycol.insert_one({"_id": 2, "ausf": docIn})

# ---------------------------------------------------------------# 

with open(nrffileName) as fileConfig:
    docIn = yaml.load(fileConfig, Loader=yaml.BaseLoader)

mydb = myclient['nrf']
mycol = mydb["config"]
x = mycol.delete_one({"_id":1})
x = mycol.delete_one({"_id":2})
x = mycol.insert_one({"_id": 1, "nrf": docIn})
x = mycol.insert_one({"_id": 2, "nrf": docIn})

# ---------------------------------------------------------------# 

with open(nssffileName) as fileConfig:
    docIn = yaml.load(fileConfig, Loader=yaml.BaseLoader)

mydb = myclient['nssf']
mycol = mydb["config"]
x = mycol.delete_one({"_id":1})
x = mycol.delete_one({"_id":2})
x = mycol.insert_one({"_id": 1, "nssf": docIn})
x = mycol.insert_one({"_id": 2, "nssf": docIn})

# ---------------------------------------------------------------# 

with open(pcffileName) as fileConfig:
    docIn = yaml.load(fileConfig, Loader=yaml.BaseLoader)

mydb = myclient['pcf']
mycol = mydb["config"]
x = mycol.delete_one({"_id":1})
x = mycol.delete_one({"_id":2})
x = mycol.insert_one({"_id": 1, "pcf": docIn})
x = mycol.insert_one({"_id": 2, "pcf": docIn})

# ---------------------------------------------------------------# 

with open(smffileName) as fileConfig:
    docIn = yaml.load(fileConfig, Loader=yaml.BaseLoader)

mydb = myclient['smf']
mycol = mydb["config"]
x = mycol.delete_one({"_id":1})
x = mycol.delete_one({"_id":2})
x = mycol.insert_one({"_id": 1, "smf": docIn})
x = mycol.insert_one({"_id": 2, "smf": docIn})

# ---------------------------------------------------------------# 

with open(udmfileName) as fileConfig:
    docIn = yaml.load(fileConfig, Loader=yaml.BaseLoader)

mydb = myclient['udm']
mycol = mydb["config"]
x = mycol.delete_one({"_id":1})
x = mycol.delete_one({"_id":2})
x = mycol.insert_one({"_id": 1, "udm": docIn})
x = mycol.insert_one({"_id": 2, "udm": docIn})

# ---------------------------------------------------------------# 

with open(upffileName) as fileConfig:
    docIn = yaml.load(fileConfig, Loader=yaml.BaseLoader)

mydb = myclient['upf']
mycol = mydb["config"]
x = mycol.delete_one({"_id":1})
x = mycol.delete_one({"_id":2})
x = mycol.insert_one({"_id": 1, "upf": docIn})
x = mycol.insert_one({"_id": 2, "upf": docIn})


# ---------------------------------------------------------------# 

with open(free5GCName) as fileConfig:
    docIn = yaml.load(fileConfig, Loader=yaml.BaseLoader)

mydb = myclient['free5GC']
mycol = mydb["config"]
x = mycol.delete_one({"_id":1})
x = mycol.delete_one({"_id":2})
x = mycol.insert_one({"_id": 1, "free5gc": docIn})
x = mycol.insert_one({"_id": 2, "free5gc": docIn})

