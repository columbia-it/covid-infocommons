import ReactDOM from 'react-dom';
import "./main.css"
import GrantsTable from './components/GrantTable';
import SearchBar from './components/SearchBar';
import { GrantsFilter, Facet } from './components/GrantsFilter';
import Box from '@mui/material/Box';
import Layout from './layout';
import Home from './home';
import Grants from './grants_index';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import React, { Component } from "react";
import axios from "axios";
import DownloadIcon from '@mui/icons-material/Download';
import axiosRetry from 'axios-retry';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import App from './app';

ReactDOM.render(
    <Router>
      <App/>
    </Router>,
    document.getElementById('root')
)
        
