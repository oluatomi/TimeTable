#--THIS MODULE HANDLES THE MANAGEMENT OF THE 'cls_pers' MODULE
#--THIS DOES NOT TAKE CARE OF THE ALGORITHM TO SORT, BUT PROVIDES VITAL INFORMATION
#--FOR THE MODULE THAT HANDLES THE ALGORITHM FOR SORTING.
#-- THE 'cls_pers' MODULE HANDLES THE OBJECTS 
#-- (MOSTLY), WITH ITS STATIC METHODS DOING SOME OF THE NEEDED (SMALL)
#--CALCULATIONS THAT ARE ALBEIT STILL NEEDED.
#--THOSE METHODS COULD HAVE BEEN PUT HERE, BUT I FEEL THEY SHOULD SHIP DIRECTLY WITH THE 'cls_pers'
#--MODULE -- THE MODULE THAT HANDLES THE TIMETABLE OBJECT.


# -- THIS IS THE OFFICIAL FORM OF THE TESTING_SETUP.PY MODULE


from Tt_models import TimeTable, ProjectExceptions
from inspect import isfunction
import string



def get_obj_from_param(g_list, attr, param):
    """ This helper function searches through a given list "g_list" and 
    checks for the object that has the attribute "attr" if it is equal to "param"
    and then returns it.

    "param" has to be string. So also "attr".
     """

    for item in g_list:
        if hasattr(item, attr):
            if isfunction(getattr(item, attr)):
                if getattr(item, attr)().lower() == param.lower():
                    return item

            else:
                if getattr(item, attr).lower() == param.lower():
                    return item
    else:
        raise ValueError(f"No item has what you checked for.")




class TimeTableManager:
    """ This class serves as the intermediary between the GUI and the TimeTable (cls_pers) module """

    def __init__(self):
        self.TimeTableObj = TimeTable()


    def create_department(self, name, HOD="HOD Sir/Ma'am"):
        #  ...
        #  ...
        #  ...
        self.TimeTableObj.create_department(name, HOD="HOD Sir/Ma'am")



    def create_special_department(self, name, HOD="HOD Sir/Ma'am"):
        #  ...
        #  ...
        #  ...
        self.TimeTableObj.create_department(name, HOD="HOD Sir/Ma'am", is_special=True)


    def edit_department(self, id, name, HOD="HOD Sir/Ma'am"):
        #  ... The "get_obj_from_list" method is called to get the department object with the id
        #  ... This method EDITS all sorts of departments, special or not.
        #  ...
        dept_obj.name = name
        dept_obj.HOD = HOD


    def remove_department(self, id):
            #  ... The "get_obj_from_list" method is called to get the department object with the id
            #  ... This method removes all sorts of departments, special or not.
            #  ...
            self.TimeTableObj.del_department(dept_obj)



    def create_school_class_group(self,class_group_name, abbrev="Jnr, Snr High"):
        #  ...
        #  ...
        #  ...
        self.TimeTableObj.create_school_class_group(class_group_name, abbrev=abbrev)


    def edit_school_class_group(self, id, class_group_name, description="None given for now",abbrev="Jnr, Snr High"):
        #  ... The "get_obj_from_list" method is called to get the department object with the id
        #  ... This method EDITS all sorts of departments, special or not.
        #  ...
        sch_class_group_obj.class_group_name = class_group_name
        sch_class_group_obj.description = description
        sch_class_group_obj.abbreviation = abbrev


    def remove_school_class_group(self, id):
        #  ...
        #  ...
        #  ...
        self.TimeTableObj.del_school_class_group(sch_clss_group_obj)



    def create_school_class(self, class_group, level_iden=1):
        #  ...
        #  ...
        #  ...
        self.TimeTableObj.create_school_class(level_iden, class_group)


    def edit_school_class(self, id, sch_class_group_obj, level_iden=1):
        #  ... The "get_obj_from_list" method is called to get the department object with the id
        #  ... This method EDITS all sorts of departments, special or not.
        #  ...
        sch_class_obj.level = level_iden
        sch_class_obj.school_class_group = sch_class_group_obj


    def remove_school_class(self, id):
        #  ...
        #  ...
        #  ...
        self.TimeTableObj.del_school_class(sch_clss_obj)


    #-- ----SHOULD SCHOOL CLASS ARMS BE EDITABLE OR JUST DELETED OUTRIGHT?


    def create_school_class_arm_alphabetical(self, num_id, school_class_obj):
        #  ...
        #  ...
        #  ...
        self.TimeTableObj.create_school_class_arm(num_id, school_class_obj)


    def create_school_class_arm_numerical(self, num_id, school_class_obj):
        #  ...
        #  ...
        #  ...
        self.TimeTableObj.create_school_class_arm(num_id, school_class_obj, is_alpha=False)


    def remove_school_class_arm(self, id):
        #  ... Removes school_class_arm objs whether named alphabetically or numerically.
        #  ...
        #  ...
        self.TimeTableObj.del_school_class_arm(sch_clss_group_arm)


    def create_teacher(self, dept_name=None):
        #  ...
        #  ...
        #  ...
        self.TimeTableObj.create_teacher(dept_name)


    def remove_teacher(self, id):
        #  ...
        #  ...
        #  ...
        self.TimeTableObj.del_school_class_group(teacher_obj)



    # -- MAKING PERIODS AND STUFF IS NEXT!

    def create_day(self,  day_name, rating=None):
        #  ...
        #  ...
        #  ...
        self.TimeTableObj.create_day(day_name, rating=rating)


    def remove_day(self, id):
        #  ...
        #  ...
        #  ...
        self.TimeTableObj.del_day(day_obj)


    def periods_schoolclassarm_per_day(self,day, sch_clss_arm):
        #  ...
        #  ...
        #  ...
        """Assigns the day to each class arm and its list of periods. Parameters are the day"""
        pass
    



