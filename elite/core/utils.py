from vocabulary.models import UserVocabulary, Word
from reading.models import UserReading
from usermanager.models import UserProfile
from tips.models import UserTips, Tips, TipsModule
from django.contrib.auth.models import User
import nltk
from nltk.corpus import wordnet
from training.models import TipsTrainingLevel, TipsTraining, UserTipsTraining



def get_user_by_auth_user(user):
	if isinstance(user, User):
		return user.profile
	else:
		return user

# ******* study history *******
def get_words_study_history(user, span = 10):
	'''
		@return:
			list of # of words studied for each day between [now - span, now]
	'''
	uv = get_uservocabulary(user)

	return uv.get_study_history(span)

def get_reading_study_history(user, span = 10):
	'''
		@return:
			list of # of words studied for each day between [now - span, now]
	'''
	ur = get_userreading(user)
	return ur.get_study_history(span)


# ******* user vocabulary ********
def get_uservocabulary(user):
	"""
		Return UserVocabulary according to auth_user.
		If UserVocabulary of user does not exist, create one.

		@param
			user : User
		@return
			UserVocabulary of user
	"""
	# print type(user)
	if isinstance(user, User):
		userProfile = user.profile
		if userProfile is None:
			print "no profile @get_uservocabulary"
			return None
	else:
		userProfile = user

	try:
		uv = userProfile.uservocabulary


	except UserVocabulary.DoesNotExist, e:
		print "new vocabulary", str(e)
		uv = UserVocabulary.objects.create(userProfile = userProfile)
		# uv.initialize_new_words()
		uv.initialize_new_words('TOEFL')
		uv.set_count_of_reviews_and_new_words(reviews = 50, new_words = 50)
		profile = get_user_by_auth_user(user)
		profile.set_have_testing_true()
	except Exception, e:
		print str(e)


		#print traceback.format_exc()
	#else:
		#print ("fatal error")
		#pass
	return uv

def get_now_book(user):
	uv = get_uservocabulary(user)
	return uv.book

def initialize_new_words(user, book):
	uv = get_uservocabulary(user)
	uv.initialize_new_words(book)

def add_unfimiliar_word(user, literal_word):
	
	try:
		literal_word = lemmatizer(literal_word)
		word = Word.objects.get(english_word = literal_word)
	except Exception, e:
		print "error", e
		return None
	uv = get_uservocabulary(user)
	uv.add_unfimiliar_word(word)
	return word

def query_word(literal_word):
	try:
		literal_word = lemmatizer(literal_word)
		word = Word.objects.get(english_word = literal_word)
		return word
	except Exception, e:
		print "error", e
		return None

def get_userreading(user):
	"""
		Return UserReading according to User.
		If UserReading of a_user does not exist, create one.

		@param
			a_user : User
		@return
			UserVocabulary of a_user
	"""
	# try:
	# 	user = User.objects.get(auth_user = auth_user)
	# except User.DoesNotExist:
	# 	print "none user @get_userreading"
	# 	return None
	uv = get_uservocabulary(user)
	if isinstance(user, User):
		userProfile = user.profile
		if userProfile is None:
			print "no userProfile @get_userreading"
			return None
	else:
		userProfile = user
	try:
		userreading = userProfile.userreading
	except UserReading.DoesNotExist:
		print "create UserReading"
		userreading = UserReading.objects.create(userProfile = userProfile)
	except Exception, e:
		print str(e)

		#print traceback.format_exc()
	#else:
		#print ("fatal error")
		#pass
	return userreading

# ********* tips **********




def get_tips_modules():
	"""
		@return:
			a list of string
	"""
	return TipsModule.get_all_modules()

def get_tips_levels_of_module(module):
	"""
		@return:
			a list of string
	"""
	return TipsModule.get_levels_of_module(module = module)

def get_tips_items_of_level(module, level):
	"""
		@return:
			a list of string
	"""
	return TipsModule.get_items_of_level(module = module, level = level)

def get_tips_all_items():
	"""
		@return:
			a list of TipsModule instance:
			the attributes includes:
				module, module_index, level, level_index, item, item_index
	"""
	return TipsModule.get_all()

def get_tips_content_of_item(module, level, item):
	tips = Tips.objects.get_tips(module = module, level = level, item = item)
	if tips:
		return tips.get_description()

	# ****** user-related *******

