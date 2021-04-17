import yaml

class YamlDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(YamlDumper, self).increase_indent(flow, False)

def configLoader(Path, fileName):
    '''
        insert path of a yaml config file
    '''
    with open(Path + fileName) as fileConfig:
        docIn = yaml.load(fileConfig, Loader=yaml.BaseLoader)
    return docIn


def configWriter(docToYaml, Path, fileName):
    '''
        write dictionary into a yaml file
        docToYaml is dict
        path, fileName are string
    '''
    documents = yaml.dump(docToYaml, Dumper=YamlDumper, default_flow_style=False,sort_keys=False)
    # documents = yaml.dump(docToYaml)
    documents = documents.replace("'","")
    with open(Path + fileName, 'w') as fileConfig:
        fileConfig.write(documents)
        fileConfig.close()


def UpdateDoc(data, IndexLists):
    '''
        A function to serialize keys retrieved from UpdateDoc function.
        for example change
        IndexList, = [['configuration', 'servedGuamiList', 0, 'plmnId', 'mcc', '555'], [..]] including value at the end
        to
        CommandString = "data['configuration']['servedGuamiList'][0]['plmnId']['mcc'] = 123"
        then to exec(CommandString)
    '''
    for IndexList in IndexLists:
        CommandString = 'data'
        for val in IndexList[:-1]:
            if type(val) is str:
                CommandString = CommandString + "['%s']" %val
            elif type(val) is int:
                CommandString = CommandString + "[%s]" %val
        CommandString = CommandString + " = '%s'" %str(IndexList[-1])
        exec(CommandString)
    return data



def findKeyParents(data, newUpdate):
    result = []
    def finder(data, newUpdate, keyParents = []):
        Cond = len(data.keys())
        for key, value in data.items():
            keyParents.append(key)
            if key == list(newUpdate.keys())[0]:
                IndexAddress = []
                for i in keyParents:
                    if 'HexOutElementIndexList' in i:
                        IndexAddress.append(int(i.strip('HexOutElementIndexList')))
                    else:
                        IndexAddress.append(i)
                IndexAddress.append(list(newUpdate.values())[0])
                result.append(IndexAddress)
                keyParents.pop()
            else:
                if type(value) is dict:
                    finder(value, newUpdate, keyParents)
                elif type(value) is list:
                    count = 0
                    for element in value:
                        count = count + 1
                        if type(element) is dict:
                            keyParents.append("HexOutElementIndexList"+str(count-1))
                            finder(element, newUpdate, keyParents)
            keyParents.pop()

    finder(data, newUpdate, keyParents = [])
    return result
