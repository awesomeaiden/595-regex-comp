function switcher() {
    if (this.data-name.substring(0, 4) === "grex") {
        console.log("grex question");
    } else if (this.data-name.substring(0, 7) === "explain") {
        console.log("explain question");
    } else if (this.data-name.substring(0, 8) === "automata") {
        console.log("automata question");
    }
}

let explainElement = document.getElementById("explain");
let automataElement = document.getElementById("automata");
let grexElement = document.getElementById("grex");

document.querySelector('div.sv-question').addEventListener('change', switcher);
console.log(explainElement);
console.log("HELLO THE SWITCHER IS RUNNING");
