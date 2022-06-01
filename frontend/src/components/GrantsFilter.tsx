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
import { CountryDropdown, RegionDropdown, CountryRegionData } from 'react-country-region-selector';
import regionData from '../data/region_data.json';

interface OrgNameFacet {
    key: string
    doc_count: number
}

interface GrantsFilterProps {
    awardee_org_names: OrgNameFacet[]
    pi_names: OrgNameFacet[]
    start_date: Date
    nsfDirectorateChangeHandler: (val:string) => void 
    filterChangeHandler: (fieldName:string, value:any) => void
}
const handleDateChange = (date:any) => {
    console.log('');
};

const selectRegion = (val:string) => {
    console.log('');
}

let region = ''

interface GrantFilterState {
    startDate: Date
    endDate: Date
    isStartDatePickerOpen: boolean
    isEndDatePickerOpen: boolean
}

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

    setRegion(val: string) {
        console.log('Selected region = ')
        console.log(val)
    }

    nsf_directorates = [
        'Biological Sciences',
        'Computer and Information Science and Engineering',
        'Education and Human Resources',
        'Engineering',
        'Geosciences',
        'Mathematical and Physical Sciences',
        'Social, Behavioral, and Economic Sciences',
        'Office of the Director'
    ]

    startDateChangeHandler(date:any) {
        const updatedDate = new Date('yyyy-MM-dd')
        date.setHours(updatedDate.getHours())
        date.setMinutes(updatedDate.getMinutes())
        date.setSeconds(updatedDate.getSeconds())
        this.setState({startDate:date})
        this.props.filterChangeHandler('startDate', date)
    }

    endDateChangeHandler(date:any) {
        const updatedDate = new Date()
        date.setHours(updatedDate.getHours())
        date.setMinutes(updatedDate.getMinutes())
        date.setSeconds(updatedDate.getSeconds())
        this.setState({endDate:date})
        this.props.filterChangeHandler('endDate', date)
    }

    nsfDirectorateChangeHandler(event:any) {
        console.log(event)
        //this.props.nsfDirectorateChangeHandler()
    }

    setIsStartDatePickerOpen(val:boolean) {
        this.setState({isStartDatePickerOpen: val})
    }

    setIsEndDatePickerOpen(val:boolean) {
        this.setState({isEndDatePickerOpen: val})
    }

    nih_institues = [
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
        'National Institute of Neurological Disorders and Stroke (NINDS)'
    ]

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
                        <Typography sx={{ px: 2 }}> NSF Directorate</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        {/* <TextField variant='outlined' label='Type directorate title'>
                        </TextField> */}
                        <Autocomplete
                            freeSolo
                            id="free-solo-3-demo"
                            disableClearable
                            options={this.nsf_directorates.map((option) => option)}
                            renderInput={(params) => (
                            <TextField        
                                {...params}
                                label="Select NSF Directorate Title"
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
                        aria-controls="panel1a-content"
                        id="panel1a-header"
                    >
                        <Typography sx={{ px: 2 }}> NIH Institute/Center</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        {/* <TextField variant='outlined' label='Type directorate title'>
                        </TextField> */}
                        <Autocomplete
                            freeSolo
                            id="free-solo-4-demo"
                            disableClearable
                            options={this.nih_institues.map((option) => option)}
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
                        {/* <TextField variant='outlined' label='Type PI name'>
                        </TextField> */}
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
                    <Autocomplete
                            freeSolo
                            id="free-solo-4-demo"
                            disableClearable
                            options={regionData.map((option) => option.name)}
                            renderInput={(params) => (
                            <TextField        
                                {...params}
                                label="Select State/Territory"
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
                        aria-controls="panel5a-content"
                        id="panel5a-header"
                    >
                        <Typography sx={{ px: 2 }}>PI Name</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                    <Autocomplete
                            freeSolo
                            id="free-solo-2-demo"
                            disableClearable
                            options={this.props.pi_names.map((option) => option.key)}
                            renderInput={(params) => (
                            <TextField        
                                {...params}
                                label="Type PI Name"
                                InputProps={{
                                    ...params.InputProps,
                                    type: 'search',
                                }}
                                variant='outlined'
                            />
                            )}
                        />
                        {/* <TextField variant='outlined' label='Type PI name'>
                        </TextField> */}
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
                            disableToolbar={true}
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

export { GrantsFilter, OrgNameFacet };


