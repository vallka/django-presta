from django.db import models

# Create your models here.
class DHLParcel(models.Model):
	name_ship_from = models.CharField(max_length=200,blank=True,null=True)
	company_ship_from = models.CharField(max_length=200,blank=True,null=True)
	address_1_ship_from = models.CharField(max_length=200,blank=True,null=True)
	address_2_ship_from = models.CharField(max_length=200,blank=True,null=True)
	address_3_ship_from = models.CharField(max_length=200,blank=True,null=True)
	house_number_ship_from = models.CharField(max_length=200,blank=True,null=True)
	postal_code_ship_from = models.CharField(max_length=200,blank=True,null=True)
	city_ship_from = models.CharField(max_length=200,blank=True,null=True)
	country_code_ship_from = models.CharField(max_length=200,blank=True,null=True)
	email_address_ship_from = models.CharField(max_length=200,blank=True,null=True)
	phone_country_code_ship_from = models.CharField(max_length=200,blank=True,null=True)
	phone_number_ship_from = models.CharField(max_length=200,blank=True,null=True)
	name_ship_to = models.CharField(max_length=200,blank=True,null=True)
	company_ship_to = models.CharField(max_length=200,blank=True,null=True)
	address_1_ship_to = models.CharField(max_length=200,blank=True,null=True)
	address_2_ship_to = models.CharField(max_length=200,blank=True,null=True)
	address_3_ship_to = models.CharField(max_length=200,blank=True,null=True)
	house_number_ship_to = models.CharField(max_length=200,blank=True,null=True)
	postal_code_ship_to = models.CharField(max_length=200,blank=True,null=True)
	city_ship_to = models.CharField(max_length=200,blank=True,null=True)
	state_code_ship_to = models.CharField(max_length=200,blank=True,null=True)
	country_code_ship_to = models.CharField(max_length=200,blank=True,null=True)
	email_address_ship_to = models.CharField(max_length=200,blank=True,null=True)
	phone_country_code_ship_to = models.CharField(max_length=200,blank=True,null=True)
	phone_number_ship_to = models.CharField(max_length=200,blank=True,null=True)
	account_number_shipper = models.CharField(max_length=200,blank=True,null=True)
	total_weight = models.CharField(max_length=200,blank=True,null=True)
	declared_value_currency = models.CharField(max_length=200,blank=True,null=True)
	declared_value = models.CharField(max_length=200,blank=True,null=True)
	product_code_3_letter = models.CharField(max_length=200,blank=True,null=True)
	summary_of_contents = models.CharField(max_length=200,blank=True,null=True)
	shipment_type = models.CharField(max_length=200,blank=True,null=True)
	shipment_reference = models.CharField(max_length=200,primary_key=True)
	total_shipment_pieces = models.CharField(max_length=200,blank=True,null=True)
	invoice_type = models.CharField(max_length=200,blank=True,null=True)
	length = models.CharField(max_length=200,blank=True,null=True)
	width = models.CharField(max_length=200,blank=True,null=True)
	depth = models.CharField(max_length=200,blank=True,null=True)


class UPSParcel(models.Model):
	ReferenceNumber = models.CharField(max_length=200,primary_key=True)
	Description = models.CharField(max_length=200,blank=True,null=True)
	ShipTo_AttentionName = models.CharField(max_length=200,blank=True,null=True)
	ShipTo_Name = models.CharField(max_length=200,blank=True,null=True)
	ShipTo_Address_AddressLine1 = models.CharField(max_length=200,blank=True,null=True)
	ShipTo_Address_AddressLine2 = models.CharField(max_length=200,blank=True,null=True)
	ShipTo_Address_City = models.CharField(max_length=200,blank=True,null=True)
	ShipTo_Address_CountryCode = models.CharField(max_length=200,blank=True,null=True)
	ShipTo_Address_StateCode = models.CharField(max_length=200,blank=True,null=True)
	ShipTo_Address_PostalCode = models.CharField(max_length=200,blank=True,null=True)
	ShipTo_EMailAddress = models.CharField(max_length=200,blank=True,null=True)
	ShipTo_Phone_Number = models.CharField(max_length=200,blank=True,null=True)
	Package_Weight = models.CharField(max_length=200,blank=True,null=True)
	#declared_value_currency = models.CharField(max_length=200,blank=True,null=True)
	#declared_value = models.CharField(max_length=200,blank=True,null=True)

class ShippingNumber(models.Model):
	ReferenceNumber = models.CharField(max_length=200,primary_key=True)
	ShippingNumber = models.CharField(max_length=200)

addresses = {
	'o':{
		'name':'Margarita Dobroskokina',
		'company':'GellifiQue Ltd',
		'address':'159 Great Junction Street',
		'postcode':'EH6 5LG',
		'city':'Edinburgh',
		'email':'info@gellifique.com',
		'phone_country':'44',
		'phone':'7729192470',
	},
	'h':{
		'name':'Margarita Dobroskokina',
		'company':'GellifiQue Ltd',
		'address':'41 Deantown Avenue',
		'postcode':'EH21 8NS',
		'city':'Musselburgh',
		'email':'info@gellifique.com',
		'phone_country':'44',
		'phone':'7729192470',
	},
}

