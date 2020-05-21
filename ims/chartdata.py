class chartdata:    
    def chartdataorder(dic):
        import datetime
        month=datetime.datetime.now().month
        year=datetime.datetime.now().year
        monthnames={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}


        ls=[]
        i=1
        j=12
        newyear=False
        for key, value in monthnames.items():
            if key==month:
                ls.append(month)
                for l in range(1,12):
                    if ls[-1] !=12 and newyear==False:
                        newmonth=month-i
                        ls.insert(0,newmonth)
                        i=i+1
                        if(newmonth==1):
                            newyear=True
                    else:
                        ls.insert(0,j)
                        j=j-1


        #{k: sample_dict[k] for k in desired_order_list}
        monthreorderdict={k: monthnames[k] for k in ls}
        #print(monthreorderdict)
        changeyear=False
        for key, value in monthreorderdict.items():
            if value!='Jan' and changeyear==False:
                monthreorderdict[key]=value+' '+str(year-2001)
                if value=='Dec':
                    changeyear=True
            else:
                monthreorderdict[key]=value+' '+str(year-2000)

        #print(monthreorderdict)
        monthreorderdict = {value:0 for key, value in monthreorderdict.items()}
        for key,values in dic.items():
            if key in monthreorderdict.keys():
               # print(key)
                monthreorderdict[key]=values
        
        return monthreorderdict       