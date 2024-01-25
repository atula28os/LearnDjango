from rest_framework.throttling import UserRateThrottle

class ReviewCreateThrottle(UserRateThrottle):
    scope = "create-movie-review"
    

class ReviewListThrottle(UserRateThrottle):
    scope = "movie-review-list"