def DHL_sql(ho='o',ids=''):
	sql = f"""
	    SELECT
				'{addresses[ho]['name']}' name_ship_from,
				'{addresses[ho]['company']}' company_ship_from,
				'{addresses[ho]['address']}' address_1_ship_from,
				'' address_2_ship_from,
				'' address_3_ship_from,
				'' house_number_ship_from,
				'{addresses[ho]['postcode']}' postal_code_ship_from,
				'{addresses[ho]['city']}' city_ship_from,
				'GB' country_code_ship_from,
				'{addresses[ho]['email']}' email_address_ship_from,
				'{addresses[ho]['phone_country']}' phone_country_code_ship_from,
				'{addresses[ho]['phone']}' phone_number_ship_from,
				concat(a.firstname,' ',a.lastname) name_ship_to,
				if (a.company!='',a.company,concat(a.firstname,' ',a.lastname)) company_ship_to,
				COALESCE(a.address1,'') address_1_ship_to,
				COALESCE(a.address2,'') address_2_ship_to,
				'' address_3_ship_to,
				'' house_number_ship_to,
				COALESCE(a.postcode,'') postal_code_ship_to,
				COALESCE(a.city,'') city_ship_to,
				COALESCE(if (a.id_country!=17,(select iso_code from ps17_state where id_state=a.id_state),''),'') state_code_ship_to,
				(select iso_code from ps17_country where id_country=a.id_country) country_code_ship_to,
				c.email email_address_ship_to,
				(select call_prefix from ps17_country where id_country=a.id_country) phone_country_code_ship_to,
				a.phone phone_number_ship_to,
				'420760711' account_number_shipper,
				(select sum(product_weight*product_quantity) from ps17_order_detail d where d.id_order=o.id_order) total_weight,
				(select iso_code from ps17_currency where id_currency=o.id_currency) declared_value_currency,
				if (a.id_country!=17,(o.total_paid_real-o.total_shipping_tax_incl),0) declared_value,
				if (a.id_country!=17,'WPX','DOM') product_code_3_letter,
				'Manicure Accessories' summary_of_contents,
				'P' shipment_type,
				o.reference shipment_reference,
				'1' total_shipment_pieces,
				if (a.id_country!=17,'PRO','') invoice_type,
				20 length,
				15 width,
				10 depth
			FROM ps17_orders o
				join ps17_address a on a.id_address=o.id_address_delivery
				join ps17_customer c on o.id_customer=c.id_customer
			WHERE 
	"""
	
	if ids=='':
		sql +="""
				id_carrier in (177,174)
				and 
				current_state=21
		"""
	else:
		ida = ids.split(',')
		map(lambda x:f"'{x}'" ,ida)
		ids = ','.join(ida)

		sql += f"o.id_order in ({ids})"

	sql += " ORDER BY o.id_order"

	return sql

def UPS_sql(ids):
	sql = f"""
		SELECT
			o.reference ReferenceNumber,
			concat(a.firstname,' ',a.lastname) Description,
			concat(a.firstname,' ',a.lastname) ShipTo_AttentionName,
			if (a.company!='',a.company,concat(a.firstname,' ',a.lastname,' ','Nails')) ShipTo_Name,
			COALESCE(a.address1,'') ShipTo_Address_AddressLine1,
			COALESCE(a.address2,'') ShipTo_Address_AddressLine2,
			COALESCE(a.city,'') ShipTo_Address_City,
			COALESCE(if (a.id_country!=17,(select iso_code from ps17_state where id_state=a.id_state),''),'') ShipTo_Address_StateCode,
			(select iso_code from ps17_country where id_country=a.id_country) ShipTo_Address_CountryCode,
			COALESCE(a.postcode,'') ShipTo_Address_PostalCode,
			c.email ShipTo_EMailAddress,
			a.phone ShipTo_Phone_Number,
			(select sum(product_weight*product_quantity) from ps17_order_detail d where d.id_order=o.id_order) Package_Weight
		FROM ps17_orders o
			join ps17_address a on a.id_address=o.id_address_delivery
			join ps17_customer c on o.id_customer=c.id_customer			
		WHERE 
	"""
	
	if ids=='':
		sql +="""
				id_carrier in (177,174)
				and 
				current_state=21
		"""
	else:
		ida = ids.split(',')
		map(lambda x:f"'{x}'" ,ida)
		ids = ','.join(ida)

		sql += f"o.id_order in ({ids})"

	sql += " ORDER BY o.id_order"

	return sql


def ShippingNumber_sql(ids):
	sql = f"""
		SELECT
			o.reference ReferenceNumber,
			o.shipping_number ShippingNumber
		FROM ps17_orders o
		WHERE 
	"""
	
	if ids=='':
		sql +="""
				id_carrier in (177,174)
				and 
				current_state=21
		"""
	else:
		ida = ids.split(',')
		map(lambda x:f"'{x}'" ,ida)
		ids = ','.join(ida)

		sql += f"o.id_order in ({ids})"

	sql += " ORDER BY o.id_order"

	return sql
