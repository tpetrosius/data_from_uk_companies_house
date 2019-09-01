import requests


def get_company_info(company_number):
	"""Calls API and returns company data"""
	company_info = {}
	data_points = {'Company Name': 'company_name', 'Company Number': 'company_number',
					'Date of Creation': 'date_of_creation', 'Company Status': 'company_status',
					'Jurisdiction': 'jurisdiction', 'Type': 'type', 'Registered office address': 'registered_office_address'}
	
	url = 'https://api.companieshouse.gov.uk/company/' + company_number
	get_info = requests.get(url, auth=('OZ7xEXg13wiq6sjvck3FBW_DwoQm8MSxjdUjyiqJ', ''))

	#print("Status code:", get_info.status_code)

	if get_info.status_code != 200:
		print("Unable to make API call to get company information.")
		return company_info
		
	else:
		company_info_dict = get_info.json()
		
		for key in data_points.keys():
			if key != 'Registered office address':
				if data_points[key] in company_info_dict:
					company_info[data_points[key]] = company_info_dict[data_points[key]]
				else:
					company_info[data_points[key]] = 'None'
			else:
				#Combine address
				address = ''
				if 'address_line_1' in company_info_dict[data_points[key]]:
					address = address + company_info_dict[data_points[key]]['address_line_1'] + ', '
				
				if 'postal_code' in company_info_dict[data_points[key]]:
					address = address + company_info_dict[data_points[key]]['postal_code'] + ', '
				
				if 'locality' in company_info_dict[data_points[key]]:
					address = address + company_info_dict[data_points[key]]['locality'] + ', '
					
				if 'country' in company_info_dict[data_points[key]]:
					address = address + company_info_dict[data_points[key]]['country']
				else:
					address = address + 'United Kingdom'
				
				company_info[data_points[key]] = address
				
	return company_info
	
def get_significant_ownership(company_number):
	"""Calls API and return company's significant ownership"""
	ownership = {}
	url = 'https://api.companieshouse.gov.uk/company/' + company_number + '/persons-with-significant-control'
	get_ownership = requests.get(url, auth=('OZ7xEXg13wiq6sjvck3FBW_DwoQm8MSxjdUjyiqJ', ''))

	if get_ownership.status_code != 200:
		print("Unable to make API call to get company's significant ownership.")
		return ownership
		
	else:
		company_ownership = get_ownership.json()
		#print(company_ownership)
		
		items = company_ownership['items']
		total_results = len(items)
		entry = 0
		
		while entry < total_results:
		
			person_number = entry + 1
			ownership[person_number] = {}
			
			#Get name and add to dictionary
			try:
				name = items[entry]['name']
				ownership[person_number]['name'] = name
			except KeyError:
				ownership[person_number]['name'] = 'None'
			
			#Get nationality and add to dictionary
			try:
				nationality = items[entry]['nationality']
				ownership[person_number]['nationality'] = nationality
			except KeyError:
				ownership[person_number]['nationality'] = 'None'
			
			#Get date of birth and add it to dictionary
			try:
				raw_date_of_birth = items[entry]['date_of_birth']
				date_of_birth = str(raw_date_of_birth['year']) + '-' + str(raw_date_of_birth['month'])
				ownership[person_number]['date_of_birth'] = date_of_birth
			except KeyError:
				ownership[person_number]['date_of_birth'] = 'None'
			
			#Get ownership and voting rights
			try:
				rights = items[entry]['natures_of_control']
				ownership_rights = rights[0]
				try:
					voting_rights = rights[1]
				except IndexError:
					voting_rights = 'None'
					
				#ownership rights and voting rights
				ownership[person_number]['ownership_rights'] = ownership_rights.replace('-', ' ')
				ownership[person_number]['voting_rights'] = voting_rights.replace('-', ' ')
			except KeyError:
				ownership[person_number]['ownership_rights'] = 'None'
				ownership[person_number]['voting_rights'] = 'None'
				
			entry += 1
			
			if entry > total_results:
				break
	
	return ownership
