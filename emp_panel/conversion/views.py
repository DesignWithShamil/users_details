from pyexpat.errors import messages
from django.http import JsonResponse
import pandas as pd
from django.shortcuts import render

from . models import employee_groups


def imp(request):
    employees = []

    if request.method == "POST" and request.FILES.get("myfile"):
        excel_file = request.FILES["myfile"]
        df = pd.read_excel(excel_file, header=None)

       
        duration = df.iloc[2, 1]
        if 'To' in duration:
            parts = duration.split('To')
            start_part = parts[0].strip()
            start_month, start_day = start_part.split()[:2]

      
        row6 = df.iloc[6]
        cells = row6.tolist()[2:]  
        days = []
        nan_indexes = []

        for idx, cell in enumerate(cells):
            if pd.isna(cell):
                nan_indexes.append(idx)
                continue
            parts = str(cell).split()
            if parts:
                days.append(parts[0])

        final_days = [f"{start_month} {num}" for num in days]

        current_emp = None

       
        for idx, row in df.iterrows():
            first_cell = str(row[0]).strip()

            if first_cell.startswith("Employee"):
                cell = str(row[4]).strip()
                parts = [p.strip() for p in cell.split(":") if p.strip()]
                if len(parts) >= 2:
                    ifid = parts[0]
                    name = parts[1]

                    current_emp = {
                        "IFID": ifid,
                        "NAME": name,
                        "InTime1": [],
                        "OutTime1": [],
                        "InTime2": [],
                        "OutTime2": []
                    }
                    employees.append(current_emp)

            elif current_emp:
                if first_cell.startswith("InTime1"):
                    current_emp["InTime1"] = row.tolist()[2:]
                elif first_cell.startswith("OutTime1"):
                    current_emp["OutTime1"] = row.tolist()[2:]
                elif first_cell.startswith("InTime2"):
                    current_emp["InTime2"] = row.tolist()[2:]
                elif first_cell.startswith("OutTime2"):
                    current_emp["OutTime2"] = row.tolist()[2:]

        
        nan_indexes = sorted(nan_indexes, reverse=True)
        for emp in employees:
            for idx in nan_indexes:
                if idx < len(emp["InTime1"]):
                    del emp["InTime1"][idx]
                if idx < len(emp["OutTime1"]):
                    del emp["OutTime1"][idx]
                if idx < len(emp["InTime2"]):
                    del emp["InTime2"][idx]
                if idx < len(emp["OutTime2"]):
                    del emp["OutTime2"][idx]

      
        final_employees = []
        for emp in employees:
            emp_result = {
                "IFID": emp["IFID"],
                "NAME": emp["NAME"]
            }
            for i, day in enumerate(final_days):
                in1 = str(emp["InTime1"][i]).strip() if i < len(emp["InTime1"]) else ""
                out1 = str(emp["OutTime1"][i]).strip() if i < len(emp["OutTime1"]) else ""
                in2 = str(emp["InTime2"][i]).strip() if i < len(emp["InTime2"]) else ""
                out2 = str(emp["OutTime2"][i]).strip() if i < len(emp["OutTime2"]) else ""

                combined = "\n".join([in1, out1, in2, out2])
                emp_result[day] = combined

            final_employees.append(emp_result)

        return render(request, "imp.html", {"employees": final_employees})

    return render(request, "imp.html")

from django.contrib import messages
import pandas as pd

