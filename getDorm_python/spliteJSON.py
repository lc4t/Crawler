for i in range(0,86,1):
    f = open('json_bak/'+str(i)+'.json','r')
    a = f.read()[16:-1]
    f = open('json/'+str(i)+'.json','w+')
    f.write(a)