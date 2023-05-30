import SearchBar from './components/SearchBar';
import Box from '@mui/material/Box';
import React, { Component } from "react";
import { useParams } from 'react-router-dom'

const Home = () => {
        const routeParams = useParams();
        console.log('****')
        console.log(routeParams)
        return (
            <div className='root'>
                <Box
                    sx={{
                        width: '100%',
                        '& .MuiTextField-root': { width: '100%' },
                    }}
                    component="form"
                    noValidate
                    autoComplete="off"
                >      
                </Box>
                <SearchBar/>
            </div>
        )
    }

export default Home;