def conversion_excel(request):
    if request.method == "POST":
        new_file = request.FILES['conversion']
        xl = pd.read_excel(new_file, sheet_name=None)

        added = 0  
        skipped = 0

        for sheet_name, df in xl.items():
            for index, row in df.iterrows():
                try:
                    ifid = row['IFID']
                    name = str(row['NAME']).strip().upper()
                    entity = sheet_name.upper().strip().replace(" ", "")

                    exists = employee_groups.objects.filter(ifid=ifid).exists()

                    if exists:
                        skipped += 1
                    else:
                        employee_groups.objects.create(
                            name=name,
                            ifid=ifid,
                            entity=entity
                        )
                        added += 1

                except Exception as e:
                    print(f"Error processing row: {row} -> {e}")
                    skipped += 1

        
        msg = f"{added} rows uploaded successfully!"
        if skipped:
            msg += f" {skipped} duplicate rows were skipped."

        messages.success(request, msg)

    infolksgroup_list = employee_groups.objects.filter(entity='INFOLKSGROUP').order_by('ifid')
    medrays_list = employee_groups.objects.filter(entity='MEDRAYS').order_by('ifid')
    webfolks_list = employee_groups.objects.filter(entity='WEBFOLKS').order_by('ifid')
    infolks_list = employee_groups.objects.filter(entity='INFOLKS').order_by('ifid')
    employee_list = employee_groups.objects.all().order_by('ifid')

    return render(request, 'imp.html', {
        'employee_list': employee_list,
        'infolks_list': infolks_list,
        'webfolks_list': webfolks_list,
        'infolksgroup_list': infolksgroup_list,
        'medrays_list': medrays_list
    })
def emp_details(request):
   

    infolksgroup_list = employee_groups.objects.filter(entity='INFOLKSGROUP').order_by('ifid')
    medrays_list = employee_groups.objects.filter(entity='MEDRAYS').order_by('ifid')
    webfolks_list = employee_groups.objects.filter(entity='WEBFOLKS').order_by('ifid')
    infolks_list = employee_groups.objects.filter(entity='INFOLKS').order_by('ifid')
    employee_list = employee_groups.objects.all().order_by('ifid')

    return render(request, 'imp.html', {
        'employee_list': employee_list,
        'infolks_list': infolks_list,
        'webfolks_list': webfolks_list,
        'infolksgroup_list': infolksgroup_list,
        'medrays_list': medrays_list
    })

def delete_conv(request, pk):
    instance = employee_groups.objects.get(pk=pk)
    name = instance.name  
    instance.delete()
    messages.success(request, f"employee '{name}' deleted successfully.")
    infolksgroup_list = employee_groups.objects.filter(entity='INFOLKSGROUP').order_by('ifid')
    medrays_list = employee_groups.objects.filter(entity='MEDRAYS').order_by('ifid')
    webfolks_list = employee_groups.objects.filter(entity='WEBFOLKS').order_by('ifid')
    infolks_list = employee_groups.objects.filter(entity='INFOLKS').order_by('ifid')
    employee_list = employee_groups.objects.all().order_by('ifid')

    return render(request, 'imp.html', {
        'employee_list': employee_list,
        'infolks_list': infolks_list,
        'webfolks_list': webfolks_list,
        'infolksgroup_list': infolksgroup_list,
        'medrays_list': medrays_list
    })

def edit_conv(request, pk):
    instance = employee_groups.objects.get(pk=pk)
    print(instance)

    if request.method == "POST":
        ifid = int(request.POST.get('ifid'))
        name = request.POST.get('name').strip().upper()
        no = request.POST.get('entity')

        if instance.ifid == ifid and instance.name == name and instance.entity == no:
            messages.error(request, "No changes were made.")
        else:
            instance.ifid = ifid
            instance.name = name
            instance.entity = no
            instance.save()
            messages.success(request, "Employee updated successfully!")

    infolksgroup_list = employee_groups.objects.filter(entity='INFOLKSGROUP').order_by('ifid')
    medrays_list = employee_groups.objects.filter(entity='MEDRAYS').order_by('ifid')
    webfolks_list = employee_groups.objects.filter(entity='WEBFOLKS').order_by('ifid')
    infolks_list = employee_groups.objects.filter(entity='INFOLKS').order_by('ifid')
    employee_list = employee_groups.objects.all().order_by('ifid')

    return render(request, 'imp.html', {
        'employee_list': employee_list,
        'infolks_list': infolks_list,
        'webfolks_list': webfolks_list,
        'infolksgroup_list': infolksgroup_list,
        'medrays_list': medrays_list
    })