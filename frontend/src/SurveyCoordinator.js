import {useCallback, useEffect, useState} from "react";
import App from './App';
import ToolAccordion from "./ToolAccordion";

export default function SurveyCoordinator() {
    const [enabledTool, setEnabledTool] = useState("");

    return (
        <div>
            <App setEnabledTool={setEnabledTool}/>
            <ToolAccordion enabledTool={enabledTool}/>
        </div>
    );
}
