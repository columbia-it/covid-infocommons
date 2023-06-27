import { Component } from "react";
import MaterialTable from "material-table";
import { Link as MaterialLink} from '@mui/material';
import Highlighter from 'react-highlight-words'
import { TablePagination, TablePaginationProps } from '@material-ui/core';

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
    pageChangeHandler?: (page:number, pageSize: number) => void 
    paging: boolean
}

function PatchedPagination(props: TablePaginationProps) {
    const {
      ActionsComponent,
      onChangePage,
      onChangeRowsPerPage,
      ...tablePaginationProps
    } = props;
  
    return (
      <TablePagination
        {...tablePaginationProps}
        // @ts-expect-error onChangePage was renamed to onPageChange
        onPageChange={onChangePage}
        onRowsPerPageChange={onChangeRowsPerPage}
        ActionsComponent={(subprops) => {
          const { onPageChange, ...actionsComponentProps } = subprops;
          return (
            // @ts-expect-error ActionsComponent is provided by material-table
            <ActionsComponent
              {...actionsComponentProps}
              onChangePage={onPageChange}
            />
          );
        }}
      />
    );
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
            <div>
            <MaterialTable
                data={ this.props.data }
                page={ this.props.pageIndex }
                totalCount={ this.props.totalCount }
                onChangePage={ (page, pageSize) => {
                    if (this.props.pageChangeHandler) this.props.pageChangeHandler(page, pageSize); 
                } }
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
                    },
                    {
                        title: 'Institutions',
                        field: 'affiliations',
                        render: (row: any) => {
                            let org_names = []
                            if (row.affiliations) {
                                for (let i = 0; i < row.affiliations.length; i++) {
                                    org_names.push(row.affiliations[i]['name'])
                                }
                            }
                            return (
                                <div>
                                    { org_names }
                                </div>
                            )
                        }
                    }
                ]}
                options={
                    { 
                        paging: this.props.paging,
                        showTitle: false,
                        search: false,
                        pageSize: 20,
                        exportAllData: false
                    }
                }
                components={
                    {
                        Pagination: PatchedPagination
                    }
                }
            >

            </MaterialTable>
            </div>
        )}
}

export default PeopleTable;
