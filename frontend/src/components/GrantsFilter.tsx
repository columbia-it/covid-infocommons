import React, {Component} from "react";
import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import { Button, TextField } from "@material-ui/core";
import Autocomplete from '@mui/material/Autocomplete';
import {
    MuiPickersUtilsProvider,
    KeyboardDatePicker,
  } from '@material-ui/pickers';
import DateFnsUtils from '@date-io/date-fns';

interface OrgNameFacet {
    key: string
    doc_count: number
}

interface GrantsFilterProps {
    awardee_org_names: OrgNameFacet[]
    filterChangeHandler: (fieldName:string, value:any) => void
}

interface GrantFilterState {
    startDate: Date
    endDate: Date
    isStartDatePickerOpen: boolean
    isEndDatePickerOpen: boolean
}

const nsf_directorates = [
    'Biological Sciences',
    'Computer and Information Science and Engineering',
    'Education and Human Resources',
    'Engineering',
    'Geosciences',
    'Mathematical and Physical Sciences',
    'Social, Behavioral, and Economic Sciences',
    'Office of the Director'
]

const nih_institues = [
    'National Cancer Institute (NCI)',
    'National Eye Institute (NEI)',
    'National Heart, Lung, and Blood Institute (NHLBI)',
    'National Human Genome Research Institute (NHGRI)',
    'National Institute on Aging (NIA)',
    'National Institute on Alcohol Abuse and Alcoholism (NIAAA)',
    'National Institute of Allergy and Infectious Diseases (NIAID)',
    'National Institute of Arthritis and Musculoskeletal and Skin Diseases (NIAMS)',
    'National Institute of Biomedical Imaging and Bioengineering (NIBIB)',
    'Eunice Kennedy Shriver National Institute of Child Health and Human Development (NICHD)',
    'National Institute on Deafness and Other Communication Disorders (NIDCD)',
    'National Institute of Dental and Craniofacial Research (NIDCR)',
    'National Institute of Diabetes and Digestive and Kidney Diseases (NIDDK)',
    'National Institute on Drug Abuse (NIDA)',
    'National Institute of Environmental Health Sciences (NIEHS)',
    'National Institute of General Medical Sciences (NIGMS)',
    'National Institute of Mental Health (NIMH)',
    'National Institute on Minority Health and Health Disparities (NIMHD)',
    'National Institute of Neurological Disorders and Stroke (NINDS)',
    'National Institute of Nursing Research (NINR)',
    'National Library of Medicine (NLM)',
    'NIH Clinical Center (CC)',
    'Center for Information Technology (CIT)',
    'Center for Scientific Review (CSR)',
    'Fogarty International Center (FIC)',
    'National Center for Advancing Translational Sciences (NCATS)',
    'National Center for Complementary and Integrative Health (NCCIH)'
]
class GrantsFilter extends Component<GrantsFilterProps, GrantFilterState> {
    constructor(props:GrantsFilterProps) {
        super(props)
        this.state = {
            startDate: new Date(),
            endDate: new Date(),
            isStartDatePickerOpen: false,
            isEndDatePickerOpen: false
        }
        this.startDateChangeHandler = this.startDateChangeHandler.bind(this)
        this.endDateChangeHandler = this.endDateChangeHandler.bind(this)
    }

    startDateChangeHandler(date:Date) {
        this.setState({startDate:date})
        this.props.filterChangeHandler('startDate', date)
    }

    endDateChangeHandler(date:Date) {
        this.setState({endDate:date})
        this.props.filterChangeHandler('endDate', date)
    }

    nsfDirectorateChangeHandler(value:string) {
        this.props.filterChangeHandler('nsf_directorate', value)
    }

    setIsStartDatePickerOpen(val:boolean) {
        this.setState({isStartDatePickerOpen: val})
    }

    setIsEndDatePickerOpen(val:boolean) {
        this.setState({isEndDatePickerOpen: val})
    }

