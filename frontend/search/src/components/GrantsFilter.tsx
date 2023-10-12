import {Component} from "react";
import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import { Button, TextField } from "@material-ui/core";
import MenuItem from '@mui/material/MenuItem';
import Autocomplete from '@mui/material/Autocomplete';
import {
    MuiPickersUtilsProvider,
    KeyboardDatePicker,
  } from '@material-ui/pickers';
import DateFnsUtils from '@date-io/date-fns';
import regionData from '../data/regions_data.json';

interface Facet {
    key: string
    doc_count: number
}

interface GrantsFilterProps {
    awardee_org_names: Facet[]
    funder_divisions: Facet[]
    pi_names: Facet[]
    program_official_names: Facet[]
    funder_names: Facet[]
    filterChangeHandler: (fieldName?:string, value?:any, reset?:boolean) => void
}

interface GrantFilterState {
    startDate?: Date | null
    endDate?: Date | null
    isStartDatePickerOpen: boolean
    isEndDatePickerOpen: boolean
    nsf_directorate?: string | null
    nih_institute?: string | null
    division?: string | null
    awardee_org?: string | null
    region?: string | null
    pi_name?: string | null
    po_name?: string | null
    clearSelectedValue: boolean
    funder_name?: string | null
}

const nsf_directorates = [
    'Biological Sciences (BIO)',
    'Computer and Information Science and Engineering (CISE)',
    'Education and Human Resources (EHR)',
    'Engineering (ENG)',
    'Environmental Research and Education (ERE)',
    'Geosciences (GEO)',
    'Mathematical and Physical Sciences (MPS)',
    'Social, Behavioral, and Economic Sciences (SBE)',
    'STEM Education (EDU)',
    'Technology, Innovation and Partnerships (TIP)',
    'Office of the Director'
]

const nih_institues = [
    'National Cancer Institute (NCI)',
    'National Eye Institute (NEI)',
    'National Heart Lung and Blood Institute (NHLBI)',
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
    'National Center for Complementary and Integrative Health (NCCIH)',
    'National Center for Emerging and Zoonotic Infectious Diseases (NCEZID)',
    'National Institute for Occupational Safety and Health (NIOSH)',
    'National Center for Immunization and Respiratory Diseases (NCIRD)',
    'National Center for Injury Prevention and Control (NCIPC)',
    'NIH Office of the Director'
]

class GrantsFilter extends Component<GrantsFilterProps, GrantFilterState> {
    constructor(props:GrantsFilterProps) {
        super(props)
        this.state = {
            startDate: null,
            endDate: null,
            isStartDatePickerOpen: false,
            isEndDatePickerOpen: false,
            funder_name: null,
            nsf_directorate: null,
            nih_institute: null,
            division: null,
            awardee_org: null,
            region: null,
            pi_name: null,
            po_name: null,
            clearSelectedValue: false
        }
        this.startDateChangeHandler = this.startDateChangeHandler.bind(this)
        this.endDateChangeHandler = this.endDateChangeHandler.bind(this)
        this.clearFilter = this.clearFilter.bind(this)
    }

    startDateChangeHandler(date:Date) {
        this.setState({startDate:date})
        this.props.filterChangeHandler('startDate', date)
    }

    endDateChangeHandler(date:Date) {
        this.setState({endDate:date})
        this.props.filterChangeHandler('endDate', date)
    }

    setIsStartDatePickerOpen(val:boolean) {
        this.setState({isStartDatePickerOpen: val})
    }

    setIsEndDatePickerOpen(val:boolean) {
        this.setState({isEndDatePickerOpen: val})
    }

