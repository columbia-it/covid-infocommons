import ReactDOM from 'react-dom';
import "./main.css"
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import React, { Component } from "react";
import axios from "axios";
import DownloadIcon from '@mui/icons-material/Download';
import axiosRetry from 'axios-retry';

import Link from '@mui/material/Link';

// THIS FILE IS NOT USED TO DELIVER A PAGE
// It is only here to guarantee a central main.css file

axiosRetry(axios, {retries: 3});

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

interface HomeState {
    keyword: string
    url: string
}


let url = ''

if (process.env.NODE_ENV == 'production') {
    url = "https://cic-apps.datascience.columbia.edu";
} else if (process.env.NODE_ENV == 'development') {
    url = "https://cic-apps-dev.datascience.columbia.edu";
} else {
    url = "http://127.0.0.1:8000"
}

class App extends Component<any, HomeState> {
    state:HomeState = {
        keyword: this.props.keyword,
        url: ''
    }

    constructor(props:any) {
        super(props)
    }


    currentURL() {
	return window.location.href;
    }

    render() {
        return (
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
		<h1>Ceci n&apos;est pas une page</h1>
    </div>
  </Box>
  );
  }
  
  }
  
  const rootElement = document.getElementById("root");
  ReactDOM.render(<App />, rootElement);
        
