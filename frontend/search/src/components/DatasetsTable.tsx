import { Component } from "react";
import MaterialTable from "material-table";
import { Link as MaterialLink} from '@mui/material';
import Highlighter from 'react-highlight-words'
import { TablePagination, TablePaginationProps } from '@material-ui/core';

type Prop = {
    'title': string
    'doi': string
}

type DatasetsTableProps = {
    data: Prop[]
    url: string
    totalCount: number
    keyword: string
    pageIndex: number
    pageChangeHandler?: (page:number, pageSize: number) => void 
    paging: boolean
}

class DatasetsTable extends Component<DatasetsTableProps> {

    PatchedPagination(props: TablePaginationProps) {
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
            rowsPerPageOptions={[]}
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
	    	    title= { "Datasets" } 
                    data={ this.props.data }
                    page={ this.props.pageIndex }
                    totalCount={ this.props.totalCount }
                    onChangePage={ (page, pageSize) => {
                        if (this.props.pageChangeHandler) this.props.pageChangeHandler(page, pageSize); 
                    }}
                    columns={[
                        {
                            title: "Title", 
                            field: "title",
                            width: "60%",
                            render: (row: any) => {
                                return (
                                    <div>
                                        <div>
                                            { row.title }
                                        </div>
                                        <div className="titleLink">
                                            <MaterialLink target="_blank" underline="hover" href={ row.doi }>{ row.doi }</MaterialLink>
                                        </div>
                                    </div>)
                            }

                        },
                        {
                            title: "Authors", 
                            field: "authors",
                            render: (row: any) => {
                                let author_names = []
                                if (row.authors) {
                                    for (let i = 0; i < row.authors.length; i++) {
                                        author_names.push(row.authors[i]['full_name'])
                                    }
                                }
                                return ( 
                                    <div>
                                        { author_names }
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
                            exportButton: false,
                            pageSize: 20,
                            exportAllData: false
                        }
                    }
                    components={{
                        Pagination: this.PatchedPagination,
                    }}
                >

                </MaterialTable>
            </div>
        )
    }
};

export default DatasetsTable;
