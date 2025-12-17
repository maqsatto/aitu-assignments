const express = require('express')
const app = express()

const port = 3000

app.use(express.urlencoded({ extended: true }))

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html')
})

app.post('/calculate-bmi', (req, res) => {
    const weight = Number(req.body.weight)
    const heightCm = Number(req.body.height)

    if (weight <= 0 || heightCm <= 0) {
        return res.send('<h2>Invalid input. Weight and height must be positive.</h2><a href="/">Go back</a>')
    }

    const heightM = heightCm / 100
    const bmi = weight / (heightM * heightM)

    let category = ''
    let color = ''

    if (bmi < 18.5) {
        category = 'Underweight'
        color = 'orange'
    } else if (bmi < 24.9) {
        category = 'Normal weight'
        color = 'green'
    } else if (bmi < 29.9) {
        category = 'Overweight'
        color = 'gold'
    } else {
        category = 'Obese'
        color = 'red'
    }

    res.send(`
        <body>
            <div style="background-color: darkgrey; padding: 20px; width: 300px; margin: 50px auto; border-radius: 8px; text-align: center;">
                <h2>BMI Result</h2>
                <p><strong>BMI:</strong> ${bmi.toFixed(2)}</p>
                <p style="color:${color}; font-size: 20px;">
                    ${category}
                </p>
            </div>
        </body>
    `)
})

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`)
})
