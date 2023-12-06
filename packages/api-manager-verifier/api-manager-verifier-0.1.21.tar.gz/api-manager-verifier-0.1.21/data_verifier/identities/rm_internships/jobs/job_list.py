import redis
import datetime
from data_verifier.utils.persist_cookies import PersistCookies
from data_verifier.identities.rm_internships.login.rm_login import RMLogin
from data_verifier.model.rm_model import RMLoginManager


class RMJobs(RMLogin):
    job_url = 'https://rm.dtu.ac.in/api/company/jobPost?page={}'
    notif_url = 'https://rm.dtu.ac.in/api/student/notifications?page={}'

    ALERT_TIME_LIMIT = 60

    INSIGNIFICANT_KEYS = ['email', 'createdAt', 'handledBy', 'updatedAt', '__v']

    def __init__(self, to_verify, **kwargs):
        super(RMJobs, self).__init__(to_verify, **kwargs)
        self.jobs = []
        self.job_filter_list = []
        # self.notifications=[]
        self.all_open_jobs = self.safe_dict(kwargs, 'all_open_jobs', False)
        self.open_jobs = self.safe_dict(kwargs, 'open_jobs', False)
        self.all_jobs = self.safe_dict(kwargs, 'all_jobs', False)
        self.get_profile()

    def filter_by_open(self):
        for i in self.jobs:

            open_date = self.get_timzone_convesion(datetime.datetime.fromisoformat(i.get('applicationOpen')[:-1]))
            close_date, now = self.get_timzone_convesion(
                datetime.datetime.fromisoformat(i.get('applicationClosed')[:-1]), True)

            index = self.jobs.index(i)
            i.pop('__v')
            if (close_date - now).total_seconds() > 60:
                diff = (close_date - now)
                i['applicationOpen'] = str(open_date.date())
                i['applicationClosed'] = str(close_date.date())
                i['remaining_time'] = diff
                i['created_at'] = str(self.get_timzone_convesion(i.pop('createdAt')[:-1]).date())
                i['updated_at'] = str(self.get_timzone_convesion(i.pop('updatedAt')[:-1]).date())
                i['seconds'] = diff.total_seconds()
                i['status'] = True
                self.job_filter_list.append(i)
            else:
                i['applicationOpen'] = str(open_date.date())
                i['applicationClosed'] = str(close_date.date())
                i['created_at'] = str(self.get_timzone_convesion(i.pop('createdAt')[:-1]).date())
                i['updated_at'] = str(self.get_timzone_convesion(i.pop('updatedAt')[:-1]).date())
                i['status'] = False

            self.jobs[index] = i

    def filter_job(self, index):

        if len(self.job_filter_list ) == 0 or index>5:
            return

        course = self.profile.get('course')
        branch = self.profile.get('branch')
        i=0
        while(i<len(self.job_filter_list)):
            course_name = self.courses[course].lower()
            if index == 0:
                if not self.job_filter_list[i].get(course_name):
                    self.job_filter_list.pop(i)
                    continue

            elif index == 1:
                if self.safe_list(self.branches, course, None) is not None:
                    if not branch in self.job_filter_list[i].get(course_name.lower() + 'Branches'):
                        self.job_filter_list.pop(i)
                        continue

            elif index == 2:
                aggr_cgpa = self.profile.get('aggregateCgpa')
                cutoff = self.job_filter_list[i].get(course_name.lower() + 'Cutoff')
                cutoff = cutoff if 0 <= cutoff <= 10 else 0
                if aggr_cgpa < cutoff:
                    self.job_filter_list.pop(i)
                    continue

            elif index == 3:
                twelth = self.profile.get('twelfthClass').get('percentage') * 9.5 if self.profile.get(
                    'twelfthClass').get(
                    'percentage') <= 10 else self.profile.get('twelfthClass').get('percentage')
                tenth = self.profile.get('tenthClass').get('percentage') * 9.5 if self.profile.get('tenthClass').get(
                    'percentage') <= 10 else self.profile.get('tenthClass').get('percentage')

                if tenth < self.job_filter_list[i].get('tenthPercentageCutoff') if self.job_filter_list[i].get('tenthPercentageCutoff') is not None else 0:
                    self.job_filter_list.pop(i)
                    continue
                elif twelth < self.job_filter_list[i].get('twelfthPercentageCutoff') if self.job_filter_list[i].get('twelfthPercentageCutoff') is not None else 0:
                    self.job_filter_list.pop(i)
                    continue

            elif index == 4:
                if self.job_filter_list[i].get('genderOpen') != "Both":
                    if self.job_filter_list[i].get('genderOpen', '').lower() != self.profile.get('gender', '').lower():
                        self.job_filter_list.pop(i)
                        continue

            elif index == 5:
                if self.job_filter_list[i].get('pwdOnly') and not self.profile.get('pwd'):
                    self.job_filter_list.pop(i)
                    continue

            i+=1

        self.filter_job(index + 1)

    def pre_query(self):
        # useless piece of code as taking much longer time to run

        # for i in range(100):
        #     response=self.smart_request('GET',self.notif_url.format(i+1),headers=self.headers)
        #     json = self.safe_json(response)
        #     if len(json.get('data'))==0:
        #         break
        #
        #     self.notifications.extend(json.get('data'))

        return self.query_info()

    def query_info(self):

        # for i in range(100):
        response = self.smart_request('GET', self.job_url.format(1), headers=self.headers)
        json = self.safe_json(response)
            # print("running loop: ",i+1)
            # print(json)
            # if len(json.get('data')) == 0:
            #     break

        self.jobs.extend(json.get('data'))

        return self.extract_info()

    def filter_branch_name(self, job_lst):
        jobs = []
        for i in job_lst:
            for j, v in enumerate(self.courses):
                if i.get(v.lower()):
                    branches = []
                    try:
                        for k in i.get(v.lower() + 'Branches'):
                            val = self.safe_list(self.safe_list(self.branches, j, []), k)
                            if val != "":
                                branches.append(val)
                    except:
                        continue
                    i[v.lower() + 'Branches'] = branches
            jobs.append(i)

        return jobs

    def filter_output(self, index=0):
        if index == 0:
            for i in self.jobs:
                indx = self.jobs.index(i)
                i['remaining_time'] = str(i.get('remaining_time', 0))
                self.jobs[indx] = i
        else:
            for i in self.job_filter_list:
                indx = self.job_filter_list.index(i)
                i['remaining_time'] = str(i.get('remaining_time'))
                self.job_filter_list[indx] = i

    def extract_info(self, **kwargs):
        self.filter_by_open()

        course = self.profile.get('course')
        branch = self.profile.get('branch')

        # this will return details of all the open jobs irrespective user branch, marks etc
        if self.all_open_jobs:
            self.filter_output(1)
            job = self.filter_branch_name(self.job_filter_list)
            return {'course': self.courses[course],
                    'branch': self.safe_list(self.safe_list(self.branches, course, []), branch), 'job_list': job}

        # this will filter job with respect to details
        self.filter_job(0)

        # this will return final open jobs that fits critera set by job poster
        if self.open_jobs:
            self.filter_output(1)
            job = self.filter_branch_name(self.job_filter_list)
            return {'course': self.courses[course],
                    'branch': self.safe_list(self.safe_list(self.branches, course, []), branch), 'job_list': job}

        # list of all the jobs irrespective of filters and open and closed both
        if self.all_jobs:
            self.filter_output(0)
            job = self.filter_branch_name(self.jobs)
            return {'course': self.courses[course],
                    'branch': self.safe_list(self.safe_list(self.branches, course, []), branch), 'job_list': job}

        self.filter_output(0)
        return self.jobs

    def get_jobs(self):
        return self.pre_query()

    @classmethod
    def extract_data(cls, db_ob, **kwargs):
        return cls(db_ob, **kwargs).pre_query()



