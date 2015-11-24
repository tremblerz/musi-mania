# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
import soundcloud
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import httplib2


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyBY_Z6jpdpSddA1VQEbAM6x0lNxLWyAir0"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

client = soundcloud.Client(client_id='f4e257503f0990527a6e17e14158076e')













def index():
    form = SQLFORM.factory(Field('query','string'), Field('option') ,formstyle='divs', submit_button="Search")
    response.flash = T("Hello World")
    if form.process().accepted:
        #k=redirect(URL('default','results', args=[1, formone.vars.search_query_1]))
        print form.vars.query
        redirect(URL('default','search_results', args=[form.vars.option, form.vars.query]))
    elif form.errors:
        print "failed"
    else:
        print "unknown"
    #return dict(form=form)
    return locals()


def test():
    
    form = SQLFORM.factory(Field('query','string'), Field('option') ,formstyle='divs', submit_button="Search")
    response.flash = T("Hello World")
    if form.process().accepted:
        #k=redirect(URL('default','results', args=[1, formone.vars.search_query_1]))
        print form.vars.query
        redirect(URL('default','search_results', args=[form.vars.option, form.vars.query]))
    elif form.errors:
        print "failed"
    else:
        print "unknown"
    return locals()

def no_net():
    return locals()
    
def search_results():
    form = SQLFORM.factory(Field('query','string'), Field('option'),formstyle='divs', submit_button="Search")
    if form.process().accepted:
        #k=redirect(URL('default','results', args=[1, formone.vars.search_query_1]))
        print form.vars.query
        redirect(URL('default','search_results', args=[form.vars.option, form.vars.query]))
    elif form.errors:
        print "failed"
    else:
        print "unknown"
    search = request.args(0) or redirect(URL('default','index'))
    if search == 'V':
        import sys
        reload(sys)
        sys.setdefaultencoding("utf-8")
        query = request.args(1) or redirect(URL('default','index'))
        try:
            youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
        #try:
            search_response = youtube.search().list(q=query.encode('utf-8'),part="id,snippet",maxResults=20).execute()
        except:# httplib2.ServerNotFoundError:
            #print ""
            redirect(URL('default','no_net'))
        #else:
            #redirect(URL('default','no_net'))
        l=[]
        videos = []
        channels = []
        playlists = []
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                l.append(search_result["snippet"]["title"])
                l.append(search_result["id"]["videoId"])
                videos.append(l)
                l=[]
            elif search_result["id"]["kind"] == "youtube#channel":
                channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
            elif search_result["id"]["kind"] == "youtube#playlist":
                playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))
        return dict(videos=videos[0:20],search=search,form=form,query=query)
    elif search == 'A':
        query = request.args(1) or redirect(URL('default','index'))
        try:
            tracks = client.get('/tracks', q=query, limit=20)
        except:# httplib2.ServerNotFoundError:
            #print "check"
            redirect(URL('default','no_net'))
        #else:
            #print "channel"
            #redirect(URL('default','no_net'))
        """emb = []
        for track in tracks:
            print track.stream_url
            url = client.get(track.stream_url, allow_redirects=False)
            emb.append(url.location)
            print url.location
            #print type(track.title)"""
        for t in tracks:
            url=t.permalink_url
            #print url
            embed_info = client.get('/oembed', url=url)
            #print embed_info.html
            #for x in t:
            #    print x,t[x]
            #print "\n\n"
        return dict(tracks=tracks,search=search,form=form,query=query)


"""def display_manual_form():
    #form = SQLFORM(db.person)
    form = SQLFORM.factory(Field('s1','string'), formstyle='divs', submit_button="Search")
    if form.process(session=None, formname='test').accepted:
        print query
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    # Note: no form instance is passed to the view
    return dict()"""

def spons_playlist():
    form = SQLFORM.factory(Field('query','string'), Field('option') ,formstyle='divs', submit_button="Search")
    if form.process().accepted:
        #k=redirect(URL('default','results', args=[1, formone.vars.search_query_1]))
        print form.vars.query
        redirect(URL('default','search_results', args=[form.vars.option, form.vars.query]))
    elif form.errors:
        print "failed"
    else:
        print "unknown"
    #search = request.args(0, cast=int) or redirect(URL('default','index'))
    return dict(form=form)

