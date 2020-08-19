const { 
    series, parallel, watch,
    src, dest} = require('gulp')
const settings = require('./project-settings.json')
const ftp = require('vinyl-ftp')
const merge = require('merge-stream')

function copyToPi(target){
    const conn = ftp.create({
        host:     settings[target].ip,
        user:     settings[target].user,
        password: settings[target].password,
    })

    return src('./virtual/' + target + '/MyScripts/**')
        .pipe(conn.newer('/home/pi/MyScripts/'))
        .pipe(conn.dest('/home/pi/MyScripts/'))
}

function cleanPi(target){
    //TODO: Clear files from directories
}

function deployToInputPi(cb){
   return copyToPi('input-pi')
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
