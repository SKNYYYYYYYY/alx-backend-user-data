const keys = [ 'firstname', 'lastname', 'age', 'field' ]
const values = [
  [ 'Johann', 'Kerbrou', '30', 'CS' ],
  [ 'Guillaume', 'Salou', '30', 'SWE' ],
  [ 'Arielle', 'Salou', '20', 'CS' ],
  [ 'Jonathan', 'Benou', '30', 'CS' ],
  [ 'Emmanuel', 'Turlou', '40', 'CS' ],
  [ 'Guillaume', 'Plessous', '35', 'CS' ],
  [ 'Joseph', 'Crisou', '34', 'SWE' ],
  [ 'Paul', 'Schneider', '60', 'SWE' ],
  [ 'Tommy', 'Schoul', '32', 'SWE' ],
  [ 'Katie', 'Shirou', '21', 'CS' ]
]

// var fields = {}
// for(let i = 0; i<values.length;  i++) {
//     const field = values[i][3]
//     fields[field] = (fields[field] || 0)+1
// }
var students = values.map(row => Object.fromEntries(keys.map((key, i) => [key, row[i]])))
var fields = {}
for (let i=0; i<students.length; i++){
    const field = students[i]["field"]
    fields[field] = (fields[field] || 0)+1
}
console.log(fields)
