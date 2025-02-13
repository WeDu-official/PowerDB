class inner_functions_class():
    def __init__(self):
        pass
    def get_the_word_inbetween(self,text, start_char, end_char):
        start_index = text.find(start_char)
        if start_index == -1:
            return None
        end_index = text.find(end_char, start_index + 1)
        if end_index == -1 or end_index <= start_index:
            return None
        return text[start_index + 1:end_index]
    def count_occurrences(self,word:str, string:str):
        count = 0
        word_len = len(word)
        text_len = len(string)

        for i in range(text_len - word_len + 1):  # Iterate through possible start positions
            if string[i:i + word_len] == word:
                count += 1

        return count

    def get_line_of_phrase_in_text(self,text, phrase):
        lines = text.splitlines()

        for line in lines:
            if phrase in line:
                # Replace all occurrences of the phrase with an empty string
                line_without_phrase = line.replace(phrase, "")
                return line_without_phrase.strip()  # Remove extra whitespace

        return None

    def modify_line_containing_word(self,text, word, new_line_content):
        lines = text.splitlines()
        line_number = -1  # Initialize to -1 to indicate word not found yet

        for i, line in enumerate(lines):
            if word in line:
                line_number = i

        if line_number != -1:
            lines[line_number] = new_line_content
            return "\n".join(lines)  # Rejoin the lines with newline characters
        else:
            return text  # Return original text if word not found
inner_functions = inner_functions_class()
class create_class():
    def __init__(self):
        pass
    def makeDB(self,newfile:str):
        if newfile[-4:] == '.pdb' or newfile[-4:] == '.PDB':
            makeDBX = open(newfile,'x')
        else:
            makeDBX = open(f'{newfile}.pdb', 'x')
        makeDBX.write('#POWER_DB')
        makeDBX.close()
    def makecontainer(self,file:str):
        scancontainers = open(file,'r')
        r = scancontainers.read()
        scancontainers.close()
        num = inner_functions.count_occurrences('$<', r)
        makecontainer = open(file, 'a')
        if num == 0:
            makecontainer.write(f"\n$<0>")
        else:
            makecontainer.write(f"\n$<{num}>")
        makecontainer.close()
    def maketable(self,file:str):
        scancontainers = open(file, 'r')
        r = scancontainers.read()
        scancontainers.close()
        num = inner_functions.count_occurrences('&<', r)
        makecontainer = open(file, 'a')
        if num == 0:
            makecontainer.write(f"\n&<0>")
        else:
            makecontainer.write(f"\n&<{num}>")
        makecontainer.close()
create = create_class()
class container_data_class():
    def __init__(self):
        pass
    def insert(self,file:str,data:str,address=None):
        if address is None:
            address = []
        containerid = address[0]
        sectorid = address[1]
        makecontainer = open(file, 'a')
        makecontainer.write(f"\n!<[{containerid},{sectorid}],{data}>!")
        makecontainer.close()
    def read(self,file:str,address=None):
        if address is None:
            address = []
        containerid = address[0]
        sectorid = address[1]
        scancontainers = open(file, 'r')
        r = scancontainers.read()
        scancontainers.close()
        data = ""
        if f'!<[{containerid},{sectorid}]' in r:
            data = inner_functions.get_line_of_phrase_in_text(r,f'!<[{containerid},{sectorid}]')[1:-2]
        return data
    def edit(self,file:str,data:str,address=None):
        if address is None:
            address = []
        containerid = address[0]
        sectorid = address[1]
        scancontainers = open(file, 'r')
        r = scancontainers.read()
        scancontainers.close()
        actdata = inner_functions.modify_line_containing_word(r,f'!<[{containerid},{sectorid}]',f'!<[{containerid},{sectorid}],{data}>!')
        rccontainers = open(file, 'w')
        rccontainers.write('')
        rccontainers.close()
        editcontainers = open(file, 'w')
        editcontainers.write(actdata)
        editcontainers.close()
    def readsectors(self,file:str,containerid:int,limit:int=100):
        scancontainers = open(file, 'r')
        r = scancontainers.read()
        scancontainers.close()
        data = []
        for i in range(limit):
            if f'!<[{containerid},{i}]' in r:
                data.append(inner_functions.get_line_of_phrase_in_text(r, f'!<[{containerid},{i}]')[1:-2])
        return data
    def numbercontainers(self, file: str,plogic:bool=False):
        scancontainers = open(file, 'r')
        r = scancontainers.read()
        scancontainers.close()
        if plogic is False:
            return inner_functions.count_occurrences('$<', r)
        else:
            return inner_functions.count_occurrences('$<', r)-1
    def numbersectors(self, file: str,containerid:int,plogic:bool=False):
        scancontainers = open(file, 'r')
        r = scancontainers.read()
        scancontainers.close()
        if plogic is False:
            return inner_functions.count_occurrences(f'!<[{containerid}', r)
        else:
            return inner_functions.count_occurrences(f'!<[{containerid}', r)
    def delete(self,file:str,address=None):
        if address is None:
            address = []
        containerid = address[0]
        sectorid = address[1]
        scancontainers = open(file, 'r')
        r = scancontainers.read()
        scancontainers.close()
        actdata = inner_functions.modify_line_containing_word(r,f'!<[{containerid},{sectorid}]',f'')
        rccontainers = open(file, 'w')
        rccontainers.write('')
        rccontainers.close()
        editcontainers = open(file, 'w')
        lines = actdata.split('\n')
        non_empty_lines = [line for line in lines if line.strip() != '']
        actdatan = '\n'.join(non_empty_lines)
        editcontainers.write(actdatan)
        editcontainers.close()
