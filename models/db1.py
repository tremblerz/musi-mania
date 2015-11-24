# coding: utf8
import datetime; now=datetime.date.today()


db.define_table('songs',
Field('title','string',requires=(IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'song.title'),IS_SLUG())),
Field('category', requires=IS_IN_SET(['Audio' , 'Video'])),
Field('url', 'string', requires=IS_NOT_EMPTY()),
Field('Likes','integer',requires=IS_NOT_EMPTY()),
Field('views', 'integer',default=0),
Field('favourite','integer',default=0),
Field('genre', 'string'))

db.define_table('songs_like',
Field('songs1','reference songs',readable=False,writable=False),
Field('total','integer',default=+1),
Field('user_id','reference auth_user'))

db.define_table('playlist',
					Field('song_id','reference songs',readable=False,writable=False),
					Field('user_id','reference auth_user',readable=False,writable=False)
				)
db.define_table('cmnt',
				Field('songs1','reference songs',readable=False,writable=False),
				Field('parent_comment','reference cmnt',readable=False,writable=False),
				Field('Likes','integer',readable=False,writable=False),
				Field('body','text',requires=IS_NOT_EMPTY()),
				auth.signature)

db.define_table('fav',
				Field('songs1','reference songs'),
				Field('rate','integer',default=0),
				auth.signature)
db.define_table('videos',
				Field('title'),
				Field('description',length=150),
				Field('dateu','date',default=now),
				Field('video','upload'),
				Field('thumbnail','upload'))

db.videos.title.requires=[IS_NOT_EMPTY()]
db.videos.description.requries=[IS_NOT_EMPTY()]
db.videos.dateu.requires=[IS_DATE()]
db.videos.video.requires=[IS_NOT_EMPTY()]



db.define_table('cmnt_like',
				Field('cmnt','reference cmnt',readable=False,writable=False),
				Field('total','integer',default=+1))

db.define_table('favourite',
				Field('songid','reference songs',readable=False,writable=False),
				Field('user_id','integer',readable=False,writable=False)
				)