from django.contrib import messages
from django.shortcuts import render
from . models import empinfo
from . form import empForm
import pandas as pd
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.db.models import Q



def create(request):
    frm = empForm()

    if request.method == "POST":
        name = request.POST.get('name', '').strip().upper()
        ifid = int(request.POST.get('ifid'))
        mobileno = int(request.POST.get('mobileno'))

        exists = empinfo.objects.filter(
            name=name,
            ifid=ifid,
           
        ).exists()

        if exists:
            messages.error(request, " This employe already exists!")
        else:
            empinfo.objects.create(
                name=name,
                ifid=ifid,
                mobileno=mobileno
            )
            messages.success(request, " employe added successfully!")

        
        empset = empinfo.objects.all()
        return render(request, 'users.html', {'employe': empset})

    return render(request, 'index.html', {'frm': frm})


def users(request):
    emp_set = empinfo.objects.all() 
    query = request.GET.get('q', '').strip()
    emp_set = empinfo.objects.all()

    if query:
        emp_set = emp_set.filter(
            Q(name__icontains=query) | Q(ifid__icontains=query)
        )
    
    print(emp_set)
    return render(request, 'users.html', {'employe': emp_set,'query': query})

def edit (request,pk):
    instance=empinfo.objects.get(pk=pk)
    print(instance)
    if request.method == "POST":  
        name = request.POST.get('name').strip().upper()
        ifid = request.POST.get('ifid')
        no = int(request.POST.get('mobileno'))
       
        instance.name=name
        instance.ifid=ifid
        instance.mobileno=no
        instance.save()
        
        instance=empinfo.objects.all() 
        return render(request, 'users.html',{'employe':instance})
    
       
    
def delete(request, pk):
    instance = empinfo.objects.get(pk=pk)
    name = instance.name  
    instance.delete()
    messages.success(request, f"Movie '{name}' deleted successfully.")
    emp_set = empinfo.objects.all()
    return render(request, 'users.html', {'employe': emp_set})



def home(request):
    return render(request, 'main.html')





def impor(request):
    if request.method == "POST":
        new_file = request.FILES['myfile']
        df = pd.read_excel(new_file)

        added = 0
        skipped = 0

        for _, row in df.iterrows():
            name = str(row['name']).strip().upper()
            ifid = int(row['ifid'])
            mobileno = int(row['mobileno'])

            exists = empinfo.objects.filter(
                name=name,
                ifid=ifid,
               
                
            ).exists()

            if exists:
                skipped += 1
            else:
                empinfo.objects.create(
                    name=name,
                    ifid=ifid,
                   mobileno=mobileno
                    
                )
                added += 1

        if added == 0:
            messages.error(request, "This file already exists! Nothing new was uploaded.")
        else:
            messages.success(request, f"{added} rows uploaded successfully!")
    empset = empinfo.objects.all()
    return render(request, 'users.html', {'employe': empset})

def export_empinfo(request):
    format = request.GET.get('format', 'csv') 

    qs = empinfo.objects.all().values()
    df = pd.DataFrame.from_records(qs)

    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="empinfo.csv"'
        df.to_csv(path_or_buf=response, index=False)

    elif format == 'xlsx':
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="empinfo.xlsx"'
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

    elif format == 'pdf':
        
        html = df.to_html(index=False)
        result = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=result)
        if pisa_status.err:
            return HttpResponse('Error generating PDF', status=500)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="empinfo.pdf"'
        response.write(result.getvalue())
    
    elif format == 'json':
        response = HttpResponse(df.to_json(orient='records'), content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="empinfo.json"'
        
    else:
        return HttpResponse('Invalid format', status=400)

    return response
