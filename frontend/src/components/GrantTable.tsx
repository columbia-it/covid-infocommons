import React, {Component} from "react";
import MaterialTable, { MTableToolbar } from "material-table";
import { TablePagination } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import { Link, TableContainer } from '@mui/material';
import NumberFormat from 'react-number-format';
import AbcIcon from '@mui/icons-material/Abc';
import { green, red } from '@mui/material/colors';
import SvgIcon, { SvgIconProps } from '@mui/material/SvgIcon';

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
        console.log(this.props.totalCount)
    }

    get_funder_icon(funder_name:string) {
        if (funder_name == 'National Institutes of Health') {
            return <SvgIcon><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" color='#008000'/></SvgIcon>
        }
        if (funder_name == 'National Science Foundation') {
            return <SvgIcon><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" color='#FF0000'/></SvgIcon>
        }
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
                                        <div>
                                            { this.get_funder_icon(row.funder_name) }
                                        </div>
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