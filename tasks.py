 #-*- coding: UTF-8 -*-
from django.db.models import F
from celery.task import *
from datetime import timedelta, datetime
from app.models import CustomUser
"""
Note: the api of twitter retards 1 minute (more or less) the update of the update_date
"""
@task
def forensic():
    logger = forensic.get_logger()
    users = CustomUser.objects.filter(next_check__lt=datetime.utcnow(),half_dead=False,dead=False,configured=True)
    
    for user in users:
	logger.info("User %s, act: %d, mail: %d, lu: %s - [%s]" % (user.username, user.activity_interval, user.mail_interval, user.last_update,  datetime.now()))	    
	
	#Get the last update date for the user
	if user.update_date():
	    logger.info("User %s, update her date update (on twitter) - [%s]" % (user.username, datetime.now()))	    

	#time from last update
	t = datetime.utcnow() - user.last_update
	
	#Check if the user is half-dead
	if t.seconds >= user.activity_interval:
	    user.half_dead = True
	    user.save()
	    logger.info("User %s, is HALF-DEAD (on twitter) - [%s]" % (user.username, datetime.now()))
	    
	    user.send_email_halfdead()
	    
@task
def killer_saver():
    logger = killer_saver.get_logger()
   
    users = CustomUser.objects.filter(half_dead=True, dead=False, configured=True)
    
    for user in users:
	logger.info("User %s, act: %d, mail: %d, lu: %s - [%s]" % (user.username, user.activity_interval, user.mail_interval, user.last_update,  datetime.now()))	    
	
	#Get the last update date for the user
	if user.update_date():
	    logger.info("User %s, update the last date update (on twitter) - [%s]" % (user.username, datetime.now()))	    
	    
        #Which is bigger?
        if user.last_update < user.last_login:
            date_substract = user.last_login
        else:
            date_substract = user.last_update

	#time from last update
	t = datetime.utcnow() - date_substract
	
	#Check if the user status
	if t.seconds < user.activity_interval:
	    #Is not still half_dead -> save it
	    user.dead = False
	    user.half_dead = False
	    user.save()
	    logger.info("User %s, is SAVED (on twitter) - [%s]" % (user.username, datetime.now()))
	    user.send_email_still_alive()
	    #user.update_twitter_status("Sigo vivo, no os preocupeis. http://foowill.com %s" % datetime.now() )
	    
	elif t.seconds >= user.activity_interval + user.mail_interval:
	    user.dead = True
	    user.save()
	    logger.info("User %s, is DEAD (on twitter) - [%s]" % (user.username, datetime.now()))
	    user.send_email_hope_to_read()
	    user.deliver_all_to_twitter()
            #TODO: Deliver messages with the publish interval !!!
            
	else:
	    logger.info("User %s, is STILL HALF-DEAD (on twitter) - [%s]" % (user.username, datetime.now()))
	    #TODO: if email: Send email for another reminder.
