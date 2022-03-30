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
        numAttempts: -1,
        numChecks: -1,
        correct: false
    },
    control2: {
        timeToComplete: -1,
        numAttempts: -1,
        numChecks: -1,
        correct: false
    },
    control3: {
        timeToComplete: -1,
        numAttempts: -1,
        numChecks: -1,
        correct: false
    },
    explain1: {
        timeToComplete: -1,
        numAttempts: -1,
        numChecks: -1,
        correct: false
    },
    explain2: {
        timeToComplete: -1,
        numAttempts: -1,
        numChecks: -1,
        correct: false
    },
    explain3: {
        timeToComplete: -1,
        numAttempts: -1,
        numChecks: -1,
        correct: false
    },
    automata1: {
        timeToComplete: -1,
        numAttempts: -1,
        numChecks: -1,
        correct: false
    },
    automata2: {
        timeToComplete: -1,
        numAttempts: -1,
        numChecks: -1,
        correct: false
    },
    automata3: {
        timeToComplete: -1,
        numAttempts: -1,
        numChecks: -1,
        correct: false
    },
    code1: {
        timeToComplete: -1,
        numAttempts: -1,
        numChecks: -1,
        correct: false
    },
    code2: {
        timeToComplete: -1,
        numAttempts: -1,
        numChecks: -1,
        correct: false
    },
    code3: {
        timeToComplete: -1,
        numAttempts: -1,
        numChecks: -1,
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


/* Validator Functions */
function startupSaver(params: any[]): any {
    // Value to save
    let value = params[0];
    // Name of attribute to save to
    let attributeName = params[1];
    console.log("Saving startup " + attributeName + ": " + value.toString());
    submission.startup[attributeName] = value;

    // NOW: Fetch question sequence from server
    // TODO: Replace placeholder with actual sequence fetch
    // TODO: Make this custom validator async so it waits properly for completion before continuing
    let sequence = [[0, 1, 3, 2], [2, 0, 3, 1], [0, 3, 2, 1]];

    // The first array represents the order of string questions to present (control, explain, automata, code)
    for (let i = 0; i < sequence[0].length; i++) {
        // Replace placeholder with question
        surveyJson.pages[2 + (i * 3)] = regexJSON.string[i];
        // Add question name to validation call
        surveyJson.pages[2 + (i * 3)].validators[0].expression = surveyJson.pages[2 + (i * 3)].validators[0].expression
    }

    // The second array represents the order of create questions to present (control, explain, automata, code)
    for (let i = 0; i < sequence[1].length; i++) {
        surveyJson.pages[3 + (i * 3)] = regexJSON.create[i];
    }

    // The third array represents the order of update questions to present (control, explain, automata, code)
    for (let i = 0; i < sequence[2].length; i++) {
        surveyJson.pages[4 + (i * 3)] = regexJSON.update[i];
    }

    return true;
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

    /* NOTE: For this scenario it might not be enough to just test it against 1 string that
     * works. For example, if we want 4 capital letters, and the user's regex accepts Capital 
     * and lowercase letters, our string will pass. In this scenario we should also test
     * against a string that should fail and we can AND the conditions together to make sure 
     * works as expected. Also, if we never test if strings fail the user could put in a regex
     * that expects any character and it would always pass.
     */
    correctAnswer[questionNum] = (regex.test('87_REDP') && !(regex.test('32_flUX')) );

    /* Set data for logging */
    submission.control2.numAttempts = numAttempts[questionNum];
    //submission.control2.timeToComplete = survey.timeSpent();
    submission.control2.numChecks = 89; //not sure what numChecks is

    /* If we've reached max number of attempts return true */
    if( numAttempts[questionNum] >= MAX_ATTEMPTS ){
        return true;
    }

    /* Otherwise just return whether it was a match or not */
    return correctAnswer[questionNum];
}

// Register Validator standard functions
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
