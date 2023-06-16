import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from './home';
import Grants from './grants_index';
import People from './people_index';
import Publications from "./publications_index";
import Datasets from "./datasets_index";
import { SearchContext } from "./search_context";
import React, { useState, Component } from "react";
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';

interface AppState {
  keyword: string
}

class App extends Component<any, AppState> {
    
    state:AppState = {
      keyword: ''
    }

    constructor(props:any) {
      super(props)
    }

    searchHandler = (event:any) => {
      event.preventDefault()
      const keyword = (document.getElementById('outlined-search') as HTMLInputElement).value;
      this.setState({'keyword': keyword})
      console.log(this.state.keyword)
    }

    render() {
      return (
        <div>
          <Box
            sx={{
              width: '100%',
                    '& .MuiTextField-root': { width: '100%' },
              }}
            component="form"
            noValidate
            autoComplete="off"
          >
          <div className='root'>
            <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"></link>
            <form className='search-form'>
              <TextField
                id="outlined-search" 
                label="Search" 
                type="search"
                value={ this.state.keyword }
                //onKeyDown={ this.enterHandler }
                onChange={ this.searchHandler }
                //onChange={(e) => this.searchHandler(e) }
              />
            </form>
            <Routes>
              <Route path="/search" element={
                <SearchContext.Provider value={ {keyword: this.state.keyword} }>
                  <Home />
                </SearchContext.Provider>
              } />
              <Route path="/search/grants" element={
                <SearchContext.Provider value={ {keyword: this.state.keyword} }>
                  <Grants />
                </SearchContext.Provider>
              } />
              <Route path="/search/people" element={<People />} />
              <Route path="/search/publications" element={<Publications />} />
              <Route path="/search/datasets" element={<Datasets />} />
            </Routes>
            </div>
          </Box>
        </div>
    )};
}

export default App;