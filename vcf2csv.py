import re
import numpy as np
import pandas as pd

with open('source_directory/contacts.vcf') as file:
    contact_list = []
    contact_field_list = ['N', 'FN', 'TEL', 'ADR']
    contact_dict = {'first_name': np.NaN, 'last_name': np.NaN, 'full_name': np.NaN, 'address': np.NaN, 
                    'address_type': np.NaN, 'phone': np.NaN, 'phone_type': np.NaN, 'preferred_address': np.NaN, 
                    'preferred_phone': np.NaN}
    adr_count = 0
    phone_count = 0
    contact_count = 0
    dict_contact_field = ''
    
    whitespace_re = re.compile('^\w')
    type_cleanup = re.compile('([^type=:]\w+)')
    
    for i, line in enumerate(file.readlines(), start=1):
        # if i == 50:
            # break

        if whitespace_re.search(line):
            contact_field = re.split(':|;', line)[0]
            line_elements = []
            contact_count += 1

            # identify the ADR field(s)
            if re.search('item\d+.ADR', contact_field):
                contact_field = 'ADR'
                if adr_count > 0:
                    contact_list.append(contact_dict)
                line_elements = [item.replace('\n', '') for item in line.split(';')[1:]]
                address_type = type_cleanup.findall(line_elements[0])[0]
                address = ','.join(line_elements[2:])
                
                if 'type=pref' in line_elements[1]:
                    preferred_address = 1
                else:
                    preferred_address = 0
                    
                contact_dict['preferred_address'] = preferred_address
                contact_dict['address_type'] = address_type
                contact_dict['address'] = address
                
                adr_count += 1
            if contact_field == 'TEL':
                if phone_count > 0:
                    contact_list.append(contact_dict)
                    
                line_elements = [item.replace('\n', '') for item in re.split(';|:', line)[1:]]
                phone_type = type_cleanup.findall(line_elements[0])[0]
                phone = line_elements[-1]
                
                if len(line_elements) > 3:
                    preferred_phone = 1
                elif len(line_elements) == 1:
                    phone_type = np.NaN
                    preferred_phone = 0
                else:
                    preferred_phone = 0
                    
                contact_dict['preferred_phone'] = preferred_phone
                contact_dict['phone_type'] = phone_type
                contact_dict['phone'] = phone
                
                phone_count += 1
                # print(contact_field, line_elements)
            elif contact_field == 'N':
                line_elements = [item.replace('N:', '') for item in line.split(';') if item not in ['\n']]
                first_name = line_elements[1]
                last_name = line_elements[0]
                contact_dict['first_name'] = first_name
                contact_dict['last_name'] = last_name
                # print(contact_field, line_elements)
            elif contact_field == 'FN':
                full_name = [item.replace('\n', '') for item in line.split(':')[1:]][0]
                contact_dict['full_name'] = full_name
                # print(contact_field, line_elements)
            if contact_count > 0:
                contact_dict = {'first_name': first_name, 'last_name': last_name, 'full_name': full_name, 
                                    'address': np.NaN, 'address_type': np.NaN, 'phone': np.NaN, 'phone_type': np.NaN, 
                                    'preferred_address': np.NaN, 'preferred_phone': np.NaN}

            elif contact_field == 'END':
                contact_list.append(contact_dict)
                adr_count = 0
                phone_count = 0
                contact_count = 0
                first_name = np.NaN
                last_name = np.NaN
                full_name = np.NaN
                phone = np.NaN
                phone_type = np.NaN
                preferred_phone = np.NaN
                address = np.NaN
                address_type = np.NaN
                preferred_address = np.NaN
                # print(contact_dict)
                # print('*' * 20)
                contact_dict = {'first_name': np.NaN, 'last_name': np.NaN, 'full_name': np.NaN, 
                                    'address': np.NaN, 'address_type': np.NaN, 'phone': np.NaN, 'phone_type': np.NaN, 
                                    'preferred_address': np.NaN, 'preferred_phone': np.NaN}
            
df = pd.DataFrame(contact_list)
df.to_csv(f'destination_dir/contacts.csv', index=False)
