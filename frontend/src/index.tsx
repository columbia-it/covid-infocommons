import ReactDOM from 'react-dom';
import "./main.css"
import GrantsTable from './components/GrantTable';
import { GrantsFilter, OrgNameFacet } from './components/GrantsFilter';
import SearchBar from './components/SearchBar';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { Component } from "react";
import axios from "axios";
import DownloadIcon from '@mui/icons-material/Download';

interface Grant {
    id: number
    title: string
    award_amount: number
    abstract: string
    award_id: string
    pi: string
    funder_name: string
}

type Filter = {
    startDate?: string,
    endDate?: string
}

interface AppState {
    data: Grant[]
    url: string
    totalCount: number
    pageIndex: number
    awardee_org_names: OrgNameFacet[]
    pi_names: string[]
    filter: Filter
}


let url = ''
if (process.env.NODE_ENV == 'production') {
    url = "https://cic-apps.datascience.columbia.edu";
} else if (process.env.NODE_ENV == 'development') {
    url = "https://cice-dev.paas.cc.columbia.edu";
} else {
    url = "http://127.0.0.1:8000"
}

class App extends Component<any, AppState> {
    state = {
        data: [],
        url: url,
        totalCount: 0,
        pageIndex: 0,
        awardee_org_names: [],
        pi_names: [],
        filter: {
            'startDate': '',
            'endDate': '',
        }
    }

    constructor(props:any) {
        super(props)
        this.pageChangeHandler = this.pageChangeHandler.bind(this)
        this.filterChangeHandler = this.filterChangeHandler.bind(this)

    }

    componentDidMount = () => {
        this.get_grants_data()
        this.get_org_name_facet()
        this.get_pi_name_facet()
    }

    filterChangeHandler(fieldName:string, value:any) {
        console.log('Field = '.concat(fieldName))
        console.log('Value = ')
        console.log(value)
        var currentFilter = this.state.filter
        if (fieldName == 'startDate') {
            currentFilter['startDate'] = value
            // this.setState({
            //     filter: {'startDate': value}    
            // })
        }
        if (fieldName == 'endDate') {
            currentFilter['endDate'] = value
            // this.setState({
            //     filter: {'endDate': value}    
            // })
        }
        this.setState({filter: currentFilter})
    }

    searchHandler = (event:any) => {
        event.preventDefault()
        const keyword = (document.getElementById('outlined-search') as HTMLInputElement).value;
        this.get_grants_data(keyword)
    }

    get_org_name_facet() {
        var url = this.state.url.concat('/search/facets?field=awardee_organization.name')
        axios.get(url).then(results => {
            this.setState({ awardee_org_names: results.data.aggregations.patterns.buckets })
        })
    }

    get_pi_name_facet() {
        var url = this.state.url.concat('/search/facets?field=principal_investigator.first_name')
        axios.get(url).then(results => {
            this.setState({ pi_names: results.data.aggregations.patterns.buckets })
        })
    }

    get_grants_data = (keyword?:string) => {
        var url = this.state.url.concat('/search/grants')
        var params: { [key: string]: any } = {};

        const from:number = (this.state.pageIndex * 20) + 1
        params.from = from

        if (!keyword) {
            keyword = (document.getElementById('outlined-search') as HTMLInputElement).value;
        }
        if (keyword && keyword.length > 0) {
            //url = url.concat('&keyword=').concat(keyword)
            params.keyword = keyword
        }
        console.log(this.state.filter)

        let property: keyof typeof this.state.filter
        for (property in this.state.filter) {
            console.log('k = ')
            console.log(property)
            console.log(this.state.filter[property])
            if (this.state.filter[property]) {
                params[property] = this.state.filter[property]
            }
        }
        console.log('Params = ')
        console.log(params)
        axios.get(url, {params: params}).then(results => {
            this.setState({ totalCount: results.data.hits.total.value })

            var newArray = results.data.hits.hits.map(function(val:any) {
                var pi_name = ''
                var funder_name = ''
                if (val['_source']['principal_investigator'] != null) {
                    pi_name = val['_source']['principal_investigator']['first_name'] + ' ' + val['_source']['principal_investigator']['last_name']
                }
                return {
                    id: val['_source']['id'],
                    title: val['_source']['title'],
                    award_id: val['_source']['award_id'],
                    pi: pi_name,
                    abstract: val['_source']['abstract'],
                    award_amount: val['_source']['award_amount'],
                    funder_name: ('name' in val['_source']['funder']) ? val['_source']['funder']['name'] : ''
                }
            })
            this.setState({ data: newArray })
        })
    }

    downloadFile = (data:any, fileName:any, fileType:any) => {
        const blob = new Blob([data], { type: fileType })
        const a = document.createElement('a')
        a.download = fileName
        a.href = window.URL.createObjectURL(blob)
        const clickEvt = new MouseEvent('click', {
          view: window,
          bubbles: true,
          cancelable: true,
        })
        a.dispatchEvent(clickEvt)
        a.remove()
    }
      

    exportToCsv = (event:any) => {
        event.preventDefault()
        // Headers for each column
        let headers = ['Id,Title,Award_Amount,Award_ID,PI,Abstract,Funder']
        // Convert grants data to csv
        let grantsCsv = this.state.data.reduce((acc:any, grant:any) => {
            const grant_to_add:Grant = grant
            acc.push([
                grant_to_add.id,
                grant_to_add.title, 
                grant_to_add.award_amount,
                grant_to_add.award_id,
                grant_to_add.pi,
                grant_to_add.abstract,
                grant_to_add.funder_name
            ]
            .join(','))
            return acc
        }, [])
        this.downloadFile([...headers, ...grantsCsv].join('\n'), 'grants.csv', 'text/csv')
    }

    enterHandler = (e:any) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            this.get_grants_data()
        }
    }

    pageChangeHandler(page:number, pageSize: number) {
        this.setState({
            pageIndex: page
        })
        this.get_grants_data()
    }

    nsfDirectorateChangeHandler(val:string) {
        console.log('add the selected nsf directorate to filter')
    }

    render() {
        return (
            <Box
                sx={{
                    width: '100%',
                    '& .MuiTextField-root': { width: '85%' },
                }}
                component="form"
                noValidate
                autoComplete="off"
            >
                <div className='root'>
                    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"></link>
                    <form className='search-form'>
                        <TextField
                            id="outlined-search" 
                            label="Search" 
                            type="search" 
                            onKeyDown={ this.enterHandler }/>
                        <Button 
                            onClick={ this.searchHandler } 
                            className='search-button' 
                            variant="contained">Search</Button>
                    </form>
                    <br/>
                    <br/>
                    <div className='flex-container'>
                        <div className='flex-child'>
                            <GrantsTable
                                totalCount={ this.state.totalCount } 
                                data={ this.state.data} 
                                url={ this.state.url }
                                pageChangeHandler={ this.pageChangeHandler }
                                pageIndex={ this.state.pageIndex }
                            />
                        </div>
                        <div className='flex-child'>
                            <div className='download-csv'>
                                <Button onClick={ this.exportToCsv } 
                                        className='download-button' 
                                        variant="contained"
                                        endIcon={ <DownloadIcon /> }>Download Results as CSV
                                </Button>
                            </div>
                            <div>
                                <GrantsFilter
                                    awardee_org_names={ this.state.awardee_org_names }
                                    pi_names={ this.state.pi_names}
                                    start_date={ new Date() }
                                    nsfDirectorateChangeHandler={ this.nsfDirectorateChangeHandler }
                                    filterChangeHandler={ this.filterChangeHandler }
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </Box>
        );
    }
    
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);
        
