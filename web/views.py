import os
import uuid
import sys
import threading
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.urls import reverse
from .forms import PortfolioAnalysisForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime

# Add modules directory to Python path
if not os.path.join(settings.BASE_DIR, 'modules') in sys.path:
    sys.path.append(os.path.join(settings.BASE_DIR, 'modules'))

def home(request):
    """Home page with portfolio analysis form"""
    form = PortfolioAnalysisForm()
    return render(request, 'web/home.html', {'form': form})

@api_view(['POST'])
def analyze_portfolio_api(request):
    """API endpoint for portfolio analysis"""
    # Extract parameters from the request
    data = request.data
    
    # Generate a unique ID for this analysis
    analysis_id = uuid.uuid4().hex
    
    # Create output directory
    output_dir = os.path.join(settings.GENERATED_FILES_ROOT, analysis_id)
    os.makedirs(output_dir, exist_ok=True)
    
    # Start analysis in background
    thread = threading.Thread(
        target=run_analysis,
        args=(data, output_dir)
    )
    thread.daemon = True
    thread.start()
    
    # Return ID and URL for results
    return Response({
        'analysis_id': analysis_id,
        'results_url': reverse('web:results', args=[analysis_id])
    })

def analyze_portfolio(request):
    """Handle portfolio analysis form submission"""
    if request.method == 'POST':
        form = PortfolioAnalysisForm(request.POST)
        if form.is_valid():
            # Generate a unique ID for this analysis
            analysis_id = uuid.uuid4().hex
            
            # Create output directory
            output_dir = os.path.join(settings.GENERATED_FILES_ROOT, analysis_id)
            os.makedirs(output_dir, exist_ok=True)
            
            # Get cleaned data
            data = form.cleaned_data
            
            # Start analysis in background
            thread = threading.Thread(
                target=run_analysis,
                args=(data, output_dir)
            )
            thread.daemon = True
            thread.start()
            
            # Redirect to results page
            return redirect('web:results', analysis_id=analysis_id)
    else:
        form = PortfolioAnalysisForm()
    
    return render(request, 'web/home.html', {'form': form})

def results(request, analysis_id):
    """Display portfolio analysis results"""
    output_dir = os.path.join(settings.GENERATED_FILES_ROOT, analysis_id)
    
    # Check if output directory exists
    if not os.path.exists(output_dir):
        return render(request, 'web/error.html', {
            'error': 'Analysis not found',
            'message': 'The requested analysis does not exist or has been deleted.'
        })
    
    # Check if analysis is complete
    results_data = {}
    
    # Check for generated images
    image_files = {
        'efficient_frontier': 'efficient_frontier.png',
        'asset_allocation': 'asset_allocation.png',
        'correlation_matrix': 'correlation_matrix.png',
        'performance_summary': 'performance_summary.png'
    }
    
    images = {}
    for key, filename in image_files.items():
        filepath = os.path.join(output_dir, filename)
        if os.path.exists(filepath):
            # Get relative path for the template
            images[key] = os.path.join(settings.MEDIA_URL, 'generated', analysis_id, filename)
    
    # Check if all images are generated
    is_complete = len(images) == len(image_files)
    
    context = {
        'analysis_id': analysis_id,
        'is_complete': is_complete,
        'images': images,
        'results': results_data
    }
    
    return render(request, 'web/results.html', context)

def run_analysis(data, output_dir):
    """Run portfolio analysis using modules"""
    try:
        # Import your modules
        from portfolio_analyzer import main
        import sys
        from io import StringIO
        import contextlib
        
        # Prepare arguments for your analyzer
        tickers = data.get('tickers', [])
        weights = data.get('weights')
        period = data.get('period', settings.PORTOPTIMA_DEFAULT_PERIOD)
        interval = data.get('interval', settings.PORTOPTIMA_DEFAULT_INTERVAL)
        risk_free_rate = data.get('risk_free_rate', settings.PORTOPTIMA_DEFAULT_RISK_FREE_RATE)
        optimization = data.get('optimization', 'sharpe')
        min_weight = data.get('min_weight', 0)
        max_weight = data.get('max_weight', 1)
        
        # Prepare command-line arguments
        sys.argv = ['portfolio_analyzer.py']
        sys.argv.extend(['--tickers'] + tickers)
        
        if weights:
            sys.argv.extend(['--weights'] + [str(w) for w in weights])
        
        sys.argv.extend([
            '--period', period,
            '--interval', interval,
            '--risk-free-rate', str(risk_free_rate),
            '--optimization', optimization,
            '--min-weight', str(min_weight),
            '--max-weight', str(max_weight),
            '--output-dir', output_dir,
            '--no-show'  # Don't show interactive plots
        ])
        
        # Redirect stdout to capture output
        output = StringIO()
        with contextlib.redirect_stdout(output):
            main()
        
        # Log the output
        with open(os.path.join(output_dir, 'log.txt'), 'w') as f:
            f.write(output.getvalue())
            
    except Exception as e:
        # Log any errors
        with open(os.path.join(output_dir, 'error.log'), 'w') as f:
            f.write(f"Error running analysis: {str(e)}")
        import traceback
        with open(os.path.join(output_dir, 'traceback.log'), 'w') as f:
            traceback.print_exc(file=f)
