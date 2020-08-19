const { 
    series, parallel, watch,
    src, dest} = require('gulp')
const settings = require('./project-settings.json')
const ftp = require('vinyl-ftp')
const merge = require('merge-stream')
const {argv} = require('yargs')

function connectToPi(target){
    const conn = ftp.create({
        host:     settings[target].ip,
        user:     settings[target].user,
        password: settings[target].password,
    })
    return conn
}

function copyToPi(target){
    
    const conn = connectToPi(target)

    return src('./virtual/' + target + '/MyScripts/**')
        .pipe(conn.newer('/home/pi/MyScripts/'))
        .pipe(conn.dest('/home/pi/MyScripts/'))
}

function initPis(){

    const hasArguments = Object.keys(argv).length > 2
    if (hasArguments){
        if (argv.input){
            // only do input pi
        } else if (argv.output){
            // only do output pi
        }
    } else {
        console.log("Ahaha! Nothing at all!")
    }
}

function initPi(target){
    const conn = connectToPi(target)
    return src("./virtual/" + target +"/*")
    .pipe(conn.dest("/home/pi"))
}

// TODO: Make async somehow
function cleanPi(target){
    const conn = connectToPi(target)
    conn.clean(["/home/pi/MyPics/**"])
}

function deployToPi(target){
   return copyToPi(target)
}

function defaultTask(cb) {
    cb();
}

function watchScripts(){
    watch("./virtual/**/*.py", deployToInputPi)
}
  
exports.default = defaultTask
exports.deploy = deployToInputPi
exports.watch = watchScripts
//TODO: Make clean task
//exports.clean = parallel()
//TODO: Make init task + vargs "--input , --output"
exports.init = initPis
