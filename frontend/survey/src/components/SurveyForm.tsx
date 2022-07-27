import React, { Component } from "react";
import { Formik, Form, FormikProps, Field } from 'formik'
import Box from '@mui/material/Box';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import Stack from '@mui/material/Stack';
import axios from "axios";

import {
    Typography,
    Paper,
    Link,
    Grid,
    Button,
    CssBaseline,
    MenuItem,
    TextField
  } from '@material-ui/core';
import { Label } from "@material-ui/icons";

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
    first_name_error_msg?: string | null
    first_name_error: boolean | false
    last_name_error_msg?: string | null
    last_name_error: boolean | false
    award_id_error_msg?: string | null
    award_id_error: boolean | false
}

interface SurveyForm {
    first_name: string
    last_name: string
    orcid: string
    emails: string
}

let url = ''
if (process.env.NODE_ENV == 'production') {
    url = "https://cic-apps.datascience.columbia.edu";
} else if (process.env.NODE_ENV == 'development') {
    url = "https://cice-dev.paas.cc.columbia.edu";
} else {
    url = "http://127.0.0.1:8000"
}

class SurveyForm extends Component <any, FormState> {    
    constructor(props:any) {
        super(props)
        this.state = {
            first_name_error_msg: null,
            first_name_error: false,
            last_name_error_msg: null,
            last_name_error: false,
            award_id_error_msg: null,
            award_id_error: false
        }
        this.firstNameChangeHandler = this.firstNameChangeHandler.bind(this)
        this.lastNameChangeHandler = this.lastNameChangeHandler.bind(this)
        this.awardIdChangeHandler = this.awardIdChangeHandler.bind(this)
    }

