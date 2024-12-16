from datetime import datetime, date, time, timedelta

from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from booking_manager.database.db import get_database
from booking_manager.controllers.base_controller import BaseController
from booking_manager.database.schemas.booking_schema import BookingSchema


# class BookingService:
    # @staticmethod
    # async def create_booking(booking_request:dict):
    #     try:
    #         bookings_collection = get_database()["bookings"]
    #
    #         service_id = booking_request.get("service_id")
    #         if not ObjectId.is_valid(service_id):
    #             return BaseController.bad_request("Invalid service ID provided.")
    #
    #         # Convert created_on fields to datetime
    #         current_datetime = datetime.now()
    #         created_on_date = current_datetime.strftime("%Y-%m-%d")  # Convert to ISO 8601 string
    #         created_on_time = current_datetime.strftime("%H:%M:%S.%f")  # Use full datetime for created_on_time
    #
    #         booking_data = {
    #             "service_id": booking_request.get("service_id"),
    #             "user_id": booking_request.get("user_id"),
    #             "booking_date": booking_request.get("booking_date"),
    #             "booking_start_time": booking_request.get("booking_start_time"),
    #             "booking_end_time": booking_request.get("booking_end_time"),
    #             "booking_type": booking_request["booking_type"],
    #             "status": booking_request.get("status", "Pending"),
    #             "created_on_date": created_on_date,
    #             "created_on_time": created_on_time,
    #             "created_by": booking_request.get("created_by"),
    #             "paid_status": booking_request.get("paid_status", False),
    #         }
    #
    #         booking_date = booking_request.get("booking_date")
    #         if isinstance(booking_date, date):  # Check if it's a `date` object
    #             booking_data["booking_date"] = booking_date.strftime("%Y-%m-%d")
    #
    #         booking_start_time = booking_request.get("booking_start_time")
    #         if isinstance(booking_start_time, time):  # Check if it's a `time` object
    #             booking_data["booking_time"] = booking_start_time.strftime("%H:%M:%S.%f")
    #
    #         booking_end_time = booking_request.get("booking_end_time")
    #         if isinstance(booking_end_time, time):  # Check if it's a `time` object
    #             booking_data["booking_end_time"] = booking_end_time.strftime("%H:%M:%S.%f")
    #
    #         print(f"Created On Date (string): {created_on_date}")
    #         print(f"Created On Time (string): {created_on_time}")
    #         print(f"Booking Date (string): {booking_date}")
    #         print(f"Booking Time (string): {booking_start_time}")
    #
    #         print("Booking Data Prepared for Insertion:", booking_data)
    #
    #         result = bookings_collection.insert_one(booking_data)
    #
    #         if not result.acknowledged:
    #             return BaseController.bad_request("Failed to create booking.")
    #
    #         created_booking = bookings_collection.find_one({"_id": result.inserted_id})
    #         if created_booking:
    #             created_booking["_id"] = str(created_booking["_id"])
    #             # created_booking["service_id"] = str(created_booking["service_id"])
    #             # created_booking["user_id"] = str(created_booking["user_id"])
    #             # created_booking["created_by"] = str(created_booking["created_by"])
    #
    #         return BaseController.success(jsonable_encoder(created_booking), "Booking created successfully.")
    #
    #     except ValueError as ve:
    #     # Handle validation-specific errors
    #         return BaseController.ise(ve)
    #
    #     except Exception as e:
    #     # Handle all other errors
    #         return BaseController.ise(e)

    # @staticmethod
    # async def create_booking(booking_request:BookingSchema):
    #     try:
    #         bookings_collection = get_database()["bookings"]
    #         schedules_collection = get_database()["schedules"]
    #
    #         service_id = booking_request.service_id
    #         if not ObjectId.is_valid(service_id):
    #             return BaseController.bad_request("Invalid service ID provided.")
    #
    #         current_datetime = datetime.now()
    #         booking_request.created_on_date = current_datetime.date()
    #         booking_request.created_on_time = current_datetime.time()
    #
    #         booking_data = booking_request.model_dump(exclude_unset=True)  # Get data from the schema
    #
    #         booking_data["created_on_date"] = booking_data["created_on_date"].isoformat()  # Convert to string
    #         booking_data["created_on_time"] = booking_data["created_on_time"].isoformat()  # Convert to string
    #         booking_data["booking_date"] = booking_data["booking_date"].isoformat()
    #         print(booking_request.booking_date.isoformat())
    #
    #         schedule = schedules_collection.find_one(
    #             {"service_id": booking_request.service_id, "date": booking_request.booking_date.isoformat()})
    #
    #         if not schedule:
    #             print("Schedule not found for service_id:", booking_request.service_id)
    #             return BaseController.bad_request("No schedule found for the given service ID and date.")
    #
    #         requested_slots = [
    #             f"{booking_request.booking_start_time.strftime('%H:%M')}-{booking_request.booking_end_time.strftime('%H:%M')}"
    #         ]
    #
    #         if any(slot not in schedule["available_slots"] for slot in requested_slots):
    #             print("Unavailable slots:", requested_slots)
    #             return BaseController.bad_request("One or more requested time slots are not available.")
    #
    #         schedule["available_slots"] = [slot for slot in schedule["available_slots"] if slot not in requested_slots]
    #         schedule.setdefault("booked_slots", []).extend(requested_slots)
    #
    #         update_result = schedules_collection.update_one({"_id": schedule["_id"]}, {"$set": {
    #             "available_slots": schedule["available_slots"],
    #             "booked_slots": schedule["booked_slots"]
    #         }})
    #
    #         print("Schedule update result:", update_result.modified_count)
    #
    #         result = bookings_collection.insert_one(booking_data)
    #
    #         if not result.acknowledged:
    #             return BaseController.bad_request("Failed to create booking.")
    #
    #         created_booking = bookings_collection.find_one({"_id": result.inserted_id})
    #         if created_booking:
    #             # Convert ObjectId to string
    #             created_booking["_id"] = str(created_booking["_id"])
    #
    #         return BaseController.success(jsonable_encoder(created_booking), "Booking created successfully.")
    #
    #     except ValueError as ve:
    #         # Handle validation-specific errors
    #         return BaseController.ise(ve)
    #
    #     except Exception as e:
    #         # Handle all other errors
    #         return BaseController.ise(e)

