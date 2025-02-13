import { Component } from "react";
import MaterialTable from "material-table";
import { Link as MaterialLink} from '@mui/material';
import Highlighter from 'react-highlight-words'
import { TablePagination, TablePaginationProps } from '@material-ui/core';

type Prop = {
    'title': string
    'doi': string
}

type PublicationsTableProps = {
    data: Prop[]
    url: string
    totalCount: number
    keyword: string
    pageIndex: number
    pageChangeHandler?: (page:number, pageSize: number) => void 
    paging: boolean
}

interface TableState {
    authors: string[]
    itemsToShow: number
    expanded: boolean
}

class PublicationsTable extends Component<PublicationsTableProps, TableState> {
    state:TableState = {
        authors: [],
        itemsToShow: 3,
        expanded: false,
    }

    constructor(props:PublicationsTableProps) {
        super(props)
        this.showLess = this.showLess.bind(this)
    }

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

    // showMore() {
    //     this.state.itemsToShow === 3 ? (
    //       this.setState({ itemsToShow: 3, expanded: false })
    //     ) : (
    //       this.setState({ itemsToShow: this.state.authors.length, expanded: true })
    //     )
    //   }

    showLess() {
        let current_state = this.state.expanded
        this.setState({expanded: !current_state})
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
                                            <MaterialLink underline="hover" href={ row.doi } target="_blank">{ row.doi } </MaterialLink>
                                        </div>
                                    </div>
                                )
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
                                    {/* <ul> */}
                                    <div id='sliced_author_names' hidden={ this.state.expanded }>
                                    { author_names.slice(0, this.state.itemsToShow) }
                                    </div>
                                    <div id='all_author_names' hidden={ !this.state.expanded }>
                                    { author_names }
                                    </div>
                                    <br/>
                                        {/* { author_names.slice(0, this.state.itemsToShow).map((author, i) => 
                                        <li key={i}>{author}</li>
                                        )} */}
                                    {/* </ul> */}
                                    {
                                        author_names.length > 3 ? 
                                        <a onClick={ this.showLess }>
                                        {this.state.expanded ? (
                                            <span>Show less</span>
                                            ) : (
                                        <span>Show more</span>
                                        )}
                                        </a> 
                                        : <div></div>
                                    }                                     
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

export default PublicationsTable;
