# my_project1

Problem Statement: Create a Django application with the below-given specification  within 16 hrs and push it to the public GitHub repository. Send a link of your repository  to our email address kirajpvtltd@gmail.com 
● You will be eligible for the next round if 50% of the task is complete. ● Using a search engine is allowed. 
● Use proper coding standards and comments. 
Specification: 
1. Django project with the name “TradingProject”. 
2. Django app within the project “MainApp”. 
3. MainApp should have a view to accepting a CSV file and timeframe(will be a  number). 
4. Store the CSV file on the Django server. You have to read a CSV file using the  fastest option available. Store the data present in the file in the python list of  candle objects. 
5. The candle object will have attributes: [id, open, high, low, close, date] 6. You have to convert the list of candles that will be one minute into a given  timeframe. [Use async operations] 
7. Store this converted data into a JSON file and store it in the file system. 8. In the response, the user should get the option to download the JSON file.


Code:-

pip install env
py -m venv myenv
myenv\Scripts\activate.bat
django-admin startproject TradingProject
cd TradingProject
python manage.py startapp MainApp

================================================================

# MainApp/models.py
from django.db import models

class Candle(models.Model):
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()

===========================================================



# MainApp/forms.py
from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()
    timeframe = forms.IntegerField()

============================================


# MainApp/views.py
from django.shortcuts import render
from django.http import JsonResponse, FileResponse
import csv
import json

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            timeframe = form.cleaned_data['timeframe']
            csv_file = form.cleaned_data['csv_file']

            # Process the CSV file
            candles = []
            with csv_file as file:
                reader = csv.DictReader(file)
                for row in reader:
                    candle = {
                        'open': row['OPEN'],
                        'high': row['HIGH'],
                        'low': row['LOW'],
                        'close': row['CLOSE'],
                        'date': f"{row['DATE']} {row['TIME']}"
                    }
                    candles.append(candle)

            # Convert to the desired timeframe
            # Implement your conversion logic here using async operations

            # Store the converted data as a JSON file
            output_file = 'output.json'
            with open(output_file, 'w') as json_file:
                json.dump(candles, json_file)

            # Return the JSON file as a response
            response = FileResponse(open(output_file, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{output_file}"'

            return response
    else:
        form = CSVUploadForm()

    return render(request, 'upload.html', {'form': form})
========================================================================


<!-- MainApp/templates/upload.html -->
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Upload CSV</button>
</form>




================================================================


# TradingProject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mainapp/', include('MainApp.urls')),
]


=======================================================

# MainApp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),
]


=================================================

python manage.py makemigrations
python manage.py migrate
python manage.py runserver
