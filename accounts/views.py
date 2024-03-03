from django.shortcuts import render

from datetime import date, timedelta
from praytimes import *  # Assuming the PrayTimes class is in praytimes.py

from django.http import JsonResponse
import calendar
from .models import Contact

# view to generate the home page

def index(request):
	if request.method == 'POST':
		# Create an instance of your model and save the form data
		email = request.POST.get('email')
		name = request.POST.get('name')
		message = request.POST.get('message')
		
		# Assuming your model is named `Contact` and has `email`, `name`, and `message` fields
		contact = Contact(email=email, name=name, message=message)
		contact.save()
		
		# Redirect or send a success response
		return JsonResponse({'success': 'Message sent successfully!'})
		 
	# Render index page for GET requests
	return render(request, 'index.html')



#views function that calculates the prayer time for kamloops with all adjustments and renders prayer page

from datetime import datetime, time
import calendar
from django.shortcuts import render
# Assuming PrayTimes and is_dst are correctly imported

def prayer_times_view(request, year=None, month=None):
	today = datetime.today().date()
	year = year or today.year
	month = month or today.month

	# Initialize PrayTimes instance and adjust settings...
	PT = PrayTimes("ISNA")
	PT.adjust({'fajr': 18, 'isha': 15, 'maghrib': '0 min'})
	PT.adjust({'highLats': 'AngleBased'})
	
	timezone_name = 'America/Vancouver'
	num_days = calendar.monthrange(year, month)[1]
	month_name = calendar.month_name[month]
	
	calendar_data = []
	for day in range(1, num_days + 1):
		current_date = datetime(year, month, day).date()
		dst = is_dst(current_date, timezone_name)
		timezone_offset = -7 if dst else -8
		times = PT.getPrayerAndIqamahTimes(current_date, (50.6833, -120.333), timezone_offset)
		calendar_data.append({'date': current_date, 'times': times})
	
	today_times = PT.getPrayerAndIqamahTimes(today, (50.6833, -120.333), timezone_offset)

	# Update today_times with datetime.time objects
	for prayer, t in today_times.items():
		if isinstance(t, str):
			today_times[prayer] = datetime.strptime(t, '%H:%M').time()

	now = datetime.now().time()
	next_prayer = None
	# Sort prayers by time to ensure correct order
	sorted_prayers = sorted(today_times.items(), key=lambda x: x[1] if isinstance(x[1], time) else time(0, 0))

	for prayer, prayer_time in sorted_prayers:
		if isinstance(prayer_time, time) and prayer_time > now:
			next_prayer = {
				'name': prayer.replace('_iqamah', '').capitalize(),
				'time': prayer_time.strftime('%H:%M'),
				'iqamah': today_times.get(prayer + '_iqamah').strftime('%H:%M') if today_times.get(prayer + '_iqamah') else 'N/A'
			}
			break

	context = {
		'calendar_data': calendar_data,
		'year': year,
		'month': month,
		'today_times': today_times,
		'month_name': month_name,
		'today': today,
		'next_prayer': next_prayer,
	}

	return render(request, 'prayer.html', context)










def test_page(request):
	
 
	context = {
		 
	} 
	return render(request,'test.html', context)

