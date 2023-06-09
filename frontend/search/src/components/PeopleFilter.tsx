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

interface PeopleFilterProps {
    institution_names: Facet[]
    filterChangeHandler: (fieldName?:string, value?:any, reset?:boolean) => void
}

interface PeopleFilterState {
    institution_name?: string | null
    region?: string | null    
    clearSelectedValue: boolean
}

class PeopleFilter extends Component<PeopleFilterProps, PeopleFilterState> {
    constructor(props:PeopleFilterProps) {
        super(props)
        this.state = {
            institution_name: null,
            region: null,
            clearSelectedValue: false
        }
        this.clearFilter = this.clearFilter.bind(this)
    }

    clearFilter() {
        this.setState( {institution_name: ''} )
        this.setState( {region: ''} )
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
                            value={ this.state.institution_name }
                            options={ this.props.institution_names.map((option) => option.key) }
                            onInputChange={(event, value) => {
                                this.setState({institution_name: value})
                                this.props.filterChangeHandler('awardee_organization', value, false)
                            }}
                            onChange={ (event, value) => {
                                this.setState({institution_name: value})
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
            </div>
        </CardContent>
    </Card>);
    };
}

export {PeopleFilter, Facet};


