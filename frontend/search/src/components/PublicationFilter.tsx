import {Component} from "react";
import Card from '@mui/material/Card';
import { Button, TextField } from "@material-ui/core";
import CardContent from '@mui/material/CardContent';
import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Autocomplete from '@mui/material/Autocomplete';

interface Facet {
    key: string
    doc_count: number
}

interface PublicationFilterProps {
    author_names: Facet[]
    filterChangeHandler: (fieldName?:string, value?:any, reset?:boolean) => void
}

interface PublicationFilterState {
    author_name?: string | null
    clearSelectedValue: boolean
}

class PublicationFilter extends Component<PublicationFilterProps, PublicationFilterState> {
    constructor(props:PublicationFilterProps) {
        super(props)
        this.state = {
            author_name: null,
            clearSelectedValue: false
        }
        this.clearFilter = this.clearFilter.bind(this)
    }

    clearFilter() {
        this.setState( {author_name: ''} )
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
                            onClick={ this.clearFilter }>
                                Clear Filter
                        </Button>
                    </div>
                    <div>
                        <Accordion>
                            <AccordionSummary
                                expandIcon={<ExpandMoreIcon />}
                                aria-controls="panel3a-content"
                                id="panel3a-header"
                            >
                                <Typography sx={{ px: 2 }}>Author</Typography>
                            </AccordionSummary>
                            <AccordionDetails>
                                <Autocomplete
                                    id="publication_author_selector"
                                    value={ this.state.author_name }
                                    options={ this.props.author_names.map((option) => option.key) }
                                    onInputChange={(event, value) => {
                                        this.setState({author_name: value})
                                        this.props.filterChangeHandler('author_name', value, false)
                                    }}
                                    onChange={ (event, value) => {
                                        this.setState({author_name: value})
                                        this.props.filterChangeHandler('author_name', value, false)
                                    }}
                                    clearOnBlur={ false }
                                    renderInput={(params) => 
                                    <TextField {...params} 
                                        placeholder="Type Author Name"
                                        variant="outlined" />
                                    }
                                />
                            </AccordionDetails>
                        </Accordion>
                    </div>
                </CardContent>
            </Card>

        )
    }
}

export { PublicationFilter, Facet };
