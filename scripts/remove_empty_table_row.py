from pymongo import MongoClient

mongo_client = MongoClient('mongodb+srv://local-home:Wigbhi5M@studentportal-uhvtp.mongodb.net/'
                           '?retryWrites=true&w=majority')
studentportal_db = mongo_client.studentportal

modules = list(studentportal_db.modules.find())

for module in modules:
    for index, instance in enumerate(module['teaching_instances']):
        for activity_index, activity in enumerate(instance['student_activity']['activities']):
            if not activity['mode'] and not activity['type'] and not activity['study_hours']:
                instance['student_activity']['activities'].pop(activity_index)

    print(module['_id'])
    studentportal_db.modules.update_one({'_id': module['_id']}, {"$set": module})
