import * as React from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import RegExrEmbed from './RegExrEmbed';
import RegExperEmbed from './RegExperEmbed';
import GrexForm from './GrexForm';

export default function ToolAccordion(props) {
    return (
        <div>
            <Accordion disabled={props.enabledTool !== "regexr"} expanded={props.enabledTool === "regexr"}>
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
            <Accordion disabled={props.enabledTool !== "regexper"} expanded={props.enabledTool === "regexper"}>
                <AccordionSummary
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="panel3a-content"
                    id="panel3a-header"
                >
                    <Typography>RegExper</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <Typography variant="h6">DISCLAIMER: This tool classifies A&#123;5&#125; as 4 repetitions of 'A', but the javascript regexes we are using considers this 5 repetitions.  Mentally add one repetition to RegExper's interpretation!</Typography>
                    <RegExperEmbed></RegExperEmbed>
                </AccordionDetails>
            </Accordion>
            <Accordion disabled={props.enabledTool !== "grex"} expanded={props.enabledTool === "grex"}>
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
