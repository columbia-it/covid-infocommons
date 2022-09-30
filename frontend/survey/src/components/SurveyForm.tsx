import React, { useEffect, Component } from "react";
import { Formik, useFormikContext } from 'formik'
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import Stack from '@mui/material/Stack';
import axios from "axios";
import * as Yup from 'yup';

import {
    Paper,
    Button,
    TextField
  } from '@material-ui/core';

import { styled } from '@mui/material/styles';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';

const styles = {
    // See MUI Button CSS classes at https://mui.com/material-ui/api/button/
    "&.MuiButton-contained": {
	color: "#FFFFFF",
	backgroundColor: "#2C6BAC",
	minWidth: "max-content",
	whiteSpace: "nowrap",
    textTransform: "none"
    },
};

interface FormState {
    other_funder: string | ''
    first_name_error_msg?: string | null
    first_name_error: boolean | false
    last_name_error_msg?: string | null
    last_name_error: boolean | false
    award_id_error_msg?: string | null
    award_id_error: boolean | false
}

interface SurveyFormData {
    first_name: string
    last_name: string
    orcid: string
    emails: string
    other_emails: string
    award_id: string
    award_title: string
    grant_kw: string
    funder: string
    other_funder: string
    dois: string
    grant_add_kw: string
    websites: string
    person_kw: string
    desired_collaboration: string
    person_comments: string
    additional_comments: string
}

enum Funder {
    NSF,
    NIH,
    OTHER
}

let url = ''
if (process.env.NODE_ENV == 'production') {
    url = "https://cic-apps.datascience.columbia.edu";
} else if (process.env.NODE_ENV == 'development') {
    url = "https://cice-dev.paas.cc.columbia.edu";
} else {
    url = "http://127.0.0.1:8000"
}

const getFieldErrorNames = (formikErrors:any) => {
    const transformObjectToDotNotation = (obj:any, prefix = "", result:any = []) => {
      Object.keys(obj).forEach(key => {
        const value = obj[key]
        if (!value) return
  
        const nextKey:string = prefix ? `${prefix}.${key}` : key
        if (typeof value === "object") {
          transformObjectToDotNotation(value, nextKey, result)
        } else {
          result.push(nextKey)
        }
      })
  
      return result
    }
  
    return transformObjectToDotNotation(formikErrors)
  }

  const ScrollToFieldError = () => {
    const { submitCount, isValid, errors } = useFormikContext()
    useEffect(() => {
      if (isValid) return
  
      const fieldErrorNames = getFieldErrorNames(errors)
      if (fieldErrorNames.length <= 0) return
  
      const element = document.querySelector(
        `input[id='${fieldErrorNames[0]}']`
      )
      if (!element) return
  
      // Scroll to first known error into view
      element.scrollIntoView({ behavior: "smooth", block: "center" })
    }, [submitCount]) // eslint-disable-line react-hooks/exhaustive-deps
  
    return null
  }
  
class SurveyForm extends Component <any, FormState> {    
    constructor(props:any) {
        super(props)
        this.state = {
            other_funder: '',
            first_name_error_msg: null,
            first_name_error: false,
            last_name_error_msg: null,
            last_name_error: false,
            award_id_error_msg: null,
            award_id_error: false,
        }
        this.firstNameChangeHandler = this.firstNameChangeHandler.bind(this)
        this.lastNameChangeHandler = this.lastNameChangeHandler.bind(this)
        this.awardIdChangeHandler = this.awardIdChangeHandler.bind(this)
        this.handleOtherFunderChange = this.handleOtherFunderChange.bind(this)
        this.get_funder_name = this.get_funder_name.bind(this)
    }

    firstNameChangeHandler(event: React.ChangeEvent<HTMLInputElement>) {
        if (!event.target.value) {
            this.setState({"first_name_error_msg": "This is a required field"})
            this.setState({"first_name_error": true})

        } else {
            this.setState({"first_name_error_msg": null})
            this.setState({"first_name_error": false})
        }
    }

    lastNameChangeHandler(event: React.ChangeEvent<HTMLInputElement>) {
        if (!event.target.value) {
            this.setState({"last_name_error_msg": "This is a required field"})
            this.setState({"last_name_error": true})
        } else {
            this.setState({"last_name_error_msg": null})
            this.setState({"last_name_error": false})
        }
    }

    awardIdChangeHandler(event: React.ChangeEvent<HTMLInputElement>) {
        if (!event.target.value) {
            this.setState({"award_id_error_msg": "This is a required field"})
            this.setState({"award_id_error": true})
        } else {
            this.setState({"award_id_error_msg": null})
            this.setState({"award_id_error": false})
        }
    }

