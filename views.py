
from django.db.models import  Count, Avg
from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models import Q
import datetime
import xlwt
from django.http import HttpResponse

# Create your views here.
from Remote_User.models import ClientRegister_Model,COVID19_transmission_model,Trained_COVID19_transmission_model,detection_ratio_model


def serviceproviderlogin(request):
    if request.method  == "POST":
        admin = request.POST.get('username')
        password = request.POST.get('password')
        if admin == "SProvider" and password =="SProvider":

            Trained_COVID19_transmission_model.objects.all().delete()
            return redirect('View_Remote_Users')

    return render(request,'SProvider/serviceproviderlogin.html')


def viewtreandingquestions(request,chart_type):
    dd = {}
    pos,neu,neg =0,0,0
    poss=None
    topic = COVID19_transmission_model.objects.values('ratings').annotate(dcount=Count('ratings')).order_by('-dcount')
    for t in topic:
        topics=t['ratings']
        pos_count=COVID19_transmission_model.objects.filter(topics=topics).values('names').annotate(topiccount=Count('ratings'))
        poss=pos_count
        for pp in pos_count:
            senti= pp['names']
            if senti == 'positive':
                pos= pp['topiccount']
            elif senti == 'negative':
                neg = pp['topiccount']
            elif senti == 'nutral':
                neu = pp['topiccount']
        dd[topics]=[pos,neg,neu]
    return render(request,'SProvider/viewtreandingquestions.html',{'object':topic,'dd':dd,'chart_type':chart_type})

def Find_Mitigation_of_COVID19_Transmission_Ratio(request):
    detection_ratio_model.objects.all().delete()
    ratio = ""
    kword = 'Medical Emergency'
    print(kword)
    obj = Trained_COVID19_transmission_model.objects.all().filter(Q(Mitigating_Status=kword))
    obj1 = Trained_COVID19_transmission_model.objects.all()
    count = obj.count();
    count1 = obj1.count();
    ratio = (count / count1) * 100
    if ratio != 0:
        detection_ratio_model.objects.create(names=kword, ratio=ratio)

    ratio1 = ""
    kword1 = 'Quarantine'
    print(kword1)
    obj1 = Trained_COVID19_transmission_model.objects.all().filter(Q(Mitigating_Status=kword1))
    obj11 = Trained_COVID19_transmission_model.objects.all()
    count1 = obj1.count();
    count11 = obj11.count();
    ratio1 = (count1 / count11) * 100
    if ratio1 != 0:
        detection_ratio_model.objects.create(names=kword1, ratio=ratio1)

    ratio12 = ""
    kword12 = 'Covid19 Test'
    print(kword12)
    obj12 = Trained_COVID19_transmission_model.objects.all().filter(Q(Mitigating_Status=kword12))
    obj112 = Trained_COVID19_transmission_model.objects.all()
    count12 = obj12.count();
    count112 = obj112.count();
    ratio12 = (count12 / count112) * 100
    if ratio12 != 0:
        detection_ratio_model.objects.create(names=kword12, ratio=ratio12)

    ratio123 = ""
    kword123 = 'No Covid19 Symptoms'
    print(kword123)
    obj123 = Trained_COVID19_transmission_model.objects.all().filter(Q(Mitigating_Status=kword123))
    obj1123 = Trained_COVID19_transmission_model.objects.all()
    count123 = obj123.count();
    count1123 = obj1123.count();
    ratio123 = (count123 / count1123) * 100
    if ratio123 != 0:
        detection_ratio_model.objects.create(names=kword123, ratio=ratio123)

    obj = detection_ratio_model.objects.all()

    return render(request, 'SProvider/Find_Mitigation_of_COVID19_Transmission_Ratio.html', {'objs': obj})

def View_All_COVID19_Transmission_Prediction(request):
    fname='Medical Emergency'
    fname1 = 'Quarantine'
    fname2 = 'Covid19 Test'
    obj = Trained_COVID19_transmission_model.objects.all().filter(Q(Mitigating_Status=fname) | Q(Mitigating_Status=fname1)| Q(Mitigating_Status=fname2))
    return render(request, 'SProvider/View_All_COVID19_Transmission_Prediction.html', {'objs': obj})

def View_Remote_Users(request):
    obj=ClientRegister_Model.objects.all()
    return render(request,'SProvider/View_Remote_Users.html',{'objects':obj})

def ViewTrendings(request):
    topic = COVID19_transmission_model.objects.values('topics').annotate(dcount=Count('topics')).order_by('-dcount')
    return  render(request,'SProvider/ViewTrendings.html',{'objects':topic})

