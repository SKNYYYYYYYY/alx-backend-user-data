const {spawn} = require("node:child_process")
const ls = spawn('ls')
const fs = require("fs")
function countStudents(filename) {
    return new Promise ((resolve) => {
        let output = '';
        ls.stdout.on("data", (data) => {
            output += data.toString();
        })
        ls.stderr.on('data', (err) => {
            rejects(new Error('Failed to list directory'))
        })
        ls.on('close', () => {
            const files = output.split("\n")
            if (files.includes(filename)){
                const dbText = fs.readFile(filename, (err, data) => {
                    if (err) {
                       return console.error(err)
                    }
                const stdout = data.toString().split('\n').filter(line => line.trim())
                const keys = stdout[0].split(",")
                var values = []
                for(let i=1; i <stdout.length; i++) {
                    const details = stdout[i].split(',')
                    values.push(details)
                }
                var students = values.map(row => Object.fromEntries(keys.map((key, i) => [key, row[i]])))

                const total_students = students.length
                console.log("Number of students: " + total_students)

                var fields = {}
                for(let i=0; i<students.length;i++){
                    const field = students[i]["field"]
                    fields[field] = (fields[field] || 0) + 1
                }
                const CS_num = fields['CS']
                const SWE_num = fields['SWE']

                const field_students = (field) => {
                    var list = []
                    for (let student of students){
                        if (student["field"] == field){
                            list.push(student["firstname"])
                        }
                    }
                    return list.join(', ')
                    }

                console.log("Number of students in CS: " + CS_num + ". " + "List: " + field_students("CS"))
                console.log("Number of students in SWE: " + SWE_num + ". " + "List: " + field_students("SWE"))
                resolve()
                })
            }
            else {
                throw new Error("Cannot load the database")
            }
        })
    })
}
module.exports = countStudents
