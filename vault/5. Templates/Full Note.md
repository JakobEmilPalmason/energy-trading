<%*
let title = await tp.system.prompt("Note title");
if (!title) { title = tp.file.title; }
await tp.file.move("/6. Zettelkasten/" + title);
-%>
<% tp.date.now("YYYY-MM-DD") %> <% tp.date.now("HH:mm") %>

Tags: 

# <% title %>



## References
- Source: 
