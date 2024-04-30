<div class="jumbotron">
  <div class="container custom-container">
    <h1>LOLPython</h1>
    <p>You finally landed on the mainframe and are soooo close to hack the world! But what is this? A <a href="http://www.dalkescientific.com/writings/diary/archive/2007/06/01/lolpython.html">LOLPython</a> interpreter in production?
     Googling quickly reveals: Thats <a href="https://esolangs.org/wiki/Language_list">one of many esolangs</a> with hacker and l33t speak. Sounds cool, right?</p>
    <p>Though, to solve this challenge, you have to take it to the next level: Not only code a program in this weird language, but escape the interpreter and execute the final payload. Go exploit it!</p>
  </div>
</div>
<div class="container">
  <main role="main">
  <form>
    <p>Type your LOLPython code here. We'll execute your file and you'll get the result</p>
    <textarea placeholder="VISIBLE 'HAI WORLD!'" id="in">
</textarea>
    <input type="button" value="Transpile and Run!" id="rock-button" onclick="transpile();">

    <br>
    <p>Output:</p>
    <textarea id="output"></textarea>
    </form>
  </main>

</div>
<br><br>