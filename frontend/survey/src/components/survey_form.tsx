import * as React from 'react';
import { Component } from "react";
import axios from 'axios';
import {
   Formik,
   FormikHelpers,
   FormikProps,
   Form,
   Field,
   FieldProps,
} from 'formik';
 
interface MyFormValues {
  firstName: string;
}

type Person = {
  firstName: string;
  lastName: string;
  privateEmails: string;
  otherEmails: string;
  orcid: string
};

async function get_oauth_token() {
  try {
    const { data, status } = await axios.get(
      'https://oauth-test.cc.columbia.edu/as/authorization.oauth2?response_type=code&client_id=CIC_E_REST_APPS&scope=auth-columbia%20create%20update%20delete%20openid&redirect_uri=https//cice-dev.paas.cc.columbia.edu/v1',
      {
        headers: {
          "Sec-Fetch-Site": 'none',
          "Sec-Fetch-Mode": "navigate",
          "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        },
      },
    );

    console.log(JSON.stringify(data, null, 4));

    // 👇️ "response status is: 200"
    console.log('response status is: ', status);

    return data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.log('error message: ', error.message);
      return error.message;
    } else {
      console.log('unexpected error: ', error);
      return 'An unexpected error occurred';
    }
  }
}

async function createPerson(values:Person) {
  try {
    const { data } = await axios.post<Person>(
      'https://cice-dev.paas.cc.columbia.edu/v1/people',
      {
        "data": {
          "type": "Person",
          "attributes": {
            "first_name": values.firstName, 
            "last_name": values.lastName,
            "emails": values.otherEmails,
            "private_emails": values.privateEmails,
            "orcid": values.orcid
          }
        }
      },
      {
        headers: {
          'Content-Type': 'application/vnd.api+json',
          'Authorization': 'Bearer 8lx2BZax4woiNOdAiJ3XxUOOVCFa'
        }
      },
    );
    console.log(JSON.stringify(data, null, 4));
    return data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.log('error message: ', error.message);
      return error.message;
    } else {
      console.log('unexpected error: ', error);
      return 'An unexpected error occurred';
    }
  }
}

class SurveyForm extends Component {
  initialValues: MyFormValues = { firstName: '' };
  render() {
    return (
      <div>
        <h1>COVID Information Commons PI Survey</h1>
        <Formik
          initialValues={this.initialValues}
          onSubmit={(values, actions) => {
            console.log({ values, actions });
            alert(JSON.stringify(values, null, 2));
            var person = values as Person
            get_oauth_token()
            //createPerson(person)
            actions.setSubmitting(false);
          }}
        >
          <Form>
            <div>
              <label htmlFor="firstName">Your first name</label>
              <Field id="firstName" name="firstName" placeholder="Your answer" />
              <label htmlFor="lastName">Your last name</label>
              <Field id="lastName" name="lastName" placeholder="Your answer" />
            </div>
            <br/>
            <div>
            <label htmlFor="privateEmails">Email address(es)</label>
             <Field id="privateEmails" name="privateEmails" placeholder="Your answer" />
           </div>
           <br/>
           <div>
             <label>
              Other institutional email address(es) in addition to email address provided above (optional)
             </label>
             <Field id="otherEmails" name="otherEmails" placeholder="Your answer" />
           </div>
           <br/>
           <div>
             <label>Your ORCID iD (type NA if you do not have an ORCID)</label>
             <Field id="orcid" name="orcid" placeholder="Your answer" />
           </div>
           <div>
            <button type="submit">Submit</button>
           </div>
         </Form>
       </Formik>
     </div>
    )};
}

export default SurveyForm;
