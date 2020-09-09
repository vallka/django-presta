import json
import pprint
import requests
import base64
from PIL import Image






def processItem(dat,rn):
    newHeaders = {
        'Content-type': 'application/json', 
        'Accept': 'application/json',
        'Username': 'info@gellifique.com',
        'Password': 'Dobroskokina1',
        'AccessLicenseNumber': 'BD878DD5B5667B91',
        'transId': 'Transaction001',
        'transactionSrc': 'test'
    }



    #response = requests.post(' https://onlinetools.ups.com/ship/v1807/shipments',data=json.dumps(dat),headers=newHeaders)
    response = requests.post(' https://wwwcie.ups.com/ship/v1807/shipments',data=json.dumps(dat),headers=newHeaders)

    print("Status code: ", response.status_code)

    with open(f"{rn}.json", "w") as file:
        file.write(response.text)

    jsn = json.loads(response.text)

    pprint.pprint(jsn["ShipmentResponse"]["ShipmentResults"]["NegotiatedRateCharges"])

    pprint.pprint(jsn["ShipmentResponse"]["ShipmentResults"]["ShipmentIdentificationNumber"])
    

    with open(f"{rn}.gif", "wb") as file:
        file.write(base64.b64decode(jsn["ShipmentResponse"]["ShipmentResults"]["PackageResults"]["ShippingLabel"]["GraphicImage"]))    

    pdf = Image.open(f"{rn}.gif")    
    pdf.save(f"{rn}.pdf", "PDF" ,resolution=100.0, save_all=True)




with open("ups.json", "r") as read_file:
    data = json.load(read_file)

pprint.pprint(data)


for p in data:
    rn = p['ShipmentRequest']['Shipment']['ReferenceNumber']['Value']
    print (rn)
    processItem(p,rn)
