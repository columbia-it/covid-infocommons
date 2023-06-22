import Box from '@mui/material/Box';
import React, { Component } from "react";
import { useParams } from 'react-router-dom'
import ModelSelect from './components/ModelSelect';
import { SearchContext } from './search_context';
import GrantsTable from './components/GrantTable';
import axios from "axios";
import PeopleTable from './components/PeopleTable';
import Link from '@mui/material/Link';
import {
    Link as RouterLink,
    LinkProps as RouterLinkProps,
    MemoryRouter,
  } from 'react-router-dom';
import { styled } from '@mui/material/styles';

interface HomeState {
    url: string
    total_grants: number,
    grants: Grant[],
    total_people: number,
    people: Person[]
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

let url = ''
if (process.env.NODE_ENV == 'production') {
    url = "https://cic-apps.datascience.columbia.edu";
} else if (process.env.NODE_ENV == 'development') {
    url = "https://cice-dev.paas.cc.columbia.edu";
} else {
    url = "http://127.0.0.1:8000"
}

class Home extends Component<any, HomeState> {

    state:HomeState = {
        url: url,
        total_grants: 0,
        grants: [],
        total_people: 0,
        people: []
    }

    componentDidMount = () => {
        this.get_grants_data()
        this.get_people_data()
    }

    get_grants_data = (kw?:any) => {
        console.log(SearchContext)
        kw = SearchContext;
        var url = this.state.url.concat('/search/grants?from=0&size=5')
        var params: { [key: string]: any } = {};

        let from:number = 0

        if (!kw) {
            kw = (document.getElementById('outlined-search') as HTMLInputElement).value;
        }
        if (kw && kw.length > 0) {
            params.keyword = kw
        }
        
        axios.get(url, {params: params}).then(results => {
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
        })
    }

    get_people_data = (kw?:string) => {
        var url = this.state.url.concat('/search/people?from=0&size=5')
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
        })
    }
    
    //const routeParams = useParams();
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
                        data={ this.state.grants} 
                        url={ this.state.url }
                        //pageChangeHandler={ null }
                        pageIndex={ 0 }
                        keyword={ '' }
                    />
                    <br/>
                    <div className='flex-container'>
                        <div className='flex-child'></div>
                        <div className='flex-child'>
                            <Link 
                                component={RouterLink} 
                                to="/search/grants"
                                sx={{ fontSize: "18px", fontFamily: "proxima-nova, Montserrat, sans-serif;" }}>
                                See all grants
                            </Link>                        
                        </div>
                    </div>
                    <br/>
                </div>
                <br/>
                <div>
                    <PeopleTable
                        paging={ false }
                        totalCount={ this.state.total_people } 
                        data={ this.state.people } 
                        url={ this.state.url }
                        //pageChangeHandler={ null }
                        pageIndex={ 0 }
                        keyword={ '' }
                    />
                </div>
            </div>
        )
    };
}

export default Home;