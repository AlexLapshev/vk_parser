import requests
import csv

import re

# id of vk group
group_id = ''
# vk api
group_url = 'https://api.vk.com/method/groups.getMembers?group_id={}&v=5.52'.format(group_id)
# vk access key
TOKEN = ''

# all users of the group
users_ids = requests.get(group_url, params={'access_token': TOKEN}).json()['response']['items']
user_url = 'https://api.vk.com/method/users.get?user_id={}&v=5.52'

# checking mobile phone
re_exp = r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'

# writing in a csv file


def csv_writer(arr):
	with open('vk_phones.csv', 'a', newline='') as csv_file:
		writer = csv.writer(csv_file, delimiter=';')
		writer.writerows(arr)


def main():
	for user in users_ids[500:1500]:
		user_info = requests.get(user_url.format(user), params={'access_token': TOKEN, 'fields': [
			'city', 'contacts',
		]}).json()
		if user_info['response'][0].get('mobile_phone'):
			mobile_phone = user_info['response'][0].get('mobile_phone')
			if re.match(re_exp, mobile_phone):
				first_name = user_info['response'][0]['first_name']
				last_name = user_info['response'][0]['last_name']
				user_id = 'http://vk.com/id{}'.format(user_info['response'][0]['id'])
				arr = [[i for i in (first_name, last_name, user_id, mobile_phone)]]
				csv_writer(arr)


if __name__ == '__main__':
	main()