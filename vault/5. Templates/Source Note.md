<%*
let title = await tp.system.prompt("Note title");
if (!title) { title = tp.file.title; }
await tp.file.move("/2. Source Material/" + title);
-%>
Created: <% tp.date.now("YYYY-MM-DD HH:mm") %>
From: 
Date of source: 
Tags: 

# <% title %>
---
### Short Description

