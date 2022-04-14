# Main module for class definition of classes(school)
# ------------------------------------------

from collections import namedtuple
import string


# ---------------------------------------------------------------------------------
# --------------------- CODE FOR ALL THE EXCEPTIONS RAISED ------------------------
# ---------------------------------------------------------------------------------
class ProjectExceptions:

    class MyOwnException(Exception):
        def __init__(self, comment):
            super().__init__(comment)
            self.comment = comment


    class ClassAlreadyExists(MyOwnException):
        """For when your're making a class that already exists"""
        pass

    class NoTeacherAvailabale(MyOwnException):
        """for when a period assigns a teacher that doesn't exist from a dept"""
        pass

    class IsASpecialDept(MyOwnException):
         """For when teachers' info or class count or academic demands are made from
         a department (OR SUBJECT) that is not an academic dept, e.g break, 
         or xtra-curriculars"""
         pass

    class SubjectOrClassNotRegistered(MyOwnException):
        """When a period is instantiated without the school class or department (subject) registered,
         i.e. being in the list of departments or classes"""
        pass

    class CannotAssignFavPeriod(MyOwnException):
        pass

    class SubjectAlreadyExists(MyOwnException):
        """When a class that already exists is about to be re-instantiated"""
        pass

    class ClassArmCannotBeMade(MyOwnException):
        """ This happens when there is a problem making class arms because the num_id or the school class
        objects have not been supplied """
        pass

    class TeacherCannotBeAssigned(MyOwnException):
        """In the event when a teacher attempts to be assigned from a department's empty list (if auto),
         or tries to access a 'teacher_index' that doesn't exist"""
        pass

    class TeacherAlreadyGivenSaidSubject(MyOwnException):
        """ This alarm is raised if a teacher is assigned a subject which he had been previously assigned """
        pass