class BookingService:
    @staticmethod
    async def create_booking(booking_request: BookingSchema):
        """Create booking api"""
        try:
            # Connect to MongoDB collections
            bookings_collection = get_database()["bookings"]
            schedules_collection = get_database()["schedules"]

            service_id = booking_request.service_id

            # Validate service_id as a string (since you're not using ObjectId for it)
            if not isinstance(service_id, str):
                return BaseController.bad_request("Invalid service ID provided.")

            # Convert start and end times to consistent formats
            booking_start_time_str = booking_request.booking_start_time.strftime("%H:%M")
            booking_end_time_str = booking_request.booking_end_time.strftime("%H:%M")

            # Assign current datetime for creation fields
            current_datetime = datetime.now()
            booking_request.created_on_date = current_datetime.strftime("%Y-%m-%d")
            booking_request.created_on_time = current_datetime.strftime("%H:%M:%S")

            # Prepare booking date
            booking_date = str(booking_request.booking_date)

            # Prepare booking data for insertion
            booking_data = booking_request.model_dump(exclude_unset=True)
            booking_data["created_on_date"] = booking_request.created_on_date
            booking_data["created_on_time"] = booking_request.created_on_time
            booking_data["booking_date"] = booking_date

            print(f"Querying schedules with service_id: {service_id} and date: {booking_date}")

            # Query the schedules collection
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

            # Extract schedule details
            available_slots = schedule.get("available_slots", [])
            booked_slots = schedule.get("booked_slots", [])
            minimum_slot = schedule.get("minimum_slot", 15)

            # Generate booking slots
            booking_slots = []
            current_slot = booking_start_time_str
            while current_slot < booking_end_time_str:
                next_slot = (datetime.strptime(current_slot, "%H:%M") + timedelta(minutes=minimum_slot)).strftime(
                    "%H:%M")
                booking_slots.append(f"{current_slot}-{next_slot}")
                current_slot = next_slot

            # Check if all requested slots are available
            if not all(slot in available_slots for slot in booking_slots):
                return BaseController.bad_request("One or more requested slots are not available.")

            # Update the schedule document
            update_result = schedules_collection.update_one(
                {"_id": schedule["_id"], "available_slots": {"$all": booking_slots}},
                {
                    "$pull": {"available_slots": {"$in": booking_slots}},
                    "$push": {"booked_slots": {"$each": booking_slots}}
                }
            )

            if update_result.matched_count == 0:
                return BaseController.bad_request("Failed to update schedule. Slots may have been booked already.")

            # Insert booking into the bookings collection
            # Ensure all datetime objects are serialized to strings
            booking_data = jsonable_encoder(booking_data)
            result = bookings_collection.insert_one(booking_data)

            if not result.acknowledged:
                return BaseController.bad_request("Failed to create booking.")

            # Retrieve and return the created booking
            created_booking = bookings_collection.find_one({"_id": result.inserted_id})
            if created_booking:
                created_booking["_id"] = str(created_booking["_id"])
                return BaseController.success(jsonable_encoder(created_booking), "Booking created successfully.")

        except Exception as e:
            return BaseController.ise(e)







