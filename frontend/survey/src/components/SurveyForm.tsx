import React, { useEffect, Component } from "react";
import { Formik, useFormikContext } from 'formik'
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import Typography from '@mui/material/Typography';
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
    ok_dialog_open: boolean | false
}

interface SurveyFormData {
    first_name: string
    last_name: string
    orcid: string
    email: string
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
    is_copi: boolean
    pi_or_copi: string
}

interface DialogTitleProps {
    id: string;
    children?: React.ReactNode;
    onClose: () => void;
}

enum Funder {
    NSF,
    NIH,
    OTHER
}

enum PI_OR_COPI {
    PI, 
    CoPI
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

  const BootstrapDialog = styled(Dialog)(({ theme }) => ({
    '& .MuiDialogContent-root': {
      padding: theme.spacing(2),
    },
    '& .MuiDialogActions-root': {
      padding: theme.spacing(1),
    },
  }));

  const BootstrapDialogTitle = (props: DialogTitleProps) => {
    const { children, onClose, ...other } = props;
  
    return (
      <DialogTitle sx={{ m: 0, p: 2 }} {...other}>
        {children}
        {onClose ? (
          <IconButton
            aria-label="close"
            onClick={onClose}
            sx={{
              position: 'absolute',
              right: 8,
              top: 8,
              color: (theme) => theme.palette.grey[500],
            }}
          >
            <CloseIcon />
          </IconButton>
        ) : null}
      </DialogTitle>
    );
  };
  
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
            ok_dialog_open: false
        }
        this.firstNameChangeHandler = this.firstNameChangeHandler.bind(this)
        this.lastNameChangeHandler = this.lastNameChangeHandler.bind(this)
        this.awardIdChangeHandler = this.awardIdChangeHandler.bind(this)
        this.handleOtherFunderChange = this.handleOtherFunderChange.bind(this)
        this.get_funder_name = this.get_funder_name.bind(this)
        this.handle_ok_dialog_close = this.handle_ok_dialog_close.bind(this)
        this.validate_comma_separated_string = this.validate_comma_separated_string.bind(this)
        this.validate_email = this.validate_email.bind(this)
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

    is_copi(value: string) {
        let selected_value = Number(value)
        if (selected_value > 0) {
            return true
        }
        return false
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

    get_pi_copi_name(value: string) {
        for (var enumMember in PI_OR_COPI) {
            var isValueProperty = Number(enumMember) >= 0
            if (isValueProperty && (enumMember == value)) {
                return PI_OR_COPI[enumMember]
            }
        }
        return ''
    }

    handleOtherFunderChange(event:any) {
        this.setState({ other_funder: event.target.value })
        event.preventDefault()
    }

    validate_comma_separated_string(value:any) {
        const specialChars = /[`!#$%^&*()_+\=\[\]{};':"\\|<>\/?~]/;
        if (specialChars.test(value)) {
            return false;
        }
        else {
            return true;
        }
    }

    validate_dois_string(value:any) {
        const specialChars = /[`!#$%^&*()_+\=\[\]{};'"\\|<>\?~]/;
        if (specialChars.test(value)) {
            return false;
        }
        else {
            return true;
        }
    }

    validate_email(value: any) {
        if (value != null) {
            value = value.trim()
            let email_exp = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            if (!value.match(email_exp)) {
                return false
            }
        }
        return true
    }

    validate_orcid(value: any) {
        let is_orcid_valid = false
        if (value != null) {
            value = value.trim()
            const regex = new RegExp('(https?://)?([\\da-z.-]+)\\.([a-z.]{2,6})[/\\w .-]*/?');    
            if (value == 'NA') {
                is_orcid_valid = true
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
                if (value.split("-").length != 4) {
                    is_orcid_valid = false
                } else {
                    let id_parts = value.split("-")
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
            return is_orcid_valid
        } 
        return is_orcid_valid
    }

    handleSubmit(values:SurveyFormData) {
        if (values.funder == 'OTHER') {
            values.funder = this.state.other_funder
        }
        if (values.orcid != 'NA' && values.orcid.indexOf("https://orcid.org/") == -1) {
            values.orcid = "https://orcid.org/" + values.orcid
        }
        // if (values.pi_or_copi == PI_OR_COPI.CoPI.toString()) {
        //     values.is_copi = true
        // } else {
        //     values.is_copi = false
        // }
        var payload = {
            first_name: values.first_name,
            last_name: values.last_name,
            orcid: values.orcid,
            email: values.email,
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
            additional_comments: values.additional_comments,
            is_copi: values.is_copi
        }
        var headers = {
            'Content-Type': 'application/json'
        }

        axios.post(url + "/survey/submit", payload, {
            headers: headers
          })
          .then((response) => {
              this.setState({
                  ok_dialog_open: true
              })
          })
          .catch((error) => {
            console.log(error)
          })
    }

    handle_ok_dialog_close() {
        this.setState({
            ok_dialog_open: false
        })
        window.scrollTo({top: 0, left: 0, behavior: 'smooth'});
    }

    handle_clear_form() {
        this.setState({
            other_funder: ''
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
                    The <a href="https://covidinfocommons.datascience.columbia.edu/">COVID Information Commons (CIC)</a> website, funded by the National Science Foundation (NSF #2028999 and 2139391) compiles information about COVID-19 related awards and research output from U.S. NSF, NIH and HHS grants. A key objective of this website is to enrich the standard public award information available regarding your research, and enhance opportunities for collaboration. 
                </p>
                <br/>
                <p>
                    As a COVID-19 research awardee, we invite you to provide voluntary contributions of additional, applicable public information about your project, beyond the award abstract, which you would like to make openly available via the <a href="https://covidinfocommons.datascience.columbia.edu/">COVID Information Commons (CIC)</a> website in our PI Database. 
                    After our staff reviews it for inclusion in the COVID Information Commons, you can view it <a href={ url + '/grants' } target="_blank">here. </a>If you have another award, please fill out the survey form again. 
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
                        email: '',
                        award_id: '',
                        award_title: '',
                        grant_kw: '',
                        dois: '',
                        funder: Funder.NSF.toString(),
                        pi_or_copi: PI_OR_COPI.PI.toString(),
                        other_funder: '',
                        grant_add_kw: '',
                        websites: '',
                        person_kw: '',
                        desired_collaboration: '',
                        person_comments: '',
                        additional_comments: '',
                        is_copi: false
                    }}
                    validationSchema = {
                        Yup.object({
                            first_name: Yup.string().required('First name is required'),
                            last_name: Yup.string().required('Last name is required'),
                            email: Yup.string().
                                required('Email address(es) is required').
                                test('validate_email', 'Email must be a valid email address', this.validate_email),
                            grant_kw: Yup.string().
                                test('no-special-chars', 'Keywords must be comma separated', this.validate_comma_separated_string),
                            grant_add_kw: Yup.string().
                                test('no-special-chars', 'Keywords must be comma separated', this.validate_comma_separated_string),
                            person_kw: Yup.string().
                                test('no-special-chars', 'Keywords must be comma separated', this.validate_comma_separated_string),
                            dois: Yup.string().
                                test('no-special-chars', 'Dois must be comma separated', this.validate_dois_string),
                            orcid: Yup.string().
                                required('ORCID iD is required').
                                test('valid-url', 'Please enter ORCID iD as: https://orcid.org/xxxx-xxxx-xxxx-xxxx or xxxx-xxxx-xxxx-xxxx', this.validate_orcid),
                            award_title: Yup.string().required('Award title is required'),
                            award_id: Yup.string().required('Award ID is required')
                        })
                    }
                    onSubmit={(values, { resetForm }) => {
                        var form_values:SurveyFormData = {
                            "first_name": values.first_name.trim(),
                            "last_name": values.last_name.trim(),
                            "orcid": values.orcid.trim(),
                            "email": values.email.trim(),
                            "award_id": values.award_id,
                            "award_title": values.award_title,
                            "grant_kw": values.grant_kw.trim(),
                            "funder": this.get_funder_name(values.funder),
                            "pi_or_copi": this.get_pi_copi_name(values.pi_or_copi),
                            "other_funder": values.other_funder,
                            "dois": values.dois.trim(),
                            "grant_add_kw": values.grant_add_kw.trim(),
                            "websites": values.websites.trim(),
                            "person_kw": values.person_kw.trim(),
                            "desired_collaboration": values.desired_collaboration.trim(),
                            "person_comments": values.person_comments.trim(),
                            "additional_comments": values.additional_comments.trim(),
                            "is_copi": this.is_copi(values.pi_or_copi),
                        }
                        this.handleSubmit(form_values)
                        resetForm({});
                        this.setState({ other_funder: '' })
                    }}
                >
                    {({ handleSubmit, handleBlur, values, handleChange, handleReset, setFieldValue, errors, touched }) => {
                        return (
                        <form onSubmit={(handleSubmit)} onKeyDown={
                            (keyEvent) => {
                                if (keyEvent.keyCode === 13) {
                                    keyEvent.preventDefault();
                                  }
                            }
                        }>
                            <ScrollToFieldError />
                            <div>
                                <Paper className="name-container">
                                    <div>
                                        <FormControl>
                                            <div>
                                                <FormLabel id="fname_label" className="label">
                                                    Your first name (plus middle initial, if any) <span className="required-text">*</span>
                                                </FormLabel>
                                            </div>
                                            <div className="name_input">
                                                <TextField 
                                                    id="first_name" 
                                                    variant="outlined" 
                                                    value={ values.first_name }
                                                    onChange={ handleChange }
                                                    onKeyUp={ handleBlur }
                                                    onBlur={ handleBlur }
                                                />
                                            </div>
                                            { errors.first_name && touched.first_name ? (<div className="required-text">{errors.first_name}</div>) : null }
                                            <br/>
                                            <br/>
                                        </FormControl>
                                    </div>
                                    <div>
                                        <FormControl sx={{width: '100%'}}>
                                            <div>
                                                <FormLabel id="lname-label" className="label">
                                                    Your last name<span className="required-text">*</span>
                                                </FormLabel>
                                            </div>
                                            <div className="name_input">
                                                <TextField 
                                                    id="last_name" 
                                                    variant="outlined" 
                                                    value={ values.last_name }
                                                    onChange={ handleChange }
                                                    onKeyUp={ handleBlur }
                                                    onBlur={ handleBlur }
                                                />
                                            </div>
                                            { errors.last_name && touched.last_name ? (<div className="required-text">{ errors.last_name }</div>) : null }
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
                                        <FormLabel id="orcid-label" className="label">
                                            Your ORCID iD (type NA if you do not have an ORCID)<span className="required-text">*</span>
                                        </FormLabel>
                                        <TextField 
                                            id="orcid" 
                                            variant="outlined" 
                                            value={ values.orcid }
                                            onChange={ handleChange }
                                            onKeyUp={ handleBlur }
                                            onBlur={ handleBlur }
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
                                        <FormLabel id="emails-label" className="label">
                                            Your email address <span className="required-text">*</span>
                                        </FormLabel>
                                        <TextField 
                                            id="email" 
                                            variant="outlined" 
                                            value={ values.email }
                                            onChange={ handleChange }
                                            onKeyUp={ handleBlur }
                                            onBlur={ handleBlur }
                                        />
                                        {errors.email && touched.email ? (<div className="required-text">{errors.email}</div>) : null}
                                    </FormControl>
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
                                                    </div>
                                                }/>
                                            <div><TextField 
                                                            onChange={ this.handleOtherFunderChange } 
                                                            id='other_funder_text'
                                                            value={ this.state.other_funder }/>
                                            </div>
                                        </RadioGroup>
                                    </FormControl>
                                </Paper>
                            </div>
                            <br/>
                            <div>
                                <Paper style={{ padding: 16 }}>
                                    <FormControl className="name-input">
                                        <FormLabel id="award-id-label" className="label">
                                            COVID-19 Research Award Number (NSF examples: 2028999, 2139391; NIH examples: 1U01CA260508-01, 1R43AI165117-01) <span className="required-text">*</span>
                                        </FormLabel>
                                        <TextField 
                                            id="award_id" 
                                            variant="outlined" 
                                            value={ values.award_id }
                                            onChange={ handleChange }
                                            onKeyUp={ handleBlur }
                                            onBlur={ handleBlur }
                                        />
                                        { errors.award_id && touched.award_id ? (<div className="required-text">{ errors.award_id }</div>) : null }                                        
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
                                            value={ values.award_title }
                                            onChange={ handleChange }
                                            onKeyUp={ handleBlur }
                                            onBlur={ handleBlur }
                                        />
                                        { errors.award_title && touched.award_title ? (<div className="required-text">{ errors.award_title }</div>) : null }

                                    </FormControl>
                                    <br/>
                                    <br/>
                                </Paper>
                            </div>
                            <br/>
                            <div>
                                <Paper style={{ padding: 16 }}>
                                    <FormControl>
                                        <FormLabel id="copi-label">Are you PI or Co-PI?</FormLabel>             
                                            <RadioGroup
                                                aria-labelledby="pi-copi-label"
                                                defaultValue="PI"
                                                name="pi_or_copi"
                                                onChange={ handleChange }
                                                value={ values.pi_or_copi.toString() }
                                            >
                                            <FormControlLabel 
                                                value={ PI_OR_COPI.PI.toString() }
                                                control={<Radio />} 
                                                label="PI" />
                                            <FormControlLabel 
                                                value={ PI_OR_COPI.CoPI.toString() }
                                                control={<Radio />} 
                                                label="CoPI" />
                                        </RadioGroup>
                                    </FormControl>
                                </Paper>
                            </div>
                            <br/>
                            <div>
                                <Paper style={{ padding: 16 }}>
                                    <FormControl className="name-input">
                                        <FormLabel id="grant-kw-label" className="label">
                                            Keywords related to your COVID project
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
                            <div>
                                <Paper style={{ padding: 16 }}>
                                    <FormControl className="name-input">
                                        <FormLabel id="grant-add-kw-label" className="label">
                                            Keywords related to your scientific research (COVID or other)
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
                            <br/>
                            <div>
                                <Paper style={{ padding: 16 }}>
                                    <FormControl className="name-input">
                                        <FormLabel id="websites-label" className="label">
                                            PI website and project relevant websites
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
                            <div>
                                <Paper style={{ padding: 16 }}>
                                    <FormControl className="name-input">
                                        <FormLabel id="dois-label" className="label">
                                            DOIs of articles, datasets 
                                        </FormLabel>
                                        <TextField 
                                            id="dois" 
                                            variant="outlined" 
                                            value={ values.dois }
                                            onChange={ handleChange }
                                            onKeyUp={ handleBlur }
                                        />
                                        { errors.dois && touched.dois ? (<div className="required-text">{errors.dois}</div>) : null }
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
                                    <BootstrapDialog
                                        onClose={ this.handle_ok_dialog_close }
                                        aria-labelledby="customized-dialog-title"
                                        open={ this.state.ok_dialog_open }
                                    >
                                        <BootstrapDialogTitle id="customized-dialog-title" onClose={ this.handle_ok_dialog_close }>
                                            Success
                                        </BootstrapDialogTitle>
                                        <DialogContent dividers>
                                            <Typography gutterBottom>
                                            Thank you for filling out the survey. After our staff reviews it for inclusion in the COVID Information Commons, you can view it <a href={ url + '/grants' } target="_blank">here.</a>
                                            If you have another award, please fill out the survey form again. 
                                            </Typography>
                                        </DialogContent>
                                        <DialogActions>
                                            <Button autoFocus onClick={ this.handle_ok_dialog_close }>
                                                OK
                                            </Button>
                                        </DialogActions>
                                    </BootstrapDialog>
                                    <Button variant="text" onClick={ () => {
                                        handleReset();
                                        this.handle_clear_form();
                                    }}>
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