"""def form_component():
    form = SQLFORM.factory(Field('query','string'), formstyle='divs', submit_button="Search")
    if form.process().accepted:
        #k=redirect(URL('default','results', args=[1, formone.vars.search_query_1]))
        print form.vars.query
        redirect(URL('default','search_results', args=[1, form.vars.query]))
    elif form.errors:
        print "failed"
    else:
        print "unknown"
    songs = db(db.songs.genre==)
    #search = request.args(0, cast=int) or redirect(URL('default','index'))
    return locals()"""


#@auth.requires_login()
def vote():
    id=request.args(0,cast=int)
    #print id
    flag=True
    if auth.user:
        song=db.songs(id)
        likes=db.songs_like(db.songs_like.songs1==id)
        #print song
        #print likes
        if song:
            if likes:
                q=db((db.songs_like.user_id==auth.user.id)&(db.songs_like.songs1==id)).select()
                print q[0].total
                if q[0].total==0:
                    print "Increased Like"
                    song.update_record(Likes=song.Likes+1)
                    likes.update_record(total=1)
                    flag=False
                else:
                    print "Deleted Like"
                    if song.Likes!=0:
                        song.update_record(Likes=song.Likes-1)
                    else:
                        song.update_record(Likes=0)
                    likes.update_record(total=0)
                    flag=True
                    #db((db.songs_like.songs1==song.id)&(db.songs_like.user_id==auth.user.id)).delete()
            else:
                #print auth.user.id , song.id
                db.songs_like.insert(total=1,songs1=song.id,user_id=auth.user.id)
        else:
            return str("Song on which you tried to vote doesnt exist")
        song=db.songs(id)
        return str(song.Likes)
    else:
        return str("Please Log IN")



@auth.requires_login()
def mark_favourite():
    id=request.args(0,cast=int)
    x=db((db.favourite.songid==id)&(db.favourite.user_id==auth.user.id)).select()
    song = db.songs(id)
    fav = song.favourite
    print "Song = ",song
    if not x:
        db.favourite.insert(songid=id,user_id=auth.user.id)
        song.update_record(fav=fav+1)
        redirect(URL('default','see', args=id))
    else:
        redirect(URL('default','see',args=id))

@auth.requires_login()
def favsong():
    form = SQLFORM.factory(Field('query','string'),Field('option') ,formstyle='divs', submit_button="Search")
    if form.process().accepted:
        #k=redirect(URL('default','results', args=[1, formone.vars.search_query_1]))
        print form.vars.query
        print form.vars.option
        redirect(URL('default','search_results', args=[form.vars.option, form.vars.query]))
    elif form.errors:
        print "failed"
    else:
        print "unknown"
    result=db(db.favourite.user_id==auth.user.id).select()
    l=[]
    for r in result:
        k=db(db.songs.id==r.songid).select()
        if k[0].category == 'Audio':
            l.append(k[0])
    return dict(song=l,form=form)

@auth.requires_login()
def favideo():
    form = SQLFORM.factory(Field('query','string'), Field('option') ,formstyle='divs', submit_button="Search")
    if form.process().accepted:
        #k=redirect(URL('default','results', args=[1, formone.vars.search_query_1]))
        print form.vars.query
        redirect(URL('default','search_results', args=[form.vars.option, form.vars.query]))
    elif form.errors:
        print "failed"
    else:
        print "unknown"
    result=db(db.favourite.user_id==auth.user.id).select()
    l=[]
    for r in result:
        k=db(db.songs.id==r.songid).select()
        if k[0].category == 'Video':
            l.append(k[0])
    return dict(song=l,form=form)

def widgets():
    form = SQLFORM.factory(Field('query','string'),Field('option') , formstyle='divs', submit_button="Search")
    if form.process().accepted:
        #k=redirect(URL('default','results', args=[1, formone.vars.search_query_1]))
        print form.vars.query
        redirect(URL('default','search_results', args=[form.vars.option, form.vars.query]))
    elif form.errors:
        print "failed"
    else:
        print "unknown"

    song=db().select(db.songs.title,db.songs.id,db.songs.category)
    return locals()


def radio():
    form = SQLFORM.factory(Field('query','string'), Field('option') ,formstyle='divs', submit_button="Search")
    response.flash = T("Hello World")
    if form.process().accepted:
        #k=redirect(URL('default','results', args=[1, formone.vars.search_query_1]))
        print form.vars.query
        redirect(URL('default','search_results', args=[form.vars.option, form.vars.query]))
    elif form.errors:
        print "failed"
    else:
        print "unknown"
    import json
    import urllib2
    url = "http://api.dirble.com/v2/stations?per_page=30&token=f1a8a36dd125c2e665dafec481"
    data = json.load(urllib2.urlopen(url))
    #return dict(form=form)
    return locals()
