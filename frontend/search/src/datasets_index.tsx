import { Component } from "react";
import SearchBar from './components/SearchBar';
import Button from '@mui/material/Button';

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

class Datasets extends Component<any, any> {
    render() {

        return (
            <div>
                <SearchBar/>
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
                    <div className='download-csv'>                            
                        <Button sx={styles}
	                            onClick={ this.exportToCsv } 
                                className='download-button' 
                                variant="contained"
                                endIcon={ <DownloadIcon /> }>Download Results as CSV (up to 1,000 awards)</Button>
                        </div>
                    </div>
            </div>
        )
    }
}

export default Datasets;