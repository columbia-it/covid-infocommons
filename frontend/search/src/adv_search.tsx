import ReactDOM from 'react-dom';
import "./main.css"
import GrantsTable from './components/GrantTable';
import PeopleTable from "./components/PeopleTable";
import PublicationsTable from "./components/PublicationsTable";
import DatasetsTable from "./components/DatasetsTable";
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import React, { Component } from "react";
import axios from "axios";
import DownloadIcon from '@mui/icons-material/Download';
import axiosRetry from 'axios-retry';

import Link from '@mui/material/Link';

/* import {
    Link as RouterLink,
    LinkProps as RouterLinkProps,
  } from 'react-router-dom';
*/

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

interface Person {
    id: number
    first_name: string
    last_name: string
    full_name: string
    institutions: string[]
}

interface Publication {
    id: number
    title: string
    doi: string
    authors: string[]
}

interface Dataset {
    id: number
    title: string
    doi: string
    authors: string[]
}


interface HomeState {
    keyword: string
    url: string
    grants: Grant[]
    total_grants: number
    people: Person[]
    total_people: number
    publications: Publication[]
    total_publications: number
    datasets: Dataset[]
    total_datasets: number
}


let url = ''
if (process.env.NODE_ENV == 'production') {
    url = "https://cic-apps.datascience.columbia.edu";
} else if (process.env.NODE_ENV == 'development') {
    url = "https://cic-apps-dev.datascience.columbia.edu";
} else {
    url = "http://127.0.0.1:8000"
}

class App extends Component<any, HomeState> {
    state:HomeState = {
        keyword: this.props.keyword,
        url: '',
        grants: [],
        total_grants: 0,
        people: [],
        total_people: 0,
        publications: [],
        total_publications: 0,
        datasets: [],
        total_datasets: 0
    }

    constructor(props:any) {
        super(props)
    }

    componentDidMount = () => {
        this.get_grants_data()
    }

    currentURL() {
	return window.location.href;
    }

    currPage() {
	if (this.currentURL().includes("adv_search")) {
	    return "search"
	} else {
	    return "grants"
	}
    }
    
    searchHandler = (event:any) => {
        event.preventDefault()
        const keyword = (document.getElementById('outlined-search') as HTMLInputElement).value;
        this.setState({'keyword': keyword})
        this.get_grants_data(keyword)
    }

    getDataPromise() {
        var params: { [key: string]: any } = {};
        params.from = 0
        params.size = 500
        let keyword = (document.getElementById('outlined-search') as HTMLInputElement).value;
        if (keyword && keyword.length > 0) {
            params.keyword = keyword
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
                console.log('App.getDataPromise()--Started at: ' + new Date().toLocaleString())
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
                console.log('App.getDataPromise()--Ended at: ' + new Date().toLocaleString())
                return newArray
           })

           .catch (err => {
               console.error(err)
            })
        }

    get_grants_data = (keyword?:string) => {
        console.log('App.get_grants_data()--Started at: ' + new Date().toLocaleString())

        var url = this.state.url.concat('/search/grants')
        var params: { [key: string]: any } = {};

        let from:number = 0

        params.from = from
        if (!keyword) {
            keyword = (document.getElementById('outlined-search') as HTMLInputElement).value;
        }
        if (keyword && keyword.length > 0) {
            params.keyword = keyword
        }

        console.log('App.get_grants_data()--Request sent at: ' + new Date().toLocaleString())
        axios.get(url, {params: params}).then(results => {
            console.log('App.get_grants_data()--Response received at: ' + new Date().toLocaleString())

            this.setState({ total_grants: results.data.hits.total.value })

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
            this.setState({ grants: newArray })
            console.log('App.get_grants_data()--Ended at: ' + new Date().toLocaleString())
	    //  this.get_pi_data()
	    this.get_people()
        })
    }


    get_people = (kw?:string) => {
        var url = this.state.url.concat('/search/people')
        var params: { [key: string]: any } = {};

        let from:number = 0

        params.from = from
        if (!kw) {
            kw = (document.getElementById('outlined-search') as HTMLInputElement).value;
        }
        if (kw && kw.length > 0) {
            params.keyword = kw
        }
        params['get_count'] = true
        console.log(params)
        axios.get(url, {params: params}).then(count_result => {
            this.setState({ total_people: count_result.data.count })
            delete params.get_count
            axios.get(url, {params: params}).then(results => {
                this.setState({ total_people: results.data.hits.total.value })

                var newArray = results.data.hits.hits.map(function(val:any) {
                    return {
                        id: val['_source']['id'],
                        name: val['_source']['full_name'],
                        emails: val['_source']['emails'],
                        private_emails: val['_source']['private_emails'],
                        affiliations: val['_source']['affiliations']
                    }
                })
                this.setState({ people: newArray })
        //        this.get_publications()
            })
        })
    }
    
    get_pi_data = (keyword?:string) => {
        console.log('App.get_pi_data()--Started at: ' + new Date().toLocaleString())

        var url = this.state.url.concat('/search/people')
        var params: { [key: string]: any } = {};

        let from:number = 0

        params.from = from
        if (!keyword) {
            keyword = (document.getElementById('outlined-search') as HTMLInputElement).value;
        }
        if (keyword && keyword.length > 0) {
            params.keyword = keyword
        }

        console.log('App.get_pi_data()--Request sent at: ' + new Date().toLocaleString())
	console.log(url + JSON.stringify(params))
        axios.get(url, {params: params}).then(results => {
            console.log('App.get_pi_data()--Response received at: ' + new Date().toLocaleString())

            this.setState({ total_people: results.data.hits.total.value })

            var newArray = results.data.hits.hits.map(function(val:any) {
		console.log('App.get_pi_data() -- result is ' + JSON.stringify(val))
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
                  /*  funder_name: ('name' in val['_source']['funder']) ? val['_source']['funder']['name'] : '', */
                    awardee_org: val['_source']['awardee_organization']['name']
                }
            })
            this.setState({ people: newArray })
            console.log('App.get_pi_data()--Ended at: ' + new Date().toLocaleString())

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

    enterHandler = (e:any) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            this.get_grants_data()
        }
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

      <div>
	  <GrantsTable
	    totalCount={ this.state.total_grants } 
            data={ this.state.grants} 
            url={ this.state.url }
	    pageIndex={ 0 }
            keyword={ this.state.keyword }
            />
       </div>
       <div className='flex-container'>
                        <div className='flex-child'></div>
                        <div className='flex-child'>
	    Placeholder for total grants link
                        </div>
       </div>

      <br/>

      <div>
	    <PeopleTable
                        paging={ false }
                        totalCount={ this.state.total_people }
                        data={ this.state.people.slice(0, 5) } 
                        url={ this.state.url }
                        pageIndex={ 0 }
                        keyword={ this.state.keyword }
                    />
       </div>    
		
    </div>
  </Box>
  );
  }
  
  }
  
  const rootElement = document.getElementById("root");
  ReactDOM.render(<App />, rootElement);
        
