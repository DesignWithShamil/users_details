from django.http import JsonResponse
import pandas as pd
from django.shortcuts import render


def impor(request):
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

        return render(request, "index.html", {"employees": final_employees})

    return render(request, "index.html")
