
from database import Base, engine

from models.admin import Admin
from models.aircraft import Aircraft, AircraftImage
from models.sales_team import SalesTeam
from models.support import SupportTicket
from models.operation_profile import OperationProfile
from models.operators_profile import OperatorsProfile

from models.request import CustomerRequest, SalesRequest
from models.request_document import (
    CustomerRequestDocument,
    SalesRequestDocument,
)
from models.request_timeline import (
    CustomerRequestTimeline,
    SalesRequestTimeline,
)

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully or already exist!")


if __name__ == "__main__":
    create_tables()
