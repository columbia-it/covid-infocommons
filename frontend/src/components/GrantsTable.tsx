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
        const url = "https://cice-dev.paas.cc.columbia.edu/v1/grants"
        //const url = "http://127.0.0.1:8000/v1/grants"

        console.log('*******')
        console.log(url)
        axios.get(url).then(results => {
            this.setState(
                { data: results.data}
            )

            var newArray = results.data.data.map(function(val:any) {
                return {
                    id: val.id,
                    title: val.attributes.title,
                    award_id: val.attributes.award_id,
                    pi: val.attributes.principal_investigator.first_name + ' ' + val.attributes.principal_investigator.last_name,
                    abstract: val.attributes.abstract
                }
            })
            console.log(newArray)
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
            options={{ search: true, paging: false, filtering: true, exportButton: true }}
        />
      );
    }
}