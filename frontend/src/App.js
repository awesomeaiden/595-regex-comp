import { useCallback } from "react";
import "survey-react/modern.min.css";
import { Survey, StylesManager, Model, FunctionFactory } from "survey-react";
import { v4 as uuidv4 } from 'uuid';

StylesManager.applyTheme("modern");

/* CONSTANTS */

/* Define the max number of attempts per question */
const MAX_ATTEMPTS = 3;

/* The total number of questions in the survey */
const NUM_QUESTIONS = 12;


/* GLOBALS */

/* Array to hold number of attempts each question took */
var numAttempts = new Array(NUM_QUESTIONS).fill(0);

/* Array to hold whether the user got the correct answer 
 * or not for that question */
var correctAnswer = new Array(NUM_QUESTIONS).fill(false);

let submission = {
    startup: {
        familiarity: -1,
        experience: -1,
        skill: -1
    },
    control: {
        timeToComplete: -1,
        numAttempts: -1,
        numChecks: -1
    },
    explain: {
        timeToComplete: -1,
        numAttempts: -1,
        numChecks: -1
    },
    automata: {
        timeToComplete: -1,
        numAttempts: -1,
        numChecks: -1
    },
    code: {
        timeToComplete: -1,
        numAttempts: -1,
        numChecks: -1
    }
}

let raffleEmail = "N/A";

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
                        "<br/><br/>You will have 3 minutes to complete each question.  The entire quiz should take less than 15 minutes." +
                        "<br/><br/>Upon completion, you will be asked for an email address to be entered into a drawing for a $50 Amazon gift card, if you so choose!" +
                        "<br/><br/>The assessment will begin with a few basic questions about your existing skill and knowledge of regular expressions." +
                        "<br/><br/>Please click on <b>'Start Assessment'</b> when you are ready!"
                }
            ]
        }, {
            elements: [
                {
                    type: "rating",
                    name: "familiarity",
                    title: "How would you rate your level of familiarity with regular expressions?",
                    minRateDescription: "Completely unfamiliar",
                    maxRateDescription: "Completely familiar",
                    rateMin: 0,
                    rateMax: 10,
                    isRequired: true
                },
                {
                    type: "rating",
                    name: "experience",
                    title: "How much prior experience do you have with regular expressions?",
                    minRateDescription: "Never worked with them",
                    maxRateDescription: "Extensive experience",
                    rateMin: 0,
                    rateMax: 10,
                    isRequired: true
                },
                {
                    type: "rating",
                    name: "skill",
                    title: "How would you rate your level of skill with regular expressions?",
                    minRateDescription: "Totally lost",
                    maxRateDescription: "I'm an expert",
                    rateMin: 0,
                    rateMax: 10,
                    isRequired: true
                }
            ]
        }, {
            elements: [
                {
                    type: "text",
                    name: "control",
                    title: "Enter a string that fits this regular expression: '^[0-9]*$'",
                    validators: [
                        {
                            type: "expression",
                            expression: "isMatch({control})",
                            text: "That string does not match the pattern."
                        }
                    ],
                    isRequired: true
                }
            ]
        }
    ],
    completedHtml: "<h4>You have answered correctly <b>{correctedAnswers}</b> questions from <b>{questionCount}</b>.</h4>"
};

function isMatch(params: any[]): any {
    let questionNum = 0;
    numAttempts[questionNum]++;
    let input_str = params[0];
    const regex = new RegExp(/^[0-9]*$/); // Should fit any number of digits 0-9 ('3426', '2', '3512317433' etc)
    correctAnswer[0] = regex.test(input_str);

    /* Set data for logging */
    submission.control.numAttempts = numAttempts[questionNum];
    //submission.control.timeToComplete = survey.timeSpent();
    submission.control.numChecks = 54; //not sure what numChecks is
    
    /* If we've reached max number of attempts return true */
    if( numAttempts[questionNum] >= MAX_ATTEMPTS ){
        return true;
    }
    
    /* Otherwise just return whether it was a match or not */
    return correctAnswer[0];
}

// Register isMatch standard function
FunctionFactory.Instance.register("isMatch", isMatch);

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
                    "context": "control",
                    "datapoint": submission.control
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