def negativechart(request,chart_type):
    dd = {}
    pos, neu, neg = 0, 0, 0
    poss = None
    topic = COVID19_transmission_model.objects.values('ratings').annotate(dcount=Count('ratings')).order_by('-dcount')
    for t in topic:
        topics = t['ratings']
        pos_count = COVID19_transmission_model.objects.filter(topics=topics).values('names').annotate(topiccount=Count('ratings'))
        poss = pos_count
        for pp in pos_count:
            senti = pp['names']
            if senti == 'positive':
                pos = pp['topiccount']
            elif senti == 'negative':
                neg = pp['topiccount']
            elif senti == 'nutral':
                neu = pp['topiccount']
        dd[topics] = [pos, neg, neu]
    return render(request,'SProvider/negativechart.html',{'object':topic,'dd':dd,'chart_type':chart_type})


def charts(request,chart_type):
    chart1 = detection_ratio_model.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts.html", {'form':chart1, 'chart_type':chart_type})

def charts1(request,chart_type):
    chart1 = Trained_COVID19_transmission_model.objects.values('names').annotate(dcount=Avg('Oxigen_level'))
    return render(request,"SProvider/charts1.html", {'form':chart1, 'chart_type':chart_type})

def Train_View_Mitigating_COVID19_Transmission(request):

    se=''
    obj1 = COVID19_transmission_model.objects.values('Scholl_Code',
    'names',
    'Scholl_Type',
    'Function1',
    'Contact_Name',
    'Address',
    'Town',
    'Zip',
    'Phone',
    'Number_Of_Children',
    'Oxigen_level',
    'Fever'
    )

    Trained_COVID19_transmission_model.objects.all().delete()
    for t in obj1:

        Scholl_Code= t['Scholl_Code']
        names= t['names']
        Scholl_Type= t['Scholl_Type']
        Function1= t['Function1']
        Contact_Name= t['Contact_Name']
        Address= t['Address']
        Town= t['Town']
        Zip= t['Zip']
        Phone= t['Phone']
        Number_Of_Children= t['Number_Of_Children']
        Oxigen_level= t['Oxigen_level']
        Fever= t['Fever']

        Oxigen_level1 = float(Oxigen_level)
        Fever1 = float(Fever)

        if Oxigen_level1<=80 and Fever1>=102:
            mitigatestatus='Medical Emergency'
        elif  Oxigen_level1<=85 and Fever1>=103:
            mitigatestatus='Quarantine'
        elif Oxigen_level1<=90 and Fever1>=100:
            mitigatestatus = 'Covid19 Test'
        elif Oxigen_level1>=95 and Fever1<=99:
            mitigatestatus = 'No Covid19 Symptoms'

        Trained_COVID19_transmission_model.objects.create(Scholl_Code=Scholl_Code,
        names=names,
        Scholl_Type=Scholl_Type,
        Function1=Function1,
        Contact_Name=Contact_Name,
        Address=Address,
        Town=Town,
        Zip=Zip,
        Phone=Phone,
        Number_Of_Children=Number_Of_Children,
        Oxigen_level=Oxigen_level,
        Fever=Fever,
        Mitigating_Status=mitigatestatus
        )

    obj =Trained_COVID19_transmission_model.objects.all()

    return render(request, 'SProvider/Train_View_Mitigating_COVID19_Transmission.html', {'list_objects': obj})

def likeschart(request,like_chart):
    charts =detection_ratio_model.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/likeschart.html", {'form':charts, 'like_chart':like_chart})

def Download_Trained_DataSets(request):

    response = HttpResponse(content_type='application/ms-excel')
    # decide file name
    response['Content-Disposition'] = 'attachment; filename="TrainedData.xls"'
    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')
    # adding sheet
    ws = wb.add_sheet("sheet1")
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True
    # writer = csv.writer(response)
    obj = Trained_COVID19_transmission_model.objects.all()
    data = obj  # dummy method to fetch data.
    for my_row in data:
        row_num = row_num + 1
        ws.write(row_num, 0, my_row.Scholl_Code, font_style)
        ws.write(row_num, 1, my_row.names, font_style)
        ws.write(row_num, 2, my_row.Scholl_Type, font_style)
        ws.write(row_num, 3, my_row.Function1, font_style)
        ws.write(row_num, 4, my_row.Contact_Name, font_style)
        ws.write(row_num, 5, my_row.Address, font_style)
        ws.write(row_num, 6, my_row.Town, font_style)
        ws.write(row_num, 7, my_row.Zip, font_style)
        ws.write(row_num, 8, my_row.Phone, font_style)
        ws.write(row_num, 9, my_row.Number_Of_Children, font_style)
        ws.write(row_num, 10, my_row.Oxigen_level, font_style)
        ws.write(row_num, 11, my_row.Fever, font_style)
        ws.write(row_num, 12, my_row.Mitigating_Status, font_style)

    wb.save(response)
    return response

















