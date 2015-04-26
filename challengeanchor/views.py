import colander

from pyramid.view import view_config
from pyramid.renderers import get_renderer

from deform import Form, ValidationFailure

class Challenge(object):
	def __init__(self, request):
		self.request = request

	def site_layout(self):
	    renderer = get_renderer("templates/layout.pt")
	    layout = renderer.implementation().macros['layout']
	    return layout

	@view_config(route_name='home', renderer='templates/index.pt')
	def home(self):
	    return {'layout': self.site_layout(),
	            'content': 'Sorry, we have nothing for you. Send me a file. ;)'}

	@view_config(route_name='uploadFile', renderer='templates/index.pt')
	def upload_file(self):
		result = []
		if 'Upload' in self.request.POST:
			try:
				uploadedFile = self.request.POST.get('file')
				contentFile = uploadedFile.file.readlines()
				coins = contentFile[0].split(' ')
				
				for coin in coins:
					result.append(str(self.coin_determiner(int(coin))))

			except Exception:
				result.append('You need to select a file.')

	        return {'layout': self.site_layout(),
	            	'content': ' - '.join(result)}

	def coin_determiner(self, num):
	    coins = [1, 5, 7, 9, 11]
	    arr_coins = []
	    total_coins = 0
	    sum_ = 0
	    index = len(coins)-1

	    while(sum_ != num):
	        try:
	            if(sum(arr_coins) + coins[index] <= num):
	                arr_coins.append(coins[index])
	                total_coins += 1
	                sum_ = sum(arr_coins)
	                index -= 1
	            else:
	                index -= 1
	        except IndexError:
	            return total_coins-1

	    return total_coins
