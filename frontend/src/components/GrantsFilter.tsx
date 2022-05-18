import * as React from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import { Button, TextField } from "@material-ui/core";
import { Box, ThemeProvider, createTheme } from '@mui/system';
import { spacing } from '@mui/system';

export default function GrantsFilter() {
  const [expanded, setExpanded] = React.useState<string | false>(false);

  const handleChange =
    (panel: string) => (event: React.SyntheticEvent, isExpanded: boolean) => {
      setExpanded(isExpanded ? panel : false);
    };
      

  return (
    <Card sx={{ width: '100%' }}>
        <CardContent>
            <div className="filter-button-div">
                <label className="filter-results-label">Filter Results</label>
                <Button 
                    variant='contained'>Clear Filter
                </Button>
            </div>
            <div>
                <Accordion>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel1a-content"
                        id="panel1a-header"
                    >
                        <Typography sx={{ px: 2 }}>Directorate</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <TextField variant='outlined' label='Type directorate title'>
                        </TextField>
                    </AccordionDetails>
                </Accordion>
                <Accordion>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel2a-content"
                        id="panel2a-header"
                    >
                        <Typography sx={{ px: 2 }}>Division</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <TextField variant='outlined' label='Type division title'>
                        </TextField>
                    </AccordionDetails>
                </Accordion>
                <Accordion>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel3a-content"
                        id="panel3a-header"
                    >
                        <Typography sx={{ px: 2 }}>Awardee Organizaion</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <TextField variant='outlined' label='Type institution name'>
                        </TextField>
                    </AccordionDetails>
                </Accordion>
                <Accordion>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel4a-content"
                        id="panel4a-header"
                    >
                        <Typography sx={{ px: 2 }}>State/Territory</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Typography>
                            Textfield goes here
                        </Typography>
                    </AccordionDetails>
                </Accordion>
                <Accordion>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel5a-content"
                        id="panel5a-header"
                    >
                        <Typography sx={{ px: 2 }}>PI Name</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <TextField variant='outlined' label='Type PI name'>
                        </TextField>
                    </AccordionDetails>
                </Accordion>
                <Accordion>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel6a-content"
                        id="panel6a-header"
                    >
                        <Typography sx={{ px: 2 }}>Program Officer/Official</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <TextField variant='outlined' label='Type Keywords'>
                        </TextField>
                    </AccordionDetails>
                </Accordion>
                <Accordion>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel7a-content"
                        id="panel7a-header"
                    >
                        <Typography sx={{ px: 2 }}>Start/End Date</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Typography>
                            Textfield goes here
                        </Typography>
                    </AccordionDetails>
                </Accordion>
            </div>
        </CardContent>
    </Card>
  );
}
