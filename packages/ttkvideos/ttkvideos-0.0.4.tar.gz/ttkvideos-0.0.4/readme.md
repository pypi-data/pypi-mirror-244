# ttkvideos

tkVideo: Python module for playing videos (with sound) inside tkinter Label widget using Pillow and imageio works best &amp; fast on small size videos however takes few seconds of time for larger videos files Copyright © 2023 vishal sharma &nbsp
<Sharma659615@gmail.com>
<br>
<br>
<h3>Built With :</h3>
<ul>
<li>tkinter & CustomTkinter (Python built-in) </li>
<li>imageio</li>
<li>Pillow</li>
</ul>
<br>
<h3>Installation: </h3>
<p>The pip command to install ttkinter videos library for use </p>
<pre><code align="center"> pip install ttkvideos </code></pre>
This will create a shim between your code and the module binaries that gets updated every time you change your code.
&nbsp<b><u><h3>Usage : </h3></u></b>
<ul>
<li>Import tkinter and tkvideo-moviepy<br></li>
<li>Create Tk() parent and the label you'd like to use<br></li>
<li>Get a moviepy video<br></li>
<li>Create tkvideo object with its parameters(video_path, label_name,number of loops for the video if required and size of the video_screen)<br></li>
<li>Start the player thread with <player_name>.play()<br></li>
<li>Start the Tk mainloop<br></li>
</ul>
<h3>Examples</h3>
The given below is an example of the <code>'demo.py'</code> file to demonstrate the syntax :<br>
<ol>
<li><p> For Tkinter </p>
<pre lan="sh">
  import ttkvideos
  import tkinter as tk
  win=tk.Tk()
  label=tk.Label(win)
  label.pack()
  player=ttkvideos.Ttkvideos( %video_path% ,label,loop=1,(640,400))
  player.play()
  win.mainloop()
</pre>
</li>
<li>
<p> For Customtkinter </p>
<pre lan="sh">
  import ttkvideos
  import customtkinter as ctk
  win=ctk.Tk()
  label=ctk.Label(win)
  label.pack()
  player=ttkvideos.Ttkvideos( %video_path% ,label,loop=1,(640,400))
  player.play()
  win.mainloop()
</pre>
</li>
</ol>
<h3> Releases :</h3>
For the updated version <b><a href="https://github.com/Vishal24102002/ttkvideos/tree/main"><u> Latest </u></a></b> version.
<h3>License</h3>
Distributed under the MIT License. See <b><a href="https://github.com/Vishal24102002/ttkvideos/blob/main/Licence.txt"> LICENSE </a></b>for more information.