    firstNameChangeHandler(event: React.ChangeEvent<HTMLInputElement>) {
        console.log(event.target.value)
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

    handleSubmit(values:any) {
        var payload = {
            "data": {
                "type": "Person",
                "attributes": values
            }
        }
        console.log(values)
        console.log('...1...')
        console.log(process.env.OAUTH_TOKEN)

        var headers = {
            'Content-Type': 'application/vnd.api+json',
            'Authorization': 'Bearer ' + process.env.OAUTH_TOKEN
        }
        console.log(headers)

        axios.post(url.concat("/v1/people"), payload, {
            headers: headers
          })
          .then((response) => {
            console.log("Person added successfully!!")
            console.log(response)
          })
          .catch((error) => {
            console.log("Error!!")

            console.log(error)
          })
    }

    render() {
        return (
            <div className="form_div">
                <br/>
                <Paper style={{ padding: 16 }}>

                <Typography variant="h4" align="center" component="h1" gutterBottom>
                    COVID Information Commons PI Survey
                </Typography>
                <Typography paragraph>
                    Congratulations on your COVID-19 related research award!         
                </Typography>
                <Typography>
                    ⭐ Please fill out this form multiple times for each NSF or NIH individual award you have received ⭐
                </Typography>
                <br/>
                <Typography>
                    The COVID Information Commons (CIC) website, funded by the National Science Foundation (NSF #2028999 and 2139391) compiles information about COVID-19 related awards and research output from U.S. NSF, NIH and HHS grants. A key objective of this website is to enrich the standard public award information available regarding your research, and enhance opportunities for collaboration. 
                </Typography>
                <br/>
                <Typography>
                    As a COVID-19 research awardee, we invite you to provide voluntary contributions of additional, applicable public information about your project, beyond the award abstract, which you would like to make openly available via the COVID Information Commons website (https://covidinfocommons.net) in our PI Database.
                </Typography>
                <br/>
                <Typography>
                    You can always make changes to the information you provided by filling out the form again. Please email any questions to info@covidinfocommons.net. Thank you!
                </Typography>
                </Paper>
                <br/>
                <br/>
                <Formik
                    initialValues={{
                        first_name: '',
                        last_name: '',
                        orcid: '',
                        emails: ''
                    }}
                    onSubmit={((values, { setSubmitting })=>{
                        console.log(values)
                        
                        this.handleSubmit(values)
                    })}
                >
                    {({ handleSubmit, values, handleChange }) => {
                        return (
                        <form onSubmit={handleSubmit}>
                        <div>
                            <Paper className="name-container">
                                <div className="name-child">
                                <FormControl>
                                    <FormLabel id="demo-radio-buttons-group-label-3">
                                        Your first name <span className="required-text">*</span>
                                    </FormLabel>
                                    <TextField 
                                        id="first_name" 
                                        variant="standard" 
                                        required 
                                        value={ values.first_name }
                                        onChange={ handleChange }
                                        error={ this.state.award_id_error }
                                        helperText={ this.state.award_id_error_msg }
                                    />
                                    <br/>
                                    <br/>
                                </FormControl>
                                </div>
                                <div className="name-child">
                                <FormControl>
                                    <FormLabel id="demo-radio-buttons-group-label-2">
                                        Your last name <span className="required-text">*</span>
                                    </FormLabel>
                                    <TextField 
                                        id="last_name" 
                                        variant="standard" 
                                        required 
                                        value={ values.last_name }
                                        onChange={ handleChange }
                                        error={ this.state.award_id_error }
                                        helperText={ this.state.award_id_error_msg }
                                    />
                                <br/>
                                <br/>
                                </FormControl>
                                </div>
                                <div className="name-child">
                                </div>
                            </Paper>    
                            <br/> 
                            <Paper style={{ padding: 16 }}>
                            <FormControl className="name-input">
                                <FormLabel id="demo-radio-buttons-group-label-3">
                                    Other institutional email address(es) in addition to email address provided above (optional)
                                </FormLabel>
                                <TextField 
                                    id="emails" 
                                    //label="COVID-19 Research Award Number" 
                                    variant="standard" 
                                    required 
                                    value={ values.emails }
                                    //className="name-input"
                                    onChange={ handleChange }
                                />
                            </FormControl>
                                <br/>
                                <br/>
                            </Paper> 
                            <Paper style={{ padding: 16 }}>
                            <FormControl className="name-input">
                                <FormLabel id="demo-radio-buttons-group-label-3">
                                    Your ORCID iD (type NA if you do not have an ORCID) * <span className="required-text">*</span>
                                </FormLabel>
                                <TextField 
                                    id="orcid" 
                                    //label="COVID-19 Research Award Number" 
                                    variant="standard" 
                                    required 
                                    value={ values.orcid }
                                    //className="name-input"
                                    onChange={ handleChange }
                                    error={ this.state.award_id_error }
                                    helperText={ this.state.award_id_error_msg }
                                />
                            </FormControl>
                                <br/>
                                <br/>
                            </Paper> 
                            <br/>
                            <Paper style={{ padding: 16 }}>
                            <FormControl className="name-input">
                                <FormLabel id="demo-radio-buttons-group-label">
                                    COVID-19 Research Award Number <span className="required-text">*</span>
                                </FormLabel>
                                <TextField 
                                    id="award_id" 
                                    //label="COVID-19 Research Award Number" 
                                    variant="standard" 
                                    required 
                                    //className="name-input"
                                    onChange={ this.awardIdChangeHandler }
                                    error={ this.state.award_id_error }
                                    helperText={ this.state.award_id_error_msg }
                                />
                            </FormControl>
                                <br/>
                                <br/>
                            </Paper>
                            <br/>
                            <Paper style={{ padding: 16 }}>
                            <FormControl>
                                <FormLabel id="demo-radio-buttons-group-label">COVID-19 Funding Agency <span className="required-text">*</span></FormLabel>
                                <RadioGroup
                                    aria-labelledby="demo-radio-buttons-group-label"
                                    defaultValue="female"
                                    name="funder-group"
                                >
                                    <FormControlLabel 
                                        value="NSF" 
                                        control={<Radio />} 
                                        label="NSF" />
                                    <FormControlLabel 
                                        value="NIH" 
                                        control={<Radio />} 
                                        label="NIH" />
                                </RadioGroup>
                            </FormControl>
                            </Paper>
                            <br/>
                            <br/>
                            <Stack spacing={20} direction="row">
                                <Button variant="contained" 
                                    //className="form-submit-btn"
                                    style={{
                                        backgroundColor: "#2C6BAC",
                                        color: "#FFFFFF"
                                    }}
                                    type='submit'
                                >
                                    Submit
                                </Button>
                                <Button variant="text">Clear form</Button>
                            </Stack>
                            <br/>
                            <br/>
                        </div>
                        </form>
                    )}}
                </Formik>
            </div>
        );
    }   
}

export default SurveyForm;
