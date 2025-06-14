const {spawn, execFileSync} = require('node:child_process')
const ls = spawn('ls')
const fs = require("fs")

function countStudents(filename) {
    ls.stdout.on('data', (data) => {
        const files = data.toString().split('\n')
        if (files.includes(filename)){
            try{
                var stdout = fs.readFileSync(filename)
                stdout = stdout.toString().split("\n").filter(line => line.trim())
                const keys = stdout[0].split(",")
                var values = []
                for(let i=1; i <stdout.length; i++) {
                    const details = stdout[i].split(',')
                    values.push(details)
                }
                var students = values.map(row => Object.fromEntries(keys.map((key, i) => [key, row[i]])))
            }
            catch(err) {
                console.log("" + err)
            }

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

        }
        else{
            throw new Error('Cannot load the database')
        }
    })
}
module.exports = countStudents