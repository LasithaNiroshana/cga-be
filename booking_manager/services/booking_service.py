from datetime import datetime, date, time, timedelta

from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from booking_manager.database.db import get_database
from booking_manager.controllers.base_controller import BaseController
from booking_manager.database.schemas.booking_schema import BookingSchema

class BookingService:
    @staticmethod
    async def create_booking(booking_request: BookingSchema):
        """Create booking API"""
        try:
            bookings_collection = get_database()["bookings"]
            schedules_collection = get_database()["schedules"]

            service_id = booking_request.service_id

            if not isinstance(service_id, str):
                return BaseController.bad_request("Invalid service ID provided.")

            # Convert start and end times to consistent formats
            booking_start_time_str = booking_request.booking_start_time.strftime("%H:%M")
            booking_end_time_str = booking_request.booking_end_time.strftime("%H:%M")

            current_datetime = datetime.now()
            booking_request.created_on_date = current_datetime.strftime("%Y-%m-%d")
            booking_request.created_on_time = current_datetime.strftime("%H:%M:%S")

            booking_date = str(booking_request.booking_date)

            booking_data = booking_request.model_dump(exclude_unset=True)
            booking_data["created_on_date"] = booking_request.created_on_date
            booking_data["created_on_time"] = booking_request.created_on_time
            booking_data["booking_date"] = booking_date

            print(f"Querying schedules with service_id: {service_id} and date: {booking_date}")

            schedule = schedules_collection.find_one({
                "service_id": service_id,
                "date": booking_date
            })

            if not schedule:
                print(f"No schedule found for service_id: {service_id} and date: {booking_date}")
                return BaseController.bad_request(
                    f"Schedule not found for service_id: {service_id} and date: {booking_date}"
                )

            print(f"Schedule retrieved: {schedule}")

            available_slots = schedule.get("available_slots", [])
            booked_slots = schedule.get("booked_slots", [])
            minimum_slot = schedule.get("minimum_slot", 15)

            booking_slots = []
            current_slot = booking_start_time_str
            while current_slot < booking_end_time_str:
                next_slot = (datetime.strptime(current_slot, "%H:%M") + timedelta(minutes=minimum_slot)).strftime(
                    "%H:%M")
                booking_slots.append(f"{current_slot}-{next_slot}")
                current_slot = next_slot

            if not all(slot in available_slots for slot in booking_slots):
                return BaseController.bad_request("One or more requested slots are not available.")

            update_result = schedules_collection.update_one(
                {"_id": schedule["_id"], "available_slots": {"$all": booking_slots}},
                {
                    "$pull": {"available_slots": {"$in": booking_slots}},
                    "$push": {"booked_slots": {"$each": booking_slots}}
                }
            )

            if update_result.matched_count == 0:
                return BaseController.bad_request("Failed to update schedule. Slots may have been booked already.")

            booking_data = jsonable_encoder(booking_data)
            result = bookings_collection.insert_one(booking_data)

            if not result.acknowledged:
                return BaseController.bad_request("Failed to create booking.")

            created_booking = bookings_collection.find_one({"_id": result.inserted_id})
            if created_booking:
                created_booking["_id"] = str(created_booking["_id"])
                return BaseController.success(jsonable_encoder(created_booking), "Booking created successfully.")

        except Exception as e:
            return BaseController.ise(e)







