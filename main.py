from open_companies_list import get_companies_list
from uk_companies_house_api import get_company_info, get_significant_ownership
from create_excel_for_company import create_excel

#Get dictionary of companies' numbers from excel file
print('Getting list of companies'' numbers...\n\n')
companies_list = get_companies_list()

report_number = 1

#Call API, get data and write it in separate excel
for company_name, company_number in companies_list.items():
	print('Making API call for ' + str(report_number) + ' company...\n\n')
	company_info = get_company_info(company_number[0])
	
	if len(company_info) == 0:
		print('Cannot receive information for ' + company_name + '.\n\n')
		report_number += 1
		continue

	ownership = get_significant_ownership(company_number[0])
	print('Creating excel file for ' + str(report_number) + ' company...\n\n') 
	report = create_excel(company_info, ownership)
	print('Finished creating report...\n\n')
	report_number += 1
