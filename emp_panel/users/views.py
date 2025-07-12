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
        ifid = int(request.POST.get('ifid'))
        name= request.POST.get('name', '').strip().upper()
        
        mobileno = int(request.POST.get('mobileno'))
        
    

        exists = empinfo.objects.filter(
            ifid=ifid,
           ).exists()

        if exists:
            messages.error(request, " This employe already exists!")
        else:
            empinfo.objects.create(
                ifid=ifid,
                name=name,
                
                mobileno=mobileno
            )
            messages.success(request, " employe added successfully!")

        
        empset = empinfo.objects.all().order_by('ifid')
        return render(request, 'users.html', {'employe': empset})

    return render(request, 'index.html', {'frm': frm})


def users(request):
    emp_set = empinfo.objects.all() 
    query = request.GET.get('q', '').strip()
    emp_set = empinfo.objects.all().order_by('ifid')

    if query:
        emp_set = emp_set.filter(
            Q(name__icontains=query) | Q(ifid__icontains=query)
        )
    
    print(emp_set)
    return render(request, 'users.html', {'employe': emp_set,'query': query})

def edit(request, pk):
    instance = empinfo.objects.get(pk=pk)
    print(instance)

    if request.method == "POST":
        ifid = request.POST.get('ifid')
        name = request.POST.get('name').strip().upper()
        no = int(request.POST.get('mobileno'))

        if  instance.ifid == ifid and instance.name == name and instance.mobileno == no:
            messages.error(request, "No changes were made.")
        else:
            instance.ifid = ifid
            instance.name = name
            instance.mobileno = no
            instance.save()
            messages.success(request, "Employee updated successfully!")

    employe_list = empinfo.objects.all().order_by('ifid')
    return render(request, 'users.html', {'employe': employe_list})

    
       
    
def delete(request, pk):
    instance = empinfo.objects.get(pk=pk)
    name = instance.name  
    instance.delete()
    messages.success(request, f"Movie '{name}' deleted successfully.")
    emp_set = empinfo.objects.all().order_by('ifid')
    return render(request, 'users.html', {'employe': emp_set})



def home(request):
    return render(request, 'main.html')





def impor(request):
    if request.method == "POST":
        new_file = request.FILES['myfile']
        df = pd.read_excel(new_file)

        added = 0
        skipped = 0
        invalid_numbers = 0
        invalid_ifids = []  # collect ifids with invalid mobile numbers

        for _, row in df.iterrows():
            try:
                ifid = int(row['ifid'])
                name = str(row['name']).strip().upper()

                mobileno_raw = str(row['mobileno']).strip()
                if not mobileno_raw.isdigit() or len(mobileno_raw) != 10:
                    invalid_numbers += 1
                    invalid_ifids.append(ifid)  # store bad ifid
                    continue  # skip this row

                mobileno = int(mobileno_raw)

                exists = empinfo.objects.filter(ifid=ifid).exists()

                if exists:
                    skipped += 1
                else:
                    empinfo.objects.create(
                        name=name,
                        ifid=ifid,
                        mobileno=mobileno
                    )
                    added += 1

            except Exception as e:
                print(f"Error processing row: {row} -> {e}")
                skipped += 1

        if added == 0 and invalid_numbers == 0:
            messages.error(request, "This file already exists! Nothing new was uploaded.")
        else:
            msg = f"{added} rows uploaded successfully!"
            if skipped:
                msg += f" {skipped} duplicate rows were skipped."
            if invalid_numbers:
                bad_ids = ", ".join(str(i) for i in invalid_ifids)
                msg += f" {invalid_numbers} rows had invalid mobile numbers (must be 10 digits). IFIDs: [{bad_ids}]."
            messages.success(request, msg)

    empset = empinfo.objects.all().order_by('ifid')
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
