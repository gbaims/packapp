from pydantic import BaseModel


class BerglerConfig(BaseModel):
    access_area: str
    customer_number: str
    password: str

    @property
    def url(self) -> str:
        return "https://services.fulfillment.digital/fm/services/BusinessLink.asmx?wsdl"
