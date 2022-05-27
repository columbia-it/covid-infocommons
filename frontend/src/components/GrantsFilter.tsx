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


interface GrantsFilterProps {
    awardee_org_names: string[]
    pi_names: string[]
    start_date: Date
}
const handleDateChange = (date:any) => {
    console.log('');
};

const selectRegion = (val:string) => {
    console.log('');
}

let region = ''

class GrantsFilter extends Component<GrantsFilterProps, any> {
    
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
                        <Typography sx={{ px: 2 }}>Directorate</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <TextField variant='outlined' label='Type directorate title'>
                        </TextField>
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
                            options={this.props.awardee_org_names.map((option) => option)}
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
                    <RegionDropdown
                        country={'US'}
                        value={region}
                        onChange={(val) => selectRegion(val)} />
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
                            options={this.props.pi_names.map((option) => option)}
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
                            disableToolbar
                            variant="inline"
                            format="MM/dd/yyyy"
                            margin="normal"
                            id="date-picker-inline"
                            label="Start Date (On or after):"
                            value={ this.props.start_date }
                            onChange={ handleDateChange }
                            KeyboardButtonProps={{
                                'aria-label': 'change date',
                            }}
                        />
                        <KeyboardDatePicker
                            disableToolbar
                            variant="inline"
                            format="MM/dd/yyyy"
                            margin="normal"
                            id="end-date-picker-inline"
                            label="End Date (On or after):"
                            value={ this.props.start_date }
                            onChange={ handleDateChange }
                            KeyboardButtonProps={{
                                'aria-label': 'change date',
                            }}
                        />
                        </MuiPickersUtilsProvider>
                    </AccordionDetails>
                </Accordion>
            </div>
        </CardContent>
    </Card>);
    };
}

export { GrantsFilter };