    get_funder_name(value: string) {
        for (var enumMember in Funder) {
            var isValueProperty = Number(enumMember) >= 0
            if (isValueProperty && (enumMember == value)) {
                if (Number(enumMember) == 2) {
                    return this.state.other_funder
                }
                return Funder[enumMember]
            }
        }
        return ''
    }

    handleOtherFunderChange(event:any) {
        this.setState({ other_funder: event.target.value })
        event.preventDefault()
    }

    validate_comma_separated_string(value:any) {
        const specialChars = /[`!#$%^&*()_+\-=\[\]{};':"\\|<>\/?~]/;
        if (specialChars.test(value)) {
            return false;
        }
        else {
            return true;
        }
    }

    validate_orcid(value: any) {
        const regex = new RegExp('(https?://)?([\\da-z.-]+)\\.([a-z.]{2,6})[/\\w .-]*/?');    
        let is_orcid_valid = true
        if (value == 'NA') {
            return is_orcid_valid
        }
        if (regex.test(value)) {
            if (value.indexOf("https://orcid.org/") !== -1) {
                let id = value.substring(18)
                if (id.length != 19) {
                    is_orcid_valid = false
                } else {
                    if (value.split("-").length != 4) {
                        is_orcid_valid = false
                    } else {
                        let id_parts = id.split("-")
                        const numbers_only_regex = new RegExp('[0-9]+');    
                        for (let i = 0; i < id_parts.length; i++) { 
                            if (numbers_only_regex.test(id_parts[i]) && id_parts[i].length == 4) {
                                is_orcid_valid = true
                            } else {
                                is_orcid_valid = false
                            }
                        }
                    }
                }
            } else {
                is_orcid_valid = false
            }
        } else {
            is_orcid_valid = false
        }
        return is_orcid_valid
    }

    handleSubmit(values:SurveyFormData) {
        if (values.funder == 'OTHER') {
            values.funder = this.state.other_funder
        }
        var payload = {
            first_name: values.first_name,
            last_name: values.last_name,
            orcid: values.orcid,
            emails: values.emails,
            other_emails: values.other_emails,
            award_id: values.award_id,
            award_title: values.award_title,
            grant_kw: values.grant_kw,
            funder: values.funder,
            dois: values.dois,
            grant_add_kw: values.grant_add_kw,
            websites: values.websites,
            person_kw: values.person_kw,
            desired_collaboration: values.desired_collaboration,
            person_comments: values.person_comments,
            additional_comments: values.additional_comments
        }
        var headers = {
            'Content-Type': 'application/json'
        }

        axios.post(url + "/survey/submit", payload, {
            headers: headers
          })
          .then((response) => {
              console.log('Success')
          })
          .catch((error) => {
            console.log(error)
          })
    }

    render() {
        return (
            <div className="form_div">
                <br/>
                <Paper style={{ padding: 16, fontFamily: '"proxima-nova","Montserrat",sans-serif' }}>
                <h1 className="survey-form-heading">
                    COVID Information Commons PI Survey
                </h1>
                <p>
                    Congratulations on your COVID-19 related research award!         
                </p>
                <p>
                    ⭐ Please fill out this form multiple times for each NSF or NIH individual award you have received ⭐
                </p>
                <br/>
                <p>
                    The COVID Information Commons (CIC) website, funded by the National Science Foundation (NSF #2028999 and 2139391) compiles information about COVID-19 related awards and research output from U.S. NSF, NIH and HHS grants. A key objective of this website is to enrich the standard public award information available regarding your research, and enhance opportunities for collaboration. 
                </p>
                <br/>
                <p>
                    As a COVID-19 research awardee, we invite you to provide voluntary contributions of additional, applicable public information about your project, beyond the award abstract, which you would like to make openly available via the COVID Information Commons website (https://covidinfocommons.net) in our PI Database.
                </p>
                <br/>
                <p>
                    You can always make changes to the information you provided by filling out the form again. Please email any questions to <a href="mailto:info@covidinfocommons.net">info@covidinfocommons.net</a>. Thank you!
                </p>
                </Paper>
                <br/>
                <br/>
                <Formik
                    initialValues={{
                        first_name: '',
                        last_name: '',
                        orcid: '',
                        emails: '',
                        other_emails: '',
                        award_id: '',
                        award_title: '',
                        grant_kw: '',
                        dois: '',
                        funder: Funder.NSF.toString(),
                        other_funder: '',
                        grant_add_kw: '',
                        websites: '',
                        person_kw: '',
                        desired_collaboration: '',
                        person_comments: '',
                        additional_comments: ''
                    }}
                    validationSchema = {
                        Yup.object({
                            emails: Yup.string().
                                required().
                                test('no-special-chars', 'Emails must be comma separated list', this.validate_comma_separated_string),
                            other_emails: Yup.string().
                                test('no-special-chars', 'Emails must be comma separated', this.validate_comma_separated_string),
                            grant_kw: Yup.string().
                                test('no-special-chars', 'Keywords must be comma separated', this.validate_comma_separated_string),
                            grant_add_kw: Yup.string().
                                test('no-special-chars', 'Keywords must be comma separated', this.validate_comma_separated_string),
                            person_kw: Yup.string().
                                test('no-special-chars', 'Keywords must be comma separated', this.validate_comma_separated_string),
                            orcid: Yup.string().
                                test('valid-url', 'Please enter ORCID as: https://orcid.org/xxxx-xxxx-xxxx-xxxx', this.validate_orcid)
                        })
                    }
                    onSubmit={(values, { resetForm }) => {
                        var form_values:SurveyFormData = {
                            "first_name": values.first_name.trim(),
                            "last_name": values.last_name.trim(),
                            "orcid": values.orcid.trim(),
                            "emails": values.emails.trim(),
                            "other_emails": values.other_emails.trim(),
                            "award_id": values.award_id,
                            "award_title": values.award_title,
                            "grant_kw": values.grant_kw.trim(),
                            "funder": this.get_funder_name(values.funder),
                            "other_funder": values.other_funder,
                            "dois": values.dois.trim(),
                            "grant_add_kw": values.grant_add_kw.trim(),
                            "websites": values.websites.trim(),
                            "person_kw": values.person_kw.trim(),
                            "desired_collaboration": values.desired_collaboration.trim(),
                            "person_comments": values.person_comments.trim(),
                            "additional_comments": values.additional_comments.trim()
                        }
                        this.handleSubmit(form_values)
                        resetForm({});
                        this.setState({ other_funder: '' })
                    }}
                >
                    {({ handleSubmit, handleBlur, values, handleChange, handleReset, setFieldValue, errors, touched }) => {
                        return (
                        <form onSubmit={(handleSubmit)} >
                            <ScrollToFieldError />
                            <div>
                                <Paper className="name-container">
                                    <div className="name-child-1">
                                        <FormControl>
                                            <FormLabel id="fname_label" className="label">
                                                Your first name <span className="required-text">*</span>
                                            </FormLabel>
                                            <TextField 
                                                id="first_name" 
                                                variant="outlined" 
                                                required 
                                                value={ values.first_name }
                                                onChange={ handleChange }
                                            />
                                            <br/>
                                            <br/>
                                        </FormControl>
                                    </div>
                                    <div className="name-child-2">
                                        <FormControl>
                                            <FormLabel id="lname-label" className="label">
                                                Your last name <span className="required-text">*</span>
                                            </FormLabel>
                                            <TextField 
                                                id="last_name" 
                                                variant="outlined" 
                                                required 
                                                value={ values.last_name }
                                                onChange={ handleChange }
                                            />
                                            <br/>
                                            <br/>
                                        </FormControl>
                                    </div>
                                </Paper>    
                                <br/> 
                            </div>
                            <br/>
                            <div>
                                <Paper style={{ padding: 16 }}>
                                    <FormControl className="name-input">
                                        <FormLabel id="emails-label" className="label">
                                            Your email address(es) <span className="required-text">*</span>
                                        </FormLabel>
                                        <TextField 
                                            id="emails" 
                                            variant="outlined" 
                                            required 
                                            value={ values.emails }
                                            onChange={ handleChange }
                                            onKeyUp={ handleBlur }
                                        />
                                        {errors.emails && touched.emails ? (<div className="required-text">{errors.emails}</div>) : null}
                                    </FormControl>
                                    <br/>
                                    <br/>
                                    <FormControl className="name-input">
                                        <FormLabel id="other-emails-label" className="label">
                                            Other institutional email address(es) in addition to email address provided above (optional)
                                        </FormLabel>
                                        <TextField 
                                            id="other_emails" 
                                            variant="outlined" 
                                            onChange={ handleChange }
                                            value={ values.other_emails }
                                            onKeyUp={ handleBlur }
                                        />
                                        { errors.other_emails && touched.other_emails ? (<div className="required-text">{errors.other_emails}</div>) : null }
                                    </FormControl>
                                    <br/>
                                </Paper> 
                            </div>
                            <br/>
                            <div>
                                <Paper style={{ padding: 16 }}>
                                    <FormControl className="name-input">
                                        <FormLabel id="orcid-label" className="label">
                                            Your ORCID iD (type NA if you do not have an ORCID)<span className="required-text">*</span>
                                        </FormLabel>
                                        <TextField 
                                            id="orcid" 
                                            variant="outlined" 
                                            required 
                                            value={ values.orcid }
                                            onChange={ handleChange }
                                            onBlur={ this.validate_orcid }
                                            onKeyUp={ handleBlur }
                                        />
                                        { errors.orcid && touched.orcid ? (<div className="required-text">{errors.orcid}</div>) : null }
                                    </FormControl>
                                    <br/>
                                    <br/>
                                </Paper> 
                            </div>
                            <br/>
                            <div>
                                <Paper style={{ padding: 16 }}>
                                    <FormControl className="name-input">
                                        <FormLabel id="award-id-label" className="label">
                                            COVID-19 Research Award Number <span className="required-text">*</span>
                                        </FormLabel>
                                        <TextField 
                                            id="award_id" 
                                            variant="outlined" 
                                            required 
                                            value={ values.award_id }
                                            onChange={ handleChange }
                                        />
                                    </FormControl>
                                    <br/>
                                    <br/>
                                </Paper>
                            </div>
                            <br/>
                            <div>
                                <Paper style={{ padding: 16 }}>
                                    <FormControl className="name-input">
                                        <FormLabel id="award-title-label" className="label">
                                            COVID-19 Research Award Title <span className="required-text">*</span>
                                        </FormLabel>
                                        <TextField 
                                            id="award_title" 
                                            variant="outlined" 
                                            required 
                                            value={ values.award_title }
                                            onChange={ handleChange }
                                        />
                                    </FormControl>
                                    <br/>
                                    <br/>
                                </Paper>
                            </div>
                            <br/>
                            <div>
                                <Paper style={{ padding: 16 }}>
                                    <FormControl>
                                        <FormLabel id="funder-label">COVID-19 Funding Agency <span className="required-text">*</span></FormLabel>             
                                            <RadioGroup
                                                aria-labelledby="funder-group-label"
                                                defaultValue="NSF"
                                                name="funder"
                                                onChange={ handleChange }
                                                value={ values.funder.toString() }
                                            >
                                            <FormControlLabel 
                                                value={ Funder.NSF.toString() } 
                                                control={<Radio />} 
                                                label="NSF" />
                                            <FormControlLabel 
                                                value={ Funder.NIH.toString() } 
                                                control={<Radio />} 
                                                label="NIH" />
                                            <FormControlLabel 
                                                value={ Funder.OTHER.toString() }
                                                control={<Radio/>}
                                                label={
                                                    <div>
                                                        <span>Other:</span>&nbsp;
                                                        <TextField 
                                                            onChange={ this.handleOtherFunderChange } 
                                                            id='other_funder_text'
                                                            value={ this.state.other_funder }/>
                                                    </div>
                                                }/>
                                        </RadioGroup>
                                    </FormControl>
                                </Paper>
                            </div>
                            <br/>
                            <br/>
                            <div>
                                <Paper style={{ padding: 16 }}>
                                    <FormControl className="name-input">
                                        <FormLabel id="grant-kw-label" className="label">
                                            Please provide suggested keywords for your award, as applicable.
                                        </FormLabel>
                                        <TextField 
                                            id="grant_kw" 
                                            variant="outlined" 
                                            value={ values.grant_kw }
                                            onChange={ handleChange }
                                            onKeyUp={ handleBlur }
                                        />
                                        { errors.grant_kw && touched.grant_kw ? (<div className="required-text">{errors.grant_kw}</div>) : null }
                                    </FormControl>
                                    <br/>
                                    <br/>
                                </Paper>
                            </div>
                            <br/>
                            <br/>
                            <div>
                                <Paper style={{ padding: 16 }}>
                                    <FormControl className="name-input">
                                        <FormLabel id="dois-label" className="label">
                                            Please list DOIs for any of your published research associated with your COVID award. This can include articles, data sets, software packages, etc.                                        
                                        </FormLabel>
                                        <TextField 
                                            id="dois" 
                                            variant="outlined" 
                                            value={ values.dois }
                                            onChange={ handleChange }
                                        />
                                    </FormControl>
                                    <br/>
                                    <br/>
                                </Paper>
                            </div>
                            <div>
                                <Paper style={{ padding: 16 }}>
                                    <FormControl className="name-input">
                                        <FormLabel id="grant-add-kw-label" className="label">
                                            Please list any areas of scientific expertise your project could benefit from or is seeking, as keywords.
                                        </FormLabel>
                                        <TextField 
                                            id="grant_add_kw" 
                                            variant="outlined" 
                                            value={ values.grant_add_kw }
                                            onChange={ handleChange }
                                            onKeyUp={ handleBlur }
                                        />
                                        { errors.grant_add_kw && touched.grant_add_kw ? (<div className="required-text">{errors.grant_add_kw}</div>) : null }
                                    </FormControl>
                                    <br/>
                                    <br/>
                                </Paper>
                            </div>
                            <div>
                                <Paper style={{ padding: 16 }}>
                                    <FormControl className="name-input">
                                        <FormLabel id="websites-label" className="label">
                                            Please list URLs of any of your professional websites associated with this award.
                                        </FormLabel>
                                        <TextField 
                                            id="websites" 
                                            variant="outlined" 
                                            value={ values.websites }
                                            onChange={ handleChange }
                                        />
                                    </FormControl>
                                    <br/>
                                    <br/>
                                </Paper>
                            </div>
                            <br/>
                            <br/>
                            <div>
                                <Paper style={{ padding: 16 }}>
                                    <FormControl className="name-input">
                                        <FormLabel id="person-kw-label" className="label">
                                            Please list your areas of scientific expertise as keywords.
                                        </FormLabel>
                                        <TextField 
                                            id="person_kw" 
                                            variant="outlined" 
                                            onChange={ handleChange }
                                            value={ values.person_kw }
                                            onKeyUp={ handleBlur }
                                        />
                                        { errors.person_kw && touched.person_kw ? (<div className="required-text">{errors.person_kw}</div>) : null }
                                    </FormControl>
                                    <br/>
                                    <br/>
                                </Paper>
                            </div>
                            <br/>
                            <br/>
                            <div>
                                <Paper style={{ padding: 16 }}>
                                    <FormControl className="name-input">
                                        <FormLabel id="desired-collaboration-label" className="label">
                                            If applicable, please further specify any collaboration opportunities you are interested in pursuing as related to this award, for instance "looking for predictive analytics experts for collaboration" or "can offer assistance with xxx".
                                        </FormLabel>
                                        <TextField 
                                            id="desired_collaboration" 
                                            variant="outlined" 
                                            onChange={ handleChange }
                                            value={ values.desired_collaboration }
                                        />
                                    </FormControl>
                                    <br/>
                                    <br/>
                                </Paper>
                            </div>
                            <br/>
                            <br/>
                            <div>
                                <Paper style={{ padding: 16 }}>
                                    <FormControl className="name-input">
                                        <FormLabel id="person-comments-label" className="label">
                                            Where would you like to connect with other COVID-19 researchers? (e.g. Slack, listserv, Google Group, etc.)
                                        </FormLabel>
                                        <TextField 
                                            id="person_comments" 
                                            variant="outlined" 
                                            onChange={ handleChange }
                                            value={ values.person_comments }
                                        />
                                    </FormControl>
                                    <br/>
                                    <br/>
                                </Paper>
                            </div>
                            <br/>
                            <br/>
                            <div>
                                <Paper style={{ padding: 16 }}>
                                    <FormControl className="name-input">
                                        <FormLabel id="add-comments-label" className="label">
                                            Additional comments
                                        </FormLabel>
                                        <TextField 
                                            id="additional_comments" 
                                            variant="outlined" 
                                            onChange={ handleChange }
                                            value={ values.additional_comments }
                                        />
                                    </FormControl>
                                    <br/>
                                    <br/>
                                </Paper>
                            </div>
                            <br/>
                            <br/>
                            <div>
                                <Stack spacing={20} direction="row">
                                    <Button variant="contained" 
                                        style={{
                                            backgroundColor: "#2C6BAC",
                                            color: "#FFFFFF"
                                        }}
                                        type='submit'
                                    >
                                        Submit
                                    </Button>
                                    <Button variant="text" onClick={ handleReset }>
                                        Clear form
                                    </Button>       
                                </Stack>
                            </div>
                            <br/>
                            <br/>
                        </form>
                    )}}
                </Formik>
            </div>
        );
    }   
}

export default SurveyForm;
