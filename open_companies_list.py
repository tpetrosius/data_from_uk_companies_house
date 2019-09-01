import openpyxl

def get_companies_list():
	"""Open excel file and get companies numbers list"""
	
	companies_list = {}
	
	#Open excel file.
	wb = openpyxl.load_workbook(r"C:\Users\Vartotojas\Desktop\Projects\UK Companies House API\Companies List.xlsx")
	sheet = wb.active

	#Get all data to dictionary.
	max_row = sheet.max_row
	
	for i in range(2, max_row+1):
		company_name = sheet['A' + str(i)].value
		company_number = sheet['B' + str(i)].value
		companies_list[company_name] = [company_number]
		
	return companies_list
