from pydantic import BaseModel

class Booking(BaseModel):
    id:str
    booking_type:str
    booking_time:str
    booking_date:str
    status:str
    booking_source:str
    created_by:str
    created_on_time:str
    created_on_date:str
    

