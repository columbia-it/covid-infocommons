import SearchBar from './components/SearchBar';
import Box from '@mui/material/Box';
import React, { Component } from "react";
import { useParams } from 'react-router-dom'
import ModelSelect from './components/ModelSelect';

const Home = () => {
        const routeParams = useParams();
        return (
            <div className='root'>
                <SearchBar/>
                <div className='flex-container'>
                    <div className='flex-child'></div>
                    <ModelSelect
                        selected_model={0}/>
                </div>
            </div>
        )
    }

export default Home;