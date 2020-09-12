const { 
    series, parallel, watch,
    src, dest} = require('gulp')
const settings = require('./project-settings.json')
const ftp = require('vinyl-ftp')
const merge = require('merge-stream')
const {argv} = require('yargs')

// Used to redirect tasks based on additional arguments, two input or output pi or both
function targetPiByArgs(task){
    const hasArguments = Object.keys(argv).length > 2
    if (hasArguments){
        if (argv.input){
           return task('input-pi')
        } else if (argv.output){
           return task('output-pi')
        }
    } else {
        return mergeStream(task('input-pi'), task('output-pi'))
    }
}

// Tasks by Target

function connectToPi(target){
    const conn = ftp.create({
        host:     settings[target].ip,
        user:     settings[target].user,
        password: settings[target].password,
    })
    return conn
}

function initPi(target){
    console.log("Initializing: ", target)
    const conn = connectToPi(target)
    return src("./virtual/" + target + "/*")
    .pipe(conn.dest("/home/pi"))
}

function cleanPi(target, cb){
    console.log("Cleaning: ", target)
    const conn = connectToPi(target)
    const targetDirectories = ["MyScripts", "MyPics"]
    for (const dir of targetDirectories){
        const path = '/home/pi/' + dir
        conn.rmdir(path, cb)
    }
}

function deployToPi(target){
    console.log("Deploying: ", target)
    return copyScriptsToPi(target)
}

function copyScriptsToPi(target){
    const conn = connectToPi(target)
    const globs = ['./virtual/' + target + '/MyScripts/**', './modules/util/*', 'project-settings.json']
    return src(globs)
        .pipe(conn.newer('/home/pi/MyScripts/'))
        .pipe(conn.dest('/home/pi/MyScripts/'))
}

// Final Tasks
// Only *inputPi for now. Will be later expanded with 'targetPiByArgs'

function testTask(cb){
    console.log("Gulp is set up correctly and ready to go!")
    cb()
}

function watchScripts(){
    watch("./virtual/**/*.py", parallel(deployToInputPi, deployToOutputPi))
}

function deployToInputPi(cb){
    return deployToPi('input-pi')
}

function initInputPi(cb){
    return initPi('input-pi')
}

function cleanInputPi(cb){
    cleanPi('input-pi', cb)
    cb()
}

function deployToOutputPi(cb){
    return deployToPi('output-pi')
}

function initOutputPi(cb){
    return initPi('output-pi')
}

function cleanOutputPi(cb){
    cleanPi('output-pi', cb)
    cb()
}

exports.default = series(
    parallel(cleanInputPi, cleanOutputPi), 
    parallel(initInputPi, initOutputPi), 
    parallel(deployToInputPi, deployToOutputPi), 
    watchScripts)
exports.test = testTask
exports.watch = watchScripts
exports.deploy = parallel(deployToInputPi, deployToOutputPi)
exports.init = parallel(initInputPi, initOutputPi)
exports.clean = parallel(cleanInputPi, cleanOutputPi)
//TODO: Make vargs "--input , --output"