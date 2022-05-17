import ReactDOM from 'react-dom';
import "./main.css"
import GrantsTable from './components/GrantsTable';
import GrantsFilter from './components/GrantsFilter';
import SearchBar from './components/SearchBar';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';


function App() {
    return (
        <Box
            sx={{
                width: '100%',
                '& .MuiTextField-root': { width: '85%' },
            }}
            component="form"
            noValidate
            autoComplete="off"
        >
            <div className='root'>
                <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"></link>
                <h1 className='cic-heading'>COVID INFORMATION COMMONS</h1>
                <form className='search-form'>
                    <TextField
                        id="outlined-search" 
                        label="Search PI Entries" 
                        type="search" />
                    <Button className='search-button' variant="contained">Search</Button>
                </form>
                <br/>
                <br/>
                <div className='flex-container'>
                    <div className='flex-child'>
                        <GrantsTable/>
                    </div>
                    <div className='flex-child'>
                        <div className='download-csv'>
                            <Button className='download-button' variant="contained">Download as CSV</Button>
                        </div>
                        <div>
                            <GrantsFilter/>
                        </div>
                    </div>
                </div>
            </div>
        </Box>
    )
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);
        