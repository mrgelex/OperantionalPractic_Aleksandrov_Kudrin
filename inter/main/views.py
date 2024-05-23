from django.shortcuts import render
from .models import Devices, Time
import plotly.express as px
# from plotly.offline import plot
import plotly.graph_objs as go
import datetime as dt

from .forms import Adjastbasic, Dateperiod


def home(request):
   all=Devices.objects.all()
   data={
      'depth' : 45,
      'power' : 28,
      'speed' : 4.0,
      'start_before' : 0,
      'clean_all' : 165,
      'clean_yester' : 2,
      'clean_to' : 1,
      'id_mod_tel' : 5643564623255646,
      'last' : '2024-04-18 18:24:47',
      'virsion' : 2504,
      'sig_lev' : 87.3
   }
   return render(request, 'main/home.html', {'all':all, 'get':data}) 

def ch(request):
   # if request.method == 'GET':
   s=request.GET.get('begin')
   e=request.GET.get('end')
   data=px.line(labels={'x':'Время', 'y':'М/%'})
   periodform=Dateperiod()
   if s and e:
      print(s,e)
      xx=[]
      yyd=list(Time.objects.values_list('depth', flat=True).filter(date_local__gte=s, date_local__lte=e))
      yyp=list(Time.objects.values_list('power', flat=True).filter(date_local__gte=s, date_local__lte=e))
      qsTidate = list(Time.objects.values_list('date_local', flat=True).filter(date_local__gte=s, date_local__lte=e))
      qsTitime=list(Time.objects.values_list('time_local', flat=True).filter(date_local__gte=s, date_local__lte=e))
      for index in range(len(qsTitime)):
         xx.append(dt.datetime.combine(qsTidate[index], qsTitime[index]))
      data.add_trace(go.Scatter(x=xx, y=yyd, mode="lines", name='Глубина'))
      data.add_trace(go.Scatter(x=xx, y=yyp, mode="lines", name='Мощность'))
      data.update_yaxes(autorange='reversed')
   gr=data.to_html(full_html=False)   
   return render(request, 'main/chart.html', {'gr':gr, 'periodform':periodform}) 

def adjust(request):
   all=Devices.objects.all()

   if request.method == 'POST':
      formbas=Adjastbasic(request.POST)
      if formbas.is_valid():
         bas = formbas.cleaned_data
         # словарь с данными уставок
         print(bas)
   data={
      'depth' : 45,
      'power' : 28,
      'speed' : 4.0,
      'start_before' : 0,
      'clean_all' : 165,
      'clean_yester' : 2,
      'clean_to' : 1,
      'id_mod_tel' : 5643564623255646,
      'last' : '2024-04-18 18:24:47',
      'virsion' : 2504,
      'sig_lev' : 87.3
   }
   formbas=Adjastbasic()
   return render(request, 'main/adjust.html', {'all':all, 'get':data, 'formbas':formbas}) 