import os
import pandas as pd
import pdfkit
import platform

class GenerateCoursePdf:
    maps = ['courseCode', 'courseGroupLabel', 'courseId', 'courseName', 'totalAvailableSeats', 'registeredFlag']
    heading = ['Course Code', 'Course Group', 'Course Id', 'Course Name', 'Available Seats', 'Is Registered']

    insignificant=[]
    def __init__(self):
        pass

    def course_details_filter(self, data: dict, filter_key=True,heading=None,map=None):
        heading = heading if heading is not None else self.heading
        map = map if map is not None else self.maps

        if filter_key:
            return {heading[i]: data.get(map[i]) for i in range(len(map))}
        else:
            return {heading[i].lower().replace(' ', '_'): data.get(map[i]) for i in range(len(map))}

    def filter_course_list(self, data: list, filter_course_items=True, filter_keys=True,heading=None,map=None):
        new_dict = dict()
        for i in data:
            if i.get('courseId') is not None:
                try:
                    # if len(i.get('courseGroupLabel'))>0 else str(i.get('courseGroupId'))
                    new_dict[i.get('courseGroupLabel')].append(
                        self.course_details_filter(i, filter_keys,heading=heading,map=map) if filter_course_items else i)
                except KeyError:
                    new_dict[i.get('courseGroupLabel')] = [
                        self.course_details_filter(i, filter_keys,heading=heading,map=map) if filter_course_items else i]
        return new_dict

    def conversion_for_xlmx(self, data: dict,heading=None):
        heading = heading if heading is not None else self.heading
        value = dict()
        for i in data.keys():
            for j in data.get(i):
                for items in heading:
                    try:
                        value[items].append(j.get(items))
                    except KeyError:
                        value[items] = [j.get(items)]
        return value

    def convert_to_pdf(self, data,heading=None,maps=None):
        data = self.filter_course_list(data,heading=heading,map=maps)
        json_data = self.conversion_for_xlmx(data,heading)
        df = pd.DataFrame(json_data)
        df.index = df.index+1
        table = df.to_html(classes='mystyle')

        text = f'''<html>
        <head><title>Course List with Available seats</title></head>
        <link rel="stylesheet" type="text/css" href="styles.css"/>
        <body>
            {table}
        </body>

        </html>'''

        return text

    @classmethod
    def get_conversion(cls, data,to_json=False):
        if not to_json:
            heading=[]
            maps=[]

            for i,j in zip(cls.maps,cls.heading):
                if i not in cls.insignificant:
                    heading.append(j)
                    maps.append(i)

            return cls().convert_to_pdf(data,heading=heading,maps=maps)
        else:
            return cls().filter_course_list(data,filter_keys=False)


