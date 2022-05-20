import React, {Component} from "react";
import MaterialTable, { MTableToolbar } from "material-table";
import { TablePagination } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import { Link } from '@mui/material';
import NumberFormat from 'react-number-format';

type Prop = {
    'title': string
    'pi': string
    'award_amount': number
}
type GrantsTableProps = {
    data: Prop[],
    url: string
    totalCount: number
    pageIndex: number
}

class GrantsTable extends Component<GrantsTableProps> {
    componentDidUpdate(prevProps:any) {
        console.log(prevProps)
    }

    pageChangeHandler = (event: any, page: number) => {
        console.log('page changed.')
    }

    render() {
        return (
            <MaterialTable
            data={this.props.data}
            onChangePage={ this.pageChangeHandler }
            page={ this.props.pageIndex }
            columns={[
                {
                    title: "Projects", 
                    field: "title",
                    render: (row: any) => {
                        const detail_url = this.props.url.concat('/grants/'+row.id)
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
                    search: false,
                    exportButton: false,
                    pageSize: 30,
                    exportAllData: false
                }
            }
            components={{
                Pagination: props => (
                    <TablePagination
                        {...props}
                        rowsPerPageOptions={[]}
                        count={ this.props.totalCount }
                    />
                ),
                Toolbar: props => {
                    const propsCopy = { ...props };
                    propsCopy.showTitle = false;
                    propsCopy.placeholder = "Search PI Entries"
                    const useStyles = makeStyles({
                        toolbarWrapper: {
                            // '& .MuiToolbar-gutters': {
                            //     paddingLeft: 0,
                            //     paddingRight: 0,
                            // },
                            '& .MTableToolbar-spacer-8': {
                                display: 'none'
                            },
                            '& .MTableToolbar-searchField-11': {
                                width: '100%'
                            },
                        },
                    });
                    const classes = useStyles();
                    return (
                        <div className={classes.toolbarWrapper}>
                            <MTableToolbar {...propsCopy}/>
                        </div>
                    )
                }
            }
        }
        />
        )
    }
}

export default GrantsTable;