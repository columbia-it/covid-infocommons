import { Component } from "react";
import SearchBar from './components/SearchBar';
import Button from '@mui/material/Button';
import DownloadIcon from '@mui/icons-material/Download';
import { DatasetFilter, Facet } from "./components/DatasetsFilter";
import axios from "axios";
import DatasetsTable from "./components/DatasetsTable";
import ModelSelect from "./components/ModelSelect";

const styles = {
    // See MUI Button CSS classes at https://mui.com/material-ui/api/button/
    "&.MuiButton-contained": {
	color: "#FFFFFF",
	backgroundColor: "#2C6BAC",
	minWidth: "max-content",
	whiteSpace: "nowrap",
    textTransform: "none"
    },
};

interface DatasetsTableProps {
    keyword: string
    data: Dataset[]
    totalCount: number
}

interface Dataset {
    id: number
    title: string
    doi: string
    authors: string[]
}

interface Filter {
    author_name?: string
}

interface DatasetsState {
    data: Dataset[]
    url: string
    totalCount: number
    pageIndex: number
    filter: Filter
    search_in_progress: boolean
    keyword: string
    author_names: Facet[]
}

let url = ''
if (process.env.NODE_ENV == 'production') {
    url = "https://cic-apps.datascience.columbia.edu";
} else if (process.env.NODE_ENV == 'development') {
    url = "https://cice-dev.paas.cc.columbia.edu";
} else {
    url = "http://127.0.0.1:8000"
}

class Datasets extends Component<DatasetsTableProps, DatasetsState> {

    state:DatasetsState = {
        totalCount: this.props.totalCount,
        search_in_progress: false,
        data: this.props.data,
        pageIndex: 0,
        keyword: this.props.keyword,
        url: url,
        filter: {},
        author_names: []
    }

    constructor(props:any) {
        super(props)
        this.pageChangeHandler = this.pageChangeHandler.bind(this)
        this.filterChangeHandler = this.filterChangeHandler.bind(this)
    }

    pageChangeHandler(page:number, pageSize: number) {
        this.setState({
            pageIndex: page
        })
        this.get_datasets()
    }

    filterChangeHandler(fieldName?:string, value?:any, reset?:boolean) {
        if (reset) {
            this.state.filter = {}
            this.get_datasets()
            return
        }
        var currentFilter = this.state.filter
        
        if (fieldName == 'author_name') {
            if (!value || value.length === 0) {
                delete currentFilter.author_name;
            } else {
                currentFilter['author_name'] = value
            }
        }
        
        console.log(currentFilter)
        this.setState({filter: currentFilter})
        this.get_datasets()
    }

    get_datasets = (kw?:string) => {
        kw = this.props.keyword;
        console.log('dataset...kw = ')
        console.log(kw)
        this.setState({
            search_in_progress: true
        })
        var url = this.state.url.concat('/search/datasets')
        var params: { [key: string]: any } = {};

        let from:number = 0

        if (this.state.pageIndex > 0) {
            from = (this.state.pageIndex * 20) + 1
        } 
        params.from = from
        if (!kw) {
            kw = (document.getElementById('outlined-search') as HTMLInputElement).value;
        }
        if (kw && kw.length > 0) {
            params.keyword = kw
        }
        axios.get(url, {params: params}).then(results => {
            this.setState({
                search_in_progress: false
            })
            this.setState({ totalCount: results.data.hits.total.value })
            var newArray = results.data.hits.hits.map(function(val:any) {
                return {
                    id: val['_source']['id'],
                    doi: val['_source']['doi'],
                    title: val['_source']['title'],
                    mime_type: val['_source']['mime_type'],
                    download_path: val['_source']['download_path'],
                    authors: val['_source']['authors']
                }
            })
            this.setState({ data: newArray })
            this.get_author_facet()
        })
    }

    get_author_facet() {
        var url = this.state.url.concat('/search/facets/datasets/authors')
        axios.get(url).then(results => {
            this.setState({ author_names: results.data.aggregations.patterns.buckets })
        })
    }


    componentDidMount = () => {
        this.get_datasets()
    }

    componentDidUpdate = (prevProps:DatasetsTableProps) => {
        if(this.props.keyword != prevProps.keyword) // Check if the search keyword has changed
        {
            this.setState({
                keyword: this.props.keyword
            })
        }
        if(this.props.data != prevProps.data) // Check if the datasets have changed
        {
            this.setState({
                data: this.props.data,
                totalCount: this.props.totalCount
            })
        }
        if(this.props.totalCount != prevProps.totalCount) // Check if the total number of datasets has changed
        {
            this.setState({
                data: this.props.data,
                totalCount: this.props.totalCount
            })
        }
    }

    render() {
        return (
            <div>
                <br/>
                <div className='flex-container'>
                    {
                        this.state.search_in_progress == false ? 
                        <div className='results-row'>
                                Showing <span style={{fontWeight: 'bold', color: '#000000'}}>{ this.state.totalCount }</span> results.
                        </div> 
                        : <div className='results-row'>Waiting for results...
                        </div> 
                    }
                    <div className='flex-child'><ModelSelect
                            selected_model={ 4 }
                        />
                    </div>
                    <div className='flex-child'></div>
                </div>
                <div>  
                    <div className='flex-container'>
                        <div className='flex-child'>
                            <DatasetsTable
                                totalCount={ this.state.totalCount } 
                                data={ this.state.data} 
                                url={ this.state.url }
                                pageChangeHandler={ this.pageChangeHandler }
                                pageIndex={ this.state.pageIndex }
                                keyword={ this.state.keyword }
                                paging={ true }
                            >
                            </DatasetsTable>
                        </div>
                        <div className='flex-child'>
                            <div>
                                <DatasetFilter
                                    author_names={ this.state.author_names }
                                    filterChangeHandler={ this.filterChangeHandler }
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default Datasets;