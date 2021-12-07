# Description
Using a raspberry pi, camera, and a display, displays GUI prompts to check an item in/out using QR Codes and a google sheet containing item ID and check in information.

# checkIn
*  Constant camera
*	Looking for barcode
*	If len barcodes > 0
* Read barcode data
* Run through database
* Is checked out (true/false)
* Is student or teacher
* If student (student ID)
* If teacher (sub1,2,3...)
* Write to sheet
* Rows: Device ID, Is Checked Out, Last Checked Out By, Check Out Date, Check In Date, Prev ID


# To Do:
- [ ] Build Container 
- [ ] Mount project   
