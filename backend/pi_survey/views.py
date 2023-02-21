from django.shortcuts import render, HttpResponse, get_list_or_404

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
import json

from urllib3 import HTTPResponse
from apis.models import Person, Grant, Funder, Publication
from .models import Survey
import logging
from .notification import send_email

logger = logging.getLogger(__name__)

# def get_token(fnc):
#     def inner(*args, **kwargs):
#         fnc(*args, **kwargs)
#     return inner

def index(request):
    return render(request, 'survey_form.html', {})

def convert_to_list(value):
        """
        Converts the given value to a list
        """
        if not value:
            return []
        if isinstance(value, list):
            return value
        return [value]

def send_notification_by_smtp(notification_data):
    from_address = notification_data.get('from_address')
    to_addresses = notification_data.get('to_addresses')
    cc_addresses = notification_data.get('cc_addresses')
    bcc_addresses = notification_data.get('bcc_addresses')
    subject = notification_data.get('subject')
    body = notification_data.get('body')
    reply_to = notification_data.get('reply_to')
    if from_address and to_addresses and subject and body:
        has_error = send_email(from_address, 
            convert_to_list(to_addresses), 
            convert_to_list(cc_addresses), 
            convert_to_list(bcc_addresses), 
            subject, body, attachments=None, 
            reply_to=reply_to)
        if has_error:
            msg = 'Error sending email'
            logger.error(msg)
        else:
            msg = 'Email sent successfully'
            logger.info(msg)
        # msg = 'Notification data does not have enough information'
        # logger.error(msg)

def create_email_body(survey):
    pi_or_copi = "Co-PI" if survey.is_copi else "PI"
    email_body = """
        <html>
            <body>
                <p>
                    Thank you for filling out the survey. After our staff reviews it for inclusion in the COVID Information Commons, you can view it <a href="https://cic-apps.datascience.columbia.edu/grants/">here.</a>
                </p>
                <p>
                    If you have another award, please fill out the survey form again. 
                </p>
                <br>
                Thanks,<br>
                CIC Project Team
                <br>
                <h2>Survey data submitted</h2>
                <table>
                    <tr>
                        <th align="left">Your first name: </th>
                        <td>{first_name}</td>
                    </tr>
                    <tr>
                        <th align="left">Your last name: </th>
                        <td>{last_name}</td>
                    </tr>
                    <tr>
                        <th align="left">Your email address: </th>
                        <td>{email}</td>
                    </tr>
                    <tr>
                        <th align="left">Your ORCID iD (type NA if you do not have an ORCID): </th>
                        <td>{orcid}</td>
                    </tr>
                    <tr>
                        <th align="left">COVID-19 Research Award Number (NSF examples: 2143487, 1449617; NIH examples: 75N94021D01039-0-759402200003-1, 3UL1TR003015-04S1)</th>
                        <td>{award_id}</td>
                    </tr>
                    <tr>
                        <th align="left">COVID-19 Research Award Title: </th>
                        <td>{award_title}</td>
                    </tr>
                    <tr>
                        <th align="left">Are you PI or Co-PI?: </th>
                        <td>{pi_or_copi}</td>
                    </tr>
                    <tr>
                        <th align="left">COVID-19 Funding Agency: </th>
                        <td>{funder_name}</td>
                    </tr>   
                    <tr>
                        <th align="left">Please provide suggested keywords for your award, as applicable.: </th>
                        <td>{grant_keywords}</td>
                    </tr>  
                    <tr>
                        <th align="left">Please list DOIs for any of your published research associated with your COVID award. This can include articles, data sets, software packages, etc.: </th>
                        <td>{dois}</td>
                    </tr> 
                    <tr>
                        <th align="left">Please list any areas of scientific expertise your project could benefit from or is seeking, as keywords.: </th>
                        <td>{grant_additional_keywords}</td>
                    </tr> 
                    <tr>
                        <th align="left">Please list URLs of any of your professional websites associated with this award.: </th>
                        <td>{websites}</td>
                    </tr>
                    <tr>
                        <th align="left">Please list your areas of scientific expertise as keywords.: </th>
                        <td>{person_keywords}</td>
                    </tr>
                    <tr>
                        <th align="left">If applicable, please further specify any collaboration opportunities you are interested in pursuing as related to this award, for instance "looking for predictive analytics experts for collaboration" or "can offer assistance with xxx".: </th>
                        <td>{desired_collaboration}</td>
                    </tr> 
                    <tr>
                        <th align="left">Where would you like to connect with other COVID-19 researchers? (e.g. Slack, listserv, Google Group, etc.): </th>
                        <td>{person_comments}</td>
                    </tr>
                    <tr>
                        <th align="left">Additional comments for CIC staff: </th>
                        <td>{person_additional_comments}</td>
                    </tr>
                </table>
            </body>
        </html>
    """.format(first_name=survey.first_name, last_name=survey.last_name, email=survey.email,
    orcid=survey.orcid, award_id=survey.award_id, award_title=survey.award_title,
    pi_or_copi=pi_or_copi, funder_name=survey.funder_name, grant_keywords=survey.grant_keywords,
    dois=survey.dois, grant_additional_keywords=survey.grant_additional_keywords,
    websites=survey.websites, person_keywords=survey.person_keywords, desired_collaboration=survey.desired_collaboration, 
    person_comments=survey.person_comments, person_additional_comments=survey.person_additional_comments)
    return email_body

@csrf_exempt
#@get_token
def submitForm(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            survey = Survey(
                first_name = data.get('first_name', None),
                last_name = data.get('last_name', None),
                email = data.get('email', None),
                orcid = data.get('orcid', None),
                award_id = data.get('award_id', None),
                award_title = data.get('award_title', None),
                funder_name = data.get('funder', None),
                grant_keywords = data.get('grant_kw', None),
                grant_additional_keywords = data.get('grant_add_kw', None),
                dois = data.get('dois', None),
                websites = data.get('websites', None),
                person_keywords = data.get('person_kw', None),
                desired_collaboration = data.get('desired_collaboration', None),
                person_comments = data.get('person_comments', None),
                person_additional_comments = data.get('additional_comments', None),
                is_copi = data.get('is_copi', None)
            )
            survey.save()
            notification_data = {
                    'from_address': 'covidinfocommons@columbia.edu',
                    'to_addresses': survey.email,
                    'bcc_addresses': 'sg3847@columbia.edu, rs4256@columbia.edu',
                    'subject': 'TEST-Thank you for submitting your COVID PI entry',
                    'reply_to': 'covidinfocommons@columbia.edu',
                    'body': create_email_body(survey)
            }
            send_notification_by_smtp(notification_data)
        except Exception as e:
            print(e)
    return HttpResponse('')