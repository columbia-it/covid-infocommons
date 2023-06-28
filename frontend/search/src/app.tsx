import { Component } from "react";
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import axios from "axios";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from './home';
import Grants from './grants_index';
import People from './people_index';
import Publications from './publications_index';
import Datasets from './datasets_index';

let url = ''
if (process.env.NODE_ENV == 'production') {
    url = "https://cic-apps.datascience.columbia.edu";
} else if (process.env.NODE_ENV == 'development') {
    url = "https://cice-dev.paas.cc.columbia.edu";
} else {
    url = "http://127.0.0.1:8000"
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

interface AppState {
  keyword: string
  total_grants: number,
  grants: Grant[],
  url: string,
  total_people: number,
  people: Person[],
  total_publications: number
  publications: Publication[]
  total_datasets: number
  datasets: Dataset[]
}

class App extends Component<any, AppState> {

  state:AppState = {
    keyword: '',
    total_grants: 0,
    grants: [],
    url: url,
    total_people: 0,
    people: [],
    total_publications: 0,
    publications: [],
    total_datasets: 0,
    datasets: []
  }

  constructor(props:any) {
    super(props)
  }

  componentDidMount = () => {
    this.get_grants()
  }

  enterHandler = (e:any) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        this.get_grants()
    }
  }

  searchHandler = (event:any) => {
    event.preventDefault()
    const keyword = (document.getElementById('outlined-search') as HTMLInputElement).value;
    this.setState({'keyword': keyword})
    this.get_grants(keyword)
  }

  get_grants = (keyword?:string) => {
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
        console.log('App.get_grants(). total grants = ')
        console.log(this.state.total_grants)
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
        this.get_people()
        //this.get_funder_facet()
        console.log('App.get_grants_data()--Ended at: ' + new Date().toLocaleString())
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
        this.get_publications()
    })
  } 

  get_publications = (kw?:string) => {
    kw = this.props.keyword;
    
    var url = this.state.url.concat('/search/publications')
    var params: { [key: string]: any } = {};

    let from:number = 0

    params.from = from
    if (!kw) {
        kw = (document.getElementById('outlined-search') as HTMLInputElement).value;
    }
    if (kw && kw.length > 0) {
        params.keyword = kw
    }
    axios.get(url, {params: params}).then(results => {
        
        this.setState({ total_publications: results.data.hits.total.value })
        var newArray = results.data.hits.hits.map(function(val:any) {
          return {
            id: val['_source']['id'],
            doi: val['_source']['doi'],
            title: val['_source']['title'],
            issn: val['_source']['issn'],
            publication_type: val['_source']['publication_type'],
            authors: val['_source']['authors']
          }
        })
        this.setState({ publications: newArray })
        console.log('totalCount for publications = ')
        console.log(this.state.total_publications)
        this.get_datasets()
    })
  }

  get_datasets = (kw?:string) => {
    kw = this.props.keyword;
    
    var url = this.state.url.concat('/search/datasets')
    var params: { [key: string]: any } = {};

    let from:number = 0

    params.from = from
    if (!kw) {
        kw = (document.getElementById('outlined-search') as HTMLInputElement).value;
    }
    if (kw && kw.length > 0) {
        params.keyword = kw
    }
    axios.get(url, {params: params}).then(results => {
        
        this.setState({ total_datasets: results.data.hits.total.value })
        var newArray = results.data.hits.hits.map(function(val:any) {
          return {
            id: val['_source']['id'],
            doi: val['_source']['doi'],
            title: val['_source']['title'],
            mime_type: val['_source']['mime_type'],
            download_path: val['_source']['download_path'],
            authors: val['_source']['authors']
          }
        })
        this.setState({ datasets: newArray })
        console.log('totalCount for datasets = ')
        console.log(this.state.total_datasets)
        //this.get_author_facet()
    })
  }
  render() {
    return (
      <div>
        <Box
            sx={{
              width: '100%',
                    '& .MuiTextField-root': { width: '100%' },
              }}
            component="form"
            noValidate
            autoComplete="off">
          <div className='root'>
            <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"></link>
            <TextField
                id="outlined-search" 
                label="Search" 
                type="search"
                value={ this.state.keyword }
                onKeyDown={ this.enterHandler }
                onChange={ this.searchHandler }
                //onChange={(e) => this.searchHandler(e) }
            />
            <br/>
            <Routes>
              <Route path="/search" element={
                <Home 
                    grants={ this.state.grants }
                    total_grants={ this.state.total_grants }
                    keyword={ this.state.keyword }
                    people={ this.state.people }
                    total_people={ this.state.total_people }
                    publications={ this.state.publications }
                    total_publications={ this.state.total_publications }
                    datasets={ this.state.datasets }
                    total_datasets={ this.state.total_datasets }
                />
              }/>
              <Route path="/search/grants" element={
                  <Grants 
                    keyword={ this.state.keyword }
                    data={ this.state.grants }
                    totalCount={ this.state.total_grants } />
              } />
              <Route path="/search/people" element={
                  <People 
                    keyword={ this.state.keyword }
                    data={ this.state.people }
                    totalCount={ this.state.total_people } />
              } />
              <Route path="/search/publications" element={
                  <Publications 
                    keyword={ this.state.keyword }
                    data={ this.state.publications }
                    totalCount={ this.state.total_publications } />
              } />
              <Route path="/search/datasets" element={
                  <Datasets 
                    keyword={ this.state.keyword }
                    data={ this.state.datasets }
                    totalCount={ this.state.total_datasets } />
              } />
            </Routes>
          </div>
        </Box>
      </div>
    )}
}

export default App;