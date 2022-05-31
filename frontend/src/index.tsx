import ReactDOM from 'react-dom';
import "./main.css"
import GrantsTable from './components/GrantTable';
import { GrantsFilter } from './components/GrantsFilter';
import SearchBar from './components/SearchBar';
import { css, jsx, ThemeProvider } from '@emotion/react'
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { createTheme } from '@mui/material/styles';
import React, { Component } from "react";
import axios from "axios";
import DownloadIcon from '@mui/icons-material/Download';

const styles = {
  "&.MuiButton-root": {
    border: "2px black solid"
  },
  "&.MuiButton-text": {
    color: "grey"
  },
  "&.MuiButton-contained": {
      color: "red",
      backgroundColor: "yellow"
  },
  "&.MuiButton-outlined": {
    color: "brown"
  }
};

const theme = createTheme({
    palette: {
	primary: {
	    // light: will be calculated from palette.primary.main,
	    main: '#808000',
	    // dark: will be calculated from palette.primary.main,
	    // contrastText: will be calculated to contrast with palette.primary.main
	},
	secondary: {
	    light: '#800000',
	    main: '#800080',
	    // dark: will be calculated from palette.secondary.main,
	    contrastText: '#ffcc00',
	},
	// Used by `getContrastText()` to maximize the contrast between
	// the background and the text.
	contrastThreshold: 3,
	// Used by the functions below to shift a color's luminance by approximately
	// two indexes within its tonal palette.
	// E.g., shift from Red 500 to Red 300 or Red 700.
	tonalOffset: 0.2,
    },
    components: {
	// Name of the component
	MuiButton: {
	    styleOverrides: {		
		// Name of the slot
		contained: {
		    // Some CSS
		    fontSize: '1rem',
		    backgroundColor: "pink",
		    color: "green",
		},
	    },
	},
	// Name of the component
	MuiButtonBase: {
	    defaultProps: {
		// The props to change the default for.
		disableRipple: true, // No more ripple, on the whole application 💣!
	    },
	},
    },
});

interface Grant {
    id: number
    title: string
    award_amount: number
    abstract: string
    award_id: string
    pi: string
    funder_name: string
}

interface AppState {
    data: Grant[]
    url: string
    totalCount: number
    pageIndex: number
    awardee_org_names: string[]
}

class App extends Component<any, AppState> {
    state = {
        data: [],
        url: '',
        totalCount: 0,
        pageIndex: 0,
        awardee_org_names: []
    };

    componentDidMount = () => {
        this.get_grants_data('')
        this.get_org_name_facet()
    }

    searchHandler = (event:any) => {
        event.preventDefault()
        const keyword = (document.getElementById('outlined-search') as HTMLInputElement).value;
        this.setState({ url: this.get_url() })
        this.get_grants_data(keyword)
    };

    get_url = () => {
        let url = "";
        if (process.env.NODE_ENV == 'production') {
            url = "https://cic-apps.datascience.columbia.edu";
        } else if (process.env.NODE_ENV == 'development') {
            url = "https://cice-dev.paas.cc.columbia.edu";
        } else {
            url = "http://127.0.0.1:8000"
        }
        return url
    }

    get_org_name_facet() {
        var url = this.get_url().concat('/search/facets?field=awardee_organization.name')
        axios.get(url).then(results => {
            this.setState({ awardee_org_names: results.data.aggregations.patterns.buckets })
        })
    }

    get_grants_data = (keyword:string) => {
        var url = this.get_url().concat('/search/grants')
        if (keyword) {
            url = url.concat('?keyword=').concat(keyword)
        }
        
        axios.get(url).then(results => {
            this.setState({ totalCount: results.data.hits.total.value })

            var newArray = results.data.hits.hits.map(function(val:any) {
                var pi_name = ''
                var funder_name = ''
                if (val['_source']['principal_investigator'] != null) {
                    pi_name = val['_source']['principal_investigator']['first_name'] + ' ' + val['_source']['principal_investigator']['last_name']
                }
                return {
                    id: val['_source']['id'],
                    title: val['_source']['title'],
                    award_id: val['_source']['award_id'],
                    pi: pi_name,
                    abstract: val['_source']['abstract'],
                    award_amount: val['_source']['award_amount'],
                    funder_name: ('name' in val['_source']['funder']) ? val['_source']['funder']['name'] : ''
                }
            })
            this.setState({ data: newArray })
        })
    }

