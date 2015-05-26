#created by Xiangmin Xu to process census data
import os
import re
import logging

def handler(outf,annf,metaf):
    #print annf.readline()
    #get head from annf
    annf.readline() #first line is useless
    headlist = re.findall(r'(?:[^\r\n,"]|"(?:\\.|[^"])*")+', annf.readline())
    headlist=map(lambda x:x.strip(),headlist)
    #print headlist
    
    #match metadata with head ang put index into indexlist
    indexlist = []
    outheadlist = []
    for x in metaf:
        try:
            x = re.findall(r'(?:[^\r\n,"]|"(?:\\.|[^"])*")+', x)[1] #use the second one to match
            outheadlist.append(x)
        except IndexError:
            raise("can not process s%: ",x)
        
        try:
            print x, headlist.index(x)
            indexlist.append(headlist.index(x))
        except ValueError:
            raise ValueError("could not find {0} in the".format(x),headlist) 
    
    #write into newfiles:
    outf.write((','.join(outheadlist)+'\r\n'))
    for line in annf:
        matched = re.findall(r'(?:[^\r\n,"]|"(?:\\.|[^"])*")+', line)
        #print matched
        #print indexlist
        #print headlist
        writelist = []
        for i in indexlist:
            #print matched[int(i)]
            writelist.append(matched[int(i)])
        outf.write(','.join(writelist)+'\r\n')
        #break
    
def main():
    logging.basicConfig(filename = 'log.log',format = '%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
    logging.info('start running')
    newdirectory = r"c:\CnsusBureau\SedData"
    directory = r"c:\CnsusBureau\raw"
    if not os.path.exists(newdirectory):
        os.makedirs(newdirectory)
    logging.debug('looks good')   
    for filename in os.listdir(directory):
        #get the needed files _with_ann and find the matching metadata
        if filename.split('.')[-1] == 'csv' and not 'metadata' in filename:
            metafile = filename.replace("with_ann","metadata")
            assert metafile in os.listdir(directory), "Cab not find metadata!!!"
            
            output = newdirectory+"\\"+filename
            outf = open(output,"wb")
            annf = open(directory+"\\"+filename,"rb") 
            metaf = open(directory+"\\"+metafile,"rb")
            handler(outf,annf,metaf)
            outf.close()
            annf.close()
            metaf.close()
            #break
main()