#-----------------------------------------------------------------------------------
# --------------------------- THE TIMETABLE CODE ITSELF ----------------------------
#-----------------------------------------------------------------------------------
class TimeTable:
    '''The universal set for all operations 
    with regard to the time-table operation code'''

    Timetable_list = []

    def __init__(self):
        TimeTable.Timetable_list.append(self)

        # Lists of Depts, classes and periods to help keep score
        self.list_of_departments = []
        self.list_of_all_teachers = []

        self.list_of_school_class_groups = []
        self.list_of_school_classes = []
        self.list_of_school_class_arms = []
        self.list_of_days = []
    


    def create_department(self, name, HOD="HOD Sir/Ma'am", is_special=False):
        '''A function to instantiate the department object'''

        # --Below checks if the subject already existed
        for dept in self.list_of_departments:
            if name.lower() == dept.dept_name.lower():
                raise SubjectAlreadyExists()

        department = self.Department(name, HOD=HOD, is_special=is_special)
        self.list_of_departments.append(department)

        return department


    def del_department(self, dept_obj):
        TimeTable.remove_from_list(self.list_of_departments,obj=dept_obj)


    def create_school_class_group(self, class_group_name, description='', abbrev=None):
        """
            This function instantiates the school_class_group, i.e. maybe Junior school 
            or Senior school
        """
        class_groups = self.SchoolClassGroup(class_group_name, class_group_description=description, abbrev=abbrev)
        self.list_of_school_class_groups.append(class_groups)

        return class_groups


    def del_school_class_groups(self, clss_gr_obj):
        TimeTable.remove_from_list(self.list_of_school_class_groups, obj=clss_gr_obj)


    def create_school_class(self, level_iden, class_group):
        """ This function creates a school class considering the school class group 
        whether 'Junior' or 'Senior' school """

        school_class = self.SchoolClass(level_iden, class_group)
        self.list_of_school_classes.append(school_class)

        return school_class


    def del_school_class(self, sch_class_obj):
        TimeTable.remove_from_list(self.list_of_school_classes, obj=sch_class_obj)


    def create_school_class_arm(self, num_id, school_class_obj, as_alpha=True):
        """ This function creates the arm for the school class passed in """

        try:
            class_arm = self.SchoolClassArm(num_id, school_class_obj, as_alpha=as_alpha)
        except Exception:
            raise ProjectExceptions.ClassArmCannotBeMade("num_id or school_class object missing")
        else:
            self.list_of_school_class_arms.append(class_arm)
            return class_arm

    
    def del_school_class_arm(self, sch_class_arm):
        TimeTable.remove_from_list(self.list_of_school_class_arms, obj=sch_class_arm)



    def create_teacher(self, dept_name=None, dept_obj_=None):

        # The code below takes in a dept object if available and checks to see if it really is a department object
        if dept_obj_:
            if isinstance(dept_obj_, self.Department):
                dept_obj = dept_obj_
        
        else:
            # --If department name and not object is given
            for dept in self.list_of_departments:
                if dept.dept_name.lower() == dept_name.lower():
                    dept_obj = dept
                    break
            else:
                dept_obj = create_department(dept_name)
                # When a teacher is made fresh, a department is also made fresh as is above

        teacher = dept_obj._add_teacher()       
            #-- Add teacher to the list of all teachers
        self.list_of_all_teachers.append(teacher)

        # -- create a personal id attr for teacher. It is their index on the list of all teachers + 1 
        # because it is not zero-based 
        
        teacher.personalId = self.list_of_all_teachers.index(teacher) + 1


    def del_teacher(self, teacher_obj):
        TimeTable.remove_from_list(self.list_of_all_teachers, obj=teacher_obj)


    def create_day(self, day_name, rating=None):
        """ This is the function to create the day instance, with day_id being a unique identifier 
        in case two or more days share the same name (in the case where the time-table spans more 
        than a week) """

        day_id = 1
        for day in self.list_of_days:
            if day.day.lower() == day_name.lower():
                day_id += 1

        day = self.Day(day_name=day_name, day_id=day_id, rating=rating)
        self.list_of_days.append(day)


    def del_day(self, day_obj):
        TimeTable.remove_from_list(self.list_of_days, obj=day_obj)


    def days_manager(self):
        """ This function manages all the day-objects that have been instantiated.
        the operative variable is called "week". This could be an actual week if the
         days are monday to friday """
        

        # -- MORE ON THIS LATER




    def create_period(self, start, day=None, end=None, sch_class_arm_obj=None, 
        dept_=None, is_fav=False, duration=0,  spot=None, title_of_fav=None):
        '''This creates the periods, both the usual and the special period
        
        dept_, sch_class_ represent the department object and the 
        school class object respectively, if none is specified, an object is expected.

        if your dept doesn't exist yet, you should call the function to make it first
        '''

        dept_obj, sch_class_arm_obj, day_obj = dept_, sch_class_arm_obj, day


        if not sch_class_arm_obj or not day_obj:
            raise ProjectExceptions().SubjectOrClassNotRegistered("Period cannot be created! school class or "
             "subject(department) or the Day is missing")


        if not is_fav:
            # checking if it is OR isn't a special period
            indiv_period = self.Period().normal_period(day_obj, start, duration, sch_class_arm_obj,dept_obj=dept_obj, end=end)
        else:
            indiv_period = self.Period().fav_period(day_obj, duration, spot=spot, start=start, dept_obj=dept_obj, 
                sch_class_arm_obj=sch_class_arm_obj, title_of_fav=title_of_fav)    


    def tt_save(self, project_name):
        """ This big-boy function will handle storing all the important info to a database.
        
        More on that later.

        """

        self.time_table_project_name = project_name
        # ...
        # ...


    # ------------------------------------------------------------------------------
    # ---------- FUNCTION DEFINITIONS ABOVE AND CLASS DEFINITIONS BELOW ------------
    # ------------------------------------------------------------------------------

    class Department:
        '''This is the department class, where teachers come from'''  
        # department_list = []

        def __init__(self, name, HOD="", is_special=False):
            """This is the department class. It is the SCHOOL SUBJECT to be 
            handled. However, it might not be an academic_class. It just 
            could be recess or what we call a special class.

            The 'is_special' argument helps to identify if the class is or isn't
            a special class"""

            self.dept_name = name.title()
            self.is_special = is_special

            # -- The "client_classes" attribute is a list of all the school class ARMS incident with the department
            self.client_classes = set()
            self.info = f"Special subject: {self.dept_name}"

            if not self.is_special:
                self.HOD = HOD
                # TimeTable.Department.department_list.append(self)
                self.id_num = 0
                self.info = f"Name of subject: {self.dept_name}"
                # print("Hello Tomi")
                self.teachers_list = []


            # -- This is_para attr is to test whether this department should always feature 
            # in the timetable alongside another department during the same period.
            self.is_para = False
                

        def teachers_rating_list(self, desc=False):
            """ This function, by default, rates the teachers according to how many classes they teach in ascending order.
             Descending order when the 'desc' (for descending) parameter is set to True """

            if not self.is_special:
                rating = namedtuple("Teachers_rating", "teacher_obj classes_taught")
                rating_list = [rating(teacher, teacher.classes_count) for teacher in self.teachers_list]

                if not desc:
                    rating_list.sort(key=lambda item: item.classes_taught)
                else:
                    rating_list.sort(key=lambda item: item.classes_taught, reverse=True)
                return rating_list

            raise ProjectExceptions.IsASpecialDept("This special subject does not possess teachers' info ")
                

        def _add_teacher(self):
            """ This function creates a teacher from scratch as a member of the department.

            The function that adds the teacher to the list of teachers in the department
            is built into the "Teacher class", and so is not necessary here. """

            teacher = TimeTable().Teacher(self)

            print(f"Teacher with id: {teacher.all_teachers_dept_id}, has been"
                f" added to the {self.dept_name} department")
            return teacher



        def assign_teacher(self, descent=False, auto=True, teacher_index=None):
            '''This function assigns a teacher already in 
            the list to a class.
            It simply gives the teacher with the lowest class rating'''

            # To rearrange the teachers according to the ratings_list sorting
            if not self.is_special:
                if auto:
                    self.teachers_list = [x.teacher_obj for x in self.teachers_rating_list(desc=descent)]
                    return self.teachers_list[0]
                else:
                    return self.teachers_list[teacher_index]
                # --- the function to assign teacher returns False if it is not a special period
            return False
            
        def __repr__(self):
            return f"Department: {self.dept_name}"
            


    class Teacher:
        '''The teacher object which is in composition
        with the department object, i.e, "teacher has a department"
        he is from'''
        def __init__(self, dept_obj):

            self.personalId = None

            self.teachers_department_list = [dept_obj]
            # self.teachers_department_set = set(self.teachers_department_list)


            # -------------------------------------------------------------------------------------------
            # -- Upon initialization, only one dept object is given thus teacher 
            # -- instance is given to its list of teachers
            self.teachers_department_list[0].teachers_list.append(self)
            # the above stores the current teacher in the array of its department for easy referencing

            self.teachers_department_list[0].id_num += 1
            self.classes_taught = []

            
        @property
        def classes_count(self):
            return len(self.classes_taught)

        @property
        def all_teachers_dept_id(self):
            self.teachers_dept_id = {}

            for dept in self.teachers_department_list:
                # dept.id_num += 1
                self.teachers_dept_id[dept] = dept.id_num

            return self.teachers_dept_id


        def __repr__(self):
            return f"'{self.teachers_department_list}' Teacher_obj with personal_id: {self.personalId}"


        def add_dept_to_teacher(self, dept_obj):
            """Apparently, a teacher can teach in more than one department (e.g. math and further maths).
            This function adds a new unique department object to the list of departments owned by the teacher"""

            # -- To check to make sure no duplicates exist
            for dept in self.teachers_department_list:
                if dept == dept_obj:
                    raise ProjectExceptions().TeacherAlreadyGivenSaidSubject("Teacher has previously been assigned dept object")
            
            dept_obj.teachers_list.append(self)
            dept_obj.id_num += 1
            self.teachers_department_list.append(dept_obj)
            


    class SchoolClassGroup:
        """ This py-class is the collection (container) of school classes of a certain kind.
        Could be thought of as the junior school or senior school which contains classes. """

        def __init__(self, class_group_name, class_group_description=None, abbrev=None):
            # -- the 'abbrev' parameter gives a short name for the school class group
            self.class_group_name = class_group_name.capitalize()
            self.description = class_group_description
            self.abbreviation = abbrev

            # -- contains all the school classes in the group
            self.school_class_list = []

        def __repr__(self):
            return self.abbreviation if self.abbreviation else self.class_group_name



    class SchoolClass:
        """ This class represents the school class.The 'level_iden' parameter implies that '1' might
         represent 'jss 1' and so on.
         """

        def __init__(self, level_iden, school_class_group_obj):

            self.level = str(level_iden + 1).title()
            self.school_class_group = school_class_group_obj
            self.school_class_arm_list = []
            self.school_class_group.school_class_list.append(self)
            

        @property
        def get_school_class_name(self):
            return f"{self.school_class_group.__repr__()}_{self.level}"

        def __repr__(self):
            return self.get_school_class_name + " object"
        

    class SchoolClassArm:
        """ This class models every arm that a school class has. It can represent the arms 
        with letters or numbers.
        The 'as_alpha' parameter controls this. short 'is_a_letter_of_the_alphabet' """

        def __init__(self, num_id, school_class_obj, as_alpha=True):

            if as_alpha:
                self.arm_id = string.ascii_letters[int(num_id)].capitalize()
            else:
                self.arm_id = num_id + 1

            self.school_class = school_class_obj


            self.periods=[]
            self.period_id_counter = 0
            self.school_class.school_class_arm_list.append(self)



            # -- This is the list of departments (str) that the school class arm offers
            self.departments_offered = []

        @property
        def get_full_arm_name(self):
            return f"{self.school_class.get_school_class_name}_{self.arm_id}"


        def para_departments(self, *dept_names):
            """This method handles a group of two more departments in which one class occur simultaneously 
            as an option to the other."""

            # -- this is a tuple holding the para-departments

            self.para_depts = str(dept_names).strip("()")
            # --more on this later



        def depts_offered_and_weights(self):
            """This function returns every subject/dept offered by the class arm 
            and how many periods(weights or frequencies, if you prefer) that they 
            take up for each per week """
            
            weight_dict ={}

            for dept in self.departments_offered:
                weight_dict[dept] = 0
            return weight_dict
            

        def __repr__(self):
            return self.get_full_arm_name
        



    class Period:
        '''Model for every class period.
        it is owned by a school class ARM and has a teacher
        from a department (or not, if it is a special (favourite) period)'''

        def normal_period(self, day_obj, start, duration, sch_class_arm_obj, dept_obj=None, end=None):
            """   This is the model of a normal academic period  """
            
            # ------ START AND END TIMES WILL BE PUT IN THE CALCULATION! WE CAN'T LEAD WITH THOSE!

            self.subject = dept_obj # the department (subject)

            day = day_obj  # the day of the week, or the time period

            self.school_class_arm = sch_class_arm_obj
            self.teacher = None if not self.subject else self.subject.assign_teacher()
            # Doing this because it's very possible for the period to be free (without a department handling it!)

            # Add the class to the list of classes taught by the teacher
            if self.subject:
                self.teacher.classes_taught.append(self.school_class_arm)

                # -- The below is to register the class arm as one of the classes taught by the department
                # -- This could have been extracted from the teacher.classes_taught of each teacher in the department
                # -- But, what if the department (maybe break time e.g) has no teacher? its class arms would still need to be recorded
                self.subject.client_classes.add(self.school_class_arm)


                # -- adds the subject to the list of subjects taken by the class arm
                self.school_class_arm.list_of_all_subjects.append(self.subject)

            self.start = start  # The start time for the period
            if end:
                self.end = end   # The end time for the period
            else:
                # self.duration = TimeTable.tuple_to_num(duration, 60)
                self.end = TimeTable.add_sub_time(start, duration)

            self.school_class_arm.periods.append(self)

            day.school_class_arms_per_day.append(self.school_class_arm)

            self.period_name = f"'{self.subject.dept_name}' period for {self.school_class_arm}" if self.subject else "Free Period"


            # -- Update the period counter of the school_class arm
            self.school_class_arm.period_id_counter += 1

            self.period_id = self.school_class_arm.period_id_counter

            return self



        def fav_period(self, day_obj, duration, spot=None, start=None, dept_obj=None, sch_class_arm_obj=None, title_of_fav=None):
            """Short for 'favourite period'. This is a period which MUST occupy a 
            particular spot on the time-table. A static period.

            START has to be a time tuple.
            so also DURATION.
            """

            day = day_obj

            if spot:
                # Put the period in the (spot-1)th spot of the period list
                pass
            else:
                if not start:
                    raise ProjectExceptions.CannotAssignFavPeriod("Cannot assign special period. Parameters have not been met")
                else:
                    self.duration = duration
                    self.start = start
                    self.end = TimeTable.add_sub_time(self.start, self.duration)
                    self.school_class_arm = sch_class_arm_obj

                    if dept_obj:
                        self.subject = dept_obj
                        self.teacher = self.subject.assign_teacher()

                        # --Add the class arm to the list of arms taught by the teacher
                        self.teacher.classes_taught.append(self.school_class_arm)

                        # -- The below is to register the class arm as one of the classes taught by the department
                        # -- This could have been extracted from the teacher.classes_taught of each teacher in the department
                        # --But, what if the department (maybe break time e.g) has no teacher? its class arms would still need to be recorded
                        self.subject.client_classes.add(self.school_class_arm)
                    else:
                        self.subject = title_of_fav if title_of_fav else "Special static period"
                    self.school_class_arm.periods.append(self)
                    self.period_name = f"Specially for {self.school_class_arm}"

            self.school_class_arm.period_id_counter += 1
            self.period_id = self.school_class_arm.period_id_counter

            day.school_class_arms_per_day.append(self)
            return self


        @property
        def get_period_name(self):
            num_name = self.school_class_arm.periods.index(self)
            return f"Period_{num_name + 1}: {self.period_name}"

        def __repr__(self):
            return self.get_period_name


        def add_dept_to_period(self, dept_obj):
            """ If the period was initially created free,and it was decided as an afterthought 
            to add a subject to it, i.e. make it an academic class, this function does the needful 
            of providing a teacher and all the other below-mentioned things. """
           
            if self.subject:
                return

            self.subject = dept_obj
            self.teacher = self.subject.assign_teacher() if self.subject.is_special else "Teacher not needed"
            self.teacher.classes_taught.append(self.school_class_arm)


    class Day:
        """
            This class represents all the days for which the timetable runs. This could be 5 days (
            the standard for schools) or other. 

            The 'rating' parameter in the init method is to help rank
            the objects of this class
        """

        def __init__(self, day_name="monday", day_id=1, rating=None):
            self.day = day_name.capitalize()
            self.day_id = day_id
            self.rating = rating

            self.day_name = self.day + "_" + str(day_id)

            self.school_class_arms_per_day = []


        def class_periods(self):
            '''This function squeezes out every period for 
            every school class arm that has been instantiated.
            It does this by going through the school class 
            list and finding out every period associated with 
            that school class (that has already been instantiated)
            for that day.
            '''
            classes_period_dict = {clss: clss.periods for clss in self.school_class_arms_per_day}
            return classes_period_dict


    #---------------------------------------------------------------------
    # --------- Below are the static class functions, that help make some
    # -- calculation or the other.

    def _remove_obj_from_list(list_obj, obj=None, id=None):
        """This function removes an object from the list given"""
        if obj:
            list_obj.remove(obj)
        else:
            del list_obj[int(id)]



    def _tuple_to_absolute(tuple, base):
        '''Important function to convert all the numbers in a 
        tuple, say a time tuple to an integer, based on a certain base.
        this could be used to convert a time tuple (hours, mins, secs) to 
        a integer in seconds.
        This function will be used in the classes (or methods defined above)'''

        tup_len = len(tuple)
        ans = 0
        for i, item in enumerate(tuple):
            ans += item*(base**(tup_len -1 -i))
        return ans


    def _add_sub_time(time_tuple1, time_tuple2, add=True):
        '''
        Adds or subtracts two (hour, minute, seconds) tuples.
        time_tuple1 always is a tuple, 

        However, time_tuple could
        be an integer or a tuple based on if it is an actual time
        (rendered as a tuple) or duration.

        WORKS FOR BOTH TIME DIFFERENCE (BETWEEN TWO TIME TUPLES) 
        AND TIME AND DURATION (TIME TUPLE AND AN INTEGER)!

        time_tuple2 is the duration for the period or whatever
        '''

        if isinstance(time_tuple2, tuple):
            time2 = TimeTable.tuple_to_num(time_tuple2, 60)
        else:
            time2 = time_tuple2
        # the above unpacks the tuple arguments.

        time1 = TimeTable.tuple_to_num(time_tuple1, 60)
        
        # The above converts the time to absolute time in 
        # seconds
        if add:
            time3 = time1 + time2
        else:
            time3 = time1 - time2
        # Adds or subtracts the time depending on the add argument
        return TimeTable.num_to_tuple(time3, 60)


    def _boundary_split_into_periods(start, end, n):
        '''To split a given duration of time into "n" periods
        START and END are tuples and are to be given in 
        24-hr format. the tuples should be populated with 
        (hour, minute, seconds) items.
        -------------------------------------------------
        '''
        lower_bound = TimeTable.tuple_to_num(start, 60)
        upper_bound = TimeTable.tuple_to_num(end, 60)

        interval = (upper_bound - lower_bound) // n

        period_interval_list = []
        indiv_time_bounds = namedtuple("boundary", "start end")

        start_iter = start
        
        for m in range(n):
            """ Primarily, this part adds the time interval the start to get 
            the end, and then the start updates to the end, so the next period begins 
            at the end of the first!
            """
            add_interval_tup = TimeTable.add_sub_time(start_iter, interval)

            #---- Adds the "interval tuple" to the start time tuple which is given as
            # one of the parameters to the function. It returns a time tuple.

            period_interval = indiv_time_bounds(start_iter, add_interval_tup)
            period_interval_list.append(period_interval)

            # -- update the start_iter variable with the end of the previous period below
            start_iter = add_interval_tup

        return period_interval_list
        
        
    def _to_base(num, base):
        '''Converts a number "num" to base "base"
        and renders it as a tuple of place values according to
        said base '''
        valid, ans_list, number = True, [], num % 86400
        
        while valid:
            if number == 0:
                valid = False
            else:
                ans_list.append(number % base)
                number = number // base

        ans_list.reverse()
        return tuple(ans_list)


    remove_from_list = staticmethod(_remove_obj_from_list)
    split_into_periods = staticmethod(_boundary_split_into_periods)
    add_sub_time = staticmethod(_add_sub_time)
    tuple_to_num = staticmethod(_tuple_to_absolute)  # takes in Time tuple, (h,m,s) as arg to yield number.
    num_to_tuple = staticmethod(_to_base) # Also time tuples



    # ACTUALLY, I DO NOT THINK THAT THE ADDING OF THE SCHOOL CLASS ARM TO THE DEPARTMENT
    # AND ADDING EACH DEPARTMENT TO THE SCHOOL CLASS ARM SHOULD TAKE PLACE IN THE PERIOD OBJECT
    # IT PROBABALY SHOULD HAVE HAPPENED BEFORE THEN.
    # CHECK THROUGH AND RE-THINK