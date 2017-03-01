from tornado import gen,web
import json,os,time
import pymongo
from pprint import pprint
from bson.objectid import ObjectId #deal with object pymongo
from bson.code import Code
from bson import ObjectId


templateurl = "../template/"

class BaseHandler(web.RequestHandler):
	def get_current_user(self):
		user_id = self.get_secure_cookie("id")
		if not user_id: return None
		user_name = str(self.get_secure_cookie("name"),'utf-8')
		user_status = str(self.get_secure_cookie("status"),'utf-8')
		user = {
			'user':str(user_id,'utf-8'),
			'name':user_name,
			'status':user_status
		}
		print("in current user")
		print(type(user_id))

		return user

class PrivateChatHandler(BaseHandler):
	@web.authenticated
	def get(self):
		count = 0

		f = open("template/test.txt")

		for line in f:
			count = count + 1

		f.seek(0);

		self.render(templateurl+"privatechat.html",user_name=self.current_user['name'], status=self.current_user['status'], id_last_index=0, filename=f, username="1", friend_name="2", posts_no=count,user_avatar="http://cs625730.vk.me/v625730358/1126a/qEjM1AnybRA.jpg")

class GroupChatHandler(BaseHandler):
	@web.authenticated
	def get(self):
		f = open("template/test.txt")
		
		count = 0

		for line in f:
		  count = count + 1

		f.seek(0)

		self.render(templateurl+"groupchat.html", user_name=self.current_user['name'], status=self.current_user['status'], id_last_index=0, group_name="Eqraa", posts_no=count, chat_members=["2","3","4"], filename=f, username="1", group_avatar="http://cs625730.vk.me/v625730358/1126a/qEjM1AnybRA.jpg")

class HomeHandler(BaseHandler):
	@web.authenticated
	def get(self):
		print("++++++++++++++++++++++++++++++++")
		print(type(self.current_user['name']))
		print("++++++++++++++++++++++++++++++++")
		print(self.current_user)
		self.render(templateurl+"home.html", user_name=self.current_user['name'], status=self.current_user['status'], group_name="Eqraa", posts_no="2000",group_avatar="http://cs625730.vk.me/v625730358/1126a/qEjM1AnybRA.jpg")

#handling signup in db and cookies (registeration and login)
class SignupHandler(BaseHandler):
	#@web.authenticated
	def post(self):
		#insert user info
		db = self.application.database
		username=self.get_argument("signupname")
		email=self.get_argument("signupemail")
		pwd=self.get_argument("signuppwd")
		new_user = {"name":username,"password":pwd,"email":email,"status":'on'}
		try:
			user_id = db.users.insert(new_user)
			self.set_secure_cookie("id",str(user_id))
			self.set_secure_cookie("name", username)
			self.set_secure_cookie("status", 'on')
			self.render(templateurl+"home.html", user_name=username, status='on', group_name="Eqraa", posts_no="2000",group_avatar="http://cs625730.vk.me/v625730358/1126a/qEjM1AnybRA.jpg")
		except pymongo.errors.DuplicateKeyError:
			# error in signup if duplicated name
			self.redirect("/?sp=1")


class GroupsHandler(BaseHandler):
	@web.authenticated
	def get(self):

		# db.users.find({name:userName}).forEach(function(user){ db.groups.find({user:user._id}).forEach(function(group) { print(group.name) }) })

		self.render(templateurl+"groups.html", user_name=self.current_user['name'], status=self.current_user['status'], group_name="Eqraa", posts_no="2000",group_avatar="http://cs625730.vk.me/v625730358/1126a/qEjM1AnybRA.jpg")

class PeopleHandler(BaseHandler):
	@web.authenticated
	def get(self):
		db = self.application.database
		userName = self.get_secure_cookie("name")
		print(userName)
		# frnds_list = db.users.find({name:userName},{friendId:1})
		# find friends
		# frnds_list = db.users.find({name:userName},{friendId:1}).forEach(function(frind){=db.users.find({_id:{$in:frind.friendId}}).forEach(function(u){print(u.name)})})

		# print(db.users.find({"name":userName},{"name":1}))
		# print(frnds_list)
		for i in frnds_list.length:
			print(frnds_list[i])

		# others_list = db.users.find({name:{$ne:userName}},{friendId:1}).forEach(function(frnd){db.users.find({$and[{_id:frnd},{name:{$ne:userName}}]},{"name":1})})

		self.render(templateurl+"people.html", user_name=self.current_user['name'], friends_list=frnds_list, status=self.current_user['status'], group_name="Eqraa", posts_no="2000",group_avatar="http://cs625730.vk.me/v625730358/1126a/qEjM1AnybRA.jpg")

