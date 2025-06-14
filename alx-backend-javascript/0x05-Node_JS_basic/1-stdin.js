console.log("Welcome to ALX, what is your name?")

process.stdin.on('readable', function(){
var input = process.stdin.read()
if (input !== null){
    process.stdout.write("Your name is: " + input)
}
})
process.stdin.on('end', function() {
    console.log("This important software is now closing")
})