def get_usertips(user):
	if isinstance(user, User):
		userProfile = user.profile
		if userProfile is None:
			print "no userProfile @get_usertips"
			return None
	else:
		userProfile = user
	try:
		usertips = userProfile.usertips
	except usertips.DoesNotExist:
		print "error no usertips@get_usertips"
		raise
	return usertips

def update_tips_a_look(user, module, level, item):
	userTips = get_usertips(user)
	if userTips:
		userTips.look_a_tips(module = module, level = level, item = item)

def get_looked_tips(user):
	'''
		@return:
			a list of Tips instance.
			the attributes includes:
				content, module, level, item, item_index
	'''
	userTips = get_usertips(user)
	if userTips:
		return userTips.get_looked_tips()



# def get_next_x_tips(user, x, module, level = ''):
# 	userTips = get_usertips(user)
# 	return userTips.get_next_x_tips(module = module, x = x, level = level)

# def update_next_x_tips(user, x, module, level = ''):
# 	userTips = get_usertips(user)
# 	return userTips.update_next_x_tips(x = x, module = module, level = level)

# def collect_tips(user, module, level, order):
# 	userTips = get_usertips(user)
# 	userTips.collect_tips(module, level, order)

# def get_collected_tips(user, module = '', level = ''):
# 	userTips = get_usertips(user)
# 	return userTips.get_collected_tips(module = module, level = level)

# def get_all_modules_of_tips():
# 	return  TipsModule.all_modules()

# def get_levels_of_module(module):
# 	return TipsModule.get_levels(module = module)

# ******** tips over ***********




# ********* tipstraiing **********

def get_all_modules_of_tipstraining():
	return TipsTrainingLevel.all_modules()

def get_training_of_module(module):
	return TipsTrainingLevel.trainging_of_module(module)


# shouldn't call it directly
def get_tipstraining(training, module = ""):
	return TipsTraining.objects.tipstraining(module = module, training = training)

def get_tutorial_of_training(training, module = ""):
	tipstraining = get_tipstraining(training = training)
	if tipstraining is None:
		print "no such tipstraining"
		return None
	return tipstraining.get_introduction()

def get_questions_of_training(training, module = ""):
	tipstraining = get_tipstraining(training = training)
	if tipstraining is None:
		print "no such tipstraining"
		return None
	return tipstraining.get_questions()

def get_questions_of_training_by_index(index, training, module = ""):
	tipstraining = get_tipstraining(training =training)
	if tipstraining is None:
		print "no such tipstraining"
		return None
	return tipstraining.get_question_by_index(index = index)


	# ****** user_related ********

# shouldn't call it directly
def get_usertipstraining(user):
	userProfile = get_user_by_auth_user(user)
	return userProfile.usertipstraining

def get_next_x_questions_by_order(user, x, training, module = ""):
	usertipstraining = get_usertipstraining(user)
	if usertipstraining is None:
		print "no such usertipstraining"
		return None
	return usertipstraining.get_next_x_questions_by_order(x = x, training = training)

def update_x_questions(user, data, training, module = ""):
	usertipstraining = get_usertipstraining(user)
	if usertipstraining is None:
		return None
	return usertipstraining.update_x_questions(training = training, module =module, data = data)

def get_done_questions(user, training, module = ""):
	usertipstraining = get_usertipstraining(user)
	if usertipstraining is None:
		return None
	return usertipstraining.get_done_questions(training = training, module = module)


# ********* tipstraiing over**********



def split_text(text):
	"""
		split text, return list of words.
		@param
			text : string
		@return
			list of string
	"""
	pattern = r'''(?x)
     ([A-Z]\.)+
   	| \w+(-\w+)*
   	| \$?\d+(\.\d+)?%?
   	| \n
	| [][.,;"'?():-_`<>]
	| \.\.\.
	'''
	words = nltk.regexp_tokenize(text, pattern)
	return words


def lemmatizer(word):
	"""
		lowercase and lemmatizer
		@param
			word : string
		@return
			word : string
	"""
	lemma = nltk.wordnet.WordNetLemmatizer()
	return lemma.lemmatize(lemma.lemmatize(lemma.lemmatize(lemma.lemmatize(word.lower()),'v'),pos=wordnet.ADJ),pos=wordnet.ADV)
