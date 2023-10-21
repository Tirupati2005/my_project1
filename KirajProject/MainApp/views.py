from django.shortcuts import render
from django.http import JsonResponse, FileResponse,HttpRequest
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
