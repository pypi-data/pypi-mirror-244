import time
import os

import redis

from data_verifier.model.lsa_model import ManageSubjectSelection
from data_verifier.identities.lsa_academy.logins.login import Login
from data_verifier.identities.lsa_academy.template import register_course_template
from data_verifier.utils.persist_cookies import PersistCookies


class RegisterCourse(Login):
    register_course_url = "https://cumsdtu.in/LSARegistration/api/saveSchedule"
    faculty_url = "https://cumsdtu.in/LSARegistration/api/getFaculties?instId=1"

    INSIGNIFICANT_KEYS = ['electiveCoursesList', 'extraValueMap', 'helperData', 'nextStageId', 'saveDeleteRecord',
                          'sessionId', 'minimumRegistrationCredit', 'maximumRegistrationCredit', 'paymentDescription',
                          'creditsRegistered', 'showSpecializations', 'specialization1', 'specialization2', 'status',
                          'totalAmount',
                          'waitListed', 'choiceType', 'countVisible', 'credits', 'creditsTypeChoice', 'extraInfo',
                          'extraValueMap',
                          'facultyName', 'gradeId', 'headerFlag', 'minimumSeats', 'numChoice', 'orgStageId',
                          'prevSubjId', 'registrationCount', 'resultStatus', 'seats',
                          'subHeader2Flag', 'subHeaderFlag', 'substitutedCourseId', 'substitutedCourseLabel',
                          'totalAvailableSeats', 'totalSeats',
                          ]
    maps = ['courseCode', 'courseGroupLabel', 'courseId', 'courseName', 'registrationCount', 'totalSeats']
    heading = ['Course Code', 'Course Group Name', 'Course Id', 'Course Name', 'Seats Registered',
               'Total Seats']

    applicant_class = ManageSubjectSelection

    def __init__(self, to_verify, **kwargs):
        super().__init__(to_verify, **kwargs)
        self.to_verify = to_verify
        self.persistor = self.safe_dict(kwargs, 'persistor')
        self.student_id = self.safe_dict(kwargs, 'student_id')
        self.force_reg = self.safe_dict(kwargs, 'force_reg', False)
        self.course_file_name = self.safe_dict(kwargs, 'course_file')

        # faculty and faculty file is new changes to the registration portal for the MOOC course
        self.faculty = self.safe_dict(kwargs, "faculty", None)
        self.faculty_file_name = self.safe_dict(kwargs, "faculty_file")

    def check_portal(self):
        if self.find_msg(self.reg_data.get('extraInfo')).__contains__('Registration is not open'):
            return False

        return True

    def pre_query(self):

        if not self.check_portal() and not self.force_reg:
            return self.custom_response(True, self.find_msg(self.reg_data.get('extraInfo')), 400)

        if self.faculty_file_name:
            self.get_faculty()
            return self.custom_response(False, "Faculty file generated", 200)


        result = self.find_subject_details(self.to_verify.set_code, self.to_verify.subject_id)

        if result.get('error'):
            return result

        # if result.get('disabledFlag'):
        #     return self.custom_response(True, "Course Disabled cannot register, Course: {} set:{}".format(
        #         result.get('courseName'), self.to_verify.set_code), 409)

        result = self.check_registered(result)
        if result.get('status') == 1:
            return self.custom_response(True, result.get('msgLst'), 400)

        return self.query_info(result=result)

    def get_faculty(self):
        response = self.smart_request("GET", self.faculty_url, headers=self.headers)

        json_data = self.safe_json(response.text)

        if json_data.get('error'):
            return self.custom_response(True, json_data.get('msgLst')[-1].get('errCode'), 400)

        details = json_data.pop('data')

        if self.faculty_file_name:
            path = os.path.join(os.getcwd(), self.faculty_file_name)
            self.get_faculty_data(details, faculty_file=path)
            return

        faculty_code = self.get_faculty_data(details, faculty_name=self.faculty)
        return faculty_code[0] if len(faculty_code) > 0 else None

    def query_info(self, **kwargs):

        result = kwargs['result']
        if self.faculty:
            result["facultyName"]=self.get_faculty()

        payload = register_course_template(self.student_id, self.to_verify.subject_id, result.get('eset_id'),
                                           result.get('facultyName'))

        respose = self.smart_request('POST', self.register_course_url, data=payload, headers=self.headers)

        json_data = self.safe_json(respose.text)
        details = json_data.pop('data')

        if json_data.get('error'):
            return self.custom_response(True, json_data.get('msgLst')[-1].get('errCode'), 400)

        self.pop_insignificant_keys(details)

        if self.course_file_name is not None:
            self.write_data(details.get('coreCoursesList'), self.course_file_name)
            return self.custom_response(False,
                                        "Course details written to {} successfully".format(self.course_file_name), 200)

        return self.custom_response(False, json_data.get('msgLst')[-1].get('errCode'), 200, data=details)

    @classmethod
    def extract_data(cls, db_ob, **kwargs):
        applicant = cls.applicant_class.applicant_to_object(db_ob)

        login_data = Login.do_login(applicant, **kwargs)

        if login_data.get('status') != 200:
            return login_data
        return cls(applicant, **{**login_data.pop('data'), **login_data, **kwargs}).pre_query()


def test():
    from data_verifier.utils.utils import EncryptDecrypt
    applicant = ManageSubjectSelection()
    applicant.username = '2K19/EE/126'
    applicant.password = EncryptDecrypt.enc_sha1('jatin_2001')
    applicant.set_code = 'E7'
    applicant.subject_id = 3811

    r = redis.StrictRedis()

    persistor = PersistCookies(r, 'api-manager-verifier:{}'.format(applicant.username.replace('/', '_')))
    print(applicant.subject_id)
    return RegisterCourse.extract_data(applicant, persistor=persistor, force_reg=True)


def test1():
    from data_verifier.utils.utils import EncryptDecrypt
    applicant = ManageSubjectSelection()
    applicant.username = '2k19/me/051'
    applicant.password = EncryptDecrypt.enc_sha1('April@2000')
    applicant.set_code = 'E10'
    applicant.subject_id = 5258

    r = redis.StrictRedis()

    persistor = PersistCookies(r, 'api-manager-verifier:{}'.format(applicant.username.replace('/', '_')))

    return RegisterCourse.extract_data(applicant, persistor=persistor, force_reg=True)


if __name__ == '__main__':
    print(test1())
    # while (True):
    #     try:
    #
    #         # print(test())
    #         details = test1()
    #
    #         print(details)
    #         if not details.get("error"):
    #             break
    #
    #         time.sleep(2)
    #
    #     except Exception as e:
    #         # import traceback
    #         #
    #         # traceback.print_exc()
    #         print("got exception: ", str(e))
