from django.shortcuts import render, redirect
from .forms import FeedbackForm

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feedback_thanks')  # Redirect to a thank-you page or similar
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})