# Handler to Create Group 
class CreateGroupHandler(BaseHandler):
	@web.authenticated
	def get(self):
		db = self.application.database
		groupname = self.get_query_arguments("groupname")
		print(groupname)
		try:
			group_id = db.groups.insert({name:groupname})
			self.render(templateurl+"groups.html", user_name=self.current_user['name'], status=self.current_user['status'], group_name="Eqraa", posts_no="2000",group_avatar="http://cs625730.vk.me/v625730358/1126a/qEjM1AnybRA.jpg")
		except pymongo.errors.DuplicateKeyError:
			self.write("Group name already in use")
			self.redirect("/addgroup")

		self.render(templateurl+"creategroup.html")

# class ChatBotHandler(BaseHandler):
# 	@web.authenticated
# 	def get(self):
# 		f = open("template/test.txt")
		
# 		count = 0

# 		for line in f:
# 		  count = count + 1

# 		f.seek(0)

# 		self.render(templateurl+"chatbot.html",user_name=self.current_user['name'], status=self.current_user['status'], id_last_index=0, filename=f, username="1", friend_name="2", posts_no=count,user_avatar="http://cs625730.vk.me/v625730358/1126a/qEjM1AnybRA.jpg")
		self.render(templateurl+"people.html", user_name=self.current_user['name'], status=self.current_user['status'], group_name="Eqraa", posts_no="2000",group_avatar="http://cs625730.vk.me/v625730358/1126a/qEjM1AnybRA.jpg")

#class to add friend
class AddFriendHandler(BaseHandler):
	@web.authenticated
	def get(self):
		#userId=self.get_secure_cookie("id")
		userId = str(self.get_secure_cookie("id"),'utf-8')
		#print(userId)
		#open connection with database
		db = self.application.database
		# iterate in users to find matched one
		for users in db.users.find({"_id":ObjectId(userId)}):
			print(users)
		#static adding friend in dbs using id of another one then trying to do it auto
		#adding only id of friends
		reqId= ObjectId("58b5b1845f4a5505a3c40c57")
		# if reqId not in db.users.find({'_id':ObjectId(userId)},{friendId:1,_id:0}).forEach(function(frind){test=db.users.find({_id:{$in:frind.friendId}})}):
		# 	print("duplicates")
		# else:
		db.users.update({"_id":ObjectId(userId)},{"$push":{"friendId":reqId}})

		# x []= Code("""db.users.find({'_id':ObjectId(userId)},{"friendId":1,"_id":0}).forEach(function(frind){test=db.users.find({reqId:{'$in':'frind.friendId'}}).forEach(function(u){print(u.name)})})""")
		#	print(x)
		# but the above code will allow dublicated
		#we need to verify if it's exist before or not may be try to remove it if it's exist before
class BlockHandler(BaseHandler):
	@web.authenticated
	def get(self):
		#__TODO__ put function body @POST method and handel fun return
		#frindblock boolean if true operation is blocking friend else Group remove
		frindblock=self.get_argument("block")
		db = self.application.database
		#__TODO__ get removeid from interface
		#removeid=ObjectId("58b5ca548d46858f7030f216")#user
		removeid=ObjectId("58b5c9b68d46858f7030f215")#group
		uid=ObjectId(self.current_user['user'])
		print(frindblock)
		if frindblock== "true":
			block = "friends"
		elif frindblock== "false":
			block = "groups_id"
		#__TODO__Exceptions handling
		update=db.users.update_one({"_id":uid},{"$pull":{block:removeid}})
		pprint(update.modified_count)
#########################################################################################3
#creating handler for create group
# don't work 
class CreateGroupHandler(BaseHandler):
	@web.authenticated
	def get(self):
		userId = str(self.get_secure_cookie("id"),'utf-8')
		groupNameCreate=self.get_argument("gx")
		print(gx)
		#db = self.application.database