class FileConversion:

    @classmethod
    def get_config(cls):

        if platform.system() == 'Darwin':
            return pdfkit.configuration()

        elif platform.system() == "Windows":
            return pdfkit.configuration(
                wkhtmltopdf=os.environ.get('WKHTMLTOPDF_BINARY',
                                           'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'))
        else:
            return pdfkit.configuration(wkhtmltopdf='./bin/wkhtmltopdf')

    @classmethod
    def to_pdf(cls, config, html_path: str, options=None, css_path: str = None):
        option = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
        }
        try:
            pdfkit.from_file(html_path, html_path.replace('.html', '.pdf'),
                             options=options if options is not None else option, configuration=config, css=css_path)
        except Exception as e:
            print(e)
            print(e.with_traceback(e.__traceback__))

        count=0
        import time
        while not os.path.exists(html_path.replace('.html', '.pdf')):
            if count>10:
                break
            count+=1
            time.sleep(1)


        if os.path.exists(html_path):
            os.remove(html_path)

        return html_path.replace('.html', '.pdf')

    @classmethod
    def to_html(cls, data: dict, html_path,insiginificant=None):
        GenerateCoursePdf.insignificant=[] if insiginificant is None else insiginificant

        html = GenerateCoursePdf.get_conversion(data)

        with open(html_path, 'w') as file:
            file.write(html)

        return html_path

class FilterJobs:

    @classmethod
    def all_jobs_html(cls, response,html_path):
        jobs=list()
        for i in response.get('job_list'):
            jobs.append(rm_all_jobs(response,i))

        df = pd.DataFrame(jobs)
        df.index = df.index + 1
        table = df.to_html(classes='mystyle')

        text = f'''<html>
                <head><title>List of all jobs at TNP RM</title></head>
                <link rel="stylesheet" type="text/css" href="all_jobs.css"/>
                <body>
                    {table}
                </body>

                </html>'''

        with open(html_path, 'w') as file:
            file.write(text)

        return html_path

def rm_all_jobs(response,i):
    return {"Name": i.get('name', ''),
            "Company Name": i.get('company', {}).get('name', ''),
          "Application Open ": i.get('applicationOpen'),
            "Application Close ": i.get('applicationClosed'),
          response.get('course'): 'Allowed' if i.get(response.get('course', '').lower()) else 'Not Allowed',
            response.get('branch'): 'Allowed' if response.get('branch') in i.get(response.get('course').lower()+"Branches", []) else 'Not Allowed',
          response.get('course') + "Cutoff": i.get(response.get('course', '').lower() + 'Cutoff', 0) if i.get(
              response.get('course', '').lower() + 'Cutoff', 0) is not None and i.get(
              response.get('course', '').lower() + 'Cutoff', 0) < 10 else '',
          "Backlogs Allowed": i.get('backlogsAllowed','0.0'),
            "Job Description": i.get('jobDescription'),
            "CTC": i.get('ctc'),
        }


def test():
    applicant = RMLoginManager()
    applicant.username = '2K19/ME/051'
    applicant.password = 'April@2000'

    r = redis.StrictRedis()

    persistor = PersistCookies(r, 'api-manager-verifier:{}'.format(applicant.username.replace('/', '_')))
    data= RMJobs.extract_data(applicant, persistor=persistor, all_jobs=True)

    option = {
        'page-size': 'Letter',
        'margin-top': '0.50in',
        'margin-right': '0.25in',
        'margin-bottom': '0.50in',
        'margin-left': '0.25in',
        'encoding': "UTF-8",
        'orientation': 'Landscape',
        'no-outline': None,
        'custom-header': [
            ('Accept-Encoding', 'gzip')]
    }

    if not os.path.exists(os.path.join(os.getcwd(), 'files')):
        os.mkdir(os.path.join(os.getcwd(), 'files'))

    path = os.path.join(os.getcwd(), 'files',applicant.username.replace('/', '_') + '_all_jobs.html')
    config = FileConversion.get_config()
    html = FilterJobs.all_jobs_html(data, path)
    pdf = FileConversion.to_pdf(config, html, options=option)
    return pdf

if __name__ == '__main__':
    print(test())
