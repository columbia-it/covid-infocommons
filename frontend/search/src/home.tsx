import { Component } from "react";
import ModelSelect from './components/ModelSelect';
import GrantsTable from './components/GrantTable';
import PeopleTable from "./components/PeopleTable";
import PublicationsTable from "./components/PublicationsTable";
import DatasetsTable from "./components/DatasetsTable";

import Link from '@mui/material/Link';
import {
    Link as RouterLink,
    LinkProps as RouterLinkProps,
  } from 'react-router-dom';
import axios from "axios";

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
}

interface Dataset {
    id: number
    title: string
    doi: string
    authors: string[]
}

interface HomeProps {
    keyword: string
    grants: Grant[]
    total_grants: number
    people: Person[]
    total_people: number
    publications: Publication[]
    total_publications: number
    datasets: Dataset[]
    total_datasets: number
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
    url = "https://cice-dev.paas.cc.columbia.edu";
} else {
    url = "http://127.0.0.1:8000"
}

class Home extends Component<HomeProps, HomeState> {
    state:HomeState = {
        keyword: this.props.keyword,
        url: '',
        grants: this.props.grants,
        total_grants: this.props.total_grants,
        people: this.props.people,
        total_people: this.props.total_people,
        publications: this.props.publications,
        total_publications: this.props.total_publications,
        datasets: this.props.datasets,
        total_datasets: this.props.total_datasets
    }

    componentDidMount = () => {}

    componentDidUpdate = (prevProps:HomeProps) => {
        if(this.props.grants != prevProps.grants) // Check if grants have changed
        {
          this.setState({
              total_grants: this.props.total_grants,
              grants: this.props.grants,
              keyword: this.props.keyword
          })
        }

        if(this.props.total_grants != prevProps.total_grants) // Check if the total number of grants has changed
        {
          this.setState({
              total_grants: this.props.total_grants,
              grants: this.props.grants,
              keyword: this.props.keyword
          })
        }
        
        if(this.props.people != prevProps.people) // Check if people have changed
        {
          this.setState({
              total_people: this.props.total_people,
              people: this.props.people,
              keyword: this.props.keyword
          })
        }

        if(this.props.total_people != prevProps.total_people) // Check if the total number of people has changed
        {
          this.setState({
              total_people: this.props.total_people,
              people: this.props.people,
              keyword: this.props.keyword
          })
        }

        if(this.props.publications != prevProps.publications) // Check if publications have changed
        {
          this.setState({
              total_publications: this.props.total_publications,
              publications: this.props.publications,
              keyword: this.props.keyword
          })
        }

        if(this.props.total_publications != prevProps.total_publications) // Check if the total number of publications has changed
        {
          this.setState({
              total_publications: this.props.total_publications,
              publications: this.props.publications,
              keyword: this.props.keyword
          })
        }

        if(this.props.datasets != prevProps.datasets) // Check if datasets have changed
        {
          this.setState({
              total_publications: this.props.total_datasets,
              publications: this.props.datasets,
              keyword: this.props.keyword
          })
        }

        if(this.props.total_datasets != prevProps.total_datasets) // Check if the total number of datasets has changed
        {
          this.setState({
              total_publications: this.props.total_datasets,
              publications: this.props.datasets,
              keyword: this.props.keyword
          })
        }
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
        axios.get(url, {params: params}).then(results => {
            this.setState({ total_grants: results.data.hits.total.value })

            var newArray = results.data.hits.hits.map(function(val:any) {
                let pi_name = ''
                let pi_id = ''
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
            //this.get_funder_facet()
            console.log('App.get_grants_data()--Ended at: ' + new Date().toLocaleString())
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
            this.get_datasets()         
        })
    }

    get_datasets = (kw?:string) => {
        kw = this.props.keyword;
        console.log('dataset...kw = ')
        console.log(kw)
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
        })
    }

    render() {
        return (
            <div>
                <div className='flex-container'>
                    <div className='flex-child'></div>
                    <ModelSelect
                        selected_model={ 0 }/>
                </div>
                <div>
                    <GrantsTable
                        paging={ false }
                        totalCount={ this.state.total_grants }
                        data={ this.state.grants.slice(0, 5) } 
                        url={ this.state.url }
                        pageIndex={ 0 }
                        keyword={ this.state.keyword }
                    />
                    <div className='flex-container'>
                        <div className='flex-child'></div>
                        <div className='flex-child'>
                            <Link 
                                component={ RouterLink } 
                                to="/search/grants"
                                sx={{ fontSize: "18px", fontFamily: "proxima-nova, Montserrat, sans-serif;" }}>
                                See all {this.state.total_grants} grants
                            </Link>                        
                        </div>
                    </div>
                    <br/>
                </div>
                <div>
                    <PeopleTable
                        paging={ false }
                        totalCount={ this.state.total_people }
                        data={ this.state.people.slice(0, 5) } 
                        url={ this.state.url }
                        pageIndex={ 0 }
                        keyword={ this.state.keyword }
                    />
                    <div className='flex-container'>
                        <div className='flex-child'></div>
                        <div className='flex-child'>
                            <Link 
                                component={RouterLink} 
                                to="/search/people"
                                sx={{ fontSize: "18px", fontFamily: "proxima-nova, Montserrat, sans-serif;" }}>
                                See all {this.state.total_people} people
                            </Link>                        
                        </div>
                    </div>
                    <br/>
                </div>
                <div>
                    <PublicationsTable
                        paging={ false }
                        totalCount={ this.state.total_publications }
                        data={ this.state.publications.slice(0, 5) } 
                        url={ this.state.url }
                        pageIndex={ 0 }
                        keyword={ this.state.keyword }
                    />
                    <div className='flex-container'>
                        <div className='flex-child'></div>
                        <div className='flex-child'>
                            <Link 
                                component={RouterLink} 
                                to="/search/publications"
                                sx={{ fontSize: "18px", fontFamily: "proxima-nova, Montserrat, sans-serif;" }}>
                                See all {this.state.total_publications} publications
                            </Link>                        
                        </div>
                    </div>
                    <br/>
                </div>
                <div>
                    <DatasetsTable
                        paging={ false }
                        totalCount={ this.state.total_datasets }
                        data={ this.state.datasets.slice(0, 5) } 
                        url={ this.state.url }
                        pageIndex={ 0 }
                        keyword={ this.state.keyword }
                    />
                    <div className='flex-container'>
                        <div className='flex-child'></div>
                        <div className='flex-child'>
                            <Link 
                                component={RouterLink} 
                                to="/search/datasets"
                                sx={{ fontSize: "18px", fontFamily: "proxima-nova, Montserrat, sans-serif;" }}>
                                See all {this.state.total_datasets} datasets
                            </Link>                        
                        </div>
                    </div>
                    <br/>
                </div>
            </div>
        )
    }
}

export default Home;
