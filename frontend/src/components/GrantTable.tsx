import { Component } from "react";
import MaterialTable, { MTableToolbar } from "material-table";
import { TablePagination } from "@material-ui/core";
import { css, jsx, ThemeProvider } from '@emotion/react'
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
    pageChangeHandler: (page:number, pageSize: number) => void 
    pageIndex: number
}


class GrantsTable extends Component<GrantsTableProps> {
    truncate = (str:string, n:number) => {
		return str?.length > n ? str.substring(0, n - 1) + "..." : str;
	}

    get_funder_icon(funder_name:string) {
        if (funder_name == 'National Institutes of Health') {
	    return(
		    <div css={css`
                     color: #FFFFFF;
                     background-color: #777777;
                     border-radius: 4px;
                     width: min-content;
                     padding-left: 5px; padding-right: 5px;
                     `}
		    >
		    NIH
		    </div>
	    )
        }
        if (funder_name == 'National Science Foundation') {
	    return (
		    <div css={css`
                     color: #FFFFFF;
                     background-color: #3C75CF;
                     border-radius: 4px;
                     width: min-content;
                     padding-left: 5px; padding-right: 5px;
                     `}
		    >
		    NSF
		    </div>
	    )
        }
    }

    render() {
        return (
            <MaterialTable
                data={ this.props.data }
                page={ this.props.pageIndex }
                totalCount={ this.props.totalCount }
                onChangePage={ (page, pageSize) => {
                    this.props.pageChangeHandler(page, pageSize)
                } }
                columns={[
                    {
                        title: "Projects", 
                        field: "title",
			width: "50%",
                        render: (row: any) => {
                            const detail_url = this.props.url.concat('/grants/'+row.id)
                            return (<div>
                                        <div>
                                            { this.get_funder_icon(row.funder_name) }
                                        </div>
                                        <div className="titleLink">
                                            <Link underline="hover" href={detail_url}>{row.title}</Link>
                                        </div>
                                        <div className="truncAbstract">
                                            <p>{ this.truncate(row.abstract, 200) }
                                            <a href={ detail_url} className="showMoreLink">SHOW MORE</a></p>
                                        </div>
                                    </div>)
                        }
                    },
                    {
                        title: "Principal Investigator", field: "pi",
                        render: (row: any) => {
                            const pi_detail_url = this.props.url.concat('/grants/pi/'+ row.pi_id)
                            return (
                                <div>
                                    <Link underline="hover" href={pi_detail_url}>{row.pi}</Link>
                                </div>
                            )
                        }
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
                components={
                    {
                        Pagination: props => (
                            <TablePagination
                                {...props}
                                rowsPerPageOptions={[]}
                            />
                        ),
                    }
                }
            />
        )
    }
}

export default GrantsTable;
