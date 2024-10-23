// document.getElementById('commandForm').addEventListener('submit', async function(event) {
//     event.preventDefault();
//     const commandInput = document.getElementById('command');
//     const command = commandInput.value;

//     const response = await fetch('/run-command/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ command })
//     });

//     const result = await response.json();
//     const output = document.getElementById('output');
//     output.textContent = result.stdout || result.stderr || result.error;
// });
document.getElementById('commandForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const commandInput = document.getElementById('command');
    const command = commandInput.value;

    const response = await fetch('/run-command/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ command })
    });

    const result = await response.json();
    const output = document.getElementById('output');
    output.textContent = result.stdout || result.stderr || result.error;
});

