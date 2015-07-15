(1) For user data, we retrieve only data for users who show at least one run in their activity array. We extract several fields from the large 'activityArray' subdocument and parse these into several columns, each containing a list. Each list is ordered in the same way, according to the order of the activity array. This means that the data from all lists with the same index is for the same event.

(2) For run data, we retrieve all runs and again extra columns of interest from the large 'run_info' subdocument. Again the data comes in lists/arrays, which we retain per row and in order, as with the user data.

Note that the user data is non-rectangular in that each user has an undetermined number of activities. 
