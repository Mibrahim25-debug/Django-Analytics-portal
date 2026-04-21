from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ClientInsight
import pandas as pd

@login_required(login_url='/admin/login/')
def dashboard_view(request):
    if request.method == 'POST' and request.FILES.get('raw_dataset'):
        csv_file = request.FILES['raw_dataset']
        
        # --- THE ELT PIPELINE ---
        # 1. Extract: Load the CSV directly into server memory
        df = pd.read_csv(csv_file)
        
        # 2. Transform: Clean and calculate data
        # (Assuming the client uploads a file with 'Revenue' and 'Product' columns)
        df = df.dropna() # Remove empty rows
        total_rev = df['Revenue'].sum() if 'Revenue' in df.columns else 0.0
        top_product = df['Product'].mode()[0] if 'Product' in df.columns else "Unknown"
        rows_processed = len(df)
        
        # 3. Load: Save the clean, gold-layer data securely to the database
        ClientInsight.objects.create(
            client=request.user,
            total_revenue=total_rev,
            top_performing_product=top_product,
            total_rows_processed=rows_processed
        )
        return redirect('dashboard')

    # Fetch only the data belonging to the logged-in client
    client_data = ClientInsight.objects.filter(client=request.user).order_by('-upload_date')
    
    return render(request, 'analytics/dashboard.html', {'insights': client_data})