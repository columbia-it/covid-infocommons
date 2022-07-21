import ReactDOM from 'react-dom';
import "./main.css"
import GrantsTable from './components/GrantTable';
import { GrantsFilter, Facet } from './components/GrantsFilter';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import React, { Component } from "react";
import axios from "axios";
import DownloadIcon from '@mui/icons-material/Download';

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

interface Grant {
    id: number
    title: string
    award_amount: number
    abstract: string
    award_id: string
    pi: string
    funder_name: string
    awardee_org: string
}

interface AppState {
    data: Grant[]
    url: string
    totalCount: number
    pageIndex: number
    awardee_org_names: Facet[]
    funder_divisions: Facet[]
    pi_names: Facet[]
    po_names: Facet[]
    filter: Filter
    keyword: string
    funder_names: Facet[]
}

interface Filter {
    nsf_division?: string
    nih_division?: string
    funder_division?: string
    start_date?: Date
    end_date?: Date
    awardee_organization?: string
    org_state?: string
    pi_name?: string
    po_name?: string
    funder_name?: string
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
    state:AppState = {
        data: [],
        url: url,
        totalCount: 0,
        pageIndex: 0,
        awardee_org_names: [],
        funder_divisions: [],
        pi_names: [],
        po_names: [],
        keyword: (window as any)['keywords'],
        filter: {},
        funder_names: []
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
        this.get_po_name_facet()
        this.get_funder_division_facet()
        this.get_funder_facet()
    }

    searchHandler = (event:any) => {
        event.preventDefault()
        const keyword = (document.getElementById('outlined-search') as HTMLInputElement).value;
        this.setState({'keyword': keyword})
        this.get_grants_data(keyword)
    }

    get_org_name_facet() {
        var url = this.state.url.concat('/search/facets?field=awardee_organization.name')
        axios.get(url).then(results => {
            this.setState({ awardee_org_names: results.data.aggregations.patterns.buckets })
        })
    }

    get_funder_division_facet() {
        var url = this.state.url.concat('/search/facets?field=funder_divisions')
        axios.get(url).then(results => {
            this.setState({ funder_divisions: results.data.aggregations.patterns.buckets })
        })
    }

    get_pi_name_facet(): Facet[] {
        var url = this.state.url.concat('/search/facets?field=principal_investigator.full_name')
        let pi_facet: Facet[] = [];
        axios.get(url).then(results => {
            this.setState({ pi_names: results.data.aggregations.patterns.buckets })
            pi_facet = results.data.aggregations.patterns.buckets

        })
        return pi_facet;
    }

    get_po_name_facet(): Facet[] {
        var url = this.state.url.concat('/search/facets?field=program_officials.full_name')
        let po_facet: Facet[] = [];
        axios.get(url).then(results => {
            this.setState({ po_names: results.data.aggregations.patterns.buckets })
            po_facet = results.data.aggregations.patterns.buckets

        })
        return po_facet;
    }

    get_funder_facet(): Facet[] {
        var url = this.state.url.concat('/search/facets?field=funder.name')
        let funder_facet: Facet[] = [];
        axios.get(url).then(results => {
            this.setState({ funder_names: results.data.aggregations.patterns.buckets })
            funder_facet = results.data.aggregations.patterns.buckets

        })
        return funder_facet;
    }