    clearFilter() {
        this.setState( {funder_name: ''} )
        this.setState( {nsf_directorate: ''} );
        this.setState( {nih_institute: ''} );
        this.setState( {division: ''} );
        this.setState( {awardee_org: ''} )
        this.setState( {region: ''} )
        this.setState( {pi_name: ''} )
        this.setState( {po_name: ''} )
        this.setState( {startDate: null} )
        this.setState( {endDate: null} )
        this.props.filterChangeHandler('', '', true)
    }
    render() {
        return (
        <Card sx={{ width: '100%' }}>
        <CardContent>
            <div className="filter-button-div">
                <label className="filter-results-label">Filter Results</label>
                <Button 
                    variant='contained'
                    onClick={ this.clearFilter }>Clear Filter
                </Button>
            </div>
            <div>
            <Accordion>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel3a-content"
                        id="panel3a-header"
                    >
                        <Typography sx={{ px: 2 }}>Funder</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Autocomplete
                            id="funder_selector"
                            value={ this.state.funder_name }
                            options={ this.props.funder_names.map((option) => option.key) }
                            onInputChange={(event, value) => {
                                this.setState({funder_name: value})
                                this.props.filterChangeHandler('funder_name', value, false)
                            }}
                            onChange={ (event, value) => {
                                this.setState({funder_name: value})
                                this.props.filterChangeHandler('funder_name', value, false)
                            }}
                            clearOnBlur={ false }
                            renderInput={(params) => 
                                <TextField {...params} 
                                    placeholder="Select Funder"
                                    variant="outlined" />
                            }
                        />
                    </AccordionDetails>
                </Accordion>
                <Accordion>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel1a-content"
                        id="panel1a-header">
                        <Typography sx={{ px: 2 }}>NSF Directorate</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Autocomplete
                            id="nsf_division_selector"
                            value={ this.state.nsf_directorate }
                            options={ nsf_directorates.map((option) => option) }
                            onInputChange={(event, value) => {
                                this.setState({nsf_directorate: value})
                                this.props.filterChangeHandler('nsf_division', value, false)
                            }}
                            onChange={ (event, value) => {
                                this.setState({nsf_directorate: value})
                                this.props.filterChangeHandler('nsf_division', value, false)
                            }}
                            clearOnBlur={ false }
                            renderInput={(params) => 
                                <TextField {...params} 
                                    placeholder="Select NSF Directorate"
                                    variant="outlined" />
                            }
                        />
                    </AccordionDetails>
                </Accordion>
                <Accordion>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel1a-content"
                        id="panel1a-header">
                        <Typography sx={{ px: 2 }}>NIH Institute/Center</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Autocomplete
                            id="nih_division_selector"
                            value={ this.state.nih_institute }
                            options={ nih_institues.map((option) => option) }
                            onInputChange={(event, value) => {
                                this.setState({nih_institute: value})
                                this.props.filterChangeHandler('nih_division', value, false)
                            }}
                            onChange={ (event, value) => {
                                this.setState({nih_institute: value})
                                this.props.filterChangeHandler('nih_division', value, false)
                            }}
                            clearOnBlur={ false }
                            renderInput={(params) => 
                                <TextField {...params} 
                                    placeholder="Select NIH Institute/Center"
                                    variant="outlined" />
                            }
                        />
                    </AccordionDetails>
                </Accordion>
                {/* <Accordion>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel2a-content"
                        id="panel2a-header"
                    >
                        <Typography sx={{ px: 2 }}>Division</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Autocomplete
                            id="division_selector"
                            value={ this.state.division }
                            options={ this.props.funder_divisions.map((option) => option.key) }
                            onInputChange={(event, value) => {
                                this.setState({division: value})
                                this.props.filterChangeHandler('funder_division', value, false)
                            }}
                            onChange={ (event, value) => {
                                this.setState({division: value})
                                this.props.filterChangeHandler('funder_division', value, false)
                            }}
                            clearOnBlur={ false }
                            renderInput={(params) => 
                                <TextField {...params} 
                                    placeholder="Type Keyword"
                                    variant="outlined" />
                            }
                        />
                    </AccordionDetails>
                </Accordion> */}
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
                            id="org_selector"
                            value={ this.state.awardee_org }
                            options={ this.props.awardee_org_names.map((option) => option.key) }
                            onInputChange={(event, value) => {
                                this.setState({awardee_org: value})
                                this.props.filterChangeHandler('awardee_organization', value, false)
                            }}
                            onChange={ (event, value) => {
                                this.setState({awardee_org: value})
                                this.props.filterChangeHandler('awardee_organization', value, false)
                            }}
                            clearOnBlur={ false }
                            renderInput={(params) => 
                                <TextField {...params} 
                                    placeholder="Type Institution Name"
                                    variant="outlined" />
                            }
                        />
                    </AccordionDetails>
                </Accordion>
                <Accordion>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel4a-content"
                        id="panel4a-header">
                        <Typography sx={{ px: 2 }}>State/Territory</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Autocomplete
                            id="state_selector"
                            value={ this.state.region }
                            options={ regionData.map((option) => option.shortCode) }
                            onInputChange={(event, value) => {
                                this.setState({region: value})
                                this.props.filterChangeHandler('org_state', value, false)
                            }}
                            onChange={ (event, value) => {
                                this.setState({region: value})
                                this.props.filterChangeHandler('org_state', value, false)
                            }}
                            clearOnBlur={ false }
                            renderInput={(params) => 
                                <TextField {...params} 
                                    placeholder="Select State/Territory"
                                    variant="outlined" />
                            }
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
                            id="pi_name_selector"
                            value={ this.state.pi_name }
                            options={ this.props.pi_names.map((option) => option.key) }
                            onInputChange={(event, value) => {
                                this.setState({pi_name: value})
                                this.props.filterChangeHandler('pi_name', value, false)
                            }}
                            onChange={ (event, value) => {
                                this.setState({pi_name: value})
                                this.props.filterChangeHandler('pi_name', value, false)
                            }}
                            clearOnBlur={ false }
                            renderInput={(params) => 
                                <TextField {...params} 
                                    placeholder="Type PI Name"
                                    variant="outlined" />
                            }
                        />
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
                        <Autocomplete
                            id="po_name_selector"
                            value={ this.state.po_name }
                            options={ this.props.program_official_names.map((option) => option.key) }
                            onInputChange={(event, value) => {
                                this.setState({po_name: value})
                                this.props.filterChangeHandler('po_name', value, false)
                            }}
                            onChange={ (event, value) => {
                                this.setState({po_name: value})
                                this.props.filterChangeHandler('po_name', value, false)
                            }}
                            clearOnBlur={ false }
                            renderInput={(params) => 
                                <TextField {...params} 
                                    placeholder="Type Program Officer/Official name"
                                    variant="outlined" />
                            }
                        />
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
                                id="start-date-picker"
                                placeholder="Start Date (On or after):"
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
                                id="end-date-picker"
                                placeholder="End Date (On or before):"
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

export {GrantsFilter, Facet};


