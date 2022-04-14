from Tt_models import TimeTable
import string
import Tt_models, Tt_manager

"""
    Setting up something similar to fego junior classes jss1-3
    -----------------------------------------------------------------
"""


W_PERIODS = 50
#-- Number of periods per week


DAYS = ["monday","Tuesday","wednesday","thursday","friday"]
    

CLASS_GROUPS = {'jss': 'junior secondary school', 'sss': 'senior secondary school'}

SUBJECT_LIST = ["Mathematics", "English", "basic science", "french", "yoruba",
                     "business studies","basic technology", "home economics", "ICT",
                     "crs", "social studies", "civic education", "history",
                    "creative arts","music", "agric science", "philosophy"]
SUBJECT_NUM = len(SUBJECT_LIST)
CLASS_ARMS = string.ascii_letters[:9]

# instantiating a timetable object for experimentation
my_tt = TimeTable()

for subj in SUBJECT_LIST:
    my_tt.create_department(subj)

                                        # for clss in CLASSES:
                                        #     for subj in my_tt.list_of_departments:
                                        #         for _ in range(2):
                                        #             my_tt.create_teacher(dept_obj_=subj)
                                        #     for arm in CLASS_ARMS:
                                        #         my_tt.create_school_class(clss, arm)

for day in DAYS:
    my_tt.create_day(day)


for nick, name in CLASS_GROUPS.items():
    my_tt.create_school_class_group(name, abbrev=nick)



                                        # my_tt.create_department("Extra-curricular",is_special=True)

# print()
print(my_tt.list_of_departments)
print("-"*80)
print(my_tt.list_of_school_class_groups)
print("-"*80)

for x in range(3):
    for y in my_tt.list_of_school_class_groups:
        my_tt.create_school_class(x, y)

print()
print()

for dept in my_tt.list_of_departments:
    for _ in range(3):
        my_tt.create_teacher(dept_obj_=dept)

periods_ = my_tt.split_into_periods((8,0,0),(15,0,0),10)


# for teacher in my_tt.list_of_all_teachers:
#     for dept in my_tt.list_of_departments:
#         teacher.add_dept_to_teacher(dept)

# for x in my_tt.list_of_school_class_groups:
#     print(x.school_class_list)
#     print("-"*80)

#     for v in x.school_class_list:
#         for m in range(8):
#             my_tt.create_school_class_arm(m, v)
#         # for s, per in zip(v.school_class_arm_list, periods_):
#         #     print(s, per)


print()

# days = my_tt.list_of_days

print(my_tt.list_of_all_teachers)
print()

print("-"*50)

m = my_tt.list_of_departments
u = my_tt.list_of_all_teachers[0]

for dept in my_tt.list_of_departments[1:5]:
    u.add_dept_to_teacher(dept)


# print(u.teachers_department_list)

r = Tt_manager.get_obj_from_param(m, "dept_name", "philosophy")
print()
print("_"*70)
print(m)
print()
print(r)

print()
print("*"*84)

print(my_tt.list_of_school_classes)

for m in my_tt.list_of_school_classes:
    for x in range(8):
        my_tt.create_school_class_arm(x, m, as_alpha=True)




for arm in my_tt.list_of_school_class_arms:
    for dept, per, day in zip(my_tt.list_of_departments, periods_, my_tt.list_of_days):
        my_tt.create_period(per.start, day=day, end=per.end, sch_class_arm_obj=arm, dept_=None, 
            is_fav=True, title_of_fav=f"Special period for {arm.arm_id}, on {day.day}")


for arm in my_tt.list_of_school_class_arms:
    print(arm, [(x.start, x.end, x.subject) for x in arm.periods])

print("_"*120)
print()

print(my_tt.list_of_departments)
my_tt.del_department(r)

print()
print(my_tt.list_of_departments)