    downloadFile = (data:any, fileName:any, fileType:any) => {
        const blob = new Blob([data], { type: fileType })
        const a = document.createElement('a')
        a.download = fileName
        a.href = window.URL.createObjectURL(blob)
        const clickEvt = new MouseEvent('click', {
          view: window,
          bubbles: true,
          cancelable: true,
        })
        a.dispatchEvent(clickEvt)
        a.remove()
    }
      

    exportToCsv = (event:any) => {
        event.preventDefault()
        // Headers for each column
        let headers = ['Id,Title,Award_Amount,Award_ID,PI,Abstract,Funder']
        // Convert grants data to csv
        let grantsCsv = this.state.data.reduce((acc:any, grant:any) => {
            const grant_to_add:Grant = grant
            acc.push([
                grant_to_add.id,
                grant_to_add.title, 
                grant_to_add.award_amount,
                grant_to_add.award_id,
                grant_to_add.pi,
                grant_to_add.abstract,
                grant_to_add.funder_name
            ]
            .join(','))
            return acc
        }, [])
        this.downloadFile([...headers, ...grantsCsv].join('\n'), 'grants.csv', 'text/csv')
    }

    enterHandler = (e:any) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            const keyword = (document.getElementById('outlined-search') as HTMLInputElement).value;
            this.setState({ url: this.get_url() })
            this.get_grants_data(keyword)
        }
    }

    render() {
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
		 <ThemeProvider theme={theme}>
                    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"></link>
                    <form className='search-form'>
                        <TextField
                            id="outlined-search" 
                            label="Search" 
                            type="search" 
                            onKeyDown={ this.enterHandler }/>
                        <Button 
                            onClick={ this.searchHandler } 
                            className='search-button'
                            variant="contained">Search</Button>
                    </form>
                    <br/>
                    <br/>
                    <div className='flex-container'>
                        <div className='flex-child'>
                            <GrantsTable
                                totalCount={ this.state.totalCount } 
                                data={ this.state.data} 
                                url={ this.state.url }
                                //pageIndex={ this.state.pageIndex }
                            />
                        </div>
                        <div className='flex-child'>
                <div className='download-csv'>
		<Button variant='outlined'
	                sx={{ color: 'yellow', backgroundColor: 'orange', borderColor: 'green' }}
		        >
		SXA Button
	    </Button>
		//JSX
		<Button
	    //just an example...better to use the const above
	    sx={{
		"&.MuiButton-text": { color: "#808080" },
		border: "2px black solid"
	    }}
	    variant="text"
	    
		>
		Text
	    </Button>
		<Button sx={styles} variant="contained">
		Contained
	    </Button>
		<Button sx={styles} variant="outlined">
		Outlined
	    </Button>
		<Button color="primary" className='download-button' variant="contained" sx={{ backgroundColor: 'green' }}>P button</Button>
		<Button color="secondary" className='download-button' variant="contained">S button</Button>
		<Button className='download-button' variant="contained" sx={{ backgroundColor: 'green', color: 'yellow' }}>SX button</Button>
                                <Button onClick={ this.exportToCsv } 
                                        className='download-button' 
            variant="contained"
	    color="primary"
                                        endIcon={ <DownloadIcon /> }>Download Results as CSV
                                </Button>
                            </div>
                            <div>
                                <GrantsFilter
                                    awardee_org_names={ this.state.awardee_org_names }
                                    />
                            </div>
                        </div>
                </div>
		</ThemeProvider>
                </div>
            </Box>
        );
    }
    
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);
        
