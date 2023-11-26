// //Pass data between js and python template

// const spawner = require('child_process').spawn; // spawner to transfer data

// const data = 'send this to python'; 

// const python_process = spawner('python',['.game/views.py', data])
//  //spawner(command that is going to run, ['python script location', 'data to send'])

// //callback function (trigger when data is returned)
// python_process.stdout.on("data", (data) => {
//     console.log("data Received from python:", data.toString());
// });

// // send an array -> stringify the data



// // Python script:
// // import sys #allow us to access the arguments passed in

// // data_to_pass_back = 'send this to node'
// // input = sys.argv[1]
// // output = data_to_pass_back
// // sys.stdout.flush()


// listButton = document.getElementById("listButton")
// listButton.addEventListener('click',() => {
//     listButton.style.
// })
