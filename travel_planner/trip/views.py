from django.contrib.auth import logout, get_user_model
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from trip.models import Trip
from django.db import connection
from .helper import TripManager
from .models import Destination
from django.shortcuts import render


def user_logout(request):
    request.session['username'] = None
    request.session.clear()
    logout(request)
    return redirect('index')


class TripPlanner(View):
    template_name = 'trip.html'

    def get(self, request):
        # Fetch the destinations
        destinations = Destination.objects.all()
        return render(request, self.template_name, {'destinations': destinations})

    def post(self, request):
        user_id = request.session.get('user_id', None)
        destination_id = request.POST.get('destination')

        # Check if destination_id is not empty or null
        if destination_id:
            title = request.POST.get('title')
            description = request.POST.get('description')
            start_date = request.POST.get('start_date')

            try:
                cursor = connection.cursor()
                cursor.callproc('AddTrip', [user_id, title, destination_id, start_date, description])
                cursor.close()
                return HttpResponse('Successfully added trip')
            except Exception as e:
                return HttpResponseServerError("Internal Server Error", e)
        else:
            return HttpResponseBadRequest("Please select a destination")


class TripUpdateView(View):
    template_name = 'home.html'

    def post(self, request, trip_id):
        title = request.POST.get('title')
        description = request.POST.get('description')
        destination = request.POST.get('destination')
        start_date = request.POST.get('start_date')

        success, message = TripManager.update_trip(trip_id, title, destination, description, start_date)
        if success:
            return redirect('index')
        else:
            return render(request, self.template_name, {'message': message}, status=500)


class TripDeleteView(View):
    def post(self, request, trip_id):
        print(trip_id, 'trip_id')
        success, message = TripManager.delete_trip(trip_id)
        if success:
            return HttpResponse(message)
        else:
            return HttpResponse(message, status=500)


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        trips = Trip.objects.all()
        destinations = Destination.objects.all()
        context = {'trips': trips, 'destinations': destinations}
        return render(request, self.template_name, context)