container_data = container_data_class()
class table_data_class():
    def __init__(self):
        pass
    def insert(self,file:str,data:str,address=None):
        if address is None:
            address = []
        tableid = address[0]
        columnid = address[1]
        rowid = address[2]
        makecontainer = open(file, 'a')
        makecontainer.write(f"\n~<[{tableid};{columnid},{rowid}],{data}>~")
        makecontainer.close()
    def read(self,file:str,address=None):
        if address is None:
            address = []
        tableid = address[0]
        columnid = address[1]
        rowid = address[2]
        scancontainers = open(file, 'r')
        r = scancontainers.read()
        scancontainers.close()
        data = ""
        if f'~<[{tableid};{columnid},{rowid}]' in r:
            data = inner_functions.get_line_of_phrase_in_text(r,f'~<[{tableid};{columnid},{rowid}]')[1:-2]
        return data
    def readcolumns(self,file:str,address=None,limit:int=100):
        tableid = address[0]
        rowid = address[1]
        scancontainers = open(file, 'r')
        r = scancontainers.read()
        scancontainers.close()
        data = []
        for i in range(limit):
            if f'~<[{tableid};{i},{rowid}]' in r:
                data.append(inner_functions.get_line_of_phrase_in_text(r, f'~<[{tableid};{i},{rowid}]')[1:-2])
        return data
    def readrows(self,file:str,address=None,limit:int=100):
        tableid = address[0]
        columnid = address[1]
        scancontainers = open(file, 'r')
        r = scancontainers.read()
        scancontainers.close()
        data = []
        for i in range(limit):
            if f'~<[{tableid};{columnid},{i}]' in r:
                data.append(inner_functions.get_line_of_phrase_in_text(r, f'~<[{tableid};{columnid},{i}]')[1:-2])
        return data
    def numbertables(self,file:str,plogic:bool=False):
        scancontainers = open(file, 'r')
        r = scancontainers.read()
        scancontainers.close()
        if plogic is False:
            return inner_functions.count_occurrences('&<',r)
        else:
            return inner_functions.count_occurrences('&<', r)-1
    def numbercolumns(self,file:str,address=None,limit:int=100,cutnumber:int=0,strictmode:bool=False,plogic:bool=False):
        tableid = address[0]
        rowid = address[1]
        scancontainers = open(file, 'r')
        r = scancontainers.read()
        scancontainers.close()
        data = []
        numl = []
        cutsnumber = cutnumber
        kill = 0
        if strictmode is False:
            for i in range(limit):
                if f'~<[{tableid};{i},{rowid}]' in r:
                    data.append(f'~<[{tableid};{i},{rowid}]')
                else:
                    if kill == cutsnumber and cutsnumber > 0:
                        kill = 0
                        break
                    if cutsnumber > 0:
                        kill = kill + 1
        else:
            for i in range(limit):
                if f'~<[{tableid};{i},{rowid}]' in r:
                    data.append(f'~<[{tableid};{i},{rowid}]')
                else:
                    if kill == 1:
                        kill = 0
                        break
                    kill = kill + 1
        for i in range(limit):
            if f'~<[{tableid};{i},{rowid}]' in r:
                data.append(f'~<[{tableid};{i},{rowid}]')
        for k in data:
            numl.append(int(inner_functions.get_the_word_inbetween(k, ';', ',')))
        if plogic is False:
            return max(numl)+1
        else:
            return max(numl)
    def numberrows(self,file:str,address=None,limit:int=100,cutnumber:int=0,strictmode:bool=False,plogic:bool=False):
        tableid = address[0]
        columnid = address[1]
        scancontainers = open(file, 'r')
        r = scancontainers.read()
        scancontainers.close()
        data = []
        numl = []
        cutsnumber = cutnumber
        kill = 0
        if strictmode is False:
            for iu in range(limit):
                print(iu)
                if f'~<[{tableid};{columnid},{iu}]' in r:
                    data.append(f'~<[{tableid};{columnid},{iu}]')
                else:
                    if kill == cutsnumber and cutsnumber > 0:
                        kill = 0
                        break
                    if cutsnumber > 0:
                        kill = kill + 1
        else:
            for iu in range(limit):
                print(iu)
                if f'~<[{tableid};{columnid},{iu}]' in r:
                    data.append(f'~<[{tableid};{columnid},{iu}]')
                else:
                    if kill == 1:
                        kill = 0
                        break
                    kill = kill + 1
        for k in data:
            numl.append(int(inner_functions.get_the_word_inbetween(k, ',', ']')))
        if plogic is False:
            return max(numl)+1
        else:
            return max(numl)
    def totaltable(self,file:str,tableid:int,multilimit:bool=False,limita:int=100,limita2:int=100,cutnumber:int=0,lcutnumber:int=0,strictmode:bool=False,plogic:bool=False):
        scancontainers = open(file, 'r')
        r = scancontainers.read()
        scancontainers.close()
        limit = []
        if multilimit is False:
            limit.append(limita)
            limit.append(limita)
        else:
            limit.append(limita)
            limit.append(limita2)
        data = []
        numl1 = []
        numl2 = []
        kill = 0
        killm = 0
        cutsnumber = cutnumber
        lcutsnumber = lcutnumber
        if strictmode is False:
            if lcutsnumber > 0:
                for i in range(limit[0]):
                    if f'~<[{tableid};{i}' in r:
                        pass
                    else:
                        if killm == lcutsnumber:
                            break
                        if lcutsnumber > 0:
                            killm = killm + 1
                    for iu in range(limit[1]):
                        if f'~<[{tableid};{i},{iu}]' in r:
                            data.append(f'~<[{tableid};{i},{iu}]')
                        else:
                            if kill == cutsnumber and cutsnumber > 0:
                                kill = 0
                                break
                            if cutsnumber > 0:
                                kill = kill + 1
            else:
                for i in range(limit[0]):
                    for iu in range(limit[1]):
                        if f'~<[{tableid};{i},{iu}]' in r:
                            data.append(f'~<[{tableid};{i},{iu}]')
                        else:
                            if kill == cutsnumber and cutsnumber > 0:
                                kill = 0
                                break
                            if cutsnumber > 0:
                                kill = kill + 1
        else:
            for i in range(limit[0]):
                if f'~<[{tableid};{i}' in r:
                    pass
                else:
                    if killm == 1:
                        break
                    killm = killm + 1
                for iu in range(limit[1]):
                    if f'~<[{tableid};{i},{iu}]' in r:
                        data.append(f'~<[{tableid};{i},{iu}]')
                    else:
                        if kill == 1:
                            kill = 0
                            break
                        kill = kill + 1
        for k in data:
            numl1.append(int(inner_functions.get_the_word_inbetween(k,';',',')))
            numl2.append(int(inner_functions.get_the_word_inbetween(k, ',', ']')))
        if plogic is False:
            return [max(numl1)+1, max(numl2)+1]
        else:
            return [max(numl1), max(numl2)]
    def edit(self,file:str,data:str,address=None):
        if address is None:
            address = []
        tableid = address[0]
        columnid = address[1]
        rowid = address[2]
        scancontainers = open(file, 'r')
        r = scancontainers.read()
        scancontainers.close()
        actdata = inner_functions.modify_line_containing_word(r,f'~<[{tableid};{columnid},{rowid}]',f'~<[{tableid};{columnid},{rowid}],{data}>')
        rccontainers = open(file, 'w')
        rccontainers.write('')
        rccontainers.close()
        editcontainers = open(file, 'w')
        lines = actdata.split('\n')
        non_empty_lines = [line for line in lines if line.strip() != '']
        actdatan = '\n'.join(non_empty_lines)
        editcontainers.write(actdatan)
        editcontainers.close()
    def delete(self,file:str,address=None):
        if address is None:
            address = []
        tableid = address[0]
        columnid = address[1]
        rowid = address[2]
        scancontainers = open(file, 'r')
        r = scancontainers.read()
        scancontainers.close()
        actdata = inner_functions.modify_line_containing_word(r,f'~<[{tableid};{columnid},{rowid}]',f'')
        rccontainers = open(file, 'w')
        rccontainers.write('')
        rccontainers.close()
        editcontainers = open(file, 'w')
        lines = actdata.split('\n')
        non_empty_lines = [line for line in lines if line.strip() != '']
        actdatan = '\n'.join(non_empty_lines)
        editcontainers.write(actdatan)
        editcontainers.close()
table_data = table_data_class()
class other_class():
    def __init__(self):
        pass
    def clear(self,file:str):
        rccontainers = open(file, 'w')
        rccontainers.write('')
        rccontainers.close()
        accontainers = open(file, 'w')
        accontainers.write('#POWER_DB')
        accontainers.close()
    def check(self, file:str, itemtype:str, address=None):
        if address is None:
            address = []
        scancontainers = open(file, 'r')
        r = scancontainers.read()
        scancontainers.close()
        if itemtype.lower() == 'container':
            containerid = address[0]
            if f'$<{containerid}>' in r:
                return True
            else:
                return False
        if itemtype.lower() == 'table':
            tableid = address[0]
            if f'&<{tableid}>' in r:
                return True
            else:
                return False
        if itemtype.lower() == 'sector':
            containerid = address[0]
            sectorid = address[1]
            if f'!<[{containerid},{sectorid}]' in r:
                return True
            else:
                return False
        if itemtype.lower() == 'cell':
            tableid = address[0]
            columnid = address[1]
            rowid = address[2]
            if f'~<[{tableid};{columnid},{rowid}]' in r:
                return True
            else:
                return False
other = other_class()