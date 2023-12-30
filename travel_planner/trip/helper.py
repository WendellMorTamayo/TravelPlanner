from django.db import connection
from django.db import connection, IntegrityError, OperationalError


class TripManager:
    @staticmethod
    def get_all_trips():
        with connection.cursor() as cursor:
            try:
                cursor.execute("CALL GetAllTrips")
                trips = dictfetchall(cursor)
                return trips
            except Exception as e:
                print(f"Error retrieving trips: {e}")
                return []

    @staticmethod
    def add_trip(user_id, destination, start_date, description):
        with connection.cursor() as cursor:
            try:
                cursor.callproc('AddTrip', [user_id, destination, start_date, description])
                return True, 'Successfully added trip'
            except IntegrityError as integrity_error:
                print(f"IntegrityError adding trip: {integrity_error}")
                return False, 'Failed to add trip: IntegrityError'
            except OperationalError as operational_error:
                print(f"OperationalError adding trip: {operational_error}")
                return False, 'Failed to add trip: OperationalError'
            except Exception as e:
                print(f"Error adding trip: {e}")
                return False, 'Failed to add trip'

    @staticmethod
    def update_trip(trip_id, title, destination, description, start_date):
        with connection.cursor() as cursor:
            try:
                cursor.callproc('ModifyTrip', [trip_id, title, destination, description, start_date])
                return True, 'Trip updated successfully'
            except Exception as e:
                print(f"Error updating trip: {e}")
                return False, 'Failed to update trip'

    @staticmethod
    def delete_trip(trip_id):
        with connection.cursor() as cursor:
            try:
                cursor.callproc('DeleteTrip', [trip_id, 1])
                return True, 'Trip deleted successfully'
            except Exception as e:
                print(f"Error deleting trip: {e}")
                return False, 'Failed to delete trip'


