import time

class TrackableObject:
	def __init__(self, objectID, centroid):

		self.objectID = objectID
		self.centroids = [centroid]
		self.counted = False
		
		self.startTime = time.time()
		self.endTime = time.time()
		self.start = 0
		# 0 means bottom
		# 1 means top