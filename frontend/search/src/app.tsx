import { Component } from "react";
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from './home';
import Grants from './grants_index';
import People from './people_index';
import Publications from './publications_index';
import Datasets from './datasets_index';

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

  enterHandler = (e:any) => {
    if (e.key === 'Enter') {
        e.preventDefault();
    }
  }

  searchHandler = (event:any) => {
    event.preventDefault()
    const keyword = (document.getElementById('outlined-search') as HTMLInputElement).value;
    this.setState({'keyword': keyword})
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
            autoComplete="off">
          <div className='root'>
            <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"></link>
            <TextField
                id="outlined-search" 
                label="Search" 
                type="search"
                value={ this.state.keyword }
                onKeyDown={ this.enterHandler }
                onChange={ this.searchHandler }
            />
            <br/>
            <Routes>
              <Route path="/search" element={
                <Home 
                    keyword={ this.state.keyword }
                />
              }/>
              <Route path="/search/grants" element={
                  <Grants 
                    keyword={ this.state.keyword }
                  />
              } />
              <Route path="/search/people" element={
                  <People 
                    keyword={ this.state.keyword }
                  />
              } />
              <Route path="/search/publications" element={
                  <Publications 
                    keyword={ this.state.keyword }
                  />
              } />
              <Route path="/search/datasets" element={
                  <Datasets 
                    keyword={ this.state.keyword }
                  />
              } />
            </Routes>
          </div>
        </Box>
      </div>
    )}
}

export default App;
