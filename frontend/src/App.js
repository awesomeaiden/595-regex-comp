import { useCallback } from "react";
import "survey-react/modern.min.css";
import { Survey, StylesManager, Model, FunctionFactory } from "survey-react";
import { v4 as uuidv4 } from 'uuid';
let startupJSON = require('./questions/startup.json');
let regexJSON = require('./questions/regex.json');

StylesManager.applyTheme("modern");

/* CONSTANTS */

/* Define the max number of attempts per question */
const MAX_ATTEMPTS = 10;

/* The total number of questions in the survey */
const NUM_QUESTIONS = 12;

/* GLOBALS */

/* Array to hold number of attempts each question took */
let numAttempts = new Array(NUM_QUESTIONS).fill(0);

/* Array to hold number of times user utilized comprehension tool */
let numChecks = new Array(NUM_QUESTIONS).fill(0);

let submission = {
    startup: {
        familiarity: -1,
        lastWorked: "",
        unique: "",
        longAgo: "",
        skill: -1,
        languages: ""
    },
    control1: {
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    control2: {
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    control3: {
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    explain1: {
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    explain2: {
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    explain3: {
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    automata1: {
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    automata2: {
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    automata3: {
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    code1: {
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    code2: {
        timeToComplete: -1,
        numAttempts: 0,
        numChecks: 0,
        correct: false
    },
    code3: {
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
                html: questionName + " placeholder"
            }
        ]
    }
}

let surveyJson = {
    title: "Regex Comprehension Study",
    showProgressBar: "bottom",
    showTimerPanel: "top",
    maxTimeToFinishPage: 180,
    maxTimeToFinish: 900,
    firstPageIsStarted: true,
    startSurveyText: "Start Assessment",
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
        }, {
            elements: [
                {
                    type: "html",
                    html: "The regular expression questions will now begin.  Please continue to initialize your survey and begin",
                    validators: [
                        {
                            type: "expression",
                            expression: "surveyInitializer()",
                            text: "Unable to initialize your survey!"
                        }
                    ]
                }
            ]
        },
        getPlaceholder("control1"),
        getPlaceholder("control2"),
        getPlaceholder("control3"),
        getPlaceholder("explain1"),
        getPlaceholder("explain2"),
        getPlaceholder("explain3"),
        getPlaceholder("automata1"),
        getPlaceholder("automata2"),
        getPlaceholder("automata3"),
        getPlaceholder("code1"),
        getPlaceholder("code2"),
        getPlaceholder("code3")
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

/* Validator Functions */
function surveyInitializer() {
    // Fetch optimal sequence of questions from backend
    // TODO: Replace placeholder with actual sequence fetch
    // TODO: Make this custom validator async so it waits properly for completion before continuing
    let sequence = [[0, 1, 3, 2], [2, 0, 3, 1], [0, 3, 2, 1]];

    let questionNames = Object.keys(submission);

    // The first array represents the order of string questions to present (control, explain, automata, code)
    for (let i = 0; i < sequence[0].length; i++) {
        // Replace placeholder with question
        surveyJson.pages[3 + (i * 3)] = regexJSON.string[i];
        // Add question name to validation call
        surveyJson.pages[3 + (i * 3)].validators[0].expression = addCallArg(surveyJson.pages[3 + (i * 3)].validators[0].expression, questionNames[1 + (i * 3)]);
    }

    // The second array represents the order of create questions to present (control, explain, automata, code)
    for (let i = 0; i < sequence[1].length; i++) {
        // Replace placeholder with question
        surveyJson.pages[4 + (i * 3)] = regexJSON.create[i];
        // Add question name to validation call
        surveyJson.pages[4 + (i * 3)].validators[0].expression = addCallArg(surveyJson.pages[4 + (i * 3)].validators[0].expression, questionNames[2 + (i * 3)]);
    }

    // The third array represents the order of update questions to present (control, explain, automata, code)
    for (let i = 0; i < sequence[2].length; i++) {
        // Replace placeholder with question
        surveyJson.pages[5 + (i * 3)] = regexJSON.update[i];
        // Add question name to validation call
        surveyJson.pages[5 + (i * 3)].validators[0].expression = addCallArg(surveyJson.pages[5 + (i * 3)].validators[0].expression, questionNames[3 + (i * 3)]);
    }

    return true;
}

function startupSaver(params: any[]): any {
    // Value to save
    let value = params[0];
    // Name of attribute to save to
    let attributeName = params[1];
    console.log("Saving startup " + attributeName + ": " + value.toString());
    submission.startup[attributeName] = value;
    return true;
}

function stringValidator(params: any[]): any {
    // First param is user's string
    let userString = new RegExp(params[0]);
    // Second param is regex to test on
    let regex = new RegExp(params[1]);
    // Last param is name of question (control1, explain3 etc)
    let questionName = params[params.length - 1];

    /* Set data for logging */
    submission[questionName].numAttempts += 1;
    //submission.control1.timeToComplete = survey.timeSpent();
    submission[questionName].numChecks = 54; //not sure what numChecks is
    submission[questionName].correct = regex.test(userString);

    /* If we've reached max number of attempts return true */
    if( submission[questionName].numAttempts >= MAX_ATTEMPTS ){
        return true;
    }

    /* Otherwise, just return whether it was a match or not */
    return submission[questionName].correct;
}

function regexValidator(params: any[]): any {
    // First param is user's regex
    let userRegex = new RegExp(params[0]);
    // Second param is "correct" regex to compare to
    let correctRegex = new RegExp(params[1]);
    // Rest of params (except for last param) are validation strings to check against
    let validationStrings = params.slice(2, params.length - 1);
    // Last param is name of question (control1, explain3 etc)
    let questionName = params[params.length - 1];

    let correct = true;
    for (let i = 0; i < validationStrings.length; i++) {
        if (userRegex.test(validationStrings[i]) !== correctRegex.test(validationStrings[i])) {
            correct = false;
        }
    }

    /* Set data for logging */
    submission[questionName].numAttempts += 1;
    //submission.control2.timeToComplete = survey.timeSpent();
    submission.control2.numChecks = 89; // TODO This is a placeholder

    /* If we've reached max number of attempts return true */
    if( submission[questionName].numAttempts >= MAX_ATTEMPTS ){
        return true;
    }

    /* Otherwise, just return whether it was a match or not */
    return correct;
}

// Register Validator standard functions
FunctionFactory.Instance.register("surveyInitializer", surveyInitializer);
FunctionFactory.Instance.register("startupSaver", startupSaver);
FunctionFactory.Instance.register("stringValidator", stringValidator);
FunctionFactory.Instance.register("regexValidator", regexValidator);

const survey = new Model(surveyJson);
function App() {
    survey.focusFirstQuestionAutomatic = false;

    const alertResults = useCallback((sender) => {
        const results = JSON.stringify(sender.data);
        alert(results);
    }, []);

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
                    "context": "explain",
                    "datapoint": submission.explain
                },
                {
                    "context": "automata",
                    "datapoint": submission.automata
                },
                {
                    "context": "code",
                    "datapoint": submission.code
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
        fetch('http://localhost:8000/log', postConfig).then(function(response) {
            // Check status
            console.log(response);
            options.showDataSavingSuccess();
        }).catch(function(error) {
            console.log(error);
            options.showDataSavingError("UNABLE TO SEND DATA! Please copy this data and send to gonza487@purdue.edu:\n" + JSON.stringify(dataToSend));
        });
    };

    survey.onComplete.add(alertResults);
    survey.onComplete.add(sendResults);

    return <Survey model={survey} />;
}

export default App;
