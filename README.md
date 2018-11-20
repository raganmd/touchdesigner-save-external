# TouchDesigner Save External
*a simple save external tox and text helper*  
[matthew ragan](matthewragan.com)

## Summary
Working with git and TouchDesigner isn't always an easy process, but it's often an essential part of the process of tracking your work and collaborating with others. It also encourages you to begin thinking about how to make your projects and components more modular, portable, and reuseable. Those aren't always easy practices to embrace, but they make a big difference in the amount of time you invest in future projects. It's often hard to plan for the gig in six months when you're worried about the gig on Friday - and we all have those sprints or last minute changes. 

It's also worth remember that no framework will ever be perfect - all of these things change and evolve over time, and that's the very idea behind externalizing pieces of your project's code-base. An assembly of concise individually maintainable tools is often more maintainable than [rube golbergian](https://en.wikipedia.org/wiki/Rube_Goldberg) contraption - and while it's certainly less cool, it does make it easier to make deadlines.

So, what does all this have to do with saving external tox files? TOX files are the modules of TouchDesigner - they're component operators that can be saved as individual files and dropped into any network. These custom operators are made out of other operators. In 099 they can be set to be private if you have a pro license - keeping prying eyes away from your work (if you're worried about that).

That makes these components excellent candidates for externalization, but it takes a little extra work to keep them saved and sycned. In a perfect world we would use the same saving mechanism that's employed to save our TOE file to also save any external file, or better yet, to ask us if we want to externalize a file. That, in fact, is the aim of this TOX.

- - -
## Supported File Types
* `.tox`
* `.py`
* `.glsl`
* `.json`

In addition to externalizing tox files, it's often helpful to also externalize any files that can be dffed in git - that is any files you can compare meaningfully. When it comes to your version control tool, this means that you can track the changes you or a team member have made from one commit to another. Being able to see what changed over time can help you determine why one version works and another does not. Practically speaking, this usually comes in the form of python files, glsl, or json files. This little tool supports the above file types, and goes a little further. 

"What's further mean?" You ask - and I'm so glad you did. Furhter means that if you change this file outside of touch - say in a text editor like Sublime or Visual Studio Code, this TOX module will watch to see if that file has changed, and if it has pulse reload the operator that's referencing that file. Better still, if it's an extension, the `parent()` operator will have its extensions reinitialized. There's a little set-up and convention required there, but well worth it if you happen to use extension on a regular basis. 

# Parameters
![base save and pars](touchdesigner-save-external/assets/base_save_and_pars.PNG)  

### Extension Flag
The Extension Flag is the tag you will add to any text DAT that you're using as an extension. This ensures that we can easily identify which text DATs are being used as externally edited extensions, and reload both the contents of the DAT, as well reinitialize the extensions for the `parent()` operator. You can use any descriptor here that you like - I happen to think that something like `EXT` works well.

### Log to Texport
If you want to track when and where your external files are being saved, or if you're worried that something might be going wrong, you can turn on the `Logtotextport` parmeter to see the results of each save operation logged for easy view and tracking.

### Default Color
The default color is set as a read-only parameter used to reset the network worksheet background color. This is used in conjunction with the following two parameters to provide visual indicators for when a save or load operation has happened.

### BG Color
This is the color that the network background will flash when you externalize a TOX - it's the visual indicator that your tox has been sucessfully saved.

### Save Color
This is the color that the network background will flash save a text based file in an external editor - it's the visual indicator that your file has been reloaded.

### EXT Color
This is the color used to set the node color of your newly externalized tox - this can help ensure that at a glance you can tell which operators have been externalized.

### Version
The version number for this tool.

# Operation

### `reinitextensions.pulse()`
If you want to use this in conjunction with extensions, you'll need to follow a few conventions: 
* The text DAT that references an extension needs to be inside of the COMP uses it as an extension. For example - let's say you have a text DAT that holds an extension called `Project`, this needs to live inside of the COMP that is using it as an extension.
* The file you're editing needs to end in `.py`. This might seem obvious, but it's important that the file you're editing is a python file. There are a number of checks that happen to make sure that we don't just reinit COMPs willy nilly, and this is one of those safety measures. 
* The text DAT holding the extension needs to be tagged `EXT`. This makes sure that we don't just reinit the extensions of our parent every-time any .py file is saved, but only if the that file belongs is being read by a textDAT that's marked as being an extension.

### `ctrl+s`
The way you'll use this tox is just as if you were working as you might normally. Only, when you hit `ctrl + s`, if you're inside of a COMP that hasn't been saved externally, you'll be asked if you want to externalize that module. If you select `yes` you'll next be asked where you want to save that module. This module will then create a folder that has the same name as your component, and save the tox inside of that folder (the tox will also have the same name as the component). Better yet, this module will auto-populate the path to the external tox with the location you've selected. When you press `ctrl + s` again it will warn you that you're about to over-write your tox. If you confirm that you want to replace your tox, it will save the updated version right where your previous tox was located. 

### Using a text editor
If you're using a text editor for supported externalized files, than work as you normally might. When you save your file in your text editor Touch will automatically reload the file in Touch. If your text DAT is tagged `EXT` it will also reinit the extensions of the text DAT's `parent()`. 

- - -
## Suggested Workflow
At this point, you might have guess that this kind of approach works best in well structured projects. Some suggestions for organization and approach:
* Think about Order and Structure - while I've structured projects lots of different ways, it's worth finding a file structure that you like and sticking with it. That might be a deeply nested structure (watch out that'll bite you if you get too deep - at least on windows), or it might be something more flat. Regardless, think about a structure and stay with it.
* Make Small Simple Tools - to the best of your ability, try to make sure your modules are independent islands. That's not always possible, but if you can think carefully about creating dependencies, you'll be happier for it. Use custom parameters on your components to keep modules independent from one another. Use select operators, or In's and Out's to build connenctions. 
* Reuse that TOX - while this approach is fancy and fun, especially when working with git, it's also about making your future self happier. Thank carefully about how you might make something re-usable and portable to another project. THe more you can think through how to make pieces that can easily move from project to project the more time you can spend on the fun stuff... not on the pieces that are fussy and take lots of time.

- - -
## An Example Project
In the folder called `sample_project` open the `Sample_project.toe` to see how this might work. 

- - -
# Credits

[Material Design Icons by Google](https://material.io/tools/icons/?icon=save_alt&style=baseline)