import * as React from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import RegExrEmbed from './RegExrEmbed';
import RegExperEmbed from './RegExperEmbed';
import GrexForm from './GrexForm';

let regexrDisabled = false;
let regexperDisabled = false;
let grexDisabled = false;

export default function ToolAccordion() {
    return (
        <div>
            <Accordion disabled={regexrDisabled}>
                <AccordionSummary
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="panel2a-content"
                    id="panel2a-header"
                >
                    <Typography>RegExr</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <RegExrEmbed></RegExrEmbed>
                </AccordionDetails>
            </Accordion>
            <Accordion disabled={regexperDisabled}>
                <AccordionSummary
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="panel3a-content"
                    id="panel3a-header"
                >
                    <Typography>RegExper</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <RegExperEmbed></RegExperEmbed>
                </AccordionDetails>
            </Accordion>
            <Accordion disabled={grexDisabled}>
                <AccordionSummary
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="panel1a-content"
                    id="panel1a-header"
                >
                    <Typography>Grex</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <GrexForm></GrexForm>
                </AccordionDetails>
            </Accordion>
        </div>
    );
}
