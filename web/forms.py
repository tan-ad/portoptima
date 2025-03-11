from django import forms

class PortfolioAnalysisForm(forms.Form):
    tickers = forms.CharField(
        label='Ticker Symbols',
        help_text='Enter ticker symbols separated by spaces (e.g., AAPL MSFT GOOGL)',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    weights = forms.CharField(
        label='Portfolio Weights (Optional)',
        help_text='Enter weights separated by spaces (e.g., 0.4 0.3 0.3). Leave blank for equal weights.',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    period_choices = [
        ('1y', '1 Year'),
        ('2y', '2 Years'),
        ('5y', '5 Years'),
        ('10y', '10 Years'),
        ('max', 'Maximum Available')
    ]
    
    period = forms.ChoiceField(
        label='Historical Period',
        choices=period_choices,
        initial='5y',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    interval_choices = [
        ('1d', 'Daily'),
        ('1wk', 'Weekly'),
        ('1mo', 'Monthly')
    ]
    
    interval = forms.ChoiceField(
        label='Data Interval',
        choices=interval_choices,
        initial='1d',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    risk_free_rate = forms.FloatField(
        label='Risk-Free Rate',
        help_text='Annual risk-free rate (e.g., 0.02 for 2%)',
        initial=0.02,
        min_value=0.0,
        max_value=0.20,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'})
    )
    
    optimization_choices = [
        ('sharpe', 'Maximize Sharpe Ratio'),
        ('min_volatility', 'Minimize Volatility'),
        ('max_return', 'Maximize Return')
    ]
    
    optimization = forms.ChoiceField(
        label='Optimization Target',
        choices=optimization_choices,
        initial='sharpe',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    min_weight = forms.FloatField(
        label='Minimum Weight',
        help_text='Minimum weight for any asset (0 to 1)',
        initial=0,
        min_value=0.0,
        max_value=1.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    
    max_weight = forms.FloatField(
        label='Maximum Weight',
        help_text='Maximum weight for any asset (0 to 1)',
        initial=1,
        min_value=0.0,
        max_value=1.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    
    def clean_tickers(self):
        """Validate and format tickers"""
        tickers = self.cleaned_data['tickers'].strip().upper()
        if not tickers:
            raise forms.ValidationError("Please enter at least one ticker symbol")
        return tickers.split()
    
    def clean_weights(self):
        """Validate and format weights"""
        weights_str = self.cleaned_data.get('weights', '').strip()
        if not weights_str:
            return None  # Equal weights will be assigned
        
        try:
            weights = [float(w) for w in weights_str.split()]
            
            # Check if number of weights matches number of tickers
            tickers = self.cleaned_data.get('tickers')
            if tickers and len(weights) != len(tickers):
                raise forms.ValidationError(
                    f"Number of weights ({len(weights)}) must match number of tickers ({len(tickers)})"
                )
            
            # Check if weights are positive
            if any(w < 0 for w in weights):
                raise forms.ValidationError("All weights must be positive")
                
            return weights
        except ValueError:
            raise forms.ValidationError("Weights must be valid numbers separated by spaces")
