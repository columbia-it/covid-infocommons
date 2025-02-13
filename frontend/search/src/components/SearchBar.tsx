import React, { Component, useContext } from "react";
import TextField from '@mui/material/TextField';
//import { createContext } from "react";
import Box from '@mui/material/Box';
import { SearchContext } from '../search_context';

interface SearchState {
    keyword: string,
    search_in_progress: boolean,
    totalCount: number
}

class SearchBar extends React.Component<any, SearchState> {

    state:SearchState = {
        keyword: '',
        search_in_progress: false,
        totalCount: 0
    }

    enterHandler = (e:any) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            //this.get_grants_data()
        }
    }

    searchHandler = (event:any) => {
        event.preventDefault()
        const keyword = (document.getElementById('outlined-search') as HTMLInputElement).value;
        this.setState({'keyword': keyword})
    }

    render() {
        return (
      <div className='search_bar'>
                <Box
                    sx={{
                        width: '100%',
                        '& .MuiTextField-root': { width: '100%' },
                    }}
                    component="form"
                    noValidate
                    autoComplete="off"
                >      
                <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"></link>
                <TextField
                        id="outlined-search" 
                        label="Search" 
                        type="search"
                        value={ this.state.keyword }
                        onKeyDown={ this.enterHandler }
                        onChange={ this.searchHandler }/>
                {/* <form className='search-form'>
                    <TextField
                        id="outlined-search" 
                        label="Search" 
                        type="search"
                        value={ this.state.keyword }
                        onKeyDown={ this.enterHandler }
                        onChange={ this.searchHandler }/>
                </form> */}
                <br/>
                {/* <div className='flex-container'>
                    {
                    this.state.search_in_progress == false ? 
                        <div className='results-row'>
                                Showing <span style={{fontWeight: 'bold', color: '#000000'}}>{ this.state.totalCount }</span> results.
                        </div> 
                        : <div className='results-row'>Waiting for results...
                          </div> 
                    } 
                </div> */}
                </Box>
            </div>
            </SearchContext.Provider>
        );
    }   
}

export default SearchBar;