    getDataPromise() {
        var params: { [key: string]: any } = {};
        params.from = 0
        params.size = 1000
        let keyword = (document.getElementById('outlined-search') as HTMLInputElement).value;
        if (keyword && keyword.length > 0) {
            params.keyword = keyword
        }
        let property: keyof typeof this.state.filter
        for (property in this.state.filter) {
            if (this.state.filter[property]) {
                params[property] = this.state.filter[property]
            }
        }
        return axios({
                url: url + '/search/grants',
                method: 'get',
                headers: {
                    'Content-Type': 'application/json',
                },
                params: params
            })
           .then(res => {
               var newArray = res.data.hits.hits.map(function(val:any) {
                   let pi_name = ''
                   let pi_id = ''
                   let funder_name = ''
                   let pi_private_emails = ''
                   if (val['_source']['principal_investigator'] != null) {
                       pi_name = val['_source']['principal_investigator']['full_name']
                       pi_id = val['_source']['principal_investigator']['id']
                       pi_private_emails = val['_source']['principal_investigator']['private_emails']
                    }
                    return {
                        id: val['_source']['id'],
                        title: val['_source']['title'],
                        award_id: val['_source']['award_id'],
                        pi: pi_name,
                        pi_id: pi_id,
                        pi_private_emails: pi_private_emails,
                        abstract: val['_source']['abstract'],
                        award_amount: val['_source']['award_amount'],
                        funder_name: ('name' in val['_source']['funder']) ? val['_source']['funder']['name'] : '',
                        awardee_org: val['_source']['awardee_organization']['name']
                    }
                })
                return newArray
           })
           .catch (err => {
               console.error(err)
            })
        }

