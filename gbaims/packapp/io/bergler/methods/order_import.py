from gbaims.packapp.api._fulfillment_order_notification import Deliverable

from .. import utils as utils
from .._client import BerglerClient


def order_import(bergler: BerglerClient, deliverable: Deliverable):
    payload = _create_payload(deliverable)
    _ = bergler.post("WebShopOrderImport", payload)


def _create_payload(deliverable: Deliverable) -> str:
    return (
        '<?xml version="1.0" encoding="utf-8" ?>'
        "<Order>"
        f"<OrderID>{deliverable['id']}</OrderID>"
        f"<OrderNumber>{deliverable['number']}</OrderNumber>"
        f"<CustomerNumber>{deliverable['customer_id']}</CustomerNumber>"
        f"<OrderDate>{utils.format_date(deliverable['date'])}</OrderDate>"
        "<HeaderText><![CDATA[]]></HeaderText>"
        "<FooterText><![CDATA[]]></FooterText>"
        "<MemoText><![CDATA[]]></MemoText>"
        # <ContactName><![CDATA[…]]></ContactName> --max 100 Zeichen optional (max 100 characters optional)
        "<Taxation></Taxation>"  # -- 1=inland;2=EU mit UStID;3=EU ohne UStID;4=Drittland (1=domestic;2=EU with VAT ID;3=EU without VAT ID;4=third country)
        "<TaxEUCountry></TaxEUCountry>"  # -- EU Land - ISO Code2 (EU country - ISO code 2)
        "<EUVATNumber></EUVATNumber>"  # -- EU-UstID (EU VAT ID)
        "<TaxNumber></TaxNumber>"  # -- Steuernummer (tax number)
        f"<OrderSum>{utils.to_german_separator(deliverable['net_amount'])}</OrderSum>"  # -- 3.432,34 (Nettowert) (net value)
        f"<OrderSumGross>{utils.to_german_separator(deliverable['gross_amount'])}</OrderSumGross>"  # -- 4.084,48 (Bruttowert) (gross value)
        # <PriceType></PriceType> --optional = Standard=-1 für Bruttopreise, 0=Nettopreise (Default=-1 for gross prices, 0=net prices)
        # <GuestOrder></GuestOrder> --optional 0=Standard,-1=Gastbestellung (0=default,-1=guest order)
        # <ShipmentCondition></ShipmentCondition> --optional DHL=DHL,DPD=DPD,Collection=Abholung,Haulier=Spedition (DHL=DHL,DPD=DPD,Collection=Collection,Haulier=Forwarding)
        # <AddRetourLabel>0</AddRetourLabel> --optional 0=false,-1=true
        "<OrderAddress>"
        # <AddrTitle></AddrTitle> -- 1=Frau 2=Herr 4=Firma (1=Mrs. 2=Mr. 4=Company)
        f"<Name1><![CDATA[{deliverable['shipping_address']['name']}]]></Name1>"  # -- z.B. Max Mustermann (John Doe)
        # <Name2><![CDATA[...]]></Name2> -- Zusatz z.B. z.H. Margit Mustermann (Jane Doe)
        f"<Street><![CDATA[{deliverable['shipping_address']['street']}]]></Street>"  # -- Strasse z.B. Hausweg 4
        f"<Street2><![CDATA[{deliverable['shipping_address']['street2']}]]></Street2>"  # -- Zusatz (Additive)
        f"<Country>{deliverable['shipping_address']['country_code']}</Country>"  # -- Land - ISO Code2 (Country - ISO code 2)
        f"<PostalCode>{deliverable['shipping_address']['postal_code']}</PostalCode>"  # -- Postleitzahl (Postal code)
        f"<City><![CDATA[{deliverable['shipping_address']['city']}]]></City>"  # -- Ort (Location)
        f"<PhoneNr>{deliverable['shipping_address']['phone']}</PhoneNr>"  # -- Telefonnummer (Phone Number)
        f"<EMail>{deliverable['shipping_address']['email']}</EMail>"  # -- E-Mail-Adresse (E-mail address)
        "</OrderAddress>"
        "<ShipmentAddress>"
        f"<Name1><![CDATA[{deliverable['shipping_address']['name']}]]></Name1>"  # -- z.B. Max Mustermann (John Doe)
        # <Name2><![CDATA[...]]></Name2> -- Zusatz z.B. z.H. Margit Mustermann (Jane Doe)
        f"<Street><![CDATA[{deliverable['shipping_address']['street']}]]></Street>"  # -- Strasse z.B. Hausweg 4
        f"<Street2><![CDATA[{deliverable['shipping_address']['street2']}]]></Street2>"  # -- Zusatz (Additive)
        f"<Country>{deliverable['shipping_address']['country_code']}</Country>"  # -- Land - ISO Code2 (Country - ISO code 2)
        f"<PostalCode>{deliverable['shipping_address']['postal_code']}</PostalCode>"  # -- Postleitzahl (Postal code)
        f"<City><![CDATA[{deliverable['shipping_address']['city']}]]></City>"  # -- Ort (Location)
        "</ShipmentAddress>"
        "<PaymentAddress>"
        f"<Name1><![CDATA[{deliverable['billing_address']['name']}]]></Name1>"  # -- z.B. Max Mustermann (John Doe)
        # <Name2><![CDATA[...]]></Name2> -- Zusatz z.B. z.H. Margit Mustermann (Jane Doe)
        f"<Street><![CDATA[{deliverable['billing_address']['street']}]]></Street>"  # -- Strasse z.B. Hausweg 4
        f"<Street2><![CDATA[{deliverable['billing_address']['street2']}]]></Street2>"  # -- Zusatz (Additive)
        f"<Country>{deliverable['billing_address']['country_code']}</Country>"  # -- Land - ISO Code2 (Country - ISO code 2)
        f"<PostalCode>{deliverable['billing_address']['postal_code']}</PostalCode>"  # -- Postleitzahl (Postal code)
        f"<City><![CDATA[{deliverable['billing_address']['city']}]]></City>"  # -- Ort (Location)
        "</PaymentAddress>"
        "<Positions>"
        f"""{"".join([(
        	"<Position>"
				f'<PositionID>{item["id"]}</PositionID>' 
				f'<ProductID>{item["inventory_item_id"]}</ProductID>' 
				f'<ProductNumber>{item["sku"]}</ProductNumber>' 
				f'<Quantity>{item["quantity"]}</Quantity>' 
				f'<Price>{utils.to_german_separator(item["price"])}</Price>' 
            "</Position>"
        ) for item in deliverable['items']])}"""
        "</Positions>"
        "</Order>"
    )
