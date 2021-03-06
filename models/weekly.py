from models.event import Event
from lib.api import PublishAPI
import functions

from datetime import datetime, timedelta
import math

class WeeklyMemento :

	@staticmethod
	def get_week_bound(date) :
		weekday = date.isoweekday() % 7 # 0(Sun) ~ 6(Sat)
		return date + timedelta(days=-weekday), date + timedelta(days=6-weekday)


	@staticmethod
	def get_week(date) :
		day1 = datetime(date.year, date.month, 1)
		start_date, end_date = WeeklyMemento.get_week_bound(date)
		diff = start_date - day1

		today = datetime.today()
		today = datetime(today.year, today.month, today.day) # Remove hour, minute, seconds
		
		if end_date >= today :
			return None

		if end_date.month == date.month :
			return date.year, date.month, int(math.ceil(diff.days / 7)) + 1

		else :
			ndate = datetime(end_date.year, end_date.month, end_date.day)
			return ndate.year, ndate.month, 1



	def __init__(self, year=None, month=None, week=None, date=None) :

		if date :
			self.year, self.month, self.week = WeeklyMemento.get_week(date)

		else :
			self.year = year
			self.month = month
			self.week = week
			date = datetime(year, month, 1 + (week-1) * 7)


		self.start_date, self.end_date = WeeklyMemento.get_week_bound(date)

		data = PublishAPI.get('/events/toprank?fromDate=%s&toDate=%s&rankLimit=12'
			% (self.start_date.strftime('%Y-%m-%d'), self.end_date.strftime('%Y-%m-%d'))
		)
		
		self.events = [ Event(**event) for event in data ]
		self.events.sort(key=lambda d: d.date, reverse=True)

		self.next_week = WeeklyMemento.get_week(date + timedelta(days=7))
		self.prev_week = WeeklyMemento.get_week(date + timedelta(days=-7))


	def repr_image(self, css_mode=False, thumbnail=False) :
		""" Get representative image of weekly-memento
		"""
		n_events = sorted(self.events[0:10], key=lambda d: d.issue_data.issue_score, reverse=True)

		if len(n_events) :
			return n_events[0].repr_image(css_mode, thumbnail)
		else :
			return functions.image_url(None, css_mode, thumbnail)



