import { Component } from "react";
import MaterialTable from "material-table";
import { Link as MaterialLink} from '@mui/material';
import Highlighter from 'react-highlight-words'

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
                    }}
                    columns={[
                        {
                            title: "Title", 
                            field: "title",
                            width: "60%",
                            render: (row: any) => {
                                console.log('....')
                                console.log(row.doi)
                                return (
                                    <div>
                                        <div>
                                            { row.title }
                                        </div>
                                        <div className="titleLink">
                                            <MaterialLink underline="hover" href={ row.doi } target="_blank">{ row.doi }</MaterialLink>
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
                            //exportButton: false,
                            pageSize: 20,
                            exportAllData: false
                        }
                    }
                >

                </MaterialTable>
            </div>
        )
    }
};

export default DatasetsTable;
