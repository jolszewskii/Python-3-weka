from imports import *

array_listInt = []
array_listDec = []

class A:
    def each_line_to_array(file):
    #data = np.genfromtxt(file, lambda:{}) #load + arrays in float
        with open(file) as f:
            for k, g in groupby(f, lambda x: x.startswith(('moved', "ok", 'slightly_moved', 'lost'))): #.data strings
                if not k: #if not 'str'
                    array_listInt.append(np.array(
                        [[int(x) for x in d.split()] for d in g if len(d.strip())]
                        )) #double array    
    def each_line_to_array_dec(file):
    #data = np.genfromtxt(file, lambda:{}) #load + arrays in float
        with open(file) as f:
            for line in f:
                line = line.rstrip('\n')
                if line.startswith(('moved', 'ok', 'slightly_moved', 'lost')):
                    array_listDec.append(line)
    def maths():
        with open('text3.csv', 'w') as f:
            print("ID","Fx_min","Fx_max","Fx_avg","Fx_stdev","Fx_med",
                    "Fy_min","Fy_max","Fy_avg","Fy_stdev","Fy_med",
                    "Fz_min","Fz_max","Fz_avg","Fz_stdev","Fz_med",
                    "Tx_min","Tx_max","Tx_avg","Tx_stdev","Tx_med",
                    "Ty_min","Ty_max","Ty_avg","Ty_stdev","Ty_med",
                    "Tz_min","Tz_max","Tz_avg","Tz_stdev","Tz_med","Dec",
                    file=f,sep=',')
            for i in range(0,47): 
                if i>0:
                    print(" ",file =f)
                print(i+1, file=f,sep=',', end=',')
                testmeanDec = array_listDec[i]
                for j in range(0,6):
                    testmeanInt = array_listInt[i].T[j].T #take 1 column for 1 list in list ||  0-46 0-5
                    p=min(testmeanInt)
                    p1=max(testmeanInt)
                    p2=mean(testmeanInt)
                    p3=stdev(testmeanInt)
                    p4=median(testmeanInt)
                    print (p,p1,p2,p3,p4, file=f,sep=',', end=',')
                    if j==5:    
                       print("".join(testmeanDec), file=f,sep=',', end='') 
        