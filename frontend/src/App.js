import { useCallback } from "react";
import "survey-react/modern.min.css";
import { Survey, StylesManager, Model } from "survey-react";

StylesManager.applyTheme("modern");

let surveyJson = {
    title: "Regex Comprehension Study",
    showProgressBar: "bottom",
    showTimerPanel: "top",
    maxTimeToFinishPage: 180,
    maxTimeToFinish: 1000,
    firstPageIsStarted: true,
    startSurveyText: "Start Assessment",
    pages: [
        {
            "elements": [
                {
                    "type": "html",
                    "html": "" +
                        "You are about to start a brief assessment covering the use of regular expressions with and without assistive tools. " +
                        "<br/><br/>You will have 3 minutes to complete each question.  The entire quiz should take less than 15 minutes." +
                        "<br/><br/>Upon completion, you will be asked for an email address to be entered into a drawing for a $50 Amazon gift card, if you so choose!" +
                        "<br/><br/>The assessment will begin with a few basic questions about your existing skill and knowledge of regular expressions." +
                        "<br/><br/>Please click on <b>'Start Assessment'</b> when you are ready!"
                }
            ]
        }, {
            "elements": [
                {
                    type: "rating",
                    name: "familiarity",
                    title: "How would you rate your level of familiarity with regular expressions?",
                    minRateDescription: "Completely unfamiliar",
                    maxRateDescription: "Completely familiar",
                    "rateMin": 0,
                    "rateMax": 10
                },
                {
                    type: "rating",
                    name: "experience",
                    title: "How much prior experience do you have with regular expressions?",
                    minRateDescription: "Never worked with them",
                    maxRateDescription: "Extensive experience",
                    "rateMin": 0,
                    "rateMax": 10
                },
                {
                    type: "rating",
                    name: "skill",
                    title: "How would you rate your level of skill with regular expressions?",
                    minRateDescription: "Totally lost",
                    maxRateDescription: "I'm an expert",
                    "rateMin": 0,
                    "rateMax": 10
                }
            ]
        }, {
            "elements": [
                {
                    "type": "radiogroup",
                    "name": "libertyordeath",
                    "title": "Who said 'Give me liberty or give me death?'",
                    "choicesOrder": "random",
                    "choices": [
                        "John Hancock", "James Madison", "Patrick Henry", "Samuel Adams"
                    ],
                    "correctAnswer": "Patrick Henry"
                }
            ]
        }, {
            "elements": [
                {
                    "type": "text",
                    "name": "control",
                    "title": "Enter a string that fits this regular expression: '[0-9]*'",
                    "validators": [
                        {
                            type: "expression",
                            expression: "isMatch({control})",
                            text:"That string does not match the pattern."
                        }
                    ]
                }
            ]
        }
    ],
    completedHtml: "<h4>You have answered correctly <b>{correctedAnswers}</b> questions from <b>{questionCount}</b>.</h4>"
};

function isMatch(params: any[]): any {
    /*
    if (params.length < 1){
        return false;
    }
    */
    console.log("here");
    var self = this;
    let input_str = params[0];
    const regex = new RegExp('[0-9]*'); //Should fit any number
    self.returnResult( regex.test(input_str) ); //return result to library
    return false; //return value is ignored
}

/* This line is supposed to register the isMatch function with 
 * the SurveyJS library so that it can be used with the validator expression.
 * It currently breaks the code 
 */
//Survey.FunctionFactory.Instance.register("isMatch",isMatch);

function App() {
    const survey = new Model(surveyJson);
    survey.focusFirstQuestionAutomatic = false;

    const alertResults = useCallback((sender) => {
        const results = JSON.stringify(sender.data);
        alert(results);
    }, []);

    survey.onComplete.add(alertResults);

    return <Survey model={survey} />;
}

export default App;
