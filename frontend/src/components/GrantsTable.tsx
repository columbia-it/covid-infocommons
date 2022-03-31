import React, { Component } from "react";
import MaterialTable from "material-table";
import axios from "axios";

const columns = [
    {
        name: 'Projects',
        selector: (row: any) => row.title,
        width: "300px",
        sortable: true
    }, 
    {
        name: 'Award ID',
        selector: (row: any) => row.award_id,
        width: "200px",
        sortable: true
    },
    {
        name: 'Principal Investigator',
        selector: (row: any) => row.principal_investigator.first_name,
        width: "200px",
        sortable: true
    },
    {
        name: 'Abstract',
        selector: (row: any) => row.abstract,
        sortable: true
    }
]

class MyState {
    data : []
    count : number

    constructor(data: [], count: number) {
        this.data = data
        this.count = count
    }
}

export default class GrantsTable extends React.Component<any, {grantsArray: [], data: []}> {
    constructor(props:any) {
        super(props)

        this.state = {
            data: [],
            grantsArray: []
        }
    }

    componentDidMount() {
        const url = "https://cice-dev.paas.cc.columbia.edu/search/grants"

        axios.get(url).then(results => {
            //console.log(results.data.hits.hits)
            this.setState(
                { data: results.data.hits.hits}
            )     
            var newArray = results.data.hits.hits.map(function(val:any) {
                var pi_name = ''
                if (val['_source']['principal_investigator'] != null) {
                    pi_name = val['_source']['principal_investigator']['first_name'] + ' ' + val['_source']['principal_investigator']['last_name']
                }
                return {
                    id: val['_source']['id'],
                    title: val['_source']['title'],
                    award_id: val['_source']['award_id'],
                    pi: pi_name,
                    abstract: val['_source']['abstract']
                }
            })
            this.setState({
                grantsArray: newArray
            })    
        })
    }

    render() {
      return (
        <MaterialTable
            title="Grants"
            data={this.state.grantsArray}
            columns={[
                {
                    title: "Title", field: "title"
                },
                {
                    title: "PI", field: "pi",
                },
                {
                    title: "Abstract", field: "abstract"
                }
            ]}
            options={{ paging: false }}
        />
      );
    }
}