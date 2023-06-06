import SearchBar from './components/SearchBar';
import Box from '@mui/material/Box';
import React, { Component } from "react";
import { useParams } from 'react-router-dom'
import { useNavigate } from "react-router-dom";
import NativeSelect from '@mui/material/NativeSelect';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';

//const navigate = useNavigate();

// function handleChange(event:any) {
//     console.log('//////')
//     console.log(event)
//     const params = new URLSearchParams(window.location.search)
//     console.log(params.get('keyword'))
//     let url = '/search/grants?keyword='+params.get('keyword')
//     navigate(url)
// }


const Home = () => {
        const navigate = useNavigate();

        const handleModelChange = (e:any) => {
            console.log(e.target.value)
            navigate('/search/grants')
        }

        const routeParams = useParams();
        console.log('****')
        console.log(routeParams)
        return (
            <div className='root'>
                {/* <Box
                    sx={{
                        width: '100%',
                        '& .MuiTextField-root': { width: '100%' },
                    }}
                    component="form"
                    noValidate
                    autoComplete="off"
                >      
                </Box> */}
                <SearchBar/>
                <div className='flex-container'>
                    <div className='flex-child'></div>
                    <div className='flex-child'>
                        <FormControl fullWidth>
                            <InputLabel variant="standard" htmlFor="uncontrolled-native">
                            </InputLabel>
                            <NativeSelect
                                defaultValue={30}
                                inputProps={{
                                    name: 'model',
                                    id: 'uncontrolled-native',
                                }}
                                onChange={ handleModelChange }
                            >
                                <option value={1}>All</option>
                                <option value={'grants'}>Grants</option>
                                <option value={'people'}>People</option>
                                <option value={'publications'}>Publications</option>
                                <option value={'datasets'}>Datasets</option>
                            </NativeSelect>
                        </FormControl>
                    </div>
                </div>
            </div>
        )
    }

export default Home;