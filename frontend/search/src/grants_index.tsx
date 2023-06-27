import React, { Component, useContext } from "react";
import { GrantsFilter, Facet } from './components/GrantsFilter';
import axios from "axios";
import Button from '@mui/material/Button';
import DownloadIcon from '@mui/icons-material/Download';
import axiosRetry from 'axios-retry';
import GrantsTable from './components/GrantTable';
import ModelSelect from './components/ModelSelect';
import {SearchContext} from './search_context';

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

interface GrantsState {
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
    search_in_progress: boolean
}

let url = ''
if (process.env.NODE_ENV == 'production') {
    url = "https://cic-apps.datascience.columbia.edu";
} else if (process.env.NODE_ENV == 'development') {
    url = "https://cice-dev.paas.cc.columbia.edu";
} else {
    url = "http://127.0.0.1:8000"
}

axiosRetry(axios, {retries: 3});

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

interface GrantTableProps {
    keyword: string,
    data: Grant[]
    totalCount: number
}

class Grants extends Component<GrantTableProps, GrantsState> {
    static context = SearchContext;
    state:GrantsState = {
        data: this.props.data,
        url: url,
        totalCount: this.props.totalCount,
        pageIndex: 0,
        awardee_org_names: [],
        funder_divisions: [],
        pi_names: [],
        po_names: [],
        //keyword: (window as any)['keywords'],
        keyword: this.props.keyword,
        filter: {},
        funder_names: [],
        search_in_progress: false
    }


    constructor(props:any) {
        super(props)
        this.pageChangeHandler = this.pageChangeHandler.bind(this)
        this.filterChangeHandler = this.filterChangeHandler.bind(this)
    }

    componentDidMount = () => {
        this.get_grants_data()
    }

    componentDidUpdate = (prevProps:GrantTableProps) => {
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


    get_org_name_facet() {
        var url = this.state.url.concat('/search/facets?field=awardee_organization.name')
        axios.get(url).then(results => {
            this.setState({ awardee_org_names: results.data.aggregations.patterns.buckets })
            this.get_pi_name_facet()    
        })
    }

    get_funder_division_facet() {
        var url = this.state.url.concat('/search/facets?field=funder_divisions')
        axios.get(url).then(results => {
            this.setState({ funder_divisions: results.data.aggregations.patterns.buckets })
            this.get_funder_facet()
        })
    }

    get_pi_name_facet(): Facet[] {
        var url = this.state.url.concat('/search/facets?field=principal_investigator.full_name')
        let pi_facet: Facet[] = [];
        axios.get(url).then(results => {
            this.setState({ pi_names: results.data.aggregations.patterns.buckets })
            pi_facet = results.data.aggregations.patterns.buckets
            this.get_po_name_facet()
        })
        return pi_facet;
    }

    get_po_name_facet(): Facet[] {
        var url = this.state.url.concat('/search/facets?field=program_officials.full_name')
        let po_facet: Facet[] = [];
        axios.get(url).then(results => {
            this.setState({ po_names: results.data.aggregations.patterns.buckets })
            po_facet = results.data.aggregations.patterns.buckets
            this.get_funder_division_facet()
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
        this.setState({filter: currentFilter})
        this.get_grants_data()
    }

    get_grants_data = (kw?:string) => {
        kw = this.props.keyword;
        this.setState({
            search_in_progress: true
        })
        var url = this.state.url.concat('/search/grants')
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
                    award_amount: (val['_source']['award_amount'] !== null) ? val['_source']['award_amount'] : 0,
                    funder_name: ('name' in val['_source']['funder']) ? val['_source']['funder']['name'] : '',
                    awardee_org: val['_source']['awardee_organization']['name']
                }
            })
            this.setState({ data: newArray })
            this.get_org_name_facet()
        })
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
                        award_amount: (val['_source']['award_amount'] !== null) ? val['_source']['award_amount'] : 0,
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


    removeTime(date:Date) {
        return new Date(
            date.getFullYear(),
            date.getMonth(),
            date.getDate()
        )
    }

    searchHandler = (event:any) => {
        event.preventDefault()
        const keyword = (document.getElementById('outlined-search') as HTMLInputElement).value;
        this.setState({'keyword': keyword})
        this.get_grants_data(keyword)
    }

    render() {
        return (
            <div>
                <br/>
                <div className='flex-container'>
                    {
                        this.state.search_in_progress == false ? 
                        <div className='results-row'>
                                Showing <span style={{fontWeight: 'bold', color: '#000000'}}>{ this.state.totalCount }</span> results.
                        </div> 
                        : <div className='results-row'>Waiting for results...
                        </div> 
                    } 
                    <div><ModelSelect
                            selected_model={ 1 }/>
                    </div>
                    <div>                            
                            <Button sx={styles}
	                            onClick={ this.exportToCsv } 
                                className='download-button' 
                                variant="contained"
                                endIcon={ <DownloadIcon /> }>Download Results as CSV (up to 1,000 awards)</Button>
                    </div>
                </div>
                <br/>
                <div>  
                    <div className='flex-container'>
                        <div className='flex-child'>
                        <GrantsTable
                            paging={ true }
                            totalCount={ this.state.totalCount } 
                            data={ this.state.data} 
                            url={ this.state.url }
                            pageIndex={ this.state.pageIndex }
                            keyword={ this.state.keyword }
                            pageChangeHandler={ this.pageChangeHandler }

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
            </div>
        );
    }
}

export default Grants;



