<h1> Virtual Pi Architecture </h1>
<h2> How to work with 'virtual' and Gulp </h2>
<p> Virtual is used for deploy purposes. On initialization the content of virtual gets copied in their respective Pi.
This is achieved thanks to the 'gulp' task-runner. </p>
<p> <em>"Heil JavaScript and NodeJS environments ;)". </em> </p>
The folders in 'input-pi' get copied to the input pi and the folders in 'output-pi' get copied to the output pi</p>
<p> To use gulp type 'npx gulp' in the terminal.
Additionally the following commands are available: </p>
<ul>
    <li> 'init': The raspberry pis get initialized </li>
    <li> 'deploy': The scripts from virtual get copied to pi </li>
    <li> 'clean': The contents of the Raspberry folders get deleted </li>
    <li> 'watch': gulp sets up a watcher, that when a file gets changed deploys the changes directly to the respective pi </li>
</ul>
<p> These commands can be targeted to specific pis by adding '--input' or '--output' respectively. 
<em> However this feature is not fully implemented yet!</em></p>
<p> If you just use 'npx gulp' you start the default task, which runs 'clean', 'init', 'deploy' and 'watch' in series. </p>
<p> Additionally you can start the project by typing 'npm start' in the terminal </p>