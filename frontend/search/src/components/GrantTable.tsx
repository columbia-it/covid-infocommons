import { Component } from "react";
import MaterialTable, { MTableToolbar } from "material-table";
//import MaterialTable from '@material-table/core';
import { TablePagination } from "@material-ui/core";
import { css } from '@emotion/react'
import { Link as MaterialLink} from '@mui/material';
import NumberFormat from 'react-number-format';
import Highlighter from 'react-highlight-words'

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
    keyword: string | ''
}


class GrantsTable extends Component<GrantsTableProps> {
    truncate = (str:string, n:number) => {
		return str?.length > n ? str.substring(0, n - 1) + "..." : str;
	}

    renderAbstract = (text: string) => {
        var truncatedAbstract = this.truncate(text, 250) 
        return this.highlightText(truncatedAbstract)
    }

    highlightText = (textToHighlight:string ) => {
        return (<Highlighter
            highlightStyle={{
                fontWeight: "bold",
                padding: 0,
                backgroundColor: "#FFFFFF"
            }}
            searchWords={[this.props.keyword]}
            autoEscape={ true }
            textToHighlight={ textToHighlight }
        />)
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
                columns={[
                    {
                        title: "Awards", 
                        field: "title",
			width: "50%",
                        render: (row: any) => {
                            let detail_url = this.props.url.concat('/grants/'+row.id)
                            if (this.props.keyword) {
                                detail_url = detail_url.concat('?keyword='+this.props.keyword)
                            }
                            return (<div>
                                        <div>
                                            { this.get_funder_icon(row.funder_name) }
                                        </div>
                                        <div className="titleLink">
                                            <MaterialLink underline="hover" href={ detail_url }>{ this.highlightText(row.title) }</MaterialLink>
                                        </div>
                                        <div className="truncAbstract">
                                            <p>{ this.renderAbstract(row.abstract) }
                                            <a href={ detail_url} className="showMoreLink">SHOW MORE</a></p>
                                        </div>
                                    </div>)
                        }
                    },
                    {
                        title: "Principal Investigator", field: "pi",
                        render: (row: any) => {
                            let pi_detail_url = (row.pi_private_emails) ? row.pi_private_emails : this.props.url.concat('/search/pi/'+ row.pi_id)
                            if (this.props.keyword) {
                                pi_detail_url = pi_detail_url.concat('?keyword='+this.props.keyword)
                            }
                            return (
                                <div>
                                    <MaterialLink underline="hover" href={ pi_detail_url }>{ this.highlightText(row.pi) }</MaterialLink>
                                </div>
                            )
                        }
                    },
                    {
                        title: "Award Amount", field: "award_amount", render: (row:any) => 
                            {
                                if (row.award_amount) {
                                    return (<div><NumberFormat value={row.award_amount} displayType={ 'text' } thousandSeparator={ true } prefix={'$'} /></div>)
                                } else {
                                    return (<div></div>)
                                }
                            }
                    }
                ]}
                options={
                    { 
                        paging: true, 
                        showTitle: false,
                        search: false,
                        //exportButton: false,
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
                                onPageChange={ (page:number, pageSize:number) => {
                                    this.props.pageChangeHandler(page, pageSize)
                                } }
                            />
                        ),
                    }
                }
            />
        )
    }
}

export default GrantsTable;
