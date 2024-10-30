function switchDestinations() {
    const startingPoint = document.getElementById('starting-point');
    const targetDestination = document.getElementById('target-destination');

    // Get the current values
    const temp = startingPoint.innerText;
    startingPoint.innerText = targetDestination.innerText;
    targetDestination.innerText = temp;
}

function switchDestinations1() {
    const startingPoint1 = document.getElementById('starting-point1');
    const targetDestination1 = document.getElementById('target-destination1');

    // Get the current values
    const temp = startingPoint1.innerText;
    startingPoint1.innerText = targetDestination1.innerText;
    targetDestination1.innerText = temp;
}

function switchDestinations2() {
    const startingPoint2 = document.getElementById('starting-point2');
    const targetDestination2 = document.getElementById('target-destination2');

    // Get the current values
    const temp = startingPoint2.innerText;
    startingPoint2.innerText = targetDestination2.innerText;
    targetDestination2.innerText = temp;
}
