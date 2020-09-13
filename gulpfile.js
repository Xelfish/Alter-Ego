const { 
    series, parallel, watch,
    src, dest} = require('gulp')
const settings = require('./project-settings.json')
const ftp = require('vinyl-ftp')
const merge = require('merge-stream')
const {argv} = require('yargs')

// Used to redirect tasks based on additional arguments, two input or output pi or both

function targetPiByArgs(task, cb){
    const hasArguments = Object.keys(argv).length > 2
    if (hasArguments){
        if (argv.in){
            return cb ?
                task('input-pi', cb)
                : task('input-pi')
        } else if (argv.out){
            return cb ? 
                task('output-pi', cb)
                : task ('output-pi')
        }
    } else {
        return cb ?
            parallel(task('input-pi', cb), task('output-pi', cb))
            : parallel(task('input-pi'), task('output-pi'))
    }
    cb()
}

// Tasks by Target

function connectToPi(target){
    const conn = ftp.create({
        host:     settings[target].ip,
        user:     settings[target].user,
        password: settings[target].password
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

function test(pi){
    console.log(pi)
}

// Final Tasks

function testTask(cb){
    console.log("This is a test output for Gulp. Everything seems to work fine!")
    targetPiByArgs(test)
    cb()
}

function watchScripts(){
    watch("./virtual/**/*.py", series(deployTask, watchScripts))
}

function deployTask(cb){
    return targetPiByArgs(deployToPi)
}

function initTask(cb){
    return targetPiByArgs(initPi)
}

function cleanTask(cb){
    targetPiByArgs(cleanPi, cb)
}

exports.test = testTask
exports.watch = watchScripts
exports.deploy = deployTask
exports.init = initTask
exports.clean = cleanTask

exports.default = series(cleanTask, initTask, deployTask, watchScripts)