def fav():
    form = SQLFORM.factory(Field('query','string'), Field('option') ,formstyle='divs', submit_button="Search")
    if form.process().accepted:
        #k=redirect(URL('default','results', args=[1, formone.vars.search_query_1]))
        print form.vars.query
        redirect(URL('default','search_results', args=[form.vars.option, form.vars.query]))
    elif form.errors:
        print "failed"
    else:
        print "unknown"
    res = db().select(orderby=~db.songs.favourite,limitby=(0,10))
    print res
    """l=[]
    for r in result:
        k=db(db.songs.id==r.songid).select()"""
    return locals()

def pop():
    form = SQLFORM.factory(Field('query','string'), Field('option') ,formstyle='divs', submit_button="Search")
    if form.process().accepted:
        #k=redirect(URL('default','results', args=[1, formone.vars.search_query_1]))
        print form.vars.query
        redirect(URL('default','search_results', args=[form.vars.option, form.vars.query]))
    elif form.errors:
        print "failed"
    else:
        print "unknown"
    res = db().select(orderby=~db.songs.views,limitby=(0,10))
    print res
    return locals()

def voted():
    form = SQLFORM.factory(Field('query','string'), Field('option') ,formstyle='divs', submit_button="Search")
    if form.process().accepted:
        #k=redirect(URL('default','results', args=[1, formone.vars.search_query_1]))
        print form.vars.query
        redirect(URL('default','search_results', args=[form.vars.option, form.vars.query]))
    elif form.errors:
        print "failed"
    else:
        print "unknown"
    res = db().select(orderby=~db.songs.Likes,limitby=(0,10))
    print res
    return locals()
    
def see():
    form = SQLFORM.factory(Field('query','string'),Field('option') , formstyle='divs', submit_button="Search")
    if form.process().accepted:
        #k=redirect(URL('default','results', args=[1, formone.vars.search_query_1]))
        #print form.vars.query
        redirect(URL('default','search_results', args=[form.vars.option, form.vars.query]))
    elif form.errors:
        print "failed"
    else:
        print "unknown"
    id=request.args(0,cast=int)
    #print db.songs(id)
    db.songs(id)
    song=db.songs(id) or redirect(URL('index'))
    views = song.views
    song.update_record(views = views+1)
    print "View = ",views
    comments=db(db.cmnt.songs1==song.id).select()
    #print song.id
    #song.Likes.default=0
    Likes=song.Likes
    #print Likes
    #for comment in comments:
    if auth.user:
        #db.cmnt.songs1=id
        db.cmnt.songs1.default=id
        formcmnt=SQLFORM(db.cmnt)
        if formcmnt.process().accepted:
            redirect(URL('see',args=id))
        else:
            response.flash="Success!"
    else:
        formcmnt=A("Please Login for commenting and liking",_href=URL('user/login',vars=dict(_next=URL(args=request.args))))
    return locals()

def upload():
    form=SQLFORM(db.videos, fields=['title','description','video'])
    return locals()

def insert():
    vars=request.get_vars
    title=vars.title
    url=vars.url
    print url
    category=vars.category
    genre=vars.genre
    likes=0
    existing=db(db.songs.title==vars.title).select()
    #if category == 'Audio':
        #url = client.get(url, allow_redirects=False)
        #url=url.location
    if existing:
        new_id=existing.id
    else:    
        db.songs.insert(title=title,url=url,category=category,genre=genre,Likes=likes)
        new_id=db(db.songs.id>0).count()
    redirect(URL('see',args=new_id))

"""def see():
    x=0
    id=request.args(0,cast=int)
    print db.songs(id)
    song=db.songs(id) or redirect(URL('index'))
    comments=db(db.cmnt.songs1==song.id).select()
    print song.id
    #song.Likes.default=0
    Likes=song.Likes
    #for comment in comments:
    if auth.user:
        #db.cmnt.songs1=id
        db.cmnt.songs1.default=id
        form=SQLFORM(db.cmnt)
        if form.process().accepted:
            redirect(URL('see',args=id))
        else:
            response.flash="Success!"
    else:
        form=A("Please Login for commenting and liking",_href=URL('user/login',vars=dict(_next=URL(args=request.args))))
    return locals()
"""
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()