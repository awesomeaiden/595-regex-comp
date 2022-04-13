import {useCallback, useEffect, useState} from "react";
import "survey-react/modern.min.css";
import { Survey, StylesManager, Model, FunctionFactory} from "survey-react";
import { v4 as uuidv4 } from 'uuid';
let startupJSON = require('./questions/startup.json');
let regexJSON = require('./questions/regex.json');
let toolsJSON = require('./questions/tools.json');
require('./questions/grex.js');

StylesManager.applyTheme("modern");

/* CONSTANTS */

/* Define the max number of attempts per question */
const MAX_ATTEMPTS = 10;

/* The total number of questions in the survey */
const NUM_QUESTIONS = 12;

/* Max time user can spend on a single page/question */
const MAX_TIME_PER_PAGE = 150; //2.5 minutes

/* Max time for survey, based on number of questions * time per question */
const MAX_TIME_FOR_SURVEY = 1950; //32.5 minutes

/* GLOBALS */

/* Array to hold number of attempts each question took */
let numAttempts = new Array(NUM_QUESTIONS).fill(0);

/* Array to hold number of times user utilized comprehension tool */
let numChecks = new Array(NUM_QUESTIONS).fill(0);

let submission = {
    startup: {
        skill: -1,
        lastWorked: "",
        uniqueRegexes: "",
        longAgo: "",
        languages: ""
    },
    control1: {
        questionName: "",
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    control2: {
        questionName: "",
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    control3: {
        questionName: "",
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    explain1: {
        questionName: "",
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    explain2: {
        questionName: "",
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    explain3: {
        questionName: "",
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    automata1: {
        questionName: "",
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    automata2: {
        questionName: "",
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    automata3: {
        questionName: "",
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    grex1: {
        questionName: "",
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    grex2: {
        questionName: "",
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    grex3: {
        questionName: "",
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    }
}

let raffleEmail = "N/A";

function getPlaceholder(questionName) {
    return {
        elements: [
            {
                type: "html",
                html: questionName + " placeholder",
                name: questionName
            }
        ]
    }
}

let surveyJson = {
    title: "Regex Comprehension Study",
    showProgressBar: "bottom",
    showTimerPanel: "top",
    maxTimeToFinishPage: MAX_TIME_PER_PAGE,
    maxTimeToFinish: MAX_TIME_FOR_SURVEY,
    firstPageIsStarted: true,
    startSurveyText: "Start Assessment",
    questionCount: NUM_QUESTIONS,
    pages: [
        {
            elements: [
                {
                    type: "html",
                    html: "" +
                        "You are about to start a brief assessment covering the use of regular expressions with and without assistive tools. " +
                        "<br/><br/>You will have 2.5 minutes to complete each question.  The entire quiz should take around 20 minutes." +
                        "<br/><br/>Upon completion, you will be asked for an email address to be entered into a drawing for a $50 Amazon gift card, if you so choose!" +
                        "<br/><br/>The assessment will begin with a few basic questions about your existing skill and knowledge of regular expressions." +
                        "<br/><br/>Please click on <b>'Start Assessment'</b> when you are ready!"
                }
            ]
        }, {
            elements: startupJSON
        },
        getPlaceholder("control1"),
        getPlaceholder("control2"),
        getPlaceholder("control3"),
        {
            elements: [
                {
                    type: "html",
                    html: "For the next three problems, you will have access to a regex explanation tool." +
                        "<br/><br/>This tool will take in a regular expression and break it down into its components to make it more understandable."
                }
            ]
        },
        getPlaceholder("explain1"),
        getPlaceholder("explain2"),
        getPlaceholder("explain3"),
        {
            elements: [
                {
                    type: "html",
                    html: "For the next three problems, you will have access to a regex diagramming tool." +
                        "<br/><br/>This tool will take in a regular expression and generate a NFA diagram to represent it."
                }
            ]
        },
        getPlaceholder("automata1"),
        getPlaceholder("automata2"),
        getPlaceholder("automata3"),
        {
            elements: [
                {
                    type: "html",
                    html: "For the next three problems, you will have access to a regex generation tool." +
                        "<br/><br/>This tool will take in a list of example strings and generate a regular expression that accepts those strings (and generally nothing else, but the tool is imperfect)."
                }
            ]
        },
        getPlaceholder("grex1"),
        getPlaceholder("grex2"),
        getPlaceholder("grex3")
    ],
    completedHtml: "<h4>You have answered correctly <b>{correctedAnswers}</b> questions from <b>{questionCount}</b>.</h4>"
};

// Function to add an argument to a function call (written in a string)
function addCallArg(functionString, argString) {
    // First split the string up
    let callArray = functionString.split('');

    // Now insert argString before last ')'
    callArray.splice(callArray.length - 1, 0, ", " + argString);

    // Finally, join the string array back into a string
    let finalString = callArray.join('');

    return finalString;
}

function surveyInitializer() {
    return new Promise((resolve) => {
        // Fetch optimal sequence of questions from backend
        const getConfig = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        };
        fetch('http://localhost:8000/sequence', getConfig).then(async function(response) {
            // Check status
            response = await response.json();
            let sequence = response.sequence;
            console.log(sequence);
            let questionNames = Object.keys(submission);

            // The first array represents the order of string questions to present (control, explain, automata, grex)
            for (let i = 0; i < sequence[0].length; i++) {
                // Replace placeholder with question in JSON
                surveyJson.pages[2 + (i * 4)] = {
                    elements: [regexJSON.string[sequence[0][i]], toolsJSON.grex]
                };

                // Add question name to validation call
                surveyJson.pages[2 + (i * 4)].elements[0].validators[0].expression = addCallArg(surveyJson.pages[2 + (i * 4)].elements[0].validators[0].expression, questionNames[1 + (i * 3)]);
                // Add question name to submission
                submission[questionNames[1 + (i * 3)]].questionName = regexJSON.string[sequence[0][i]].name
            }

            // The second array represents the order of create questions to present (control, explain, automata, grex)
            for (let i = 0; i < sequence[1].length; i++) {
                // Replace placeholder with question
                surveyJson.pages[3 + (i * 4)] = {
                    elements: [regexJSON.create[sequence[1][i]]]
                };
                // Add question name to validation call
                surveyJson.pages[3 + (i * 4)].elements[0].validators[0].expression = addCallArg(surveyJson.pages[3 + (i * 4)].elements[0].validators[0].expression, questionNames[2 + (i * 3)]);
                // Add question name to submission
                submission[questionNames[2 + (i * 3)]].questionName = regexJSON.create[sequence[1][i]].name
            }

            // The third array represents the order of update questions to present (control, explain, automata, grex)
            for (let i = 0; i < sequence[2].length; i++) {
                // Replace placeholder with question
                surveyJson.pages[4 + (i * 4)] = {
                    elements: [regexJSON.update[sequence[2][i]]]
                };
                // Add question name to validation call
                surveyJson.pages[4 + (i * 4)].elements[0].validators[0].expression = addCallArg(surveyJson.pages[4 + (i * 4)].elements[0].validators[0].expression, questionNames[3 + (i * 3)]);
                // Add question name to submission
                submission[questionNames[3 + (i * 3)]].questionName = regexJSON.update[sequence[2][i]].name
            }

            console.log(surveyJson);

            resolve(new Model(surveyJson));
        }).catch(function(error) {
            console.log(error);
            resolve(false);
        });
    });
}

/* Validator Functions */
function startupSaver(params: any[]): any {
    // Value to save
    let value = params[0];
    // Name of attribute to save to
    let attributeName = params[1];
    submission.startup[attributeName] = value;
    return true;
}

// To help prevent duplicate submission of results
let submitted = false;

// Initialize survey
function App() {

    useEffect(() => {
        document.title = "Regex Comprehension Study";
    }, []);

    const [survey, setSurvey] = useState(null);

    useEffect(() => {
        surveyInitializer().then((newSurvey) => {
            setSurvey(newSurvey);
        });
    }, []);

    if (survey) {
        function stringValidator(params: any[]): any {
            // First param is user's string
            let userString = params[0];
            // Second param is regex to test on
            let regex = new RegExp(params[1]);
            // Last param is context of question (control1, explain3 etc)
            let context = params[params.length - 1];

            //TODO: Remove
            console.log("userString: " + userString);
            console.log(regex);
            console.log("context: " + context);
            console.log("timeToComplete: " + survey.currentPage.timeSpent);

            /* Set data for logging */
            submission[context].numAttempts += 1;
            submission[context].timeToComplete = survey.currentPage.timeSpent;
            submission[context].numChecks = 54; //TODO: This is a placeholder
            submission[context].correct = regex.test(userString);

            /* If we've reached max number of attempts return true */
            if( submission[context].numAttempts >= MAX_ATTEMPTS ){
                return true;
            }
            /* If we are past the time limit, advance to the next question */
            else if( survey.currentPage.timeSpent > MAX_TIME_PER_PAGE ){
                return true;
            }

            /* Otherwise, just return whether it was a match or not */
            return submission[context].correct;
        }

        function regexValidator(params: any[]): any {
            // TODO If time limit is violated, don't return false - needs to allow survey to continue
            // Ensure user regex string begins with ^ and $

            if (params[0].charAt(0) !== '^') {
                params[0] = "^" + params[0];
            }
            if (params[0].charAt(params[0].length - 1) !== '$') {
                params[0] = params[0] + "$";
            }
            // First param is user's regex
            let userRegex;
            try {
                userRegex = new RegExp(params[0]);
            } catch (error) {
                alert(error);
                return false;
            }
            // Second param is "correct" regex to compare to
            let correctRegex = new RegExp(params[1]);
            // Rest of params (except for last param) are validation strings to check against
            let validationStrings = params.slice(2, params.length - 1);
            // Last param is context of question (control1, explain3 etc)
            let context = params[params.length - 1];

            //TODO: Remove
            console.log(userRegex);
            console.log(correctRegex);
            console.log(context);
            console.log("timeToComplete: " + survey.currentPage.timeSpent);

            let correct = true;
            for (let i = 0; i < validationStrings.length; i++) {
                if (userRegex.test(validationStrings[i]) !== correctRegex.test(validationStrings[i])) {
                    correct = false;
                    console.log(validationStrings[i]);
                    console.log(userRegex.test(validationStrings[i]));
                    console.log(correctRegex.test(validationStrings[i]));
                }
            }

            /* Set data for logging */
            submission[context].numAttempts += 1;
            submission[context].timeToComplete = survey.currentPage.timeSpent;
            submission[context].numChecks = 89; // TODO This is a placeholder

            /* If we've reached max number of attempts return true */
            if( submission[context].numAttempts >= MAX_ATTEMPTS ){
                return true;
            }
            /* If we are past the time limit, advance to the next question */
            else if( survey.currentPage.timeSpent > MAX_TIME_PER_PAGE ){
                return true;
            }

            /* Otherwise, just return whether it was a match or not */
            submission[context].correct = correct;
            return correct;
        }

        survey.focusFirstQuestionAutomatic = false;

        // Register Validator standard functions
        FunctionFactory.Instance.register("startupSaver", startupSaver);
        FunctionFactory.Instance.register("stringValidator", stringValidator);
        FunctionFactory.Instance.register("regexValidator", regexValidator);

        const sendResults = function (sender, options) {
            // Show message about saving results
            options.showDataSaving();

            // Parse survey data into proper format
            let dataToSend = {
                "participantID": uuidv4(),
                "payloads": [
                    {
                        "context": "startup",
                        "datapoint": submission.startup
                    },
                    {
                        "context": "control1",
                        "datapoint": submission.control1
                    },
                    {
                        "context": "control2",
                        "datapoint": submission.control2
                    },
                    {
                        "context": "control3",
                        "datapoint": submission.control3
                    },
                    {
                        "context": "explain1",
                        "datapoint": submission.explain1
                    },
                    {
                        "context": "explain2",
                        "datapoint": submission.explain2
                    },
                    {
                        "context": "explain3",
                        "datapoint": submission.explain3
                    },
                    {
                        "context": "automata1",
                        "datapoint": submission.automata1
                    },
                    {
                        "context": "automata2",
                        "datapoint": submission.automata2
                    },
                    {
                        "context": "automata3",
                        "datapoint": submission.automata3
                    },
                    {
                        "context": "grex1",
                        "datapoint": submission.grex1
                    },
                    {
                        "context": "grex2",
                        "datapoint": submission.grex2
                    },
                    {
                        "context": "grex3",
                        "datapoint": submission.grex3
                    }
                ],
                "timestamp": Date.now()
            };

            const postConfig = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dataToSend)
            };
            if (!submitted) {
                submitted = true;
                fetch('http://localhost:8000/log', postConfig).then(function (response) {
                    // Check status
                    console.log(response);
                    options.showDataSavingSuccess();
                }).catch(function (error) {
                    console.log(error);
                    options.showDataSavingError("UNABLE TO SEND DATA! Please copy this data and send to gonza487@purdue.edu:\n" + JSON.stringify(dataToSend));
                });
            }
        };

        survey.onComplete.add(sendResults);

        return (
            <div>
                <Survey model={survey}></Survey>
                {/*<script type="text/javascript" src="switcher.js"></script>*/}
            </div>
        );
    }

    return <div>Awaiting connection to backend... Refresh to retry!</div>;
}

export default App;
