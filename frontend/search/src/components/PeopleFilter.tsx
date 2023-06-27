import { Component } from "react";
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

interface PeopleFilterProps {
    institution_names: Facet[]
    filterChangeHandler: (fieldName?:string, value?:any, reset?:boolean) => void
}

interface PeopleFilterState {
    org_name?: string | null
    org_state?: string | null    
    clearSelectedValue: boolean
}

class PeopleFilter extends Component<PeopleFilterProps, PeopleFilterState> {
    constructor(props:PeopleFilterProps) {
        super(props)
        this.state = {
            org_name: null,
            org_state: null,
            clearSelectedValue: false
        }
        this.clearFilter = this.clearFilter.bind(this)
    }

    clearFilter() {
        this.setState( {org_name: ''} )
        this.setState( {org_state: ''} )
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
                        <Typography sx={{ px: 2 }}>Institution</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Autocomplete
                            id="org_selector"
                            value={ this.state.org_name }
                            options={ this.props.institution_names.map((option) => option.key) }
                            onInputChange={(event, value) => {
                                this.setState({org_name: value})
                                this.props.filterChangeHandler('org_name', value, false)
                            }}
                            onChange={ (event, value) => {
                                this.setState({org_name: value})
                                this.props.filterChangeHandler('org_name', value, false)
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
                            value={ this.state.org_state }
                            options={ regionData.map((option) => option.shortCode) }
                            onInputChange={(event, value) => {
                                this.setState({org_state: value})
                                this.props.filterChangeHandler('org_state', value, false)
                            }}
                            onChange={ (event, value) => {
                                this.setState({org_state: value})
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
            </div>
        </CardContent>
    </Card>);
    };
}

export {PeopleFilter, Facet};


