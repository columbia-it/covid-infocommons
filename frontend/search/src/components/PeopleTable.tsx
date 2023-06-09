import { Component } from "react";
import MaterialTable from "material-table";
import { Link as MaterialLink} from '@mui/material';
import Highlighter from 'react-highlight-words'
import { TablePagination } from "@material-ui/core";

type Prop = {
    'full_name': string
    'institutions': string[]
}

type PeopleTableProps = {
    data: Prop[],
    totalCount: number
    keyword: string | ''
    url: string
    pageIndex: number
    pageChangeHandler: (page:number, pageSize: number) => void 
}

class PeopleTable extends Component<PeopleTableProps> {
    
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

    render() {
        return (
            <MaterialTable
                data={ this.props.data }
                totalCount={ this.props.totalCount }
                columns={[
                    {
                        title: "Name", 
                        field: "name",
                        render: (row: any) => {
                            let pi_detail_url = (row.private_emails) ? row.private_emails : this.props.url.concat('/search/pi/'+ row.id)
                            if (this.props.keyword) {
                                pi_detail_url = pi_detail_url.concat('?keyword='+this.props.keyword)
                            }
                            return (
                                <div>
                                    <MaterialLink underline="hover" href={ pi_detail_url }>{ this.highlightText(row.name) }</MaterialLink>
                                </div>
                            )
                        }
                    }
                ]}
                options={
                    { 
                        paging: true, 
                        showTitle: false,
                        search: false,
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
            >

            </MaterialTable>
        )}
}

export default PeopleTable;