    render() {
        return (
        <Card sx={{ width: '100%' }}>
        <CardContent>
            <div className="filter-button-div">
                <label className="filter-results-label">Filter Results</label>
                <Button 
                    variant='contained'>Clear Filter
                </Button>
            </div>
            <div>
                <Accordion>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel1a-content"
                        id="panel1a-header"
                    >
                        <Typography sx={{ px: 2 }}>NSF Directorate</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        {/* <TextField variant='outlined' label='Type directorate title'>
                        </TextField> */}
                        <Autocomplete
                            freeSolo
                            id="free-solo-3-demo"
                            disableClearable
                            onChange={ (event, value) => this.nsfDirectorateChangeHandler(value) }
                            options={ nsf_directorates.map((option) => option) }
                            renderInput={(params) => (
                            <TextField        
                                {...params}
                                label="Select NSF Directorate"
                                InputProps={{
                                    ...params.InputProps,
                                    type: 'search',
                                    onChange: e => {
                                        this.nsfDirectorateChangeHandler(e.target.value)
                                    },
                                }}
                                variant='outlined'
                            />
                            )}
                        />
                    </AccordionDetails>
                </Accordion>
                <Accordion>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel1a-content"
                        id="panel1a-header"
                    >
                        <Typography sx={{ px: 2 }}>NIH Institute/Center</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        {/* <TextField variant='outlined' label='Type directorate title'>
                        </TextField> */}
                        <Autocomplete
                            freeSolo
                            id="free-solo-5-demo"
                            disableClearable
                            onChange={ (event, value) => this.nsfDirectorateChangeHandler(value) }
                            options={ nih_institues.map((option) => option) }
                            renderInput={(params) => (
                            <TextField        
                                {...params}
                                label="Select NIH Institute/Center"
                                InputProps={{
                                    ...params.InputProps,
                                    type: 'search',
                                }}
                                variant='outlined'
                            />
                            )}
                        />
                    </AccordionDetails>
                </Accordion>
                <Accordion>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel2a-content"
                        id="panel2a-header"
                    >
                        <Typography sx={{ px: 2 }}>Division</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <TextField variant='outlined' label='Type division title'>
                        </TextField>
                    </AccordionDetails>
                </Accordion>
                <Accordion>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel3a-content"
                        id="panel3a-header"
                    >
                        <Typography sx={{ px: 2 }}>Awardee Organization</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Autocomplete
                            freeSolo
                            id="free-solo-2-demo"
                            disableClearable
                            options={this.props.awardee_org_names.map((option) => option.key)}
                            renderInput={(params) => (
                            <TextField        
                                {...params}
                                label="Search input"
                                InputProps={{
                                    ...params.InputProps,
                                    type: 'search',
                                }}
                                variant='outlined'
                            />
                            )}
                        />
                    </AccordionDetails>
                </Accordion>
                <Accordion>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel4a-content"
                        id="panel4a-header"
                    >
                        <Typography sx={{ px: 2 }}>State/Territory</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Typography>
                            Textfield goes here
                        </Typography>
                    </AccordionDetails>
                </Accordion>
                <Accordion>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel5a-content"
                        id="panel5a-header"
                    >
                        <Typography sx={{ px: 2 }}>PI Name</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <TextField variant='outlined' label='Type PI name'>
                        </TextField>
                    </AccordionDetails>
                </Accordion>
                <Accordion>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel6a-content"
                        id="panel6a-header"
                    >
                        <Typography sx={{ px: 2 }}>Program Officer/Official</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <TextField variant='outlined' label='Type Keywords'>
                        </TextField>
                    </AccordionDetails>
                </Accordion>
                <Accordion>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel7a-content"
                        id="panel7a-header"
                    >
                        <Typography sx={{ px: 2 }}>Start/End Date</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <MuiPickersUtilsProvider utils={DateFnsUtils}>
                            <KeyboardDatePicker
                                disableToolbar={ true }
                                variant="inline"
                                format="MM/dd/yyyy"
                                margin="normal"
                                id="date-picker-inline"
                                label="Start Date (On or after):"
                                value={ this.state.startDate }
                                inputVariant="outlined"
                                onChange={ this.startDateChangeHandler }
                                KeyboardButtonProps={{
                                    onFocus: (e) => {
                                        this.setIsStartDatePickerOpen(true);
                                    },
                                    'aria-label': 'change date',
                                }}
                                PopoverProps={{
                                    disableRestoreFocus: true,
                                    onClose: () => {
                                        this.setIsStartDatePickerOpen(false);
                                    }
                                }}
                                open={ this.state.isStartDatePickerOpen }
                            />
                            <KeyboardDatePicker
                                disableToolbar={true}
                                variant="inline"
                                format="MM/dd/yyyy"
                                margin="normal"
                                id="date-picker-inline"
                                label="End Date (On or before):"
                                value={ this.state.endDate }
                                inputVariant="outlined"
                                onChange={ this.endDateChangeHandler }
                                KeyboardButtonProps={{
                                    onFocus: (e) => {
                                        this.setIsEndDatePickerOpen(true);
                                    },
                                    'aria-label': 'change date',
                                }}
                                PopoverProps={{
                                    disableRestoreFocus: true,
                                    onClose: () => {
                                        this.setIsEndDatePickerOpen(false);
                                    }
                                }}
                                open={ this.state.isEndDatePickerOpen }
                            />
                        </MuiPickersUtilsProvider>
                    </AccordionDetails>
                </Accordion>
            </div>
        </CardContent>
    </Card>);
    };
}

export {GrantsFilter, OrgNameFacet};


