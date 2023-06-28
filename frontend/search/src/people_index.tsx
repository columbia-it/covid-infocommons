import { Component } from "react";
import Button from '@mui/material/Button';
import DownloadIcon from '@mui/icons-material/Download';
import SearchBar from './components/SearchBar';
import PeopleTable from "./components/PeopleTable";
import axios from "axios";
import ModelSelect from "./components/ModelSelect";
import { PeopleFilter, Facet } from "./components/PeopleFilter";
import {SearchContext} from './search_context';

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

interface Person {
    id: number
    first_name: string
    last_name: string
    full_name: string
    institutions: string[]
}

interface PeopleState {
    totalCount: number
    search_in_progress: boolean
    data: Person[]
    pageIndex: number
    keyword: string
    url: string
    filter: Filter
    institution_names: Facet[]
}

interface Filter {
    org_name?: string
    org_state?: string
}

interface PeopleTableProps {
    keyword: string
    data: Person[]
    totalCount: number
}

let url = ''
if (process.env.NODE_ENV == 'production') {
    url = "https://cic-apps.datascience.columbia.edu";
} else if (process.env.NODE_ENV == 'development') {
    url = "https://cice-dev.paas.cc.columbia.edu";
} else {
    url = "http://127.0.0.1:8000"
}

class People extends Component<PeopleTableProps, PeopleState> {
    static context = SearchContext;

    state:PeopleState = {
        totalCount: this.props.totalCount,
        search_in_progress: false,
        data: this.props.data,
        pageIndex: 0,
        keyword: this.props.keyword,
        url: url,
        filter: {},
        institution_names: []
    }

    constructor(props:any) {
        super(props)
        this.pageChangeHandler = this.pageChangeHandler.bind(this)
        this.filterChangeHandler = this.filterChangeHandler.bind(this)
    }

    componentDidMount = () => {
        this.get_people_data()
    }

    componentDidUpdate = (prevProps:PeopleTableProps) => {
        if(this.props.keyword != prevProps.keyword) // Check if it's a new user, you can also use some unique property, like the ID  (this.props.user.id !== prevProps.user.id)
        {
            this.setState({
                keyword: this.props.keyword
            })
        }
        if(this.props.totalCount != prevProps.totalCount) // Check if it's a new user, you can also use some unique property, like the ID  (this.props.user.id !== prevProps.user.id)
        {
          this.setState({
              totalCount: this.props.totalCount,
              data: this.props.data,
              keyword: this.props.keyword
          })
        }
        if(this.props.data != prevProps.data) // Check if it's a new user, you can also use some unique property, like the ID  (this.props.user.id !== prevProps.user.id)
        {
          this.setState({
              totalCount: this.props.totalCount,
              data: this.props.data,
              keyword: this.props.keyword
          })
        }

    }

    get_institution_facet() {
        var url = this.state.url.concat('/search/facets?field=awardee_organization.name')
        axios.get(url).then(results => {
            this.setState({ institution_names: results.data.aggregations.patterns.buckets })
        })
    }

    get_people_data = (kw?:string) => {
        kw = this.props.keyword;
        this.setState({
            search_in_progress: true
        })
        var url = this.state.url.concat('/search/people')
        var params: { [key: string]: any } = {};

        let from:number = 0

        if (this.state.pageIndex > 0) {
            from = (this.state.pageIndex * 20) + 1
        } 
        params.from = from
        if (!kw) {
            kw = (document.getElementById('outlined-search') as HTMLInputElement).value;
        }
        if (kw && kw.length > 0) {
            params.keyword = kw
        }

        let property: keyof typeof this.state.filter
        for (property in this.state.filter) {
            if (this.state.filter[property]) {
                params[property] = this.state.filter[property]
            }
        }
        axios.get(url, {params: params}).then(results => {
            this.setState({
                search_in_progress: false
            })
            this.setState({ totalCount: results.data.hits.total.value })
            var newArray = results.data.hits.hits.map(function(val:any) {
                return {
                    id: val['_source']['id'],
                    name: val['_source']['full_name'],
                    emails: val['_source']['emails'],
                    private_emails: val['_source']['private_emails'],
                    affiliations: val['_source']['affiliations']
                }
            })
            this.setState({ data: newArray })
            this.get_institution_facet()
        })
    }
    
    pageChangeHandler(page:number, pageSize: number) {
        this.setState({
            pageIndex: page
        })
        this.get_people_data()
    }

    exportToCsv = (event:any) => {
        event.preventDefault()
    }

    filterChangeHandler(fieldName?:string, value?:any, reset?:boolean) {
        if (reset) {
            this.state.filter = {}
            this.get_people_data()
            return
        }
        var currentFilter = this.state.filter
        if (fieldName == 'org_name') {
            if (!value || value.length === 0) {
                delete currentFilter.org_name;
            } else {
                currentFilter['org_name'] = value
            }
        }
        
        if (fieldName == 'org_state') {
            if (!value || value.length === 0) {
                delete currentFilter.org_state;
            } else {
                currentFilter['org_state'] = value
            }
        }
        this.setState({filter: currentFilter})
        this.get_people_data()
    }

    render() {
        return (
            <div>
                <br/>
                <div className='flex-container'>
                    {
                        this.state.search_in_progress == false ? 
                        <div className='results-row flex-child'>
                                Showing <span style={{fontWeight: 'bold', color: '#000000'}}>{ this.state.totalCount }</span> results.
                        </div> 
                        : <div className='results-row flex-child'>Waiting for results...
                        </div> 
                    } 
                    <div className="flex-child">                            
                            <Button sx={styles}
	                            onClick={ this.exportToCsv } 
                                className='download-button' 
                                variant="contained"
                                endIcon={ <DownloadIcon /> }>Download Results as CSV (up to 1,000 people)</Button>
                    </div>
                    <div className="flex-child">
                        <ModelSelect
                        selected_model={ 2 }
                    /></div>
                </div>
                <br/>
                <div>  
                    <div className='flex-container'>
                        <div className='flex-child'>
                        <PeopleTable
                            totalCount={ this.state.totalCount } 
                            data={ this.state.data} 
                            url={ this.state.url }
                            pageChangeHandler={ this.pageChangeHandler }
                            pageIndex={ this.state.pageIndex }
                            keyword={ this.state.keyword }
                            paging={ true }
                        >
                        </PeopleTable>
                    </div>
                    <div className='flex-child'>
                        <div>
                            <PeopleFilter
                                institution_names={ this.state.institution_names }
                                filterChangeHandler={ this.filterChangeHandler }
                            />
                        </div>
                    </div>
                </div>
                </div>
            </div>
        )
    }
}

export default People;