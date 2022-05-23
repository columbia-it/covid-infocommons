import React, {Component} from "react";
import MaterialTable, { MTableToolbar } from "material-table";
import { TablePagination } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import { Link, TableContainer } from '@mui/material';
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
    //pageIndex: number
}

class GrantsTable extends Component<GrantsTableProps> {
    componentDidUpdate(prevProps:any) {
        console.log(prevProps)
    }

    pageChangeHandler = (event: any, page: number) => {
        console.log('page changed.')
    }

    truncate = (str:string, n:number) => {
		return str?.length > n ? str.substring(0, n - 1) + "..." : str;
	};

    componentDidMount() {
        console.log('Table rendered')
        console.log(this.props.totalCount)
    }

    render() {
        return (
            <MaterialTable
                data={ this.props.data }
                totalCount={ this.props.totalCount }
                columns={[
                    {
                        title: "Projects", 
                        field: "title",
                        render: (row: any) => {
                            const detail_url = this.props.url.concat('/grants/'+row.id)
                            return (<div>
                                        <div className="titleLink">
                                            <Link href={detail_url}>{row.title}</Link>
                                        </div>
                                        <div className="truncAbstract">
                                            <p>{ this.truncate(row.abstract, 100) }
                                            <a href={ detail_url} className="showMoreLink">SHOW MORE</a></p>
                                        </div>
                                    </div>)
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
                        pageSize: 20,
                        exportAllData: false
                    }
                }
                // components={{
                //     Pagination: props => (
                //         <TablePagination
                //             {...props}
                //             rowsPerPageOptions={[]}
                //             count={ this.props.totalCount }
                //         />
                //     ),
                // }

                // }
            />
        )
    }
}

export default GrantsTable;