    get_grants_data = (keyword?:string) => {
        var url = this.state.url.concat('/search/grants')
        var params: { [key: string]: any } = {};

        let from:number = 0

        if (this.state.pageIndex > 0) {
            from = (this.state.pageIndex * 20) + 1
        } 
        params.from = from
        if (!keyword) {
            keyword = (document.getElementById('outlined-search') as HTMLInputElement).value;
        }
        if (keyword && keyword.length > 0) {
            params.keyword = keyword
        }

        let property: keyof typeof this.state.filter
        for (property in this.state.filter) {
            if (this.state.filter[property]) {
                params[property] = this.state.filter[property]
            }
        }
        
        axios.get(url, {params: params}).then(results => {
            this.setState({ totalCount: results.data.hits.total.value })

            var newArray = results.data.hits.hits.map(function(val:any) {
                let pi_name = ''
                let pi_id = ''
                let funder_name = ''
                let pi_private_emails = ''
                if (val['_source']['principal_investigator'] != null) {
                    pi_name = val['_source']['principal_investigator']['full_name']
                    pi_id = val['_source']['principal_investigator']['id']
                    pi_private_emails = val['_source']['principal_investigator']['private_emails']
                }
                return {
                    id: val['_source']['id'],
                    title: val['_source']['title'],
                    award_id: val['_source']['award_id'],
                    pi: pi_name,
                    pi_id: pi_id,
                    pi_private_emails: pi_private_emails,
                    abstract: val['_source']['abstract'],
                    award_amount: val['_source']['award_amount'],
                    funder_name: ('name' in val['_source']['funder']) ? val['_source']['funder']['name'] : '',
                    awardee_org: val['_source']['awardee_organization']['name']
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
        let headers = ['Funder, Award ID, Award Amount, Title, PI Name, Awardee Organization, Abstract, CIC ID']
        // Convert grants data to csv
        this.getDataPromise().then(res => {
            let grantsCsv = res.reduce((acc:any, grant:any) => {
                let grant_to_add:Grant = grant
                let abstract = grant_to_add.abstract
                if (abstract) {
                    abstract = grant_to_add.abstract.replaceAll('"', "'")
                }
                let awardee_org = grant_to_add.awardee_org
                if (awardee_org) {
                    if (awardee_org.indexOf(',') > -1) {
                        awardee_org = grant_to_add.awardee_org.replaceAll(',', '')
                    }
                }
                let pi_name = grant_to_add.pi
                if (pi_name) {
                    if (pi_name.indexOf(',') > -1) {
                        pi_name = grant_to_add.pi.replaceAll(',', '')
                    }
                }
                acc.push([
                    grant_to_add.funder_name,
                    grant_to_add.award_id,
                    grant_to_add.award_amount,
                    '"' + grant_to_add.title + '"', 
                    pi_name,
                    awardee_org,
                    '"' + abstract + '"', 
                    grant_to_add.id
                ]
                .join(','))
                return acc
            }, [])
            this.downloadFile([...headers, ...grantsCsv].join('\n'), 'grants.csv', 'text/csv')    
        })
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


    filterChangeHandler(fieldName?:string, value?:any, reset?:boolean) {
        if (reset) {
            this.state.filter = {}
            this.get_grants_data()
            return
        }
        var currentFilter = this.state.filter
        if (fieldName == 'nsf_division') {
            if (!value || value.length === 0) {
                delete currentFilter.nsf_division;
            } else {
                currentFilter['nsf_division'] = value
            }
        }
        if (fieldName == 'nih_division') {
            if (!value || value.length === 0) {
                delete currentFilter.nih_division;
            } else {
                currentFilter['nih_division'] = value
            }
        }
        if (fieldName == 'funder_division') {
            if (!value || value.length === 0) {
                delete currentFilter.funder_division;
            } else {
                currentFilter['funder_division'] = value
            }
        }
        if (fieldName == 'awardee_organization') {
            if (!value || value.length === 0) {
                delete currentFilter.awardee_organization;
            } else {
                currentFilter['awardee_organization'] = value
            }
        }
        if (fieldName == 'startDate') {
            if (value) {
                currentFilter['start_date'] = this.removeTime(value)
            } else {
                delete currentFilter.start_date;
            }
        }
        if (fieldName == 'endDate') {
            if (value) {
                currentFilter['end_date'] = this.removeTime(value)
            } else {
                delete currentFilter.end_date;
            }
        }
        if (fieldName == 'org_state') {
            if (!value || value.length === 0) {
                delete currentFilter.org_state;
            } else {
                currentFilter['org_state'] = value
            }
        }
        if (fieldName == 'pi_name') {
            if (!value || value.length === 0) {
                delete currentFilter.pi_name;
            } else {
                currentFilter['pi_name'] = value
            }
        }
        if (fieldName == 'po_name') {
            if (!value || value.length === 0) {
                delete currentFilter.po_name;
            } else {
                currentFilter['po_name'] = value
            }
        }
        if (fieldName == 'funder_name') {
            if (!value || value.length === 0) {
                delete currentFilter.funder_name;
            } else {
                currentFilter['funder_name'] = value
            }
        }
        console.log(currentFilter)
        this.setState({filter: currentFilter})
        this.get_grants_data()
    }

    removeTime(date:Date) {
        return new Date(
            date.getFullYear(),
            date.getMonth(),
            date.getDate()
        )
    }

    render() {
        return (
            <Box
                sx={{
                    width: '100%',
                    '& .MuiTextField-root': { width: '100%' },
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
                            value={ this.state.keyword }
                            onKeyDown={ this.enterHandler }
                            onChange={ this.searchHandler }/>

                        {/* <Button
	                    sx={styles}
                            onClick={ this.searchHandler } 
                            className='search-button' 
                            variant="contained">Search</Button> */}
                    </form>
                    <br/>
                    <div className='flex-container'>
                        <div className='results-row'>
                            Showing <span style={{fontWeight: 'bold', color: '#000000'}}>{ this.state.totalCount }</span> results.
                        </div>
                        <div className='download-csv'>                            
                            <Button sx={styles}
	                            onClick={ this.exportToCsv } 
                                className='download-button' 
                                variant="contained"
                                endIcon={ <DownloadIcon /> }>Download Results as CSV (up to 1,000 awards)</Button>
                        </div>
                    </div>    
                    <br/>
                    <div className='flex-container'>
                        <div className='flex-child'>
                            <GrantsTable
                                totalCount={ this.state.totalCount } 
                                data={ this.state.data} 
                                url={ this.state.url }
                                pageChangeHandler={ this.pageChangeHandler }
                                pageIndex={ this.state.pageIndex }
                                keyword={ this.state.keyword }
                            />
                </div>
                <div className='flex-child'>
                            <div>
                                <GrantsFilter
                                    awardee_org_names={ this.state.awardee_org_names }
                                    funder_divisions={ this.state.funder_divisions }
                                    pi_names={ this.state.pi_names }
                                    program_official_names={ this.state.po_names}
                                    funder_names={ this.state.funder_names }
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
        
