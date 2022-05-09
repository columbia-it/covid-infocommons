import React, { Component } from "react";
import MaterialTable, { MTableToolbar } from "material-table";
import axios from "axios";
import { makeStyles } from "@material-ui/core/styles";
import NumberFormat from 'react-number-format';
import { Link } from '@mui/material';

export default class GrantsTable extends React.Component<any, {grantsArray: [], data: [], url: string}> {
    constructor(props:any) {
        super(props)

        this.state = {
            data: [],
            grantsArray: [],
            url: ""
        }
    }

    componentDidMount() {
        const url = process.env.NODE_ENV == 'production' ? 
        "https://cic-apps.datascience.columbia.edu" : "https://cice-dev.paas.cc.columbia.edu"

        axios.get(url.concat('/search/grants')).then(results => {
            this.setState(
                { data: results.data.hits.hits }
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
                    abstract: val['_source']['abstract'],
                    award_amount: val['_source']['award_amount']
                }
            })
            this.setState({
                grantsArray: newArray,
                url: url
            })    
        })
    }

    render() {
      return (
        <MaterialTable
            data={this.state.grantsArray}
            columns={[
                {
                    title: "Projects", 
                    render: (row: any) => {
                        const detail_url = this.state.url.concat('/v1/grants/'+row.id)
                        return (<Link href={detail_url}>{row.title}</Link>)
                    }
                },
                {
                    title: "Principal Investigator", field: "pi",
                },
                {
                    title: "Award Amount", field: "award_amount", render: (row:any) => 
                    <div><NumberFormat value={row.award_amount} displayType={'text'} thousandSeparator={true} prefix={'$'} /></div>
                }
            ]}
            options={
                { 
                    paging: true, 
                    showTitle: false,
                    search: true,
                    searchFieldStyle: {
                        width: "100%",
                    }
                }
            }
            components={{
                Toolbar: props => {
                    const propsCopy = { ...props };
                    propsCopy.showTitle = false;
                    propsCopy.searchText = "Search PI Entries"
                    const useStyles = makeStyles({
                        toolbarWrapper: {
                            '& .MuiFormControl-root': {
                                width: '100%'
                            }
                        },
                        searchField: {
                            width: '80%'
                        }
                    });
                    const classes = useStyles();
                    return (
                        <div className={classes.toolbarWrapper}>
                            <MTableToolbar {...propsCopy}/>
                        </div>
                    );
                }
            }
        }
        />
      );
    }
}